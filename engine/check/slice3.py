"""Slice 3 — intent extraction by grilling: the floor, the gate.

Acceptance (spec §9.3): a filed ask above the floor is grilled — its residual decisions
surface as questions one at a time, each with the machine's lean; the gate holds work
until the operator ratifies the view entry; the pass yields a foldable spec delta. A
below-floor ask files straight to standing work.
"""
from __future__ import annotations

import json

from .harness import ok, scripted


def check(root: str) -> None:
    from .. import delta, tree, grill, render, spec
    from ..communication import Thread, speak

    print("\nslice 3 — acceptance check  (intent extraction by grilling)\n")
    base = len(tree.standing())

    # an above-floor ask: the architect files, the floor finds two stakes
    t = Thread()
    r = speak(t, "set up the berserk download", scripted(
        '{"say":"Let me pin two things down first.","file":"download new Berserk '
        'episodes","done":false}',
        '{"questions":[{"q":"which quality tier?","lean":"1080p","flip":"a tight disk '
        'budget"},{"q":"keep seeding after?","lean":"yes, to ratio 2.0","flip":"a '
        'metered connection"}]}'))
    ok(r.filed is None and r.grilling is not None, "an above-floor ask is held, not filed")
    ok(len(tree.standing()) == base, "the gate holds: no standing work while grilling")
    qcards = [c for c in tree.cards() if grill.is_question(c)]
    ok(len(qcards) == 1, "one grilling question is on the queue at a time")
    ok(grill.lean_of(qcards[0]) == "1080p" and bool(grill.flip_of(qcards[0])),
       "the question card carries the machine's lean and what would flip it")
    ok(grill.card_kind(qcards[0]) == "grilling question"
       and render._card_label(qcards[0]) == "grilling question",
       "the render reads the card's kind from the one authority — a grilling question")

    # accept the lean on the first; the second surfaces, still gated
    grill.advance(qcards[0], grill.lean_of(qcards[0]))
    qcards = [c for c in tree.cards() if grill.is_question(c)]
    ok(len(qcards) == 1 and grill.question_of(qcards[0]).startswith("keep seeding"),
       "answering one question surfaces the next")
    ok(len(tree.standing()) == base, "the work stays gated through the interview")

    # answer the last in the operator's own words: the pass yields the entry + delta
    products = json.dumps({
        "entry": "A recurring pull of new Berserk episodes from nyaa at 1080p, "
                 "seeding to ratio 2.0.",
        "delta": ("## ADDED — communication\n"
                  "### Requirement: a download arc names its source\n"
                  "The arc MUST record where it pulls from.\n"
                  "#### Scenario: an arc is set up\n"
                  "- WHEN a download arc is filed\n- THEN its source is named")})
    entry = grill.advance(qcards[0], "no — delete it once I have watched it",
                          scripted(products))
    ok(grill.is_entry(entry) and "1080p" in grill.contract(entry),
       "the resolved pass raises the view entry — the contract to ratify")
    ok(grill.card_kind(entry) == "ratification",
       "a resolved grilling tree reads as a ratification — off the pass, not guessed")
    ok(len(tree.standing()) == base, "the gate holds until the entry is ratified")

    # the fourth product is a well-formed, foldable spec delta
    d = delta.parse("# delta — the pass's product\n\n" + grill.delta_of(entry))
    ok(not d.trivial and delta.check(d, spec.read_spec()) is None,
       "the pass's spec delta is well-formed and folds clean")

    # ratifying the view entry is the gate: the held ask spawns, the queue clears
    grill.ratify(entry)
    ok(len(tree.standing()) == base + 1, "ratifying the view entry spawns the work")
    ok(not [c for c in tree.cards() if c.parent],
       "ratifying clears the grilling pass from the queue")

    # a below-floor ask: the floor finds no residual stake, so it files straight through
    t2 = Thread()
    r2 = speak(t2, "downloads should land in /mnt/media", scripted(
        '{"say":"Noted and filed.","file":"downloads land in /mnt/media","done":true}',
        '{"questions":[]}'))
    ok(r2.filed is not None and r2.grilling is None, "a below-floor ask files directly")
    ok(len(tree.standing()) == base + 2, "the below-floor ask is standing work, ungrilled")

    # ── card kind: recorded on the node, read not guessed (card-kind) ──────────────────────
    # A decision card's kind is recorded; the render reads it through the one authority and speaks the
    # glossary word — "decision", not the raw stored "decide" the pre-fix render returned verbatim.
    dcard = tree.raise_card("a real fork the operator must reason through", kind="decide")
    ok(grill.card_kind(dcard) == "decision" and render._card_label(dcard) == "decision",
       "a decision card reads as 'decision' — the render reads the recorded kind, not the raw code")
    # all five kinds are representable: the three recorded kinds map to their glossary words, the two
    # pass-stage kinds (question, ratification) were read off the held tree above.
    acc = tree.raise_card("sign off the result meets its bar", kind="acceptance")
    rfa = tree.raise_card("a go on a planned step", kind="approval")
    ok(grill.card_kind(acc) == "acceptance" and grill.card_kind(rfa) == "request for approval",
       "the acceptance and request-for-approval kinds are representable, recorded on the node")
