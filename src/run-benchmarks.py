import inspect
import os
import time
import timeit
from dataclasses import dataclass
from typing import Any, Callable

import click
import emoji
import numpy as np
import pandas as pd
import polars as pl
import polars_bio as pb
import pybedtools
import yaml
from genomicranges import GenomicRanges
from polars_bio._metadata import set_coordinate_system
from pygenomics.interval import GenomicBase
from rich.box import MARKDOWN
from rich.console import Console
from rich.markup import escape
from rich.table import Table
from tqdm import tqdm

import operations as ops
from logger import logger
from utils import df2pr1, prepare_datatests


@dataclass(frozen=True)
class ToolVariant:
    base_tool: str
    name: str
    input_type: str | None = None
    output_type: str | None = None


@dataclass
class TimedInvocation:
    func: Callable[[], Any]
    row_count_fallback: Callable[[], int | None] | None = None
    last_result: Any = None

    def __call__(self) -> Any:
        self.last_result = self.func()
        return self.last_result

    def row_count(self) -> int | None:
        if self.last_result is not None:
            return int(self.last_result)
        if self.row_count_fallback is None:
            return None
        row_count = self.row_count_fallback()
        if row_count is None:
            return None
        return int(row_count)


class TestCaseInputs:
    def __init__(
        self,
        df_path_1: str | None,
        df_path_2: str | None,
        coordinate_system_zero_based: bool = True,
    ):
        self.df_path_1 = df_path_1
        self.df_path_2 = df_path_2
        self.coordinate_system_zero_based = coordinate_system_zero_based
        self._pandas_frames: tuple[pd.DataFrame, pd.DataFrame | None] | None = None
        self._pandas_pyarrow_frames: tuple[pd.DataFrame, pd.DataFrame | None] | None = (
            None
        )
        self._polars_frames: tuple[pl.DataFrame, pl.DataFrame | None] | None = None
        self._polars_lazy_frames: tuple[pl.LazyFrame, pl.LazyFrame | None] | None = None
        self._pyranges_frames = None
        self._pybedtools_frames = None
        self._pygenomics_frames = None
        self._genomicranges_frames = None

    def parquet_paths(self) -> tuple[str | None, str | None]:
        return self.df_path_1, self.df_path_2

    def pandas_frames(self) -> tuple[pd.DataFrame, pd.DataFrame | None]:
        if self._pandas_frames is None:
            self._pandas_frames = (
                _set_polars_bio_coordinate_system(
                    _read_pandas_parquet(self.df_path_1),
                    self.coordinate_system_zero_based,
                ),
                _set_polars_bio_coordinate_system(
                    _read_pandas_parquet(self.df_path_2),
                    self.coordinate_system_zero_based,
                ),
            )
        return self._pandas_frames

    def pandas_pyarrow_frames(self) -> tuple[pd.DataFrame, pd.DataFrame | None]:
        if self._pandas_pyarrow_frames is None:
            self._pandas_pyarrow_frames = (
                _set_polars_bio_coordinate_system(
                    _read_pandas_parquet(
                        self.df_path_1,
                        dtype_backend="pyarrow",
                    ),
                    self.coordinate_system_zero_based,
                ),
                _set_polars_bio_coordinate_system(
                    _read_pandas_parquet(
                        self.df_path_2,
                        dtype_backend="pyarrow",
                    ),
                    self.coordinate_system_zero_based,
                ),
            )
        return self._pandas_pyarrow_frames

    def polars_frames(self) -> tuple[pl.DataFrame, pl.DataFrame | None]:
        if self._polars_frames is None:
            self._polars_frames = (
                _set_polars_bio_coordinate_system(
                    _read_polars_parquet(self.df_path_1),
                    self.coordinate_system_zero_based,
                ),
                _set_polars_bio_coordinate_system(
                    _read_polars_parquet(self.df_path_2),
                    self.coordinate_system_zero_based,
                ),
            )
        return self._polars_frames

    def polars_lazy_frames(self) -> tuple[pl.LazyFrame, pl.LazyFrame | None]:
        if self._polars_lazy_frames is None:
            self._polars_lazy_frames = (
                _set_polars_bio_coordinate_system(
                    _scan_polars_parquet(self.df_path_1),
                    self.coordinate_system_zero_based,
                ),
                _set_polars_bio_coordinate_system(
                    _scan_polars_parquet(self.df_path_2),
                    self.coordinate_system_zero_based,
                ),
            )
        return self._polars_lazy_frames

    def polars_bio_inputs(
        self, input_type: str | None
    ) -> tuple[str | pd.DataFrame | pl.DataFrame | pl.LazyFrame | None, Any]:
        normalized_input_type = normalize_polars_bio_input_type(input_type)
        if normalized_input_type == "parquet":
            return self.parquet_paths()
        if normalized_input_type == "pandas.DataFrame":
            return self.pandas_frames()
        if normalized_input_type == "pandas.pyarrow.DataFrame":
            return self.pandas_pyarrow_frames()
        if normalized_input_type == "polars.DataFrame":
            return self.polars_frames()
        if normalized_input_type == "polars.LazyFrame":
            return self.polars_lazy_frames()
        raise ValueError(f"Unsupported polars_bio input type: {normalized_input_type}")

    def pyranges_frames(self):
        if self._pyranges_frames is None:
            df_1, df_2 = self.pandas_frames()
            self._pyranges_frames = (
                df2pr1(df_1),
                df2pr1(df_2) if df_2 is not None else None,
            )
        return self._pyranges_frames

    def pybedtools_frames(self):
        if self._pybedtools_frames is None:
            df_1, df_2 = self.pandas_frames()
            bed_df_1 = df_1.sort_values(by=["contig", "pos_start", "pos_end"])
            bed_df_2 = (
                df_2.sort_values(by=["contig", "pos_start", "pos_end"])
                if df_2 is not None
                else None
            )
            self._pybedtools_frames = (
                pybedtools.BedTool.from_dataframe(bed_df_1),
                (
                    pybedtools.BedTool.from_dataframe(bed_df_2)
                    if bed_df_2 is not None
                    else None
                ),
            )
        return self._pybedtools_frames

    def pygenomics_frames(self):
        if self._pygenomics_frames is None:
            df_1, df_2 = self.pandas_frames()
            self._pygenomics_frames = (
                GenomicBase(
                    [
                        (row.contig, row.pos_start, row.pos_end)
                        for row in df_1.itertuples()
                    ]
                ),
                df_2.values.tolist() if df_2 is not None else None,
            )
        return self._pygenomics_frames

    def genomicranges_frames(self):
        if self._genomicranges_frames is None:
            df_1, df_2 = self.pandas_frames()
            self._genomicranges_frames = (
                _to_genomicranges(df_1),
                _to_genomicranges(df_2),
            )
        return self._genomicranges_frames


