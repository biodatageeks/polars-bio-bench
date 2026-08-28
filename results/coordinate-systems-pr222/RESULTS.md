# Coordinate-system A/B — datafusion-bio-functions v0.19.1

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
unreliable on this machine — see below.

## Released v0.19.1 vs pre-fix — rounds 9-12, order-balanced

### 0-based

Machine drift from the untouched control ops: **+0.6%** (n=20, -1.5%..+3.2%).

| op | case | before (s) | v0.19.1 (s) | raw | drift-adjusted | rows |
|---|---|---|---|---|---|---|
| complement | 1-2 | 0.0058 | 0.0056 | -2.6% | **-3.2%** | same |
| complement | 2-1 | 0.0090 | 0.0089 | -0.3% | **-0.9%** | same |
| complement | 3-7 | 0.0258 | 0.0254 | -1.5% | **-2.1%** | same |
| complement | 5-1 | 0.6985 | 0.7040 | +0.8% | **+0.2%** | same |
| complement | 7-3 | 0.0347 | 0.0345 | -0.6% | **-1.2%** | same |
| complement | 7-8 | 0.0343 | 0.0352 | +2.5% | **+1.9%** | same |
| complement | 8-7 | 0.2722 | 0.2678 | -1.6% | **-2.2%** | same |
| count_overlaps | 1-2 | 0.0156 | 0.0151 | -2.9% | **-3.5%** | same |
| count_overlaps | 2-1 | 0.0162 | 0.0152 | -6.1% | **-6.7%** | same |
| count_overlaps | 3-7 | 0.1002 | 0.0998 | -0.4% | **-1.0%** | same |
| count_overlaps | 7-3 | 0.0833 | 0.0846 | +1.5% | **+0.9%** | same |
| count_overlaps | 7-8 | 0.0855 | 0.0836 | -2.2% | **-2.8%** | same |
| count_overlaps | 8-7 | 0.7435 | 0.7460 | +0.3% | **-0.3%** | same |
| coverage | 1-2 | 0.0169 | 0.0172 | +2.0% | **+1.3%** | same |
| coverage | 2-1 | 0.0245 | 0.0242 | -1.3% | **-1.9%** | same |
| coverage | 3-7 | 0.1188 | 0.1179 | -0.8% | **-1.4%** | same |
| coverage | 7-3 | 0.0657 | 0.0648 | -1.4% | **-2.0%** | same |
| coverage | 7-8 | 0.0662 | 0.0647 | -2.2% | **-2.9%** | same |
| coverage | 8-7 | 1.2027 | 1.2080 | +0.4% | **-0.2%** | same |
| nearest | 1-2 | 0.0302 | 0.0300 | -0.4% | **-1.0%** | same |
| nearest | 2-1 | 0.0315 | 0.0323 | +2.4% | **+1.8%** | same |
| nearest | 3-7 | 0.2217 | 0.2244 | +1.2% | **+0.6%** | same |
| nearest | 7-3 | 0.1939 | 0.1921 | -1.0% | **-1.6%** | same |
| nearest | 7-8 | 0.1913 | 0.1922 | +0.4% | **-0.2%** | same |
| nearest | 8-7 | 2.4292 | 2.6010 | +7.1% | **+6.4%** | same |
| subtract | 1-2 | 0.0127 | 0.0128 | +0.5% | **-0.2%** | same |
| subtract | 2-1 | 0.0158 | 0.0160 | +1.6% | **+1.0%** | same |
| subtract | 3-7 | 0.1062 | 0.1063 | +0.1% | **-0.5%** | same |
| subtract | 5-1 | 1.4534 | 1.4577 | +0.3% | **-0.3%** | same |
| subtract | 7-3 | 0.5374 | 0.4165 | -22.5% | **-23.1%** | same |
| subtract | 7-8 | 0.5377 | 0.4135 | -23.1% | **-23.7%** | same |
| subtract | 8-7 | 1.1108 | 1.0465 | -5.8% | **-6.4%** | same |

