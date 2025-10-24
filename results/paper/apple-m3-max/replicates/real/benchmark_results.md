[19:30:22] ## Benchmark overlap for overlap with dataset databio                                                                                                                                                                                                  run-benchmarks.py:107

[19:30:29]  Benchmark Results, operation: overlap dataset: databio,                                                                                                                                                                                               run-benchmarks.py:476
                                   test: 7-3

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.200215 | 0.222133 | 0.209348 |   4.40x |
           | bioframe   | 0.912386 | 0.935237 | 0.921090 |   1.00x |
           | pyranges0  | 0.396694 | 0.434848 | 0.413098 |   2.23x |
           | pyranges1  | 0.690719 | 0.710924 | 0.700157 |   1.32x |

[19:32:45]   Benchmark Results, operation: overlap dataset: databio,                                                                                                                                                                                              run-benchmarks.py:476
                                    test: 0-8

           | Library    |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |------------|-----------|-----------|-----------|---------|
           | polars_bio |  1.767233 |  2.180063 |  1.941156 |   8.14x |
           | bioframe   | 15.607675 | 16.105240 | 15.806031 |   1.00x |
           | pyranges0  |  9.028246 |  9.278568 |  9.116237 |   1.73x |
           | pyranges1  | 16.141273 | 16.243732 | 16.183118 |   0.98x |

[19:32:49]  Benchmark Results, operation: overlap dataset: databio,                                                                                                                                                                                               run-benchmarks.py:476
                                   test: 1-0

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.090537 | 0.095694 | 0.093262 |   5.39x |
           | bioframe   | 0.498528 | 0.507002 | 0.502499 |   1.00x |
           | pyranges0  | 0.261368 | 0.287940 | 0.271472 |   1.85x |
           | pyranges1  | 0.392985 | 0.426657 | 0.412493 |   1.22x |

[19:36:03]   Benchmark Results, operation: overlap dataset: databio,                                                                                                                                                                                              run-benchmarks.py:476
                                    test: 4-8

           | Library    |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |------------|-----------|-----------|-----------|---------|
           | polars_bio |  2.564904 |  2.831996 |  2.677653 |   8.55x |
           | bioframe   | 22.246166 | 23.930289 | 22.881234 |   1.00x |
           | pyranges0  | 12.564652 | 12.946732 | 12.756828 |   1.79x |
           | pyranges1  | 22.928933 | 23.184763 | 23.081595 |   0.99x |

[19:54:50]  Benchmark Results, operation: overlap dataset: databio, test:                                                                                                                                                                                         run-benchmarks.py:476
                                         3-0

           | Library    |    Min (s) |    Max (s) |   Mean (s) | Speedup |
           |------------|------------|------------|------------|---------|
           | polars_bio |   8.081568 |  12.137477 |  10.184250 |  12.68x |
           | bioframe   | 120.309157 | 146.796864 | 129.143834 |   1.00x |
           | pyranges0  |  74.723421 |  76.591913 |  75.485290 |   1.71x |
           | pyranges1  | 145.429260 | 146.601740 | 145.914339 |   0.89x |

[19:54:56]  Benchmark Results, operation: overlap dataset: databio,                                                                                                                                                                                               run-benchmarks.py:476
                                   test: 2-3

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.128855 | 0.338951 | 0.203348 |   3.37x |
           | bioframe   | 0.679385 | 0.697892 | 0.685639 |   1.00x |
           | pyranges0  | 0.330337 | 0.361576 | 0.341795 |   2.01x |
           | pyranges1  | 0.536370 | 0.540087 | 0.538102 |   1.27x |

[19:55:14]  Benchmark Results, operation: overlap dataset: databio,                                                                                                                                                                                               run-benchmarks.py:476
                                   test: 4-2

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.600334 | 0.786014 | 0.666635 |   3.63x |
           | bioframe   | 2.377175 | 2.478303 | 2.418331 |   1.00x |
           | pyranges0  | 0.700737 | 0.807055 | 0.758352 |   3.19x |
           | pyranges1  | 1.404265 | 1.454845 | 1.432555 |   1.69x |

           ## Benchmark nearest for nearest with dataset databio                                                                                                                                                                                                  run-benchmarks.py:107

