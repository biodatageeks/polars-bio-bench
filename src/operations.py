import itertools
from typing import Any

import bioframe as bf
import pandas as pd
import polars as pl
import polars_bio as pb
from genomicranges import GenomicRanges
from memory_profiler import profile

from utils import df2pr1, overlaps_to_df

columns = ("contig", "pos_start", "pos_end")
OUTPUT_CSV = "/tmp/output.csv"
POLARS_BIO_CONSUME_MODES = {"count", "len"}


def _pandas_parquet_path(path: str | None) -> str | None:
    if path is None:
        return None
    return path.replace("*.parquet", "")


def _read_pandas_parquet(path: str | None) -> pd.DataFrame | None:
    parquet_path = _pandas_parquet_path(path)
    if parquet_path is None:
        return None
    return pd.read_parquet(parquet_path, engine="pyarrow")


def _collect_lazyframe_count(df: pl.LazyFrame) -> int:
    return int(df.select(pl.len()).collect().item())


def _normalize_polars_bio_consume_mode(consume_mode: str) -> str:
    normalized_consume_mode = consume_mode.strip().lower()
    if normalized_consume_mode not in POLARS_BIO_CONSUME_MODES:
        raise ValueError(f"Unsupported polars_bio consume mode: {consume_mode}")
    return normalized_consume_mode


def _collect_datafusion_len(df: Any) -> int:
    return sum(batch.num_rows for batch in df.collect())


def _consume_polars_bio_result(
    df: Any,
    output_type: str,
    consume_mode: str = "count",
) -> int:
    normalized_consume_mode = _normalize_polars_bio_consume_mode(consume_mode)
    if output_type == "polars.LazyFrame":
        if normalized_consume_mode == "count":
            return _collect_lazyframe_count(df)
        return len(df.collect())
    if output_type == "datafusion.DataFrame":
        if normalized_consume_mode == "count":
            return int(df.count())
        return _collect_datafusion_len(df)
    return len(df)


def _write_csv(df: Any) -> None:
    if isinstance(df, pl.DataFrame):
        df.write_csv(OUTPUT_CSV)
        return
    if hasattr(df, "to_polars"):
        df.to_polars().write_csv(OUTPUT_CSV)
        return
    df.to_csv(OUTPUT_CSV)


def _write_csv_and_return_count(df: Any) -> int:
    _write_csv(df)
    return len(df)


def nearest_bioframe(df_1, df_2) -> int:
    return len(bf.closest(df_1, df_2, cols1=columns, cols2=columns))


def nearest_polars_bio(
    df_1,
    df_2,
    output_type: str,
    consume_mode: str = "count",
) -> int:
    return _consume_polars_bio_result(
        pb.nearest(
            df_1,
            df_2,
            cols1=columns,
            cols2=columns,
            output_type=output_type,
        ),
        output_type,
        consume_mode=consume_mode,
    )


def nearest_pyranges1(df_1_pr1, df_2_pr1) -> int:
    return len(df_1_pr1.nearest_ranges(df_2_pr1, preserve_input_order=False))


def nearest_pybedtools(df_1_bed, df_2_bed) -> int:
    return len(df_1_bed.closest(df_2_bed, s=False, t="first"))


def nearest_genomicranges(df_1, df_2, n: int = 1) -> int:
    return len(
        df_1.nearest(df_2, ignore_strand=True, select="arbitrary", num_threads=n)
    )


def overlap_bioframe(df_1, df_2) -> int:
    return len(bf.overlap(df_1, df_2, cols1=columns, cols2=columns, how="inner"))


def overlap_polars_bio(
    df_1,
    df_2,
    output_type: str,
    consume_mode: str = "count",
) -> int:
    return _consume_polars_bio_result(
        pb.overlap(
            df_1,
            df_2,
            cols1=columns,
            cols2=columns,
            output_type=output_type,
        ),
        output_type,
        consume_mode=consume_mode,
    )


def overlap_polars_bio_intervaltree(
    df_1,
    df_2,
    output_type: str,
    consume_mode: str = "count",
) -> int:
    return _consume_polars_bio_result(
        pb.overlap(
            df_1,
            df_2,
            cols1=columns,
            cols2=columns,
            algorithm="IntervalTree",
            output_type=output_type,
        ),
        output_type,
        consume_mode=consume_mode,
    )


