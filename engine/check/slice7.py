"""Slice 7 — the architecture re-grounded in depth (Ousterhout): the worker grounding and the review.

The gate, the length signal, and the accepted-length record this slice once also drove have migrated
to `folding-conditions`' own executable scenarios (`engine/check/scenarios.py`,
`spec/folding-conditions.md`). What stays here is the re-grounding's other-capability surface, untouched
by that migration:

1. **the worker is grounded in the depth standards every episode** — the deep-module framework and the
   red flags are in its prompt by construction (the proactive defense, a `worker` concern);
2. **the operator reads depth, not merely length** — the standing review renders length as a labeled
   context-cost signal and records the deeper model-driven red-flag scan as not-yet-built, honestly (an
   `architecture-review` concern).
"""
from __future__ import annotations

from .harness import ok


def check(root: str) -> None:
    from .. import tree, review, worker

    print("\nslice 7 — acceptance check  (the depth re-grounding: worker grounding + the review)\n")

    def staged(text: str) -> tree.Node:
        ask = tree.file_intent(text)
        tree.approve(tree.raise_card("contract.", kind="decide", parent=ask.id))
        worker.worktree(ask, root)
        tree.dispatch(ask)
        return ask

    # 1. the worker is grounded in the depth standards EVERY episode — the proactive defense: the
    # deep-module framework and the red flags are in its prompt by construction, so it builds deep up
    # front and the gate stays a rarely-tripped backstop.
    ask = staged("any worker episode")
    text = worker.prompt(ask, worker.context(ask, root))
    ok(all(s in text for s in ("deep modules", "downward", "strategic", "red flags", "shallow module")),
       "the worker's prompt carries the deep-module framework and the red flags by construction")
    worker.teardown(ask, root)

    # 2. the operator reads DEPTH, not merely length: the review renders length as a labeled
    # context-cost signal and records the deeper model-driven red-flag scan as not-yet-built —
    # the honest self-record (F1), not a fabricated verdict.
    rv = review.review(tree._DEFAULT_ROOT)
    line = " ".join(review.backlog(rv))
    ok("length signal" in line and "not yet built" in line,
       "the review names length as the signal and records the red-flag depth scan as not-yet-built")
    ok(review.DEPTH_NOT_YET in line or any(f.kind == "past the length signal" for f in rv.findings),
       "the depth lens beyond length is surfaced as not-yet-built, never fabricated")