[19:55:25]  Benchmark Results, operation: nearest dataset: databio,                                                                                                                                                                                               run-benchmarks.py:476
                                   test: 7-3

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.220153 | 0.262372 | 0.236706 |   7.63x |
           | bioframe   | 1.741266 | 1.909801 | 1.805391 |   1.00x |
           | pyranges0  | 0.568548 | 0.647330 | 0.607074 |   2.97x |
           | pyranges1  | 0.758521 | 0.783880 | 0.771850 |   2.34x |

[19:57:22]   Benchmark Results, operation: nearest dataset: databio,                                                                                                                                                                                              run-benchmarks.py:476
                                    test: 0-8

           | Library    |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |------------|-----------|-----------|-----------|---------|
           | polars_bio |  1.156578 |  1.277890 |  1.212970 |  25.76x |
           | bioframe   | 30.945764 | 31.513268 | 31.240792 |   1.00x |
           | pyranges0  |  2.769026 |  2.954805 |  2.842411 |  10.99x |
           | pyranges1  |  3.178281 |  3.252540 |  3.227586 |   9.68x |

[19:57:28]  Benchmark Results, operation: nearest dataset: databio,                                                                                                                                                                                               run-benchmarks.py:476
                                   test: 1-0

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.095979 | 0.110348 | 0.103188 |   6.83x |
           | bioframe   | 0.691668 | 0.714308 | 0.704505 |   1.00x |
           | pyranges0  | 0.531339 | 0.585887 | 0.556175 |   1.27x |
           | pyranges1  | 0.613251 | 0.633949 | 0.626760 |   1.12x |

[19:59:54]   Benchmark Results, operation: nearest dataset: databio,                                                                                                                                                                                              run-benchmarks.py:476
                                    test: 4-8

           | Library    |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |------------|-----------|-----------|-----------|---------|
           | polars_bio |  1.782625 |  1.824964 |  1.800638 |  20.49x |
           | bioframe   | 36.552222 | 37.448433 | 36.892526 |   1.00x |
           | pyranges0  |  3.850678 |  3.892007 |  3.870412 |   9.53x |
           | pyranges1  |  4.916280 |  5.203312 |  5.023854 |   7.34x |

[20:05:23]  Benchmark Results, operation: nearest dataset: databio, test:                                                                                                                                                                                         run-benchmarks.py:476
                                         3-0

           | Library    |    Min (s) |    Max (s) |   Mean (s) | Speedup |
           |------------|------------|------------|------------|---------|
           | polars_bio |   0.920362 |   0.942113 |   0.930760 | 115.10x |
           | bioframe   | 106.301312 | 108.214897 | 107.133575 |   1.00x |
           | pyranges0  |   0.652080 |   0.695173 |   0.678523 | 157.89x |
           | pyranges1  |   0.873081 |   0.887810 |   0.878507 | 121.95x |

[20:05:30]  Benchmark Results, operation: nearest dataset: databio,                                                                                                                                                                                               run-benchmarks.py:476
                                   test: 2-3

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.116653 | 0.123563 | 0.119627 |   7.96x |
           | bioframe   | 0.929956 | 0.969509 | 0.951841 |   1.00x |
           | pyranges0  | 0.482174 | 0.503374 | 0.490538 |   1.94x |
           | pyranges1  | 0.587255 | 0.591904 | 0.589893 |   1.61x |

[20:05:59]  Benchmark Results, operation: nearest dataset: databio,                                                                                                                                                                                               run-benchmarks.py:476
                                   test: 4-2

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.659799 | 0.682241 | 0.670445 |   8.01x |
           | bioframe   | 5.293736 | 5.469513 | 5.367076 |   1.00x |
           | pyranges0  | 1.176025 | 1.306442 | 1.228992 |   4.37x |
           | pyranges1  | 2.104309 | 2.145562 | 2.126413 |   2.52x |

           ## Benchmark count-overlaps for count_overlaps with dataset databio                                                                                                                                                                                    run-benchmarks.py:107

