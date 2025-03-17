[07:53:49] ## Benchmark e2e-overlap-csv for e2e_overlap with dataset databio                                                                                                                                   run-benchmarks.py:92

[07:53:54]  Benchmark Results, operation: e2e_overlap dataset: databio, test:                                                                                                                                 run-benchmarks.py:454
                                           1-2

           | Library              |  Min (s) |  Max (s) | Mean (s) | Speedup | Peak memory (MB) |
           |----------------------|----------|----------|----------|---------|------------------|
           | polars_bio           | 0.072393 | 0.151871 | 0.099160 |   2.80x | 314.234          |
           | polars_bio_streaming | 0.064092 | 0.067914 | 0.066202 |   4.19x | 288.621          |
           | bioframe             | 0.258278 | 0.312880 | 0.277225 |   1.00x | 287.101          |
           | pyranges0            | 0.591745 | 0.599954 | 0.595204 |   0.47x | 307.218          |
           | pyranges1            | 0.683388 | 0.702289 | 0.690362 |   0.40x | 327.863          |


[09:16:07]   Benchmark Results, operation: e2e_overlap dataset: databio, test: 8-7                                                                                                                            run-benchmarks.py:454

           | Library              |    Min (s) |    Max (s) |   Mean (s) | Speedup | Peak memory (MB) |
           |----------------------|------------|------------|------------|---------|------------------|
           | polars_bio           |  44.539766 |  45.543038 |  45.196903 |  12.55x | 14575.140        |
           | polars_bio_streaming |  34.007093 |  35.972075 |  35.309756 |  16.06x | 480.207          |
           | bioframe             | 566.167037 | 567.617695 | 567.130690 |   1.00x | 43295.378        |
           | pyranges0            | 417.291061 | 421.875539 | 419.571591 |   1.35x | 22915.917        |
           | pyranges1            | 538.365637 | 548.624613 | 543.918168 |   1.04x | 43408.699        |

