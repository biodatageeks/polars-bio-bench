[18:34:14] ## Benchmark overlap-single-4tools for overlap with dataset databio                                                                                                 run-benchmarks.py:122

[18:34:15]   Benchmark Results, operation: overlap dataset: databio,                                                                                                           run-benchmarks.py:510
                                    test: 1-2

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.028936 | 0.038268 | 0.032794 |   1.00x |
           | pyranges1     | 0.043439 | 0.049034 | 0.045346 |   0.72x |
           | genomicranges | 0.018218 | 0.019594 | 0.018833 |   1.74x |
           | bioframe      | 0.110580 | 0.113586 | 0.111732 |   0.29x |

[18:34:16]   Benchmark Results, operation: overlap dataset: databio,                                                                                                           run-benchmarks.py:510
                                    test: 2-1

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.035498 | 0.037476 | 0.036722 |   1.00x |
           | pyranges1     | 0.043780 | 0.044451 | 0.044033 |   0.83x |
           | genomicranges | 0.018029 | 0.019202 | 0.018569 |   1.98x |
           | bioframe      | 0.108587 | 0.108976 | 0.108723 |   0.34x |

[18:34:22]   Benchmark Results, operation: overlap dataset: databio,                                                                                                           run-benchmarks.py:510
                                    test: 3-7

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.199771 | 0.207562 | 0.202599 |   1.00x |
           | pyranges1     | 0.521392 | 0.537319 | 0.529443 |   0.38x |
           | genomicranges | 0.243421 | 0.247851 | 0.245982 |   0.82x |
           | bioframe      | 0.984643 | 1.015430 | 1.000765 |   0.20x |

[18:34:29]   Benchmark Results, operation: overlap dataset: databio,                                                                                                           run-benchmarks.py:510
                                    test: 7-3

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.199167 | 0.204863 | 0.202769 |   1.00x |
           | pyranges1     | 0.514221 | 0.520300 | 0.516434 |   0.39x |
           | genomicranges | 0.366392 | 0.373131 | 0.368686 |   0.55x |
           | bioframe      | 0.977936 | 0.991472 | 0.984231 |   0.21x |

[18:34:37]   Benchmark Results, operation: overlap dataset: databio,                                                                                                           run-benchmarks.py:510
                                    test: 7-8

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.195990 | 0.206468 | 0.201882 |   1.00x |
           | pyranges1     | 0.521395 | 0.528779 | 0.525874 |   0.38x |
           | genomicranges | 0.366967 | 0.373943 | 0.369597 |   0.55x |
           | bioframe      | 0.981377 | 0.995773 | 0.990414 |   0.20x |

[18:38:18]  Benchmark Results, operation: overlap dataset: databio, test:                                                                                                      run-benchmarks.py:510
                                         8-7

           | Library       |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |---------------|-----------|-----------|-----------|---------|
           | polars_bio    |  4.361992 |  4.453583 |  4.403671 |   1.00x |
           | pyranges1     | 22.002710 | 27.179457 | 24.524774 |   0.18x |
           | genomicranges |  5.569787 |  6.771170 |  6.009197 |   0.73x |
           | bioframe      | 30.582480 | 40.018276 | 34.033871 |   0.13x |

           ## Benchmark nearest-single-4tools for nearest with dataset databio                                                                                                 run-benchmarks.py:122

[18:38:20]   Benchmark Results, operation: nearest dataset: databio,                                                                                                           run-benchmarks.py:510
                                    test: 1-2

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.042563 | 0.052281 | 0.046509 |   1.00x |
           | pyranges1     | 0.087620 | 0.090224 | 0.088784 |   0.52x |
           | genomicranges | 0.062736 | 0.067257 | 0.064379 |   0.72x |
           | bioframe      | 0.207649 | 0.213450 | 0.210654 |   0.22x |

[18:38:21]   Benchmark Results, operation: nearest dataset: databio,                                                                                                           run-benchmarks.py:510
                                    test: 2-1

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.048485 | 0.049860 | 0.048967 |   1.00x |
           | pyranges1     | 0.102571 | 0.106125 | 0.104037 |   0.47x |
           | genomicranges | 0.038705 | 0.040618 | 0.039601 |   1.24x |
           | bioframe      | 0.300209 | 0.324331 | 0.308300 |   0.16x |

