"""In-Python implementations, run as a fresh subprocess by the harness.

usage: python pyrun.py TOOL OPERATION INPUT OUTPUT THREADS

TOOL is ``polars_bio`` or ``biopython``. Each implementation reads INPUT and
writes OUTPUT in the same format the command-line tools produce, so the
correctness check can compare them:

- revcomp:  FASTQ, sequence reverse-complemented and quality reversed
- gc_qual:  TSV ``name<TAB>gc_pct<TAB>avg_qual``; GC over A+C+G+T (seqkit
            ``fx2tab -g``), mean quality by error probability (seqkit ``-q``)
- translate: FASTA, frame 1, standard table, trailing partial codon dropped

Timing: when SEQOPS_TIMING_FILE is set, the wall and CPU time of the work
itself, measured after every import, are written there as JSON. The harness
reports that as the tool's time, so interpreter start-up and imports
(about half a second for polars-bio) are not counted; the full process time
is recorded separately.

Biopython uses its fast low-level parsers (``FastqGeneralIterator``,
``SimpleFastaParser``) and string-level functions rather than ``SeqRecord``
objects, which is the fastest documented way to use it.
"""

import gzip
import json
import math
import os
import resource
import sys
import time


def _open_text(path):
    with open(path, "rb") as fh:
        gz = fh.read(2) == b"\x1f\x8b"
    return gzip.open(path, "rt") if gz else open(path)


_T0 = None


def start_clock():
    """Mark the end of imports and set-up; the measured work starts here."""
    global _T0
    r = resource.getrusage(resource.RUSAGE_SELF)
    _T0 = (time.perf_counter(), r.ru_utime + r.ru_stime)


def _report():
    path = os.environ.get("SEQOPS_TIMING_FILE")
    if path and _T0:
        r = resource.getrusage(resource.RUSAGE_SELF)
        with open(path, "w") as fh:
            json.dump({"wall_s": time.perf_counter() - _T0[0],
                       "cpu_s": r.ru_utime + r.ru_stime - _T0[1]}, fh)


# --- polars-bio -------------------------------------------------------------


def polars_bio(op, inp, out, threads):
    os.environ["POLARS_MAX_THREADS"] = str(threads)
    import polars as pl

    import polars_bio as pb

    pb.set_option("datafusion.execution.target_partitions", str(threads))
    pb.set_progress_bar(False)
    seq = pl.col("sequence")
    start_clock()
    if op == "revcomp":
        lf = pb.scan_fastq(inp).with_columns(
            sequence=seq.seq.revcomp(),
            quality_scores=pl.col("quality_scores").seq.reverse(),
        )
        pb.sink_fastq(lf, out)
    elif op == "gc_qual":
        lf = pb.scan_fastq(inp).select(
            "name",
            gc_pct=seq.seq.gc_content(denominator="acgt") * 100,
            avg_qual=pl.col("quality_scores").seq.mean_quality(),
        )
        lf.sink_csv(out, separator="\t", include_header=False, float_precision=2)
    elif op == "translate":
        lf = pb.scan_fasta(inp).with_columns(sequence=seq.seq.translate())
        pb.sink_fasta(lf, out)
    else:
        raise SystemExit(f"polars_bio: unknown operation {op}")


# --- Biopython -------------------------------------------------------------


def biopython(op, inp, out, threads):
    from Bio.Seq import reverse_complement, translate
    from Bio.SeqIO.FastaIO import SimpleFastaParser
    from Bio.SeqIO.QualityIO import FastqGeneralIterator

    start_clock()
    with _open_text(inp) as fh, open(out, "w") as w:
        if op == "revcomp":
            for title, s, q in FastqGeneralIterator(fh):
                w.write(f"@{title}\n{reverse_complement(s)}\n+\n{q[::-1]}\n")
        elif op == "gc_qual":
            err = [10 ** (-q / 10) for q in range(94)]
            for title, s, q in FastqGeneralIterator(fh):
                u = s.upper()
                gc = u.count("G") + u.count("C")
                acgt = gc + u.count("A") + u.count("T")
                gc_pct = f"{100 * gc / acgt:.2f}" if acgt else ""
                if q:
                    mean_err = sum(err[ord(c) - 33] for c in q) / len(q)
                    avg = f"{-10 * math.log10(mean_err):.2f}"
                else:
                    avg = ""
                w.write(f"{title.split()[0]}\t{gc_pct}\t{avg}\n")
        elif op == "translate":
            for title, s in SimpleFastaParser(fh):
                s = s[: len(s) // 3 * 3]
                w.write(f">{title}\n{translate(s)}\n")
        else:
            raise SystemExit(f"biopython: unknown operation {op}")


if __name__ == "__main__":
    tool, op, inp, out, threads = sys.argv[1:6]
    {"polars_bio": polars_bio, "biopython": biopython}[tool](op, inp, out, int(threads))
    _report()
