[18:53:50] ## Benchmark overlap for overlap with dataset databio                                                                                                                                               run-benchmarks.py:92

[18:55:10]   Benchmark Results, operation: overlap dataset: databio,                                                                                                                                          run-benchmarks.py:454
                                    test: 8-7

           | Library      |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |--------------|----------|----------|----------|---------|
           | polars_bio   | 3.247022 | 3.803021 | 3.370889 |   1.00x |
           | polars_bio-2 | 1.798569 | 1.848162 | 1.811417 |   1.86x |
           | polars_bio-4 | 1.140229 | 1.158243 | 1.147355 |   2.94x |
           | polars_bio-6 | 0.959703 | 0.968725 | 0.962915 |   3.50x |
           | polars_bio-8 | 0.694637 | 0.710492 | 0.701048 |   4.81x |

           ## Benchmark nearest for nearest with dataset databio                                                                                                                                               run-benchmarks.py:92

[18:55:26]   Benchmark Results, operation: nearest dataset: databio,                                                                                                                                          run-benchmarks.py:454
                                    test: 8-7

           | Library      |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |--------------|----------|----------|----------|---------|
           | polars_bio   | 2.186354 | 2.248171 | 2.220822 |   1.00x |
           | polars_bio-2 | 1.162969 | 1.222115 | 1.187505 |   1.87x |
           | polars_bio-4 | 0.708508 | 0.735763 | 0.720115 |   3.08x |
           | polars_bio-6 | 0.632877 | 0.652955 | 0.642816 |   3.45x |
           | polars_bio-8 | 0.456674 | 0.476473 | 0.465284 |   4.77x |

           ## Benchmark count-overlaps for count_overlaps with dataset databio                                                                                                                                 run-benchmarks.py:92

[18:55:36]    Benchmark Results, operation: count_overlaps dataset:                                                                                                                                           run-benchmarks.py:454
                               databio, test: 8-7

           | Library      |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |--------------|----------|----------|----------|---------|
           | polars_bio   | 1.502551 | 1.534006 | 1.515078 |   1.00x |
           | polars_bio-2 | 0.811236 | 0.821365 | 0.815682 |   1.86x |
           | polars_bio-4 | 0.440628 | 0.467780 | 0.455358 |   3.33x |
           | polars_bio-6 | 0.331317 | 0.338207 | 0.334638 |   4.53x |
           | polars_bio-8 | 0.280465 | 0.282707 | 0.281311 |   5.39x |

           ## Benchmark coverage for coverage with dataset databio                                                                                                                                             run-benchmarks.py:92

[18:55:44]  Benchmark Results, operation: coverage dataset: databio,                                                                                                                                          run-benchmarks.py:454
                                    test: 8-7

           | Library      |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |--------------|----------|----------|----------|---------|
           | polars_bio   | 1.181806 | 1.185549 | 1.183889 |   1.00x |
           | polars_bio-2 | 0.644288 | 0.645076 | 0.644587 |   1.84x |
           | polars_bio-4 | 0.362752 | 0.363411 | 0.363036 |   3.26x |
           | polars_bio-6 | 0.258583 | 0.272702 | 0.264111 |   4.48x |
           | polars_bio-8 | 0.222888 | 0.234884 | 0.229052 |   5.17x |