POLARS_BIO_INPUT_ALIASES = {
    None: "parquet",
    "path": "parquet",
    "parquet_path": "parquet",
    "parquet": "parquet",
    "pandas": "pandas.DataFrame",
    "pandas.DataFrame": "pandas.DataFrame",
    "pandas.pyarrow": "pandas.pyarrow.DataFrame",
    "pandas.pyarrow.DataFrame": "pandas.pyarrow.DataFrame",
    "pandas.PyArrowDataFrame": "pandas.pyarrow.DataFrame",
    "pandas_arrow": "pandas.pyarrow.DataFrame",
    "polars": "polars.DataFrame",
    "polars.DataFrame": "polars.DataFrame",
    "polars.LazyFrame": "polars.LazyFrame",
    "lazy": "polars.LazyFrame",
}


POLARS_BIO_COORDINATE_SYSTEM_ALIASES = {
    None: True,
    True: True,
    False: False,
    "0-based": True,
    "0_based": True,
    "0based": True,
    "zero-based": True,
    "zero_based": True,
    "zero based": True,
    "zero": True,
    "0": True,
    "true": True,
    "1-based": False,
    "1_based": False,
    "1based": False,
    "one-based": False,
    "one_based": False,
    "one based": False,
    "one": False,
    "1": False,
    "false": False,
}


POLARS_BIO_CONSUME_MODE_ALIASES = {
    None: "count",
    "count": "count",
    "len": "len",
    "length": "len",
    "materialize": "len",
}


NON_PARALLEL_TOOLS = {"bioframe", "pyranges1", "pybedtools", "pygenomics"}


