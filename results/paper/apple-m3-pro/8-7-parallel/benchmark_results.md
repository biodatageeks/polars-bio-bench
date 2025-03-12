[18:01:08] ## Benchmark overlap for overlap with dataset databio                                                                                                                                               run-benchmarks.py:86

[18:01:35]   Benchmark Results, operation: overlap dataset: databio,                                                                                                                                          run-benchmarks.py:418
                                    test: 8-7

           | Library      |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |--------------|----------|----------|----------|---------|
           | polars_bio   | 3.669992 | 4.567576 | 4.142872 |   1.00x |
           | polars_bio-2 | 1.872993 | 1.986568 | 1.927047 |   2.15x |
           | polars_bio-4 | 1.156394 | 1.182449 | 1.168503 |   3.55x |
           | polars_bio-6 | 0.981693 | 1.002629 | 0.995204 |   4.16x |
           | polars_bio-8 | 0.702201 | 0.749915 | 0.723033 |   5.73x |

           ## Benchmark nearest for nearest with dataset databio                                                                                                                                               run-benchmarks.py:86

[18:01:51]   Benchmark Results, operation: nearest dataset: databio,                                                                                                                                          run-benchmarks.py:418
                                    test: 8-7

           | Library      |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |--------------|----------|----------|----------|---------|
           | polars_bio   | 2.341672 | 2.486488 | 2.393080 |   1.00x |
           | polars_bio-2 | 1.229150 | 1.258844 | 1.243750 |   1.92x |
           | polars_bio-4 | 0.732996 | 0.744632 | 0.739464 |   3.24x |
           | polars_bio-6 | 0.655340 | 0.673741 | 0.664448 |   3.60x |
           | polars_bio-8 | 0.462252 | 0.480818 | 0.471103 |   5.08x |

           ## Benchmark count-overlaps for count_overlaps with dataset databio                                                                                                                                 run-benchmarks.py:86

[18:02:02]    Benchmark Results, operation: count_overlaps dataset:                                                                                                                                           run-benchmarks.py:418
                               databio, test: 8-7

           | Library      |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |--------------|----------|----------|----------|---------|
           | polars_bio   | 1.535449 | 1.562630 | 1.547632 |   1.00x |
           | polars_bio-2 | 0.798849 | 0.805491 | 0.801319 |   1.93x |
           | polars_bio-4 | 0.439225 | 0.458996 | 0.450230 |   3.44x |
           | polars_bio-6 | 0.320933 | 0.337937 | 0.331990 |   4.66x |
           | polars_bio-8 | 0.276917 | 0.457481 | 0.339130 |   4.56x |

           ## Benchmark coverage for coverage with dataset databio                                                                                                                                             run-benchmarks.py:86

[18:02:10]  Benchmark Results, operation: coverage dataset: databio,                                                                                                                                          run-benchmarks.py:418
                                    test: 8-7

           | Library      |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |--------------|----------|----------|----------|---------|
           | polars_bio   | 1.184437 | 1.193681 | 1.190128 |   1.00x |
           | polars_bio-2 | 0.626552 | 0.631670 | 0.629656 |   1.89x |
           | polars_bio-4 | 0.360965 | 0.366674 | 0.364691 |   3.26x |
           | polars_bio-6 | 0.258221 | 0.278457 | 0.270340 |   4.40x |
           | polars_bio-8 | 0.219943 | 0.230581 | 0.226905 |   5.25x |

