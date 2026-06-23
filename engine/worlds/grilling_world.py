"""The grilling scenario world — the floor, the one-at-a-time interview, and the gate, driven through
the real `grill` over a seeded, isolated tree.

The verbs name grilling's domain nouns — an ask above or below the floor, the surfaced question and
its lean, the resolved entry, the delta, the spawn — never engine symbols, so a worker rewriting
`grill` has nothing in the scenario to tamper with to pass. The fixture seeds the real spec into an
isolated `ENGINE_ROOT` (so `grill`'s floor digest, the products' delta, and `delta.check` all read the
live capabilities exactly as in production) and drives the real `grill.consider` / `grill.advance` /
`grill.ratify` with a prompt-routing scripted transport: the floor prompt gets the residual questions
(two for an above-floor ask, none for a below-floor one), the products prompt gets the contract and a
foldable delta. The root and `ENGINE_ROOT` are restored and dropped on teardown.
"""
from __future__ import annotations

import json
import os
import shutil
import tempfile

from .. import delta, grill, render, spec, tree
from ..scenario import _git                                  # the worlds share the core's git helper
from . import World as _Base

_REAL = tree._DEFAULT_ROOT                                  # the real spec, seeded so the floor/products assemble as in production
_ASK = "download new Berserk episodes"
_FLOOR = json.dumps({"questions": [
    {"q": "which quality tier?", "lean": "1080p", "flip": "a tight disk budget"},
    {"q": "keep seeding after?", "lean": "yes, to ratio 2.0", "flip": "a metered connection"}]})
_PRODUCTS = json.dumps({
    "entry": "A recurring pull of new Berserk episodes from nyaa at 1080p, seeding to ratio 2.0.",
    "delta": ("## ADDED — communication\n### Requirement: a download arc names its source\n"
              "The arc MUST record where it pulls from.\n#### Scenario: an arc is set up\n"
              "- WHEN a download arc is filed\n- THEN its source is named")})


