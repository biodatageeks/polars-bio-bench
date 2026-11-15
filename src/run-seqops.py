"""Benchmark polars-bio's sequence operations against seqkit, seqfu, seqtk and
Biopython, end to end and file to file.

usage: python src/run-seqops.py conf/seqops/expressions.yaml --data-dir DIR
           [--work-dir DIR] [--results-dir results] [--repeats N]
           [--datasets a,b] [--tools a,b] [--benchmarks a,b] [--threads 1,8]

For every benchmark, dataset and input variant (BGZF and plain gzip) each tool
runs as a fresh subprocess, interleaved across repeats. Wall time is the best
of N runs; CPU time and peak RSS come from the same run. The first run of
every configuration passes through the correctness gate (seqops/check.py)
against the reference tool; mismatches are reported, never used as baselines.

Results go to results/seqops-<suite>-<date>/: runs.csv (every run),
summary.csv, benchmark_results.md and provenance.json.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import shutil
import sys
from collections import defaultdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from seqops import check, provenance, tools  # noqa: E402
from seqops.measure import run_measured  # noqa: E402

INPUT_SUFFIX = {
    ("fastq", "bgzf"): ".fastq.bgz",
    ("fastq", "gzip"): ".fastq.gz",
    ("fasta", "bgzf"): ".fa.bgz",
    ("fasta", "gzip"): ".fa.gz",
}


def parse_args():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("config")
    p.add_argument("--data-dir", required=True)
    p.add_argument("--work-dir", default=None, help="scratch space for outputs")
    p.add_argument("--results-dir", default="results")
    p.add_argument("--repeats", type=int)
    p.add_argument("--datasets")
    p.add_argument("--tools")
    p.add_argument("--benchmarks")
    p.add_argument("--threads")
    p.add_argument("--inputs", help="bgzf,gzip")
    p.add_argument("--timeout", type=float, default=7200)
    return p.parse_args()


def csv_list(value):
    return [v for v in value.split(",") if v] if value else None


def gate(op, kind, ref_out, ref_digest, out, tool):
    """(status, detail) for one output against the reference."""
    if op == "gc_qual":
        ok, detail = check.compare_gc_qual(ref_out, out, tool)
        return ("ok" if ok else "mismatch"), detail
    out_kind = "fasta" if op == "translate" else kind
    digest = check.fastx_digest(out, out_kind, tool)
    if digest == ref_digest:
        return "ok", f"{digest[0]} records"
    return "mismatch", f"{digest[0]} records, digest {digest[1][:12]} vs reference {ref_digest[1][:12]}"


def main():
    args = parse_args()
    conf = yaml.safe_load(open(args.config))
    suite = Path(args.config).stem
    repeats = args.repeats or conf.get("num_repeats", 3)
    thread_list = [int(t) for t in csv_list(args.threads) or conf.get("threads", [1, 2, 4, 8])]
    reference = conf.get("reference", "seqkit")
    data_dir = Path(os.path.expanduser(args.data_dir))
    work = Path(args.work_dir or data_dir / "_work")
    work.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M")
    res_dir = Path(args.results_dir) / f"seqops-{suite}-{stamp}"
    res_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(args.config, res_dir / Path(args.config).name)

    runs = []
    for bench in conf["benchmarks"]:
        if args.benchmarks and bench["name"] not in csv_list(args.benchmarks):
            continue
        op = bench["operation"]
        for ds_name in bench["datasets"]:
            if args.datasets and ds_name not in csv_list(args.datasets):
                continue
            ds = conf["datasets"][ds_name]
            kind = ds.get("kind", "fastq")
            for variant in csv_list(args.inputs) or bench.get("inputs", ["bgzf", "gzip"]):
                inp = data_dir / f"{ds.get('file', ds_name)}{INPUT_SUFFIX[(kind, variant)]}"
                if not inp.exists():
                    print(f"skip {bench['name']} {ds_name} {variant}: {inp} missing", flush=True)
                    continue
                tool_names = [
                    t for t in bench["tools"]
                    if (not args.tools or t in csv_list(args.tools))
                    and tools.supports(t, op)
                    and ds_name in bench.get("tool_datasets", {}).get(t, [ds_name])
                ]
                configs = []
                for t in tool_names:
                    for n in thread_list if t in tools.MULTI_THREADED else [1]:
                        configs.append((t, n))
                # The reference runs first, so later outputs can be checked.
                ref_cfg = (reference, 1)
                if ref_cfg not in configs:
                    configs.insert(0, ref_cfg)
                configs.remove(ref_cfg)
                ref_out = work / f"ref{tools.output_suffix(op)}"
                ref_digest = None
                status = {}
                for rep in range(repeats):
                    k = rep % max(len(configs), 1)
                    order = ([ref_cfg] if rep == 0 else []) + configs[k:] + configs[:k]
                    if rep > 0:
                        order.insert(rep % (len(order) + 1), ref_cfg)
                    for tool, n in order:
                        is_ref = (tool, n) == ref_cfg
                        out = ref_out if (is_ref and rep == 0) else work / f"out{tools.output_suffix(op)}"
                        argv, stdout_path = tools.command(tool, op, str(inp), str(out), n)
                        stdout_path = str(out) if stdout_path else None
                        m = run_measured(argv, stdout_path, timeout_s=args.timeout)
                        if m.returncode != 0:
                            st, detail = "error", m.stderr_tail.strip().splitlines()[-1:] or [""]
                            detail = detail[0][:300]
                        elif rep == 0 and is_ref:
                            if op != "gc_qual":
                                ref_digest = check.fastx_digest(
                                    str(out), "fasta" if op == "translate" else kind
                                )
                            st, detail = "reference", ""
                        elif (tool, n) not in status:
                            st, detail = gate(op, kind, str(ref_out), ref_digest, str(out), tool)
                        else:
                            st, detail = status[(tool, n)]
                        status.setdefault((tool, n), (st, detail))
                        row = {
                            "benchmark": bench["name"], "operation": op, "dataset": ds_name,
                            "input": variant, "tool": tool, "threads": n, "repeat": rep,
                            "wall_s": round(m.wall_s, 3), "cpu_s": round(m.cpu_s, 3),
                            "peak_rss_mb": round(m.peak_rss_mb, 1),
                            "status": status[(tool, n)][0], "detail": status[(tool, n)][1],
                            "command": " ".join(argv) + (f" > {stdout_path}" if stdout_path else ""),
                        }
                        runs.append(row)
                        print(
                            f"{row['benchmark']:10} {ds_name:14} {variant:4} {tool:10} t={n} r={rep} "
                            f"{m.wall_s:8.2f}s cpu={m.cpu_s:8.1f}s rss={m.peak_rss_mb:7.0f}MB {row['status']}",
                            flush=True,
                        )
                        if out != ref_out and out.exists():
                            out.unlink()
                if ref_out.exists():
                    ref_out.unlink()
                write_results(res_dir, runs, args.data_dir)
    write_results(res_dir, runs, args.data_dir)
    print(f"results: {res_dir}")


def summarise(runs):
    groups = defaultdict(list)
    for r in runs:
        groups[(r["benchmark"], r["dataset"], r["input"], r["tool"], r["threads"])].append(r)
    summary = []
    for (b, d, i, t, n), rs in groups.items():
        best = min(rs, key=lambda r: r["wall_s"])
        summary.append({
            "benchmark": b, "dataset": d, "input": i, "tool": t, "threads": n,
            "best_wall_s": best["wall_s"], "cpu_s": best["cpu_s"],
            "peak_rss_mb": max(r["peak_rss_mb"] for r in rs),
            "runs": len(rs), "status": rs[0]["status"], "detail": rs[0]["detail"],
        })
    return summary


def markdown(summary):
    lines = []
    by_case = defaultdict(list)
    for s in summary:
        by_case[(s["benchmark"], s["dataset"], s["input"])].append(s)
    for (b, d, i), rows in by_case.items():
        tools_ = sorted({r["tool"] for r in rows}, key=lambda t: (t != "polars_bio", t))
        threads = sorted({r["threads"] for r in rows})
        cell = {(r["tool"], r["threads"]): r for r in rows}
        lines += [f"### {b} — {d} ({i})", "",
                  "| threads | " + " | ".join(tools_) + " |",
                  "|---|" + "---|" * len(tools_)]
        for n in threads:
            vals = []
            for t in tools_:
                r = cell.get((t, n)) or (cell.get((t, 1)) if t not in tools.MULTI_THREADED else None)
                if not r:
                    vals.append("—")
                    continue
                mark = "" if r["status"] in ("ok", "reference") else f" **{r['status']}**"
                single = "†" if t not in tools.MULTI_THREADED else ""
                vals.append(f"{r['best_wall_s']:.2f} s / {r['cpu_s']:.1f} CPU-s / {r['peak_rss_mb']:.0f} MB{single}{mark}")
            lines.append(f"| {n} | " + " | ".join(vals) + " |")
        lines.append("")
    lines.append("Wall = best of N runs; CPU-s and peak RSS from that run. † single-threaded tool, run once.")
    return "\n".join(lines)


def write_results(res_dir, runs, data_dir):
    if not runs:
        return
    with open(res_dir / "runs.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(runs[0]))
        w.writeheader()
        w.writerows(runs)
    summary = summarise(runs)
    with open(res_dir / "summary.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(summary[0]))
        w.writeheader()
        w.writerows(summary)
    (res_dir / "benchmark_results.md").write_text(markdown(summary) + "\n")
    prov = res_dir / "provenance.json"
    if not prov.exists():
        prov.write_text(json.dumps({
            "date": dt.datetime.now().isoformat(timespec="seconds"),
            "command": " ".join(sys.argv),
            "machine": provenance.machine(),
            "versions": provenance.tool_versions(),
            "datasets": provenance.dataset_checksums(os.path.expanduser(data_dir)),
        }, indent=2) + "\n")


if __name__ == "__main__":
    main()
