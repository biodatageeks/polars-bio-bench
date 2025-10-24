#!/usr/bin/env python3
"""
Unified script for generating random genomic interval datasets and uploading them to cloud storage.
Creates datasets with unique timestamps and uploads them with proper directory structure.
"""

import os
import re
import shutil
import subprocess
import sys
from datetime import datetime

import numpy as np
import polars as pl
import yaml
from pyspark.sql import SparkSession


def print_status(msg, level=0):
    """Print status message with proper indentation and flushing"""
    indent = "  " * level
    print(f"{indent}{msg}", flush=True)


def get_spark_session():
    """Initialize and return Spark session with proper memory configuration"""
    print_status("Initializing Spark session...")
    spark = (
        SparkSession.builder.appName("ParquetPartitioning")
        .config("spark.driver.memory", "4g")
        .config("spark.driver.maxResultSize", "2g")
        .config("spark.executor.memory", "4g")
        .config("spark.executor.cores", "2")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .config("spark.sql.adaptive.advisoryPartitionSizeInBytes", "128MB")
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
        .getOrCreate()
    )

    # Set log level to reduce verbose output
    spark.sparkContext.setLogLevel("WARN")
    return spark


def cleanup_old_files(data_dir, conf_dir, project_root):
    """Remove old files before generating new ones"""
    print_status("Cleaning up old files...")

    # Remove old data folder
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
        print_status(f"Removed old {data_dir} folder", 1)

    # Remove old ZIP files in project root
    old_zips = [
        f
        for f in os.listdir(project_root)
        if f.endswith(".zip") and "random_intervals" in f
    ]
    for file in old_zips:
        zip_path = os.path.join(project_root, file)
        os.remove(zip_path)
        print_status(f"Removed old ZIP: {zip_path}", 1)

    # Remove old YAML files in conf directory
    if os.path.exists(conf_dir):
        for file in ["common.yaml", "random.yaml"]:
            conf_file = os.path.join(conf_dir, file)
            if os.path.exists(conf_file):
                os.remove(conf_file)
                print_status(f"Removed old config: {conf_file}", 1)


