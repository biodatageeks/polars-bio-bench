import itertools

import bioframe as bf
import polars_bio as pb

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


def nearest_pyranges0(df_1_pr0, df_2_pr0, n=1):
    len(df_1_pr0.nearest(df_2_pr0, nb_cpu=n))


def nearest_pyranges1(df_1_pr1, df_2_pr1):
    len(df_1_pr1.nearest(df_2_pr1))


def nearest_pybedtools(df_1_bed, df_2_bed):
    len(df_1_bed.closest(df_2_bed, s=False, t="first"))


def nearest_genomicranges(df_1, df_2):
    len(df_1.nearest(df_2, ignore_strand=True, select="arbitrary"))


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


def overlap_pyranges0(df_1_pr0, df_2_pr0, n=1):
    len(df_1_pr0.join(df_2_pr0, nb_cpu=n))


def overlap_pyranges1(df_1_pr1, df_2_pr1):
    len(df_1_pr1.join_ranges(df_2_pr1))


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


def overlap_genomicranges(df_1, df_2):
    len(df_1.find_overlaps(df_2, ignore_strand=True, query_type="any"))


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


def count_overlaps_pyranges0(df_1_pr0, df_2_pr0, n=1):
    print(len(df_1_pr0.count_overlaps(df_2_pr0)))


def count_overlaps_pyranges1(df_1_pr1, df_2_pr1):
    print(len(df_1_pr1.count_overlaps(df_2_pr1)))


def count_overlaps_pybedtools(df_1_bed, df_2_bed):
    print(len(df_1_bed.intersect(df_2_bed, wa=True, c=True)))


def count_overlaps_genomicranges(df_1, df_2):
    print(len(df_2.count_overlaps(df_1, ignore_strand=True, query_type="any")))


def merge_polars_bio(df_path_1, df_path_2, output_type):
    if output_type == "polars.LazyFrame":
        len(pb.merge(df_path_1, cols=columns, output_type=output_type).collect())
    else:
        len(pb.merge(df_path_1, cols=columns, output_type=output_type))


def merge_bioframe(df_1, df_2):
    len(bf.merge(df_1, cols=columns, min_dist=None))


def merge_pyranges0(df_1_pr0, df_2_pr0, n=1):
    len(df_1_pr0.merge())


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


def coverage_pyranges0(df_1_pr0, df_2_pr0, n=1):
    len(df_1_pr0.coverage(df_2_pr0))


def coverage_pyranges1(df_1_pr1, df_2_pr1):
    len(df_1_pr1.count_overlaps(df_2_pr1, calculate_coverage=True))


def coverage_pybedtools(df_1_bed, df_2_bed):
    len(df_1_bed.coverage(df_2_bed, counts=True))


def coverage_genomicranges(df_1, df_2):
    len(df_1.subset_by_overlaps(df_2))


## Input file formats benchmarking
def read_vcf_polars_bio(df_path_1, th=1):
    len(pb.read_vcf(df_path_1, thread_num=th).collect())
