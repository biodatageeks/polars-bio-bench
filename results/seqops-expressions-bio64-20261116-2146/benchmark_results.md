### gc_qual — SRR39421268 (bgzf)

| threads | biopython | seqkit |
|---|---|---|
| 1 | 380.41 s / 378.7 CPU-s / 57 MB† | 65.27 s / 64.8 CPU-s / 55 MB |

### gc_qual — SRR39421268 (gzip)

| threads | biopython | seqkit |
|---|---|---|
| 1 | 357.75 s / 355.6 CPU-s / 49 MB† | 63.51 s / 63.1 CPU-s / 58 MB |

Wall = best of N runs; CPU-s and peak RSS from that run. Python tools (polars_bio, biopython) are timed after imports; summary.csv also has the full process time. † single-threaded tool, run once.