def make_random_intervals(
    n=1e5,
    n_chroms=1,
    max_coord=None,
    max_length=10,
    sort=False,
    categorical_chroms=False,
):
    """Generate random genomic intervals"""
    n = int(n)
    n_chroms = int(n_chroms)
    max_coord = (n // n_chroms) if max_coord is None else int(max_coord)
    max_length = int(max_length)

    chroms = np.array(["chr" + str(i + 1) for i in range(n_chroms)])[
        np.random.randint(0, n_chroms, n)
    ]
    starts = np.random.randint(0, max_coord, n)
    ends = starts + np.random.randint(1, max_length, n)

    # Create Polars DataFrame
    df = pl.DataFrame({"contig": chroms, "pos_start": starts, "pos_end": ends})

    if categorical_chroms:
        df = df.with_columns(pl.col("contig").cast(pl.Categorical))

    if sort:
        df = df.sort(["contig", "pos_start", "pos_end"])

    return df


def generate_test_data(data_dir="tmp/data", num_partitions=8):
    """Generate test datasets with various sizes and partition them using Spark"""
    print_status(f"Generating test datasets with {num_partitions} partition(s)...")

    os.makedirs(data_dir, exist_ok=True)

    # Initialize Spark session
    spark = get_spark_session()

    try:
        sizes = [1e2, 1e3, 1e4, 1e5, 1e6, 10e6]
        for i, n in enumerate(sizes):
            n_int = int(n)
            print_status(f"Generating dataset {i+1}/{len(sizes)}: n={n_int}", 1)

            # Define output paths
            path1 = os.path.join(data_dir, f"df1-{n_int}.parquet")
            path2 = os.path.join(data_dir, f"df2-{n_int}.parquet")

            # Remove existing directories if they exist
            if os.path.exists(path1):
                shutil.rmtree(path1)
            if os.path.exists(path2):
                shutil.rmtree(path2)

            # Generate data using Polars
            df1_polars = make_random_intervals(n=n, n_chroms=1)
            df2_polars = make_random_intervals(n=n, n_chroms=1)

            # Convert to Pandas for Spark compatibility
            df1_pandas = df1_polars.to_pandas()
            df2_pandas = df2_polars.to_pandas()

            # Create Spark DataFrames
            df1_spark = spark.createDataFrame(df1_pandas)
            df2_spark = spark.createDataFrame(df2_pandas)

            print_status(f"Partitioning df1 into {num_partitions} partitions...", 2)
            # Repartition and write
            df1_spark.repartition(num_partitions).write.mode("overwrite").parquet(path1)

            print_status(f"Partitioning df2 into {num_partitions} partitions...", 2)
            df2_spark.repartition(num_partitions).write.mode("overwrite").parquet(path2)

            # Verify partitioning
            partition_count_1 = len(
                [f for f in os.listdir(path1) if f.startswith("part-")]
            )
            partition_count_2 = len(
                [f for f in os.listdir(path2) if f.startswith("part-")]
            )

            print_status(
                f"Saved: {os.path.basename(path1)} ({partition_count_1} partitions), "
                f"{os.path.basename(path2)} ({partition_count_2} partitions)",
                2,
            )

    finally:
        # Stop Spark session
        print_status("Stopping Spark session...", 1)
        spark.stop()


def create_partitioned_versions(base_data_dir, output_dir_1p, output_dir_8p):
    """Create 1-partition and 8-partition versions from the same base data"""
    print_status("Creating partitioned versions from base data...")

    # Initialize Spark session
    spark = get_spark_session()

    try:
        # Create output directories
        os.makedirs(output_dir_1p, exist_ok=True)
        os.makedirs(output_dir_8p, exist_ok=True)

        # Find all parquet directories in base data
        parquet_dirs = [
            d
            for d in os.listdir(base_data_dir)
            if os.path.isdir(os.path.join(base_data_dir, d)) and d.endswith(".parquet")
        ]

        for parquet_dir in parquet_dirs:
            print_status(f"Processing {parquet_dir}...", 1)

            base_path = os.path.join(base_data_dir, parquet_dir)
            path_1p = os.path.join(output_dir_1p, parquet_dir)
            path_8p = os.path.join(output_dir_8p, parquet_dir)

            # Remove existing directories if they exist
            if os.path.exists(path_1p):
                shutil.rmtree(path_1p)
            if os.path.exists(path_8p):
                shutil.rmtree(path_8p)

            # Read the base data
            df_spark = spark.read.parquet(base_path)

            print_status("Creating 1-partition version...", 2)
            # Create 1-partition version
            df_spark.repartition(1).write.mode("overwrite").parquet(path_1p)

            print_status("Creating 8-partition version...", 2)
            # Create 8-partition version
            df_spark.repartition(8).write.mode("overwrite").parquet(path_8p)

            # Verify partitioning
            partition_count_1p = len(
                [f for f in os.listdir(path_1p) if f.startswith("part-")]
            )
            partition_count_8p = len(
                [f for f in os.listdir(path_8p) if f.startswith("part-")]
            )

            print_status(
                f"Created: {parquet_dir} -> 1p({partition_count_1p} partitions), 8p({partition_count_8p} partitions)",
                2,
            )

    finally:
        # Stop Spark session
        print_status("Stopping Spark session...", 1)
        spark.stop()


def find_test_cases(folder):
    """Find matching test case pairs (now directories instead of files)"""
    items = os.listdir(folder)
    df1_cases = set()
    df2_cases = set()

    for item in items:
        item_path = os.path.join(folder, item)
        if os.path.isdir(item_path):
            # Check for df1 directories
            df1_match = re.match(r"df1-(\d+)\.parquet$", item)
            if df1_match:
                df1_cases.add(df1_match.group(1))

            # Check for df2 directories
            df2_match = re.match(r"df2-(\d+)\.parquet$", item)
            if df2_match:
                df2_cases.add(df2_match.group(1))

    return sorted(df1_cases & df2_cases, key=lambda x: int(x))


def create_zip_archive(source_dir, dataset_id, project_root):
    """Create ZIP archive of the data directory with proper folder structure"""
    print_status("Creating ZIP archive...")

    # Place ZIP file in project root
    zip_name = os.path.join(project_root, f"{dataset_id}.zip")

    # Remove old ZIP if exists
    if os.path.exists(zip_name):
        os.remove(zip_name)
        print_status(f"Removed existing {zip_name}", 1)

    print_status(f"Archiving {source_dir} -> {zip_name}", 1)

    # Create a temporary directory structure with the dataset_id folder
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create the dataset folder inside temp directory
        dataset_folder = os.path.join(temp_dir, dataset_id)
        shutil.copytree(source_dir, dataset_folder)

        # Create ZIP with the dataset folder structure
        base_name = os.path.join(project_root, dataset_id)
        shutil.make_archive(base_name, "zip", temp_dir)

    size_mb = os.path.getsize(zip_name) / 1024 / 1024
    print_status(f"Created: {zip_name} ({size_mb:.1f} MB)", 1)

    return zip_name


def upload_to_remote(zip_path, dataset_id, remote="tgambin"):
    """Upload ZIP file to remote storage and return public link"""
    print_status("Uploading to remote storage...")

    remote_dir = f"polars-bio-datasets/{dataset_id}"
    remote_path = f"{remote}:{remote_dir}"

    # Create remote directory
    print_status(f"Creating remote directory: {remote_path}", 1)
    try:
        subprocess.run(
            ["rclone", "mkdir", remote_path], check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError:
        print_status("Warning: Could not create directory (may already exist)", 1)

    # Upload file
    print_status(f"Uploading {zip_path} to {remote_path}/", 1)
    try:
        subprocess.run(
            ["rclone", "copy", zip_path, f"{remote_path}/"],
            check=True,
            capture_output=True,
            text=True,
        )
        print_status("Upload successful", 2)
    except subprocess.CalledProcessError as e:
        print_status(f"Upload failed: {e}", 1)
        return None

    # Generate public link
    remote_file = f"{remote}:{remote_dir}/{os.path.basename(zip_path)}"
    print_status(f"Generating public link for: {remote_file}", 1)

    try:
        link = subprocess.check_output(
            ["rclone", "link", remote_file],
            universal_newlines=True,
            stderr=subprocess.STDOUT,
        ).strip()
        print_status(f"Public link: {link}", 2)
        return link
    except subprocess.CalledProcessError as e:
        print_status(f"Link generation failed: {e}", 1)
        fallback = f"File available at: {remote_file}"
        print_status(f"Fallback info: {fallback}", 2)
        return fallback


def create_config_files(dataset_id, zip_path, url, test_cases, conf_dir="tmp/conf"):
    """Create YAML configuration files"""
    print_status("Creating configuration files...")

    # Create config directory if it doesn't exist
    os.makedirs(conf_dir, exist_ok=True)

    # Convert Google Drive URL to direct download format if needed
    if "drive.google.com/open?id=" in url:
        # Extract file ID from URL like: https://drive.google.com/open?id=1pew9OD-pn8svUmk0Hsq8lmdiMbSOCjdT
        file_id = url.split("id=")[1]
        url = f"https://drive.google.com/uc?id={file_id}"
        print_status(f"Converted URL to direct download format: {url}", 1)

    # Common configuration
    common_config = {
        "datasets": [
            {
                "name": dataset_id,
                "source": "gdrive",
                "unzip": True,
                "format": "zip",
                "url": url,
                "remote_path": f"tgambin:polars-bio-datasets/{dataset_id}/{os.path.basename(zip_path)}",
                "generated": datetime.now().isoformat(),
                "size_mb": round(os.path.getsize(zip_path) / 1024 / 1024, 1),
            }
        ],
        "test-cases": [
            {
                "name": case,
                "df_path_1": f"df1-{case}.parquet/*.parquet",
                "df_path_2": f"df2-{case}.parquet/*.parquet",
            }
            for case in test_cases
        ],
        "benchmark": {"export": {"format": "csv"}},
    }

    # Benchmark configuration
    benchmark_config = {"common": {"baseline": "polars_bio"}, "benchmarks": []}

    # Define operations
    operations = ["overlap", "nearest", "coverage", "count_overlaps"]

    # Define test case groups
    small_test_cases = [
        case for case in test_cases if int(case) <= 100000
    ]  # 100 to 100000
    large_test_cases = [
        case for case in test_cases if int(case) >= 1000000
    ]  # 1000000 to 10000000

    for operation in operations:
        # Single benchmarks - split into small and large datasets

        # Small datasets (100-100000) - all tools
        tools_all = ["polars_bio", "bioframe", "pyranges1", "pybedtools"]
        if operation in ["overlap", "count_overlaps"]:
            tools_all.extend(["genomicranges", "pygenomics"])

        benchmark_small = {
            "name": f"{operation}-single-small",
            "operation": operation,
            "dataset": dataset_id,
            "tools": tools_all,
            "parallel": False,
            "input_dataframes": False,
            "num_repeats": 3,
            "num_executions": 1,
            "test-cases": list(small_test_cases),
        }
        benchmark_config["benchmarks"].append(benchmark_small)

        # Large datasets (1000000-10000000) - fast tools only
        tools_fast = ["polars_bio", "bioframe", "pyranges1"]

        benchmark_large = {
            "name": f"{operation}-single-large",
            "operation": operation,
            "dataset": dataset_id,
            "tools": tools_fast,
            "parallel": False,
            "input_dataframes": False,
            "num_repeats": 3,
            "num_executions": 1,
            "test-cases": list(large_test_cases),
        }
        benchmark_config["benchmarks"].append(benchmark_large)

        # Parallel benchmarks - only polars_bio for all test cases
        benchmark_parallel = {
            "name": f"{operation}-parallel",
            "operation": operation,
            "dataset": dataset_id,
            "tools": ["polars_bio"],
            "parallel": True,
            "input_dataframes": False,
            "num_repeats": 3,
            "num_executions": 1,
            "test-cases": list(test_cases),
            "threads": [1, 2, 4, 6, 8],
        }
        benchmark_config["benchmarks"].append(benchmark_parallel)

    # Save files
    common_path = os.path.join(conf_dir, "common.yaml")
    random_path = os.path.join(conf_dir, "random.yaml")

    with open(common_path, "w") as f:
        yaml.dump(
            common_config,
            f,
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
        )
    print_status(f"Saved: {common_path}", 1)

    with open(random_path, "w") as f:
        yaml.dump(
            benchmark_config,
            f,
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
        )
    print_status(f"Saved: {random_path}", 1)


def create_combined_config_files(datasets_info, conf_dir="tmp/conf"):
    """Create YAML configuration files for both datasets"""
    print_status("Creating combined configuration files...")

    # Create config directory if it doesn't exist
    os.makedirs(conf_dir, exist_ok=True)

    # Common configuration - combine both datasets
    datasets_config = []
    all_test_cases = []

    for dataset_info in datasets_info:
        # Convert Google Drive URL to direct download format if needed
        url = dataset_info["url"]
        if "drive.google.com/open?id=" in url:
            file_id = url.split("id=")[1]
            url = f"https://drive.google.com/uc?id={file_id}"

        datasets_config.append(
            {
                "name": dataset_info["dataset_id"],
                "source": "gdrive",
                "unzip": True,
                "format": "zip",
                "url": url,
                "remote_path": f"tgambin:polars-bio-datasets/{dataset_info['dataset_id']}/{os.path.basename(dataset_info['zip_path'])}",
                "generated": datetime.now().isoformat(),
                "size_mb": round(
                    os.path.getsize(dataset_info["zip_path"]) / 1024 / 1024, 1
                ),
            }
        )

        # Add test cases for this dataset
        for case in dataset_info["test_cases"]:
            all_test_cases.append(
                {
                    "name": f"{case}-{dataset_info['dataset_id'].split('-')[-1]}",  # e.g., "100-1p", "1000-8p"
                    "df_path_1": f"df1-{case}.parquet/*.parquet",
                    "df_path_2": f"df2-{case}.parquet/*.parquet",
                    "dataset": dataset_info["dataset_id"],
                }
            )

    common_config = {
        "datasets": datasets_config,
        "test-cases": all_test_cases,
        "benchmark": {"export": {"format": "csv"}},
    }

    # Save combined config
    common_path = os.path.join(conf_dir, "common.yaml")
    with open(common_path, "w") as f:
        yaml.dump(
            common_config,
            f,
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
        )
    print_status(f"Saved combined config: {common_path}", 1)


def main():
    """Main execution function"""
    # Generate unique dataset ID with timestamp
    base_dataset_id = datetime.now().strftime("random_intervals_%Y%m%d_%H%M%S")

    # Define directory structure - use absolute paths relative to polars-bio-bench root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # Go up from src/ to polars-bio-bench/
    conf_dir = os.path.join(project_root, "tmp", "conf")

    print_status("=" * 60)
    print_status("DATASET GENERATION AND UPLOAD")
    print_status(f"Base Dataset ID: {base_dataset_id}")
    print_status(f"Will generate: {base_dataset_id}-1p and {base_dataset_id}-8p")
    print_status(f"Project root: {project_root}")
    print_status(f"Config directory: {conf_dir}")
    print_status("=" * 60)

    datasets_info = []

    try:
        # Step 1: Generate base data once
        print_status("=" * 60)
        print_status("GENERATING BASE DATA")
        print_status("=" * 60)

        base_data_dir = os.path.join(project_root, "tmp", "data-base")
        cleanup_old_files(
            data_dir=base_data_dir, conf_dir=conf_dir, project_root=project_root
        )
        generate_test_data(
            data_dir=base_data_dir, num_partitions=8
        )  # Generate with 8 partitions first

        # Step 2: Create partitioned versions from base data
        print_status("=" * 60)
        print_status("CREATING PARTITIONED VERSIONS")
        print_status("=" * 60)

        data_dir_1p = os.path.join(project_root, "tmp", "data-1p")
        data_dir_8p = os.path.join(project_root, "tmp", "data-8p")

        create_partitioned_versions(base_data_dir, data_dir_1p, data_dir_8p)

        # Step 3: Create datasets and upload
        dataset_configs = [
            {
                "id": f"{base_dataset_id}-1p",
                "dir": data_dir_1p,
                "partitions": "1-partition",
            },
            {
                "id": f"{base_dataset_id}-8p",
                "dir": data_dir_8p,
                "partitions": "8-partition",
            },
        ]

        for config in dataset_configs:
            print_status("=" * 60)
            print_status(f"PROCESSING {config['partitions'].upper()} VERSION")
            print_status("=" * 60)

            dataset_id = config["id"]
            data_dir = config["dir"]

            test_cases = find_test_cases(data_dir)
            print_status(f"Found {len(test_cases)} test cases: {test_cases}", 1)

            zip_path = create_zip_archive(data_dir, dataset_id, project_root)
            url = upload_to_remote(zip_path, dataset_id)

            if url:
                datasets_info.append(
                    {
                        "dataset_id": dataset_id,
                        "zip_path": zip_path,
                        "url": url,
                        "test_cases": test_cases,
                    }
                )

        if not datasets_info:
            print_status("ERROR: No datasets were successfully generated!", 0)
            sys.exit(1)

        # Step 4: Create combined configuration files
        create_combined_config_files(datasets_info, conf_dir=conf_dir)

        # Step 5: Cleanup base data directory
        print_status("Cleaning up base data directory...", 0)
        if os.path.exists(base_data_dir):
            shutil.rmtree(base_data_dir)

        # Summary
        print_status("=" * 60)
        print_status("GENERATION COMPLETED SUCCESSFULLY")
        print_status("=" * 60)

        for dataset_info in datasets_info:
            print_status(f"Dataset ID: {dataset_info['dataset_id']}")
            print_status(f"ZIP file: {dataset_info['zip_path']}")
            print_status(f"Public URL: {dataset_info['url']}")
            print_status(
                f"Test cases: {len(dataset_info['test_cases'])} ({', '.join(dataset_info['test_cases'])})"
            )
            print_status("-" * 40)

        print_status(f"Configuration files: {conf_dir}/common.yaml")
        print_status("=" * 60)

    except KeyboardInterrupt:
        print_status("\nProcess interrupted by user", 0)
        sys.exit(1)
    except Exception as e:
        print_status(f"ERROR: {e}", 0)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
