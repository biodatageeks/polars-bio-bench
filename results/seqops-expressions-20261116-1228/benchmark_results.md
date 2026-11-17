### revcomp — DRR609229_1 (bgzf)

| threads | seqkit |
|---|---|
| 1 | 0.54 s / 0.5 CPU-s / 138 MB |
| 8 | 0.54 s / 0.6 CPU-s / 139 MB |

### revcomp — DRR609229_1 (gzip)

| threads | seqkit |
|---|---|
| 1 | 0.49 s / 0.5 CPU-s / 75 MB |
| 8 | 0.27 s / 0.5 CPU-s / 75 MB |

### revcomp — ERR5897746_1 (bgzf)

| threads | seqkit |
|---|---|
| 1 | 5.21 s / 5.2 CPU-s / 161 MB |
| 8 | 5.23 s / 5.8 CPU-s / 160 MB |

### revcomp — ERR5897746_1 (gzip)

| threads | seqkit |
|---|---|
| 1 | 4.88 s / 4.9 CPU-s / 75 MB |
| 8 | 2.90 s / 4.9 CPU-s / 75 MB |

### revcomp — DRR013000_1 (bgzf)

| threads | seqkit |
|---|---|
| 1 | 22.41 s / 22.3 CPU-s / 162 MB |
| 8 | 22.66 s / 24.6 CPU-s / 160 MB |

### revcomp — DRR013000_1 (gzip)

| threads | seqkit |
|---|---|
| 1 | 21.25 s / 21.2 CPU-s / 75 MB |
| 8 | 12.52 s / 21.5 CPU-s / 75 MB |

### revcomp — SRR39421268 (bgzf)

| threads | seqkit |
|---|---|
| 1 | 58.95 s / 58.4 CPU-s / 163 MB |
| 8 | 60.26 s / 65.5 CPU-s / 161 MB |

### revcomp — SRR39421268 (gzip)

| threads | seqkit |
|---|---|
| 1 | 55.53 s / 54.8 CPU-s / 75 MB |
| 8 | 30.14 s / 56.1 CPU-s / 76 MB |

### gc_qual — DRR609229_1 (bgzf)

| threads | seqkit |
|---|---|
| 1 | 0.66 s / 0.7 CPU-s / 54 MB |
| 8 | 0.67 s / 0.7 CPU-s / 56 MB |

### gc_qual — DRR609229_1 (gzip)

| threads | seqkit |
|---|---|
| 1 | 0.62 s / 0.6 CPU-s / 57 MB |
| 8 | 0.40 s / 0.6 CPU-s / 57 MB |

### gc_qual — ERR5897746_1 (bgzf)

| threads | seqkit |
|---|---|
| 1 | 5.75 s / 5.7 CPU-s / 55 MB |
| 8 | 5.84 s / 6.4 CPU-s / 57 MB |

### gc_qual — ERR5897746_1 (gzip)

| threads | seqkit |
|---|---|
| 1 | 5.42 s / 5.4 CPU-s / 57 MB |
| 8 | 2.90 s / 5.5 CPU-s / 61 MB |

### gc_qual — DRR013000_1 (bgzf)

| threads | seqkit |
|---|---|
| 1 | 26.71 s / 26.7 CPU-s / 55 MB |
| 8 | 27.00 s / 29.1 CPU-s / 58 MB |

### gc_qual — DRR013000_1 (gzip)

| threads | seqkit |
|---|---|
| 1 | 25.55 s / 25.5 CPU-s / 58 MB |
| 8 | 12.67 s / 25.9 CPU-s / 70 MB |

### gc_qual — SRR39421268 (bgzf)

| threads | seqkit |
|---|---|
| 1 | 66.15 s / 66.1 CPU-s / 55 MB |
| 8 | 67.42 s / 74.3 CPU-s / 75 MB |

### gc_qual — SRR39421268 (gzip)

| threads | seqkit |
|---|---|
| 1 | 63.17 s / 63.1 CPU-s / 57 MB |
| 8 | 32.07 s / 64.5 CPU-s / 81 MB |

### translate — ensembl_cds (bgzf)

| threads | seqkit |
|---|---|
| 1 | 3.52 s / 3.5 CPU-s / 57 MB |
| 8 | 3.57 s / 3.8 CPU-s / 56 MB |

### translate — ensembl_cds (gzip)

| threads | seqkit |
|---|---|
| 1 | 3.36 s / 3.4 CPU-s / 57 MB |
| 8 | 2.99 s / 3.4 CPU-s / 58 MB |

Wall = best of N runs; CPU-s and peak RSS from that run. Python tools (polars_bio, biopython) are timed after imports; summary.csv also has the full process time. † single-threaded tool, run once.