class World(_Base):
    """A scenario's fixture: an isolated, git-backed `ENGINE_ROOT` seeded with the real spec, the
    real `grill` run over it. `ask` runs the floor; `answer` advances the interview; the assertion
    verbs read the held tree's pass, the queue, and the produced delta."""

    def __init__(self):
        self._prev_root = os.environ.get("ENGINE_ROOT")
        self.root = tempfile.mkdtemp(prefix="scenario-grilling-")
        os.environ["ENGINE_ROOT"] = self.root              # the tree/spec seams read the ambient root; restored on teardown
        for cmd in (("init", "-q"), ("config", "user.email", "scenario@hypercore"),
                    ("config", "user.name", "scenario")):
            _git(self.root, *cmd)
        shutil.copytree(os.path.join(_REAL, "spec"), os.path.join(self.root, "spec"),
                        ignore=shutil.ignore_patterns("__pycache__"))
        _git(self.root, "add", "-A"); _git(self.root, "commit", "-qm", "base")
        self.node = None
        self.base_standing = 0

    @staticmethod
    def _transport(floor: str):
        """Route the floor prompt to its residual questions and the products prompt to the contract +
        delta — the one transport `consider` and `advance` both call."""
        return lambda prompt: _PRODUCTS if "grilling pass is resolved" in prompt else floor

    # ── fixture verbs ───────────────────────────────────────────────────────────
    def _v_ask(self, args: list[str]) -> tuple[bool, str]:
        """ask <above-floor|below-floor> — file an ask whose floor leaves a stake open (held and
        grilled) or leaves none (filed straight to standing work)."""
        self.base_standing = len(tree.standing())
        floor = _FLOOR if args[0] == "above-floor" else json.dumps({"questions": []})
        self.node, _ = grill.consider(_ASK, self._transport(floor))
        return True, ""

    def _v_answer(self, args: list[str]) -> tuple[bool, str]:
        """answer <lean|words> — settle the surfaced question by accepting its lean, or in the
        operator's own words; the pass surfaces the next question or, on the last, produces the
        contract and delta."""
        ans = grill.lean_of(self.node) if args[0] == "lean" else "no — delete it once I have watched it"
        self.node = grill.advance(self.node, ans, self._transport(_FLOOR))
        return True, ""

    # ── assertion verbs ─────────────────────────────────────────────────────────
    def _v_held(self, args: list[str]) -> tuple[bool, str]:
        """held grilled — the ask is held as its own tree with a running grilling pass."""
        if args[0] != "grilled":
            return False, f"unknown held assertion {args[0]!r}"
        return (True, "") if grill.is_question(self.node) else (False, "the ask is not held and grilled")

    def _v_filed(self, args: list[str]) -> tuple[bool, str]:
        """filed standing — the ask filed straight to standing work (no grilling pass)."""
        if args[0] != "standing":
            return False, f"unknown filed assertion {args[0]!r}"
        if grill.is_question(self.node) or grill.is_entry(self.node):
            return False, "the ask was grilled, not filed straight through"
        return ((True, "") if len(tree.standing()) == self.base_standing + 1
                else (False, "the below-floor ask is not standing work"))

    def _v_grilled(self, args: list[str]) -> tuple[bool, str]:
        """grilled none — no grilling pass exists for the ask."""
        if args[0] != "none":
            return False, f"unknown grilled assertion {args[0]!r}"
        return (True, "") if grill._load(self.node) is None else (False, "a grilling pass exists for the ask")

    def _v_standing(self, args: list[str]) -> tuple[bool, str]:
        """standing none — no standing work appeared while the ask is grilled (the gate holds)."""
        if args[0] != "none":
            return False, f"unknown standing assertion {args[0]!r}"
        now = len(tree.standing())
        return ((True, "") if now == self.base_standing
                else (False, f"standing work changed during grilling ({now} vs {self.base_standing})"))

    def _v_question(self, args: list[str]) -> tuple[bool, str]:
        """question <one|next> — exactly one grilling question on the queue, carrying a lean and a flip,
        its kind read as a grilling question; `next` is the question that surfaced after an answer."""
        qcards = [c for c in tree.cards() if grill.is_question(c)]
        if len(qcards) != 1:
            return False, f"expected exactly one grilling question on the queue, got {len(qcards)}"
        q = qcards[0]
        if not grill.lean_of(q) or not grill.flip_of(q):
            return False, "the question does not carry both a lean and a flip"
        if grill.card_kind(q) != "grilling question":
            return False, f"the card's kind is not a grilling question: {grill.card_kind(q)!r}"
        want = {"one": "which quality", "next": "keep seeding"}.get(args[0])
        if want and not grill.question_of(q).lower().startswith(want):
            return False, f"the surfaced question is not the {args[0]} one: {grill.question_of(q)!r}"
        return True, ""

    def _v_entry(self, args: list[str]) -> tuple[bool, str]:
        """entry raised — the resolved pass shows the contract as a ratification card carrying the
        resolved answers."""
        if args[0] != "raised":
            return False, f"unknown entry assertion {args[0]!r}"
        if not grill.is_entry(self.node):
            return False, "the pass did not resolve into an entry"
        if grill.card_kind(self.node) != "ratification":
            return False, f"the entry's kind is not a ratification: {grill.card_kind(self.node)!r}"
        return (True, "") if "1080p" in grill.contract(self.node) else (False, "the contract does not carry the resolved answer")

    def _v_delta(self, args: list[str]) -> tuple[bool, str]:
        """delta folds — the pass produced a well-formed spec delta that folds clean onto the spec."""
        if args[0] != "folds":
            return False, f"unknown delta assertion {args[0]!r}"
        d = delta.parse("# delta — the pass's product\n\n" + grill.delta_of(self.node))
        if d.trivial:
            return False, "the pass produced a trivial delta"
        reason = delta.check(d, spec.read_spec())
        return (True, "") if reason is None else (False, f"the delta does not fold clean: {reason}")

    def _v_ratify(self, args: list[str]) -> tuple[bool, str]:
        """ratify spawns — ratifying the entry spawns the work as standing and clears the pass from
        the queue (the gate opens here and only here)."""
        if args[0] != "spawns":
            return False, f"unknown ratify assertion {args[0]!r}"
        before = len(tree.standing())
        grill.ratify(self.node)
        if len(tree.standing()) != before + 1:
            return False, "ratifying did not spawn the work as standing"
        if [c for c in tree.cards() if c.parent]:
            return False, "ratifying did not clear the pass from the queue"
        return True, ""

    def teardown(self) -> None:
        if self._prev_root is None:
            os.environ.pop("ENGINE_ROOT", None)
        else:
            os.environ["ENGINE_ROOT"] = self._prev_root
        shutil.rmtree(self.root, ignore_errors=True)
