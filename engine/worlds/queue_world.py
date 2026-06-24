"""The queue scenario world — the decision surface driven through the real `tree` settle path,
`grill.card_kind`, `communication.explain`, and `conditions.accept_length` over an isolated tree.

The verbs name the queue's domain nouns — a card on the surface, its recorded kind, the three
endorsements (approve / cut / explain), a surfaced grilling question and its lean/flip, the
ratification gate, the accept-the-length act — never engine symbols, so a worker rewriting the queue
has nothing in the scenario to tamper with to pass. The fixture seeds an isolated `ENGINE_ROOT` git
repo (so `tree.raise_card`, the queue view, the fold, and the accepted-length record assemble exactly
as in production) and drives the real seams with a prompt-shaped scripted transport where a turn needs
the model: a grilling floor returns one canned question, the products call returns a canned contract,
and explain returns a canned story. The root and `ENGINE_ROOT` are restored and dropped on teardown.

The render is read where the queue requires the card's kind to be *read, not inferred*: a card's label
and its opened detail go through `render._card_label` / `render._card_detail`, the same authority the
window paints, so a scenario proves the surface speaks the recorded kind rather than guessing it.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile

from .. import communication, conditions, grill, render, tree
from ..scenario import _git                                  # the worlds share the core's git helper
from . import World as _Base, scripted

_DECISION = "a real fork the operator must reason through"
_STATEMENT = "a machine-owned statement to cut"
_APPROVAL = "a go on a planned step"
_ACCEPTANCE = "sign off that the done work meets its bar"
_ASK = "download the new berserk episodes"
_REL, _LEN = "engine/grew.py", 460
_LENGTH_DECISION = (f"the depth gate flagged a long file — accept it or re-cut.\n\n"
                    f"To accept, record `accepted: {_REL} @{_LEN} — long but cohesive`.")
_STORY = json.dumps({"say": "it changes the intake source; I lean nyaa; what flips it is licensing."})
_FLOOR_ONE = json.dumps({"questions": [
    {"q": "which tracker?", "lean": "nyaa", "flip": "a licensed source appears"}]})
_PRODUCTS = json.dumps({"entry": "pull the berserk releases from nyaa", "delta": "# delta — trivial"})


class World(_Base):
    """A scenario's fixture: an isolated, git-backed `ENGINE_ROOT` the real queue settles over.
    `raise` puts a card of a given kind on the surface; the endorsement verbs run approve / cut /
    explain; the grilling verbs surface a question and drive it to a ratifiable entry; the assertion
    verbs read the queue view, the recorded kind through the render, the spawn gate, and the record."""

    def __init__(self):
        self._prev_root = os.environ.get("ENGINE_ROOT")
        self.root = tempfile.mkdtemp(prefix="scenario-queue-")
        os.environ["ENGINE_ROOT"] = self.root              # the tree/queue/record seams read the ambient root
        for cmd in (("init", "-q"), ("config", "user.email", "scenario@hypercore"),
                    ("config", "user.name", "scenario")):
            _git(self.root, *cmd)
        self.card = None                                   # the last-raised card the assertions read
        self.held = None                                   # a held grilling tree, once surfaced
        self.story = None                                  # explain's returned story

    # ── action verbs ──────────────────────────────────────────────────────────────
    def _v_raise(self, args: list[str]) -> tuple[bool, str]:
        """raise <decision|statement|approval|length> — put a machine-owned card of that kind on the
        queue. `length` carries the depth gate's `accepted: <rel> @<N>` template, the card whose
        approval records an accepted length."""
        kind = args[0] if args else ""
        text, code = {
            "decision": (_DECISION, "decide"),
            "statement": (_STATEMENT, "statement"),
            "approval": (_APPROVAL, "approval"),
            "acceptance": (_ACCEPTANCE, "acceptance"),
            "length": (_LENGTH_DECISION, "decide"),
        }.get(kind, (None, None))
        if text is None:
            return False, f"unknown card kind {kind!r}"
        self.card = tree.raise_card(text, kind=code)
        return True, ""

    def _v_approve(self, args: list[str]) -> tuple[bool, str]:
        """approve — endorse the current card: the marker drops, it leaves the queue, the node folds."""
        tree.approve(self.card)
        return True, ""

    def _v_cut(self, args: list[str]) -> tuple[bool, str]:
        """cut — remove the current card's words from the tree (recoverable from the record)."""
        tree.cut(self.card)
        return True, ""

    def _v_explain(self, args: list[str]) -> tuple[bool, str]:
        """explain — the architect tells the story toward the decision; the card stays standing."""
        self.story = communication.explain(self.card, scripted(_STORY))
        return True, ""

    def _v_accept_length(self, args: list[str]) -> tuple[bool, str]:
        """accept-length — the queue's accept-the-length act: record the length the card names through
        the one writer seam, then approve, exactly as the window's approve handler does."""
        conditions.accept_length(self.card.text, self.root)
        tree.approve(self.card)
        return True, ""

    def _v_surface(self, args: list[str]) -> tuple[bool, str]:
        """surface — run a grilling floor that returns one stake-bearing question, so the held ask sits
        on the queue as a grilling-question card carrying its lean and flip."""
        self.held, _qs = grill.consider(_ASK, scripted(_FLOOR_ONE))
        return True, ""

    def _v_resolve(self, args: list[str]) -> tuple[bool, str]:
        """resolve — answer the surfaced question so the pass produces its contract; the held tree now
        shows the entry awaiting ratification (a ratification card), and no work has spawned yet."""
        self.held = grill.advance(self.held, "nyaa", scripted(_PRODUCTS))
        return True, ""

    def _v_ratify(self, args: list[str]) -> tuple[bool, str]:
        """ratify — the operator ratifies the view entry; the held ask spawns as standing work."""
        grill.ratify(self.held)
        return True, ""

    # ── assertion verbs ───────────────────────────────────────────────────────────
    def _v_on_queue(self, args: list[str]) -> tuple[bool, str]:
        """on-queue — the current card is on the live queue view (awaiting the operator)."""
        cards = tree.cards()
        if self.card.id not in {c.id for c in cards}:
            return False, "the card is not on the queue while awaiting"
        return (True, "") if self.card.is_card or tree.find(self.card.id).is_card else (False, "the card is not awaiting")

    def _v_off_queue(self, args: list[str]) -> tuple[bool, str]:
        """off-queue — settling removed the card from the view in the same act (no list to sync)."""
        return ((True, "") if self.card.id not in {c.id for c in tree.cards()}
                else (False, "the settled card is still on the queue"))

    def _v_endorsed(self, args: list[str]) -> tuple[bool, str]:
        """endorsed — approve dropped the [machine] marker, the owner became the operator, and the
        node folded into the archive (location authoritative)."""
        n = tree.find(self.card.id)
        if n is None or n.machine:
            return False, "the approved node still carries the [machine] marker"
        if n.owner != "operator":
            return False, "the approved node's owner did not become the operator"
        return (True, "") if n.folded else (False, "the settled decision did not fold to the archive")

    def _v_gone(self, args: list[str]) -> tuple[bool, str]:
        """gone — cut removed the node from the tree, and the removal is recoverable from the record."""
        if tree.find(self.card.id) is not None:
            return False, "the cut node is still on the tree"
        log = subprocess.run(["git", "log", "--oneline"], cwd=self.root,
                             capture_output=True, text=True).stdout
        return (True, "") if "cut:" in log else (False, "the cut is not recoverable from the record")

    def _v_told(self, args: list[str]) -> tuple[bool, str]:
        """told — explain returned a story toward the decision, and the card still stands on the queue."""
        if not self.story:
            return False, "explain returned no story"
        return ((True, "") if self.card.id in {c.id for c in tree.cards()}
                else (False, "explain cleared the card — it must leave it standing"))

    def _v_reads(self, args: list[str]) -> tuple[bool, str]:
        """reads <decision|approval> — the card's recorded kind is read through the one authority
        (`grill.card_kind`) and the render speaks that glossary word, never inferred from the shape."""
        want = {"decision": "decision", "approval": "request for approval",
                "acceptance": "acceptance"}.get(args[0] if args else "")
        if want is None:
            return False, f"unknown kind {args!r}"
        kind = grill.card_kind(self.card)
        if kind != want:
            return False, f"the recorded kind reads {kind!r}, not {want!r}"
        return ((True, "") if render._card_label(self.card) == want
                else (False, "the render does not speak the recorded kind"))

    def _v_question(self, args: list[str]) -> tuple[bool, str]:
        """question — the surfaced card reads as a grilling question and its opened detail carries the
        machine's lean and the one thing that would flip it (read through the render the window paints)."""
        if grill.card_kind(self.held) != "grilling question":
            return False, "the surfaced card does not read as a grilling question"
        lean, flip = grill.lean_of(self.held), grill.flip_of(self.held)
        if not lean or not flip:
            return False, "the question card carries no lean or no flip"
        detail = "".join(t for row in render._card_detail(self.held, 76) for t, _s in row)
        return ((True, "") if lean in detail and flip in detail
                else (False, "the opened card does not show the lean and flip"))

    def _v_accepts_lean(self, args: list[str]) -> tuple[bool, str]:
        """accepts-lean — approving a grilling question accepts the machine's lean as the answer."""
        held = grill.advance(self.held, grill.lean_of(self.held), scripted(_PRODUCTS))
        ans = [q["answer"] for q in grill._load(held).questions]
        return (True, "") if "nyaa" in ans else (False, "approving did not record the lean as the answer")

    def _v_unspawned(self, args: list[str]) -> tuple[bool, str]:
        """unspawned — the resolved pass has not spawned work: no standing work exists for the ask, and
        the held tree shows the entry as a ratification card awaiting the operator's go."""
        if tree.standing():
            return False, "standing work exists before the entry was ratified"
        return ((True, "") if grill.card_kind(self.held) == "ratification"
                else (False, "the resolved pass does not show a ratification entry"))

    def _v_spawned(self, args: list[str]) -> tuple[bool, str]:
        """spawned — ratifying the entry spawned exactly the one piece of standing work."""
        standing = tree.standing()
        return ((True, "") if len(standing) == 1 and standing[0].id == self.held.id
                else (False, "ratifying did not spawn the ask as standing work"))

    def _v_recorded(self, args: list[str]) -> tuple[bool, str]:
        """recorded — the accepted length named on the card was recorded through the writer seam, and
        the depth gate now clears that file at the recorded length."""
        if conditions.accepted_at(_REL, self.root) != _LEN:
            return False, "the accepted length was not recorded through the writer seam"
        return ((True, "") if conditions.accepted(_REL, _LEN, self.root)
                else (False, "the gate did not clear for the file at the recorded length"))

    def teardown(self) -> None:
        if self._prev_root is None:
            os.environ.pop("ENGINE_ROOT", None)
        else:
            os.environ["ENGINE_ROOT"] = self._prev_root
        shutil.rmtree(self.root, ignore_errors=True)
