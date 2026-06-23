"""Acceptance — the self-model is self-verifying: a capability's scenarios are its executable checks.

This is the acceptance path that replaces the dissolved by-slice harness for every migrated
capability. As each capability's checks home in its own spec (`spec/<capability>.md`), it runs here
with no edit: the green-and-derive loop iterates **every capability whose spec carries a check block**
— the set is read off the specs, never hand-listed — so a newly migrated capability appears the moment
its first block lands. It asserts three things:

1. **the scenarios are green** — every `#### Scenario:` check block in every migrated capability runs
   against the live engine and passes, so the system meets its own spec right now;
2. **the classification is derived, not hand-tended** — a requirement is gated exactly when one of its
   scenarios carries a check block and watched otherwise (`scenario.classification`), checked here to
   read off the blocks themselves, so the register cannot drift from what is gated;
3. **the scenario gate is a real red→green** — over a fence whose tip changes a folding-conditions
   behavior (the length signal) and whose base does not, the gate runs the capability's scenarios at
   the fork base (red) and the tip (green), trusting exit codes — and refuses a tip that is not green.
   This is the gate the worker's self-authored loop is replaced by; it cannot certify itself from
   inside a fold, so the harness exercises it here, from outside.

A migrated capability may also carry **watched** invariants the closed scenario vocabulary cannot
honestly express — a retired constant, a scaffold the live model would otherwise verify, a structural
fact. Those are exercised here from outside (never a faked in-spec block), grouped by capability: the
gate red→green above is folding-conditions'; the worker section below is the worker's.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile

from .harness import ok
from .. import design, review, scenario, schedule, spec, transport, tree, worker

REAL = tree._DEFAULT_ROOT                                  # hypercore's own source tree — the spec under test

# A behavior change touching folding-conditions: the delta the synthetic hand-off carries, so the gate
# runs that capability's scenarios. The worktree is the demo fence (below).
_DELTA = ("# delta — signal change\n## MODIFIED — folding-conditions\n"
          "### Requirement: length past the signal raises a decision, never a silent refusal\nx\n")


def check(root: str) -> None:
    print("\nscenarios — acceptance check  (the self-model is self-verifying: capability scenarios)\n")

    # 1. every capability that carries check blocks is green, and its gated/watched classification is
    #    READ OFF the blocks — derived, never hand-tended. The set of migrated capabilities is the set
    #    whose spec carries a block, read live, so a newly migrated capability appears here with no edit.
    migrated = [c.name for c in spec.read_spec(REAL).capabilities if scenario.checks(c.name, REAL)]
    ok({"folding-conditions", "coherence", "worker", "architecture-review", "design-it-twice"} <= set(migrated),
       f"the migrated capabilities carry their executable scenarios ({', '.join(migrated)})")
    for cap in migrated:
        for o in scenario.run(cap, REAL):
            ok(o.passed, f"{cap} — scenario green: {o.scenario}" + ("" if o.passed else f": {o.detail}"))
        blocked = {c.requirement for c in scenario.checks(cap, REAL)}
        cls = dict(scenario.classification(cap, REAL))
        ok(all((k == "gated") == (r in blocked) for r, k in cls.items()),
           f"{cap} — gated/watched is read off the check blocks "
           f"({sum(k == 'gated' for k in cls.values())} gated, {sum(k == 'watched' for k in cls.values())} watched)")

    # 2. the scenario gate is a REAL red→green — and refuses a tip that is not green ───────────────────
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

    # 3. worker — structural/scaffold invariants the closed scenario vocabulary cannot honestly express
    #    (a retired constant, the model the worker targets, the scheduler's injection point): watched,
    #    exercised here from outside, never faked. The worker's behavior is gated in spec/worker.md.
    ok(not hasattr(worker, "DEPTH"),
       "worker — the frozen DEPTH constant is retired; the depth standards are single-sourced from spec/depth.md")
    argv = transport.worker_argv("PROMPT")
    ok(transport.WORKER_CMD in argv and transport.WORKER_MODEL in argv,
       "worker — the harness binary and model are named in one place, bound at the fence (the OMP/GPT flip point)")
    ok(schedule.Scheduler().transport is None,
       "worker — the scheduler forwards the live worker injection point untouched, so the worker binds its own fence")

    # 4. architecture-review — facts about hypercore's OWN source the standing scan reads, exercised
    #    from outside. The review's *behavior* (flag a god-file, tell a stale acceptance from an over
    #    file, read the mechanical red flags, render the derived operator view) is gated in
    #    spec/architecture-review.md; what no fixture can assert is the artifact itself — that the live
    #    engine tree is honestly clean, so a regression that grows a god-file or a cycle goes red here.
    rv = review.review(REAL)
    ok(not any(m.status in ("over", "exceeded", "accepted") for m in rv.modules),
       "architecture-review — the real engine tree is honestly clean: no module past the length signal")
    flags = review.red_flags(REAL)
    ok(not flags, "architecture-review — the real engine tree carries no mechanical red flags"
       + (f" (found: {[f.subject for f in flags]})" if flags else " (dead symbols, circular imports)"))

    # 5. design-it-twice — the architect's selection prompt names the three comparison axes by
    #    construction (a prompt-construction fact no domain verb can honestly express without naming the
    #    prompt; cf. the worker prompt invariants). The contest behavior is gated in
    #    spec/design-it-twice.md.
    ok(all(ax in design.SELECT for ax in ("DEPTH", "LOCALITY", "SEAM PLACEMENT")),
       "design-it-twice — the selection prompt compares candidates on depth, locality, and seam placement")


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
