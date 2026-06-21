"""The folding conditions — the engineering disciplines made structural.

The disciplines that keep the model from drifting into a god-file of tangled code
(rebuild-spec §7) bite only because each is a *folding condition* in hypercore's
existing sense: the thing that lets a graph fold. Advice can be ignored; a folding
condition cannot. This module is the gate, run at the archive stage before the merge:

- **the spec delta applies** (§3.3) — the delta the graph carries lands cleanly on the
  current spec. (Owned by the self-model; re-checked here so the gate gives one verdict.)
- **a recorded red→green feedback loop** (§7.2) — a behavior-changing graph hands back a
  loop that drove the behavior red before the fix and green after. The feedback loop *is*
  the skill; a correct narrative with no harness is the failure this kills.
- **the line-count budget** (§7.1) — no source file the graph created or grew crosses a
  low line-count ceiling without a decision record justifying it, so the god-file cannot
  re-accrete one quiet edit at a time.

An unmet condition refuses the fold and returns its reason; `conversation.integrate` turns
that into a decision (re-cut, fix the loop, deepen the module), never a silent pass. The
self-model owns the atomic merge (`delta.fold`); this owns the gate before it.

The budget is the antidote keyed to what a module actually costs an agent — its length,
every line context the worker must load — not a subtler property easier to argue around.
The deletion test and "testable through the interface" are the judgment the architecture
review applies (slice 6); the line count is the part that gates mechanically here.
"""
from __future__ import annotations

import os
import subprocess

from . import delta, spec

# The low line-count tripwire (rebuild-spec §7.1). A starting value to tune (§11), not a
# law: the 6,348-line `window.py` it exists to prevent is ~16× this. Keyed to length
# because length is what a long file costs the worker's window, whatever each line means.
BUDGET = 400


def unmet(result, root: str | None = None) -> str | None:
    """The first folding condition this graph's material fails to meet, or None when all are
    met. `result` is the worker's hand-off (its delta, its loop, its worktree)."""
    d = delta.parse(result.delta)
    sp = spec.read_spec(root)
    return _delta(d, sp) or _feedback_loop(d, result) or _deep_module(result, root)


def _delta(d: delta.Delta, sp: spec.Spec) -> str | None:
    reason = delta.check(d, sp)
    return f"the spec delta does not apply: {reason}" if reason else None


def _feedback_loop(d: delta.Delta, result) -> str | None:
    """A behavior-changing graph (a non-trivial delta) MUST hand back a loop that records its
    invocation, its red verdict on the behavior before the fix, and its green verdict after
    it (§7.2). A trivial graph changes no behavior and needs none."""
    if d.trivial:
        return None
    loop = result.loop if isinstance(result.loop, dict) else {}
    missing = [k for k in ("command", "red", "green") if not str(loop.get(k, "")).strip()]
    if missing:
        return ("no recorded red→green feedback loop: the result's loop is missing "
                f"{', '.join(missing)} (rebuild-spec §7.2)")
    return None


def _deep_module(result, root: str | None) -> str | None:
    """No source file this graph created or grew may cross the line-count budget without a
    decision justifying it (§7.1). Scoped to what this graph touched — the .py files in its
    own commit — so a graph is gated by the god-file *it* makes, not a sibling's."""
    tree = result.worktree
    for rel in _touched_py(tree):
        path = os.path.join(tree, rel)
        if not os.path.isfile(path):
            continue                        # removed by the graph — frees budget, never spends it
        n = sum(1 for _ in open(path, encoding="utf-8", errors="ignore"))
        if n > BUDGET and not justified(rel, root):
            return (f"deep-module budget: {rel} is {n} lines, over the {BUDGET}-line ceiling, "
                    "with no decision record justifying it (rebuild-spec §7.1)")
    return None


def _touched_py(tree: str) -> list[str]:
    """The .py files this graph's commit added or grew — its own material, not the whole tree.
    The worker hands back one commit (`worker._record`); its diff against the fork is exactly
    what the graph built."""
    out = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], cwd=tree,
                         capture_output=True, text=True).stdout
    return [ln for ln in out.split() if ln.endswith(".py")]


def justified(rel: str, root: str | None) -> bool:
    """A file over budget is allowed only when a decision record names it — the ADR escape
    hatch (§7.1): crossing the ceiling is a recorded trade-off, never a silent one. Public
    because the architecture review (`review`) consults the same budget and escape hatch for
    its standing whole-tree scan — one budget, the per-graph gate and the standing scan."""
    d = os.path.join(spec.spec_dir(root), "decisions")
    if not os.path.isdir(d):
        return False
    base = os.path.basename(rel)
    return any(base in open(os.path.join(d, n)).read()
               for n in os.listdir(d) if n.endswith(".md"))
