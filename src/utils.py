import os
import shutil
import zipfile
from pathlib import Path
from urllib.parse import urlparse

import emoji
import gdown
import numpy as np
import pyranges as pr1
from google.cloud import storage
from tqdm import tqdm

from logger import logger


def df2pr1(df):
    return pr1.PyRanges(
        {
            "Chromosome": df.contig,
            "Start": df.pos_start,
            "End": df.pos_end,
        }
    )


def download_from_gs(gs_url, destination_dir):
    # Parse the gs:// URL
    parsed_url = urlparse(gs_url)
    if parsed_url.scheme != "gs":
        raise ValueError("URL must start with 'gs://'")

    bucket_name = parsed_url.netloc
    blob_path = parsed_url.path.lstrip("/")  # Remove leading slash

    # Determine local file name (using the basename of the blob)
    local_filename = os.path.join(destination_dir, os.path.basename(blob_path))

    # Initialize the client and get the blob
    storage_client = storage.Client.create_anonymous_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    # Download the blob to the local file
    blob.download_to_filename(local_filename)
    logger.info(f"Downloaded {gs_url} to {local_filename}")


def prepare_datatests(datasets, BECH_DATA_ROOT):
    global dataset, file
    Path.mkdir(Path(BECH_DATA_ROOT), parents=True, exist_ok=True)
    for d in tqdm(datasets, desc="Downloading benchmark datasets"):
        url = d["url"]
        dataset = d["name"]
        unzip = d["unzip"]
        format = d["format"] if "format" in d else None
        file = f"{dataset}.{format}" if format else dataset
        extract_dir = f"{BECH_DATA_ROOT}/"
        if os.path.exists(f"{extract_dir}/{dataset}"):
            logger.info(
                emoji.emojize(
                    f"Dataset {file.split(".")[0]} already exists :file_folder: To re-download, remove the directory."
                )
            )
            continue
        source = d["source"].lower()
        if source == "gdrive":
            gdown.download(url, f"{BECH_DATA_ROOT}/{file}", quiet=True, verify=True)
        elif source == "gcs":
            Path.mkdir(Path(f"{BECH_DATA_ROOT}/{dataset}"), parents=True, exist_ok=True)
            download_from_gs(url, f"{BECH_DATA_ROOT}/{dataset}")
        else:
            raise ValueError(f"Unknown source: {source}")
        logger.info(emoji.emojize(f"Downloaded {dataset} :check_box_with_check: "))
        if unzip:
            ds_zip_file = f"{BECH_DATA_ROOT}/{file}"
            Path.mkdir(Path(extract_dir), parents=True, exist_ok=True)
            shutil.rmtree(f"{extract_dir}/*", ignore_errors=True)
            with zipfile.ZipFile(ds_zip_file, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
            logger.info(emoji.emojize(f"Extracted {file} :open_file_folder: "))
            os.remove(ds_zip_file)
        else:
            Path.mkdir(Path(f"{BECH_DATA_ROOT}/{dataset}"), parents=True, exist_ok=True)
    logger.info(emoji.emojize("Downloaded all benchmark datasets :check_mark_button:"))


def overlaps_to_df(query_gr, subject_gr, hits_bf, backend="polars"):
    # Convert hits to pandas to check available columns
    hits_df = hits_bf.to_pandas() if hasattr(hits_bf, "to_pandas") else hits_bf

    # Determine correct column names for query and subject indices
    if "queryHits" in hits_df.columns:
        q_idx = np.asarray(hits_df["queryHits"], dtype=int)
        s_idx = np.asarray(hits_df["subjectHits"], dtype=int)
    elif "query_hits" in hits_df.columns:
        # SWAP: Based on debugging, self_hits contains query indices, query_hits contains subject indices
        q_idx = np.asarray(hits_df["self_hits"], dtype=int)  # Actually query indices
        s_idx = np.asarray(hits_df["query_hits"], dtype=int)  # Actually subject indices
    else:
        # Fallback: assume first two columns are indices
        cols = list(hits_df.columns)
        q_idx = np.asarray(hits_df[cols[0]], dtype=int)
        s_idx = np.asarray(hits_df[cols[1]], dtype=int)
        print(f"Using fallback columns: {cols[0]} -> query, {cols[1]} -> subject")

    # Bounds checking to prevent index errors - ensure indices are 0-based and within bounds
    q_len = len(query_gr.seqnames)
    s_len = len(subject_gr.seqnames)

    # Filter indices to ensure they're within bounds (0-based indexing)
    valid_mask = (q_idx >= 0) & (q_idx < q_len) & (s_idx >= 0) & (s_idx < s_len)

    q_idx = q_idx[valid_mask]
    s_idx = s_idx[valid_mask]

    # pull arrays from GenomicRanges
    q_seq = np.asarray(query_gr.seqnames)[q_idx]
    q_start = np.asarray(query_gr.ranges.start)[q_idx]
    q_end = np.asarray(query_gr.ranges.end)[q_idx]

    s_seq = np.asarray(subject_gr.seqnames)[s_idx]
    s_start = np.asarray(subject_gr.ranges.start)[s_idx]
    s_end = np.asarray(subject_gr.ranges.end)[s_idx]

    data = {
        "contig1": q_seq,
        "start1": q_start,
        "end1": q_end,
        "contig2": s_seq,
        "start2": s_start,
        "end2": s_end,
    }

    if backend == "polars":
        import polars as pl

        return pl.DataFrame(data)
    else:
        import pandas as pd

        return pd.DataFrame(data)
