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
pip install poetry-plugin-shell
poetry shell
python src/run-benchmarks.py
```

## Run
```bash
# export dir where the benchmark data set will be downloaded
export BENCH_DATA_ROOT=/tmp/databio
```