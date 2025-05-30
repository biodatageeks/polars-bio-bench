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

For e2e test suite ([benchmark-e2e-overlap](conf/paper/benchmark-e2e-overlap.yaml)) please additionally set :
```bash
export POLARS_MAX_THREADS=1
```


### Datasets
[Datasets overview](https://biodatageeks.org/polars-bio/performance/#test-datasets)

### Sample benchmark scenarios
 * `conf/benchmark_small.yaml` - small dataset, small number of operations for nearest and overlap, native DataFusion input
 * `conf/benchmark_dataframes.yaml` - as above but with DataFrames (Polars/Pandas) as input
 * `conf/benchmark_large.yaml` - large dataset, large number of operations for nearest and overlap, native DataFusion input
 * `conf/benchmark_parallel.yaml` - comparison parallel operations for pyranges0 and polars_bio with bioframe as a baseline
 * `conf/benchmark_count_overlaps.yaml` - comparison of count overlaps operation for pyranges{0,1} and polars_bio with bioframe as a baseline
 * `conf/benchmark_merge.yaml` - comparison of merge operation for pyranges{0,1} and polars_bio with bioframe as a baseline
 * `conf/benchmark_coverage.yaml` - comparison of coverage operation for pyranges{0,1} and polars_bio with bioframe as a baseline


### Paper benchmarks
* `conf/paper/benchmark-e2e-overlap.yaml` - end-to-end benchmark for overlap operation with writing results to a CSV file (1-2 and 8-7 datasets)
* `conf/paper/benchmark-4ops-1-2.yaml` - overlap, nearest, count_overlaps and coverage operations for 1-2 datasets
* `conf/paper/benchmark-4ops-8-7.yaml` - as above but for 8-7 datasets
* `conf/paper/benchmark-4ops-8-7-polars-bio-parallel.yaml` - as above but polars_bio only and  with parallel operations 1,2,4,6,8 threads
* `conf/paper/benchmark-read_vcf.yaml` - read VCF file with polars_bio and  1,2,4,6,8 threads

### Paper memory benchmarks
Example of running memory profiler for polars_bio with 1-2 dataset for polars_bio:
```bash
PRFOF_FILE="polars_bio_1-2.dat"
mprof run --output $PRFOF_FILE python src/run-memory-profiler.py --bench-config conf/paper/benchmark-e2e-overlap.yaml --tool polars_bio --test-case 1-2
mprof plot $PRFOF_FILE
```

```bash
for tool in "polars_bio" "polars_bio_streaming" "bioframe" "pyranges0" "pyranges1"; do
    for test_case in "8-7"; do
        PRFOF_FILE="${tool}_${test_case}.dat"
        mprof run --output $PRFOF_FILE python src/run-memory-profiler.py --bench-config conf/paper/benchmark-e2e-overlap.yaml --tool $tool --test-case $test_case
    done
done
```

## Generating New Datasets

This repository includes a unified script for generating random genomic interval datasets and uploading them to cloud storage. The script creates datasets with unique timestamps and uploads them with proper directory structure.

### Prerequisites for Dataset Generation

1. **rclone** - Required for uploading datasets to Google Drive
   ```bash
   # Install rclone
   curl https://rclone.org/install.sh | sudo bash
   
   # Configure rclone with your Google Drive (follow interactive setup)
   rclone config
   ```

2. **Python dependencies** - The script requires pandas, numpy, and yaml:
   ```bash
   # These are already included in the poetry environment
   poetry install
   ```

### Usage

To generate a new dataset:

```bash
# From the polars-bio-bench root directory
poetry run python src/generate_dataset.py
```

The script will:

1. **Clean up old files** - Remove previous datasets and ZIP archives
2. **Generate test data** - Create parquet files with different sizes (100, 1K, 10K, 100K, 1M records)
3. **Create ZIP archive** - Package the datasets into a single ZIP file
4. **Upload to Google Drive** - Upload via rclone and generate public download link
5. **Generate configuration files** - Create YAML configs for benchmarking

### Output Structure

The script generates files in the following structure:

```
polars-bio-bench/
├── tmp/
│   ├── data/                          # Generated parquet files
│   │   ├── df1-100.parquet
│   │   ├── df2-100.parquet
│   │   ├── df1-1000.parquet
│   │   ├── df2-1000.parquet
│   │   ├── ... (up to 1M records)
│   └── conf/                          # Configuration files
│       ├── common.yaml                # Dataset metadata and test cases
│       └── random.yaml                # Benchmark definitions
└── random_intervals_YYYYMMDD_HHMMSS.zip  # ZIP archive for upload
```

### Generated Dataset Properties

- **Dataset ID**: `random_intervals_YYYYMMDD_HHMMSS` (unique timestamp)
- **Test cases**: 5 different sizes (100, 1K, 10K, 100K, 1M records)
- **File format**: Parquet files with genomic intervals (chrom, start, end)
- **Chromosome range**: chr1 only for simplicity
- **Coordinate range**: Random intervals up to dataset size
- **Archive size**: ~17-18 MB (compressed)

### Configuration Files

**common.yaml** - Contains dataset metadata:
```yaml
datasets:
- name: random_intervals_20250530_231351
  source: tgambin
  unzip: true
  format: zip
  url: https://drive.google.com/open?id=...
  # ... additional metadata
test-cases:
- name: '100'
  df_path_1: df1-100.parquet
  df_path_2: df2-100.parquet
# ... more test cases
```

**random.yaml** - Contains benchmark definitions for overlap and nearest operations with various tools and parallelization options.

### Cloud Storage

Datasets are automatically uploaded to:
- **Remote path**: `tgambin:polars-bio-datasets/{dataset_id}/`
- **Public URL**: Generated automatically via rclone link
- **Access**: Public download links for easy integration

### Integration with Benchmarks

Once generated, the new dataset can be used in benchmarks by:
1. Copying the configuration files to the main `conf/` directory
2. Updating benchmark YAML files to reference the new dataset ID
3. Running benchmarks with the new configuration

Example:
```bash
# Copy generated configs (optional)
cp tmp/conf/common.yaml conf/
cp tmp/conf/random.yaml conf/benchmark_random_new.yaml

# Run benchmarks with new dataset
poetry run python src/run-benchmarks.py --bench-config conf/benchmark_random_new.yaml
```


