import os

import click
import emoji
import yaml

from logger import logger
from operations import (
    e2e_overlap_bioframe,
    e2e_overlap_polars_bio,
    e2e_overlap_polars_bio_streaming,
    e2e_overlap_pyranges0,
    e2e_overlap_pyranges1,
)


@click.command()
@click.option(
    "--bench-config",
    help="Benchmark config file",
)
@click.option(
    "--tool",
    help="Tool to profile",
)
@click.option(
    "--test-case",
    help="Test case to profile",
)
def run(bench_config: str, tool: str, test_case: str):
    BECH_DATA_ROOT = os.getenv("BENCH_DATA_ROOT")
    if not BECH_DATA_ROOT:
        logger.error(
            emoji.emojize("Env variable BENCH_DATA_ROOT is not set :pile_of_poo:")
        )
        exit(1)

    logger.info(f"Using config file: {bench_config}")
    logger.info(emoji.emojize("Starting polars_bio memory_profiler :rocket:"))

    with open("conf/common.yaml", "r") as file:
        config = yaml.safe_load(file)
    logger.info(emoji.emojize("Loaded config. :open_book:"))
    with open(bench_config, "r") as file:
        benchmarks = yaml.safe_load(file)
    logger.info(emoji.emojize("Loaded benchmarks. :open_book:"))
    test_cases = config["test-cases"]
    benchmarks = benchmarks["benchmarks"]
    dataset = benchmarks[0]["dataset"]
    test = [test for test in test_cases if test["name"] == test_case][0]
    df_path_1 = (
        f"{BECH_DATA_ROOT}/{dataset}/{test['df_path_1']}"
        if "df_path_1" in test
        else None
    )
    df_path_2 = (
        f"{BECH_DATA_ROOT}/{dataset}/{test['df_path_2']}"
        if "df_path_2" in test
        else None
    )
    functions_e2_overlap = [
        e2e_overlap_polars_bio,
        e2e_overlap_bioframe,
        e2e_overlap_pyranges0,
        e2e_overlap_pyranges1,
        e2e_overlap_polars_bio_streaming,
    ]
    test_func = [func for func in functions_e2_overlap if func.__name__.endswith(tool)][
        0
    ]
    logger.info(f"Running test case: {test_case}")
    logger.info(f"Running tool: {tool}")
    logger.info(f"Running dataset: {dataset}")
    test_func(df_path_1, df_path_2)


if __name__ == "__main__":
    run()
