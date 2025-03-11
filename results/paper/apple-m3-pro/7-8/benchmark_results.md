[17:45:19] ## Benchmark overlap for overlap with dataset databio                                                                                                                                               run-benchmarks.py:84

[19:01:59] Benchmark Results, operation: overlap dataset: databio, test: 7-8                                                                                                                                  run-benchmarks.py:399

           | Library       |    Min (s) |    Max (s) |   Mean (s) | Speedup |
           |---------------|------------|------------|------------|---------|
           | polars_bio    |   3.690849 |   4.521195 |   4.133256 |   8.14x |
           | bioframe      |  32.992552 |  34.653587 |  33.627669 |   1.00x |
           | pyranges0     |  17.257820 |  17.572468 |  17.422332 |   1.93x |
           | pyranges1     |  37.944865 |  38.349443 |  38.103580 |   0.88x |
           | pybedtools    | 928.899599 | 941.145935 | 935.928867 |   0.04x |
           | genomicranges | 488.103586 | 501.321331 | 494.727019 |   0.07x |

           ## Benchmark nearest for nearest with dataset databio                                                                                                                                               run-benchmarks.py:84

[19:06:02]   Benchmark Results, operation: nearest dataset: databio,                                                                                                                                          run-benchmarks.py:399
                                    test: 7-8

           | Library    |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |------------|-----------|-----------|-----------|---------|
           | polars_bio |  0.997866 |  1.097910 |  1.035164 |  58.27x |
           | bioframe   | 59.434924 | 61.437155 | 60.321533 |   1.00x |
           | pyranges0  |  2.584567 |  2.654851 |  2.609247 |  23.12x |
           | pyranges1  |  2.981571 |  2.991015 |  2.986111 |  20.20x |
           | pybedtools |  9.591584 |  9.694962 |  9.641826 |   6.26x |

           ## Benchmark count-overlaps for count_overlaps with dataset databio                                                                                                                                 run-benchmarks.py:84

[19:36:47]   Benchmark Results, operation: count_overlaps dataset: databio,                                                                                                                                   run-benchmarks.py:399
                                       test: 7-8

           | Library       |    Min (s) |    Max (s) |   Mean (s) | Speedup |
           |---------------|------------|------------|------------|---------|
           | polars_bio    |   0.607341 |   0.649601 |   0.625818 | 153.22x |
           | bioframe      |  94.752099 |  97.140491 |  95.889287 |   1.00x |
           | pyranges0     |   8.006050 |   8.094492 |   8.049485 |  11.91x |
           | pyranges1     |   8.179629 |   8.360123 |   8.246488 |  11.63x |
           | pybedtools    |  21.760503 |  21.884291 |  21.803886 |   4.40x |
           | genomicranges | 474.604178 | 474.770272 | 474.691771 |   0.20x |

           ## Benchmark coverage for coverage with dataset databio                                                                                                                                             run-benchmarks.py:84

[20:04:17] Benchmark Results, operation: coverage dataset: databio, test: 7-8                                                                                                                                 run-benchmarks.py:399

           | Library       |    Min (s) |    Max (s) |   Mean (s) | Speedup |
           |---------------|------------|------------|------------|---------|
           | polars_bio    |   0.355176 |   0.404522 |   0.376343 |   7.18x |
           | bioframe      |   2.664851 |   2.752263 |   2.700862 |   1.00x |
           | pyranges0     |   8.811767 |   8.932990 |   8.856726 |   0.30x |
           | pyranges1     |   9.318718 |   9.350268 |   9.337817 |   0.29x |
           | pybedtools    |  41.135649 |  41.197101 |  41.158139 |   0.07x |
           | genomicranges | 482.299664 | 482.451084 | 482.360109 |   0.01x |