OPERATION_FUNCTIONS = {
    "overlap": {
        "polars_bio": [
            ops.overlap_polars_bio,
            ops.overlap_polars_bio_intervaltree,
            ops.overlap_polars_bio_arrayintervaltree,
            ops.overlap_polars_bio_lapper,
            ops.overlap_polars_bio_superintervals,
        ],
        "bioframe": [ops.overlap_bioframe],
        "pyranges1": [
            ops.overlap_pyranges1_join_overlaps,
            ops.overlap_pyranges1_overlap,
        ],
        "pybedtools": [ops.overlap_pybedtools],
        "pygenomics": [ops.overlap_pygenomics],
        "genomicranges": [ops.overlap_genomicranges],
    },
    "nearest": {
        "polars_bio": [ops.nearest_polars_bio],
        "bioframe": [ops.nearest_bioframe],
        "pyranges1": [ops.nearest_pyranges1],
        "pybedtools": [ops.nearest_pybedtools],
        "genomicranges": [ops.nearest_genomicranges],
    },
    "count_overlaps": {
        "polars_bio": [ops.count_overlaps_polars_bio],
        "bioframe": [ops.count_overlaps_bioframe],
        "pyranges1": [ops.count_overlaps_pyranges1],
        "pybedtools": [ops.count_overlaps_pybedtools],
        "genomicranges": [ops.count_overlaps_genomicranges],
    },
    "merge": {
        "polars_bio": [ops.merge_polars_bio],
        "bioframe": [ops.merge_bioframe],
        "pyranges1": [ops.merge_pyranges1],
        "genomicranges": [ops.merge_genomicranges],
    },
    "cluster": {
        "polars_bio": [ops.cluster_polars_bio],
        "bioframe": [ops.cluster_bioframe],
        "pyranges1": [ops.cluster_pyranges1],
    },
    "complement": {
        "polars_bio": [ops.complement_polars_bio],
        "bioframe": [ops.complement_bioframe],
        "pyranges1": [ops.complement_pyranges1],
        "genomicranges": [ops.complement_genomicranges],
    },
    "subtract": {
        "polars_bio": [ops.subtract_polars_bio],
        "bioframe": [ops.subtract_bioframe],
        "pyranges1": [ops.subtract_pyranges1],
        "genomicranges": [ops.subtract_genomicranges],
    },
    "coverage": {
        "polars_bio": [ops.coverage_polars_bio],
        "bioframe": [ops.coverage_bioframe],
        "pyranges1": [ops.coverage_pyranges1],
        "pybedtools": [ops.coverage_pybedtools],
        "genomicranges": [ops.coverage_genomicranges],
    },
    "read_vcf": {
        "polars_bio": [ops.read_vcf_polars_bio],
    },
    "e2e_overlap": {
        "polars_bio": [
            ops.e2e_overlap_polars_bio,
            ops.e2e_overlap_polars_bio_streaming,
        ],
        "bioframe": [ops.e2e_overlap_bioframe],
        "pyranges1": [ops.e2e_overlap_pyranges1],
        "genomicranges": [ops.e2e_overlap_genomicranges],
    },
    "e2e_nearest": {
        "polars_bio": [
            ops.e2e_nearest_polars_bio,
            ops.e2e_nearest_polars_bio_streaming,
        ],
        "bioframe": [ops.e2e_nearest_bioframe],
        "pyranges1": [ops.e2e_nearest_pyranges1],
        "genomicranges": [ops.e2e_nearest_genomicranges],
    },
    "e2e_coverage": {
        "polars_bio": [
            ops.e2e_coverage_polars_bio,
            ops.e2e_coverage_polars_bio_streaming,
        ],
        "bioframe": [ops.e2e_coverage_bioframe],
        "pyranges1": [ops.e2e_coverage_pyranges1],
    },
    "e2e_count_overlaps": {
        "polars_bio": [
            ops.e2e_count_overlaps_polars_bio,
            ops.e2e_count_overlaps_polars_bio_streaming,
        ],
        "bioframe": [ops.e2e_count_overlaps_bioframe],
        "pyranges1": [ops.e2e_count_overlaps_pyranges1],
        "genomicranges": [ops.e2e_count_overlaps_genomicranges],
    },
}


