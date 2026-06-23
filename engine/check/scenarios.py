"""Acceptance — the self-model is self-verifying: a capability's scenarios are its executable checks.

This is the acceptance path that replaces the dissolved by-slice harness for a migrated capability.
It is the home of `folding-conditions`' checks now that slices 5/7/9/20/21's folding-conditions
content has dissolved into the capability's own scenarios (`spec/folding-conditions.md`). It asserts
three things:

1. **the scenarios are green** — every `#### Scenario:` check block in `spec/folding-conditions.md`
   runs against the live engine and passes, so the system meets its own spec right now;
2. **the classification is derived, not hand-tended** — the gated/watched register is read off the
   presence of check blocks (`scenario.classification`), so it cannot drift from what is gated;
3. **the scenario gate is a real red→green** — over a fence whose tip changes a folding-conditions
   behavior (the length signal) and whose base does not, the gate runs the capability's scenarios at
   the fork base (red) and the tip (green), trusting exit codes — and refuses a tip that is not green.
   This is the gate the worker's self-authored loop is replaced by; it cannot certify itself from
   inside a fold, so the harness exercises it here, from outside.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile

from .harness import ok
from .. import scenario, tree, worker

REAL = tree._DEFAULT_ROOT                                  # hypercore's own source tree — the spec under test

# A behavior change touching folding-conditions: the delta the synthetic hand-off carries, so the gate
# runs that capability's scenarios. The worktree is the demo fence (below).
_DELTA = ("# delta — signal change\n## MODIFIED — folding-conditions\n"
          "### Requirement: length past the signal raises a decision, never a silent refusal\nx\n")


def check(root: str) -> None:
    print("\nscenarios — acceptance check  (the self-model is self-verifying: folding-conditions)\n")

    # 1. every folding-conditions scenario is green against the live engine ───────────────────────────
    outcomes = scenario.run("folding-conditions", REAL)
    ok(len(outcomes) >= 7, f"folding-conditions carries its executable scenarios ({len(outcomes)} blocks)")
    for o in outcomes:
        ok(o.passed, f"scenario green: {o.scenario}" + ("" if o.passed else f" — {o.detail}"))

    # 2. the gated/watched classification is DERIVED from the presence of a check block ───────────────
    cls = dict(scenario.classification("folding-conditions", REAL))
    gated = [n for n, k in cls.items() if k == "gated"]
    ok(all(cls.get(r) == "gated" for r in (
        "length past the signal raises a decision, never a silent refusal",
        "an accepted length is bounded to the length it names, and ratchets",
        "the accepted-length record is durable authored state, written through one seam")),
       f"the standards proven by a check block are gated, read off the blocks ({len(gated)} gated)")
    ok(cls.get("a behavior change folds only when its capability's scenario goes red→green") == "watched"
       and cls.get("a standard is gated by carrying a scenario, watched without one") == "watched",
       "the gate mechanism and the deriving rule carry no in-spec block — watched, exercised here, never faked")

    # 3. the scenario gate is a REAL red→green — and refuses a tip that is not green ───────────────────
    # The fence's tip lowers the length signal 500→400 (a real folding-conditions behavior change); its
    # scenarios are calibrated to 400, so they FAIL at the base (signal 500) and PASS at the tip. The
    # gate runs them in the fence, trusting only the exit codes.
    transit = _demo_fence(base=500, tip=400)
    try:
        ok(scenario.gate(worker.WorkerResult("built it", _DELTA, transit), REAL) is None,
           "RED→GREEN: the capability's scenarios fail at the fork base and pass at the tip — the gate clears")
    finally:
        _drop(transit)

    held = _demo_fence(base=500, tip=500)                  # the tip never built the behavior — still red
    try:
        ok(scenario.gate(worker.WorkerResult("did not build it", _DELTA, held), REAL) is not None,
           "a tip whose scenarios are not green is refused — narration is never the gate, the exit code is")
    finally:
        _drop(held)


# ── a fence with a real engine at two commits: the base and tip differ only in the length signal ──

def _demo_fence(base: int, tip: int) -> str:
    f = tempfile.mkdtemp(prefix="scenario-demo-")
    for c in (("init", "-q"), ("config", "user.email", "demo@hypercore"), ("config", "user.name", "demo")):
        subprocess.run(["git", *c], cwd=f, check=True, stdout=subprocess.DEVNULL)
    for d in ("engine", "spec"):                           # a real, runnable engine + the spec under test
        shutil.copytree(os.path.join(REAL, d), os.path.join(f, d),
                        ignore=shutil.ignore_patterns("__pycache__"))
    _set_signal(f, base); _commit(f, "base")               # HEAD~1 — the behavior not yet built
    _set_signal(f, tip); _commit(f, "tip")                 # HEAD — the tip the worker hands back
    return f


def _set_signal(fence: str, n: int) -> None:
    p = os.path.join(fence, "engine", "conditions.py")
    with open(p, encoding="utf-8") as fh:
        text = fh.read()
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(re.sub(r"^SIGNAL = \d+", f"SIGNAL = {n}", text, count=1, flags=re.MULTILINE))


def _commit(fence: str, msg: str) -> None:
    subprocess.run(["git", "add", "-A"], cwd=fence, check=True, stdout=subprocess.DEVNULL)
    # --allow-empty: the no-transition fence (base == tip) commits an identical tip — a legitimate fixture
    subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", msg], cwd=fence, check=True,
                   stdout=subprocess.DEVNULL)


def _drop(path: str) -> None:
    shutil.rmtree(path, ignore_errors=True)
