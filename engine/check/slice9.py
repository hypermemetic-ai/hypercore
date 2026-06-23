"""Slice 9 — the accepted-length ratchet: acceptance is bounded, and ratchets.

Acceptance: an accepted-length record that accepts a file no
longer silences it forever. The acceptance is **bounded to the length it names** and **ratchets**:
it clears the gate only while the file stays within that bar (plus a materiality margin), renewed
growth past it re-opens the decision, and renewing the acceptance at the new length raises
the bar. An acceptance with no stated length (no `@<N>`) clears nothing. The standing review tells a
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
5. **the durable home and the one writer** (accepted-length-home) — the record lives at
   `engine/accepted-lengths.md`, beside its reader and apart from any node, written through the one
   `conditions.accept` seam: a record at the retired repo-root home is dead, the writer ratchets.
"""
from __future__ import annotations

import json
import os
import tempfile

from .harness import LOOP, ok, scripted


def check(root: str) -> None:
    from .. import conditions, communication, tree, review, worker

    print("\nslice 9 — acceptance check  (the accepted-length ratchet)\n")

    SLACK = conditions.SLACK
    margin = lambda bar: round(bar * SLACK)

    def decide(body: str) -> None:
        # the gate's source is engine/accepted-lengths.md; append so plants accumulate
        f = os.path.join(root, "engine", "accepted-lengths.md")
        prior = open(f, encoding="utf-8").read() if os.path.isfile(f) else ""
        tree.atomic_write(f, prior + body)

    # ── 1. acceptance is BOUNDED to the length it names ───────────────────────────────────
    # An accepted-length record accepts engine/ratchet.py at 450 lines. It clears the gate within the bar
    # plus the materiality margin, and stops clearing once the file grows materially past it —
    # the hole (unbounded acceptance) closed.
    BAR = 450
    decide(f"accepted: engine/ratchet.py @{BAR} — deep behind a small "
           "interface; its length is context-cost, not shallowness.\n")
    ok(conditions.accepted_at("engine/ratchet.py", root) == BAR,
       f"the structured record names the accepted length — accepted_at reads it as {BAR}")
    ok(conditions.accepted("engine/ratchet.py", BAR, root) is True
       and conditions.accepted("engine/ratchet.py", BAR + margin(BAR), root) is True,
       "within the bar plus the materiality margin, the acceptance clears the gate")
    ok(conditions.accepted("engine/ratchet.py", BAR + margin(BAR) + 5, root) is False,
       "materially past the bar, the acceptance no longer clears — acceptance is not unbounded")

    # ── 2. a stable or shrinking file stays cleared; the bar RATCHETS up on renewal ────────
    ok(conditions.accepted("engine/ratchet.py", 300, root) is True,
       "a shrunk file stays cleared — the bar lives in the record, a shrink never lowers it")
    # renewing the acceptance at a higher length raises the bar; the highest recorded bar governs.
    HIGHER = 600
    ok(conditions.accepted("engine/ratchet.py", HIGHER - 20, root) is False,
       "before renewal, a length near the higher bar does not clear")
    decide(f"accepted: engine/ratchet.py @{HIGHER} — renewed at the "
           "grown size after a deepening pass kept it deep.\n")
    ok(conditions.accepted_at("engine/ratchet.py", root) == HIGHER,
       "the highest recorded bar governs — the ratchet only rises")
    ok(conditions.accepted("engine/ratchet.py", HIGHER - 20, root) is True,
       "after renewal at the new length, the higher bar clears what the old one did not")

    # ── 3. a BARE acceptance names no bound — it does not clear the gate ───────────────────
    decide("accepted: engine/bare.py — we are fine with its size.\n")
    ok(conditions.accepted_at("engine/bare.py", root) is None,
       "an acceptance with no `@<N>` names no length — accepted_at finds no bar")
    ok(conditions.accepted("engine/bare.py", conditions.SIGNAL + 10, root) is False,
       "a bare acceptance clears nothing — the exception is the decision at a stated size")

    # ── 4. the gate end to end: a file grown past its bar re-raises the decision ─────
    cap = "folding-conditions"
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

    GROWN_BAR = conditions.SIGNAL + 10
    decide(f"accepted: engine/grown.py @{GROWN_BAR} — accepted when it "
           "was barely over; deep behind its interface.\n")
    ask = staged("a tree that grows a once-accepted file far past its bar", "the ratchet re-fires")
    fence = worker._tree_path(ask, root)
    grown_n = conditions.SIGNAL * 2
    tree.atomic_write(os.path.join(fence, "engine", "grown.py"),
                       "# once accepted small, since grown\n" + "x = 0\n" * (grown_n - 1))
    result = worker.apply(ask, scripted(json.dumps({
        "report": "grew a once-accepted file far past its accepted bar",
        "delta": delta_for("the ratchet re-fires"),
        "loop": LOOP})), root)
    blocked = conditions.unmet(result, root)
    ok(blocked is not None and "materially past" in blocked and str(GROWN_BAR) in blocked,
       "a file grown materially past its accepted bar re-raises the decision, naming the bar")
    ok(blocked is not None and "stale" in blocked and "ratchet" in blocked,
       "the gate frames the old acceptance as stale and ratcheting — not a silent pass on growth")
    reply = communication.integrate(ask, result, scripted(
        json.dumps({"coherent": True, "say": "held.", "card": None})), root)
    ok(reply.card is not None and reply.card.kind == "decide" and not reply.done,
       "the architect raises the re-opened decision on the queue — the fold is held, not silenced")
    # renewing the acceptance at the new length clears the same material — the ratchet, completed.
    decide(f"accepted: engine/grown.py @{grown_n} — renewed at the new "
           "length; re-judged deep at this size.\n")
    ok(conditions.unmet(result, root) is None,
       "renewing the acceptance at the grown length lets the same file fold — the bar ratcheted up")
    worker.teardown(ask, root)

    # ── 5. the review distinguishes EXCEEDED from over from accepted ──────────────────────
    scan = tempfile.mkdtemp(prefix="engine-ratchet-")
    N = conditions.SIGNAL + 100                               # one over-signal length, three fates
    for name in ("over", "exceeded", "accepted"):
        tree.atomic_write(os.path.join(scan, "engine", f"{name}.py"), "x = 0\n" * N)
    LOW, HIGH = conditions.SIGNAL + 10, conditions.SIGNAL + 200   # below N+margin; above N
    # both records live in the one engine/accepted-lengths.md the gate and the review read
    tree.atomic_write(os.path.join(scan, "engine", "accepted-lengths.md"),
                       f"accepted: engine/exceeded.py @{LOW} — accepted small, since outgrown.\n"
                       f"accepted: engine/accepted.py @{HIGH} — deep; within the accepted length.\n")
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
       "over and exceeded are complexity debt; the still-accepted file is not debt")
    exc = subjects["exceeded.py"]
    ok(str(LOW) in exc.note and "stale" in exc.note and exc.kind == "past its accepted bar",
       "the exceeded finding names the stale bar — a settled-then-grown decision, re-opened")
    mark = "".join(review.bars(rv))
    ok("grew past its accepted bar" in mark and "decision re-opened" in mark,
       "the structural map marks the exceeded file distinctly from a never-decided over file")

    # ── 6. the durable home and the one writer (accepted-length-home) ─────────────────────
    # The record's home is engine/accepted-lengths.md, beside its reader — not the repo root — and the
    # one writer is conditions.accept. RED→GREEN on the relocation: a record at the retired repo-root
    # home is dead; the gate reads the engine/ home the writer lands in.
    REL = "engine/relocated.py"
    tree.atomic_write(os.path.join(root, "accepted-lengths.md"),
                       f"accepted: {REL} @{conditions.SIGNAL + 50} — at the retired repo-root home.\n")
    ok(conditions.accepted_at(REL, root) is None,
       "a record at the retired repo-root home is not read — the home moved to engine/")
    BAR6 = conditions.SIGNAL + 120
    ok(conditions.accept(REL, BAR6, "deep behind a small interface", root) is True
       and conditions.accepted_at(REL, root) == BAR6,
       "conditions.accept writes the record the reader honors — one seam over one durable store")
    ok(os.path.isfile(os.path.join(root, "engine", "accepted-lengths.md")),
       "the durable store is engine/accepted-lengths.md — beside its reader, apart from any node")
    ok(conditions.accept(REL, BAR6, "again", root) is False
       and conditions.accept(REL, BAR6 - 10, "lower", root) is False,
       "re-accepting at the same or a lower length writes nothing — the bar only rises (idempotent)")
    ok(conditions.accept(REL, BAR6 + 80, "renewed deeper", root) is True
       and conditions.accepted_at(REL, root) == BAR6 + 80,
       "re-accepting at a higher length ratchets the bar up")
