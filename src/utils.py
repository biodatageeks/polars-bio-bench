# pyranges0
import os
import shutil
import zipfile
from pathlib import Path
from urllib.parse import urlparse

import emoji
import gdown
import pyranges as pr0
import pyranges1 as pr1
from google.cloud import storage
from tqdm import tqdm

from logger import logger


def df2pr0(df):
    return pr0.PyRanges(
        chromosomes=df.contig,
        starts=df.pos_start,
        ends=df.pos_end,
    )


### pyranges1
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
    storage_client = storage.Client()
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