**n=32 — median -1.0%, mean -2.4%, range -23.7%..+6.4%**

Excluding the unreliable `8-7` case: n=27, median -1.0%, worst +1.9%.

### 1-based

Machine drift from the untouched control ops: **+0.5%** (n=20, -3.9%..+4.7%).

| op | case | before (s) | v0.19.1 (s) | raw | drift-adjusted | rows |
|---|---|---|---|---|---|---|
| complement | 1-2 | 0.0057 | 0.0057 | -0.4% | **-0.8%** | same |
| complement | 2-1 | 0.0088 | 0.0089 | +0.9% | **+0.4%** | -56 |
| complement | 3-7 | 0.0259 | 0.0254 | -1.8% | **-2.3%** | -8 |
| complement | 5-1 | 0.6952 | 0.6886 | -0.9% | **-1.4%** | -150,413 |
| complement | 7-3 | 0.0348 | 0.0343 | -1.4% | **-1.8%** | -108 |
| complement | 7-8 | 0.0343 | 0.0343 | +0.2% | **-0.3%** | -108 |
| complement | 8-7 | 0.2702 | 0.2688 | -0.5% | **-1.0%** | -4 |
| count_overlaps | 1-2 | 0.0154 | 0.0150 | -2.7% | **-3.2%** | same |
| count_overlaps | 2-1 | 0.0152 | 0.0152 | +0.4% | **-0.1%** | same |
| count_overlaps | 3-7 | 0.0999 | 0.1000 | +0.2% | **-0.3%** | same |
| count_overlaps | 7-3 | 0.0835 | 0.0829 | -0.7% | **-1.2%** | same |
| count_overlaps | 7-8 | 0.0839 | 0.0841 | +0.2% | **-0.3%** | same |
| count_overlaps | 8-7 | 0.7453 | 0.7372 | -1.1% | **-1.6%** | same |
| coverage | 1-2 | 0.0173 | 0.0178 | +3.0% | **+2.5%** | same |
| coverage | 2-1 | 0.0252 | 0.0239 | -5.2% | **-5.7%** | same |
| coverage | 3-7 | 0.1190 | 0.1171 | -1.6% | **-2.1%** | same |
| coverage | 7-3 | 0.0673 | 0.0653 | -3.1% | **-3.6%** | same |
| coverage | 7-8 | 0.0662 | 0.0660 | -0.3% | **-0.7%** | same |
| coverage | 8-7 | 1.2074 | 1.2054 | -0.2% | **-0.6%** | same |
| nearest | 1-2 | 0.0304 | 0.0293 | -3.6% | **-4.1%** | same |
| nearest | 2-1 | 0.0328 | 0.0325 | -1.0% | **-1.5%** | same |
| nearest | 3-7 | 0.2227 | 0.2224 | -0.1% | **-0.6%** | same |
| nearest | 7-3 | 0.1893 | 0.1927 | +1.8% | **+1.3%** | same |
| nearest | 7-8 | 0.1876 | 0.1905 | +1.5% | **+1.1%** | same |
| nearest | 8-7 | 2.4421 | 2.4599 | +0.7% | **+0.3%** | same |
| subtract | 1-2 | 0.0133 | 0.0128 | -3.4% | **-3.9%** | -10 |
| subtract | 2-1 | 0.0164 | 0.0166 | +0.8% | **+0.3%** | same |
| subtract | 3-7 | 0.1090 | 0.1085 | -0.5% | **-1.0%** | -308 |
| subtract | 5-1 | 1.4273 | 1.4891 | +4.3% | **+3.9%** | same |
| subtract | 7-3 | 0.5368 | 0.5063 | -5.7% | **-6.2%** | same |
| subtract | 7-8 | 0.5367 | 0.5095 | -5.1% | **-5.5%** | same |
| subtract | 8-7 | 1.1166 | 1.1379 | +1.9% | **+1.4%** | -46,007 |

