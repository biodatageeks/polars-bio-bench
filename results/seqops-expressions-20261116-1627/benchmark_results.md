### revcomp — DRR609229_1 (bgzf)

| threads | polars_bio | seqkit |
|---|---|---|
| 1 | 0.21 s / 0.3 CPU-s / 176 MB | 0.55 s / 0.5 CPU-s / 138 MB |
| 2 | 0.11 s / 0.4 CPU-s / 286 MB | — |
| 4 | 0.08 s / 0.4 CPU-s / 457 MB | — |
| 8 | 0.07 s / 0.4 CPU-s / 538 MB | — |

### revcomp — DRR609229_1 (gzip)

| threads | polars_bio | seqkit |
|---|---|---|
| 1 | 0.22 s / 0.4 CPU-s / 173 MB | 0.49 s / 0.5 CPU-s / 75 MB |
| 2 | 0.23 s / 0.4 CPU-s / 278 MB | — |
| 4 | 0.23 s / 0.4 CPU-s / 314 MB | — |
| 8 | 0.24 s / 0.4 CPU-s / 372 MB | — |

### revcomp — ERR5897746_1 (bgzf)

| threads | polars_bio | seqkit |
|---|---|---|
| 1 | 1.69 s / 2.5 CPU-s / 208 MB | 5.22 s / 5.1 CPU-s / 161 MB |
| 2 | 0.82 s / 2.5 CPU-s / 373 MB | — |
| 4 | 0.42 s / 2.6 CPU-s / 524 MB | — |
| 8 | 0.35 s / 2.8 CPU-s / 1299 MB | — |

### revcomp — ERR5897746_1 (gzip)

| threads | polars_bio | seqkit |
|---|---|---|
| 1 | 1.92 s / 2.7 CPU-s / 179 MB | 4.87 s / 4.8 CPU-s / 75 MB |
| 2 | 1.89 s / 2.7 CPU-s / 305 MB | — |
| 4 | 1.92 s / 2.8 CPU-s / 380 MB | — |
| 8 | 1.90 s / 2.8 CPU-s / 484 MB | — |

### revcomp — DRR013000_1 (bgzf)

| threads | polars_bio | seqkit |
|---|---|---|
| 1 | 8.06 s / 11.5 CPU-s / 259 MB | 22.64 s / 22.2 CPU-s / 161 MB |
| 2 | 3.88 s / 11.7 CPU-s / 568 MB | — |
| 4 | 2.30 s / 11.7 CPU-s / 850 MB | — |
| 8 | 1.90 s / 12.5 CPU-s / 1421 MB | — |

### revcomp — DRR013000_1 (gzip)

| threads | polars_bio | seqkit |
|---|---|---|
| 1 | 9.09 s / 12.4 CPU-s / 230 MB | 21.26 s / 21.0 CPU-s / 75 MB |
| 2 | 9.11 s / 12.7 CPU-s / 477 MB | — |
| 4 | 9.12 s / 12.7 CPU-s / 456 MB | — |
| 8 | 9.12 s / 12.7 CPU-s / 566 MB | — |

### revcomp — SRR39421268 (bgzf)

| threads | polars_bio | seqkit |
|---|---|---|
| 1 | 19.72 s / 30.4 CPU-s / 300 MB | 58.05 s / 57.0 CPU-s / 162 MB |
| 2 | 9.95 s / 31.3 CPU-s / 620 MB | — |
| 4 | 5.45 s / 31.7 CPU-s / 1005 MB | — |
| 8 | 5.68 s / 32.9 CPU-s / 1926 MB | — |

### revcomp — SRR39421268 (gzip)

| threads | polars_bio | seqkit |
|---|---|---|
| 1 | 22.30 s / 33.1 CPU-s / 277 MB | 54.80 s / 53.6 CPU-s / 75 MB |
| 2 | 22.37 s / 33.6 CPU-s / 588 MB | — |
| 4 | 22.32 s / 33.7 CPU-s / 607 MB | — |
| 8 | 22.36 s / 33.9 CPU-s / 736 MB | — |

### translate — ensembl_cds (bgzf)

| threads | polars_bio | seqkit |
|---|---|---|
| 1 | 0.73 s / 1.1 CPU-s / 362 MB | 3.46 s / 3.4 CPU-s / 56 MB |
| 2 | 0.74 s / 1.1 CPU-s / 546 MB | — |
| 4 | 0.75 s / 1.1 CPU-s / 640 MB | — |
| 8 | 0.76 s / 1.1 CPU-s / 802 MB | — |

### translate — ensembl_cds (gzip)

| threads | polars_bio | seqkit |
|---|---|---|
| 1 | 0.78 s / 1.2 CPU-s / 360 MB | 3.31 s / 3.3 CPU-s / 57 MB |
| 2 | 0.79 s / 1.2 CPU-s / 575 MB | — |
| 4 | 0.80 s / 1.2 CPU-s / 650 MB | — |
| 8 | 0.79 s / 1.2 CPU-s / 800 MB | — |

Wall = best of N runs; CPU-s and peak RSS from that run. Python tools (polars_bio, biopython) are timed after imports; summary.csv also has the full process time. † single-threaded tool, run once.
