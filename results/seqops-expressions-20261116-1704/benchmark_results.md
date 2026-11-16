### revcomp — DRR013000_1 (bgzf)

| threads | polars_bio | seqkit |
|---|---|---|
| 1 | 7.87 s / 11.1 CPU-s / 255 MB | 22.10 s / 21.8 CPU-s / 161 MB |
| 2 | 3.84 s / 11.4 CPU-s / 542 MB | — |
| 4 | 2.34 s / 11.6 CPU-s / 904 MB | — |
| 8 | 1.92 s / 12.3 CPU-s / 1419 MB | — |

### revcomp — SRR39421268 (bgzf)

| threads | polars_bio | seqkit |
|---|---|---|
| 1 | 19.52 s / 30.2 CPU-s / 314 MB | 58.27 s / 57.2 CPU-s / 162 MB |
| 2 | 12.04 s / 31.3 CPU-s / 668 MB | — |
| 4 | 6.00 s / 31.7 CPU-s / 935 MB | — |
| 8 | 5.48 s / 32.8 CPU-s / 1752 MB | — |

Wall = best of N runs; CPU-s and peak RSS from that run. Python tools (polars_bio, biopython) are timed after imports; summary.csv also has the full process time. † single-threaded tool, run once.