def _pandas_parquet_path(path: str | None) -> str | None:
    if path is None:
        return None
    return path.replace("*.parquet", "")


def _read_pandas_parquet(
    path: str | None,
    dtype_backend: str | None = None,
) -> pd.DataFrame | None:
    parquet_path = _pandas_parquet_path(path)
    if parquet_path is None:
        return None
    read_parquet_kwargs: dict[str, Any] = {"engine": "pyarrow"}
    if dtype_backend is not None:
        if "dtype_backend" not in inspect.signature(pd.read_parquet).parameters:
            raise RuntimeError(
                "pandas parquet Arrow dtype backend requires pandas read_parquet(dtype_backend=...) support"
            )
        read_parquet_kwargs["dtype_backend"] = dtype_backend
    return pd.read_parquet(parquet_path, **read_parquet_kwargs)


def _read_polars_parquet(path: str | None) -> pl.DataFrame | None:
    if path is None:
        return None
    return pl.read_parquet(path)


def _scan_polars_parquet(path: str | None) -> pl.LazyFrame | None:
    if path is None:
        return None
    return pl.scan_parquet(path)


def _to_genomicranges(df: pd.DataFrame | None):
    if df is None:
        return None
    return GenomicRanges.from_pandas(
        df.rename(
            columns={
                "contig": "seqnames",
                "pos_start": "starts",
                "pos_end": "ends",
            }
        )
    )


def _set_polars_bio_coordinate_system(
    df: pd.DataFrame | pl.DataFrame | pl.LazyFrame | None,
    zero_based: bool,
):
    if df is None:
        return None
    set_coordinate_system(df, zero_based=zero_based)
    return df


def normalize_polars_bio_input_type(input_type: str | None) -> str:
    normalized_input_type = POLARS_BIO_INPUT_ALIASES.get(input_type, input_type)
    supported_input_types = {
        "parquet",
        "pandas.DataFrame",
        "pandas.pyarrow.DataFrame",
        "polars.DataFrame",
        "polars.LazyFrame",
    }
    if normalized_input_type not in supported_input_types:
        raise ValueError(f"Unsupported polars_bio input type: {input_type}")
    return normalized_input_type


def normalize_polars_bio_coordinate_system(value: Any) -> bool:
    if isinstance(value, str):
        normalized_value = value.strip().lower()
    else:
        normalized_value = value

    coordinate_system_zero_based = POLARS_BIO_COORDINATE_SYSTEM_ALIASES.get(
        normalized_value
    )
    if coordinate_system_zero_based is None:
        raise ValueError(f"Unsupported polars_bio coordinate system: {value}")
    return coordinate_system_zero_based


def normalize_polars_bio_consume_mode(value: Any) -> str:
    if isinstance(value, str):
        normalized_value = value.strip().lower()
    else:
        normalized_value = value

    consume_mode = POLARS_BIO_CONSUME_MODE_ALIASES.get(normalized_value)
    if consume_mode is None:
        raise ValueError(f"Unsupported polars_bio consume mode: {value}")
    return consume_mode


def parse_polars_bio_io_spec(
    io_spec: str | dict[str, str],
    default_output_type: str,
) -> tuple[str, str]:
    if isinstance(io_spec, str):
        input_type, output_type = io_spec.split(":", 1)
        return normalize_polars_bio_input_type(input_type.strip()), output_type.strip()

    input_type = io_spec.get("input_type") or io_spec.get("input")
    if input_type is None:
        raise ValueError(f"Missing input_type in polars_bio IO spec: {io_spec}")
    output_type = io_spec.get("output_type", default_output_type)
    return normalize_polars_bio_input_type(input_type), output_type


def polars_bio_variant_name(input_type: str, output_type: str) -> str:
    return f"polars_bio[{input_type}->{output_type}]"


