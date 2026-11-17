"""What produced a set of results: machine, tool versions, inputs."""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from importlib import metadata


def _out(argv):
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=30)
        return (p.stdout + p.stderr).strip()
    except (OSError, subprocess.TimeoutExpired):
        return None


def _first_line_matching(text, word):
    for line in (text or "").splitlines():
        if word.lower() in line.lower():
            return line.strip()
    return None


def tool_versions() -> dict:
    v = {
        "seqkit": _out(["seqkit", "version"]),
        "seqfu": _out(["seqfu", "version"]),
        "seqtk": _first_line_matching(_out(["seqtk"]), "version"),
        "samtools": (_out(["samtools", "--version"]) or "").split("\n")[0] or None,
        "bedtools": _out(["bedtools", "--version"]),
        "bgzip": (_out(["bgzip", "--version"]) or "").split("\n")[0] or None,
        "python": sys.version.split()[0],
    }
    for pkg in ("polars-bio", "polars", "biopython", "pyfaidx", "pyfastx"):
        try:
            v[pkg] = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            v[pkg] = None
    return v


def machine() -> dict:
    info = {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "logical_cpus": os.cpu_count(),
    }
    if sys.platform == "darwin":
        info["cpu"] = _out(["sysctl", "-n", "machdep.cpu.brand_string"])
        mem = _out(["sysctl", "-n", "hw.memsize"])
        info["ram_gb"] = round(int(mem) / 2**30, 1) if mem and mem.isdigit() else None
    else:
        info["cpu"] = _first_line_matching(_out(["cat", "/proc/cpuinfo"]), "model name")
        mem = _first_line_matching(_out(["cat", "/proc/meminfo"]), "MemTotal")
        info["ram_gb"] = round(int(mem.split()[1]) / 2**20, 1) if mem else None
    info["conda_env"] = os.environ.get("CONDA_DEFAULT_ENV")
    info["tools_on_path"] = {t: shutil.which(t) for t in ("seqkit", "seqfu", "seqtk")}
    return info


def dataset_checksums(data_dir: str) -> dict:
    """SHA-256 of each input, from prepare_datasets.sh's checksums.tsv."""
    path = os.path.join(data_dir, "checksums.tsv")
    out = {}
    if os.path.exists(path):
        for line in open(path):
            parts = line.rstrip("\n").split("\t")
            if len(parts) == 3:
                out[parts[0]] = {"gzip_sha256": parts[1], "bgzf_sha256": parts[2]}
    return out
