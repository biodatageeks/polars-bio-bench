[05:27:49] ## Benchmark overlap for overlap with dataset databio                                                                                                                                               run-benchmarks.py:84

[07:03:37]   Benchmark Results, operation: overlap dataset: databio, test: 7-8                                                                                                                                run-benchmarks.py:399

           | Library       |     Min (s) |     Max (s) |    Mean (s) | Speedup |
           |---------------|-------------|-------------|-------------|---------|
           | polars_bio    |    5.963408 |    9.301349 |    7.137417 |   6.59x |
           | bioframe      |   46.917082 |   47.064881 |   47.008068 |   1.00x |
           | pyranges0     |   38.998641 |   39.235061 |   39.094404 |   1.20x |
           | pyranges1     |   58.893228 |   59.189104 |   59.018261 |   0.80x |
           | pybedtools    | 1140.170191 | 1154.471479 | 1146.928179 |   0.04x |
           | genomicranges |  608.651610 |  609.655036 |  609.138146 |   0.08x |

           ## Benchmark nearest for nearest with dataset databio                                                                                                                                               run-benchmarks.py:84

[07:06:55]   Benchmark Results, operation: nearest dataset: databio,                                                                                                                                          run-benchmarks.py:399
                                    test: 7-8

           | Library    |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |------------|-----------|-----------|-----------|---------|
           | polars_bio |  1.718840 |  1.819572 |  1.768159 |  21.07x |
           | bioframe   | 37.234216 | 37.267567 | 37.252052 |   1.00x |
           | pyranges0  |  3.793256 |  3.813382 |  3.801250 |   9.80x |
           | pyranges1  |  3.989960 |  4.021302 |  4.000560 |   9.31x |
           | pybedtools | 14.254434 | 14.389208 | 14.313488 |   2.60x |

           ## Benchmark count-overlaps for count_overlaps with dataset databio                                                                                                                                 run-benchmarks.py:84

[07:43:12]   Benchmark Results, operation: count_overlaps dataset: databio,                                                                                                                                   run-benchmarks.py:399
                                       test: 7-8

           | Library       |    Min (s) |    Max (s) |   Mean (s) | Speedup |
           |---------------|------------|------------|------------|---------|
           | polars_bio    |   0.894491 |   0.992091 |   0.928374 |  73.44x |
           | bioframe      |  68.134710 |  68.248018 |  68.176729 |   1.00x |
           | pyranges0     |  14.000387 |  14.031491 |  14.017435 |   4.86x |
           | pyranges1     |  14.347921 |  14.374372 |  14.362947 |   4.75x |
           | pybedtools    |  22.498061 |  22.555980 |  22.525745 |   3.03x |
           | genomicranges | 599.088590 | 600.057943 | 599.693688 |   0.11x |

           ## Benchmark coverage for coverage with dataset databio                                                                                                                                             run-benchmarks.py:84

[08:18:30] Benchmark Results, operation: coverage dataset: databio, test: 7-8                                                                                                                                 run-benchmarks.py:399

           | Library       |    Min (s) |    Max (s) |   Mean (s) | Speedup |
           |---------------|------------|------------|------------|---------|
           | polars_bio    |   0.616830 |   0.652835 |   0.632323 |   5.01x |
           | bioframe      |   3.160851 |   3.172302 |   3.165307 |   1.00x |
           | pyranges0     |  14.336820 |  14.370083 |  14.354427 |   0.22x |
           | pyranges1     |  15.626344 |  15.730648 |  15.673289 |   0.20x |
           | pybedtools    |  45.224326 |  50.118518 |  46.934375 |   0.07x |
           | genomicranges | 614.536679 | 623.262875 | 619.269005 |   0.01x |