def build_tool_variants(
    benchmark: dict[str, Any],
    default_polars_bio_output_type: str,
    console: Console,
) -> list[ToolVariant]:
    tool_variants: list[ToolVariant] = []
    benchmark_output_type = benchmark.get(
        "polars_bio_output_type",
        default_polars_bio_output_type,
    )

    for tool in benchmark["tools"]:
        if tool == "polars_bio":
            tool_variants.append(
                ToolVariant(
                    base_tool="polars_bio",
                    name="polars_bio",
                    input_type="parquet",
                    output_type=benchmark_output_type,
                )
            )
            if benchmark_output_type != "polars.LazyFrame":
                console.log(
                    f":bulb: Benchmark {benchmark['name']} uses polars_bio output_type={benchmark_output_type}"
                )
            continue
        tool_variants.append(ToolVariant(base_tool=tool, name=tool))

    use_dataframe_inputs = (
        benchmark.get("input_dataframes", False)
        and not benchmark["operation"].startswith("e2e_")
        and benchmark["operation"] != "read_vcf"
    )
    if not use_dataframe_inputs:
        return tool_variants

    for io_spec in benchmark.get("dataframes_io", []):
        input_type, output_type = parse_polars_bio_io_spec(
            io_spec,
            benchmark_output_type,
        )
        tool_variants.append(
            ToolVariant(
                base_tool="polars_bio",
                name=polars_bio_variant_name(input_type, output_type),
                input_type=input_type,
                output_type=output_type,
            )
        )

    return tool_variants


def select_operation_functions(
    operation: str,
    tool: str,
    all_algorithms: bool,
) -> list[Callable[..., Any]]:
    operation_table = OPERATION_FUNCTIONS.get(operation)
    if operation_table is None:
        raise ValueError(f"Operation {operation} not found")

    tool_functions = operation_table.get(tool, [])
    if operation == "overlap" and tool == "polars_bio" and not all_algorithms:
        return tool_functions[:1]
    return tool_functions


def configure_polars_bio_threads(
    operation: str,
    thread_count: int,
    repartition: bool,
    coordinate_system_zero_based: bool,
) -> None:
    pb.set_option(
        "datafusion.bio.coordinate_system_zero_based",
        str(coordinate_system_zero_based).lower(),
    )
    if operation != "read_vcf":
        pb.set_option("datafusion.execution.target_partitions", str(thread_count))

    if thread_count == 1:
        pb.set_option("datafusion.optimizer.repartition_joins", "false")
        pb.set_option("datafusion.optimizer.repartition_file_scans", "false")
        pb.set_option("datafusion.execution.coalesce_batches", "false")
        return

    if repartition:
        pb.set_option("datafusion.optimizer.repartition_joins", "true")
        pb.set_option("datafusion.optimizer.repartition_file_scans", "true")
        pb.set_option("datafusion.execution.coalesce_batches", "false")
        return

    pb.set_option("datafusion.optimizer.repartition_joins", "false")
    pb.set_option("datafusion.optimizer.repartition_file_scans", "false")
    pb.set_option("datafusion.execution.coalesce_batches", "false")


def _csv_output_row_count() -> int | None:
    if not os.path.exists(ops.OUTPUT_CSV):
        return None
    with open(ops.OUTPUT_CSV, "r", encoding="utf-8") as output_file:
        return max(sum(1 for _ in output_file) - 1, 0)


def build_result_name(
    operation: str,
    tool_variant: ToolVariant,
    func: Callable[..., Any],
    thread_count: int,
) -> str:
    func_name = func.__name__.replace(f"{operation}_", "", 1)
    if func_name == tool_variant.base_tool:
        result_name = tool_variant.name
    elif func_name.startswith(f"{tool_variant.base_tool}_"):
        suffix = func_name.removeprefix(f"{tool_variant.base_tool}_")
        if "[" in tool_variant.name:
            prefix, details = tool_variant.name.split("[", 1)
            result_name = f"{prefix}_{suffix}[{details}"
        else:
            result_name = f"{tool_variant.name}_{suffix}"
    else:
        result_name = func_name

    if thread_count != 1:
        return f"{result_name}-{thread_count}"
    return result_name


