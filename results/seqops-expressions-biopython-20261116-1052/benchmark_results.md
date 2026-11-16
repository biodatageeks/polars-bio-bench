### revcomp — DRR013000_1 (bgzf)

| threads | biopython | seqkit |
|---|---|---|
| 1 | 48.28 s / 48.0 CPU-s / 53 MB† | 22.21 s / 22.1 CPU-s / 162 MB |

### revcomp — DRR013000_1 (gzip)

| threads | biopython | seqkit |
|---|---|---|
| 1 | 46.00 s / 45.7 CPU-s / 48 MB† | 20.88 s / 20.8 CPU-s / 75 MB |

### gc_qual — DRR013000_1 (bgzf)

| threads | biopython | seqkit |
|---|---|---|
| 1 | 114.29 s / 114.1 CPU-s / 54 MB† | 25.94 s / 25.9 CPU-s / 55 MB |

### gc_qual — DRR013000_1 (gzip)

| threads | biopython | seqkit |
|---|---|---|
| 1 | 114.28 s / 114.1 CPU-s / 47 MB† | 24.96 s / 24.9 CPU-s / 58 MB |

Wall = best of N runs; CPU-s and peak RSS from that run. Python tools (polars_bio, biopython) are timed after imports; summary.csv also has the full process time. † single-threaded tool, run once.