[18:38:34]   Benchmark Results, operation: nearest dataset: databio,                                                                                                           run-benchmarks.py:510
                                    test: 3-7

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.278205 | 0.300924 | 0.286764 |   1.00x |
           | pyranges1     | 1.189684 | 1.237277 | 1.206616 |   0.24x |
           | genomicranges | 0.250873 | 0.255593 | 0.252685 |   1.13x |
           | bioframe      | 2.069018 | 2.081794 | 2.076468 |   0.14x |

[18:38:44]   Benchmark Results, operation: nearest dataset: databio,                                                                                                           run-benchmarks.py:510
                                    test: 7-3

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.251478 | 0.265760 | 0.259197 |   1.00x |
           | pyranges1     | 0.865958 | 0.877741 | 0.871034 |   0.30x |
           | genomicranges | 0.333628 | 0.336944 | 0.335259 |   0.77x |
           | bioframe      | 1.690321 | 1.715582 | 1.706313 |   0.15x |

[18:38:55]   Benchmark Results, operation: nearest dataset: databio,                                                                                                           run-benchmarks.py:510
                                    test: 7-8

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.256689 | 0.266380 | 0.261130 |   1.00x |
           | pyranges1     | 0.858691 | 0.878073 | 0.868218 |   0.30x |
           | genomicranges | 0.334291 | 0.341414 | 0.338776 |   0.77x |
           | bioframe      | 1.675093 | 1.724964 | 1.696286 |   0.15x |

[18:45:11]  Benchmark Results, operation: nearest dataset: databio, test:                                                                                                      run-benchmarks.py:510
                                         8-7

           | Library       |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |---------------|-----------|-----------|-----------|---------|
           | polars_bio    |  2.627357 |  2.709195 |  2.663066 |   1.00x |
           | pyranges1     | 42.257371 | 47.116624 | 44.304117 |   0.06x |
           | genomicranges |  1.610249 |  1.659889 |  1.629660 |   1.63x |
           | bioframe      | 73.147450 | 73.619109 | 73.456578 |   0.04x |

           ## Benchmark count_overlaps-single-4tools for count_overlaps with dataset databio                                                                                   run-benchmarks.py:122

[18:45:15]    Benchmark Results, operation: count_overlaps dataset:                                                                                                            run-benchmarks.py:510
                                databio, test: 1-2

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.024774 | 0.037235 | 0.029450 |   1.00x |
           | pyranges1     | 0.042595 | 0.047459 | 0.045425 |   0.65x |
           | genomicranges | 0.020207 | 0.022569 | 0.021187 |   1.39x |
           | bioframe      | 0.158036 | 0.166181 | 0.161498 |   0.18x |

[18:45:16]    Benchmark Results, operation: count_overlaps dataset:                                                                                                            run-benchmarks.py:510
                                databio, test: 2-1

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.029707 | 0.031111 | 0.030284 |   1.00x |
           | pyranges1     | 0.044984 | 0.046234 | 0.045544 |   0.66x |
           | genomicranges | 0.022618 | 0.024365 | 0.023739 |   1.28x |
           | bioframe      | 0.190925 | 0.201636 | 0.197508 |   0.15x |

[18:45:24]    Benchmark Results, operation: count_overlaps dataset:                                                                                                            run-benchmarks.py:510
                                databio, test: 3-7

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.143885 | 0.153324 | 0.147127 |   1.00x |
           | pyranges1     | 0.314493 | 0.322636 | 0.318886 |   0.46x |
           | genomicranges | 0.298148 | 0.299242 | 0.298578 |   0.49x |
           | bioframe      | 1.610782 | 1.700885 | 1.654848 |   0.09x |

[18:45:31]    Benchmark Results, operation: count_overlaps dataset:                                                                                                            run-benchmarks.py:510
                                databio, test: 7-3

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.133004 | 0.139156 | 0.136089 |   1.00x |
           | pyranges1     | 0.311841 | 0.314443 | 0.313402 |   0.43x |
           | genomicranges | 0.420214 | 0.426318 | 0.423974 |   0.32x |
           | bioframe      | 1.299018 | 1.328843 | 1.310574 |   0.10x |

[18:45:38]    Benchmark Results, operation: count_overlaps dataset:                                                                                                            run-benchmarks.py:510
                                databio, test: 7-8

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.134406 | 0.137607 | 0.135598 |   1.00x |
           | pyranges1     | 0.310137 | 0.316331 | 0.312380 |   0.43x |
           | genomicranges | 0.416677 | 0.418342 | 0.417503 |   0.32x |
           | bioframe      | 1.305494 | 1.340924 | 1.325137 |   0.10x |

