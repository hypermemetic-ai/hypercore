"""Slice 20 — the red→green loop is EXECUTED, not narrated (the methodological keystone).

Acceptance (spec/folding-conditions §the loop is executed): the repo's mantra is "advice can be
ignored, a folding condition cannot" — and the loop is the discipline the system most identifies with.
But `_feedback_loop` only checked that three strings were non-empty: research Experiment 2 proved a
fabricated loop whose own field *says it never ran* — `{red:"PASSED",green:"PASSED"}`, `{red:".",
green:"."}`, `{red:"i did not run this",green:"nor this"}` — folded clean. The gate now **executes**
the recorded command in the fence and requires a real red→green transition (FAIL at the fork base,
PASS at the tip), trusting the exit codes, never the narration. This slice is the guard that makes the
loop real: it drives Experiment 2's fabricated loops and asserts they are **gated**, and drives a
genuinely executable loop and asserts it **folds**.

1. **a fabricated loop is gated** — each Experiment-2 loop now refuses, because the command does not
   make the transition. *RED against the old string-presence gate (every one folded).*
2. **red == green is rejected** — identical verdicts are no transition.
3. **a real red→green loop folds** — a command that fails at the base and passes at the tip clears the
   gate, executed in the fence.
4. **an un-runnable command is gated** — a command that cannot run is not a loop that drove anything.
"""
from __future__ import annotations

import json
import os

from .harness import LOOP, ok, scripted


def check(root: str) -> None:
    from .. import conditions, graph, worker

    print("\nslice 20 — acceptance check  (the red→green loop is executed, not narrated)\n")

    cap = "folding-conditions"

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

    def result_with(name: str, loop: dict):
        ask = staged(f"a change with loop {name}", name)
        res = worker.apply(ask, scripted(json.dumps({
            "report": "did the work", "delta": delta_for(name), "loop": loop})), root)
        return ask, res

    # ── 1. each fabricated Experiment-2 loop is GATED — the central theater, killed ──────────────────
    fabricated = {
        "both-passed": {"command": "true", "red": "PASSED", "green": "PASSED"},
        "dot-dot": {"command": "true", "red": ".", "green": "."},
        "never-ran": {"command": "true", "red": "i did not run this", "green": "nor this"},
        "green-red": {"command": "true", "red": "green", "green": "red"},
    }
    for name, loop in fabricated.items():
        ask, res = result_with(f"fab-{name}", loop)
        blocked = conditions.unmet(res, root)
        ok(blocked is not None and "loop" in blocked,
           f"the fabricated loop {name!r} is gated — its narration is not the gate, the execution is")
        worker.teardown(ask, root)

    # ── 2. red == green is rejected outright — identical verdicts are no transition ──────────────────
    ask, res = result_with("identical", {"command": "test -f RESULT.md", "red": "same", "green": "same"})
    blocked = conditions.unmet(res, root)
    ok(blocked is not None and "transition" in blocked,
       "a loop whose red and green verdicts are identical is rejected — it did not go red→green")
    worker.teardown(ask, root)

    # ── 3. a genuinely executable red→green loop FOLDS — run in the fence, FAIL→PASS ─────────────────
    # RESULT.md exists at the worker's tip (committed) and not at the fork base, so `test -f RESULT.md`
    # fails at HEAD~1 (red) and passes at HEAD (green) — a real transition the gate runs.
    ask, res = result_with("real", LOOP)
    ok(conditions.unmet(res, root) is None,
       "a command that fails at the fork base and passes at the tip clears the gate — executed, not narrated")
    worker.teardown(ask, root)

    # ── 4. an un-runnable command is gated — a loop that cannot run drove nothing ────────────────────
    ask, res = result_with("unrunnable",
                           {"command": "this-command-does-not-exist-xyz --nope",
                            "red": "was broken", "green": "now works"})
    blocked = conditions.unmet(res, root)
    ok(blocked is not None,
       "a command that cannot run in the fence is gated — an un-runnable loop is not a driven behavior")
    worker.teardown(ask, root)

    # ── 5. a command that passes at BOTH base and tip is gated — no red, no transition proven ────────
    ask, res = result_with("no-red",
                           {"command": "true", "red": "claimed broken", "green": "claimed fixed"})
    blocked = conditions.unmet(res, root)
    ok(blocked is not None and ("red" in blocked or "transition" in blocked or "fork base" in blocked),
       "a command that passes even at the fork base is gated — it never went red, so it proved nothing")
    worker.teardown(ask, root)