def build_timed_invocation(
    operation: str,
    tool_variant: ToolVariant,
    func: Callable[..., Any],
    inputs: TestCaseInputs,
    thread_count: int,
    polars_bio_consume_mode: str,
) -> TimedInvocation | None:
    if thread_count != 1 and tool_variant.base_tool in NON_PARALLEL_TOOLS:
        return None

    row_count_fallback = _csv_output_row_count if operation.startswith("e2e_") else None

    if operation == "read_vcf":
        return TimedInvocation(
            lambda: func(
                inputs.df_path_1,
                th=thread_count,
                consume_mode=polars_bio_consume_mode,
            )
        )

    if tool_variant.base_tool == "polars_bio":
        df_1, df_2 = inputs.polars_bio_inputs(tool_variant.input_type)
        return TimedInvocation(
            lambda: func(
                df_1,
                df_2,
                output_type=tool_variant.output_type,
                consume_mode=polars_bio_consume_mode,
            ),
            row_count_fallback=row_count_fallback,
        )

    if tool_variant.base_tool == "bioframe":
        if operation.startswith("e2e_"):
            df_path_1, df_path_2 = inputs.parquet_paths()
            return TimedInvocation(
                lambda: func(df_path_1, df_path_2),
                row_count_fallback=row_count_fallback,
            )
        df_1, df_2 = inputs.pandas_frames()
        return TimedInvocation(lambda: func(df_1, df_2))

    if tool_variant.base_tool == "pyranges1":
        if operation.startswith("e2e_"):
            df_path_1, df_path_2 = inputs.parquet_paths()
            return TimedInvocation(
                lambda: func(df_path_1, df_path_2),
                row_count_fallback=row_count_fallback,
            )
        df_1_pr1, df_2_pr1 = inputs.pyranges_frames()
        return TimedInvocation(lambda: func(df_1_pr1, df_2_pr1))

    if tool_variant.base_tool == "pybedtools":
        df_1_bed, df_2_bed = inputs.pybedtools_frames()
        return TimedInvocation(lambda: func(df_1_bed, df_2_bed))

    if tool_variant.base_tool == "pygenomics":
        df_1_pg, df_2_array = inputs.pygenomics_frames()
        return TimedInvocation(lambda: func(df_1_pg, df_2_array))

    if tool_variant.base_tool == "genomicranges":
        if operation.startswith("e2e_"):
            df_path_1, df_path_2 = inputs.parquet_paths()
            return TimedInvocation(
                lambda: func(df_path_1, df_path_2, n=thread_count),
                row_count_fallback=row_count_fallback,
            )
        df_1_gr, df_2_gr = inputs.genomicranges_frames()
        return TimedInvocation(lambda: func(df_1_gr, df_2_gr, n=thread_count))

    return None


def resolve_baseline_mean(results: list[dict[str, Any]], baseline: str) -> float:
    if baseline == "fastest":
        return min(result["mean"] for result in results)
    if baseline == "slowest":
        return max(result["mean"] for result in results)

    for result in results:
        if result["name"] == baseline:
            return result["mean"]

    raise ValueError(f"Baseline '{baseline}' not found in benchmark results")


def add_speedups(results: list[dict[str, Any]], baseline: str) -> None:
    baseline_mean = resolve_baseline_mean(results, baseline)
    for result in results:
        result["speedup"] = baseline_mean / result["mean"]


def render_results_table(
    results: list[dict[str, Any]],
    operation: str,
    dataset: str,
    test_name: str,
) -> Table:
    table = Table(
        title=f"Benchmark Results, operation: {operation} dataset: {dataset}, test: {test_name}",
        box=MARKDOWN,
    )
    table.add_column("Library", justify="left", style="cyan")
    table.add_column("Rows Returned", justify="right", style="yellow")
    table.add_column("Min (s)", justify="right", style="green")
    table.add_column("Max (s)", justify="right", style="green")
    table.add_column("Mean (s)", justify="right", style="green")
    table.add_column("Speedup", justify="right", style="magenta")

    for result in results:
        rows_returned = result["rows_returned"]
        table.add_row(
            escape(result["name"]),
            "n/a" if rows_returned is None else f"{rows_returned}",
            f"{result['min']:.6f}",
            f"{result['max']:.6f}",
            f"{result['mean']:.6f}",
            f"{result['speedup']:.2f}x",
        )

    return table


def export_results(
    results: list[dict[str, Any]],
    output_path: str,
    export_format: str,
) -> None:
    result_frame = pd.DataFrame(results)
    if export_format == "csv":
        result_frame.to_csv(output_path, index=False)