[18:51:03] Benchmark Results, operation: count_overlaps dataset: databio,                                                                                                      run-benchmarks.py:510
                                      test: 8-7

           | Library       |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |---------------|-----------|-----------|-----------|---------|
           | polars_bio    |  1.529389 |  1.572387 |  1.554115 |   1.00x |
           | pyranges1     |  6.493528 |  6.557687 |  6.522070 |   0.24x |
           | genomicranges |  8.292888 |  8.344869 |  8.312885 |   0.19x |
           | bioframe      | 89.612161 | 92.417743 | 91.066487 |   0.02x |

           ## Benchmark coverage-single-4tools for coverage with dataset databio                                                                                               run-benchmarks.py:122

[18:51:13]   Benchmark Results, operation: coverage dataset: databio,                                                                                                          run-benchmarks.py:510
                                    test: 1-2

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.023627 | 0.028958 | 0.025476 |   1.00x |
           | genomicranges | 2.950809 | 3.043073 | 2.983638 |   0.01x |
           | bioframe      | 0.194362 | 0.199102 | 0.197285 |   0.13x |

[18:51:23]   Benchmark Results, operation: coverage dataset: databio,                                                                                                          run-benchmarks.py:510
                                    test: 2-1

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.032870 | 0.033753 | 0.033189 |   1.00x |
           | genomicranges | 2.856622 | 2.916637 | 2.883608 |   0.01x |
           | bioframe      | 0.288977 | 0.300123 | 0.295489 |   0.11x |

[18:51:39]   Benchmark Results, operation: coverage dataset: databio,                                                                                                          run-benchmarks.py:510
                                    test: 3-7

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.137977 | 0.146281 | 0.141597 |   1.00x |
           | genomicranges | 3.370454 | 3.413056 | 3.389711 |   0.04x |
           | bioframe      | 1.423067 | 1.482548 | 1.457209 |   0.10x |

[18:51:54]   Benchmark Results, operation: coverage dataset: databio,                                                                                                          run-benchmarks.py:510
                                    test: 7-3

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.082493 | 0.088217 | 0.084966 |   1.00x |
           | genomicranges | 3.685924 | 3.755402 | 3.730644 |   0.02x |
           | bioframe      | 0.951276 | 1.001568 | 0.976343 |   0.09x |

[18:52:09]   Benchmark Results, operation: coverage dataset: databio,                                                                                                          run-benchmarks.py:510
                                    test: 7-8

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.081963 | 0.086746 | 0.084234 |   1.00x |
           | genomicranges | 3.715615 | 3.733771 | 3.727649 |   0.02x |
           | bioframe      | 0.934695 | 0.947705 | 0.941544 |   0.09x |

[18:53:41] Benchmark Results, operation: coverage dataset: databio, test:                                                                                                      run-benchmarks.py:510
                                         8-7

           | Library       |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |---------------|-----------|-----------|-----------|---------|
           | polars_bio    |  1.194831 |  1.214221 |  1.203526 |   1.00x |
           | genomicranges |  3.315165 |  3.392603 |  3.362900 |   0.36x |
           | bioframe      | 25.272138 | 25.387094 | 25.323171 |   0.05x |

           ## Benchmark merge-single-3tools for merge with dataset databio                                                                                                     run-benchmarks.py:122

[18:56:28] Benchmark Results, operation: merge dataset: databio, test: 5-1                                                                                                     run-benchmarks.py:510

           | Library       |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |---------------|-----------|-----------|-----------|---------|
           | polars_bio    |  0.761094 |  0.881909 |  0.809541 |   1.00x |
           | bioframe      |  8.014142 |  8.200274 |  8.083652 |   0.10x |
           | pyranges1     |  3.566200 |  3.577657 |  3.573658 |   0.23x |
           | genomicranges | 39.380598 | 39.496033 | 39.445994 |   0.02x |

[18:56:30] Benchmark Results, operation: merge dataset: databio, test:                                                                                                         run-benchmarks.py:510
                                       1-2

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.007570 | 0.011930 | 0.009051 |   1.00x |
           | bioframe      | 0.036626 | 0.037658 | 0.037089 |   0.24x |
           | pyranges1     | 0.013098 | 0.013953 | 0.013453 |   0.67x |
           | genomicranges | 0.409088 | 0.420049 | 0.413040 |   0.02x |

