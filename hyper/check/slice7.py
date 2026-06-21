"""Slice 7 — the architecture re-grounded in depth (Ousterhout).

Acceptance (next-work.md / research/regrounding.md §9): the constraints read in Ousterhout's
terms (deep modules, the red flags); the mechanical gate and the standing review reflect them;
**the operator reads the system's depth, not merely its length**; and the slice-6 check.py split
is re-decided on the new criteria (kept, on locality — see ADR 0006). This check drives the
re-grounded gate, review, and worker grounding deterministically, and pins the two properties
that distinguish the re-grounding from slice 5's budget:

1. length **never auto-refuses** — even far past the signal it raises a *decision* the operator
   can accept (F2: no hard ceiling); and
2. the justification hole is **closed by construction** — only a *structured* depth-decision
   clears the gate, never a coincidental mention (the old substring hole).
"""
from __future__ import annotations

import json
import os

from .harness import ok, scripted


def check(root: str) -> None:
    from .. import conditions, conversation, graph, review, spec, worker

    print("\nslice 7 — acceptance check  (the architecture re-grounded in depth)\n")

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

    def longfile(tree: str, name: str, lines: int) -> None:
        graph.atomic_write(os.path.join(tree, "hyper", name),
                           "# a long module\n" + "x = 0\n" * lines)

    def decide(name: str, body: str):
        graph.atomic_write(os.path.join(spec.spec_dir(root), "decisions", name), body)

    # 1. length raises a DECISION, never a silent veto — and the reason names the three
    # outcomes (re-cut / deepen / accept). The gate hands the operator a depth judgment, not a
    # number's verdict (re-grounding §4; spec/folding-conditions, spec/conversation-as-architect).
    # (A file with no depth-decision record of its own — names are unique so a sibling slice's
    # record can't clear it.)
    ask = staged("a change past the signal", "a depth decision is raised")
    longfile(worker._tree_path(ask, root), "tall.py", conditions.SIGNAL + 50)
    result = worker.apply(ask, scripted(json.dumps({
        "report": "grew a long module",
        "delta": delta_for("a depth decision is raised"),
        "loop": {"command": "run", "red": "failed", "green": "passed"}})), root)
    blocked = conditions.unmet(result, root)
    ok(blocked is not None and "depth decision" in blocked
       and all(w in blocked for w in ("re-cut", "deepen", "accept")),
       "length past the signal raises a depth decision naming re-cut / deepen / accept")
    ok(blocked is not None and "context-cost signal" in blocked and "not a depth verdict" in blocked,
       "the gate frames length as a context-cost signal, not a depth verdict — the operator judges")
    reply = conversation.integrate(ask, result, coherent(), root)
    ok(reply.card is not None and reply.card.kind == "decide" and not reply.done,
       "the architect raises the depth decision on the queue — never a silent veto or pass")
    worker.teardown(ask, root)

    # 2. NO hard auto-refusing ceiling (F2): a file FAR past the signal — pathological length —
    # still only raises a decision, and a structured depth-decision accepting it lets it fold.
    # No number refuses outright; judgment + the operator-decision carry the whole range.
    decide("0101-pathological-depth.md",
           f"# ADR 0101\n\ndepth-decision: hyper/huge.py accepted@{conditions.SIGNAL * 6 + 1} — "
           "generated table, deep behind a three-call interface; length is context-cost, not "
           "shallowness.\n")
    ask = staged("a pathologically long but accepted module", "a far-past-signal module folds")
    longfile(worker._tree_path(ask, root), "huge.py", conditions.SIGNAL * 6)   # ~6× the signal
    result = worker.apply(ask, scripted(json.dumps({
        "report": "grew a very long but depth-accepted module",
        "delta": delta_for("a far-past-signal module folds"),
        "loop": {"command": "run", "red": "failed", "green": "passed"}})), root)
    ok(conditions.unmet(result, root) is None,
       "even ~6× the signal does not auto-refuse — a structured depth-decision lets it fold (F2)")
    reply = conversation.integrate(ask, result, coherent(), root)
    ok(reply.done and req("a far-past-signal module folds") is not None,
       "length has no hard ceiling: judgment + the operator-decision carry the whole range")
    worker.teardown(ask, root)

    # 3. THE HOLE CLOSED BY CONSTRUCTION: a coincidental mention of the file in decision prose —
    # the old loose-substring escape — does NOT clear the gate. Only the structured
    # `depth-decision: <path> accepted` record does. This is the regression the re-grounding adds.
    decide("0102-coincidental.md",
           "# ADR 0102\n\nWe discussed hyper/wide.py at length; it is over the old budget but "
           "the team is fine with it.\n")                                # prose only — no structured record
    ask = staged("a change naming the file only in prose", "the substring hole stays closed")
    graph.atomic_write(os.path.join(worker._tree_path(ask, root), "hyper", "wide.py"),
                       "# coincidentally named in an ADR, but no structured depth-decision\n"
                       + "x = 0\n" * (conditions.SIGNAL + 50))
    result = worker.apply(ask, scripted(json.dumps({
        "report": "grew a module merely mentioned in an ADR",
        "delta": delta_for("the substring hole stays closed"),
        "loop": {"command": "run", "red": "failed", "green": "passed"}})), root)
    ok(conditions.accepted("hyper/wide.py", conditions.SIGNAL + 51, root) is False,
       "a coincidental prose mention is not a structured depth-decision — the hole stays closed")
    ok(conditions.unmet(result, root) is not None,
       "the file mentioned only in prose still raises a depth decision — no free pass by spelling")
    worker.teardown(ask, root)

    # 4. the worker is grounded in the depth disciplines EVERY episode — the proactive defense
    # (re-grounding §3): the deep-module framework and the red flags are in its prompt by
    # construction, so it builds deep up front and the gate stays a rarely-tripped backstop.
    ask = staged("any worker episode", "the worker is grounded in depth")
    ctx = worker.context(ask, root)
    text = worker.prompt(ask, ctx)
    ok(all(s in text for s in ("DEEP MODULES", "RED FLAGS", "shallow module",
                               "COMPLEXITY DOWNWARD", "STRATEGIC")),
       "the worker's prompt carries the deep-module framework and the red flags by construction")
    worker.teardown(ask, root)

    # 5. the operator reads DEPTH, not merely length: the review renders length as a labeled
    # context-cost signal and records the deeper model-driven red-flag scan as not-yet-built —
    # the honest self-record (F1), not a fabricated verdict.
    rv = review.review(graph._DEFAULT_ROOT)
    line = " ".join(review.backlog(rv))
    ok("length signal" in line and "not yet built" in line,
       "the review names length as the signal and records the red-flag depth scan as not-yet-built")
    ok(review.DEPTH_NOT_YET in " ".join(review.backlog(rv)) or
       any(f.kind == "past the length signal" for f in rv.findings),
       "the depth lens beyond length is surfaced as not-yet-built, never fabricated")
