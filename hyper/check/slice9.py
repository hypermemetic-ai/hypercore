"""Slice 9 — the accepted-length ratchet: acceptance is bounded, and ratchets.

Acceptance (ADR 0008): a structured depth-decision that accepts a file no
longer silences it forever. The acceptance is **bounded to the length it names** and **ratchets**:
it clears the gate only while the file stays within that bar (plus a materiality margin), renewed
growth past it re-opens the depth decision, and renewing the acceptance at the new length raises
the bar. A bare `accepted` with no stated length clears nothing. The standing review tells a
*stale* acceptance (a file that outgrew its bar) apart from a never-decided over-signal file.

This drives the real conditions predicate, a real gate round-trip over a worktree, and the real
review over a planted scan tree — pinning the four properties that define the ratchet:

1. **bounded** — within the bar (+ margin) clears; materially past it does not;
2. **ratchets, and shrink-safe** — a shrink never lowers the bar, renewal raises it, the highest
   recorded bar governs;
3. **a bare acceptance names no bound** — it does not clear the gate (the slice-7 closure, applied
   to the length);
4. **the review distinguishes exceeded from over from accepted** — a stale acceptance returns to
   the backlog, marked as having outgrown its bar.
"""
from __future__ import annotations

import json
import os
import tempfile

from .harness import ok, scripted


