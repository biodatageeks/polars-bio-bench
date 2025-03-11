[17:47:58] ## Benchmark overlap for overlap with dataset databio                                                                                                                                               run-benchmarks.py:84

[17:56:06]   Benchmark Results, operation: overlap dataset: databio,                                                                                                                                          run-benchmarks.py:399
                                    test: 7-8

           | Library    |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |------------|-----------|-----------|-----------|---------|
           | polars_bio |  6.429061 |  9.531259 |  7.480953 |   6.62x |
           | bioframe   | 49.229800 | 49.794657 | 49.516737 |   1.00x |
           | pyranges0  | 40.332748 | 40.573018 | 40.417290 |   1.23x |
           | pyranges1  | 62.376796 | 62.497577 | 62.423127 |   0.79x |

           ## Benchmark nearest for nearest with dataset databio                                                                                                                                               run-benchmarks.py:84

[17:59:32]   Benchmark Results, operation: nearest dataset: databio,                                                                                                                                          run-benchmarks.py:399
                                    test: 7-8

           | Library    |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |------------|-----------|-----------|-----------|---------|
           | polars_bio |  1.756373 |  1.778567 |  1.768523 |  22.56x |
           | bioframe   | 39.852615 | 39.993454 | 39.903635 |   1.00x |
           | pyranges0  |  3.748316 |  3.762895 |  3.757848 |  10.62x |
           | pyranges1  |  4.132873 |  4.143734 |  4.139812 |   9.64x |
           | pybedtools | 14.008201 | 14.264574 | 14.094361 |   2.83x |

           ## Benchmark count-overlaps for count_overlaps with dataset databio                                                                                                                                 run-benchmarks.py:84

[18:05:59]    Benchmark Results, operation: count_overlaps dataset:                                                                                                                                           run-benchmarks.py:399
                                databio, test: 7-8

           | Library    |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |------------|-----------|-----------|-----------|---------|
           | polars_bio |  0.868312 |  0.932008 |  0.897455 |  79.04x |
           | bioframe   | 70.895304 | 70.987676 | 70.934219 |   1.00x |
           | pyranges0  | 15.022168 | 15.053584 | 15.033701 |   4.72x |
           | pyranges1  | 15.364527 | 15.429814 | 15.386847 |   4.61x |
           | pybedtools | 21.602490 | 21.707206 | 21.651674 |   3.28x |

           ## Benchmark coverage for coverage with dataset databio                                                                                                                                             run-benchmarks.py:84

[18:10:15]   Benchmark Results, operation: coverage dataset: databio,                                                                                                                                         run-benchmarks.py:399
                                    test: 7-8

           | Library    |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |------------|-----------|-----------|-----------|---------|
           | polars_bio |  0.609361 |  0.631925 |  0.619775 |   5.56x |
           | bioframe   |  3.434331 |  3.457579 |  3.446962 |   1.00x |
           | pyranges0  | 15.692374 | 15.741281 | 15.714699 |   0.22x |
           | pyranges1  | 15.576217 | 16.832754 | 16.134836 |   0.21x |
           | pybedtools | 44.253595 | 44.298738 | 44.271122 |   0.08x |

