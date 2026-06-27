"""The folding-conditions scenario world — the verbs `spec/folding-conditions.md`'s check blocks name,
turned into a real verdict from the `conditions` gate (and, for the provenance gate, the real
`provenance` seam) over planted material.

The verbs name domain nouns, never engine symbols or paths-into-the-code, so a worker rewriting the
engine has nothing in the scenario to tamper with to pass. The length verbs (`grow` / `accept` / `gate`
/ `spec`) plant material and read the depth gate's verdict over it. The **provenance** verbs plant the
two contrasts the trail gate turns on: a record produced by **running the mechanism** (an `accept`
through the seam, a real `build` crossing, a real `contest`) versus the byte-indistinguishable record a
role **hand-faked** without running it (`forge`), and read whether the gate folds the real one and
refuses the fake. The root is seeded with the real spec and ambient (`ENGINE_ROOT`), so a worker
crossing, a contest, and the accept seam's durable commit assemble exactly as in production.

A capability with no world module fails honestly; this one carries folding-conditions' length and
provenance vocabulary. New provenance behavior that needs the brand-new `provenance` seam is lazily
imported inside its verb — absent at the fork base, present at the tip — the watched-residue shape the
self-model's new-verb hardening names.
"""
from __future__ import annotations

import os
import shutil
import tempfile
from dataclasses import dataclass

from .. import conditions, design, transport, tree, worker
from ..scenario import _GATE_GUARD, _git, _write           # the worlds share the core's git/write helpers + the gate guard
from . import World as _Base

_REAL = tree._DEFAULT_ROOT                                  # the real spec to seed, so crossings assemble as in production
_DEMO = "demo-prov"                                         # a throwaway capability with no scenarios — its trail is watched
_DEMO_DELTA = (f"## ADDED — {_DEMO}\n### Requirement: a provenance demo requirement\n"
               "The demo MUST hold.\n#### Scenario: s\n- WHEN it runs\n- THEN it holds\n")
_BRIEFS = [("minimal", "Minimize the interface; pull complexity down inside."),
           ("flexible", "Maximize flexibility; make future variation cheap.")]


def _design_transport():
    """A prompt-routing scripted transport: a candidate prompt gets a design, the architect's
    selection prompt gets the pick — so the real `design.design_twice` runs deterministically."""
    design_reply = transport.emit(design.CANDIDATE_SCHEMA,
        {"interface": "one entry over the hidden work", "hides": "the work it pulls down",
         "seam": "where the model varies", "depth": "deleting it scatters the work"})
    select = transport.emit(design.SELECT_SCHEMA,
        {"chosen": "minimal", "hybrid": False,
         "reasoning": "minimal is deepest across depth, locality, and seam",
         "comparison": [{"brief": "minimal", "note": "deepest"},
                        {"brief": "flexible", "note": "wider surface for unproven variation"}],
         "stake": None})
    return lambda p: select if "design-it-twice contest" in p else design_reply


@dataclass
class _Result:
    """The synthetic hand-off the length verbs assert against — the real gate reads exactly these
    three fields (its delta, its touched material, its fence)."""
    report: str
    delta: str
    worktree: str


