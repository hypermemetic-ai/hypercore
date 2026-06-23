"""Slice 9 — the standing review distinguishes a stale acceptance from a never-decided over file.

The accepted-length ratchet this slice once drove — bounded acceptance, the durable single-writer
store, the length-acceptance producer — has migrated to `folding-conditions`' own executable scenarios
(`engine/check/scenarios.py`, `spec/folding-conditions.md`). What stays here is the
`architecture-review` surface over the same record: the standing scan tells a *stale* acceptance (a
file that outgrew its bar) apart from a never-decided over-signal file and a still-accepted one, marking
the exceeded file as a re-opened decision. It will migrate to architecture-review's own scenarios when
that capability is migrated; for now it is driven by-slice against a planted scan tree.
"""
from __future__ import annotations

import os
import tempfile

from .harness import ok


def check(root: str) -> None:
    from .. import conditions, tree, review

    print("\nslice 9 — acceptance check  (the review distinguishes exceeded / over / accepted)\n")

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
