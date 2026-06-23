"""The communication scenario world — the thread and the architect's single operator-facing voice,
driven through the real `communication.speak` and `communication.integrate` over an isolated tree.

The verbs name communication's domain nouns — the thread, the consequence a turn lands, the worker's
raw words that must not cross — never engine symbols, so a worker rewriting `communication` has nothing
in the scenario to tamper with to pass. The fixture seeds an isolated `ENGINE_ROOT` git repo (so
`tree.file_intent`, the node record, and `read_spec` assemble exactly as in production) and drives the
real seams with a prompt-routing scripted transport: the architect's turn gets a reply of the asked
shape, the grilling floor that a filed ask passes through gets "no questions" so the ask files straight
through (the floor itself is gated in `spec/grilling.md`). The worker hand-off carries a **leak
sentinel** in its machine-facing report, so a scenario can assert the raw prose reaches no card,
render, or node. The root and `ENGINE_ROOT` are restored and dropped on teardown.

Two of communication's requirements stay **watched**, not gated here: *the operator's act never makes
them wait* is the window's off-input-loop threading, a fact no in-process fixture can honestly express
(the interface's concern); *the architect selects among design-it-twice candidates* is gated where its
mechanism lives — `design-it-twice`'s own scenarios drive the real `design.design_twice` — so a second
in-spec block here would only restate it. The glossary's content (the `thread` definition, the open
*operator view* naming question) is communication's vocabulary, exercised from outside in
`engine/check/scenarios.py`, never faked as a scenario.
"""
from __future__ import annotations

import json
import os
import shutil
import tempfile

from .. import communication, render, tree, worker
from ..scenario import _git                                  # the worlds share the core's git helper
from . import World as _Base, scripted

_REAL = tree._DEFAULT_ROOT                                   # the real spec, seeded so speak/integrate assemble as in production
_FILE_ASK = "download the new berserk episodes"
_CARD = "the intake box pulls torrents from nyaa"
_AUTHORED = "It landed — the change is in."                  # the architect's own operator-facing words
_SENTINEL = "<<RAW WORKER REPORT — machine-facing only>>"    # planted in the worker's report; must never cross
_CAP = "demo-communication"                                  # a throwaway capability, absent from the real spec, carrying no scenarios
_REQ = "the operator-facing words are the architect's own"

# The architect's reply for each turn shape — one concrete consequence per turn (the three-consequences
# requirement): a filed ask, a card raised, or a plain answer with nothing filed or carded.
_TURN = {
    "file": json.dumps({"say": "Filing that as standing work.", "file": _FILE_ASK, "card": None, "done": True}),
    "card": json.dumps({"say": "Put that to your queue.", "file": None, "card": _CARD, "done": True}),
    "answer": json.dumps({"say": "I am hypercore's architect.", "file": None, "card": None, "done": True}),
}
_FLOOR_CLEAR = json.dumps({"questions": []})                 # the filed ask is below the floor — it files straight through


