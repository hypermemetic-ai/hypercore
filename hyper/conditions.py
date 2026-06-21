"""The folding conditions — the engineering disciplines made structural.

The disciplines that keep the model from drifting into a god-file of tangled code
(rebuild-spec §7) bite only because each is a *folding condition* in hypercore's
existing sense: the thing that lets a graph fold. Advice can be ignored; a folding
condition cannot. This module is the gate, run at the archive stage before the merge.

Two of the three conditions are **non-negotiable facts** — they refuse the fold
automatically, exactly as before, because there is nothing to judge:

- **the spec delta applies** (§3.3) — the delta the graph carries lands cleanly on the
  current spec. (Owned by the self-model; re-checked here so the gate gives one verdict.)
- **a recorded red→green feedback loop** (§7.2) — a behavior-changing graph hands back a
  loop that drove the behavior red before the fix and green after. The feedback loop *is*
  the skill; a correct narrative with no harness is the failure this kills.

The third condition is a **judgment**, and so it is shaped differently (rebuild-spec §7.1,
re-grounded in Ousterhout — `research/aposd.md`, ADR 0006):

- **depth** — the criterion is a *deep module*: a lot of behavior behind a small interface.
  Length is not the criterion; it is one **signal** of it, kept for a reason Ousterhout
  doesn't address and that survives his objection — every line is context an agent must
  load, so length is a fair proxy for a module's **context cost**. A source file the graph
  created or grew past the length signal does **not** auto-refuse (length is a signal, not a
  verdict). It **raises a decision** — re-cut / deepen / accept-with-reason — which
  `conversation.integrate` puts on the operator's queue. The fold is held until that depth
  decision is settled; it is never silently refused and never silently passed.

**There is no second, higher length ceiling that auto-refuses** (slice 7, F2). A ceiling at
any number would be the very thing this re-grounding removes — a number standing in for the
judgment of depth — and would force back the escape hatch it deletes. Length raises a
decision across its whole range; judgment and the operator carry it. The anti-dilution
guarantee still holds: over-signal material is *un-foldable* until the operator settles the
depth decision — stronger than the old coincidental-ADR escape, not weaker.

The model-driven red-flag depth *verdict* (is it actually shallow?) is the architecture
review's standing job to grow and is not yet built (slice 7, F1); this slice ships the
mechanical scaffold — length raises the decision, the operator judges depth — honestly.
"""
from __future__ import annotations

import os
import subprocess

from . import delta, spec

# The length signal (rebuild-spec §7.1). Past this many lines a touched source file raises a
# depth decision — not a refusal. A starting value to tune (§11), not a law: the 6,348-line
# `window.py` it exists to catch early is ~16× this. Keyed to length because length is what a
# file costs the worker's window, whatever each line means — its context cost, not its depth.
SIGNAL = 400


def unmet(result, root: str | None = None) -> str | None:
    """The first folding condition this graph's material fails to meet, or None when all are
    met. `result` is the worker's hand-off (its delta, its loop, its worktree). The delta and
    the loop are non-negotiable facts; the depth condition returns a *decision* (re-cut /
    deepen / accept), which the architect raises on the operator's queue."""
    d = delta.parse(result.delta)
    sp = spec.read_spec(root)
    return _delta(d, sp) or _feedback_loop(d, result) or _depth(result, root)


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


def _depth(result, root: str | None) -> str | None:
    """Depth is the criterion; length is its signal (§7.1). A source file this graph created or
    grew past the length signal, with no depth-decision accepting it, raises a depth decision —
    re-cut / deepen / accept-with-reason — never a silent refusal and never a silent pass.
    Scoped to what this graph touched — the .py files in its own commit — so a graph is judged
    on the depth of what *it* built, not a sibling's. Length never auto-refuses (F2): a long
    file is either judged deep (fine — length was only context-cost signal) or raises this
    decision for the operator to settle."""
    tree = result.worktree
    for rel in _touched_py(tree):
        path = os.path.join(tree, rel)
        if not os.path.isfile(path):
            continue                        # removed by the graph — frees context, never spends it
        n = sum(1 for _ in open(path, encoding="utf-8", errors="ignore"))
        if n > SIGNAL and not accepted(rel, root):
            return (f"depth decision: {rel} is {n} lines, past the {SIGNAL}-line length signal "
                    "— re-cut it, deepen it, or record a depth-decision accepting it "
                    "(rebuild-spec §7.1). Length is a context-cost signal, not a depth verdict; "
                    "the depth judgment is the operator's.")
    return None


def _touched_py(tree: str) -> list[str]:
    """The .py files this graph's commit added or grew — its own material, not the whole tree.
    The worker hands back one commit (`worker._record`); its diff against the fork is exactly
    what the graph built."""
    out = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], cwd=tree,
                         capture_output=True, text=True).stdout
    return [ln for ln in out.split() if ln.endswith(".py")]


def accepted(rel: str, root: str | None) -> bool:
    """True when a **structured depth-decision** records this exact file as accepted past the
    length signal (rebuild-spec §7.1, ADR 0006). The record is a line in a decision file:

        depth-decision: <repo-relative path> accepted — <reason>

    The gate matches the *path*, not a basename appearing anywhere in prose — so a coincidental
    mention can no longer grant an exception. This replaces the old loose substring `justified`
    match, whose hole was that any ADR naming a coincidentally-large file read as a free pass.
    The exception is the *decision*, not the *spelling*. Public because the architecture review
    (`review`) consults the same record for its standing whole-tree scan — one criterion, the
    per-graph gate and the standing scan. `rel` is the file's path relative to the repo root
    (e.g. `hyper/foo.py`)."""
    d = os.path.join(spec.spec_dir(root), "decisions")
    if not os.path.isdir(d):
        return False
    want = rel.replace(os.sep, "/")
    for name in os.listdir(d):
        if not name.endswith(".md"):
            continue
        for line in open(os.path.join(d, name), encoding="utf-8", errors="ignore"):
            if _depth_record(line) == want:
                return True
    return False


def _depth_record(line: str) -> str | None:
    """Parse one `depth-decision: <path> accepted — …` line to the accepted path, or None.
    A line is a depth-decision only with the exact structured prefix and an `accepted` outcome;
    anything else (prose, a different outcome) is not a pass."""
    text = line.strip()
    if not text.lower().startswith("depth-decision:"):
        return None
    body = text.split(":", 1)[1].strip()
    parts = body.split()
    if len(parts) < 2 or "accepted" not in (p.strip(",.—-").lower() for p in parts[1:]):
        return None
    return parts[0].rstrip(",").replace(os.sep, "/")
