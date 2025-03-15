[08:40:58] ## Benchmark e2e-overlap-csv for e2e_overlap with dataset databio                                                                                                                                   run-benchmarks.py:92

[08:41:02]  Benchmark Results, operation: e2e_overlap dataset: databio, test:                                                                                                                                 run-benchmarks.py:454
                                           1-2

           | Library              |  Min (s) |  Max (s) | Mean (s) | Speedup |
           |----------------------|----------|----------|----------|---------|
           | polars_bio           | 0.042378 | 0.130957 | 0.071929 |   3.10x |
           | polars_bio_streaming | 0.035498 | 0.037438 | 0.036653 |   6.09x |
           | bioframe             | 0.208548 | 0.251457 | 0.223219 |   1.00x |
           | pyranges0            | 0.409707 | 0.415361 | 0.412135 |   0.54x |
           | pyranges1            | 0.475180 | 0.491508 | 0.482739 |   0.46x |

[09:35:14]   Benchmark Results, operation: e2e_overlap dataset: databio, test: 8-7                                                                                                                            run-benchmarks.py:454

           | Library              |    Min (s) |    Max (s) |   Mean (s) | Speedup |
           |----------------------|------------|------------|------------|---------|
           | polars_bio           |  22.781745 |  23.916568 |  23.161559 |  16.64x |
           | polars_bio_streaming |  18.501279 |  18.797602 |  18.676707 |  20.63x |
           | bioframe             | 383.108514 | 387.500069 | 385.309331 |   1.00x |
           | pyranges0            | 276.421312 | 279.839508 | 277.845198 |   1.39x |
           | pyranges1            | 355.703878 | 367.680249 | 360.875151 |   1.07x |

