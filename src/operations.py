import itertools

import bioframe as bf
import pandas as pd
import polars as pl
import polars_bio as pb
from genomicranges import GenomicRanges
from memory_profiler import profile

from utils import df2pr1, overlaps_to_df

columns = ("contig", "pos_start", "pos_end")


def nearest_bioframe(df_1, df_2):
    len(bf.closest(df_1, df_2, cols1=columns, cols2=columns))


def nearest_polars_bio(df_path_1, df_path_2, output_type):
    if output_type == "polars.LazyFrame":
        len(
            pb.nearest(
                df_path_1,
                df_path_2,
                cols1=columns,
                cols2=columns,
                output_type=output_type,
            ).collect()
        )
    else:
        len(
            pb.nearest(
                df_path_1,
                df_path_2,
                cols1=columns,
                cols2=columns,
                output_type=output_type,
            )
        )


def nearest_pyranges1(df_1_pr1, df_2_pr1):
    len(df_1_pr1.nearest_ranges(df_2_pr1))


def nearest_pybedtools(df_1_bed, df_2_bed):
    len(df_1_bed.closest(df_2_bed, s=False, t="first"))


def nearest_genomicranges(df_1, df_2, n: int = 1):
    len(df_1.nearest(df_2, ignore_strand=True, select="arbitrary", num_threads=n))


def overlap_bioframe(df_1, df_2):
    len(bf.overlap(df_1, df_2, cols1=columns, cols2=columns, how="inner"))


def overlap_polars_bio(df_path_1, df_path_2, output_type):
    if output_type == "polars.LazyFrame":
        len(pb.overlap(df_path_1, df_path_2, cols1=columns, cols2=columns).collect())
    elif output_type == "datafusion.DataFrame":
        pb.overlap(
            df_path_1,
            df_path_2,
            cols1=columns,
            cols2=columns,
            output_type=output_type,
        ).count()
    else:
        len(
            pb.overlap(
                df_path_1,
                df_path_2,
                cols1=columns,
                cols2=columns,
                output_type=output_type,
            )
        )


# Coitrees, IntervalTree, ArrayIntervalTree, Lapper, SuperIntervals
def overlap_polars_bio_intervaltree(df_path_1, df_path_2, output_type):
    len(
        pb.overlap(
            df_path_1, df_path_2, cols1=columns, cols2=columns, algorithm="IntervalTree"
        ).collect()
    )


def overlap_polars_bio_arrayintervaltree(df_path_1, df_path_2, output_type):
    len(
        pb.overlap(
            df_path_1,
            df_path_2,
            cols1=columns,
            cols2=columns,
            algorithm="ArrayIntervalTree",
        ).collect()
    )


def overlap_polars_bio_lapper(df_path_1, df_path_2, output_type):
    len(
        pb.overlap(
            df_path_1, df_path_2, cols1=columns, cols2=columns, algorithm="Lapper"
        ).collect()
    )


def overlap_polars_bio_superintervals(df_path_1, df_path_2, output_type):
    len(
        pb.overlap(
            df_path_1,
            df_path_2,
            cols1=columns,
            cols2=columns,
            algorithm="SuperIntervals",
        ).collect()
    )


def overlap_pyranges1(df_1_pr1, df_2_pr1):
    len(df_1_pr1.join_overlaps(df_2_pr1))


def overlap_pybedtools(df_1_bed, df_2_bed):
    len(df_1_bed.intersect(df_2_bed, wa=True, wb=True))


def overlap_pygenomics(df_1_pg, df_2_array):
    len(
        list(
            itertools.chain.from_iterable(
                [df_1_pg.find_all((r[0], r[1], r[2])) for r in df_2_array]
            )
        )
    )


def overlap_genomicranges(df_1, df_2, n: int = 1):
    len(df_1.find_overlaps(df_2, ignore_strand=True, query_type="any", num_threads=n))