def overlap_polars_bio_arrayintervaltree(
    df_1,
    df_2,
    output_type: str,
    consume_mode: str = "count",
) -> int:
    return _consume_polars_bio_result(
        pb.overlap(
            df_1,
            df_2,
            cols1=columns,
            cols2=columns,
            algorithm="ArrayIntervalTree",
            output_type=output_type,
        ),
        output_type,
        consume_mode=consume_mode,
    )


def overlap_polars_bio_lapper(
    df_1,
    df_2,
    output_type: str,
    consume_mode: str = "count",
) -> int:
    return _consume_polars_bio_result(
        pb.overlap(
            df_1,
            df_2,
            cols1=columns,
            cols2=columns,
            algorithm="Lapper",
            output_type=output_type,
        ),
        output_type,
        consume_mode=consume_mode,
    )


def overlap_polars_bio_superintervals(
    df_1,
    df_2,
    output_type: str,
    consume_mode: str = "count",
) -> int:
    return _consume_polars_bio_result(
        pb.overlap(
            df_1,
            df_2,
            cols1=columns,
            cols2=columns,
            algorithm="SuperIntervals",
            output_type=output_type,
        ),
        output_type,
        consume_mode=consume_mode,
    )


def overlap_pyranges1_join_overlaps(df_1_pr1, df_2_pr1) -> int:
    return len(
        df_1_pr1.join_overlaps(
            df_2_pr1,
            multiple="all",
            preserve_input_order=False,
        )
    )


def overlap_pyranges1_overlap(df_1_pr1, df_2_pr1) -> int:
    return len(
        df_1_pr1.overlap(
            df_2_pr1,
            multiple=True,
            preserve_input_order=False,
        )
    )


def overlap_pybedtools(df_1_bed, df_2_bed) -> int:
    return len(df_1_bed.intersect(df_2_bed, wa=True, wb=True))


def overlap_pygenomics(df_1_pg, df_2_array) -> int:
    return len(
        list(
            itertools.chain.from_iterable(
                [df_1_pg.find_all((r[0], r[1], r[2])) for r in df_2_array]
            )
        )
    )


def overlap_genomicranges(df_1, df_2, n: int = 1) -> int:
    return len(
        df_1.find_overlaps(df_2, ignore_strand=True, query_type="any", num_threads=n)
    )


def count_overlaps_polars_bio_mz(
    df_1,
    df_2,
    output_type: str,
    consume_mode: str = "count",
) -> int:
    return _consume_polars_bio_result(
        pb.count_overlaps(
            df_1,
            df_2,
            cols1=columns,
            cols2=columns,
            naive_query=False,
            output_type=output_type,
        ),
        output_type,
        consume_mode=consume_mode,
    )


def count_overlaps_polars_bio(
    df_1,
    df_2,
    output_type: str,
    consume_mode: str = "count",
) -> int:
    return _consume_polars_bio_result(
        pb.count_overlaps(
            df_1,
            df_2,
            cols1=columns,
            cols2=columns,
            naive_query=True,
            output_type=output_type,
        ),
        output_type,
        consume_mode=consume_mode,
    )


def count_overlaps_bioframe(df_1, df_2) -> int:
    return len(bf.count_overlaps(df_1, df_2, cols1=columns, cols2=columns))


def count_overlaps_pyranges1(df_1_pr1, df_2_pr1) -> int:
    return len(df_1_pr1.count_overlaps(df_2_pr1))


def count_overlaps_pybedtools(df_1_bed, df_2_bed) -> int:
    return len(df_1_bed.intersect(df_2_bed, wa=True, c=True))


def count_overlaps_genomicranges(df_1, df_2, n: int = 1) -> int:
    return len(
        df_1.count_overlaps(df_2, ignore_strand=True, query_type="any", num_threads=n)
    )


def merge_polars_bio(
    df_1,
    df_2,
    output_type: str,
    consume_mode: str = "count",
) -> int:
    return _consume_polars_bio_result(
        pb.merge(df_1, cols=columns, output_type=output_type),
        output_type,
        consume_mode=consume_mode,
    )