def resolve_test_case_inputs(
    bench_data_root: str,
    benchmark_dataset: str,
    test_case: dict[str, Any],
    coordinate_system_zero_based: bool,
) -> tuple[str, TestCaseInputs]:
    dataset = test_case.get("dataset", benchmark_dataset)
    df_path_1 = (
        f"{bench_data_root}/{dataset}/{test_case['df_path_1']}"
        if "df_path_1" in test_case
        else None
    )
    df_path_2 = (
        f"{bench_data_root}/{dataset}/{test_case['df_path_2']}"
        if "df_path_2" in test_case
        else None
    )
    return dataset, TestCaseInputs(
        df_path_1,
        df_path_2,
        coordinate_system_zero_based=coordinate_system_zero_based,
    )


def run_benchmark(
    benchmarks: list[dict[str, Any]],
    test_cases: list[dict[str, Any]],
    bench_data_root: str,
    output_dir: str,
    baseline: str,
    export_format: str,
    default_polars_bio_output_type: str = "polars.LazyFrame",
    default_polars_bio_coordinate_system: Any = "0-based",
    default_polars_bio_consume_mode: Any = "count",
    console: Console = Console(record=True),
) -> None:
    test_cases_by_name = {test_case["name"]: test_case for test_case in test_cases}

    for benchmark in tqdm(benchmarks, desc="Running benchmarks"):
        benchmark_name = benchmark["name"]
        benchmark_dataset = benchmark["dataset"]
        operation = benchmark["operation"]
        num_executions = benchmark["num_executions"]
        num_repeats = benchmark["num_repeats"]
        repartition = benchmark.get("repartition", False)
        all_algorithms = benchmark.get("all_algorithms", False)
        coordinate_system_zero_based = normalize_polars_bio_coordinate_system(
            benchmark.get(
                "polars_bio_coordinate_system",
                default_polars_bio_coordinate_system,
            )
        )
        polars_bio_consume_mode = normalize_polars_bio_consume_mode(
            benchmark.get(
                "polars_bio_consume_mode",
                default_polars_bio_consume_mode,
            )
        )
        thread_counts = benchmark["threads"] if benchmark["parallel"] else [1]
        tool_variants = build_tool_variants(
            benchmark,
            default_polars_bio_output_type,
            console,
        )

        console.log(
            f"## Benchmark {benchmark_name} for {operation} with dataset {benchmark_dataset}\n"
        )
        logger.info(emoji.emojize(f"Running benchmark {benchmark_name} :racing_car: "))

        pb.set_option("datafusion.execution.batch_size", str(65536))

        for test_name in tqdm(
            benchmark["test-cases"], desc=f"{benchmark_name} tests", leave=False
        ):
            test_case = test_cases_by_name.get(test_name)
            if test_case is None:
                logger.warning(
                    emoji.emojize(
                        f"Test case {test_name} not found in conf/common.yaml :warning: Skipping."
                    )
                )
                console.log(f":bulb: Skipping unknown test-case '{test_name}'")
                continue

            resolved_dataset, inputs = resolve_test_case_inputs(
                bench_data_root,
                benchmark_dataset,
                test_case,
                coordinate_system_zero_based,
            )
            results: list[dict[str, Any]] = []

            for thread_count in thread_counts:
                configure_polars_bio_threads(
                    operation,
                    thread_count,
                    repartition,
                    coordinate_system_zero_based,
                )
                logger.info(
                    emoji.emojize(
                        f"Running benchmark {benchmark_name} with {thread_count} threads :gear:"
                    )
                )
                logger.info(
                    emoji.emojize(f"Loading test case {test_name}... :chequered_flag:")
                )

                for tool_variant in tqdm(
                    tool_variants,
                    desc=f"{test_name} tools",
                    leave=False,
                ):
                    logger.info(
                        emoji.emojize(
                            f"Running benchmark {benchmark_name}, test-case {test_name} for {tool_variant.name} :hammer_and_wrench:"
                        )
                    )

                    tool_functions = select_operation_functions(
                        operation,
                        tool_variant.base_tool,
                        all_algorithms,
                    )
                    if not tool_functions:
                        logger.warning(
                            emoji.emojize(
                                f"Operation {operation} not found for tool {tool_variant.base_tool} :no_entry:"
                            )
                        )
                        console.log(
                            f":bulb: Tool {tool_variant.base_tool} does not support operation {operation}"
                        )
                        continue

                    for func in tool_functions:
                        invocation = build_timed_invocation(
                            operation,
                            tool_variant,
                            func,
                            inputs,
                            thread_count,
                            polars_bio_consume_mode,
                        )
                        if invocation is None:
                            continue

                        timings = timeit.repeat(
                            invocation,
                            repeat=num_repeats,
                            number=num_executions,
                        )
                        per_run_timings = [
                            elapsed / num_executions for elapsed in timings
                        ]

                        logger.info(
                            emoji.emojize(
                                f"Finished benchmark for {tool_variant.name} :check_mark_button:"
                            )
                        )

                        results.append(
                            {
                                "name": build_result_name(
                                    operation,
                                    tool_variant,
                                    func,
                                    thread_count,
                                ),
                                "rows_returned": invocation.row_count(),
                                "min": min(per_run_timings),
                                "max": max(per_run_timings),
                                "mean": float(np.mean(per_run_timings)),
                            }
                        )

            if not results:
                console.log(
                    f":bulb: No benchmark results collected for {benchmark_name}/{test_name}"
                )
                continue

            add_speedups(results, baseline)
            table = render_results_table(
                results,
                operation,
                resolved_dataset,
                test_name,
            )
            console.print(table)

            table_path = f"{output_dir}/{benchmark_name}_{test_name}.{export_format}"
            export_results(results, table_path, export_format)
            console.save_text(
                f"{output_dir}/benchmark_results.md",
                clear=False,
                styles=False,
            )

        logger.info(
            emoji.emojize(f"Finished benchmark {benchmark_name} :check_mark_button:")
        )

    console.print("Benchmark results saved to benchmark_results.md")


