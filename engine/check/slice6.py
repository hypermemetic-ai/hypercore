"""Slice 6 — the architecture review render: the standing scan, the map, the backlog.

Acceptance (spec §9.6): the operator can read a current, honest, visual map of as-built
reality — vision beside as-built, debt marked — without reading code. The standing review
scans the source tree live, surfaces god-files-in-the-making before they set, and its output
is the operator view's upper levels (the structural map) and the deepening backlog (the gap).
Drives the real review over the real tree and a planted scan tree.
"""
from __future__ import annotations

import os
import tempfile

from .harness import ok


def check(root: str) -> None:
    from .. import conditions, graph, render, review, view

    REAL = graph._DEFAULT_ROOT                              # hypercore's own source tree

    print("\nslice 6 — acceptance check  (the architecture review render)\n")

    # 1. the review is a standing scan, read live off the real tree: every module measured.
    rv = review.review(REAL)
    ok(len(rv.modules) > 5 and all(m.lines > 0 for m in rv.modules),
       f"the review scans the source tree live ({len(rv.modules)} modules measured)")

    # 2. the real tree is honestly clean — the per-slice check split kept every module within
    # the length signal, so nothing is over (debt) or depth-accepted (the discipline on itself).
    ok(not any(m.status in ("over", "exceeded", "accepted") for m in rv.modules),
       "no module is past the length signal — the real tree is honestly clean (check.py split)")
    ok(not any(f.kind == "past the length signal" for f in rv.findings),
       "the deepening backlog carries no past-the-signal debt on the real tree")

    # 3. it surfaces a god-file-in-the-making before it sets: plant one in a scan tree, the
    # review flags it as a strong deepening opportunity; an in-budget sibling is left alone.
    scan = tempfile.mkdtemp(prefix="engine-review-")
    graph.atomic_write(os.path.join(scan, "engine", "giant.py"),
                       "# a shallow god-file\n" + "x = 0\n" * (conditions.SIGNAL + 60))
    graph.atomic_write(os.path.join(scan, "engine", "small.py"), "y = 1\n")
    planted = review.review(scan)
    big = next((f for f in planted.findings if f.subject.endswith("giant.py")), None)
    ok(big is not None and big.strength == "strong" and big.kind == "past the length signal",
       "the review surfaces a past-the-signal god-file as a strong deepening opportunity")
    ok(not any(f.subject.endswith("small.py") for f in planted.findings),
       "a module within the signal raises no finding")

    # 4. the depth-decision record — the same record folding-conditions consults: a structured
    # depth-decision naming the file clears it from the backlog, but the map still shows it.
    graph.atomic_write(os.path.join(scan, "spec", "decisions", "0099-giant.md"),
                       f"# ADR 0099\n\ndepth-decision: engine/giant.py accepted@{conditions.SIGNAL + 61} "
                       "— deep behind a small interface; its length is context-cost, not shallowness.\n")
    dec = review.review(scan)
    ok(not any(f.subject.endswith("giant.py") for f in dec.findings),
       "a file past the signal with a structured depth-decision accepting it is not debt")
    gm = next(m for m in dec.modules if m.rel.endswith("giant.py"))
    ok(gm.status == "accepted", "the structural map still shows the depth-accepted file, marked")

    # 5. the operator view's upper levels ARE the review's output — derived, not hand-authored.
    v = view.operator_view(root=REAL)
    ok(v.structure and any("█" in line for line in v.structure),
       "the operator view root renders the visual structural map from the review")
    for line in review.backlog(rv):
        ok(line in v.gap, "the deepening backlog is the operator view's gap — derived from the review")

    # 6. read without reading code: the map is styled spans, no TTY, the system's shape not source.
    rows = render.view_body(v, 0, 76)
    text = "".join(t for row in rows for t, _s in row)
    ok("operator view" in text and "█" in text and f"/{conditions.SIGNAL}" in text,
       "the operator reads a visual map of as-built reality against the length signal, no TTY")
    ok("import " not in text and "def " not in text,
       "the map shows the system's shape, not its source — read without reading code")