def count_overlaps_polars_bio_mz(df_path_1, df_path_2, output_type):
    if output_type == "polars.LazyFrame":
        print(
            len(
                pb.count_overlaps(
                    df_path_1,
                    df_path_2,
                    cols1=columns,
                    cols2=columns,
                    naive_query=False,
                ).collect()
            )
        )
    else:
        len(
            pb.count_overlaps(
                df_path_1,
                df_path_2,
                cols1=columns,
                cols2=columns,
                output_type=output_type,
            )
        )


def count_overlaps_polars_bio(df_path_1, df_path_2, output_type):
    if output_type == "polars.LazyFrame":
        print(
            len(
                pb.count_overlaps(
                    df_path_1, df_path_2, cols1=columns, cols2=columns, naive_query=True
                ).collect()
            )
        )
    else:
        len(
            pb.count_overlaps(
                df_path_1,
                df_path_2,
                cols1=columns,
                cols2=columns,
                output_type=output_type,
            )
        )


def count_overlaps_bioframe(df_1, df_2):
    print(len(bf.count_overlaps(df_1, df_2, cols1=columns, cols2=columns)))


def count_overlaps_pyranges1(df_1_pr1, df_2_pr1):
    print(len(df_1_pr1.count_overlaps(df_2_pr1)))


def count_overlaps_pybedtools(df_1_bed, df_2_bed):
    print(len(df_1_bed.intersect(df_2_bed, wa=True, c=True)))


def count_overlaps_genomicranges(df_1, df_2, n: int = 1):
    print(
        len(
            df_1.count_overlaps(
                df_2, ignore_strand=True, query_type="any", num_threads=n
            )
        )
    )


def merge_polars_bio(df_path_1, df_path_2, output_type):
    if output_type == "polars.LazyFrame":
        len(pb.merge(df_path_1, cols=columns, output_type=output_type).collect())
    else:
        len(pb.merge(df_path_1, cols=columns, output_type=output_type))


def merge_bioframe(df_1, df_2):
    len(bf.merge(df_1, cols=columns, min_dist=None))


def merge_pyranges1(df_1_pr1, df_2_pr1):
    len(df_1_pr1.merge_overlaps())


def coverage_polars_bio(df_path_1, df_path_2, output_type):
    if output_type == "polars.LazyFrame":
        len(pb.coverage(df_path_1, df_path_2, cols1=columns, cols2=columns).collect())
    else:
        len(
            pb.coverage(
                df_path_1,
                df_path_2,
                cols1=columns,
                cols2=columns,
                output_type=output_type,
            )
        )


def coverage_bioframe(df_1, df_2):
    len(bf.coverage(df_1, df_2, cols1=columns, cols2=columns))


def coverage_pyranges1(df_1_pr1, df_2_pr1):
    len(df_1_pr1.count_overlaps(df_2_pr1, calculate_coverage=True))


def coverage_pybedtools(df_1_bed, df_2_bed):
    len(df_1_bed.coverage(df_2_bed, counts=True))


## Input file formats benchmarking
def read_vcf_polars_bio(df_path_1, th=1):
    len(pb.read_vcf(df_path_1, thread_num=th).collect())


## E2E overlap and export to csv
OUTPUT_CSV = "/tmp/output.csv"

fp = open("memory_profiler_polars_bio.log", "w+")


@profile(stream=fp)
def e2e_overlap_polars_bio(df_path_1, df_path_2, output_type=None):
    df = pb.overlap(df_path_1, df_path_2, cols1=columns, cols2=columns).collect()
    df.write_csv(OUTPUT_CSV)


@profile(stream=fp)
def e2e_nearest_polars_bio(df_path_1, df_path_2, output_type=None):
    df = pb.nearest(df_path_1, df_path_2, cols1=columns, cols2=columns).collect()
    df.write_csv(OUTPUT_CSV)


@profile(stream=fp)
def e2e_coverage_polars_bio(df_path_1, df_path_2, output_type=None):
    df = pb.coverage(df_path_1, df_path_2, cols1=columns, cols2=columns).collect()
    df.write_csv(OUTPUT_CSV)


