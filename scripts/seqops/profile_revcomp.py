"""Split polars-bio's reverse-complement pipeline into stages and time each.

usage: python profile_revcomp.py STAGE INPUT OUTPUT   (prints one JSON line)

Stages, each adding one step to the previous ones:
  read        scan_fastq, stream every batch (all columns) and discard it
  compute     + .seq.revcomp() and .seq.reverse() on quality, discard batches
  sink_plain  scan_fastq -> pb.sink_fastq, no transformation (read + write)
  sink_full   scan_fastq -> revcomp -> pb.sink_fastq (the benchmarked pipeline)
  polars_csv  same transformation, but written by Polars' own streaming CSV
              sink as one pre-formatted FASTQ record per row

Everything runs on one thread. Timing starts after imports.
"""

import json
import os
import resource
import sys
import time

os.environ["POLARS_MAX_THREADS"] = "1"
import polars as pl  # noqa: E402

import polars_bio as pb  # noqa: E402

pb.set_option("datafusion.execution.target_partitions", "1")
pb.set_progress_bar(False)

stage, inp, out = sys.argv[1:4]


def transformed():
    return pb.scan_fastq(inp).with_columns(
        sequence=pl.col("sequence").seq.revcomp(),
        quality_scores=pl.col("quality_scores").seq.reverse(),
    )


def drain(lf):
    n = 0
    for batch in lf.collect_batches(engine="streaming"):
        n += batch.height
    return n


t0 = time.perf_counter()
r0 = resource.getrusage(resource.RUSAGE_SELF)
if stage == "read":
    rows = drain(pb.scan_fastq(inp))
elif stage == "compute":
    rows = drain(transformed())
elif stage == "sink_plain":
    rows = pb.sink_fastq(pb.scan_fastq(inp), out)
elif stage == "sink_full":
    rows = pb.sink_fastq(transformed(), out)
elif stage == "polars_csv":
    lf = transformed().select(
        pl.concat_str(
            [
                pl.lit("@"),
                pl.col("name"),
                pl.when(pl.col("description").is_not_null() & (pl.col("description") != ""))
                .then(pl.lit(" ") + pl.col("description"))
                .otherwise(pl.lit("")),
                pl.lit("\n"),
                pl.col("sequence"),
                pl.lit("\n+\n"),
                pl.col("quality_scores"),
            ]
        ).alias("record")
    )
    lf.sink_csv(out, include_header=False, quote_style="never")
    rows = None
else:
    raise SystemExit(f"unknown stage {stage}")
r1 = resource.getrusage(resource.RUSAGE_SELF)
wall = time.perf_counter() - t0
cpu = (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime)
print(json.dumps({"stage": stage, "wall_s": wall, "cpu_s": cpu, "rows": rows,
                  "rss_mb": r1.ru_maxrss / 2**20 if sys.platform == "darwin" else r1.ru_maxrss / 1024}))
