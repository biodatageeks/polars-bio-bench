"""Compare interval-operation performance between polars-bio builds.

Runs only polars-bio, with exactly the calls and session options that
run-benchmarks.py uses (operations.py ``*_polars_bio``, default parquet-path
input, ``polars.LazyFrame`` output consumed with ``select(pl.len())``), so a
build can be checked for regressions without installing the other tools.

usage (one build per virtualenv; the orchestrator interleaves them):
    python src/regression-polars-bio.py --one OP CASE THREADS --data-root DIR
    python src/regression-polars-bio.py --compare NAME=PYTHON [NAME=PYTHON ...]
        [--conf conf/benchmark-pull-request.yaml] [--threads 1,8] [--rounds 2]
        --data-root DIR

--compare prints a table of median wall time per build and the change
relative to the first build, and writes regression.csv / regression.md to
--out (default results/regression-<date>).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import statistics
import subprocess
import sys
import time
from pathlib import Path

import yaml

COLUMNS = ["contig", "pos_start", "pos_end"]
HERE = Path(__file__).resolve()


def one(op, case, threads, data_root, conf_common, repeats):
    import polars as pl

    import polars_bio as pb

    cases = {c["name"]: c for c in yaml.safe_load(open(conf_common))["test-cases"]}
    c = cases[case]
    ds = c.get("dataset", "databio")
    df1 = f"{data_root}/{ds}/{c['df_path_1']}"
    df2 = f"{data_root}/{ds}/{c['df_path_2']}"

    pb.set_option("datafusion.bio.coordinate_system_zero_based", "true")
    pb.set_option("datafusion.execution.target_partitions", str(threads))
    for key in ("repartition_joins", "repartition_file_scans"):
        pb.set_option(f"datafusion.optimizer.{key}", "false")
    pb.set_option("datafusion.execution.coalesce_batches", "false")
    try:
        pb.set_progress_bar(False)
    except AttributeError:
        pass

    def call():
        kw = dict(cols1=COLUMNS, cols2=COLUMNS, output_type="polars.LazyFrame")
        if op == "overlap":
            lf = pb.overlap(df1, df2, **kw)
        elif op == "nearest":
            lf = pb.nearest(df1, df2, **kw)
        elif op == "count_overlaps":
            lf = pb.count_overlaps(df1, df2, naive_query=True, **kw)
        elif op == "coverage":
            lf = pb.coverage(df1, df2, **kw)
        else:
            raise SystemExit(f"unknown op {op}")
        return int(lf.select(pl.len()).collect().item())

    rows = call()  # warm-up: file cache, lazy imports
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        n = call()
        times.append(time.perf_counter() - t0)
        assert n == rows, (n, rows)
    print(json.dumps({"rows": rows, "times": times, "version": pb.__version__}))


def compare(args):
    builds = [b.split("=", 1) for b in args.compare]
    conf = yaml.safe_load(open(args.conf))
    jobs = []
    for bench in conf["benchmarks"]:
        op = bench["operation"]
        if op not in ("overlap", "nearest", "count_overlaps", "coverage"):
            continue
        for case in bench["test-cases"]:
            for t in [int(x) for x in args.threads.split(",")]:
                jobs.append((op, case, t))
    out = Path(args.out or f"results/regression-{dt.datetime.now():%Y%m%d-%H%M}")
    out.mkdir(parents=True, exist_ok=True)
    results = {}
    for rnd in range(args.rounds):
        for j, (op, case, t) in enumerate(jobs):
            k = (j + rnd) % len(builds)
            for name, py in builds[k:] + builds[:k]:
                p = subprocess.run(
                    [py, str(HERE), "--one", op, case, str(t), "--data-root", args.data_root,
                     "--common", args.common, "--repeats", str(args.repeats)],
                    capture_output=True, text=True,
                )
                if p.returncode:
                    print(f"{name} {op} {case} t={t}: FAILED\n{p.stderr[-800:]}", file=sys.stderr)
                    continue
                r = json.loads(p.stdout.strip().splitlines()[-1])
                results.setdefault((op, case, t, name), {"rows": r["rows"], "times": [], "version": r["version"]})
                results[(op, case, t, name)]["times"] += r["times"]
                print(f"r{rnd} {op:15} {case:4} t={t} {name:10} median={statistics.median(r['times']):.3f}s rows={r['rows']}", flush=True)
    names = [n for n, _ in builds]
    lines = ["| operation | case | threads | " + " | ".join(names) + " | rows |",
             "|---|---|---|" + "---|" * (len(names) + 1)]
    rows_out = []
    for op, case, t in jobs:
        meds = {n: statistics.median(results[(op, case, t, n)]["times"]) for n in names if (op, case, t, n) in results}
        rows = {results[(op, case, t, n)]["rows"] for n in names if (op, case, t, n) in results}
        base = meds.get(names[0])
        cells = []
        for n in names:
            if n not in meds:
                cells.append("failed")
            elif n == names[0] or not base:
                cells.append(f"{meds[n]:.3f} s")
            else:
                cells.append(f"{meds[n]:.3f} s ({(meds[n] / base - 1) * 100:+.1f}%)")
        flag = "" if len(rows) == 1 else " **rows differ**"
        lines.append(f"| {op} | {case} | {t} | " + " | ".join(cells) + f" | {', '.join(map(str, sorted(rows)))}{flag} |")
        rows_out.append({"operation": op, "case": case, "threads": t, **{f"{n}_median_s": meds.get(n) for n in names}, "rows": sorted(rows)})
    versions = {n: results[next(k for k in results if k[3] == n)]["version"] for n in names if any(k[3] == n for k in results)}
    md = "\n".join(lines) + f"\n\nMedian of {args.repeats} runs × {args.rounds} rounds after a warm-up; builds: {json.dumps(versions)}\n"
    (out / "regression.md").write_text(md)
    with open(out / "regression.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows_out[0]))
        w.writeheader()
        w.writerows(rows_out)
    print(md)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--one", nargs=3, metavar=("OP", "CASE", "THREADS"))
    p.add_argument("--compare", nargs="+", metavar="NAME=PYTHON")
    p.add_argument("--data-root", default=os.getenv("BENCH_DATA_ROOT"))
    p.add_argument("--conf", default=str(HERE.parent.parent / "conf/benchmark-pull-request.yaml"))
    p.add_argument("--common", default=str(HERE.parent.parent / "conf/common.yaml"))
    p.add_argument("--threads", default="1,8")
    p.add_argument("--rounds", type=int, default=2)
    p.add_argument("--repeats", type=int, default=5)
    p.add_argument("--out")
    a = p.parse_args()
    if a.one:
        one(a.one[0], a.one[1], int(a.one[2]), a.data_root, a.common, a.repeats)
    else:
        compare(a)