[18:56:33] Benchmark Results, operation: merge dataset: databio, test:                                                                                                         run-benchmarks.py:510
                                       2-1

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.012575 | 0.013395 | 0.012872 |   1.00x |
           | bioframe      | 0.066743 | 0.071896 | 0.069333 |   0.19x |
           | pyranges1     | 0.027578 | 0.028891 | 0.028217 |   0.46x |
           | genomicranges | 0.622420 | 0.630404 | 0.627667 |   0.02x |

[18:56:40] Benchmark Results, operation: merge dataset: databio, test:                                                                                                         run-benchmarks.py:510
                                       3-7

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.031628 | 0.037189 | 0.033742 |   1.00x |
           | bioframe      | 0.328191 | 0.347511 | 0.340524 |   0.10x |
           | pyranges1     | 0.118971 | 0.126976 | 0.124041 |   0.27x |
           | genomicranges | 1.531683 | 1.658074 | 1.579478 |   0.02x |

[18:56:46] Benchmark Results, operation: merge dataset: databio, test:                                                                                                         run-benchmarks.py:510
                                       7-3

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.047582 | 0.068433 | 0.055429 |   1.00x |
           | bioframe      | 0.187000 | 0.248271 | 0.207648 |   0.27x |
           | pyranges1     | 0.075129 | 0.077690 | 0.076433 |   0.73x |
           | genomicranges | 1.356467 | 1.389175 | 1.370189 |   0.04x |

[18:56:51] Benchmark Results, operation: merge dataset: databio, test:                                                                                                         run-benchmarks.py:510
                                       7-8

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.043363 | 0.044113 | 0.043715 |   1.00x |
           | bioframe      | 0.174348 | 0.181267 | 0.178237 |   0.25x |
           | pyranges1     | 0.076778 | 0.077868 | 0.077211 |   0.57x |
           | genomicranges | 1.360457 | 1.372662 | 1.366979 |   0.03x |

[18:57:44] Benchmark Results, operation: merge dataset: databio, test: 8-7                                                                                                     run-benchmarks.py:510

           | Library       |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |---------------|-----------|-----------|-----------|---------|
           | polars_bio    |  0.298890 |  0.309353 |  0.303081 |   1.00x |
           | bioframe      |  2.404101 |  2.493700 |  2.457382 |   0.12x |
           | pyranges1     |  0.588877 |  0.598713 |  0.594331 |   0.51x |
           | genomicranges | 12.894173 | 13.664537 | 13.197781 |   0.02x |

           ## Benchmark cluster-single-3tools for cluster with dataset databio                                                                                                 run-benchmarks.py:122

[18:58:27]  Benchmark Results, operation: cluster dataset: databio,                                                                                                            run-benchmarks.py:510
                                   test: 5-1

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 1.735250 | 1.745132 | 1.740618 |   1.00x |
           | bioframe   | 7.950163 | 8.238409 | 8.097720 |   0.21x |
           | pyranges1  | 3.861925 | 3.991190 | 3.905789 |   0.45x |

            Benchmark Results, operation: cluster dataset: databio,                                                                                                            run-benchmarks.py:510
                                   test: 1-2

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.009088 | 0.013972 | 0.011125 |   1.00x |
           | bioframe   | 0.037525 | 0.041250 | 0.038996 |   0.29x |
           | pyranges1  | 0.013110 | 0.014884 | 0.013981 |   0.80x |

[18:58:28]  Benchmark Results, operation: cluster dataset: databio,                                                                                                            run-benchmarks.py:510
                                   test: 2-1

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.019824 | 0.022064 | 0.020688 |   1.00x |
           | bioframe   | 0.066246 | 0.075719 | 0.069902 |   0.30x |
           | pyranges1  | 0.026034 | 0.026728 | 0.026364 |   0.78x |

[18:58:30]  Benchmark Results, operation: cluster dataset: databio,                                                                                                            run-benchmarks.py:510
                                   test: 3-7

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.073082 | 0.079643 | 0.075337 |   1.00x |
           | bioframe   | 0.322518 | 0.340875 | 0.331939 |   0.23x |
           | pyranges1  | 0.133313 | 0.138702 | 0.135869 |   0.55x |

[18:58:31]  Benchmark Results, operation: cluster dataset: databio,                                                                                                            run-benchmarks.py:510
                                   test: 7-3

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.063069 | 0.066934 | 0.064671 |   1.00x |
           | bioframe   | 0.162938 | 0.176500 | 0.169522 |   0.38x |
           | pyranges1  | 0.080858 | 0.082413 | 0.081515 |   0.79x |

