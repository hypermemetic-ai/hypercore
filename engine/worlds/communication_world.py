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

import os
import shutil
import tempfile

from .. import communication, conditions, depth_scan, grill, render, transport, tree, worker
from ..scenario import _git                                  # the worlds share the core's git helper
from . import World as _Base, scripted

_REAL = tree._DEFAULT_ROOT                                   # the real spec, seeded so speak/integrate assemble as in production
_FILE_ASK = "download the new berserk episodes"
_CARD = "the intake box pulls torrents from nyaa"
_AUTHORED = "It landed — the change is in."                  # the architect's own operator-facing words
_SENTINEL = "<<RAW WORKER REPORT — machine-facing only>>"    # planted in the worker's report; must never cross
_CAP = "demo-communication"                                  # a throwaway capability, absent from the real spec, carrying no scenarios
_REQ = "the operator-facing words are the architect's own"
_DEPTH_FILE = "engine/depth_trip.py"
_LEAN = "lean: accept this file as deep enough for this pass"
_FLIP = "flip: finding a caller that only needs a split-out helper would change the call"

# The architect's reply for each turn shape — one concrete consequence per turn (the three-consequences
# requirement): a filed ask, a card raised, or a plain answer with nothing filed or carded.
_TURN = {
    "file": transport.emit(communication.SYSTEM_SCHEMA,
                           {"say": "Filing that as standing work.", "file": _FILE_ASK, "card": None, "done": True}),
    "card": transport.emit(communication.SYSTEM_SCHEMA,
                           {"say": "Put that to your queue.", "file": None, "card": _CARD, "done": True}),
    "answer": transport.emit(communication.SYSTEM_SCHEMA,
                             {"say": "I am hypercore's architect.", "file": None, "card": None, "done": True}),
}
_FLOOR_CLEAR = transport.emit(grill.FLOOR_SCHEMA, {"questions": []})   # below the floor — it files straight through
_PRODUCTS = transport.emit(grill.PRODUCTS_SCHEMA,
                           {"entry": "download the new berserk episodes.",
                            "delta": "# delta — below-floor ask"})
_CAVEAT = "if the one-writer lock is not a true single holder, concurrent folds corrupt the record"
_CAVEAT_CONTRACT = f"land the migration, carrying this load-bearing caveat: {_CAVEAT}"
_WITHOUT_CAVEAT = "The migration can land on the one-writer lock."
_WITH_CAVEAT = ("The migration can land on the one-writer lock only if it is a true single holder; "
                "otherwise concurrent folds corrupt the record.")
_CAVEAT_DELTA = "# delta — caveat routing fixture"


def _sequence(*replies: str):
    """A prompt-order scripted transport: coherence first, entailment second."""
    pending = list(replies)
    def call(_prompt: str) -> str:
        return pending.pop(0) if pending else ""
    return call


def _coherence_reply(say: str, caveat: str) -> str:
    """A coherence envelope with the caveat tag written manually so the base engine, whose schema lacks
    the tag, still runs the scenario and fails for the behavior rather than for a missing fixture seam."""
    return (f"<say>{say}</say>\n"
            f"<caveat>{caveat}</caveat>\n"
            "<coherent>true</coherent>\n"
            "<card></card>")


def _entailment(survives: bool) -> str:
    return f"<survives>{'true' if survives else 'false'}</survives>"