@click.command()
@click.option(
    "--bench-config",
    default="conf/benchmark_small.yaml",
    help="Benchmark config file (default: conf/benchmark_small.yaml)",
)
def run(bench_config: str) -> None:
    logger.info(f"Using config file: {bench_config}")
    tag_datetime = time.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(emoji.emojize("Starting polars_bio_benchmark :rocket:"))

    output_dir = f"results/{tag_datetime}"
    os.makedirs(output_dir, exist_ok=True)

    report_file = f"{output_dir}/benchmark_results.md"
    if os.path.exists(report_file):
        logger.info(
            emoji.emojize(
                f"Performance report file {report_file} already exist...quiting. Rename/remove it to re-run the benchmark :wastebasket:"
            )
        )
        raise SystemExit(1)

    bench_data_root = os.getenv("BENCH_DATA_ROOT")
    if not bench_data_root:
        logger.error(
            emoji.emojize("Env variable BENCH_DATA_ROOT is not set :pile_of_poo:")
        )
        raise SystemExit(1)

    with open("conf/common.yaml", "r", encoding="utf-8") as config_file:
        common_config = yaml.safe_load(config_file)
    logger.info(emoji.emojize("Loaded config. :open_book:"))

    with open(bench_config, "r", encoding="utf-8") as benchmark_file:
        benchmark_config = yaml.safe_load(benchmark_file)
    logger.info(emoji.emojize("Loaded benchmarks. :open_book:"))

    datasets = common_config["datasets"]
    test_cases = common_config["test-cases"]
    common_benchmark_config = benchmark_config["common"]
    baseline = common_benchmark_config["baseline"].lower()
    default_polars_bio_output_type = common_benchmark_config.get(
        "polars_bio_output_type",
        "polars.LazyFrame",
    )
    default_polars_bio_coordinate_system = common_benchmark_config.get(
        "polars_bio_coordinate_system",
        "0-based",
    )
    default_polars_bio_consume_mode = common_benchmark_config.get(
        "polars_bio_consume_mode",
        "count",
    )
    benchmarks = benchmark_config["benchmarks"]
    export_format = common_config["benchmark"]["export"]["format"].lower()

    prepare_datatests(datasets, bench_data_root)

    run_benchmark(
        benchmarks,
        test_cases,
        bench_data_root,
        output_dir,
        baseline,
        export_format,
        default_polars_bio_output_type=default_polars_bio_output_type,
        default_polars_bio_coordinate_system=default_polars_bio_coordinate_system,
        default_polars_bio_consume_mode=default_polars_bio_consume_mode,
    )
    logger.info(emoji.emojize("Finished polars_bio_benchmark :check_mark_button:"))


if __name__ == "__main__":
    run()
