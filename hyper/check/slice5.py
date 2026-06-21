"""Slice 5 — the folding conditions: the gate, the loop, the budget.

Acceptance (spec §9.5): a graph that hands back a behavior change with no recorded
red→green loop, or one that grows a source file past the line-count budget, cannot fold —
the folding conditions refuse it and return a decision, leaving the spec untouched; a
result that meets every condition folds, and a file over budget folds only when a decision
record justifies it. Drives the conditions through the real integrate path and real
worktrees.
"""
from __future__ import annotations

import json
import os

from .harness import ok, scripted


def check(root: str) -> None:
    from .. import conditions, conversation, graph, spec, worker

    print("\nslice 5 — acceptance check  (the folding conditions)\n")

    cap = "folding-conditions"
    req = lambda name: spec.read_spec(root).capability(cap) and \
        spec.read_spec(root).capability(cap).requirement(name)
    coherent = lambda: scripted(json.dumps({"coherent": True, "say": "it landed.", "card": None}))

    def delta_for(name: str) -> str:
        return (f"## ADDED — {cap}\n### Requirement: {name}\nThe gate MUST hold.\n"
                f"#### Scenario: s\n- WHEN a fold is attempted\n- THEN the gate runs\n")

    def staged(text: str, name: str):
        ask = graph.file_intent(text)
        graph.approve(graph.raise_card("contract.\n\ndelta:\n" + delta_for(name),
                                       kind="decide", parent=ask.id))
        worker.worktree(ask, root)
        graph.delegate(ask)
        return ask

    def godfile(tree: str) -> None:
        graph.atomic_write(os.path.join(tree, "hyper", "giant.py"),
                           "# a shallow god-file\n" + "x = 0\n" * (conditions.BUDGET + 60))

    # 1. a behavior change handed back with no recorded loop cannot fold
    ask = staged("a behavior change handed back with no loop", "a loopless change is gated")
    result = worker.apply(ask, scripted(json.dumps({
        "report": "did the work, no harness",
        "delta": delta_for("a loopless change is gated"),
        "loop": {"command": "", "red": "", "green": ""}})), root)         # no recorded loop
    reply = conversation.integrate(ask, result, coherent(), root)
    ok(reply.card is not None and not reply.done,
       "a behavior change with no recorded red→green loop cannot fold")
    ok(req("a loopless change is gated") is None, "the refused fold leaves the spec untouched")
    ok(graph.find(ask.id).is_live, "the work stays live with a decision raised, not folded")
    worker.teardown(ask, root)

    # 2. a graph that grows a source file past the budget cannot fold (loop + delta both fine,
    # so the budget is what bites)
    ask = staged("a change that grows a god-file", "a god-file is gated")
    godfile(worker._tree_path(ask, root))
    result = worker.apply(ask, scripted(json.dumps({
        "report": "grew a giant module",
        "delta": delta_for("a god-file is gated"),
        "loop": {"command": "run", "red": "failed", "green": "passed"}})), root)
    blocked = conditions.unmet(result, root)
    ok(blocked is not None and "budget" in blocked and "giant.py" in blocked,
       f"the budget condition catches the god-file the graph grew ({conditions.BUDGET}-line ceiling)")
    reply = conversation.integrate(ask, result, coherent(), root)
    ok(reply.card is not None and not reply.done, "a graph that grows a god-file cannot fold")
    ok(req("a god-file is gated") is None, "the refused fold leaves the spec untouched")
    worker.teardown(ask, root)

    # 3. a result that meets every condition folds — a recorded loop, an in-budget module
    ask = staged("a clean behavior change", "a clean change folds")
    result = worker.apply(ask, scripted(json.dumps({
        "report": "did the work behind a loop",
        "delta": delta_for("a clean change folds"),
        "loop": {"command": "python3 -m hyper --check", "red": "absent", "green": "present"}})), root)
    ok(conditions.unmet(result, root) is None,
       "a recorded loop and an in-budget module meet every folding condition")
    reply = conversation.integrate(ask, result, coherent(), root)
    ok(reply.done and req("a clean change folds") is not None,
       "the met conditions let the delta fold into the spec")
    worker.teardown(ask, root)

    # 4. a file over budget folds when a decision record justifies it (the ADR escape hatch)
    graph.atomic_write(os.path.join(spec.spec_dir(root), "decisions", "0099-giant-justified.md"),
                       "# ADR 0099\n\nhyper/giant.py is allowed over the budget here.\n")
    ask = staged("a justified large module", "a justified module folds")
    godfile(worker._tree_path(ask, root))
    result = worker.apply(ask, scripted(json.dumps({
        "report": "grew a justified module",
        "delta": delta_for("a justified module folds"),
        "loop": {"command": "run", "red": "failed", "green": "passed"}})), root)
    ok(conditions.unmet(result, root) is None,
       "a file over budget but named in a decision record clears the budget condition")
    reply = conversation.integrate(ask, result, coherent(), root)
    ok(reply.done and req("a justified module folds") is not None, "the justified exception folds")
    worker.teardown(ask, root)

    # 5. the delta condition is part of the same gate: a delta that will not apply is caught
    # as a decision, not an uncaught CannotFold
    ask = staged("a change carrying a delta that will not apply", "unused")
    result = worker.apply(ask, scripted(json.dumps({
        "report": "built it",
        "delta": "## MODIFIED — folding-conditions\n### Requirement: nonexistent\nx\n",
        "loop": {"command": "run", "red": "failed", "green": "passed"}})), root)
    reply = conversation.integrate(ask, result, coherent(), root)
    ok(reply.card is not None and not reply.done,
       "a delta that will not apply is caught by the gate as a decision, not a crash")
    worker.teardown(ask, root)
