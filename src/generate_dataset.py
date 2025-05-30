#!/usr/bin/env python3
"""
Unified script for generating random genomic interval datasets and uploading them to cloud storage.
Creates datasets with unique timestamps and uploads them with proper directory structure.
"""

import os
import sys
import shutil
import subprocess
import yaml
import re
import pandas as pd
import numpy as np
from datetime import datetime

def print_status(msg, level=0):
    """Print status message with proper indentation and flushing"""
    indent = "  " * level
    print(f"{indent}{msg}", flush=True)

def cleanup_old_files(data_dir, conf_dir, project_root):
    """Remove old files before generating new ones"""
    print_status("Cleaning up old files...")
    
    # Remove old data folder
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
        print_status(f"Removed old {data_dir} folder", 1)
    
    # Remove old ZIP files in project root
    old_zips = [f for f in os.listdir(project_root) if f.endswith(".zip") and "random_intervals" in f]
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

def make_random_intervals(n=1e5, n_chroms=1, max_coord=None, max_length=10, 
                         sort=False, categorical_chroms=False):
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

    df = pd.DataFrame({"chrom": chroms, "start": starts, "end": ends})

    if categorical_chroms:
        df["chrom"] = df["chrom"].astype("category")

    if sort:
        df = df.sort_values(["chrom", "start", "end"]).reset_index(drop=True)

    return df

def generate_test_data(data_dir="tmp/data"):
    """Generate test datasets with various sizes"""
    print_status("Generating test datasets...")
    
    os.makedirs(data_dir, exist_ok=True)
    
    sizes = [1e2, 1e3, 1e4, 1e5, 1e6]
    for i, n in enumerate(sizes):
        n_int = int(n)
        print_status(f"Generating dataset {i+1}/{len(sizes)}: n={n_int}", 1)
        
        df1 = make_random_intervals(n=n, n_chroms=1)
        df2 = make_random_intervals(n=n, n_chroms=1)
        
        path1 = os.path.join(data_dir, f'df1-{n_int}.parquet')
        path2 = os.path.join(data_dir, f'df2-{n_int}.parquet')
        
        df1.to_parquet(path1)
        df2.to_parquet(path2)
        
        print_status(f"Saved: {os.path.basename(path1)}, {os.path.basename(path2)}", 2)

def find_test_cases(folder):
    """Find matching test case pairs"""
    files = os.listdir(folder)
    df1_cases = {re.match(r'df1-(\d+)\.parquet$', f).group(1)
                 for f in files if re.match(r'df1-(\d+)\.parquet$', f)}
    df2_cases = {re.match(r'df2-(\d+)\.parquet$', f).group(1)
                 for f in files if re.match(r'df2-(\d+)\.parquet$', f)}
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
        shutil.make_archive(base_name, 'zip', temp_dir)
    
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
        subprocess.run(["rclone", "mkdir", remote_path], check=True, 
                      capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print_status(f"Warning: Could not create directory (may already exist)", 1)
    
    # Upload file
    print_status(f"Uploading {zip_path} to {remote_path}/", 1)
    try:
        subprocess.run(["rclone", "copy", zip_path, f"{remote_path}/"], 
                      check=True, capture_output=True, text=True)
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
            stderr=subprocess.STDOUT
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
        "datasets": [{
            "name": dataset_id,
            "source": "gdrive",
            "unzip": True,
            "format": "zip",
            "url": url,
            "remote_path": f"tgambin:polars-bio-datasets/{dataset_id}/{os.path.basename(zip_path)}",
            "generated": datetime.now().isoformat(),
            "size_mb": round(os.path.getsize(zip_path) / 1024 / 1024, 1)
        }],
        "test-cases": [
            {
                "name": case,
                "df_path_1": f"df1-{case}.parquet",
                "df_path_2": f"df2-{case}.parquet",
            }
            for case in test_cases
        ],
        "benchmark": {
            "export": {
                "format": "csv"
            }
        }
    }
    
    # Benchmark configuration
    benchmark_config = {
        "common": {"baseline": "polars_bio"},
        "benchmarks": []
    }
    
    # Define benchmark types
    benchmark_definitions = [
        ("overlap-single", "overlap", False, []),
        ("nearest-single", "nearest", False, []),
        ("overlap-parallel", "overlap", True, [1, 2, 4]),
        ("nearest-parallel", "nearest", True, [1, 2, 4]),
    ]
    
    for name, operation, parallel, threads in benchmark_definitions:
        tools = ["polars_bio", "bioframe", "pyranges0", "pyranges1", "pybedtools"]
        if "overlap" in name:
            tools.extend(["genomicranges", "pygenomics"])
        
        benchmark = {
            "name": name,
            "operation": operation,
            "dataset": dataset_id,
            "tools": tools,
            "parallel": parallel,
            "input_dataframes": False,
            "num_repeats": 3,
            "num_executions": 1,
            "test-cases": list(test_cases)  # Create a copy to avoid YAML references
        }
        
        if parallel and threads:
            benchmark["threads"] = threads
        
        benchmark_config["benchmarks"].append(benchmark)
    
    # Save files
    common_path = os.path.join(conf_dir, "common.yaml")
    random_path = os.path.join(conf_dir, "random.yaml")
    
    with open(common_path, "w") as f:
        yaml.dump(common_config, f, sort_keys=False, allow_unicode=True, 
                  default_flow_style=False)
    print_status(f"Saved: {common_path}", 1)
    
    with open(random_path, "w") as f:
        yaml.dump(benchmark_config, f, sort_keys=False, allow_unicode=True, 
                  default_flow_style=False)
    print_status(f"Saved: {random_path}", 1)