def _redraft_reply(say: str) -> str:
    """The architect's redrafted operator-facing words — the self-repair of a dropped caveat."""
    return f"<say>{say}</say>"


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
        self.caveat_node = self.caveat_result = None
        self.redrafted_reply = self.redrafted_node = None
        self.held_reply = self.held_node = None
        self.kept_reply = self.kept_node = None
        self._caveat_nodes = []

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
                                          lambda p: (_PRODUCTS if "grilling pass is resolved" in p
                                                     else _FLOOR_CLEAR if "running a grilling pass" in p
                                                     else reply))
        return True, ""

    def _v_hand_back(self, args: list[str]) -> tuple[bool, str]:
        """hand-back — a worker produces a machine-facing result carrying the leak sentinel, and the
        architect integrates it at the archive gate with a coherent verdict and its own authored words."""
        self.node = grill.propose(tree.file_intent("a worker hands back a technical result"),
                                  "contract.", self._delta())
        worker.worktree(self.node, self.root)
        tree.dispatch(self.node)
        result = worker.apply(self.node, scripted(transport.emit(worker.WORKER_SCHEMA,
            {"report": f"did the work — {_SENTINEL}", "delta": self._delta()})), self.root)
        self.reply = communication.integrate(self.node, result, scripted(transport.emit(
            communication.COHERENCE_SCHEMA, {"coherent": True, "say": _AUTHORED, "card": None})), self.root)
        return True, ""

    def _v_integrate(self, args: list[str]) -> tuple[bool, str]:
        """integrate <depth-trip assessment-with-lean-flip | flat-refusal verbatim>."""
        if args == ["depth-trip", "assessment-with-lean-flip"]:
            return self._integrate_depth_trip()
        if args == ["flat-refusal", "verbatim"]:
            return self._integrate_flat_refusal()
        return False, f"unknown integrate assertion {' '.join(args)!r}"

    def _v_contract_caveat(self, args: list[str]) -> tuple[bool, str]:
        """contract-caveat — stage a worker hand-off whose contract carries a load-bearing caveat."""
        self.caveat_node, self.caveat_result = self._stage_caveat_handoff()
        return True, ""

    def _v_drafts_without(self, args: list[str]) -> tuple[bool, str]:
        """drafts-without — integrate a coherent architect draft that drops the contract's caveat. The
        scripted oracle returns not-survived on the first draft; the architect redrafts its own words to
        carry the caveat, and the verdict re-run over the revision returns survived — the self-repair path
        (dropped → redraft-carrying → survived)."""
        if self.caveat_node is None or self.caveat_result is None:
            self.caveat_node, self.caveat_result = self._stage_caveat_handoff()
        self.redrafted_node = self.caveat_node
        self.redrafted_reply = communication.integrate(
            self.caveat_node, self.caveat_result,
            _sequence(_coherence_reply(_WITHOUT_CAVEAT, _CAVEAT), _entailment(False),
                      _redraft_reply(_WITH_CAVEAT), _entailment(True)),
            self.root)
        return True, ""

    def _v_redrafted_crosses(self, args: list[str]) -> tuple[bool, str]:
        """redrafted-crosses — the dropped caveat was repaired by the architect's redraft, not raised: the
        corrected words carrying the caveat crossed and folded, with no decision and no held artifact left."""
        if self.redrafted_reply is None or self.redrafted_node is None:
            return False, "no redrafted-caveat draft was integrated"
        if not self.redrafted_reply.done:
            return False, "the redrafted-caveat draft did not fold"
        if self.redrafted_reply.card is not None:
            return False, "the dropped caveat raised a decision instead of being redrafted to fold"
        if self.redrafted_reply.say != _WITH_CAVEAT:       # exact: the redraft carrying it, not the dropped words
            return False, "the words that crossed are not the redraft carrying the caveat"
        node = tree.find(self.redrafted_node.id)
        if node is None or not node.folded:
            return False, "the redrafted-caveat draft did not archive the node"
        if communication.has_held_build(node):
            return False, "the redrafted-and-folded build left a held artifact"
        return True, ""

    def _v_drafts_uncarriable(self, args: list[str]) -> tuple[bool, str]:
        """drafts-uncarriable — integrate a coherent draft whose caveat the architect's redrafts never
        carry; the scripted oracle returns not-survived on the first draft and on every redraft, so the
        bounded self-revision exhausts and the verdict must escalate."""
        self.held_node, result = self._stage_caveat_handoff()
        replies = [_coherence_reply(_WITHOUT_CAVEAT, _CAVEAT), _entailment(False)]
        for _ in range(communication.CAVEAT_ATTEMPTS):
            replies += [_redraft_reply(_WITHOUT_CAVEAT), _entailment(False)]
        self.held_reply = communication.integrate(self.held_node, result, _sequence(*replies), self.root)
        return True, ""

    def _v_escalates_held(self, args: list[str]) -> tuple[bool, str]:
        """escalates-held — the uncarriable caveat surfaced a held-build decision: the draft did not fold,
        the dropped words never crossed, a parented decision was raised, and the verified build is held for a
        no-rebuild settle — preserve-and-decide intact for the genuine, wording-incurable miss."""
        if self.held_reply is None or self.held_node is None:
            return False, "no uncarriable-caveat draft was integrated"
        if self.held_reply.done:
            return False, "the uncarriable-caveat draft folded"
        if _WITHOUT_CAVEAT in self.held_reply.say:
            return False, "the dropped-caveat words crossed in the reply"
        node = tree.find(self.held_node.id)
        if node is None or node.folded:
            return False, "the uncarriable-caveat draft archived the node"
        if not communication.has_held_build(node):
            return False, "the verified build was not held behind the decision"
        decisions = [c for c in tree.cards() if c.parent == self.held_node.id]
        if not decisions:
            return False, "the uncarriable-caveat draft raised no parented decision"
        return ((True, "") if any("could not be carried" in c.text for c in decisions)
                else (False, "the decision did not name the uncarriable caveat"))

    def _v_drafts_with(self, args: list[str]) -> tuple[bool, str]:
        """drafts-with — integrate a second coherent draft under the same caveated contract, this time
        keeping the caveat and carrying a positive entailment verdict."""
        self.kept_node, result = self._stage_caveat_handoff()
        self.kept_reply = communication.integrate(
            self.kept_node, result,
            _sequence(_coherence_reply(_WITH_CAVEAT, _CAVEAT), _entailment(True)),
            self.root)
        return True, ""

    def _v_crosses(self, args: list[str]) -> tuple[bool, str]:
        """crosses — the caveat-surviving draft folded and its authored words crossed."""
        if self.kept_reply is None or self.kept_node is None:
            return False, "no caveat-surviving draft was integrated"
        if not self.kept_reply.done:
            return False, "the caveat-surviving draft did not fold"
        if self.kept_reply.card is not None:
            return False, "the caveat-surviving draft raised a decision"
        if self.kept_reply.say != _WITH_CAVEAT:
            return False, "the caveat-surviving words did not cross as authored"
        node = tree.find(self.kept_node.id)
        return ((True, "") if node is not None and node.folded
                else (False, "the caveat-surviving draft did not archive the node"))

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

    def _integrate_depth_trip(self) -> tuple[bool, str]:
        node = tree.dispatch(tree.file_intent("a worker hands back a long file"))
        fence = worker.worktree(node, self.root)
        path = os.path.join(fence, _DEPTH_FILE)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("# depth-trip fixture\n" + "x = 1\n" * conditions.SIGNAL)
        worker.commit_tree(fence, "fixture: depth trip")
        result = worker.WorkerResult("machine report", "# delta — depth trip\n", fence)
        seen = {}
        def assess(prompt: str) -> str:
            seen["prompt"] = prompt
            return transport.emit(depth_scan.ASSESSMENT_SCHEMA, {
                "findings": [{"subject": _DEPTH_FILE, "red_flag": "neighborhood tension",
                              "evidence": "callers and siblings stay coherent on the handed map",
                              "lean": _LEAN, "flip": _FLIP}],
                "lean": _LEAN, "flip": _FLIP})
        try:
            reply = communication.integrate(node, result, assess, self.root)
        finally:
            worker.teardown(node, self.root)
        card = reply.card
        if card is None:
            return False, "the depth trip raised no decision card"
        text = card.text
        if _LEAN not in text or _FLIP not in text:
            return False, f"the assessment lacks lean/flip: {text}"
        if "re-cut" in text or "deepen it" in text or "accepted:" in text:
            return False, "the bare depth template leaked into the assessment card"
        prompt = seen.get("prompt", "")
        if "Structural map already computed by architecture-review" not in prompt:
            return False, "the depth scan was not fed the standing review map"
        verdicts = [p for dp, _dirs, fs in os.walk(os.path.join(self.root, "work"))
                    for p in (os.path.join(dp, fn) for fn in fs) if p.endswith(".verdict.md")]
        return (True, "") if not verdicts else (False, f"unexpected watched trace(s): {verdicts}")

    def _integrate_flat_refusal(self) -> tuple[bool, str]:
        node = tree.dispatch(tree.file_intent("a worker hands back a bad delta"))
        fence = worker.worktree(node, self.root)
        with open(os.path.join(fence, "flat-refusal.txt"), "w", encoding="utf-8") as f:
            f.write("fixture\n")
        worker.commit_tree(fence, "fixture: flat refusal")
        bad = ("## MODIFIED — communication\n### Requirement: missing fixture requirement\n"
               "This requirement is absent.\n")
        result = worker.WorkerResult("machine report", bad, fence)
        expected = conditions.verdict(result, self.root, node).reason
        try:
            reply = communication.integrate(node, result, lambda _p: "", self.root)
        finally:
            worker.teardown(node, self.root)
        card = reply.card
        if card is None:
            return False, "the flat refusal raised no card"
        if card.text != expected:
            return False, f"flat refusal was dressed up: expected {expected!r}, got {card.text!r}"
        return (True, "") if "Lean:" not in card.text and "Flip:" not in card.text else (False, "flat refusal became negotiable prose")

    def _stage_caveat_handoff(self):
        node = grill.propose(tree.file_intent("a caveated worker hand-off renders for the operator"),
                             _CAVEAT_CONTRACT, _CAVEAT_DELTA)
        worker.worktree(node, self.root)
        tree.dispatch(node)
        result = worker.apply(node, scripted(transport.emit(worker.WORKER_SCHEMA,
            {"report": "machine-facing caveat fixture report", "delta": _CAVEAT_DELTA})), self.root)
        self._caveat_nodes.append(node)
        return node, result

    def teardown(self) -> None:
        if self.node is not None:
            worker.teardown(self.node, self.root)
        for node in self._caveat_nodes:
            worker.teardown(node, self.root)
        if self._prev_root is None:
            os.environ.pop("ENGINE_ROOT", None)
        else:
            os.environ["ENGINE_ROOT"] = self._prev_root
        shutil.rmtree(self.root, ignore_errors=True)
