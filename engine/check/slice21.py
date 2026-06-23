"""Slice 21 — the coherence gate's incoherent branch is exercised (both branches are real).

The machine-readable gated-vs-watched register this slice once also asserted has been retired: the
classification is now **derived** from the presence of a check block on a scenario
(`scenario.classification`, `engine/check/scenarios.py`), so there is no hand-maintained table to
drift, and the folding-conditions content has migrated to that capability's own scenarios. What stays
here is the `coherence` surface: research Experiment 3/6 proved the coherence gate's incoherent branch
was never driven — replacing the gate with `if False` (always coherent) left the harness fully GREEN.
This slice closes that, and migrates to coherence's own scenarios when that capability is migrated.

1. **the incoherent branch is exercised** — feeding `coherent: false` refuses the fold, leaves the
   spec untouched, keeps the node live (recovered, not folded), and raises a decision card carrying the
   architect's words. *RED if the incoherent branch is never driven (the gate could be removed).*
2. **a coherent result still folds** — the gate's two branches are both real, not one-sided.
"""
from __future__ import annotations

import json

from .harness import ok, scripted


def check(root: str) -> None:
    from .. import communication, tree, spec, worker

    print("\nslice 21 — acceptance check  (the coherence incoherent branch is exercised)\n")

    # A fixture capability that carries no executable scenarios, so the scenario gate stays inert and
    # this check isolates the coherence branch — the gate has its own red→green in `scenarios`.
    cap = "demo-coherence"
    req = lambda name: (spec.read_spec(root).capability(cap)
                        and spec.read_spec(root).capability(cap).requirement(name))

    def delta_for(name: str) -> str:
        return (f"## ADDED — {cap}\n### Requirement: {name}\nThe gate MUST hold.\n"
                f"#### Scenario: s\n- WHEN a fold is attempted\n- THEN the gate runs\n")

    def staged(text: str, name: str) -> tree.Node:
        ask = tree.file_intent(text)
        tree.approve(tree.raise_card("contract.\n\ndelta:\n" + delta_for(name),
                                       kind="decide", parent=ask.id))
        worker.worktree(ask, root)
        tree.dispatch(ask)
        return ask

    # ── 1. the incoherent branch: coherent:false refuses, the spec is untouched, the node is live ────
    ask = staged("a result the architect judges incoherent", "an incoherent result is gated")
    result = worker.apply(ask, scripted(json.dumps({
        "report": "did the work but missed the contract",
        "delta": delta_for("an incoherent result is gated")})), root)
    incoherent = scripted(json.dumps({
        "coherent": False,
        "say": "This doesn't honor the contract — it solved a different problem.",
        "card": "the result did not honor the contract — re-cut, abandon, or change the ask"}))
    reply = communication.integrate(ask, result, incoherent, root)
    ok(not reply.done and reply.card is not None,
       "a result judged incoherent does not fold — the incoherent branch raises a decision (Exp 3/6)")
    ok(reply.card.kind == "decide" and reply.card.parent == ask.id,
       "the incoherent verdict raises a decision card parented to the node — recovery, not a silent drop")
    ok(req("an incoherent result is gated") is None,
       "the refused fold leaves the spec untouched — coherent:false never merges the delta")
    after = tree.find(ask.id)
    ok(after is not None and after.folded is False,
       "the node is not folded on an incoherent verdict — it stays live for the operator's decision")
    worker.teardown(ask, root)

    # ── 2. a coherent result still folds — both branches of the gate are real ───────────────────────
    ask = staged("a result the architect judges coherent", "a coherent result folds")
    result = worker.apply(ask, scripted(json.dumps({
        "report": "honored the contract", "delta": delta_for("a coherent result folds")})), root)
    coherent = scripted(json.dumps({"coherent": True, "say": "it landed.", "card": None}))
    reply = communication.integrate(ask, result, coherent, root)
    ok(reply.done and req("a coherent result folds") is not None,
       "a coherent result folds — the gate's two branches are both real, not one-sided")
    worker.teardown(ask, root)
