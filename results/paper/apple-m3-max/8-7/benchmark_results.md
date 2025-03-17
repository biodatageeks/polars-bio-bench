[18:18:23] ## Benchmark overlap for overlap with dataset databio                                                                                                                                               run-benchmarks.py:86

[19:33:08] Benchmark Results, operation: overlap dataset: databio, test: 8-7                                                                                                                                  run-benchmarks.py:418

           | Library       |    Min (s) |    Max (s) |   Mean (s) | Speedup |
           |---------------|------------|------------|------------|---------|
           | polars_bio    |   3.987391 |   4.648581 |   4.235518 |   7.17x |
           | bioframe      |  29.793837 |  30.991576 |  30.375518 |   1.00x |
           | pyranges0     |  15.632212 |  15.974075 |  15.857213 |   1.92x |
           | pyranges1     |  31.622804 |  33.699074 |  32.680701 |   0.93x |
           | pybedtools    | 916.711575 | 919.974811 | 918.154834 |   0.03x |
           | genomicranges | 479.214112 | 487.832054 | 484.579554 |   0.06x |

           ## Benchmark nearest for nearest with dataset databio                                                                                                                                               run-benchmarks.py:86

[19:38:54]   Benchmark Results, operation: nearest dataset: databio,                                                                                                                                          run-benchmarks.py:418
                                    test: 8-7

           | Library    |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |------------|-----------|-----------|-----------|---------|
           | polars_bio |  2.116922 |  2.169534 |  2.139006 |  32.13x |
           | bioframe   | 68.581465 | 68.992651 | 68.725495 |   1.00x |
           | pyranges0  |  1.381964 |  1.508513 |  1.424446 |  48.25x |
           | pyranges1  |  2.697684 |  2.728407 |  2.717532 |  25.29x |
           | pybedtools | 35.528719 | 35.876667 | 35.699544 |   1.93x |

           ## Benchmark count-overlaps for count_overlaps with dataset databio                                                                                                                                 run-benchmarks.py:86

[20:10:41]   Benchmark Results, operation: count_overlaps dataset: databio,                                                                                                                                   run-benchmarks.py:418
                                       test: 8-7

           | Library       |    Min (s) |    Max (s) |   Mean (s) | Speedup |
           |---------------|------------|------------|------------|---------|
           | polars_bio    |   1.445467 |   1.484052 |   1.462250 |  58.77x |
           | bioframe      |  85.632767 |  86.261480 |  85.935955 |   1.00x |
           | pyranges0     |   9.674847 |   9.833233 |   9.753982 |   8.81x |
           | pyranges1     |  10.170249 |  10.254359 |  10.201813 |   8.42x |
           | pybedtools    |  33.101592 |  33.966188 |  33.423595 |   2.57x |
           | genomicranges | 488.972732 | 490.395787 | 489.548184 |   0.18x |

           ## Benchmark coverage for coverage with dataset databio                                                                                                                                             run-benchmarks.py:86

[20:41:31] Benchmark Results, operation: coverage dataset: databio, test: 8-7                                                                                                                                 run-benchmarks.py:418

           | Library       |    Min (s) |    Max (s) |   Mean (s) | Speedup |
           |---------------|------------|------------|------------|---------|
           | polars_bio    |   1.195279 |   1.205765 |   1.199323 |  20.45x |
           | bioframe      |  24.423391 |  24.682901 |  24.525909 |   1.00x |
           | pyranges0     |  11.093644 |  11.328071 |  11.220416 |   2.19x |
           | pyranges1     |  11.987003 |  12.147925 |  12.066045 |   2.03x |
           | pybedtools    |  59.699275 |  60.040870 |  59.849650 |   0.41x |
           | genomicranges | 500.041974 | 503.319360 | 502.043072 |   0.05x |

