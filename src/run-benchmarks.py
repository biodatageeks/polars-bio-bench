import logging
import os
import shutil
import zipfile
from pathlib import Path

import emoji
import gdown
import yaml
from tqdm import tqdm

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger("polars_bio_bench")

logger.info(emoji.emojize("Starting polars_bio_benchmark :rocket:"))

BECH_DATA_ROOT = os.getenv("BENCH_DATA_ROOT")
if not BECH_DATA_ROOT:
    logger.error(emoji.emojize("Env variable BENCH_DATA_ROOT is not set :pile_of_poo:"))
    exit(1)


with open("conf/benchmark.yaml", "r") as file:
    config = yaml.safe_load(file)
    logger.info(emoji.emojize("Loaded config. :open_book:"))

datasets = config["datasets"]

Path.mkdir(Path(BECH_DATA_ROOT), parents=True, exist_ok=True)
for d in tqdm(datasets, desc="Downloading benchmark datasets"):
    url = d["url"]
    file = d["name"]
    extract_dir = f"{BECH_DATA_ROOT}/{file.split('.')[0]}"
    if os.path.exists(extract_dir):
        logger.info(
            emoji.emojize(
                f"Dataset {file.split(".")[0]} already exists :file_folder: To re-download, remove the directory."
            )
        )
        continue
    gdown.download(url, f"{BECH_DATA_ROOT}/{file}", quiet=True, verify=True)
    logger.info(emoji.emojize(f"Downloaded {file} :check_box_with_check: "))
    ds_zip_file = f"{BECH_DATA_ROOT}/{file}"
    Path.mkdir(Path(extract_dir), parents=True, exist_ok=True)
    shutil.rmtree(f"{extract_dir}/*", ignore_errors=True)
    with zipfile.ZipFile(ds_zip_file, "r") as zip_ref:
        zip_ref.extractall(extract_dir)
    logger.info(emoji.emojize(f"Extracted {file} :open_file_folder: "))
    os.remove(ds_zip_file)
logger.info(emoji.emojize("Downloaded all benchmark datasets :check_mark_button:"))