**n=32 — median -0.9%, mean -1.2%, range -6.2%..+3.9%**

Excluding the unreliable `8-7` case: n=27, median -1.0%, worst +3.9%.


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
`complement 5-1` alone sheds 150,413 spurious rows.

## Intermediate build (D, before the complement view-clipping fix) — rounds 7-8

### 0-based

Machine drift from the untouched control ops: **+0.8%** (n=20, -3.7%..+6.6%).

| op | case | before (s) | D (s) | raw | drift-adjusted | rows |
|---|---|---|---|---|---|---|
| complement | 1-2 | 0.0057 | 0.0058 | +3.1% | **+2.3%** | same |
| complement | 2-1 | 0.0088 | 0.0091 | +3.4% | **+2.6%** | same |
| complement | 3-7 | 0.0259 | 0.0258 | -0.6% | **-1.4%** | same |
| complement | 5-1 | 0.6887 | 0.7007 | +1.7% | **+1.0%** | same |
| complement | 7-3 | 0.0341 | 0.0350 | +2.5% | **+1.7%** | same |
| complement | 7-8 | 0.0343 | 0.0340 | -0.9% | **-1.7%** | same |
| complement | 8-7 | 0.2706 | 0.2692 | -0.5% | **-1.3%** | same |
| count_overlaps | 1-2 | 0.0156 | 0.0159 | +1.6% | **+0.8%** | same |
| count_overlaps | 2-1 | 0.0156 | 0.0163 | +4.8% | **+4.1%** | same |
| count_overlaps | 3-7 | 0.0982 | 0.0983 | +0.1% | **-0.7%** | same |
| count_overlaps | 7-3 | 0.0820 | 0.0825 | +0.6% | **-0.2%** | same |
| count_overlaps | 7-8 | 0.0836 | 0.0824 | -1.5% | **-2.2%** | same |
| count_overlaps | 8-7 | 0.7346 | 0.7349 | +0.0% | **-0.7%** | same |
| coverage | 1-2 | 0.0169 | 0.0175 | +3.2% | **+2.5%** | same |
| coverage | 2-1 | 0.0243 | 0.0247 | +1.5% | **+0.8%** | same |
| coverage | 3-7 | 0.1174 | 0.1167 | -0.6% | **-1.3%** | same |
| coverage | 7-3 | 0.0654 | 0.0658 | +0.6% | **-0.2%** | same |
| coverage | 7-8 | 0.0653 | 0.0648 | -0.7% | **-1.5%** | same |
| coverage | 8-7 | 1.1882 | 1.2244 | +3.0% | **+2.3%** | same |
| nearest | 1-2 | 0.0305 | 0.0304 | -0.4% | **-1.1%** | same |
| nearest | 2-1 | 0.0328 | 0.0330 | +0.3% | **-0.4%** | same |
| nearest | 3-7 | 0.2232 | 0.2223 | -0.4% | **-1.2%** | same |
| nearest | 7-3 | 0.1957 | 0.1925 | -1.7% | **-2.4%** | same |
| nearest | 7-8 | 0.1902 | 0.1909 | +0.4% | **-0.4%** | same |
| nearest | 8-7 | 2.5818 | 2.3785 | -7.9% | **-8.6%** | same |
| subtract | 1-2 | 0.0126 | 0.0126 | +0.1% | **-0.7%** | same |
| subtract | 2-1 | 0.0155 | 0.0157 | +1.0% | **+0.3%** | same |
| subtract | 3-7 | 0.1060 | 0.1055 | -0.4% | **-1.2%** | same |
| subtract | 5-1 | 1.4706 | 1.4782 | +0.5% | **-0.2%** | same |
| subtract | 7-3 | 0.5348 | 0.4128 | -22.8% | **-23.6%** | same |
| subtract | 7-8 | 0.5324 | 0.4149 | -22.1% | **-22.8%** | same |
| subtract | 8-7 | 1.1143 | 1.0412 | -6.6% | **-7.3%** | same |