@profile(stream=fp)
def e2e_count_overlaps_polars_bio(df_path_1, df_path_2, output_type=None):
    df = pb.count_overlaps(df_path_1, df_path_2, cols1=columns, cols2=columns).collect()
    df.write_csv(OUTPUT_CSV)


fp = open("memory_profiler_polars_bio.log", "w+")


@profile(stream=fp)
def e2e_overlap_polars_bio_streaming(
    df_path_1, df_path_2, output_type=None, low_memory=False
):
    if low_memory:
        pb.overlap(
            df_path_1, df_path_2, cols1=columns, cols2=columns, low_memory=True
        ).sink_csv(OUTPUT_CSV)
    else:
        pb.overlap(
            df_path_1, df_path_2, cols1=columns, cols2=columns, streaming=True
        ).sink_csv(OUTPUT_CSV)


@profile(stream=fp)
def e2e_nearest_polars_bio_streaming(df_path_1, df_path_2, output_type=None):
    pb.nearest(df_path_1, df_path_2, cols1=columns, cols2=columns).sink_csv(OUTPUT_CSV)


@profile(stream=fp)
def e2e_coverage_polars_bio_streaming(df_path_1, df_path_2, output_type=None):
    pb.coverage(df_path_1, df_path_2, cols1=columns, cols2=columns).sink_csv(OUTPUT_CSV)


@profile(stream=fp)
def e2e_count_overlaps_polars_bio_streaming(df_path_1, df_path_2, output_type=None):
    pb.count_overlaps(df_path_1, df_path_2, cols1=columns, cols2=columns).sink_csv(
        OUTPUT_CSV
    )


fp = open("memory_profiler_bioframe.log", "w+")


@profile(stream=fp)
def e2e_overlap_bioframe(df_path_1, df_path_2):
    df_1 = pd.read_parquet(df_path_1.replace("*.parquet", ""))
    df_2 = pd.read_parquet(df_path_2.replace("*.parquet", ""))
    df = bf.overlap(df_1, df_2, cols1=columns, cols2=columns, how="inner")
    df.to_csv("output.csv")


@profile(stream=fp)
def e2e_nearest_bioframe(df_path_1, df_path_2):
    df_1 = pd.read_parquet(df_path_1.replace("*.parquet", ""))
    df_2 = pd.read_parquet(df_path_2.replace("*.parquet", ""))
    df = bf.closest(df_1, df_2, cols1=columns, cols2=columns)
    df.to_csv("output.csv")


@profile(stream=fp)
def e2e_coverage_bioframe(df_path_1, df_path_2):
    df_1 = pd.read_parquet(df_path_1.replace("*.parquet", ""))
    df_2 = pd.read_parquet(df_path_2.replace("*.parquet", ""))
    df = bf.coverage(df_1, df_2, cols1=columns, cols2=columns)
    df.to_csv("output.csv")


@profile(stream=fp)
def e2e_count_overlaps_bioframe(df_path_1, df_path_2):
    df_1 = pd.read_parquet(df_path_1.replace("*.parquet", ""))
    df_2 = pd.read_parquet(df_path_2.replace("*.parquet", ""))
    df = bf.count_overlaps(df_1, df_2, cols1=columns, cols2=columns)
    df.to_csv("output.csv")


fp = open("memory_profiler_pyranges1.log", "w+")


@profile(stream=fp)
def e2e_overlap_pyranges1(df_path_1, df_path_2):
    df_1 = pd.read_parquet(df_path_1.replace("*.parquet", ""))
    df_2 = pd.read_parquet(df_path_2.replace("*.parquet", ""))
    df_1_pr1 = df2pr1(df_1)
    df_2_pr1 = df2pr1(df_2)
    df = df_1_pr1.join_overlaps(df_2_pr1)
    df.to_csv("output.csv")


@profile(stream=fp)
def e2e_nearest_pyranges1(df_path_1, df_path_2):
    df_1 = pd.read_parquet(df_path_1.replace("*.parquet", ""))
    df_2 = pd.read_parquet(df_path_2.replace("*.parquet", ""))
    df_1_pr1 = df2pr1(df_1)
    df_2_pr1 = df2pr1(df_2)
    df = df_1_pr1.nearest_ranges(df_2_pr1)
    df.to_csv("output.csv")


