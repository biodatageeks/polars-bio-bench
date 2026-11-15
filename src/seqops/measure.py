"""Run one command and measure wall time, CPU time and peak RSS.

Every tool, including polars-bio and Biopython, runs as its own subprocess so
all of them are measured the same way. ``os.wait4`` returns the child's
resource usage directly: user + system CPU and the peak resident set size of
that process (threads included). No ``/usr/bin/time`` parsing is needed.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass

# ru_maxrss is bytes on macOS and kilobytes on Linux.
_RSS_UNIT = 1 if sys.platform == "darwin" else 1024


@dataclass
class Measurement:
    wall_s: float
    cpu_s: float
    peak_rss_mb: float
    returncode: int
    stderr_tail: str


def run_measured(
    argv: list[str],
    stdout_path: str | None = None,
    env: dict[str, str] | None = None,
    timeout_s: float | None = None,
) -> Measurement:
    """Run ``argv``, sending stdout to ``stdout_path`` (or discarding it)."""
    stdout = open(stdout_path, "wb") if stdout_path else subprocess.DEVNULL
    # stderr goes to a file: a pipe could fill up and block a chatty tool.
    with tempfile.TemporaryFile() as stderr:
        try:
            start = time.perf_counter()
            proc = subprocess.Popen(
                argv, stdout=stdout, stderr=stderr, env={**os.environ, **(env or {})}
            )
            deadline = None if timeout_s is None else start + timeout_s
            while True:
                pid, status, usage = os.wait4(proc.pid, os.WNOHANG)
                if pid:
                    break
                if deadline and time.perf_counter() > deadline:
                    proc.kill()
                    pid, status, usage = os.wait4(proc.pid, 0)
                    break
                time.sleep(0.002)
            wall = time.perf_counter() - start
            proc.returncode = os.waitstatus_to_exitcode(status)
        finally:
            if stdout_path:
                stdout.close()
        stderr.seek(0)
        tail = stderr.read()[-2000:].decode(errors="replace")
    return Measurement(
        wall_s=wall,
        cpu_s=usage.ru_utime + usage.ru_stime,
        peak_rss_mb=usage.ru_maxrss * _RSS_UNIT / 2**20,
        returncode=proc.returncode,
        stderr_tail=tail,
    )
