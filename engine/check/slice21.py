"""Slice 21 — the coherence incoherent branch is exercised; the gated-vs-watched standards are real.

Acceptance (spec/coherence, spec/folding-conditions §the standards declare gated or watched):
research Experiment 3/6 proved the coherence gate's incoherent branch was never driven — replacing the
gate with `if False` (always coherent) left the harness fully GREEN; the gate could be removed and
nothing noticed. And the meta-weakness — a regenerating author scripting a judgment and calling it
tested — had no machine-readable backstop. This slice closes both:

1. **the incoherent branch is exercised** — feeding `coherent: false` refuses the fold, leaves the
   spec untouched, keeps the node live (recovered, not folded), and raises a decision card carrying the
   architect's words. *RED if the incoherent branch is never driven (the gate could be removed).*
2. **a coherent result still folds** — the gate's two branches are both real, not one-sided.
3. **the gated-vs-watched standards are machine-readable and honest** — every standard is classified
   gated or watched on a parseable line; the gated ones name a real gate, the watched ones are recorded
   as not mechanically enforced. *RED if a model-side judgment is declared gated (scripted-and-called-
   tested) or a standard is unclassified.*
"""
from __future__ import annotations

import json
import os

from .harness import LOOP, ok, scripted


def check(root: str) -> None:
    from .. import communication, tree, spec, worker

    print("\nslice 21 — acceptance check  (the coherence incoherent branch; the gated-vs-watched register)\n")

    cap = "folding-conditions"

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

    req = lambda name: (spec.read_spec(root).capability(cap)
                        and spec.read_spec(root).capability(cap).requirement(name))

    # ── 1. the incoherent branch: coherent:false refuses, the spec is untouched, the node is live ────
    ask = staged("a result the architect judges incoherent", "an incoherent result is gated")
    result = worker.apply(ask, scripted(json.dumps({
        "report": "did the work but missed the contract",
        "delta": delta_for("an incoherent result is gated"), "loop": LOOP})), root)
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
        "report": "honored the contract", "delta": delta_for("a coherent result folds"),
        "loop": LOOP})), root)
    coherent = scripted(json.dumps({"coherent": True, "say": "it landed.", "card": None}))
    reply = communication.integrate(ask, result, coherent, root)
    ok(reply.done and req("a coherent result folds") is not None,
       "a coherent result folds — the gate's two branches are both real, not one-sided")
    worker.teardown(ask, root)

    # ── 3. the gated-vs-watched standards are machine-readable and honest ────────────────────────────
    fc = spec.read_spec(root).capability(cap) or spec.read_spec(tree._DEFAULT_ROOT).capability(cap)
    text = "\n".join(r.block for r in fc.requirements) if fc else ""
    standards = {}
    for line in text.splitlines():
        s = line.strip().lstrip("- ").strip()
        if s.startswith("standard:"):
            parts = [p.strip() for p in s[len("standard:"):].split("—")]
            if len(parts) >= 2 and parts[1] in ("gated", "watched"):
                standards[parts[0]] = parts[1]
    ok(len(standards) >= 8,
       f"every standard declares gated or watched on a parseable line (found {len(standards)})")
    ok(standards.get("red-green-loop") == "gated" and standards.get("delta-applies") == "gated"
       and standards.get("mechanical-red-flags") == "gated" and standards.get("length-ratchet") == "gated",
       "the deterministically-gated standards are declared gated — a real gate, not a scripted judgment")
    ok(standards.get("module-depth-judgment") == "watched" and standards.get("coherence") == "watched"
       and standards.get("grilling-floor") == "watched" and standards.get("design-it-twice-selection") == "watched",
       "the model-side judgments are declared watched — not scripted-and-called-tested (the meta-weakness)")

    # the classification's own honesty bites: the loop it declares gated is the one slice 20 proves
    # executed, and the module depth judgment it declares watched is the one the review records as
    # not-yet-built — so the classification is not free prose, it tracks what the code actually does.
    from .. import review
    backlog = " ".join(review.backlog(review.review(tree._DEFAULT_ROOT)))
    ok("not yet built" in backlog and standards.get("module-depth-judgment") == "watched",
       "the watched module-depth-judgment standard matches the review's honest not-yet-built record")
