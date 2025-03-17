[16:25:36] ## Benchmark overlap for overlap with dataset databio                                                                                                                                               run-benchmarks.py:84

[16:25:43]   Benchmark Results, operation: overlap dataset: databio,                                                                                                                                          run-benchmarks.py:399
                                    test: 1-2

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.045943 | 0.064732 | 0.054234 |   1.66x |
           | bioframe      | 0.084137 | 0.099481 | 0.090107 |   1.00x |
           | pyranges0     | 0.056206 | 0.065654 | 0.061844 |   1.46x |
           | pyranges1     | 0.099080 | 0.119018 | 0.106228 |   0.85x |
           | pybedtools    | 0.382460 | 0.406379 | 0.391530 |   0.23x |
           | genomicranges | 1.199390 | 1.224621 | 1.208255 |   0.07x |

           ## Benchmark nearest for nearest with dataset databio                                                                                                                                               run-benchmarks.py:84

[16:25:48]  Benchmark Results, operation: nearest dataset: databio,                                                                                                                                           run-benchmarks.py:399
                                   test: 1-2

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.057012 | 0.073822 | 0.064665 |   2.49x |
           | bioframe   | 0.158764 | 0.165707 | 0.161273 |   1.00x |
           | pyranges0  | 0.172297 | 0.176259 | 0.173630 |   0.93x |
           | pyranges1  | 0.217619 | 0.234088 | 0.223350 |   0.72x |
           | pybedtools | 0.845945 | 0.848980 | 0.847447 |   0.19x |

           ## Benchmark count-overlaps for count_overlaps with dataset databio                                                                                                                                 run-benchmarks.py:84

[16:25:55]    Benchmark Results, operation: count_overlaps dataset:                                                                                                                                           run-benchmarks.py:399
                                databio, test: 1-2

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.035631 | 0.043555 | 0.040660 |   2.74x |
           | bioframe      | 0.108015 | 0.116522 | 0.111266 |   1.00x |
           | pyranges0     | 0.077336 | 0.080282 | 0.078440 |   1.42x |
           | pyranges1     | 0.100883 | 0.106671 | 0.103181 |   1.08x |
           | pybedtools    | 0.745958 | 0.759006 | 0.754393 |   0.15x |
           | genomicranges | 1.154942 | 1.164158 | 1.158506 |   0.10x |

           ## Benchmark coverage for coverage with dataset databio                                                                                                                                             run-benchmarks.py:84

[16:26:04]   Benchmark Results, operation: coverage dataset: databio,                                                                                                                                         run-benchmarks.py:399
                                    test: 1-2

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.036476 | 0.040001 | 0.037897 |   5.10x |
           | bioframe      | 0.189201 | 0.200460 | 0.193401 |   1.00x |
           | pyranges0     | 0.141659 | 0.144240 | 0.143188 |   1.35x |
           | pyranges1     | 0.206033 | 0.224902 | 0.213089 |   0.91x |
           | pybedtools    | 0.773732 | 0.780424 | 0.776934 |   0.25x |
           | genomicranges | 1.186341 | 1.194172 | 1.189255 |   0.16x |

