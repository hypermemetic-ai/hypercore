"""Slice 6 — the architecture review render: the standing scan, the map, the backlog.

Acceptance (spec §9.6): the operator can read a current, honest, visual map of as-built
reality — vision beside as-built, debt marked — without reading code. The standing review
scans the source tree live, surfaces god-files-in-the-making before they set, and its output
is the operator view's upper levels (the structural map) and the complexity debt (the gap).
Drives the real review over the real tree and a planted scan tree.
"""
from __future__ import annotations

import os
import tempfile

from .harness import ok


def check(root: str) -> None:
    from .. import conditions, tree, render, review, view

    REAL = tree._DEFAULT_ROOT                              # hypercore's own source tree

    print("\nslice 6 — acceptance check  (the architecture review render)\n")

    # 1. the review is a standing scan, read live off the real tree: every module measured.
    rv = review.review(REAL)
    ok(len(rv.modules) > 5 and all(m.lines > 0 for m in rv.modules),
       f"the review scans the source tree live ({len(rv.modules)} modules measured)")

    # 2. the real tree is honestly clean — the per-slice check split kept every module within
    # the length signal, so nothing is over (debt) or accepted (the standard on itself).
    ok(not any(m.status in ("over", "exceeded", "accepted") for m in rv.modules),
       "no module is past the length signal — the real tree is honestly clean (check.py split)")
    ok(not any(f.kind == "past the length signal" for f in rv.findings),
       "the complexity debt carries no past-the-signal debt on the real tree")

    # 3. it surfaces a god-file-in-the-making before it sets: plant one in a scan tree, the
    # review flags it as a strong complexity-debt finding; an in-budget sibling is left alone.
    scan = tempfile.mkdtemp(prefix="engine-review-")
    tree.atomic_write(os.path.join(scan, "engine", "giant.py"),
                       "# a shallow god-file\n" + "x = 0\n" * (conditions.SIGNAL + 60))
    tree.atomic_write(os.path.join(scan, "engine", "small.py"), "y = 1\n")
    planted = review.review(scan)
    big = next((f for f in planted.findings if f.subject.endswith("giant.py")), None)
    ok(big is not None and big.strength == "strong" and big.kind == "past the length signal",
       "the review surfaces a past-the-signal god-file as a strong complexity-debt finding")
    ok(not any(f.subject.endswith("small.py") for f in planted.findings),
       "a module within the signal raises no finding")

    # 4. the accepted-length record — the same record folding-conditions consults: an
    # accepted-length record naming the file clears it from the backlog, but the map still shows it.
    tree.atomic_write(os.path.join(scan, "spec", "decisions", "0099-giant.md"),
                       f"# ADR 0099\n\naccepted: engine/giant.py @{conditions.SIGNAL + 61} "
                       "— deep behind a small interface; its length is context-cost, not shallowness.\n")
    dec = review.review(scan)
    ok(not any(f.subject.endswith("giant.py") for f in dec.findings),
       "a file past the signal with an accepted-length record accepting it is not debt")
    gm = next(m for m in dec.modules if m.rel.endswith("giant.py"))
    ok(gm.status == "accepted", "the structural map still shows the accepted file, marked")

    # 5. the operator view's upper levels ARE the review's output — derived, not hand-authored.
    v = view.operator_view(root=REAL)
    ok(v.structure and any("█" in line for line in v.structure),
       "the operator view root renders the visual structural map from the review")
    for line in review.backlog(rv):
        ok(line in v.gap, "the complexity debt is the operator view's gap — derived from the review")

    # 6. read without reading code: the map is styled spans, no TTY, the system's shape not source.
    rows = render.view_body(v, 0, 76)
    text = "".join(t for row in rows for t, _s in row)
    ok("operator view" in text and "█" in text and f"/{conditions.SIGNAL}" in text,
       "the operator reads a visual map of as-built reality against the length signal, no TTY")
    ok("import " not in text and "def " not in text,
       "the map shows the system's shape, not its source — read without reading code")