@profile(stream=fp)
def e2e_coverage_pyranges1(df_path_1, df_path_2):
    df_1 = pd.read_parquet(df_path_1.replace("*.parquet", ""))
    df_2 = pd.read_parquet(df_path_2.replace("*.parquet", ""))
    df_1_pr1 = df2pr1(df_1)
    df_2_pr1 = df2pr1(df_2)
    df = df_1_pr1.count_overlaps(df_2_pr1, calculate_coverage=True)
    df.to_csv("output.csv")


@profile(stream=fp)
def e2e_count_overlaps_pyranges1(df_path_1, df_path_2):
    df_1 = pd.read_parquet(df_path_1.replace("*.parquet", ""))
    df_2 = pd.read_parquet(df_path_2.replace("*.parquet", ""))
    df_1_pr1 = df2pr1(df_1)
    df_2_pr1 = df2pr1(df_2)
    df = df_1_pr1.count_overlaps(df_2_pr1)
    df.to_csv("output.csv")


# GenomicRanges E2E tests
fp = open("memory_profiler_genomicranges.log", "w+")


@profile(stream=fp)
def e2e_overlap_genomicranges(df_path_1, df_path_2, n: int = 1):
    df_1 = pl.read_parquet(df_path_1)
    df_2 = pl.read_parquet(df_path_2) if df_path_2 else None
    df_1_gr = GenomicRanges.from_polars(
        df_1.rename(
            {
                "contig": "seqnames",
                "pos_start": "starts",
                "pos_end": "ends",
            }
        )
    )
    df_2_gr = (
        GenomicRanges.from_polars(
            df_2.rename(
                {
                    "contig": "seqnames",
                    "pos_start": "starts",
                    "pos_end": "ends",
                }
            )
        )
        if df_2 is not None
        else None
    )
    hits = df_1_gr.find_overlaps(
        df_2_gr, ignore_strand=True, query_type="any", num_threads=n
    )
    df = overlaps_to_df(df_1_gr, df_2_gr, hits, backend="polars")
    df.write_csv(OUTPUT_CSV)
    # hits.to_polars().write_csv(OUTPUT_CSV)


@profile(stream=fp)
def e2e_nearest_genomicranges(df_path_1, df_path_2, n: int = 1):
    df_1 = pl.read_parquet(df_path_1)
    df_2 = pl.read_parquet(df_path_2) if df_path_2 else None
    df_1_gr = GenomicRanges.from_polars(
        df_1.rename(
            {
                "contig": "seqnames",
                "pos_start": "starts",
                "pos_end": "ends",
            }
        )
    )
    df_2_gr = (
        GenomicRanges.from_polars(
            df_2.rename(
                {
                    "contig": "seqnames",
                    "pos_start": "starts",
                    "pos_end": "ends",
                }
            )
        )
        if df_2 is not None
        else None
    )
    df = df_1_gr.nearest(df_2_gr, ignore_strand=True, select="arbitrary", num_threads=n)
    df.to_polars().write_csv(OUTPUT_CSV)


@profile(stream=fp)
def e2e_count_overlaps_genomicranges(df_path_1, df_path_2, n: int = 1):
    df_1 = pl.read_parquet(df_path_1)
    df_2 = pl.read_parquet(df_path_2) if df_path_2 else None
    df_1_gr = GenomicRanges.from_polars(
        df_1.rename(
            {
                "contig": "seqnames",
                "pos_start": "starts",
                "pos_end": "ends",
            }
        )
    )
    df_2_gr = (
        GenomicRanges.from_polars(
            df_2.rename(
                {
                    "contig": "seqnames",
                    "pos_start": "starts",
                    "pos_end": "ends",
                }
            )
        )
        if df_2 is not None
        else None
    )
    df = df_1_gr.count_overlaps(
        df_2_gr, ignore_strand=True, query_type="any", num_threads=n
    )
    df.to_polars().write_csv(OUTPUT_CSV)