class World(_Base):
    """A scenario's fixture: a throwaway fence (a two-commit git worktree, so the gate's touched-file
    diff is well defined) and a throwaway, spec-seeded, ambient root (where the accepted-length record
    commits, a crossing runs, and a contest records its pick). Both dropped on teardown."""

    def __init__(self):
        self.cap = "folding-conditions"
        self._prev_root = os.environ.get("ENGINE_ROOT")
        self.root = tempfile.mkdtemp(prefix="scenario-root-")          # the durable store + crossings live under here
        os.environ["ENGINE_ROOT"] = self.root                          # so the accept seam, tree, and design target this root
        self.fence = tempfile.mkdtemp(prefix="scenario-fence-")
        for d in (self.root, self.fence):                             # both git-backed: the store commits, the fence diffs
            for cmd in (("init", "-q"), ("config", "user.email", "scenario@hypercore"),
                        ("config", "user.name", "scenario")):
                _git(d, *cmd)
        shutil.copytree(os.path.join(_REAL, "spec"), os.path.join(self.root, "spec"),
                        ignore=shutil.ignore_patterns("__pycache__"))  # seed the real spec for the crossings
        _git(self.root, "add", "-A"); _git(self.root, "commit", "-qm", "base")
        _write(os.path.join(self.fence, ".keep"), "")
        _git(self.fence, "add", "-A"); _git(self.fence, "commit", "-qm", "base")     # the fork base (HEAD~1)
        self._dirty = self._final = False
        self.result = self.node = self.selection = None

    # ── length fixture verbs ─────────────────────────────────────────────────────
    def _v_grow(self, args: list[str]) -> tuple[bool, str]:
        """grow <path> <past-signal|within-signal|N> — the tree's commit grows a source file to a length."""
        path, n = args[0], self._lines(args[1])
        _write(os.path.join(self.fence, path), f"# scenario fixture: {path}\n" + "x = 0\n" * (n - 1))
        self._dirty = True
        return True, ""

    def _v_accept(self, args: list[str]) -> tuple[bool, str]:
        """accept <path> <@N|none> — record an accepted length through the one writer seam
        (`conditions.accept`, which ratchets AND commits the ledger, so the record is reachable). A bare
        `none` record names no bound and is planted directly, since the writer seam cannot express one."""
        path, bound = args[0], args[1]
        if bound == "none":
            f = os.path.join(self.root, "engine", "accepted-lengths.md")
            _write(f, (open(f, encoding="utf-8").read() if os.path.isfile(f) else "")
                   + f"accepted: {path} — accepted with no stated length\n")
        else:
            conditions.accept(path, int(bound.lstrip("@")), "deep behind a small interface", self.root)
        return True, ""

    # ── provenance fixture verbs ─────────────────────────────────────────────────
    def _v_forge(self, args: list[str]) -> tuple[bool, str]:
        """forge <accepted-length <path> @N | ran-flag> — a record hand-faked with no mechanism trail.
        `accepted-length` hand-appends a ledger line the accept seam never wrote (working tree only, never
        committed); `ran-flag` hand-authors a worker RESULT carrying a self-asserted `ran: true` the gate
        must ignore — a record that asserts its own provenance is no trail at all."""
        kind = args[0]
        if kind == "accepted-length":
            self._forge_ledger(args[1], args[2])
            return True, ""
        if kind == "ran-flag":
            from .. import provenance                       # the brand-new seam — lazily, absent at the base
            self.result = provenance.forged_result(self.root, flag=True)
            return True, ""
        return False, f"unknown forge kind {kind!r}"

    def _v_grandfathered(self, args: list[str]) -> tuple[bool, str]:
        """grandfathered pre-gate — a record already durable in the source of truth, folded before the
        gate landed: an accepted-length line committed through the seam. Forward-only, the gate does not
        retroactively refuse it — a retroactive bar could not tell a fake from a legitimately-swept trail."""
        if args != ["pre-gate"]:
            return False, f"unknown grandfathered assertion {' '.join(args)!r}"
        conditions.accept("engine/grandfathered.py", 460, "accepted before the provenance gate landed", self.root)
        return True, ""

    def _v_genesis(self, args: list[str]) -> tuple[bool, str]:
        """genesis anchor trail-less — forge a trail-less record naming a genesis authored-trust root
        (the minimal shared anchor), which necessarily predates the gate, so it folds under the one named
        exemption where a non-genesis trail-less record does not."""
        if args != ["anchor", "trail-less"]:
            return False, f"unknown genesis assertion {' '.join(args)!r}"
        self._forge_ledger("AGENTS.md", "@460")            # the minimal shared anchor — a named genesis root
        return True, ""

    def _v_build(self, args: list[str]) -> tuple[bool, str]:
        """build — a real worker crossing whose RESULT folds, the trail-bearing baseline a forge is
        contrasted against. It touches a no-scenario demo capability, so its trail is present (watched)."""
        self.node = tree.file_intent("a provenance demo crossing")
        fence = worker.worktree(self.node, self.root)
        _write(os.path.join(fence, "demo.txt"), "demo")
        worker.commit_tree(fence, "demo: tip")             # a real two-commit fence
        self.result = worker.WorkerResult("built the demo crossing", _DEMO_DELTA, fence)
        return True, ""

    def _v_contest(self, args: list[str]) -> tuple[bool, str]:
        """contest <N> — a real design-it-twice contest of N candidates, each fenced, the pick recorded
        with its candidate set durable on the node."""
        self.node = tree.file_intent("the shape of a load-bearing interface")
        self.selection = design.design_twice(self.node, _BRIEFS[:int(args[0])], _design_transport(), self.root)
        return True, ""

    # ── provenance assertion verbs ───────────────────────────────────────────────
    def _v_gate(self, args: list[str]) -> tuple[bool, str]:
        """gate <held|folds> [because <word|provenance> …] [names <path> …] — the real gate's verdict on
        the planted material (in-process, via `material_unmet`): held (a folding condition refuses) or
        folds (every condition met). `because provenance` matches the flat trail refusal."""
        reason = self._verdict()
        if args[0] in ("held", "holds"):
            return (self._reason(args[1:], reason) if reason is not None
                    else (False, "expected the gate to hold, but every condition was met"))
        if args[0] in ("folds", "clears"):
            return (True, "") if reason is None else (False, f"expected a fold, but the gate held: {reason}")
        return False, f"unknown gate verdict {args[0]!r}"

    def _v_spec(self, args: list[str]) -> tuple[bool, str]:
        """spec <untouched|folds> — the merge guarantee. `untouched`: a refused condition holds the
        fold, so the delta never reaches the spec. `folds`: every condition met, the delta is free."""
        reason = self._verdict()
        if args[0] == "untouched":
            return (True, "") if reason is not None else (False, "expected the spec untouched, but the gate cleared")
        if args[0] == "folds":
            return (True, "") if reason is None else (False, f"expected the delta to fold, but the gate held: {reason}")
        return False, f"unknown spec state {args[0]!r}"

    def _v_integrates(self, args: list[str]) -> tuple[bool, str]:
        """integrates — the real crossing's folding conditions are met: its trail is present, it folds."""
        if self.result is None:
            return False, "integrates read before build"
        reason = self._fold_verdict()
        return (True, "") if reason is None else (False, f"the real crossing did not fold: {reason}")

    def _v_fold(self, args: list[str]) -> tuple[bool, str]:
        """fold <held [because provenance] | folds> — the full fold's verdict over the forged record
        (`conditions.unmet`, the derived trail included). The gate guard is cleared so the re-derivation
        genuinely runs; the forge's dir is no fence, so clearing cannot recurse (as `_new_verb_fence`)."""
        reason = self._fold_verdict()
        if args[:1] == ["held"]:
            return (self._reason(args[1:], reason) if reason is not None
                    else (False, "expected the fold to hold, but every condition was met"))
        return (True, "") if reason is None else (False, f"expected the fold, but: {reason}")

    def _v_provenance(self, args: list[str]) -> tuple[bool, str]:
        """provenance attests-presence — the gate attests the real record's trail is present and a
        trail-less forge's is absent: the structural verdict, the boundary of what it can say."""
        if args != ["attests-presence"]:
            return False, f"unknown provenance assertion {' '.join(args)!r}"
        from .. import provenance
        guard = os.environ.pop(_GATE_GUARD, None)
        try:
            present = provenance.attest(self.result, self.root).present
            absent = not provenance.attest(provenance.forged_result(self.root), self.root).present
        finally:
            if guard is not None:
                os.environ[_GATE_GUARD] = guard
        return (True, "") if present and absent else (False, f"present={present}, forge-absent={absent}")

    def _v_adequacy(self, args: list[str]) -> tuple[bool, str]:
        """adequacy deferred — the gate makes no check-adequacy claim; that layer is
        `gate-vouches-for-the-new-verb`'s. A real red→green can still test nothing, so trail-presence is
        all this attests."""
        if args != ["deferred"]:
            return False, f"unknown adequacy assertion {' '.join(args)!r}"
        from .. import provenance
        att = provenance.attest(self.result, self.root)
        return ((True, "") if att.adequacy == "deferred" and att.residue == "watched"
                else (False, f"the gate claimed adequacy={att.adequacy!r}, residue={att.residue!r}"))

    def _v_reason(self, args: list[str]) -> tuple[bool, str]:
        """reason watched — a pick's reason is irreducibly creative, recorded watched, never pretend-
        gated: the gate attests the structural trail and says the reasoning is outside its reach."""
        if args != ["watched"]:
            return False, f"unknown reason assertion {' '.join(args)!r}"
        from .. import provenance
        if not (self.selection and self.selection.reasoning):
            return False, "the contest recorded no reason to watch"
        return ((True, "") if provenance.Attestation(present=True).residue == "watched"
                else (False, "the pick's reason is not recorded watched"))

    def _v_recorded(self, args: list[str]) -> tuple[bool, str]:
        """recorded — the pick is recorded on the node with its contest's candidate set reachable."""
        path = os.path.join(self.node.path, "design-decision.md")
        if not os.path.isfile(path):
            return False, "no design-decision recorded on the node"
        text = open(path, encoding="utf-8").read()
        bullets = sum(1 for ln in text.splitlines() if ln.lstrip().startswith("- **"))
        return ((True, "") if "design-decision:" in text and bullets >= 2
                else (False, "the recorded pick has no reachable candidate set"))

    # ── internals ────────────────────────────────────────────────────────────────
    def _forge_ledger(self, path: str, bound: str) -> None:
        """Hand-append an accepted-length line to the working-tree ledger the accept seam never wrote —
        never committed, so it has no seam trail. The byte-indistinguishable fake the gate must refuse."""
        f = os.path.join(self.root, "engine", "accepted-lengths.md")
        _write(f, (open(f, encoding="utf-8").read() if os.path.isfile(f) else "")
               + f"accepted: {path} {bound} — hand-authored to clear the gate\n")

    def _reason(self, args: list[str], reason: str) -> tuple[bool, str]:
        low, i = reason.lower(), 0
        while i < len(args) - 1:
            key, val = args[i], args[i + 1]
            if key == "because" and val == "provenance" and "no trail" not in low:
                return False, f"the gate held but not for a missing provenance trail: {reason}"
            if key == "because" and val != "provenance" and val.replace("-", " ").lower() not in low:
                return False, f"the gate held but its reason lacks {val!r}: {reason}"
            if key == "names" and val not in reason:
                return False, f"the gate held but its reason does not name {val!r}: {reason}"
            i += 2 if key in ("because", "names") else 1
        return True, ""

    def _verdict(self) -> str | None:
        self._finalize()
        return conditions.material_unmet(_Result("scenario fixture", self._delta(), self.fence), self.root)

    def _fold_verdict(self) -> str | None:
        """The full fold's verdict over the planted record, the gate guard cleared so the derived
        re-derivation genuinely runs (the forge carries no fence, so clearing cannot recurse)."""
        guard = os.environ.pop(_GATE_GUARD, None)
        try:
            return conditions.unmet(self.result, self.root)
        finally:
            if guard is not None:
                os.environ[_GATE_GUARD] = guard

    def _delta(self) -> str:
        return (f"# delta — scenario fixture\n## ADDED — {self.cap}\n"
                "### Requirement: scenario fixture\nfixture\n#### Scenario: s\n- WHEN x\n- THEN y\n")

    def _finalize(self) -> None:
        if not self._final:
            _git(self.fence, "add", "-A")
            _git(self.fence, "commit", "-q", *(() if self._dirty else ("--allow-empty",)), "-m", "tip")
            self._final = True

    @staticmethod
    def _lines(spec_: str) -> int:
        return {"past-signal": conditions.SIGNAL + 60,
                "within-signal": max(1, conditions.SIGNAL - 100)}.get(spec_, None) or int(spec_)

    def teardown(self) -> None:
        if self._prev_root is None:
            os.environ.pop("ENGINE_ROOT", None)
        else:
            os.environ["ENGINE_ROOT"] = self._prev_root
        shutil.rmtree(self.root, ignore_errors=True)
        shutil.rmtree(self.fence, ignore_errors=True)
