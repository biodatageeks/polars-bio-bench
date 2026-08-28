#!/usr/bin/env python3
"""Regenerate RESULTS.md from the per-round CSVs in this directory.

    python3 results/coordinate-systems-pr222/analyze.py > RESULTS.md

Each `<build>-round<N>.csv` holds one round of
`conf/benchmark-coordinate-systems.yaml`: every operation, both coordinate
systems, every test case. The builds are

  A  polars-bio master on datafusion-bio-function-ranges v0.18.0 (pre-fix)
  E  the same tree on the released v0.19.1
  C  intermediate branch build, before the subtract hoist
  D  intermediate branch build, before the complement view-clipping fix

`overlap`, `merge` and `cluster` are untouched by the change, so their delta
measures machine drift and the treated operations are reported net of it.
"""

import collections
import csv
import pathlib
import statistics

STAT = "min"  # min over the in-run repeats: robust to transient contention
CONTROL = {"overlap", "merge", "cluster"}
HERE = pathlib.Path(__file__).parent


def load(paths):
    values, rows = collections.defaultdict(list), {}
    for path in paths:
        for record in csv.DictReader(open(path)):
            if record["library"] != "polars_bio":
                continue
            key = (
                record["operation"],
                record["coordinate_system"],
                record["test_case"],
            )
            values[key].append(float(record[STAT]))
            rows[key] = record["rows_returned"]
    return values, rows


def section(title, a_rounds, b_rounds, label, prefix_a="A", prefix_b="E"):
    a_values, a_rows = load(HERE / f"{prefix_a}-round{r}.csv" for r in a_rounds)
    b_values, b_rows = load(HERE / f"{prefix_b}-round{r}.csv" for r in b_rounds)
    print(f"\n## {title}\n")
    for system in ("0-based", "1-based"):
        control, treated = {}, {}
        for key in sorted(set(a_values) & set(b_values)):
            if key[1] != system:
                continue
            before = statistics.median(a_values[key])
            after = statistics.median(b_values[key])
            delta = (after - before) / before * 100
            (control if key[0] in CONTROL else treated)[key] = delta
        drift = statistics.median(control.values())
        print(f"### {system}\n")
        print(
            f"Machine drift from the untouched control ops: **{drift:+.1f}%** "
            f"(n={len(control)}, {min(control.values()):+.1f}%.."
            f"{max(control.values()):+.1f}%).\n"
        )
        print(f"| op | case | before (s) | {label} (s) | raw | drift-adjusted | rows |")
        print("|---|---|---|---|---|---|---|")
        for key in sorted(treated):
            before = statistics.median(a_values[key])
            after = statistics.median(b_values[key])
            same = a_rows.get(key) == b_rows.get(key)
            rows = "same" if same else f"{int(b_rows[key]) - int(a_rows[key]):+,}"
            print(
                f"| {key[0]} | {key[2]} | {before:.4f} | {after:.4f} | "
                f"{treated[key]:+.1f}% | **{treated[key] - drift:+.1f}%** | {rows} |"
            )
        adjusted = [d - drift for d in treated.values()]
        without_87 = [d - drift for k, d in treated.items() if k[2] != "8-7"]
        print(
            f"\n**n={len(adjusted)} — median {statistics.median(adjusted):+.1f}%, "
            f"mean {statistics.mean(adjusted):+.1f}%, "
            f"range {min(adjusted):+.1f}%..{max(adjusted):+.1f}%**"
        )
        print(
            f"\nExcluding the unreliable `8-7` case: n={len(without_87)}, median "
            f"{statistics.median(without_87):+.1f}%, worst {max(without_87):+.1f}%.\n"
        )


