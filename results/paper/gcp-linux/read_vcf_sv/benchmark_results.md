[16:15:55] ## Benchmark read_vcf for read_vcf with dataset gnomad-vcf-sv                                                                                                                                       run-benchmarks.py:86

[16:17:29] Benchmark Results, operation: read_vcf dataset: gnomad-vcf-sv,                                                                                                                                     run-benchmarks.py:418
                                  test: gnomad-sv

           | Library      |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |--------------|-----------|-----------|-----------|---------|
           | polars_bio   | 12.515988 | 13.244607 | 12.828105 |   1.00x |
           | polars_bio-2 |  6.165673 |  6.264022 |  6.209827 |   2.07x |
           | polars_bio-4 |  4.106742 |  4.312496 |  4.193489 |   3.06x |
           | polars_bio-6 |  4.163757 |  4.294907 |  4.213461 |   3.04x |
           | polars_bio-8 |  4.037023 |  4.095520 |  4.066964 |   3.15x |