class World(_Base):
    """A scenario's fixture: an isolated, git-backed `ENGINE_ROOT` the real architect speaks over.
    `speak` runs one operator turn; `hand-back` stages a worker result and runs the archive integrate;
    the assertion verbs read the thread, the landed consequence, and the leak guard."""

    def __init__(self):
        self._prev_root = os.environ.get("ENGINE_ROOT")
        self.root = tempfile.mkdtemp(prefix="scenario-communication-")
        os.environ["ENGINE_ROOT"] = self.root              # the tree seams read the ambient root; restored on teardown
        for cmd in (("init", "-q"), ("config", "user.email", "scenario@hypercore"),
                    ("config", "user.name", "scenario")):
            _git(self.root, *cmd)
        shutil.copytree(os.path.join(_REAL, "spec"), os.path.join(self.root, "spec"),
                        ignore=shutil.ignore_patterns("__pycache__"))
        g = os.path.join(_REAL, "glossary.md")
        if os.path.isfile(g):
            shutil.copy(g, os.path.join(self.root, "glossary.md"))
        _git(self.root, "add", "-A"); _git(self.root, "commit", "-qm", "base")    # a HEAD for the fence to diff against
        self.thread = self.reply = self.node = None

    def _delta(self) -> str:
        return (f"## ADDED — {_CAP}\n### Requirement: {_REQ}\n"
                "The architect MUST author the operator-facing words.\n"
                "#### Scenario: a hand-off is authored\n- WHEN a result is archived\n- THEN it is authored\n")

    # ── fixture verbs ───────────────────────────────────────────────────────────
    def _v_speak(self, args: list[str]) -> tuple[bool, str]:
        """speak <file|card|answer> — run one operator turn through the real architect with a scripted
        reply of the asked shape; the grilling floor a filed ask passes is routed to "no questions"."""
        mode = args[0] if args else ""
        if mode not in _TURN:
            return False, f"unknown speak shape {mode!r}"
        reply = _TURN[mode]
        self.thread = communication.Thread()
        self.reply = communication.speak(self.thread, f"<operator: {mode}>",
                                          lambda p: _FLOOR_CLEAR if "grilling pass" in p else reply)
        return True, ""

    def _v_hand_back(self, args: list[str]) -> tuple[bool, str]:
        """hand-back — a worker produces a machine-facing result carrying the leak sentinel, and the
        architect integrates it at the archive gate with a coherent verdict and its own authored words."""
        self.node = tree.file_intent("a worker hands back a technical result")
        worker.worktree(self.node, self.root)
        tree.dispatch(self.node)
        result = worker.apply(self.node, scripted(json.dumps(
            {"report": f"did the work — {_SENTINEL}", "delta": self._delta()})), self.root)
        self.reply = communication.integrate(self.node, result, scripted(json.dumps(
            {"coherent": True, "say": _AUTHORED, "card": None})), self.root)
        return True, ""

    # ── assertion verbs: the thread ─────────────────────────────────────────────
    def _v_closes(self, args: list[str]) -> tuple[bool, str]:
        """closes — the thread closed on satisfaction (the operator has what they came for)."""
        if self.thread is None:
            return False, "no turn was spoken"
        return (True, "") if not self.thread.open else (False, "the thread did not close on satisfaction")

    def _v_on_tree(self, args: list[str]) -> tuple[bool, str]:
        """on-tree — the filed intent is standing work, and its unit on disk is the tree (a folder
        under work/), not the thread."""
        standing = tree.standing()
        if len(standing) != 1:
            return False, f"expected one piece of standing work, found {len(standing)}"
        sw = standing[0]
        if not os.path.isfile(os.path.join(self.root, "work", sw.id, "intent.md")):
            return False, "the standing work is not a folder under work/ — the unit on disk is the tree"
        return True, ""

    def _v_reopens(self, args: list[str]) -> tuple[bool, str]:
        """reopens — re-reading the tree fresh shows the work, and no thread is persisted to resume."""
        if len(tree.standing(tree.read_tree())) != 1:
            return False, "re-reading the tree fresh did not show the standing work"
        if os.path.isdir(os.path.join(self.root, "threads")):
            return False, "a thread was persisted — durability must live only on the tree"
        return True, ""

    def _v_no_resume(self, args: list[str]) -> tuple[bool, str]:
        """no-resume — nothing thread-shaped is durable; the thread held no state to resume."""
        return ((True, "") if not os.path.isdir(os.path.join(self.root, "threads"))
                else (False, "a thread was persisted — the thread must hold no durable state"))

    # ── assertion verbs: the one concrete consequence ───────────────────────────
    def _v_filed(self, args: list[str]) -> tuple[bool, str]:
        """filed — the turn filed intent and nothing else (one consequence)."""
        if self.reply is None:
            return False, "no turn was spoken"
        if self.reply.filed is None:
            return False, "the turn filed no intent"
        return (True, "") if self.reply.card is None else (False, "the turn both filed and carded — not one consequence")

    def _v_carded(self, args: list[str]) -> tuple[bool, str]:
        """carded — the turn raised a card on the queue and nothing else (one consequence)."""
        if self.reply is None:
            return False, "no turn was spoken"
        if self.reply.card is None:
            return False, "the turn raised no card"
        if len(tree.cards()) < 1:
            return False, "the card did not reach the queue"
        return (True, "") if self.reply.filed is None else (False, "the turn both carded and filed — not one consequence")

    def _v_answered(self, args: list[str]) -> tuple[bool, str]:
        """answered — the turn answered the question, filing nothing and carding nothing."""
        if self.reply is None:
            return False, "no turn was spoken"
        return ((True, "") if self.reply.filed is None and self.reply.card is None
                else (False, "the answer turn filed or carded — a question lands no consequence on the tree"))

    # ── assertion verbs: the worker's raw words never cross ──────────────────────
    def _v_authored(self, args: list[str]) -> tuple[bool, str]:
        """authored — the operator-facing words are the architect's own, not the worker's report, and
        the result folded at the archive gate."""
        if self.reply is None:
            return False, "no hand-off was integrated"
        if not self.reply.done:
            return False, "the coherent result did not fold at the archive gate"
        if self.reply.say != _AUTHORED:
            return False, "the operator-facing words are not the architect's authored say"
        return (False, "the raw report leaked into the operator-facing words") if _SENTINEL in self.reply.say else (True, "")

    def _v_no_raw_leak(self, args: list[str]) -> tuple[bool, str]:
        """no-raw-leak — the worker's machine-facing report (the leak sentinel) reaches no card, render,
        or node on the main line; it stays fenced, never crossing to the operator."""
        frame = "".join(t for row in render.main_body(tree.read_tree(), -1) for t, _s in row)
        cards_text = "".join(c.text for c in tree.read_tree())
        nodefiles = ""
        for dp, dirs, fs in os.walk(os.path.join(self.root, "work")):
            if "worktrees" in dirs:
                dirs.remove("worktrees")                     # the worker's fence, off the main line — not a node
            nodefiles += "".join(open(os.path.join(dp, fn), encoding="utf-8").read()
                                 for fn in fs if fn in ("intent.md", "grilling.md", "design-decision.md"))
        if _SENTINEL in frame or _SENTINEL in cards_text or _SENTINEL in nodefiles:
            return False, "the raw worker report leaked to a card, render, or node"
        return True, ""

    def teardown(self) -> None:
        if self.node is not None:
            worker.teardown(self.node, self.root)
        if self._prev_root is None:
            os.environ.pop("ENGINE_ROOT", None)
        else:
            os.environ["ENGINE_ROOT"] = self._prev_root
        shutil.rmtree(self.root, ignore_errors=True)
