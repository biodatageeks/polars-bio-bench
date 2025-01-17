import os
import timeit

import emoji
import numpy as np
import pandas as pd
import pybedtools
import rich
import yaml
from genomicranges import GenomicRanges
from pygenomics.interval import GenomicBase
from rich.box import MARKDOWN
from rich.console import Console
from rich.table import Table
from tqdm import tqdm

from logger import logger
from operations import (
    nearest_bioframe,
    nearest_genomicranges,
    nearest_polars_bio,
    nearest_pybedtools,
    nearest_pyranges0,
    nearest_pyranges1,
    overlap_bioframe,
    overlap_genomicranges,
    overlap_polars_bio,
    overlap_pybedtools,
    overlap_pygenomics,
    overlap_pyranges0,
    overlap_pyranges1,
)
from utils import df2pr0, df2pr1, prepare_datatests

logger.info(emoji.emojize("Starting polars_bio_benchmark :rocket:"))
REPORT_FILE = "benchmark_results.md"
if os.path.exists(REPORT_FILE):
    logger.info(
        emoji.emojize(
            f"Performance report file {REPORT_FILE} already exist...quiting :wastebasket:"
        )
    )
    exit(1)
BECH_DATA_ROOT = os.getenv("BENCH_DATA_ROOT")
if not BECH_DATA_ROOT:
    logger.error(emoji.emojize("Env variable BENCH_DATA_ROOT is not set :pile_of_poo:"))
    exit(1)

columns = ("contig", "pos_start", "pos_end")

with open("conf/benchmark.yaml", "r") as file:
    config = yaml.safe_load(file)
    logger.info(emoji.emojize("Loaded config. :open_book:"))

datasets = config["datasets"]
test_cases = config["test-cases"]
benchmarks = config["benchmarks"]
tools = config["tools"]
functions_overlap = [
    overlap_polars_bio,
    overlap_bioframe,
    overlap_pyranges0,
    overlap_pyranges1,
    overlap_pybedtools,
    overlap_pygenomics,
    overlap_genomicranges,
]

functions_nearest = [
    nearest_polars_bio,
    nearest_bioframe,
    nearest_pyranges0,
    nearest_pyranges1,
    nearest_pybedtools,
    nearest_genomicranges,
]


