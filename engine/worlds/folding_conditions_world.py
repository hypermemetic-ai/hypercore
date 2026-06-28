"""The folding-conditions scenario world.

The verbs plant real fold material and read the real gates: length, accepted-lengths,
provenance trails, watched-evidence traces, vocabulary, and now typed gate verdicts. New
seams used by new verbs are imported inside the verb, so the fork-base run is red because
the behavior is absent there.
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
        self.vocab_node = self.vrun_node = None            # the vocabulary guard's node, and the watched run's

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
        if args != ["pre-gate"]:
            return False, f"unknown grandfathered assertion {' '.join(args)!r}"
        conditions.accept("engine/grandfathered.py", 460, "accepted before the provenance gate landed", self.root)
        return True, ""

    def _v_genesis(self, args: list[str]) -> tuple[bool, str]:
        if args != ["anchor", "trail-less"]:
            return False, f"unknown genesis assertion {' '.join(args)!r}"
        self._forge_ledger("AGENTS.md", "@460")            # the minimal shared anchor — a named genesis root
        return True, ""

    def _v_build(self, args: list[str]) -> tuple[bool, str]:
        self.node = tree.file_intent("a provenance demo crossing")
        fence = worker.worktree(self.node, self.root)
        _write(os.path.join(fence, "demo.txt"), "demo")
        worker.commit_tree(fence, "demo: tip")             # a real two-commit fence
        self.result = worker.WorkerResult("built the demo crossing", _DEMO_DELTA, fence)
        return True, ""

    def _v_contest(self, args: list[str]) -> tuple[bool, str]:
        self.node = tree.file_intent("the shape of a load-bearing interface")
        self.selection = design.design_twice(self.node, _BRIEFS[:int(args[0])], _design_transport(), self.root)
        return True, ""

    # ── watched-evidence + vocabulary fixture verbs ──────────────────────────────
    def _v_watched_run(self, args: list[str]) -> tuple[bool, str]:
        from .. import provenance
        self.vrun_node = tree.file_intent("a watched mechanism's run on its node")
        if args[:1] == ["committed-verdict"]:
            provenance.commit_verdict(self.vrun_node, "watched-demo",
                                      "a model verdict no fixture re-derives", self.root)
            return True, ""
        if args[:1] == ["no-verdict"]:
            return True, ""                                # the run was skipped — no trace committed
        return False, f"unknown watched-run kind {' '.join(args)!r}"

    def _v_orphan(self, args: list[str]) -> tuple[bool, str]:
        if args[:1] != ["glossary-term"] or len(args) < 2:
            return False, f"unknown orphan assertion {' '.join(args)!r}"
        term = args[1]
        self._minimal_corpus(f"# glossary\n\n- **{term}** — a defined concept the corpus names nowhere\n")
        self.vocab_node = tree.file_intent("a fold the vocabulary check guards")
        return True, ""

    def _v_corpus(self, args: list[str]) -> tuple[bool, str]:
        if args[:1] != ["consistent"]:
            return False, f"unknown corpus assertion {' '.join(args)!r}"
        self._minimal_corpus("# glossary\n\n- **guard** — a folding condition the system evaluates\n")
        self.vocab_node = tree.file_intent("a fold over a consistent corpus")
        return True, ""

    def _v_vocabulary(self, args: list[str]) -> tuple[bool, str]:
        if args != ["is-its-own-module"]:
            return False, f"unknown vocabulary assertion {' '.join(args)!r}"
        import inspect
        from .. import vocabulary
        if list(inspect.signature(vocabulary.check).parameters) != ["root"]:
            return False, "vocabulary.check does not take only the corpus root"
        src = inspect.getsource(conditions)
        if "def _vocabulary" in src or "_corpus_glossary" in src or "_orphan_term" in src:
            return False, "conditions.py still carries the vocabulary check body"
        gate_body = inspect.getsource(getattr(conditions, "material_verdict", conditions.material_unmet))
        if "vocabulary.check(root)" not in gate_body:
            return False, "material_unmet does not call the vocabulary condition module"
        self._finalize()
        prior = vocabulary.check
        seen = {}
        def fake(root=None):
            seen["root"] = root
            return "decision — vocabulary: sentinel widget"
        vocabulary.check = fake
        try:
            reason = conditions.material_unmet(_Result("scenario fixture", self._delta(), self.fence),
                                               self.root, self.vocab_node)
        finally:
            vocabulary.check = prior
        if seen.get("root") != self.root:
            return False, "the gate did not hand vocabulary.check the live corpus root"
        return ((True, "") if reason == "decision — vocabulary: sentinel widget"
                else (False, f"the gate did not return vocabulary.check's verdict: {reason!r}"))

    def _v_gate_type(self, args: list[str]) -> tuple[bool, str]:
        """gate-type <depth|vocabulary|delta|provenance> <escalating|flat> | string-seam-intact."""
        from ..conditions import material_unmet, material_verdict, unmet, verdict
        if args == ["string-seam-intact"]:
            v, result, root = self._typed_case("depth", verdict)
            mat, full = material_unmet(result, root), unmet(result, root)
            ok = isinstance(mat, str) and isinstance(full, str) and mat == full == v.reason
            return (True, "") if ok else (False, f"string seams drifted: material={mat!r}, full={full!r}, verdict={v!r}")
        if len(args) != 2:
            return False, f"unknown gate-type assertion {' '.join(args)!r}"
        guard, kind = args
        v, _result, _root = self._typed_case(guard, material_verdict)
        if v.guard != guard:
            return False, f"expected guard {guard!r}, got {v.guard!r}"
        expected = kind == "escalating"
        return ((True, "") if v.escalating is expected
                else (False, f"expected escalating={expected}, got {v.escalating} for {v.reason!r}"))

    # ── provenance assertion verbs ───────────────────────────────────────────────
    def _v_gate(self, args: list[str]) -> tuple[bool, str]:
        reason = self._verdict()
        if args[0] in ("held", "holds"):
            return (self._reason(args[1:], reason) if reason is not None
                    else (False, "expected the gate to hold, but every condition was met"))
        if args[0] in ("folds", "clears"):
            return (True, "") if reason is None else (False, f"expected a fold, but the gate held: {reason}")
        return False, f"unknown gate verdict {args[0]!r}"

    def _v_spec(self, args: list[str]) -> tuple[bool, str]:
        reason = self._verdict()
        if args[0] == "untouched":
            return (True, "") if reason is not None else (False, "expected the spec untouched, but the gate cleared")
        if args[0] == "folds":
            return (True, "") if reason is None else (False, f"expected the delta to fold, but the gate held: {reason}")
        return False, f"unknown spec state {args[0]!r}"

    def _v_integrates(self, args: list[str]) -> tuple[bool, str]:
        if self.result is None:
            return False, "integrates read before build"
        reason = self._fold_verdict()
        return (True, "") if reason is None else (False, f"the real crossing did not fold: {reason}")

    def _v_fold(self, args: list[str]) -> tuple[bool, str]:
        reason = self._fold_verdict()
        if args[:1] == ["held"]:
            return (self._reason(args[1:], reason) if reason is not None
                    else (False, "expected the fold to hold, but every condition was met"))
        return (True, "") if reason is None else (False, f"expected the fold, but: {reason}")

    def _v_provenance(self, args: list[str]) -> tuple[bool, str]:
        from .. import provenance
        if args == ["attests", "present"]:
            if self.vrun_node is None:
                return False, "attest read before a watched run"
            r = provenance.watched_trace(self.vrun_node, "watched-demo", self.root)
            return (True, "") if r is None else (False, f"the committed verdict was not attested present: {r}")
        if args == ["refuses", "no-trail"]:
            if self.vrun_node is None:
                return False, "refuse read before a watched run"
            r = provenance.watched_trace(self.vrun_node, "watched-demo", self.root)
            return (True, "") if r and "no trail" in r.lower() else (False, f"expected a no-trail refusal, got {r!r}")
        if args != ["attests-presence"]:
            return False, f"unknown provenance assertion {' '.join(args)!r}"
        guard = os.environ.pop(_GATE_GUARD, None)
        try:
            present = provenance.attest(self.result, self.root).present
            absent = not provenance.attest(provenance.forged_result(self.root), self.root).present
        finally:
            if guard is not None:
                os.environ[_GATE_GUARD] = guard
        return (True, "") if present and absent else (False, f"present={present}, forge-absent={absent}")

    def _v_adequacy(self, args: list[str]) -> tuple[bool, str]:
        if args != ["deferred"]:
            return False, f"unknown adequacy assertion {' '.join(args)!r}"
        from .. import provenance
        att = provenance.attest(self.result, self.root)
        return ((True, "") if att.adequacy == "deferred" and att.residue == "watched"
                else (False, f"the gate claimed adequacy={att.adequacy!r}, residue={att.residue!r}"))

    def _v_reason(self, args: list[str]) -> tuple[bool, str]:
        if args != ["watched"]:
            return False, f"unknown reason assertion {' '.join(args)!r}"
        from .. import provenance
        if not (self.selection and self.selection.reasoning):
            return False, "the contest recorded no reason to watch"
        return ((True, "") if provenance.Attestation(present=True).residue == "watched"
                else (False, "the pick's reason is not recorded watched"))

    def _v_recorded(self, args: list[str]) -> tuple[bool, str]:
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

    def _minimal_corpus(self, glossary: str) -> None:
        """Replace the seeded corpus with a controlled minimal one the gated floor reads — `glossary`,
        a one-line folding-conditions stub (so the fixture delta still applies), and no other prose — so
        the only defined-vs-used relation is the one the scenario plants."""
        sp = os.path.join(self.root, "spec")
        shutil.rmtree(sp, ignore_errors=True)
        _write(os.path.join(sp, "folding-conditions.md"), "# folding-conditions\n\nThe guards.\n")
        _write(os.path.join(self.root, "glossary.md"), glossary)
        intent = os.path.join(self.root, "intent.md")
        if os.path.isfile(intent):
            os.remove(intent)

    def _typed_case(self, kind: str, read_verdict):
        root, fence = tempfile.mkdtemp(prefix="typed-root-"), tempfile.mkdtemp(prefix="typed-fence-")
        self._typed_roots = getattr(self, "_typed_roots", []) + [root, fence]
        for d in (root, fence):
            for cmd in (("init", "-q"), ("config", "user.email", "scenario@hypercore"),
                        ("config", "user.name", "scenario")):
                _git(d, *cmd)
        _write(os.path.join(fence, ".keep"), "base\n")
        _git(fence, "add", "-A"); _git(fence, "commit", "-qm", "base")
        delta_text = "# delta — typed fixture\n"
        node = None
        if kind == "delta":
            delta_text = "## MODIFIED — absent-capability\n### Requirement: absent\nx\n"
        elif kind == "depth":
            _write(os.path.join(fence, "engine", "typed_depth.py"),
                   "# typed depth\n" + "x = 1\n" * conditions.SIGNAL)
        elif kind == "vocabulary":
            _write(os.path.join(root, "glossary.md"), "- **widget** — an orphan defined term\n")
            _write(os.path.join(root, "spec", "folding-conditions.md"),
                   "# folding-conditions\n\n### Requirement: guard\nThe guard holds.\n")
        elif kind == "provenance":
            _write(os.path.join(root, "engine", "accepted-lengths.md"),
                   "accepted: engine/forged.py @460 — hand-authored\n")
        else:
            raise AssertionError(f"unknown gate type {kind!r}")
        _write(os.path.join(fence, ".keep"), f"{kind}\n")
        _git(fence, "add", "-A"); _git(fence, "commit", "-qm", "tip")
        result = _Result("typed fixture", delta_text, fence)
        v = read_verdict(result, root, node)
        if v is None:
            raise AssertionError(f"{kind!r} produced no typed verdict")
        return v, result, root

    def _verdict(self) -> str | None:
        self._finalize()
        return conditions.material_unmet(_Result("scenario fixture", self._delta(), self.fence),
                                         self.root, self.vocab_node)

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
        for path in getattr(self, "_typed_roots", []):
            shutil.rmtree(path, ignore_errors=True)
