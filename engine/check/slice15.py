"""Slice 15 — the mechanical red-flag scan: dead symbols and import cycles (ADR 0020).

Acceptance: the architecture review's standing scan now reads the mechanical structural red
flags a tool can read without judgment — module-level symbols referenced nowhere (dead code)
and import cycles (the circular-dependency signature of information leakage) — and surfaces them
in the operator-view gap, derived, never hand-authored. The model-driven *verdict* (shallow
module, leakage, the deletion test) stays judgment, still not built (ADR 0006), recorded not faked.

This slice is the first dogfood of hypercore's red→green discipline (no RESULT.md/delta.md had
ever existed): the scan went **red** on the live findings the coherence audit named — dead
`tree.PENDING` and the `communication↔grill` cycle — and **green** once they were cleared (the
symbol cut, the transport named so the cycle dissolves). Drives the real scan over the real tree
(the green half of the loop) and over a planted tree carrying one of each rule (proof the rules
detect, not just that the tree is clean).
"""
from __future__ import annotations

import os
import tempfile

from .harness import ok


def check(root: str) -> None:
    from .. import tree, review, view

    REAL = tree._DEFAULT_ROOT                              # hypercore's own source tree

    print("\nslice 15 — acceptance check  (the mechanical red-flag scan)\n")

    # 1. the rules detect — plant one of each in a scan tree; the scan names both, with no false
    # positive on a symbol that is actually used across the seam.
    scan = tempfile.mkdtemp(prefix="engine-redflag-")
    eng = os.path.join(scan, "engine")
    tree.atomic_write(os.path.join(eng, "api.py"), "def value():\n    return 1\n")
    tree.atomic_write(os.path.join(eng, "consumer.py"),
                       "from . import api\n\nORPHAN = 99            # bound, read by nobody\n\n\n"
                       "def use():\n    return api.value()\n")
    tree.atomic_write(os.path.join(eng, "ring_a.py"), "from . import ring_b\n\nA = 1\n")
    tree.atomic_write(os.path.join(eng, "ring_b.py"), "from . import ring_a\n\nB = 1\n")
    flags = review.red_flags(scan)
    dead = [f.subject for f in flags if f.rule == "dead symbol"]
    cycles = [f for f in flags if f.rule == "import cycle"]
    ok("consumer.ORPHAN" in dead,
       "the scan flags a module-level symbol referenced nowhere as a dead symbol")
    ok("api.value" not in dead,
       "a symbol used across the seam raises no dead-symbol flag (conservative, no false positive)")
    ok(any(set(c.subject.split(" ↔ ")) == {"ring_a", "ring_b"} for c in cycles),
       "the scan flags two modules that import each other as an import cycle")

    # 2. the green half of the audit's red→green loop: the real engine tree carries no mechanical
    # red flags — dead tree.PENDING cut, the communication↔grill cycle dissolved by naming the
    # transport. (This assertion was the recorded RED before those fixes landed.)
    real = review.red_flags(REAL)
    ok(not real, "the real engine tree carries no mechanical red flags "
       + (f"(found: {[f.subject for f in real]})" if real else "(clean)"))

    # 3. the red flags are the operator view's gap — derived from the scan, never hand-authored.
    rv = review.review(REAL)
    v = view.operator_view(root=REAL)
    for line in review.backlog(rv):
        ok(line in v.gap, "the scan's backlog is the operator view's gap — derived, not authored")
