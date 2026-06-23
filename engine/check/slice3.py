"""Slice 3 — residue: the card-kind seam, awaiting the queue/card-kind migration.

Grilling's own behavior — the floor (above and below), the one-question-at-a-time interview, and the
resolved pass yielding the contract and a foldable delta — has migrated to `grilling`'s own executable
scenarios (`spec/grilling.md`, `engine/worlds/grilling_world.py`).

What stays is the **card-kind** seam: a decision card's kind is recorded on the node and read through
the one authority (`grill.card_kind`), which the render speaks as the glossary word — "decision", not
the raw stored "decide" — and all five kinds are representable. This is not grilling's own behavior; it
is the queue's card-kind concern (`card-kind`, folded 2026-06), surfaced here. It stays by-slice until
the queue/card-kind capability is migrated, at which point this file dissolves like the others.
"""
from __future__ import annotations

from .harness import ok


def check(root: str) -> None:
    from .. import tree, grill, render

    print("\nslice 3 — acceptance check  (residue: the card-kind seam)\n")

    # A decision card's kind is recorded; the render reads it through the one authority and speaks the
    # glossary word — "decision", not the raw stored "decide" the pre-fix render returned verbatim.
    dcard = tree.raise_card("a real fork the operator must reason through", kind="decide")
    ok(grill.card_kind(dcard) == "decision" and render._card_label(dcard) == "decision",
       "a decision card reads as 'decision' — the render reads the recorded kind, not the raw code")
    # all five kinds are representable: the three recorded kinds map to their glossary words, the two
    # pass-stage kinds (grilling question, ratification) are read off a held grilling tree (now gated in
    # spec/grilling.md's scenarios).
    acc = tree.raise_card("sign off the result meets its bar", kind="acceptance")
    rfa = tree.raise_card("a go on a planned step", kind="approval")
    ok(grill.card_kind(acc) == "acceptance" and grill.card_kind(rfa) == "request for approval",
       "the acceptance and request-for-approval kinds are representable, recorded on the node")
