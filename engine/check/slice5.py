"""Slice 5 — the folding conditions: the gate, the loop, the length signal.

Acceptance (spec §9.5): a tree that hands back a behavior change with no recorded
red→green loop cannot fold (a non-negotiable fact); one that grows a source file past the
length signal raises a decision and holds the fold (re-grounded in slice 7 — length
is a signal, not an auto-refusal), leaving the spec untouched; a result that meets every
condition folds, and a file past the signal folds when an accepted-length record accepts
it. Drives the conditions through the real integrate path and real worktrees.
"""
from __future__ import annotations

import json
import os

from .harness import LOOP, ok, scripted


def check(root: str) -> None:
    from .. import conditions, communication, tree, spec, worker

    print("\nslice 5 — acceptance check  (the folding conditions)\n")

    cap = "folding-conditions"
    req = lambda name: spec.read_spec(root).capability(cap) and \
        spec.read_spec(root).capability(cap).requirement(name)
    coherent = lambda: scripted(json.dumps({"coherent": True, "say": "it landed.", "card": None}))

    def delta_for(name: str) -> str:
        return (f"## ADDED — {cap}\n### Requirement: {name}\nThe gate MUST hold.\n"
                f"#### Scenario: s\n- WHEN a fold is attempted\n- THEN the gate runs\n")

    def staged(text: str, name: str):
        ask = tree.file_intent(text)
        tree.approve(tree.raise_card("contract.\n\ndelta:\n" + delta_for(name),
                                       kind="decide", parent=ask.id))
        worker.worktree(ask, root)
        tree.dispatch(ask)
        return ask

    def godfile(fence: str) -> None:
        tree.atomic_write(os.path.join(fence, "engine", "giant.py"),
                           "# a shallow god-file\n" + "x = 0\n" * (conditions.SIGNAL + 60))

    # 1. a behavior change handed back with no recorded loop cannot fold
    ask = staged("a behavior change handed back with no loop", "a loopless change is gated")
    result = worker.apply(ask, scripted(json.dumps({
        "report": "did the work, no harness",
        "delta": delta_for("a loopless change is gated"),
        "loop": {"command": "", "red": "", "green": ""}})), root)         # no recorded loop
    reply = communication.integrate(ask, result, coherent(), root)
    ok(reply.card is not None and not reply.done,
       "a behavior change with no recorded red→green loop cannot fold")
    ok(req("a loopless change is gated") is None, "the refused fold leaves the spec untouched")
    ok(tree.find(ask.id).is_live, "the work stays live with a decision raised, not folded")
    worker.teardown(ask, root)

    # 2. a tree that grows a source file past the length signal raises a decision — the
    # work stays live (re-cut/deepen/accept), never silently folds (loop + delta both fine, so
    # the depth condition is what bites). Length raises a decision, not an auto-refusal.
    ask = staged("a change that grows a god-file", "a god-file is gated")
    godfile(worker._tree_path(ask, root))
    result = worker.apply(ask, scripted(json.dumps({
        "report": "grew a giant module",
        "delta": delta_for("a god-file is gated"),
        "loop": LOOP})), root)
    blocked = conditions.unmet(result, root)
    ok(blocked is not None and "depth" in blocked and "length signal" in blocked
       and "giant.py" in blocked,
       f"length past the {conditions.SIGNAL}-line signal raises a decision on the file")
    reply = communication.integrate(ask, result, coherent(), root)
    ok(reply.card is not None and not reply.done,
       "the decision is raised and the fold is held — not a silent pass")
    ok(req("a god-file is gated") is None, "the held fold leaves the spec untouched")
    worker.teardown(ask, root)

    # 3. a result that meets every condition folds — a recorded loop, an in-signal module
    ask = staged("a clean behavior change", "a clean change folds")
    result = worker.apply(ask, scripted(json.dumps({
        "report": "did the work behind a loop",
        "delta": delta_for("a clean change folds"),
        "loop": LOOP})), root)
    ok(conditions.unmet(result, root) is None,
       "a recorded loop and an in-signal module meet every folding condition")
    reply = communication.integrate(ask, result, coherent(), root)
    ok(reply.done and req("a clean change folds") is not None,
       "the met conditions let the delta fold into the spec")
    worker.teardown(ask, root)

    # 4. a file past the signal folds when an accepted-length record accepts it — the
    # decision's accept-with-reason outcome, recorded as a parseable record (not a substring).
    tree.atomic_write(os.path.join(root, "accepted-lengths.md"),
                       f"accepted: engine/giant.py @{conditions.SIGNAL + 61} "
                       "— deep behind a small interface; its length is context-cost, not shallowness.\n")
    ask = staged("an accepted-length large module", "an accepted-length module folds")
    godfile(worker._tree_path(ask, root))
    result = worker.apply(ask, scripted(json.dumps({
        "report": "grew an accepted-length module",
        "delta": delta_for("an accepted-length module folds"),
        "loop": LOOP})), root)
    ok(conditions.unmet(result, root) is None,
       "a file past the signal with an accepted-length record accepting it clears the gate")
    reply = communication.integrate(ask, result, coherent(), root)
    ok(reply.done and req("an accepted-length module folds") is not None,
       "the accepted-length exception folds")
    worker.teardown(ask, root)

    # 5. the delta condition is part of the same gate: a delta that will not apply is caught
    # as a decision, not an uncaught CannotFold
    ask = staged("a change carrying a delta that will not apply", "unused")
    result = worker.apply(ask, scripted(json.dumps({
        "report": "built it",
        "delta": "## MODIFIED — folding-conditions\n### Requirement: nonexistent\nx\n",
        "loop": LOOP})), root)
    reply = communication.integrate(ask, result, coherent(), root)
    ok(reply.card is not None and not reply.done,
       "a delta that will not apply is caught by the gate as a decision, not a crash")
    worker.teardown(ask, root)
