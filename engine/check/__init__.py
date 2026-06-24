"""Acceptance harness — the operator's path and the disciplines, run headlessly.

    python3 -m engine --check

Each capability's acceptance is its own executable scenarios, homed in its `spec/<capability>.md` and
compiled by the `scenario` binding, driven against the *real* tree, spec, conditions, and worktrees —
it asserts the system, not a story. The live architect and the window are the evidence you watch by
running `python3 -m engine` and `--frame`; this is the evidence that gates.

run() lays the shared ground — a throwaway git-backed root — and runs the scenario acceptance path:
every migrated capability's check blocks against the live engine, the gated/watched register derived
off those blocks, the real red→green fold gate, and the watched structural invariants the closed
scenario vocabulary cannot honestly express. The by-slice harness is gone — the last group
(queue / interface / channels) migrated to its own scenarios, so nothing is checked by build-slice
anymore; `scenario` is the one acceptance module.
"""
from __future__ import annotations

import os
import subprocess
import tempfile

from . import harness, scenarios

# The acceptance path is the capability scenarios, end to end. Every migrated capability runs off its
# own executable scenarios (`spec/<capability>.md`'s `#### Scenario:` check blocks), discovered live —
# so a newly migrated capability appears with no edit here — never a by-slice module. `scenarios` is the
# self-verifying gate: it runs every capability's blocks, derives the gated/watched register off them,
# exercises the real red→green fold gate, and asserts the watched structural invariants from outside.
SLICES = (scenarios,)


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
    print("  all checks pass — the capability scenarios are met\n")
    return 0