def merge_bioframe(df_1, df_2) -> int:
    return len(bf.merge(df_1, cols=columns, min_dist=None))


def merge_pyranges1(df_1_pr1, df_2_pr1) -> int:
    return len(df_1_pr1.merge_overlaps())


def merge_genomicranges(df_1, df_2, n: int = 1) -> int:
    return len(df_1.reduce(ignore_strand=True))


def cluster_polars_bio(
    df_1,
    df_2,
    output_type: str,
    consume_mode: str = "count",
) -> int:
    return _consume_polars_bio_result(
        pb.cluster(df_1, cols=columns, output_type=output_type),
        output_type,
        consume_mode=consume_mode,
    )


def cluster_bioframe(df_1, df_2) -> int:
    return len(bf.cluster(df_1, cols=columns, min_dist=None))


def cluster_pyranges1(df_1_pr1, df_2_pr1) -> int:
    return len(df_1_pr1.cluster_overlaps())


def complement_polars_bio(
    df_1,
    df_2,
    output_type: str,
    consume_mode: str = "count",
) -> int:
    return _consume_polars_bio_result(
        pb.complement(df_1, cols=columns, output_type=output_type),
        output_type,
        consume_mode=consume_mode,
    )


def complement_bioframe(df_1, df_2) -> int:
    return len(bf.complement(df_1, cols=columns))


def complement_pyranges1(df_1_pr1, df_2_pr1) -> int:
    return len(df_1_pr1.complement_ranges())


def complement_genomicranges(df_1, df_2, n: int = 1) -> int:
    return len(df_1.gaps(ignore_strand=True))


def subtract_polars_bio(
    df_1,
    df_2,
    output_type: str,
    consume_mode: str = "count",
) -> int:
    return _consume_polars_bio_result(
        pb.subtract(
            df_1,
            df_2,
            cols1=columns,
            cols2=columns,
            output_type=output_type,
        ),
        output_type,
        consume_mode=consume_mode,
    )


def subtract_bioframe(df_1, df_2) -> int:
    return len(bf.subtract(df_1, df_2, cols1=columns, cols2=columns))


def subtract_pyranges1(df_1_pr1, df_2_pr1) -> int:
    return len(df_1_pr1.subtract_overlaps(df_2_pr1))


def subtract_genomicranges(df_1, df_2, n: int = 1) -> int:
    return len(df_1.subtract(df_2, ignore_strand=True))


def coverage_polars_bio(
    df_1,
    df_2,
    output_type: str,
    consume_mode: str = "count",
) -> int:
    return _consume_polars_bio_result(
        pb.coverage(
            df_1,
            df_2,
            cols1=columns,
            cols2=columns,
            output_type=output_type,
        ),
        output_type,
        consume_mode=consume_mode,
    )


def coverage_bioframe(df_1, df_2) -> int:
    return len(bf.coverage(df_1, df_2, cols1=columns, cols2=columns))


def coverage_pyranges1(df_1_pr1, df_2_pr1) -> int:
    return len(df_1_pr1.count_overlaps(df_2_pr1, calculate_coverage=True))


def coverage_genomicranges(df_1, df_2, n: int = 1) -> int:
    return len(df_2.coverage())


def coverage_pybedtools(df_1_bed, df_2_bed) -> int:
    return len(df_1_bed.coverage(df_2_bed, counts=True))


def read_vcf_polars_bio(df_path_1, th: int = 1, consume_mode: str = "count") -> int:
    return _consume_polars_bio_result(
        pb.read_vcf(df_path_1, thread_num=th),
        output_type="polars.LazyFrame",
        consume_mode=consume_mode,
    )


polars_bio_profile_fp = open("memory_profiler_polars_bio.log", "w+")


@profile(stream=polars_bio_profile_fp)
def e2e_overlap_polars_bio(df_path_1, df_path_2, output_type=None) -> int:
    df = pb.overlap(df_path_1, df_path_2, cols1=columns, cols2=columns).collect()
    return _write_csv_and_return_count(df)


