[19:55:24]   Benchmark Results, operation: overlap dataset: databio, test: 8-7                                                                                                                                run-benchmarks.py:418

           | Library       |     Min (s) |     Max (s) |    Mean (s) | Speedup |
           |---------------|-------------|-------------|-------------|---------|
           | polars_bio    |    6.235223 |    9.614410 |    7.723144 |   6.54x |
           | bioframe      |   50.319263 |   50.956633 |   50.537202 |   1.00x |
           | pyranges0     |   36.371926 |   36.581642 |   36.448645 |   1.39x |
           | pyranges1     |   63.336711 |   63.455435 |   63.406540 |   0.80x |
           | pybedtools    | 1149.001487 | 1152.127068 | 1150.070659 |   0.04x |
           | genomicranges |  597.951648 |  599.960895 |  599.002871 |   0.08x |



[20:04:22] ## Benchmark nearest for nearest with dataset databio                                                                                                                                               run-benchmarks.py:86

[20:10:14]   Benchmark Results, operation: nearest dataset: databio,                                                                                                                                          run-benchmarks.py:418
                                    test: 8-7

           | Library    |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |------------|-----------|-----------|-----------|---------|
           | polars_bio |  3.576373 |  3.679698 |  3.633697 |  15.54x |
           | bioframe   | 56.301865 | 56.776617 | 56.464305 |   1.00x |
           | pyranges0  |  2.453080 |  2.604940 |  2.505172 |  22.54x |
           | pyranges1  |  4.975662 |  5.011008 |  4.997007 |  11.30x |
           | pybedtools | 44.181913 | 44.794090 | 44.386971 |   1.27x |

           ## Benchmark count-overlaps for count_overlaps with dataset databio                                                                                                                                 run-benchmarks.py:86

[20:49:01]   Benchmark Results, operation: count_overlaps dataset: databio,                                                                                                                                   run-benchmarks.py:418
                                       test: 8-7

           | Library       |    Min (s) |    Max (s) |   Mean (s) | Speedup |
           |---------------|------------|------------|------------|---------|
           | polars_bio    |   2.052196 |   2.104447 |   2.075706 |  38.15x |
           | bioframe      |  79.174164 |  79.234115 |  79.194209 |   1.00x |
           | pyranges0     |  18.797436 |  18.851941 |  18.824498 |   4.21x |
           | pyranges1     |  20.399172 |  20.436149 |  20.418562 |   3.88x |
           | pybedtools    |  35.850631 |  36.142479 |  36.041115 |   2.20x |
           | genomicranges | 612.985873 | 613.520870 | 613.229997 |   0.13x |

           ## Benchmark coverage for coverage with dataset databio                                                                                                                                             run-benchmarks.py:86

[21:27:50] Benchmark Results, operation: coverage dataset: databio, test: 8-7                                                                                                                                 run-benchmarks.py:418

           | Library       |    Min (s) |    Max (s) |   Mean (s) | Speedup |
           |---------------|------------|------------|------------|---------|
           | polars_bio    |   1.829478 |   1.838981 |   1.834999 |  15.44x |
           | bioframe      |  28.291360 |  28.361417 |  28.326821 |   1.00x |
           | pyranges0     |  18.611247 |  20.021441 |  19.473105 |   1.45x |
           | pyranges1     |  22.118838 |  22.210733 |  22.161329 |   1.28x |
           | pybedtools    |  74.477086 |  74.868659 |  74.618066 |   0.38x |
           | genomicranges | 623.865655 | 623.949550 | 623.896645 |   0.05x |