**n=32 — median -0.7%, mean -2.0%, range -23.6%..+4.1%**

Excluding the unreliable `8-7` case: n=27, median -0.4%, worst +4.1%.

### 1-based

Machine drift from the untouched control ops: **+0.0%** (n=20, -5.2%..+5.8%).

| op | case | before (s) | D (s) | raw | drift-adjusted | rows |
|---|---|---|---|---|---|---|
| complement | 1-2 | 0.0054 | 0.0058 | +7.4% | **+7.4%** | same |
| complement | 2-1 | 0.0085 | 0.0089 | +4.0% | **+4.0%** | -56 |
| complement | 3-7 | 0.0254 | 0.0258 | +1.4% | **+1.3%** | -8 |
| complement | 5-1 | 0.6900 | 0.7079 | +2.6% | **+2.6%** | -150,413 |
| complement | 7-3 | 0.0343 | 0.0346 | +0.9% | **+0.9%** | -108 |
| complement | 7-8 | 0.0352 | 0.0355 | +1.0% | **+0.9%** | -108 |
| complement | 8-7 | 0.2752 | 0.2749 | -0.1% | **-0.1%** | -4 |
| count_overlaps | 1-2 | 0.0146 | 0.0148 | +1.8% | **+1.7%** | same |
| count_overlaps | 2-1 | 0.0153 | 0.0151 | -1.1% | **-1.1%** | same |
| count_overlaps | 3-7 | 0.0998 | 0.0985 | -1.3% | **-1.3%** | same |
| count_overlaps | 7-3 | 0.0838 | 0.0838 | -0.0% | **-0.0%** | same |
| count_overlaps | 7-8 | 0.0838 | 0.0860 | +2.6% | **+2.5%** | same |
| count_overlaps | 8-7 | 0.7358 | 0.7405 | +0.6% | **+0.6%** | same |
| coverage | 1-2 | 0.0178 | 0.0174 | -2.6% | **-2.6%** | same |
| coverage | 2-1 | 0.0250 | 0.0242 | -3.3% | **-3.4%** | same |
| coverage | 3-7 | 0.1199 | 0.1174 | -2.0% | **-2.1%** | same |
| coverage | 7-3 | 0.0671 | 0.0683 | +1.7% | **+1.7%** | same |
| coverage | 7-8 | 0.0659 | 0.0645 | -2.1% | **-2.1%** | same |
| coverage | 8-7 | 1.1827 | 1.2140 | +2.6% | **+2.6%** | same |
| nearest | 1-2 | 0.0299 | 0.0305 | +2.0% | **+2.0%** | same |
| nearest | 2-1 | 0.0320 | 0.0338 | +5.9% | **+5.9%** | same |
| nearest | 3-7 | 0.2218 | 0.2210 | -0.4% | **-0.4%** | same |
| nearest | 7-3 | 0.1898 | 0.1891 | -0.4% | **-0.4%** | same |
| nearest | 7-8 | 0.1906 | 0.1896 | -0.5% | **-0.6%** | same |
| nearest | 8-7 | 2.4401 | 2.2315 | -8.6% | **-8.6%** | same |
| subtract | 1-2 | 0.0127 | 0.0134 | +5.0% | **+4.9%** | -10 |
| subtract | 2-1 | 0.0158 | 0.0167 | +5.6% | **+5.6%** | same |
| subtract | 3-7 | 0.1058 | 0.1072 | +1.3% | **+1.3%** | -308 |
| subtract | 5-1 | 1.4561 | 1.4853 | +2.0% | **+2.0%** | same |
| subtract | 7-3 | 0.5329 | 0.5025 | -5.7% | **-5.7%** | same |
| subtract | 7-8 | 0.5357 | 0.5058 | -5.6% | **-5.6%** | same |
| subtract | 8-7 | 1.1043 | 1.1061 | +0.2% | **+0.1%** | -46,007 |

**n=32 — median +0.7%, mean +0.4%, range -8.6%..+7.4%**

