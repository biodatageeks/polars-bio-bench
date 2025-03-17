[17:30:55] ## Benchmark overlap for overlap with dataset databio                                                                                                                                               run-benchmarks.py:86

[17:32:44]   Benchmark Results, operation: overlap dataset: databio,                                                                                                                                          run-benchmarks.py:418
                                    test: 8-7

           | Library      |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |--------------|----------|----------|----------|---------|
           | polars_bio   | 6.325617 | 8.185275 | 7.005925 |   1.00x |
           | polars_bio-2 | 3.920645 | 4.617084 | 4.198055 |   1.67x |
           | polars_bio-4 | 3.036273 | 3.060781 | 3.045200 |   2.30x |
           | polars_bio-6 | 2.127994 | 2.134505 | 2.131016 |   3.29x |
           | polars_bio-8 | 1.731485 | 1.789347 | 1.752986 |   4.00x |

           ## Benchmark nearest for nearest with dataset databio                                                                                                                                               run-benchmarks.py:86

[17:33:18]   Benchmark Results, operation: nearest dataset: databio,                                                                                                                                          run-benchmarks.py:418
                                    test: 8-7

           | Library      |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |--------------|----------|----------|----------|---------|
           | polars_bio   | 4.047329 | 4.439016 | 4.198198 |   1.00x |
           | polars_bio-2 | 2.624132 | 2.722843 | 2.682361 |   1.57x |
           | polars_bio-4 | 1.809028 | 1.917798 | 1.871763 |   2.24x |
           | polars_bio-6 | 1.309557 | 1.362131 | 1.333989 |   3.15x |
           | polars_bio-8 | 1.066945 | 1.113168 | 1.087907 |   3.86x |

           ## Benchmark count-overlaps for count_overlaps with dataset databio                                                                                                                                 run-benchmarks.py:86

[17:33:34]    Benchmark Results, operation: count_overlaps dataset:                                                                                                                                           run-benchmarks.py:418
                               databio, test: 8-7

           | Library      |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |--------------|----------|----------|----------|---------|
           | polars_bio   | 2.426441 | 2.456318 | 2.439266 |   1.00x |
           | polars_bio-2 | 1.225160 | 1.272066 | 1.245401 |   1.96x |
           | polars_bio-4 | 0.711421 | 0.744023 | 0.724315 |   3.37x |
           | polars_bio-6 | 0.563797 | 0.607321 | 0.580574 |   4.20x |
           | polars_bio-8 | 0.459308 | 0.493886 | 0.479126 |   5.09x |

           ## Benchmark coverage for coverage with dataset databio                                                                                                                                             run-benchmarks.py:86

[17:33:49]  Benchmark Results, operation: coverage dataset: databio,                                                                                                                                          run-benchmarks.py:418
                                    test: 8-7

           | Library      |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |--------------|----------|----------|----------|---------|
           | polars_bio   | 2.212958 | 2.230350 | 2.222531 |   1.00x |
           | polars_bio-2 | 1.132056 | 1.154050 | 1.146413 |   1.94x |
           | polars_bio-4 | 0.645737 | 0.661564 | 0.652277 |   3.41x |
           | polars_bio-6 | 0.505890 | 0.511256 | 0.508390 |   4.37x |
           | polars_bio-8 | 0.439503 | 0.450924 | 0.447075 |   4.97x |

