"""Acceptance harness — the operator's path and the disciplines, run headlessly.

    python3 -m engine --check

Each slice's acceptance check is its own module, driven with a
*scripted* transport (no LLM, so the loop is deterministic and fast) over the *real*
tree, spec, conditions, and worktrees — it asserts the system, not a story. The live
architect and the window are the evidence you watch by running `python3 -m engine`
and `--frame`; this is the evidence that gates.

run() lays the shared ground — a throwaway git-backed root — and walks the slices in
order; each carries its own acceptance contract in its module docstring.
"""
from __future__ import annotations

import os
import subprocess
import tempfile

# Capability scenarios + the remaining by-slice checks. Migrated capabilities run off their own
# executable scenarios (`scenarios`), not a slice: folding-conditions left slices 5/7/9/20/21,
# coherence left slice 21, worker left slices 4/7/10/23, and architecture-review left slices 6/7/9/15 —
# so each wholly-migrated slice file is gone (4/5/6/7/9/10/15/20/21/23). The gaps in the numbering mark
# the migration; each remaining capability dissolves its slice content the same way as it migrates,
# until no slice file is left and `--check` runs entirely off capability scenarios.
from . import (harness, scenarios, slice1, slice2, slice3, slice8,
               slice11, slice12, slice13, slice14, slice16, slice17,
               slice18, slice19, slice22)

SLICES = (slice1, slice2, slice3, slice8,
          slice11, slice12, slice13, slice14, slice16, slice17, slice18, slice19,
          slice22, scenarios)


def run() -> int:
    harness.reset()
    root = tempfile.mkdtemp(prefix="engine-check-")
    os.environ["ENGINE_ROOT"] = root
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
    print("  all checks pass — the capability scenarios and the remaining slice checks are met\n")
    return 0
