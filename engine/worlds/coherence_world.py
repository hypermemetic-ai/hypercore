"""The coherence scenario world — the branches of the architect's archive-gate judgment, driven
through the real `communication.integrate` over a staged worker hand-off.

`hand <coherent|incoherent|unreadable-then-coherent|unreadable-persistent>` files an ask, cuts its
fence, runs a worker (a scripted hand-back), and runs the architect's integrate with a scripted
verdict; the assertion verbs read what integrate did — `fold <lands|held>`,
`spec <folds|untouched>`, `card <decide|unreadable|none>`, `node <live>`. The fixture seeds a real
spec into an isolated root (so the worker prompt and `read_spec` assemble exactly as in
production) and the worker's delta touches a throwaway capability that carries no scenarios, so the
**scenario gate stays inert** and the block isolates the coherence branch — the gate has its own
red→green in the acceptance harness (`engine/check/scenarios.py`).
"""
from __future__ import annotations

import os
import shutil
import tempfile

from .. import communication, grill, spec, transport, tree, worker
from ..scenario import _git                                 # the worlds share the core's git helper
from . import World as _Base, scripted

_REAL = tree._DEFAULT_ROOT                                  # the real spec, seeded so the worker assembles as in production
_CAP = "demo-coherence"                                     # a throwaway capability, absent from the real spec, carrying no scenarios
_REQ = "the archived result is judged at the operator's altitude"
_UNREADABLE = "<say>format slipped</say>\n<card></card>"     # carries tags, but no usable coherent verdict


def _sequence(*replies: str):
    pending = list(replies)
    def call(_prompt: str) -> str:
        return pending.pop(0) if pending else replies[-1]
    return call


class World(_Base):
    def __init__(self):
        self._prev_root = os.environ.get("ENGINE_ROOT")
        self.root = tempfile.mkdtemp(prefix="scenario-coherence-")
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
        self.node = self.reply = None
        self._nodes = []

    def _delta(self) -> str:
        return (f"## ADDED — {_CAP}\n### Requirement: {_REQ}\n"
                "The architect MUST judge the hand-off at the operator's altitude.\n"
                "#### Scenario: a hand-off is judged\n- WHEN a result is archived\n- THEN it is judged\n")

    # fixture verb ────────────────────────────────────────────────────────────
    def _v_hand(self, args: list[str]) -> tuple[bool, str]:
        """hand <coherent|incoherent|unreadable-then-coherent|unreadable-persistent> — stage a node,
        run a worker (scripted hand-back), and run the architect's integrate with a scripted verdict."""
        mode = args[0] if args else ""
        if mode not in ("coherent", "honors", "incoherent", "unreadable-then-coherent",
                        "unreadable-persistent"):
            return False, f"unknown hand mode {mode!r}"
        self.node = grill.propose(tree.file_intent("a worker hands a result back"), "contract.", self._delta())
        self._nodes.append(self.node)
        worker.worktree(self.node, self.root)
        tree.dispatch(self.node)
        result = worker.apply(self.node, scripted(transport.emit(worker.WORKER_SCHEMA,
            {"report": "did the work — machine-facing", "delta": self._delta()})), self.root)
        coherent = mode in ("coherent", "honors")
        usable = transport.emit(communication.COHERENCE_SCHEMA, {
            "coherent": coherent,
            "say": "it landed." if coherent else "this doesn't honor the contract.",
            "card": None if coherent else
                    "the result did not honor the contract — re-cut, abandon, or change the ask"})
        if mode == "unreadable-then-coherent":
            coherence = _sequence(_UNREADABLE, transport.emit(
                communication.COHERENCE_SCHEMA,
                {"coherent": True, "say": "it landed after retry.", "card": None}))
        elif mode == "unreadable-persistent":
            coherence = _sequence(*([_UNREADABLE] * communication.COHERENCE_ATTEMPTS))
        else:
            coherence = scripted(usable)
        self.reply = communication.integrate(self.node, result, coherence, self.root)
        return True, ""

    # assertion verbs ───────────────────────────────────────────────────────────
    def _v_fold(self, args: list[str]) -> tuple[bool, str]:
        """fold <lands|held> — whether integrate folded the result (`done`) or held it."""
        if self.reply is None:
            return False, "fold read before a result was handed"
        if args[0] in ("lands", "folds"):
            return (True, "") if self.reply.done else (False, "expected the result to fold, but it was held")
        if args[0] in ("held", "holds"):
            return (True, "") if not self.reply.done else (False, "expected the result held, but it folded")
        return False, f"unknown fold verdict {args[0]!r}"

    def _v_spec(self, args: list[str]) -> tuple[bool, str]:
        """spec <folds|untouched> — whether the refined delta reached the spec."""
        cap = spec.read_spec(self.root).capability(_CAP)
        present = cap is not None and cap.requirement(_REQ) is not None
        if args[0] == "folds":
            return (True, "") if present else (False, "expected the delta in the spec, but it is absent")
        if args[0] == "untouched":
            return (True, "") if not present else (False, "expected the spec untouched, but the delta merged")
        return False, f"unknown spec state {args[0]!r}"

    def _v_card(self, args: list[str]) -> tuple[bool, str]:
        """card <decide|none> — the decision integrate raised (parented to the node), or none."""
        card = self.reply.card if self.reply else None
        if args[0] == "none":
            return (True, "") if card is None else (False, f"expected no card, but one was raised: {card.text}")
        if args[0] == "decide":
            if card is None:
                return False, "expected a decision card, but none was raised"
            if card.kind != "decide":
                return False, f"the card is not a decision: kind={card.kind!r}"
            if card.parent != self.node.id:
                return False, "the decision card is not parented to the node"
            return True, ""
        if args[0] == "unreadable":
            if card is None:
                return False, "expected an unreadable-reply decision card, but none was raised"
            if card.kind != "decide":
                return False, f"the unreadable-reply card is not a decision: kind={card.kind!r}"
            if card.parent != self.node.id:
                return False, "the unreadable-reply card is not parented to the node"
            if "coherence reply unreadable" not in card.text:
                return False, f"the decision did not name the unreadable coherence reply: {card.text}"
            if "did not honor the contract" in card.text:
                return False, "the unreadable reply was raised as the incoherence refusal"
            return True, ""
        return False, f"unknown card kind {args[0]!r}"

    def _v_node(self, args: list[str]) -> tuple[bool, str]:
        """node <live> — the node stayed live for the operator's decision, not folded out."""
        after = tree.find(self.node.id)
        if args[0] == "live":
            return ((True, "") if after is not None and after.folded is False
                    else (False, "expected the node live, but it folded"))
        return False, f"unknown node state {args[0]!r}"

    def teardown(self) -> None:
        for node in self._nodes:
            worker.teardown(node, self.root)
        if self._prev_root is None:
            os.environ.pop("ENGINE_ROOT", None)
        else:
            os.environ["ENGINE_ROOT"] = self._prev_root
        shutil.rmtree(self.root, ignore_errors=True)