[18:58:32]  Benchmark Results, operation: cluster dataset: databio,                                                                                                            run-benchmarks.py:510
                                   test: 7-8

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.062570 | 0.064995 | 0.063843 |   1.00x |
           | bioframe   | 0.175119 | 0.192346 | 0.182545 |   0.35x |
           | pyranges1  | 0.079098 | 0.079647 | 0.079343 |   0.80x |

[18:58:44]  Benchmark Results, operation: cluster dataset: databio,                                                                                                            run-benchmarks.py:510
                                   test: 8-7

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.473616 | 0.510887 | 0.488205 |   1.00x |
           | bioframe   | 2.410919 | 2.466561 | 2.434142 |   0.20x |
           | pyranges1  | 0.783368 | 0.812884 | 0.796963 |   0.61x |

           ## Benchmark complement-single-3tools for complement with dataset databio                                                                                           run-benchmarks.py:122

[19:02:04]   Benchmark Results, operation: complement dataset: databio,                                                                                                        run-benchmarks.py:510
                                      test: 5-1

           | Library       |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |---------------|-----------|-----------|-----------|---------|
           | polars_bio    |  0.736799 |  0.832063 |  0.770759 |   1.00x |
           | bioframe      | 21.938314 | 22.767620 | 22.254110 |   0.03x |
           | pyranges1     |  3.132103 |  3.139368 |  3.134913 |   0.25x |
           | genomicranges | 36.791966 | 36.854441 | 36.816021 |   0.02x |

[19:02:06]  Benchmark Results, operation: complement dataset: databio,                                                                                                         run-benchmarks.py:510
                                    test: 1-2

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.007402 | 0.009665 | 0.008157 |   1.00x |
           | bioframe      | 0.104588 | 0.107486 | 0.105673 |   0.08x |
           | pyranges1     | 0.015252 | 0.016353 | 0.015949 |   0.51x |
           | genomicranges | 0.374328 | 0.380545 | 0.376992 |   0.02x |

[19:02:09]  Benchmark Results, operation: complement dataset: databio,                                                                                                         run-benchmarks.py:510
                                    test: 2-1

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.011849 | 0.013226 | 0.012339 |   1.00x |
           | bioframe      | 0.183789 | 0.193621 | 0.188521 |   0.07x |
           | pyranges1     | 0.029244 | 0.030756 | 0.029754 |   0.41x |
           | genomicranges | 0.573768 | 0.578593 | 0.576642 |   0.02x |

[19:02:17]  Benchmark Results, operation: complement dataset: databio,                                                                                                         run-benchmarks.py:510
                                    test: 3-7

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.031141 | 0.036951 | 0.033140 |   1.00x |
           | bioframe      | 0.865023 | 0.885029 | 0.875449 |   0.04x |
           | pyranges1     | 0.110823 | 0.121385 | 0.115787 |   0.29x |
           | genomicranges | 1.441060 | 1.460203 | 1.449572 |   0.02x |

[19:02:23]  Benchmark Results, operation: complement dataset: databio,                                                                                                         run-benchmarks.py:510
                                    test: 7-3

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.040543 | 0.041311 | 0.040978 |   1.00x |
           | bioframe      | 0.476319 | 0.489923 | 0.483830 |   0.08x |
           | pyranges1     | 0.071276 | 0.072858 | 0.072120 |   0.57x |
           | genomicranges | 1.246462 | 1.257000 | 1.252709 |   0.03x |

[19:02:30]  Benchmark Results, operation: complement dataset: databio,                                                                                                         run-benchmarks.py:510
                                    test: 7-8

           | Library       |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |---------------|----------|----------|----------|---------|
           | polars_bio    | 0.039871 | 0.041037 | 0.040323 |   1.00x |
           | bioframe      | 0.468496 | 0.482247 | 0.475617 |   0.08x |
           | pyranges1     | 0.072003 | 0.078775 | 0.075762 |   0.53x |
           | genomicranges | 1.251609 | 1.290483 | 1.268181 |   0.03x |