def check(root: str) -> None:
    from .. import conditions, conversation, graph, review, spec, worker

    print("\nslice 9 — acceptance check  (the accepted-length ratchet)\n")

    SLACK = conditions.SLACK
    margin = lambda bar: round(bar * SLACK)

    def decide(name: str, body: str) -> None:
        graph.atomic_write(os.path.join(spec.spec_dir(root), "decisions", name), body)

    # ── 1. acceptance is BOUNDED to the length it names ───────────────────────────────────
    # A depth-decision accepts hyper/ratchet.py at 450 lines. It clears the gate within the bar
    # plus the materiality margin, and stops clearing once the file grows materially past it —
    # the hole (unbounded acceptance) closed.
    BAR = 450
    decide("0103-ratchet.md",
           f"# ADR 0103\n\ndepth-decision: hyper/ratchet.py accepted@{BAR} — deep behind a small "
           "interface; its length is context-cost, not shallowness.\n")
    ok(conditions.accepted_at("hyper/ratchet.py", root) == BAR,
       f"the structured record names the accepted length — accepted_at reads it as {BAR}")
    ok(conditions.accepted("hyper/ratchet.py", BAR, root) is True
       and conditions.accepted("hyper/ratchet.py", BAR + margin(BAR), root) is True,
       "within the bar plus the materiality margin, the acceptance clears the gate")
    ok(conditions.accepted("hyper/ratchet.py", BAR + margin(BAR) + 5, root) is False,
       "materially past the bar, the acceptance no longer clears — acceptance is not unbounded")

    # ── 2. a stable or shrinking file stays cleared; the bar RATCHETS up on renewal ────────
    ok(conditions.accepted("hyper/ratchet.py", 300, root) is True,
       "a shrunk file stays cleared — the bar lives in the record, a shrink never lowers it")
    # renewing the acceptance at a higher length raises the bar; the highest recorded bar governs.
    HIGHER = 600
    ok(conditions.accepted("hyper/ratchet.py", HIGHER - 20, root) is False,
       "before renewal, a length near the higher bar does not clear")
    decide("0104-ratchet-renewed.md",
           f"# ADR 0104\n\ndepth-decision: hyper/ratchet.py accepted@{HIGHER} — renewed at the "
           "grown size after a deepening pass kept it deep.\n")
    ok(conditions.accepted_at("hyper/ratchet.py", root) == HIGHER,
       "the highest recorded bar governs — the ratchet only rises")
    ok(conditions.accepted("hyper/ratchet.py", HIGHER - 20, root) is True,
       "after renewal at the new length, the higher bar clears what the old one did not")

    # ── 3. a BARE acceptance names no bound — it does not clear the gate ───────────────────
    decide("0105-bare.md",
           "# ADR 0105\n\ndepth-decision: hyper/bare.py accepted — we are fine with its size.\n")
    ok(conditions.accepted_at("hyper/bare.py", root) is None,
       "a bare `accepted` names no length — accepted_at finds no bar")
    ok(conditions.accepted("hyper/bare.py", conditions.SIGNAL + 10, root) is False,
       "a bare acceptance clears nothing — the exception is the decision at a stated size")

    # ── 4. the gate end to end: a file grown past its bar re-raises the depth decision ─────
    cap = "folding-conditions"
    def delta_for(name: str) -> str:
        return (f"## ADDED — {cap}\n### Requirement: {name}\nThe gate MUST hold.\n"
                f"#### Scenario: s\n- WHEN a fold is attempted\n- THEN the gate runs\n")

    def staged(text: str, name: str) -> graph.Node:
        ask = graph.file_intent(text)
        graph.approve(graph.raise_card("contract.\n\ndelta:\n" + delta_for(name),
                                       kind="decide", parent=ask.id))
        worker.worktree(ask, root)
        graph.delegate(ask)
        return ask

    GROWN_BAR = conditions.SIGNAL + 10
    decide("0106-grown.md",
           f"# ADR 0106\n\ndepth-decision: hyper/grown.py accepted@{GROWN_BAR} — accepted when it "
           "was barely over; deep behind its interface.\n")
    ask = staged("a graph that grows a once-accepted file far past its bar", "the ratchet re-fires")
    tree = worker._tree_path(ask, root)
    grown_n = conditions.SIGNAL * 2
    graph.atomic_write(os.path.join(tree, "hyper", "grown.py"),
                       "# once accepted small, since grown\n" + "x = 0\n" * (grown_n - 1))
    result = worker.apply(ask, scripted(json.dumps({
        "report": "grew a once-accepted file far past its accepted bar",
        "delta": delta_for("the ratchet re-fires"),
        "loop": {"command": "run", "red": "failed", "green": "passed"}})), root)
    blocked = conditions.unmet(result, root)
    ok(blocked is not None and "materially past" in blocked and str(GROWN_BAR) in blocked,
       "a file grown materially past its accepted bar re-raises the depth decision, naming the bar")
    ok(blocked is not None and "stale" in blocked and "ratchet" in blocked,
       "the gate frames the old acceptance as stale and ratcheting — not a silent pass on growth")
    reply = conversation.integrate(ask, result, scripted(
        json.dumps({"coherent": True, "say": "held.", "card": None})), root)
    ok(reply.card is not None and reply.card.kind == "decide" and not reply.done,
       "the architect raises the re-opened decision on the queue — the fold is held, not silenced")
    # renewing the acceptance at the new length clears the same material — the ratchet, completed.
    decide("0107-grown-renewed.md",
           f"# ADR 0107\n\ndepth-decision: hyper/grown.py accepted@{grown_n} — renewed at the new "
           "length; re-judged deep at this size.\n")
    ok(conditions.unmet(result, root) is None,
       "renewing the acceptance at the grown length lets the same file fold — the bar ratcheted up")
    worker.teardown(ask, root)

    # ── 5. the review distinguishes EXCEEDED from over from accepted ──────────────────────
    scan = tempfile.mkdtemp(prefix="hyper-ratchet-")
    N = conditions.SIGNAL + 100                               # one over-signal length, three fates
    for name in ("over", "exceeded", "accepted"):
        graph.atomic_write(os.path.join(scan, "hyper", f"{name}.py"), "x = 0\n" * N)
    LOW, HIGH = conditions.SIGNAL + 10, conditions.SIGNAL + 200   # below N+margin; above N
    graph.atomic_write(os.path.join(scan, "spec", "decisions", "0001-exceeded.md"),
                       f"# ADR\n\ndepth-decision: hyper/exceeded.py accepted@{LOW} — accepted small, "
                       "since outgrown.\n")
    graph.atomic_write(os.path.join(scan, "spec", "decisions", "0002-accepted.md"),
                       f"# ADR\n\ndepth-decision: hyper/accepted.py accepted@{HIGH} — deep; within "
                       "the accepted length.\n")
    rv = review.review(scan)
    by = {m.rel: m for m in rv.modules}
    ok(by["over.py"].status == "over" and by["over.py"].bar is None,
       "a never-decided over-signal file is `over` — no accepted bar")
    ok(by["exceeded.py"].status == "exceeded" and by["exceeded.py"].bar == LOW,
       "a file grown past a lower accepted bar is `exceeded`, carrying the stale bar it outgrew")
    ok(by["accepted.py"].status == "accepted" and by["accepted.py"].bar == HIGH,
       "a file within its accepted length is `accepted`, carrying its bar")

    subjects = {f.subject: f for f in rv.findings}
    ok("over.py" in subjects and "exceeded.py" in subjects and "accepted.py" not in subjects,
       "over and exceeded are deepening opportunities; the still-accepted file is not debt")
    exc = subjects["exceeded.py"]
    ok(str(LOW) in exc.note and "stale" in exc.note and exc.kind == "past its accepted bar",
       "the exceeded finding names the stale bar — a settled-then-grown decision, re-opened")
    mark = "".join(review.bars(rv))
    ok("grew past its accepted bar" in mark and "decision re-opened" in mark,
       "the structural map marks the exceeded file distinctly from a never-decided over file")
