# pyranges0
import pyranges as pr0
import pyranges1 as pr1


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
