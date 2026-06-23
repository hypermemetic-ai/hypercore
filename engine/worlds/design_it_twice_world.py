"""The design-it-twice scenario world — the contest behavior driven through the real `design` over a
seeded, isolated tree.

The verbs name the contest's domain nouns — the candidates, their fences, the recorded pick, the stake
that crosses — never engine symbols, so a worker rewriting `design` has nothing in the scenario to
tamper with to pass. The fixture seeds an isolated `ENGINE_ROOT` git repo (so `worker.worktree`,
`tree.file_intent`, and the node record assemble exactly as in production) and drives the real
`design.contest` / `design.design_twice` with a prompt-routing scripted transport: a candidate prompt
gets a design reply, the architect's selection prompt gets the pick. The candidate design carries a
**leak sentinel** in its `hides` field, so a scenario can assert the raw machine-side design reaches no
card, render, or node. Both the root and `ENGINE_ROOT` are restored and dropped on teardown.

The selection-prompt-names-the-three-axes guarantee is a prompt-construction fact no domain verb can
honestly express without naming the prompt; it is a watched invariant exercised from outside
(`engine/check/scenarios.py`), not faked here. The concurrent-isolation property the contest once
shared a slice with is the cross-cutting single-writer-line proof — not design-it-twice's own — and
homes with `schedule` (the behavior gated in `spec/schedule.md`, the record mechanism watched), not here.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile

from .. import design, render, tree, worker
from ..scenario import _git                                  # the worlds share the core's git helper
from . import World as _Base

_BRIEFS = [("minimal", "Minimize the interface; pull complexity down inside."),
           ("flexible", "Maximize flexibility; make future variation cheap.")]
_SENTINEL = "<<RAW CANDIDATE DESIGN — machine-side only>>"   # planted in a design's hides; must never leak
_STAKE = "the two shapes differ in whether a re-opened contest is visible to you — your call"


class World(_Base):
    """A scenario's fixture: an isolated, git-backed `ENGINE_ROOT` the real `design` runs the contest
    over. `contest` plants the candidates; `twice` runs the whole contest behind one call; the
    assertion verbs read the fences, the recorded pick, the card, and the leak guard."""

    def __init__(self):
        self._prev_root = os.environ.get("ENGINE_ROOT")
        self.root = tempfile.mkdtemp(prefix="scenario-design-")
        os.environ["ENGINE_ROOT"] = self.root              # the tree seams read the ambient root; restored on teardown
        for cmd in (("init", "-q"), ("config", "user.email", "scenario@hypercore"),
                    ("config", "user.name", "scenario")):
            _git(self.root, *cmd)
        tree.atomic_write(os.path.join(self.root, ".keep"), "")
        _git(self.root, "add", "-A"); _git(self.root, "commit", "-qm", "base")    # a HEAD for the fences to branch from
        self.node = self.cands = self.sel = None
        self._before_cards = 0

    # ── the prompt-routing transport ────────────────────────────────────────────
    @staticmethod
    def _design_reply() -> str:
        return json.dumps({"interface": "one entry over the hidden work", "hides": _SENTINEL,
                           "seam": "where the model varies", "depth": "deleting it scatters the work — it earns its keep"})

    def _transport(self, stake: str | None):
        select = json.dumps({"chosen": "minimal", "hybrid": False,
                             "reasoning": "minimal is deepest across depth, locality, and seam",
                             "comparison": {"minimal": "deepest", "flexible": "wider surface for unproven variation"},
                             "stake": stake})
        design_reply = self._design_reply()
        return lambda prompt: select if "design-it-twice contest" in prompt else design_reply

    # ── fixture verbs ───────────────────────────────────────────────────────────
    def _v_contest(self, args: list[str]) -> tuple[bool, str]:
        """contest <N> — file a load-bearing interface decision and design it N ways, each fenced."""
        n = int(args[0])
        self.node = tree.file_intent("the shape of a load-bearing interface")
        self.cands = design.contest(self.node, _BRIEFS[:n], self._transport(None), self.root)
        return True, ""

    def _v_twice(self, args: list[str]) -> tuple[bool, str]:
        """twice <nostake|stake> — run the whole contest behind one call, with or without a
        stake-bearing difference the architect takes to the operator."""
        stake = _STAKE if args[0] == "stake" else None
        self.node = tree.file_intent("a load-bearing interface for the pick")
        self._before_cards = len(tree.cards())
        self.sel = design.design_twice(self.node, _BRIEFS, self._transport(stake), self.root)
        return True, ""

    # ── assertion verbs ─────────────────────────────────────────────────────────
    def _v_candidates(self, args: list[str]) -> tuple[bool, str]:
        """candidates <N> — N candidates were produced, each holding a distinct, live fence."""
        n = int(args[0])
        if not self.cands:
            return False, "the contest has not run"
        if len(self.cands) != n:
            return False, f"expected {n} candidates, got {len(self.cands)}"
        wts = [c.worktree for c in self.cands]
        if len(set(wts)) != n or not all(os.path.isdir(w) for w in wts):
            return False, "the candidates do not each hold a distinct, live fence"
        return True, ""

    def _v_branch(self, args: list[str]) -> tuple[bool, str]:
        """branch each — each candidate committed its design on its own branch, off the main line."""
        for c in self.cands:
            out = self._git_out("log", "--oneline", f"worker/{self.node.id}-{c.brief}")
            if f"candidate: {c.brief} design" not in out:
                return False, f"the {c.brief} candidate's design is not committed on its own branch"
        return True, ""

    def _v_off_main(self, args: list[str]) -> tuple[bool, str]:
        """off-main <file> — the named candidate material never reached the main line (the fence held)."""
        rc = subprocess.run(["git", "cat-file", "-e", f"HEAD:{args[0]}"], cwd=self.root,
                            capture_output=True).returncode
        return (True, "") if rc != 0 else (False, f"{args[0]} reached the main line — the fence leaked")

    def _v_design(self, args: list[str]) -> tuple[bool, str]:
        """design complete — each candidate handed back a full design (interface, hides, seam, depth),
        never an implementation."""
        if args[0] != "complete":
            return False, f"unknown design assertion {args[0]!r}"
        for c in self.cands:
            if not all(c.design.get(k) for k in ("interface", "hides", "seam", "depth")):
                return False, f"the {c.brief} candidate did not hand back a full design"
        return True, ""

    def _v_recorded(self, args: list[str]) -> tuple[bool, str]:
        """recorded — the pick is recorded on the node as a structured, machine-owned design-decision."""
        path = os.path.join(self.node.path, "design-decision.md")
        if not os.path.isfile(path):
            return False, "no design-decision was recorded on the node"
        text = open(path, encoding="utf-8").read()
        if "design-decision:" not in text or f"→ {self.sel.chosen}" not in text:
            return False, "the recorded pick is not a structured design-decision"
        return (True, "") if "[machine]" in text else (False, "the design-decision is not marked machine-owned")

    def _v_card(self, args: list[str]) -> tuple[bool, str]:
        """card <none|decide> — the selection raised no operator card, or a decision card parented to
        the decision node."""
        card = self.sel.card if self.sel else None
        if args[0] == "none":
            return ((True, "") if card is None and len(tree.cards()) == self._before_cards
                    else (False, "expected no operator card, but one was raised"))
        if args[0] == "decide":
            if card is None:
                return False, "expected a decision card, but none was raised"
            if card.kind != "decide":
                return False, f"the card is not a decision: kind={card.kind!r}"
            if card.parent != self.node.id:
                return False, "the decision card is not parented to the decision node"
            return True, ""
        return False, f"unknown card state {args[0]!r}"

    def _v_stake_crosses(self, args: list[str]) -> tuple[bool, str]:
        """stake-crosses — the card carries the architect-authored stake, and no raw candidate design."""
        card = self.sel.card if self.sel else None
        if card is None:
            return False, "no card to carry the stake"
        if _STAKE not in card.text:
            return False, "the card does not carry the architect-authored stake"
        return (False, "a raw candidate design leaked onto the card") if _SENTINEL in card.text else (True, "")

    def _v_no_leak(self, args: list[str]) -> tuple[bool, str]:
        """no-leak — the raw candidate design (the leak sentinel) reaches no card, render, or node."""
        frame = "".join(t for row in render.main_body(tree.read_tree(), -1) for t, _s in row)
        cards_text = "".join(c.text for c in tree.read_tree())
        nodefiles = ""
        for dp, dirs, fs in os.walk(os.path.join(self.root, "work")):
            if "worktrees" in dirs:
                dirs.remove("worktrees")                     # the scratch fences, not the tree's nodes
            nodefiles += "".join(open(os.path.join(dp, fn), encoding="utf-8").read()
                                 for fn in fs if fn in ("intent.md", "grilling.md", "design-decision.md"))
        if _SENTINEL in frame or _SENTINEL in cards_text or _SENTINEL in nodefiles:
            return False, "a raw candidate design leaked to a card, render, or node"
        return True, ""

    def _v_scratch(self, args: list[str]) -> tuple[bool, str]:
        """scratch torn-down — the candidate fences are scratch, torn down once the pick is recorded."""
        if args[0] != "torn-down":
            return False, f"unknown scratch assertion {args[0]!r}"
        for brief, _ in _BRIEFS:
            if os.path.isdir(worker._tree_path(self.node, self.root, tag=brief)):
                return False, f"the {brief} candidate fence was not torn down"
        return True, ""

    # ── internals ───────────────────────────────────────────────────────────────
    def _git_out(self, *args: str) -> str:
        return subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True).stdout

    def teardown(self) -> None:
        if self._prev_root is None:
            os.environ.pop("ENGINE_ROOT", None)
        else:
            os.environ["ENGINE_ROOT"] = self._prev_root
        shutil.rmtree(self.root, ignore_errors=True)