@profile(stream=polars_bio_profile_fp)
def e2e_nearest_polars_bio(df_path_1, df_path_2, output_type=None) -> int:
    df = pb.nearest(df_path_1, df_path_2, cols1=columns, cols2=columns).collect()
    return _write_csv_and_return_count(df)


@profile(stream=polars_bio_profile_fp)
def e2e_coverage_polars_bio(df_path_1, df_path_2, output_type=None) -> int:
    df = pb.coverage(df_path_1, df_path_2, cols1=columns, cols2=columns).collect()
    return _write_csv_and_return_count(df)


@profile(stream=polars_bio_profile_fp)
def e2e_count_overlaps_polars_bio(df_path_1, df_path_2, output_type=None) -> int:
    df = pb.count_overlaps(df_path_1, df_path_2, cols1=columns, cols2=columns).collect()
    return _write_csv_and_return_count(df)


polars_bio_streaming_profile_fp = open("memory_profiler_polars_bio.log", "w+")


@profile(stream=polars_bio_streaming_profile_fp)
def e2e_overlap_polars_bio_streaming(
    df_path_1, df_path_2, output_type=None, low_memory: bool = False
) -> None:
    if low_memory:
        pb.overlap(
            df_path_1, df_path_2, cols1=columns, cols2=columns, low_memory=True
        ).sink_csv(OUTPUT_CSV)
        return
    pb.overlap(
        df_path_1, df_path_2, cols1=columns, cols2=columns, streaming=True
    ).sink_csv(OUTPUT_CSV)


@profile(stream=polars_bio_streaming_profile_fp)
def e2e_nearest_polars_bio_streaming(df_path_1, df_path_2, output_type=None) -> None:
    pb.nearest(df_path_1, df_path_2, cols1=columns, cols2=columns).sink_csv(OUTPUT_CSV)


@profile(stream=polars_bio_streaming_profile_fp)
def e2e_coverage_polars_bio_streaming(df_path_1, df_path_2, output_type=None) -> None:
    pb.coverage(df_path_1, df_path_2, cols1=columns, cols2=columns).sink_csv(OUTPUT_CSV)


@profile(stream=polars_bio_streaming_profile_fp)
def e2e_count_overlaps_polars_bio_streaming(
    df_path_1, df_path_2, output_type=None
) -> None:
    pb.count_overlaps(df_path_1, df_path_2, cols1=columns, cols2=columns).sink_csv(
        OUTPUT_CSV
    )


bioframe_profile_fp = open("memory_profiler_bioframe.log", "w+")


@profile(stream=bioframe_profile_fp)
def e2e_overlap_bioframe(df_path_1, df_path_2) -> int:
    df_1 = _read_pandas_parquet(df_path_1)
    df_2 = _read_pandas_parquet(df_path_2)
    df = bf.overlap(df_1, df_2, cols1=columns, cols2=columns, how="inner")
    return _write_csv_and_return_count(df)


@profile(stream=bioframe_profile_fp)
def e2e_nearest_bioframe(df_path_1, df_path_2) -> int:
    df_1 = _read_pandas_parquet(df_path_1)
    df_2 = _read_pandas_parquet(df_path_2)
    df = bf.closest(df_1, df_2, cols1=columns, cols2=columns)
    return _write_csv_and_return_count(df)


@profile(stream=bioframe_profile_fp)
def e2e_coverage_bioframe(df_path_1, df_path_2) -> int:
    df_1 = _read_pandas_parquet(df_path_1)
    df_2 = _read_pandas_parquet(df_path_2)
    df = bf.coverage(df_1, df_2, cols1=columns, cols2=columns)
    return _write_csv_and_return_count(df)


@profile(stream=bioframe_profile_fp)
def e2e_count_overlaps_bioframe(df_path_1, df_path_2) -> int:
    df_1 = _read_pandas_parquet(df_path_1)
    df_2 = _read_pandas_parquet(df_path_2)
    df = bf.count_overlaps(df_1, df_2, cols1=columns, cols2=columns)
    return _write_csv_and_return_count(df)


pyranges1_profile_fp = open("memory_profiler_pyranges1.log", "w+")