HEADER = """# Coordinate-system A/B — datafusion-bio-functions v0.19.1

Does making the range operations coordinate-aware cost anything?

* **A** — polars-bio `master` (0.35.0) on `datafusion-bio-function-ranges`
  **v0.18.0**, before the fixes.
* **E** — the same tree on the released **v0.19.1**, which carries
  biodatageeks/datafusion-bio-functions#220, #221 and #222. This is the shipped
  artifact, built from a plain tag with no local patch.
* **C**, **D** — intermediate branch builds, kept because they are the evidence
  for the `subtract` regression described below.

All built from the same source tree and commit, `--release` with
`RUSTFLAGS="-C target-cpu=native"`; the ranges crate version is the only delta.
macOS arm64, `conf/benchmark-coordinate-systems.yaml`, `databio` dataset.

## Data layout

One CSV per build per round — `<build>-round<N>.csv` — each holding every
operation, both coordinate systems and every test case for that round.
Regenerate this file with:

```
python3 results/coordinate-systems-pr222/analyze.py > results/coordinate-systems-pr222/RESULTS.md
```

## Method

Rounds run both builds back to back with the run **order reversed** between
rounds so ordering bias cancels (rounds 9 and 11 run A first, 10 and 12 run E
first). 7 in-run repeats per case per round; the statistic is the **min** of
those, pooled across rounds by median — min is robust to transient contention in
a way the mean is not.

`overlap`, `merge` and `cluster` are untouched by the change, so their delta
measures **machine drift**; treated operations are reported net of it.

Both controls earned their keep. Before order-balancing, four small-case
measurements looked like regressions and flipped sign the moment the order
reversed. And the control ops are what identify the `8-7` test case as
unreliable on this machine — see below."""

CONCLUSION = """
## Conclusion

**No regression on either coordinate path.** Drift-adjusted medians are -1.0%
(0-based) and -0.9% (1-based). `subtract` is materially faster, about **-23%**
on the 0-based 7-3/7-8 cases.

### The `8-7` case is not measurable on this machine

`nearest 8-7` shows +6.4% on the 0-based path, and it is noise rather than a
regression. Per-round it swings +6.8 / +8.7 / +8.4 / -10.1%, with no relation to
run order. The proof is the control: `overlap 8-7` — code this change does not
touch — swings -1.6 / +5.1 / +1.8 / **-44.7%** over the same four rounds. `8-7`
is the largest input in the suite and its timings here are dominated by
page-cache and thermal state.

Dropping that one case moves the 0-based worst case from +6.4% to **+1.9%** and
leaves the medians unchanged, so no conclusion depends on it either way.

By contrast `subtract 7-3` reads -21.8 / -23.2 / -21.1 / -24.0% across the same
rounds — that is what an order-independent, real effect looks like.

### Where the speed-up came from

The first patched build genuinely *regressed* `subtract` — +9% on 0-based and
+18% on 1-based, reproducible across interleaved rounds and with byte-identical
row counts, so code-path cost rather than extra work. `this.strict` is read
inside the emit loop between `this.*_builder` writes through the same
`&mut self`, so it cannot stay in a register and is reloaded every iteration;
the change added two more reads and tipped it. Hoisting it into a local fixed
that and removed the two reads the loop already had, leaving `subtract` faster
than before. The `C-round*` files are that measurement.

## Correctness evidence from the same runs

Row counts are **byte-identical on the 0-based path** for every operation and
case, independently confirming that path is untouched.

On the 1-based path v0.19.1 returns **fewer** rows, exactly where it stops
emitting zero-length fragments that were previously produced in error —
`complement 5-1` alone sheds 150,413 spurious rows."""

if __name__ == "__main__":
    print(HEADER)
    section(
        "Released v0.19.1 vs pre-fix — rounds 9-12, order-balanced",
        (9, 10, 11, 12),
        (9, 10, 11, 12),
        "v0.19.1",
    )
    print(CONCLUSION)
    section(
        "Intermediate build (D, before the complement view-clipping fix) — rounds 7-8",
        (7, 8),
        (7, 8),
        "D",
        prefix_b="D",
    )
    section(
        "Intermediate build (C, before the subtract hoist) — rounds 3-6",
        (3, 4, 5, 6),
        (3, 4, 5, 6),
        "C",
        prefix_b="C",
    )
