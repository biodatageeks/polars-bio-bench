[06:20:21] ## Benchmark overlap for overlap with dataset databio                                                                                                                                               run-benchmarks.py:86

[06:21:13]   Benchmark Results, operation: overlap dataset: databio,                                                                                                                                          run-benchmarks.py:418
                                    test: 8-7

           | Library      |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |--------------|----------|----------|----------|---------|
           | polars_bio   | 3.631019 | 4.222567 | 3.836674 |   1.00x |
           | polars_bio-2 | 1.866739 | 1.947024 | 1.901366 |   2.02x |
           | polars_bio-4 | 1.160112 | 1.171989 | 1.164340 |   3.30x |
           | polars_bio-6 | 0.983742 | 0.994754 | 0.988346 |   3.88x |
           | polars_bio-8 | 0.704727 | 0.722828 | 0.712285 |   5.39x |

           ## Benchmark nearest for nearest with dataset databio                                                                                                                                               run-benchmarks.py:86

[06:21:30]   Benchmark Results, operation: nearest dataset: databio,                                                                                                                                          run-benchmarks.py:418
                                    test: 8-7

           | Library      |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |--------------|----------|----------|----------|---------|
           | polars_bio   | 2.352758 | 2.503053 | 2.415894 |   1.00x |
           | polars_bio-2 | 1.208868 | 1.297379 | 1.247201 |   1.94x |
           | polars_bio-4 | 0.739411 | 0.760896 | 0.748205 |   3.23x |
           | polars_bio-6 | 0.659575 | 0.670452 | 0.664539 |   3.64x |
           | polars_bio-8 | 0.461611 | 0.478764 | 0.467581 |   5.17x |

           ## Benchmark count-overlaps for count_overlaps with dataset databio                                                                                                                                 run-benchmarks.py:86

[06:21:40]    Benchmark Results, operation: count_overlaps dataset:                                                                                                                                           run-benchmarks.py:418
                               databio, test: 8-7

           | Library      |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |--------------|----------|----------|----------|---------|
           | polars_bio   | 1.547673 | 1.557833 | 1.552131 |   1.00x |
           | polars_bio-2 | 0.793873 | 0.803828 | 0.798642 |   1.94x |
           | polars_bio-4 | 0.453521 | 0.460848 | 0.457059 |   3.40x |
           | polars_bio-6 | 0.334935 | 0.341904 | 0.338485 |   4.59x |
           | polars_bio-8 | 0.280059 | 0.280591 | 0.280255 |   5.54x |

           ## Benchmark coverage for coverage with dataset databio                                                                                                                                             run-benchmarks.py:86

[06:21:48]  Benchmark Results, operation: coverage dataset: databio,                                                                                                                                          run-benchmarks.py:418
                                    test: 8-7

           | Library      |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |--------------|----------|----------|----------|---------|
           | polars_bio   | 1.206831 | 1.219476 | 1.213735 |   1.00x |
           | polars_bio-2 | 0.637306 | 0.644183 | 0.640547 |   1.89x |
           | polars_bio-4 | 0.368383 | 0.371543 | 0.369612 |   3.28x |
           | polars_bio-6 | 0.275598 | 0.281646 | 0.277798 |   4.37x |
           | polars_bio-8 | 0.221916 | 0.235038 | 0.229151 |   5.30x |

