"""Acceptance harness — the operator's path and the disciplines, run headlessly.

    python3 -m hyper --check

Each slice's acceptance check (rebuild-spec §9) is its own module, driven with a
*scripted* transport (no LLM, so the loop is deterministic and fast) over the *real*
graph, spec, conditions, and worktrees — it asserts the system, not a story. The live
architect and the window are the evidence you watch by running `python3 -m hyper`
and `--frame`; this is the evidence that gates.

run() lays the shared ground — a throwaway git-backed root — and walks the slices in
order; each carries its own acceptance contract in its module docstring.
"""
from __future__ import annotations

import os
import subprocess
import tempfile

from . import harness, slice1, slice2, slice3, slice4, slice5, slice6, slice7, slice8

SLICES = (slice1, slice2, slice3, slice4, slice5, slice6, slice7, slice8)


def run() -> int:
    harness.reset()
    root = tempfile.mkdtemp(prefix="hyper-check-")
    os.environ["HYPER_ROOT"] = root
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "check@hypercore"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "check"], cwd=root, check=True)

    for mod in SLICES:
        mod.check(root)

    print()
    n = harness.failures()
    if n:
        print(f"  {n} FAILED\n")
        return 1
    print("  all checks pass — slices 1–8 meet their acceptance checks\n")
    return 0
