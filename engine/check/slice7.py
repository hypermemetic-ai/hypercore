"""Slice 7 — the architecture re-grounded in depth (Ousterhout): the standing review's depth lens.

This slice's worker-grounding half — the deep-module framework and the red flags in the worker's
prompt by construction — has migrated to `worker`'s own executable scenarios (`spec/worker.md`,
`engine/worlds/worker.py`); the gate / length-signal / accepted-length content migrated earlier to
`folding-conditions`. What stays here is the `architecture-review` surface, until that capability
migrates:

- **the operator reads DEPTH, not merely length** — the standing review renders length as a labeled
  context-cost signal and records the deeper model-driven red-flag scan as not-yet-built, honestly (an
  `architecture-review` concern; the F1 honest self-record, never a fabricated verdict).
"""
from __future__ import annotations

from .harness import ok


def check(root: str) -> None:
    from .. import review, tree

    print("\nslice 7 — acceptance check  (the depth re-grounding: the standing review's depth lens)\n")

    # the operator reads DEPTH, not merely length: the review renders length as a labeled
    # context-cost signal and records the deeper model-driven red-flag scan as not-yet-built —
    # the honest self-record (F1), not a fabricated verdict.
    rv = review.review(tree._DEFAULT_ROOT)
    line = " ".join(review.backlog(rv))
    ok("length signal" in line and "not yet built" in line,
       "the review names length as the signal and records the red-flag depth scan as not-yet-built")
    ok(review.DEPTH_NOT_YET in line or any(f.kind == "past the length signal" for f in rv.findings),
       "the depth lens beyond length is surfaced as not-yet-built, never fabricated")
