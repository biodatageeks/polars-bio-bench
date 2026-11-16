### revcomp — SRR39421268 (bgzf)

| threads | biopython | seqkit |
|---|---|---|
| 1 | 144.07 s / 133.4 CPU-s / 57 MB† | 68.56 s / 59.2 CPU-s / 165 MB |

### revcomp — SRR39421268 (gzip)

| threads | biopython | seqkit |
|---|---|---|
| 1 | 135.38 s / 127.0 CPU-s / 48 MB† | 56.67 s / 54.2 CPU-s / 75 MB |

Wall = best of N runs; CPU-s and peak RSS from that run. Python tools (polars_bio, biopython) are timed after imports; summary.csv also has the full process time. † single-threaded tool, run once.
