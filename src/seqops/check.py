"""Correctness gate: is a tool's output the same as the reference output?

Times are only reported for runs whose output passed. A run that fails is
reported as a mismatch and is never used as a baseline.

- FASTQ/FASTA outputs are compared as an order-independent multiset of
  records. polars-bio may write records in a different order when it reads a
  BGZF file in parallel, so order is not part of the contract. Each record is
  reduced to (ID, sequence[, quality]); headers are compared by their first
  word, because tools format the rest of the header differently.
- TSV outputs (per-read GC and mean quality) are compared numerically after
  sorting, with a tolerance of seqkit's printed precision (two decimals).

Known definitional differences from polars-bio's oracles.md are normalised
before comparing: Biopython's B/Z/J ambiguity letters become X.
"""

from __future__ import annotations

import gzip
import hashlib

_MOD = 1 << 160


def _open(path):
    with open(path, "rb") as fh:
        gz = fh.read(2) == b"\x1f\x8b"
    return gzip.open(path, "rb") if gz else open(path, "rb")


def _records(path, kind):
    """Yield (id, sequence, quality) as bytes; quality is b"" for FASTA."""
    with _open(path) as fh:
        if kind == "fastq":
            while True:
                head = fh.readline()
                if not head:
                    return
                seq = fh.readline().rstrip(b"\r\n")
                fh.readline()
                qual = fh.readline().rstrip(b"\r\n")
                yield head[1:].split(None, 1)[0], seq, qual
        else:  # FASTA, possibly wrapped
            name, chunks = None, []
            for line in fh:
                line = line.rstrip(b"\r\n")
                if line.startswith(b">"):
                    if name is not None:
                        yield name, b"".join(chunks), b""
                    name, chunks = line[1:].split(None, 1)[0], []
                elif line:
                    chunks.append(line)
            if name is not None:
                yield name, b"".join(chunks), b""


_BZJ = bytes.maketrans(b"BZJ", b"XXX")


def fastx_digest(path: str, kind: str, tool: str = "") -> tuple[int, str]:
    """(record count, order-independent digest) of a FASTQ or FASTA file."""
    total, count = 0, 0
    for rid, seq, qual in _records(path, kind):
        seq = seq.upper()
        if tool == "biopython" and kind == "fasta":
            seq = seq.translate(_BZJ)
        h = hashlib.blake2b(rid + b"\0" + seq + b"\0" + qual, digest_size=20)
        total = (total + int.from_bytes(h.digest(), "big")) % _MOD
        count += 1
    return count, f"{total:040x}"


def _gc_table(path: str, tool: str):
    """Load a per-read GC/quality table as a sorted polars DataFrame."""
    import polars as pl

    if tool == "seqtk":
        # seqtk comp: name, length, #A, #C, #G, #T, ... Derive GC over A+C+G+T.
        raw = pl.read_csv(path, separator="\t", has_header=False, infer_schema=False)
        # Select by position: headerless column names differ between Polars
        # versions (column_1... in 1.x, column_0... in 2.x).
        c = raw.columns
        df = raw.select(
            pl.col(c[0]).alias("id"),
            *(pl.col(c[i]).cast(pl.Int64).alias(b) for i, b in zip(range(2, 6), "acgt")),
        )
        acgt = pl.col("a") + pl.col("c") + pl.col("g") + pl.col("t")
        df = df.select(
            "id",
            gc=pl.when(acgt > 0).then(100 * (pl.col("c") + pl.col("g")) / acgt),
            qual=pl.lit(None, pl.Float64),
        )
    else:
        df = pl.read_csv(
            path, separator="\t", has_header=False, new_columns=["id", "gc", "qual"],
            schema_overrides={"id": pl.String, "gc": pl.Float64, "qual": pl.Float64},
            null_values=["", "NaN"],
        )
    return df.sort("id", "gc", "qual", nulls_last=True)


def compare_gc_qual(ref_path: str, path: str, tool: str, tol: float = 0.0051):
    """(ok, detail). seqtk has no quality column, so only GC is compared."""
    import polars as pl

    ref, got = _gc_table(ref_path, "seqkit"), _gc_table(path, tool)
    if ref.height != got.height:
        return False, f"{got.height} rows, reference has {ref.height}"
    if not ref["id"].equals(got["id"]):
        return False, "read IDs differ"
    cols = ["gc"] if tool == "seqtk" else ["gc", "qual"]
    for c in cols:
        diff = (ref[c] - got[c]).abs()
        both_null = ref[c].is_null() & got[c].is_null()
        bad = ~both_null & (diff.is_null() | (diff > tol))
        n_bad = int(bad.sum())
        if n_bad:
            i = int(bad.arg_max())
            return False, f"{n_bad} rows differ in {c}, e.g. {ref['id'][i]}: {ref[c][i]} vs {got[c][i]}"
    return True, "ok"