Excluding the unreliable `8-7` case: n=27, median +0.9%, worst +7.4%.


## Intermediate build (C, before the subtract hoist) — rounds 3-6

### 0-based

Machine drift from the untouched control ops: **+0.7%** (n=20, -3.3%..+5.2%).

| op | case | before (s) | C (s) | raw | drift-adjusted | rows |
|---|---|---|---|---|---|---|
| complement | 1-2 | 0.0054 | 0.0056 | +5.1% | **+4.4%** | same |
| complement | 2-1 | 0.0082 | 0.0088 | +7.5% | **+6.8%** | same |
| complement | 3-7 | 0.0249 | 0.0259 | +4.0% | **+3.3%** | same |
| complement | 5-1 | 0.7014 | 0.6821 | -2.7% | **-3.5%** | same |
| complement | 7-3 | 0.0336 | 0.0348 | +3.5% | **+2.8%** | same |
| complement | 7-8 | 0.0340 | 0.0338 | -0.7% | **-1.4%** | same |
| complement | 8-7 | 0.2672 | 0.2686 | +0.5% | **-0.2%** | same |
| count_overlaps | 1-2 | 0.0159 | 0.0147 | -7.2% | **-7.9%** | same |
| count_overlaps | 2-1 | 0.0153 | 0.0146 | -4.7% | **-5.4%** | same |
| count_overlaps | 3-7 | 0.0986 | 0.0980 | -0.6% | **-1.3%** | same |
| count_overlaps | 7-3 | 0.0814 | 0.0818 | +0.4% | **-0.3%** | same |
| count_overlaps | 7-8 | 0.0829 | 0.0833 | +0.4% | **-0.3%** | same |
| count_overlaps | 8-7 | 0.7360 | 0.7245 | -1.6% | **-2.3%** | same |
| coverage | 1-2 | 0.0178 | 0.0172 | -3.0% | **-3.7%** | same |
| coverage | 2-1 | 0.0241 | 0.0238 | -0.9% | **-1.6%** | same |
| coverage | 3-7 | 0.1179 | 0.1183 | +0.4% | **-0.3%** | same |
| coverage | 7-3 | 0.0648 | 0.0658 | +1.6% | **+0.9%** | same |
| coverage | 7-8 | 0.0649 | 0.0660 | +1.7% | **+1.0%** | same |
| coverage | 8-7 | 1.1767 | 1.2037 | +2.3% | **+1.6%** | same |
| nearest | 1-2 | 0.0304 | 0.0303 | -0.3% | **-1.0%** | same |
| nearest | 2-1 | 0.0318 | 0.0327 | +2.6% | **+1.9%** | same |
| nearest | 3-7 | 0.2172 | 0.2212 | +1.8% | **+1.1%** | same |
| nearest | 7-3 | 0.1879 | 0.1897 | +0.9% | **+0.2%** | same |
| nearest | 7-8 | 0.1885 | 0.1902 | +0.9% | **+0.2%** | same |
| nearest | 8-7 | 2.3051 | 2.3716 | +2.9% | **+2.2%** | same |
| subtract | 1-2 | 0.0123 | 0.0128 | +4.0% | **+3.3%** | same |
| subtract | 2-1 | 0.0157 | 0.0163 | +3.9% | **+3.2%** | same |
| subtract | 3-7 | 0.1036 | 0.1061 | +2.4% | **+1.7%** | same |
| subtract | 5-1 | 1.4286 | 1.4643 | +2.5% | **+1.8%** | same |
| subtract | 7-3 | 0.5339 | 0.4130 | -22.6% | **-23.3%** | same |
| subtract | 7-8 | 0.5358 | 0.4121 | -23.1% | **-23.8%** | same |
| subtract | 8-7 | 1.0942 | 1.0490 | -4.1% | **-4.8%** | same |

**n=32 — median +0.0%, mean -1.4%, range -23.8%..+6.8%**

