"""Slice 7 — the architecture re-grounded in depth (Ousterhout).

Acceptance: the constraints read in Ousterhout's
terms (deep modules, the red flags); the mechanical gate and the standing review reflect them;
**the operator reads the system's depth, not merely its length**; and the slice-6 check.py split
is re-decided on the new criteria (kept, on locality). This check drives the
re-grounded gate, review, and worker grounding deterministically, and pins the two properties
that distinguish the re-grounding from slice 5's budget:

1. length **never auto-refuses** — even far past the signal it raises a *decision* the operator
   can accept (F2: no hard ceiling); and
2. the justification hole is **closed by construction** — only a *structured* accepted-length
   record clears the gate, never a coincidental mention (the old substring hole).
"""
from __future__ import annotations

import json
import os

from .harness import LOOP, ok, scripted


def check(root: str) -> None:
    from .. import conditions, communication, tree, review, spec, worker

    print("\nslice 7 — acceptance check  (the architecture re-grounded in depth)\n")

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

    def longfile(fence: str, name: str, lines: int) -> None:
        tree.atomic_write(os.path.join(fence, "engine", name),
                           "# a long module\n" + "x = 0\n" * lines)

    def decide(body: str):
        # the gate's source is engine/accepted-lengths.md; append so plants accumulate
        f = os.path.join(root, "engine", "accepted-lengths.md")
        prior = open(f, encoding="utf-8").read() if os.path.isfile(f) else ""
        tree.atomic_write(f, prior + body)

    # 1. length raises a DECISION, never a silent veto — and the reason names the three
    # outcomes (re-cut / deepen / accept). The gate hands the operator a depth judgment, not a
    # number's verdict (spec/folding-conditions, spec/communication-as-architect).
    # (A file with no accepted-length record of its own — names are unique so a sibling slice's
    # record can't clear it.)
    ask = staged("a change past the signal", "a decision is raised")
    longfile(worker._tree_path(ask, root), "tall.py", conditions.SIGNAL + 50)
    result = worker.apply(ask, scripted(json.dumps({
        "report": "grew a long module",
        "delta": delta_for("a decision is raised"),
        "loop": LOOP})), root)
    blocked = conditions.unmet(result, root)
    ok(blocked is not None and "decision" in blocked
       and all(w in blocked for w in ("re-cut", "deepen", "accept")),
       "length past the signal raises a decision naming re-cut / deepen / accept")
    ok(blocked is not None and "context-cost signal" in blocked and "not a verdict on depth" in blocked,
       "the gate frames length as a context-cost signal, not a verdict on depth — the operator judges")
    reply = communication.integrate(ask, result, coherent(), root)
    ok(reply.card is not None and reply.card.kind == "decide" and not reply.done,
       "the architect raises the decision on the queue — never a silent veto or pass")
    worker.teardown(ask, root)

    # 2. NO hard auto-refusing ceiling (F2): a file FAR past the signal — pathological length —
    # still only raises a decision, and an accepted-length record accepting it lets it fold.
    # No number refuses outright; judgment + the operator-decision carry the whole range.
    decide(f"accepted: engine/huge.py @{conditions.SIGNAL * 6 + 1} — "
           "generated table, deep behind a three-call interface; length is context-cost, not "
           "shallowness.\n")
    ask = staged("a pathologically long but accepted module", "a far-past-signal module folds")
    longfile(worker._tree_path(ask, root), "huge.py", conditions.SIGNAL * 6)   # ~6× the signal
    result = worker.apply(ask, scripted(json.dumps({
        "report": "grew a very long but accepted-length module",
        "delta": delta_for("a far-past-signal module folds"),
        "loop": LOOP})), root)
    ok(conditions.unmet(result, root) is None,
       "even ~6× the signal does not auto-refuse — an accepted-length record lets it fold (F2)")
    reply = communication.integrate(ask, result, coherent(), root)
    ok(reply.done and req("a far-past-signal module folds") is not None,
       "length has no hard ceiling: judgment + the operator-decision carry the whole range")
    worker.teardown(ask, root)

    # 3. THE HOLE CLOSED BY CONSTRUCTION: a coincidental mention of the file in record prose —
    # the old loose-substring escape — does NOT clear the gate. Only the structured
    # `accepted: <path> @<N>` record does. This is the regression the re-grounding adds.
    decide("We discussed engine/wide.py at length; it is over the old budget but "
           "the team is fine with it.\n")                                # prose only — no structured record
    ask = staged("a change naming the file only in prose", "the substring hole stays closed")
    tree.atomic_write(os.path.join(worker._tree_path(ask, root), "engine", "wide.py"),
                       "# coincidentally named in a record's prose, but no accepted-length record\n"
                       + "x = 0\n" * (conditions.SIGNAL + 50))
    result = worker.apply(ask, scripted(json.dumps({
        "report": "grew a module merely mentioned in a record's prose",
        "delta": delta_for("the substring hole stays closed"),
        "loop": LOOP})), root)
    ok(conditions.accepted("engine/wide.py", conditions.SIGNAL + 51, root) is False,
       "a coincidental prose mention is not an accepted-length record — the hole stays closed")
    ok(conditions.unmet(result, root) is not None,
       "the file mentioned only in prose still raises a decision — no free pass by spelling")
    worker.teardown(ask, root)

    # 4. the worker is grounded in the depth standards EVERY episode — the proactive defense:
    # the deep-module framework and the red flags are in its prompt by
    # construction, so it builds deep up front and the gate stays a rarely-tripped backstop.
    ask = staged("any worker episode", "the worker is grounded in depth")
    ctx = worker.context(ask, root)
    text = worker.prompt(ask, ctx)
    ok(all(s in text for s in ("deep modules", "downward", "strategic", "red flags", "shallow module")),
       "the worker's prompt carries the deep-module framework and the red flags by construction")
    worker.teardown(ask, root)

    # 5. the operator reads DEPTH, not merely length: the review renders length as a labeled
    # context-cost signal and records the deeper model-driven red-flag scan as not-yet-built —
    # the honest self-record (F1), not a fabricated verdict.
    rv = review.review(tree._DEFAULT_ROOT)
    line = " ".join(review.backlog(rv))
    ok("length signal" in line and "not yet built" in line,
       "the review names length as the signal and records the red-flag depth scan as not-yet-built")
    ok(review.DEPTH_NOT_YET in " ".join(review.backlog(rv)) or
       any(f.kind == "past the length signal" for f in rv.findings),
       "the depth lens beyond length is surfaced as not-yet-built, never fabricated")
