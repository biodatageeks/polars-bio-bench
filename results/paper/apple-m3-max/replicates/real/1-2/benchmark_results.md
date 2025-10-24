[17:34:36] ## Benchmark overlap for overlap with dataset databio                                                                                                                                               run-benchmarks.py:84

[17:34:41]   Benchmark Results, operation: overlap dataset: databio,                                                                                                                                          run-benchmarks.py:399
                                    test: 1-2

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.035619 | 0.043113 | 0.038300 |   2.70x |
           | bioframe      | 0.102257 | 0.104425 | 0.103354 |   1.00x |
           | pyranges0     | 0.025425 | 0.032821 | 0.028001 |   3.69x |
           | pyranges1     | 0.059608 | 0.064147 | 0.061763 |   1.67x |
           | pybedtools    | 0.343204 | 0.352804 | 0.348434 |   0.30x |
           | genomicranges | 1.042893 | 1.044245 | 1.043488 |   0.10x |

           ## Benchmark nearest for nearest with dataset databio                                                                                                                                               run-benchmarks.py:84

[17:34:46]  Benchmark Results, operation: nearest dataset: databio,                                                                                                                                           run-benchmarks.py:399
                                   test: 1-2

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.039943 | 0.045166 | 0.042109 |   4.45x |
           | bioframe   | 0.185452 | 0.189631 | 0.187388 |   1.00x |
           | pyranges0  | 0.092334 | 0.096340 | 0.093688 |   2.00x |
           | pyranges1  | 0.133631 | 0.134179 | 0.133981 |   1.40x |
           | pybedtools | 0.756676 | 0.761866 | 0.759530 |   0.25x |

           ## Benchmark count-overlaps for count_overlaps with dataset databio                                                                                                                                 run-benchmarks.py:84

[17:34:52]    Benchmark Results, operation: count_overlaps dataset:                                                                                                                                           run-benchmarks.py:399
                                databio, test: 1-2

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.026706 | 0.029754 | 0.028142 |   4.69x |
           | bioframe      | 0.131124 | 0.133729 | 0.132052 |   1.00x |
           | pyranges0     | 0.039136 | 0.039774 | 0.039377 |   3.35x |
           | pyranges1     | 0.061976 | 0.063181 | 0.062658 |   2.11x |
           | pybedtools    | 0.665804 | 0.673844 | 0.668534 |   0.20x |
           | genomicranges | 0.994963 | 1.006435 | 0.999389 |   0.13x |

           ## Benchmark coverage for coverage with dataset databio                                                                                                                                             run-benchmarks.py:84

[17:35:00]   Benchmark Results, operation: coverage dataset: databio,                                                                                                                                         run-benchmarks.py:399
                                    test: 1-2

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.026200 | 0.028749 | 0.027418 |   6.30x |
           | bioframe      | 0.169490 | 0.176628 | 0.172842 |   1.00x |
           | pyranges0     | 0.073760 | 0.076708 | 0.075369 |   2.29x |
           | pyranges1     | 0.128027 | 0.133263 | 0.130247 |   1.33x |
           | pybedtools    | 0.701817 | 0.708726 | 0.705839 |   0.24x |
           | genomicranges | 1.032651 | 1.049059 | 1.040799 |   0.17x |