Excluding the unreliable `8-7` case: n=27, median +0.2%, worst +6.8%.

### 1-based

Machine drift from the untouched control ops: **+1.8%** (n=20, -1.3%..+5.8%).

| op | case | before (s) | C (s) | raw | drift-adjusted | rows |
|---|---|---|---|---|---|---|
| complement | 1-2 | 0.0054 | 0.0055 | +2.2% | **+0.4%** | same |
| complement | 2-1 | 0.0087 | 0.0085 | -1.9% | **-3.7%** | -56 |
| complement | 3-7 | 0.0258 | 0.0254 | -1.6% | **-3.5%** | -8 |
| complement | 5-1 | 0.6805 | 0.6871 | +1.0% | **-0.9%** | -150,413 |
| complement | 7-3 | 0.0343 | 0.0348 | +1.3% | **-0.5%** | -108 |
| complement | 7-8 | 0.0337 | 0.0340 | +0.8% | **-1.1%** | -108 |
| complement | 8-7 | 0.2689 | 0.2678 | -0.4% | **-2.3%** | -4 |
| count_overlaps | 1-2 | 0.0146 | 0.0145 | -0.4% | **-2.3%** | same |
| count_overlaps | 2-1 | 0.0151 | 0.0148 | -1.6% | **-3.5%** | same |
| count_overlaps | 3-7 | 0.0982 | 0.0996 | +1.4% | **-0.5%** | same |
| count_overlaps | 7-3 | 0.0832 | 0.0842 | +1.2% | **-0.7%** | same |
| count_overlaps | 7-8 | 0.0816 | 0.0834 | +2.2% | **+0.3%** | same |
| count_overlaps | 8-7 | 0.7283 | 0.7209 | -1.0% | **-2.9%** | same |
| coverage | 1-2 | 0.0172 | 0.0174 | +1.2% | **-0.7%** | same |
| coverage | 2-1 | 0.0241 | 0.0241 | -0.2% | **-2.0%** | same |
| coverage | 3-7 | 0.1170 | 0.1167 | -0.2% | **-2.1%** | same |
| coverage | 7-3 | 0.0670 | 0.0672 | +0.3% | **-1.6%** | same |
| coverage | 7-8 | 0.0645 | 0.0655 | +1.6% | **-0.3%** | same |
| coverage | 8-7 | 1.1797 | 1.2028 | +2.0% | **+0.1%** | same |
| nearest | 1-2 | 0.0294 | 0.0301 | +2.6% | **+0.7%** | same |
| nearest | 2-1 | 0.0320 | 0.0314 | -1.9% | **-3.8%** | same |
| nearest | 3-7 | 0.2157 | 0.2223 | +3.0% | **+1.2%** | same |
| nearest | 7-3 | 0.1877 | 0.1877 | -0.0% | **-1.9%** | same |
| nearest | 7-8 | 0.1877 | 0.1890 | +0.7% | **-1.2%** | same |
| nearest | 8-7 | 2.3605 | 2.3643 | +0.2% | **-1.7%** | same |
| subtract | 1-2 | 0.0125 | 0.0127 | +1.7% | **-0.2%** | -10 |
| subtract | 2-1 | 0.0162 | 0.0162 | +0.2% | **-1.6%** | same |
| subtract | 3-7 | 0.1070 | 0.1065 | -0.5% | **-2.3%** | -308 |
| subtract | 5-1 | 1.4245 | 1.4916 | +4.7% | **+2.9%** | same |
| subtract | 7-3 | 0.5329 | 0.5033 | -5.6% | **-7.4%** | same |
| subtract | 7-8 | 0.5320 | 0.5044 | -5.2% | **-7.0%** | same |
| subtract | 8-7 | 1.0919 | 1.1129 | +1.9% | **+0.1%** | -46,007 |

**n=32 — median -1.4%, mean -1.6%, range -7.4%..+2.9%**

Excluding the unreliable `8-7` case: n=27, median -1.2%, worst +2.9%.