[20:06:07]   Benchmark Results, operation: count_overlaps dataset:                                                                                                                                                                                                run-benchmarks.py:476
                              databio, test: 7-3

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.154149 | 0.163985 | 0.159832 |   7.52x |
           | bioframe   | 1.188614 | 1.228266 | 1.202618 |   1.00x |
           | pyranges0  | 0.415695 | 0.434500 | 0.424526 |   2.83x |
           | pyranges1  | 0.524324 | 0.544140 | 0.532293 |   2.26x |

[20:09:07]    Benchmark Results, operation: count_overlaps dataset:                                                                                                                                                                                               run-benchmarks.py:476
                                databio, test: 0-8

           | Library    |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |------------|-----------|-----------|-----------|---------|
           | polars_bio |  0.647103 |  0.653053 |  0.649550 |  75.26x |
           | bioframe   | 48.274281 | 49.364491 | 48.887211 |   1.00x |
           | pyranges0  |  4.818071 |  4.921056 |  4.862178 |  10.05x |
           | pyranges1  |  5.065523 |  5.122070 |  5.102034 |   9.58x |

[20:09:11]   Benchmark Results, operation: count_overlaps dataset:                                                                                                                                                                                                run-benchmarks.py:476
                              databio, test: 1-0

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.092007 | 0.094660 | 0.093680 |   5.84x |
           | bioframe   | 0.538049 | 0.558483 | 0.547176 |   1.00x |
           | pyranges0  | 0.275445 | 0.283689 | 0.280915 |   1.95x |
           | pyranges1  | 0.344748 | 0.352893 | 0.349026 |   1.57x |

[20:12:38]    Benchmark Results, operation: count_overlaps dataset:                                                                                                                                                                                               run-benchmarks.py:476
                                databio, test: 4-8

           | Library    |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |------------|-----------|-----------|-----------|---------|
           | polars_bio |  1.040516 |  1.047734 |  1.043240 |  50.79x |
           | bioframe   | 52.743948 | 53.194348 | 52.981064 |   1.00x |
           | pyranges0  |  6.935818 |  7.045903 |  6.983107 |   7.59x |
           | pyranges1  |  7.364518 |  7.451714 |  7.399304 |   7.16x |

[20:23:03] Benchmark Results, operation: count_overlaps dataset: databio,                                                                                                                                                                                         run-benchmarks.py:476
                                      test: 3-0

           | Library    |    Min (s) |    Max (s) |   Mean (s) | Speedup |
           |------------|------------|------------|------------|---------|
           | polars_bio |   0.617238 |   0.619040 |   0.618284 | 251.10x |
           | bioframe   | 152.560115 | 159.126999 | 155.248050 |   1.00x |
           | pyranges0  |  25.961310 |  26.082456 |  26.040234 |   5.96x |
           | pyranges1  |  25.799545 |  26.033198 |  25.918084 |   5.99x |

[20:23:08]   Benchmark Results, operation: count_overlaps dataset:                                                                                                                                                                                                run-benchmarks.py:476
                              databio, test: 2-3

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.097879 | 0.119281 | 0.105919 |   7.90x |
           | bioframe   | 0.830815 | 0.844694 | 0.836444 |   1.00x |
           | pyranges0  | 0.340924 | 0.347411 | 0.343539 |   2.43x |
           | pyranges1  | 0.390456 | 0.405657 | 0.397331 |   2.11x |

[20:23:28]   Benchmark Results, operation: count_overlaps dataset:                                                                                                                                                                                                run-benchmarks.py:476
                              databio, test: 4-2

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.403209 | 0.416641 | 0.408158 |   8.62x |
           | bioframe   | 3.501471 | 3.553667 | 3.519531 |   1.00x |
           | pyranges0  | 1.065134 | 1.129803 | 1.090222 |   3.23x |
           | pyranges1  | 1.317194 | 1.363398 | 1.341083 |   2.62x |

           ## Benchmark coverage for coverage with dataset databio                                                                                                                                                                                                run-benchmarks.py:107