@profile(stream=pyranges1_profile_fp)
def e2e_overlap_pyranges1(df_path_1, df_path_2) -> int:
    df_1 = _read_pandas_parquet(df_path_1)
    df_2 = _read_pandas_parquet(df_path_2)
    df_1_pr1 = df2pr1(df_1)
    df_2_pr1 = df2pr1(df_2)
    df = df_1_pr1.join_overlaps(
        df_2_pr1,
        multiple="all",
        preserve_input_order=False,
    )
    return _write_csv_and_return_count(df)


@profile(stream=pyranges1_profile_fp)
def e2e_nearest_pyranges1(df_path_1, df_path_2) -> int:
    df_1 = _read_pandas_parquet(df_path_1)
    df_2 = _read_pandas_parquet(df_path_2)
    df_1_pr1 = df2pr1(df_1)
    df_2_pr1 = df2pr1(df_2)
    df = df_1_pr1.nearest_ranges(df_2_pr1, preserve_input_order=False)
    return _write_csv_and_return_count(df)


@profile(stream=pyranges1_profile_fp)
def e2e_coverage_pyranges1(df_path_1, df_path_2) -> int:
    df_1 = _read_pandas_parquet(df_path_1)
    df_2 = _read_pandas_parquet(df_path_2)
    df_1_pr1 = df2pr1(df_1)
    df_2_pr1 = df2pr1(df_2)
    df = df_1_pr1.count_overlaps(df_2_pr1, calculate_coverage=True)
    return _write_csv_and_return_count(df)


@profile(stream=pyranges1_profile_fp)
def e2e_count_overlaps_pyranges1(df_path_1, df_path_2) -> int:
    df_1 = _read_pandas_parquet(df_path_1)
    df_2 = _read_pandas_parquet(df_path_2)
    df_1_pr1 = df2pr1(df_1)
    df_2_pr1 = df2pr1(df_2)
    df = df_1_pr1.count_overlaps(df_2_pr1)
    return _write_csv_and_return_count(df)


genomicranges_profile_fp = open("memory_profiler_genomicranges.log", "w+")


def _to_genomicranges(df: pl.DataFrame | None):
    if df is None:
        return None
    return GenomicRanges.from_polars(
        df.rename(
            {
                "contig": "seqnames",
                "pos_start": "starts",
                "pos_end": "ends",
            }
        )
    )


@profile(stream=genomicranges_profile_fp)
def e2e_overlap_genomicranges(df_path_1, df_path_2, n: int = 1) -> int:
    df_1 = pl.read_parquet(df_path_1)
    df_2 = pl.read_parquet(df_path_2) if df_path_2 else None
    df_1_gr = _to_genomicranges(df_1)
    df_2_gr = _to_genomicranges(df_2)
    hits = df_1_gr.find_overlaps(
        df_2_gr, ignore_strand=True, query_type="any", num_threads=n
    )
    df = overlaps_to_df(df_1_gr, df_2_gr, hits, backend="polars")
    return _write_csv_and_return_count(df)


@profile(stream=genomicranges_profile_fp)
def e2e_nearest_genomicranges(df_path_1, df_path_2, n: int = 1) -> int:
    df_1 = pl.read_parquet(df_path_1)
    df_2 = pl.read_parquet(df_path_2) if df_path_2 else None
    df_1_gr = _to_genomicranges(df_1)
    df_2_gr = _to_genomicranges(df_2)
    df = df_1_gr.nearest(
        df_2_gr,
        ignore_strand=True,
        select="arbitrary",
        num_threads=n,
    )
    return _write_csv_and_return_count(df)


@profile(stream=genomicranges_profile_fp)
def e2e_count_overlaps_genomicranges(df_path_1, df_path_2, n: int = 1) -> int:
    df_1 = pl.read_parquet(df_path_1)
    df_2 = pl.read_parquet(df_path_2) if df_path_2 else None
    df_1_gr = _to_genomicranges(df_1)
    df_2_gr = _to_genomicranges(df_2)
    df = df_1_gr.count_overlaps(
        df_2_gr, ignore_strand=True, query_type="any", num_threads=n
    )
    return _write_csv_and_return_count(df)
