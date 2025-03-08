# polars-bio-bench
Benchmarks of various genomic ranges operations

Pre-requisites

* pyenv
```bash
➜  polars-bio-bench git:(init) ✗ pyenv --version
pyenv 2.5.0
```
* poetry
```bash
➜  polars-bio-bench git:(init) ✗ poetry --version
Poetry (version 2.0.0)
```
## Setup
```bash
pyenv install 3.12.8
pyenv local 3.12.8
poetry env use 3.12
poetry update
```

### Hardware requirements
Please note that you need at least 64GB of RAM to run the full benchmarks. For the default 16-32GB should be enough.

## Run
All the benchmarking scenarios are defined in the `conf/benchmark_*.yaml` files. By default, the `conf/benchmark_small.yaml` file is used.
If you would like to run the benchmarks with a different configuration file, you can specify it using the `--bench-config` option.
```bash
export BENCH_DATA_ROOT=/tmp/polars-bio-bench/

poetry run python src/run-benchmarks.py --help
INFO:polars_bio:Creating BioSessionContext
Usage: run-benchmarks.py [OPTIONS]

Options:
  --bench-config TEXT  Benchmark config file (default:
                       conf/benchmark_small.yaml)
  --help               Show this message and exit.

```

### Sample benchmark scenarios
 * `conf/benchmark_small.yaml` - small dataset, small number of operations for nearest and overlap, native DataFusion input
 * `conf/benchmark_dataframes.yaml` - as above but with DataFrames (Polars/Pandas) as input
 * `conf/benchmark_large.yaml` - large dataset, large number of operations for nearest and overlap, native DataFusion input
 * `conf/benchmark_parallel.yaml` - comparison parallel operations for pyranges0 and polars_bio with bioframe as a baseline
 * `conf/benchmark_count_overlaps.yaml` - comparison of count overlaps operation for pyranges{0,1} and polars_bio with bioframe as a baseline
 * `conf/benchmark_merge.yaml` - comparison of merge operation for pyranges{0,1} and polars_bio with bioframe as a baseline
 * `conf/benchmark_coverage.yaml` - comparison of coverage operation for pyranges{0,1} and polars_bio with bioframe as a baseline