def main():
    """Main execution function"""
    # Generate unique dataset ID with timestamp
    dataset_id = datetime.now().strftime("random_intervals_%Y%m%d_%H%M%S")
    
    # Define directory structure - use absolute paths relative to polars-bio-bench root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # Go up from src/ to polars-bio-bench/
    data_dir = os.path.join(project_root, "tmp", "data")
    conf_dir = os.path.join(project_root, "tmp", "conf")
    
    print_status("=" * 60)
    print_status(f"DATASET GENERATION AND UPLOAD")
    print_status(f"Dataset ID: {dataset_id}")
    print_status(f"Project root: {project_root}")
    print_status(f"Data directory: {data_dir}")
    print_status(f"Config directory: {conf_dir}")
    print_status("=" * 60)
    
    try:
        # Step 1: Clean up old files
        cleanup_old_files(data_dir=data_dir, conf_dir=conf_dir, project_root=project_root)
        
        # Step 2: Generate test data
        generate_test_data(data_dir=data_dir)
        
        # Step 3: Find test cases
        print_status("Discovering test cases...")
        test_cases = find_test_cases(data_dir)
        print_status(f"Found {len(test_cases)} test cases: {test_cases}", 1)
        
        # Step 4: Create ZIP archive
        zip_path = create_zip_archive(data_dir, dataset_id, project_root)
        
        # Step 5: Upload to remote storage
        url = upload_to_remote(zip_path, dataset_id)
        if not url:
            print_status("ERROR: Upload failed!", 0)
            sys.exit(1)
        
        # Step 6: Create configuration files
        create_config_files(dataset_id, zip_path, url, test_cases, conf_dir=conf_dir)
        
        # Summary
        print_status("=" * 60)
        print_status("GENERATION COMPLETED SUCCESSFULLY")
        print_status("=" * 60)
        print_status(f"Dataset ID: {dataset_id}")
        print_status(f"ZIP file: {zip_path}")
        print_status(f"Remote location: tgambin:polars-bio-datasets/{dataset_id}/")
        print_status(f"Public URL: {url}")
        print_status(f"Test cases: {len(test_cases)} ({', '.join(test_cases)})")
        print_status(f"Configuration files: {conf_dir}/common.yaml, {conf_dir}/random.yaml")
        print_status("=" * 60)
        
    except KeyboardInterrupt:
        print_status("\nProcess interrupted by user", 0)
        sys.exit(1)
    except Exception as e:
        print_status(f"ERROR: {e}", 0)
        sys.exit(1)

if __name__ == "__main__":
    main()