[20:23:35] Benchmark Results, operation: coverage dataset: databio,                                                                                                                                                                                               run-benchmarks.py:476
                                   test: 7-3

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.100889 | 0.108216 | 0.103820 |   8.03x |
           | bioframe   | 0.790077 | 0.903074 | 0.833493 |   1.00x |
           | pyranges0  | 0.535388 | 0.560006 | 0.544381 |   1.53x |
           | pyranges1  | 0.739374 | 0.769016 | 0.749269 |   1.11x |

[20:24:24] Benchmark Results, operation: coverage dataset: databio,                                                                                                                                                                                               run-benchmarks.py:476
                                   test: 0-8

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.409347 | 0.473370 | 0.431078 |   7.39x |
           | bioframe   | 3.134288 | 3.220348 | 3.184673 |   1.00x |
           | pyranges0  | 5.590345 | 5.853159 | 5.699476 |   0.56x |
           | pyranges1  | 6.177614 | 6.318087 | 6.268886 |   0.51x |

[20:24:28] Benchmark Results, operation: coverage dataset: databio,                                                                                                                                                                                               run-benchmarks.py:476
                                   test: 1-0

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.064557 | 0.070229 | 0.066887 |   6.21x |
           | bioframe   | 0.412883 | 0.418646 | 0.415467 |   1.00x |
           | pyranges0  | 0.362041 | 0.368727 | 0.366392 |   1.13x |
           | pyranges1  | 0.514364 | 0.521139 | 0.517741 |   0.80x |

[20:25:40] Benchmark Results, operation: coverage dataset: databio,                                                                                                                                                                                               run-benchmarks.py:476
                                   test: 4-8

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.593232 | 0.603167 | 0.598824 |   9.53x |
           | bioframe   | 5.616444 | 5.762011 | 5.707860 |   1.00x |
           | pyranges0  | 7.728351 | 7.969978 | 7.885749 |   0.72x |
           | pyranges1  | 8.704718 | 8.817648 | 8.752228 |   0.65x |

[20:28:22]   Benchmark Results, operation: coverage dataset: databio,                                                                                                                                                                                             run-benchmarks.py:476
                                    test: 3-0

           | Library    |   Min (s) |   Max (s) |  Mean (s) | Speedup |
           |------------|-----------|-----------|-----------|---------|
           | polars_bio |  0.130734 |  0.132831 |  0.132030 |   8.94x |
           | bioframe   |  1.145848 |  1.228190 |  1.179978 |   1.00x |
           | pyranges0  | 26.170386 | 26.571433 | 26.435880 |   0.04x |
           | pyranges1  | 26.009510 | 26.121703 | 26.080100 |   0.05x |

[20:28:27] Benchmark Results, operation: coverage dataset: databio,                                                                                                                                                                                               run-benchmarks.py:476
                                   test: 2-3

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.068783 | 0.071337 | 0.069762 |   6.63x |
           | bioframe   | 0.460063 | 0.464570 | 0.462859 |   1.00x |
           | pyranges0  | 0.408624 | 0.411188 | 0.410261 |   1.13x |
           | pyranges1  | 0.549487 | 0.586788 | 0.568549 |   0.81x |

[20:28:52] Benchmark Results, operation: coverage dataset: databio,                                                                                                                                                                                               run-benchmarks.py:476
                                   test: 4-2

           | Library    |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |------------|----------|----------|----------|---------|
           | polars_bio | 0.385967 | 0.391327 | 0.388398 |  10.06x |
           | bioframe   | 3.808965 | 4.037969 | 3.906427 |   1.00x |
           | pyranges0  | 1.439572 | 1.500977 | 1.465785 |   2.67x |
           | pyranges1  | 2.005107 | 2.058748 | 2.032527 |   1.92x |