prepare_datatests(datasets, BECH_DATA_ROOT)
console = Console(record=True)
for b in tqdm(benchmarks, desc="Running benchmarks"):
    dataset = b["dataset"]
    operation = b["operation"]
    num_executions = b["num_executions"]
    num_repeats = b["num_repeats"]
    console.log(f"## Benchmark {b["name"]} for {operation} with dataset {dataset} \n")
    logger.info(emoji.emojize(f"Running benchmark {b["name"]} :racing_car: "))
    for t in tqdm(b["test-cases"]):
        results = []
        logger.info(emoji.emojize(f"Loading test case {t}... :chequered_flag:  "))
        test = [test for test in test_cases if test["name"] == t][0]
        df_path_1 = f"{BECH_DATA_ROOT}/{dataset}/{test['df_path_1']}"
        df_path_2 = f"{BECH_DATA_ROOT}/{dataset}/{test['df_path_2']}"
        for tool in tqdm(tools):
            logger.info(
                emoji.emojize(
                    f"Running benchmark {b["name"]}, test-case {t} for {tool} :hammer_and_wrench:"
                )
            )
            times = None
            func = None
            table = None
            if operation == "overlap":
                table = [
                    func
                    for func in functions_overlap
                    if func.__name__ == f"{operation}_{tool}"
                ]
            elif operation == "nearest":
                table = [
                    func
                    for func in functions_nearest
                    if func.__name__ == f"{operation}_{tool}"
                ]
            else:
                logger.error(
                    emoji.emojize(f"Operation {operation} not found :no_entry:")
                )
                exit(1)
            if len(table) == 0:
                logger.warning(
                    emoji.emojize(
                        f"Operation {operation} not found for tool {tool} :no_entry:"
                    )
                )
                console.log(
                    f":bulb: Tool {tool} does not support operation {operation}"
                )
                continue
            func = table[0]
            if tool == "polars_bio":
                times = timeit.repeat(
                    lambda: func(df_path_1, df_path_2),
                    repeat=num_repeats,
                    number=num_executions,
                )

            elif tool == "bioframe":
                df_1 = pd.read_parquet(
                    df_path_1.replace("*.parquet", ""), engine="pyarrow"
                )
                df_2 = pd.read_parquet(
                    df_path_2.replace("*.parquet", ""), engine="pyarrow"
                )
                times = timeit.repeat(
                    lambda: func(df_1, df_2),
                    repeat=num_repeats,
                    number=num_executions,
                )
            elif tool == "pyranges0":
                df_1 = pd.read_parquet(
                    df_path_1.replace("*.parquet", ""), engine="pyarrow"
                )
                df_2 = pd.read_parquet(
                    df_path_2.replace("*.parquet", ""), engine="pyarrow"
                )
                df_1_pr0 = df2pr0(df_1)
                df_2_pr0 = df2pr0(df_2)
                times = timeit.repeat(
                    lambda: func(df_1_pr0, df_2_pr0),
                    repeat=num_repeats,
                    number=num_executions,
                )
            elif tool == "pyranges1":
                df_1 = pd.read_parquet(
                    df_path_1.replace("*.parquet", ""), engine="pyarrow"
                )
                df_2 = pd.read_parquet(
                    df_path_2.replace("*.parquet", ""), engine="pyarrow"
                )
                df_1_pr1 = df2pr1(df_1)
                df_2_pr1 = df2pr1(df_2)
                times = timeit.repeat(
                    lambda: func(df_1_pr1, df_2_pr1),
                    repeat=num_repeats,
                    number=num_executions,
                )
            elif tool == "pybedtools":
                df_1 = pd.read_parquet(
                    df_path_1.replace("*.parquet", ""), engine="pyarrow"
                )
                df_2 = pd.read_parquet(
                    df_path_2.replace("*.parquet", ""), engine="pyarrow"
                )
                df_1_bed = pybedtools.BedTool.from_dataframe(df_1)
                df_2_bed = pybedtools.BedTool.from_dataframe(df_2)
                times = timeit.repeat(
                    lambda: func(df_1_bed, df_2_bed),
                    repeat=num_repeats,
                    number=num_executions,
                )
            elif tool == "pygenomics":
                df_1 = pd.read_parquet(
                    df_path_1.replace("*.parquet", ""), engine="pyarrow"
                )
                df_2 = pd.read_parquet(
                    df_path_2.replace("*.parquet", ""), engine="pyarrow"
                )
                df_1_pg = GenomicBase(
                    [(r.contig, r.pos_start, r.pos_end) for r in df_1.itertuples()]
                )
                df_2_array = df_2.values.tolist()
                times = timeit.repeat(
                    lambda: func(df_1_pg, df_2_array),
                    repeat=num_repeats,
                    number=num_executions,
                )
            elif tool == "genomicranges":
                df_1 = pd.read_parquet(
                    df_path_1.replace("*.parquet", ""), engine="pyarrow"
                )
                df_2 = pd.read_parquet(
                    df_path_2.replace("*.parquet", ""), engine="pyarrow"
                )
                df_1_gr = GenomicRanges.from_pandas(
                    df_1.rename(
                        columns={
                            "contig": "seqnames",
                            "pos_start": "starts",
                            "pos_end": "ends",
                        }
                    )
                )
                df_2_gr = GenomicRanges.from_pandas(
                    df_2.rename(
                        columns={
                            "contig": "seqnames",
                            "pos_start": "starts",
                            "pos_end": "ends",
                        }
                    )
                )
                times = timeit.repeat(
                    lambda: func(df_1_gr, df_2_gr),
                    repeat=num_repeats,
                    number=num_executions,
                )
            else:
                logger.error(emoji.emojize(f"Tool {tool} not found :no_entry:"))
                exit(1)
            logger.info(
                emoji.emojize(f"Finished benchmark for {tool} :check_mark_button:")
            )
            per_run_times = [
                time / num_executions for time in times
            ]  # Convert to per-run times
            results.append(
                {
                    "name": tool,
                    "min": min(per_run_times),
                    "max": max(per_run_times),
                    "mean": np.mean(per_run_times),
                }
            )
        fastest_mean = min(result["mean"] for result in results)
        for result in results:
            result["speedup"] = fastest_mean / result["mean"]

        # Create Rich table
        table = Table(
            title=f"Benchmark Results, operation: {operation} dataset: {dataset}, test: {t}",
            box=MARKDOWN,
        )
        table.add_column("Library", justify="left", style="cyan", no_wrap=True)
        table.add_column("Min (s)", justify="right", style="green")
        table.add_column("Max (s)", justify="right", style="green")
        table.add_column("Mean (s)", justify="right", style="green")
        table.add_column("Speedup", justify="right", style="magenta")

        # Add rows to the table
        for result in results:
            table.add_row(
                result["name"],
                f"{result['min']:.6f}",
                f"{result['max']:.6f}",
                f"{result['mean']:.6f}",
                f"{result['speedup']:.2f}x",
            )
        rich.print(table)
        console.log(table)
        console.save_text(REPORT_FILE, clear=False, styles=False)
    logger.info(emoji.emojize(f"Finished benchmark {b["name"]} :check_mark_button:"))
