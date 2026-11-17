"""How each tool performs each operation, as a command line.

``command(tool, op, inp, out, threads)`` returns ``(argv, stdout_path)``: the
command to run and, for tools that only write to stdout, the file to send
stdout to. Single-threaded tools ignore ``threads``.

Each command produces the same output the correctness check expects for that
operation (see ``pyrun.py`` for the formats).
"""

from __future__ import annotations

import sys
from pathlib import Path

PYRUN = str(Path(__file__).with_name("pyrun.py"))

# Tools that take a thread count. The others run once per dataset and appear
# in every thread row of the results table.
MULTI_THREADED = {"polars_bio", "seqkit"}


def command(tool: str, op: str, inp: str, out: str, threads: int):
    t = str(threads)
    if tool in ("polars_bio", "biopython"):
        return [sys.executable, PYRUN, tool, op, inp, out, t], None
    if tool == "seqkit":
        return {
            # -t dna: skip alphabet guessing; -r reverses quality too.
            "revcomp": (["seqkit", "seq", "-t", "dna", "-r", "-p", "-j", t, inp, "-o", out], None),
            # -i: ID only, -g: GC over A+C+G+T, -q: error-probability mean.
            "gc_qual": (["seqkit", "fx2tab", "-n", "-i", "-g", "-q", "-j", t, inp, "-o", out], None),
            "translate": (["seqkit", "translate", "-w", "0", "-j", t, inp, "-o", out], None),
        }[op]
    if tool == "seqtk":
        return {
            "revcomp": (["seqtk", "seq", "-r", inp], out),
            # Per-read base counts; GC is derived by the check (comp_to_gc).
            "gc_qual": (["seqtk", "comp", inp], out),
        }[op]
    if tool == "seqfu":
        return {"revcomp": (["seqfu", "rc", inp], out)}[op]
    raise KeyError(f"{tool} has no {op}")


def supports(tool: str, op: str) -> bool:
    try:
        command(tool, op, "in", "out", 1)
        return True
    except KeyError:
        return False


def output_suffix(op: str) -> str:
    return {"revcomp": ".fastq", "gc_qual": ".tsv", "translate": ".fasta"}[op]