[19:03:26]   Benchmark Results, operation: complement dataset: databio,                                                                                                        run-benchmarks.py:510
                                      test: 8-7

           | Library       |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |---------------|-----------|-----------|-----------|---------|
           | polars_bio    |  0.288371 |  0.293229 |  0.290854 |   1.00x |
           | bioframe      |  5.079455 |  5.137270 |  5.117035 |   0.06x |
           | pyranges1     |  0.542777 |  0.546701 |  0.544945 |   0.53x |
           | genomicranges | 11.762000 | 12.295385 | 12.105526 |   0.02x |

           ## Benchmark subtract-single-3tools for subtract with dataset databio                                                                                               run-benchmarks.py:122

[19:05:34] Benchmark Results, operation: subtract dataset: databio, test:                                                                                                      run-benchmarks.py:510
                                         1-2

           | Library       |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |---------------|-----------|-----------|-----------|---------|
           | polars_bio    |  0.016597 |  0.018587 |  0.017679 |   1.00x |
           | bioframe      |  0.385833 |  0.397739 |  0.393629 |   0.04x |
           | pyranges1     |  0.045605 |  0.046230 |  0.045999 |   0.38x |
           | genomicranges | 41.946304 | 42.058249 | 42.019365 |   0.00x |

[19:09:12] Benchmark Results, operation: subtract dataset: databio, test:                                                                                                      run-benchmarks.py:510
                                         2-1

           | Library       |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |---------------|-----------|-----------|-----------|---------|
           | polars_bio    |  0.020220 |  0.022110 |  0.021300 |   1.00x |
           | bioframe      |  0.432496 |  0.436250 |  0.434262 |   0.05x |
           | pyranges1     |  0.051087 |  0.053831 |  0.052788 |   0.40x |
           | genomicranges | 71.632908 | 72.186910 | 71.891232 |   0.00x |

[19:43:07] Benchmark Results, operation: subtract dataset: databio, test: 3-7                                                                                                  run-benchmarks.py:510

           | Library       |    Min (s) |    Max (s) |   Mean (s) | Speedup |
           |---------------|------------|------------|------------|---------|
           | polars_bio    |   0.116777 |   0.124259 |   0.121036 |   1.00x |
           | bioframe      |   2.114580 |   2.186240 |   2.142240 |   0.06x |
           | pyranges1     |   0.364630 |   0.370571 |   0.368206 |   0.33x |
           | genomicranges | 671.490013 | 679.209374 | 675.433468 |   0.00x |

[20:43:48]  Benchmark Results, operation: subtract dataset: databio, test: 7-3                                                                                                 run-benchmarks.py:510

           | Library       |     Min (s) |     Max (s) |    Mean (s) | Speedup |
           |---------------|-------------|-------------|-------------|---------|
           | polars_bio    |    0.539986 |    0.550802 |    0.544779 |   1.00x |
           | bioframe      |    1.620771 |    1.634901 |    1.629450 |   0.33x |
           | pyranges1     |    0.220759 |    0.227925 |    0.224777 |   2.42x |
           | genomicranges | 1204.252273 | 1215.624717 | 1211.213090 |   0.00x |

[21:44:14]  Benchmark Results, operation: subtract dataset: databio, test: 7-8                                                                                                 run-benchmarks.py:510

           | Library       |     Min (s) |     Max (s) |    Mean (s) | Speedup |
           |---------------|-------------|-------------|-------------|---------|
           | polars_bio    |    0.541180 |    0.552357 |    0.544947 |   1.00x |
           | bioframe      |    1.551784 |    1.631252 |    1.591499 |   0.34x |
           | pyranges1     |    0.234128 |    0.240824 |    0.236386 |   2.31x |
           | genomicranges | 1204.213268 | 1208.295047 | 1206.064836 |   0.00x |

[21:44:14]  Benchmark Results, operation: subtract dataset: databio, test: 8-7

           | Library    |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |------------|-----------|-----------|-----------|---------|
           | polars_bio |  1.105731 |  1.254162 |  1.163900 |   1.00x |
           | bioframe   | 25.271473 | 25.877168 | 25.658833 |   0.05x |
           | pyranges1  |  5.058301 |  5.090548 |  5.069764 |   0.23x |


[09:13:36]   Benchmark Results, operation: subtract dataset: databio,                                                                                                         run-benchmarks.py:510
test: 5-1

           | Library    |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |------------|-----------|-----------|-----------|---------|
           | polars_bio |  1.489116 |  1.561817 |  1.519482 |   1.00x |
           | bioframe   | 35.429718 | 35.606569 | 35.505508 |   0.04x |
           | pyranges1  |  5.533196 |  5.648918 |  5.594587 |   0.27x |
