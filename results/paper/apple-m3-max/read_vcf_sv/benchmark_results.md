[15:05:44] ## Benchmark read_vcf for read_vcf with dataset gnomad-vcf-sv                                                                                                                                       run-benchmarks.py:84

[15:07:02] Benchmark Results, operation: read_vcf dataset: gnomad-vcf-sv,                                                                                                                                     run-benchmarks.py:411
                                  test: gnomad-sv

           | Library      |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |--------------|-----------|-----------|-----------|---------|
           | polars_bio   | 10.635991 | 10.715213 | 10.674258 |   1.00x |
           | polars_bio-2 |  6.270964 |  6.337421 |  6.306631 |   1.69x |
           | polars_bio-4 |  3.345155 |  3.346796 |  3.346028 |   3.19x |
           | polars_bio-6 |  2.799833 |  2.806898 |  2.802285 |   3.81x |
           | polars_bio-8 |  2.736320 |  2.756394 |  2.746718 |   3.89x |

