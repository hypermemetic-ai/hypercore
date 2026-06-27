"""The self-model scenario world — the living spec, the delta, the transactional fold, and the
operator view, driven through the real `spec` / `delta` / `view` over hypercore's own seeded model.

The verbs name the self-model's domain nouns — the spec read flat, a delta that folds or is refused, a
fold that lands and archives in one act, a crash mid-fold, the operator view's vision/as-built/gap —
never engine symbols, so a worker rewriting the fold has nothing in the scenario to tamper with to
pass. The fixture seeds hypercore's *own* spec, intent, and glossary into an isolated `ENGINE_ROOT` (so
the read self-hosts, the view renders the real vision beside the real as-built, and a fold grows the
real model exactly as in production) and drives the real `delta.fold` / `view.operator_view`. The
crash-mid-fold scenario injects a failure into the fold's archive step the way a process killed between
the spec write and the commit would, then proves the retry completes idempotently rather than wedging.
The root and `ENGINE_ROOT` are restored and dropped on teardown.

The self-verifying requirement (a scenario *is* the executable check of its requirement) is not gated
by a block here — it is the very mechanism this whole harness embodies, proven from outside over every
migrated capability and the real red→green gate (`engine/check/scenarios.py` sections 1–2): it stays
**watched**, its honest home the harness's own structure, never a self-referential block.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile

from .. import delta, review, spec, tree, view
from ..scenario import _git                                  # the worlds share the core's git helper
from . import World as _Base
from . import _live_run_fixture
from . import _new_verb_fence                                # the heavyweight new-verb gate fixture, held off this module

_REAL = tree._DEFAULT_ROOT                                  # hypercore's own model, seeded so the read/view/fold self-host
_ADDED = ("queue", "the order is the machine's claim about attention")  # an ADDED into an existing capability
_NEWCAP = ("beacon", "it shines")                          # an ADDED into a capability that does not yet exist
_CRASHCAP = ("gamma", "the gamma property holds")          # the cap grown under an injected crash, then retried
_RENAME_CAP = "queue"
_RENAME_OLD = "the operator endorses with approve, cut, or explain"
_RENAME_NEW = "the operator endorses with approve, cut, or explain in the window"
_RENAME_COLLISION = "the queue is a view of awaiting nodes"
_REMODELED = "The renamed requirement MUST carry the modified body."
_PROBE_WORK = "PROBE-OPEN-WORK"                            # a standing unit, must surface in the gap
_PROBE_CARD = "PROBE-DECISION"                             # a decision awaiting the operator, must not
_FAITHFUL_SUMMARY = "the faithful summary survives intact"
_FAITHFUL_LONG_TOKEN = "boundarytoken" + "x" * 120
_FAITHFUL_TEXT = f"# faithful-crossing — {_FAITHFUL_SUMMARY} before {_FAITHFUL_LONG_TOKEN}\n\ntrivial"

def _delta_text(cap: str, req: str) -> str:
    return (f"# delta — grow {cap}\n\n## ADDED — {cap}\n### Requirement: {req}\n"
            f"The {cap} MUST hold.\n#### Scenario: s\n- WHEN x\n- THEN y\n")

class World(_Base):
    """A scenario's fixture: an isolated, git-backed `ENGINE_ROOT` seeded with hypercore's own spec,
    intent, and glossary, the real `delta` / `view` run over it. The `read` verb caches the spec or the
    view; the `fold` verb performs a fold variant; the assertion verbs read what landed, what was
    refused, the one-commit atomicity, and the view's derived renders."""

    def __init__(self):
        self._prev_root = os.environ.get("ENGINE_ROOT")
        self.root = tempfile.mkdtemp(prefix="scenario-self-model-")
        os.environ["ENGINE_ROOT"] = self.root              # the spec/tree/view seams read the ambient root; restored on teardown
        for cmd in (("init", "-q"), ("config", "user.email", "scenario@hypercore"),
                    ("config", "user.name", "scenario")):
            _git(self.root, *cmd)
        for name in ("spec",):
            shutil.copytree(os.path.join(_REAL, name), os.path.join(self.root, name),
                            ignore=shutil.ignore_patterns("__pycache__"))
        for name in ("intent.md", "glossary.md"):
            shutil.copyfile(os.path.join(_REAL, name), os.path.join(self.root, name))
        tree.commit([os.path.join(self.root, "spec"), os.path.join(self.root, "intent.md"),
                     os.path.join(self.root, "glossary.md")], "seed: hypercore's own model")
        self._spec = None
        self._view = None
        self._node = None
        self._added = None                                 # (capability, requirement) the last adding fold targeted
        self._sig = None                                   # the spec signature captured before a fold, for unchanged/untouched
        self._commits = 0                                  # HEAD commit count captured before a fold, for atomicity
        self._refused = False
        self._renamed = None                               # (capability, old title, new title) for rename assertions
        self._rename_before = None                         # pre-rename block for the untouched-body assertion
        self._rename_modified = False
        self._gate_verdict = None                          # the scenario gate's verdict over the last staged new verb
        self._faithful_messages: list[str] = []             # commit subjects from the faithful-provenance fixture

    # ── internals ────────────────────────────────────────────────────────────────
    def _signature(self) -> set:
        return {(c.name, r.name) for c in spec.read_spec(self.root).capabilities for r in c.requirements}

    def _commit_count(self) -> int:
        out = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=self.root,
                             capture_output=True, text=True).stdout.strip()
        return int(out) if out else 0

    def _try_fold(self, d, node=None) -> None:
        """Attempt a fold, recording whether it was refused — so the refusal scenarios read a real
        CannotFold, never a swallowed one."""
        self._sig = self._signature()
        self._commits = self._commit_count()
        try:
            delta.fold(d, self.root, node=node)
            self._refused = False
        except delta.CannotFold:
            self._refused = True

    # ── action verbs ─────────────────────────────────────────────────────────────
    def _v_read(self, args: list[str]) -> tuple[bool, str]:
        """read <spec|view|view-real> — read the seeded spec, or render the operator view over the
        seeded model (or over hypercore's real tree, where the root's structural map is read)."""
        if args[0] == "spec":
            self._spec = spec.read_spec(self.root)
        elif args[0] == "view":
            self._view = view.operator_view(self.root)
        elif args[0] == "view-real":
            self._view = view.operator_view(_REAL)
        else:
            return False, f"unknown read subject {args[0]!r}"
        return True, ""

    def _v_fold(self, args: list[str]) -> tuple[bool, str]:
        """fold <trivial|missing|mismatched|added|newcap|crash|retry|faithful> — perform one fold variant
        against the seeded spec, node-backed where a fold also archives a node."""
        mode = args[0]
        if mode == "trivial":
            self._try_fold(delta.parse("# delta — trivial (no behavior change)"))
        elif mode == "missing":
            self._try_fold(None)
        elif mode == "mismatched":
            self._try_fold(delta.parse("## MODIFIED — queue\n### Requirement: nonexistent\nx\n"))
        elif mode in ("added", "newcap"):
            cap, req = _ADDED if mode == "added" else _NEWCAP
            self._added = (cap, req)
            self._node = tree.file_intent(f"grow {cap}")
            self._try_fold(delta.parse(_delta_text(cap, req)), node=self._node)
        elif mode == "faithful":
            self._node = tree.file_intent(_FAITHFUL_TEXT)
            tree.dispatch(self._node)
            self._try_fold(delta.parse("# delta\n\nNo behavior change.\n"), node=self._node)
            self._faithful_messages = subprocess.run(
                ["git", "log", "-5", "--format=%s"], cwd=self.root, capture_output=True, text=True
            ).stdout.splitlines()
        elif mode in ("renamed", "renamed-modified"):
            self._renamed = (_RENAME_CAP, _RENAME_OLD, _RENAME_NEW)
            self._rename_before = spec.read_spec(self.root).capability(_RENAME_CAP).requirement(_RENAME_OLD).block
            self._rename_modified = mode == "renamed-modified"
            self._node = tree.file_intent(f"rename {_RENAME_OLD}")
            extra = ""
            if self._rename_modified:
                extra = (f"\n## MODIFIED — {_RENAME_CAP}\n### Requirement: {_RENAME_NEW}\n"
                         f"{_REMODELED}\n#### Scenario: renamed behavior\n"
                         "- WHEN the renamed behavior is read\n- THEN the modified body is present\n")
            self._try_fold(delta.parse(f"# delta — rename queue requirement\n\n"
                                       f"## RENAMED — {_RENAME_CAP}\n"
                                       f"### Requirement: {_RENAME_OLD}\n→ {_RENAME_NEW}\n{extra}"),
                           node=self._node)
        elif mode == "rename-absent":
            # Catches: a RENAMED parser that drops invalid rename blocks as a trivial delta.
            self._try_fold(delta.parse(f"## RENAMED — {_RENAME_CAP}\n"
                                       "### Requirement: an absent old title\n→ a new absent title\n"))
        elif mode == "rename-collision":
            # Catches: a retitle that silently overwrites an existing requirement title.
            self._try_fold(delta.parse(f"## RENAMED — {_RENAME_CAP}\n"
                                       f"### Requirement: {_RENAME_OLD}\n→ {_RENAME_COLLISION}\n"))
        elif mode == "crash":
            cap, req = _CRASHCAP
            self._added = (cap, req)
            self._node = tree.file_intent(f"grow {cap} under a crash")
            self._crash_delta = delta.parse(_delta_text(cap, req))
            self._sig = self._signature()
            real = tree.archive_in_place
            tree.archive_in_place = lambda n: (_ for _ in ()).throw(RuntimeError("crash mid-fold"))
            try:
                delta.fold(self._crash_delta, self.root, node=self._node)
                return False, "the injected crash did not raise — the fold completed when it should have failed"
            except RuntimeError:
                pass
            finally:
                tree.archive_in_place = real
        elif mode == "retry":
            self._try_fold(self._crash_delta, node=tree.find(self._node.id))
        else:
            return False, f"unknown fold mode {mode!r}"
        return True, ""

    def _v_plant(self, args: list[str]) -> tuple[bool, str]:
        """plant <machinery|open-mix> — plant fixtures into the seeded root. `machinery` plants two
        capabilities (one declaring a vision binding, one pure machinery declaring none) so the
        per-capability vision is shown to be a derived binding. `open-mix` files one standing unit of
        open work and raises one decision awaiting the operator, so the gap can be shown to surface the
        open work and exclude the decision."""
        mode = args[0]
        if mode == "machinery":
            tree.atomic_write(os.path.join(self.root, "spec", "lighthouse.md"),
                "# lighthouse\n<!-- vision: legibility -->\n\nA planted capability.\n\n"
                "### Requirement: it shines\n#### Scenario: night\n- WHEN dark\n- THEN light\n")
            tree.atomic_write(os.path.join(self.root, "spec", "boiler.md"),
                "# boiler\n\nA planted machinery capability, declaring no vision.\n\n"
                "### Requirement: it heats\n#### Scenario: cold\n- WHEN cold\n- THEN warm\n")
            return True, ""
        if mode == "open-mix":
            tree.file_intent(f"{_PROBE_WORK} a standing unit of open work")
            tree.raise_card(f"{_PROBE_CARD} a decision awaiting the operator")
            return True, ""
        return False, f"unknown plant subject {mode!r}"

    def _v_watched_evidence(self, args: list[str]) -> tuple[bool, str]:
        """watched-evidence present — plant a committed non-fenced watched-evidence trace, so the view's
        live-run signal proves it reads only fenced-run evidence."""
        if args != ["present"]:
            return False, f"unknown watched-evidence assertion {' '.join(args)!r}"
        _live_run_fixture.plant_non_fenced_trace(self.root)
        return True, ""

    def _v_fenced_crossing(self, args: list[str]) -> tuple[bool, str]:
        """fenced-crossing folds — drive the real worker-apply → integrate path over a fenced worktree
        with scripted models, so the only way the view can flip is the integrate-stage fenced-run trace."""
        if args != ["folds"]:
            return False, f"unknown fenced-crossing action {' '.join(args)!r}"
        return _live_run_fixture.fold_fenced_crossing(self.root)

    def _v_stage_new_verb(self, args: list[str]) -> tuple[bool, str]:
        """stage-new-verb <vacuous|real|multicommit> — stage a fence and run the real scenario gate."""
        mode = args[0]
        if mode in ("vacuous", "real"):
            self._gate_verdict = _new_verb_fence.run_gate(mode)
            return True, ""
        if mode == "multicommit":
            self._gate_verdict = self._multicommit_gate()
            return True, ""
        return False, f"unknown new-verb mode {mode!r}"

    def _multicommit_gate(self) -> str | None:
        """Stage a self-committing worker and run the real gate from the recorded fork base."""
        from .. import scenario, worker
        fence = _new_verb_fence._build("real")             # C0 fork base (behavior absent) → C1 built tip
        _new_verb_fence._write(os.path.join(fence, "RESULT.md"), "# worker result\nhand-off\n")
        _new_verb_fence._commit(fence, "worker: result")    # C2 — the self-committing worker's tip is C1, not the fork
        base = subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=fence,
                              capture_output=True, text=True).stdout.strip()        # C0, the recorded fork base
        result = worker.WorkerResult("built it", _new_verb_fence._DELTA, fence)
        result.base = base                                  # recorded, never inferred from the tip's parent
        guard = os.environ.pop(scenario._GATE_GUARD, None)
        try:
            return scenario.gate(result, fence)
        finally:
            if guard is not None:
                os.environ[scenario._GATE_GUARD] = guard
            shutil.rmtree(fence, ignore_errors=True)

    # ── assertion verbs ──────────────────────────────────────────────────────────
    def _v_gate(self, args: list[str]) -> tuple[bool, str]:
        """gate <held|folds> — the scenario gate's verdict over the staged new verb. `held` asserts the
        gate refused the fold (the vacuous new verb is caught: its fixture now rides onto the base run,
        so it is green at the base too and never transitions); `folds` asserts a real fixture for the
        same new verb still goes red→green and folds — the hardening refuses only the hollow fixture."""
        want = args[0]
        held = self._gate_verdict is not None
        if want == "held":
            return (True, "") if held else (False, "the gate did not hold — a vacuous new verb cleared it, testing nothing")
        if want == "folds":
            return (True, "") if not held else (False, f"the gate held a real fixture that should fold: {self._gate_verdict}")
        return False, f"unknown gate expectation {want!r}"

    def _v_faithful(self, args: list[str]) -> tuple[bool, str]:
        fold_msg = next((m for m in self._faithful_messages if m.startswith("fold: ")), "")
        dispatch_msg = next((m for m in self._faithful_messages if m.startswith("dispatch: ")), "")
        msgs = [fold_msg, dispatch_msg]
        if not all(msgs):
            return False, "the faithful crossing did not record both dispatch and fold subjects"
        bad = [msg for msg in msgs if "# faithful-crossing" in msg or _FAITHFUL_SUMMARY not in msg
               or (_FAITHFUL_LONG_TOKEN[:24] in msg and _FAITHFUL_LONG_TOKEN not in msg)]
        if bad:
            return False, "unfaithful subject: " + "; ".join(bad)
        if "→ channels" in fold_msg or not fold_msg.endswith("→ no-op"):
            return False, f"the fold subject did not name the honest no-capability label: {fold_msg}"
        return True, ""

    def _v_self_hosts(self, args: list[str]) -> tuple[bool, str]:
        """self-hosts — the read spec yields the glossary and the system's own capabilities, segmented
        by capability."""
        sp = self._spec
        names = {c.name for c in sp.capabilities}
        if not {"interface", "tree", "queue", "communication", "self-model"} <= names:
            return False, f"the spec does not self-host hypercore's capabilities ({', '.join(sorted(names))})"
        return (True, "") if sp.glossary.strip() else (False, "the read yields no glossary")

    def _v_covered(self, args: list[str]) -> tuple[bool, str]:
        """covered — every requirement the read yields carries at least one scenario (the floor of
        requirement↔scenario coverage)."""
        uncovered = [r.name for c in self._spec.capabilities for r in c.requirements if not r.scenarios]
        return (True, "") if not uncovered else (False, f"a requirement carries no scenario: {uncovered}")

    def _v_unchanged(self, args: list[str]) -> tuple[bool, str]:
        """unchanged — the trivial fold applied nothing: the spec is exactly as before."""
        return (True, "") if self._signature() == self._sig else (False, "a trivial fold changed the spec")

    def _v_refused(self, args: list[str]) -> tuple[bool, str]:
        """refused — the last fold was refused (CannotFold)."""
        return (True, "") if self._refused else (False, "the fold was not refused")

    def _v_untouched(self, args: list[str]) -> tuple[bool, str]:
        """untouched — a refused fold left the spec exactly as it was."""
        return (True, "") if self._signature() == self._sig else (False, "a refused fold altered the spec")

    def _v_landed(self, args: list[str]) -> tuple[bool, str]:
        """landed [once] — the added requirement is present in its capability's spec (exactly once)."""
        cap, req = self._added
        c = spec.read_spec(self.root).capability(cap)
        present = [r for r in (c.requirements if c else []) if r.name == req]
        if not present:
            return False, f"the added requirement is absent from {cap!r}"
        if args and args[0] == "once" and len(present) != 1:
            return False, f"the requirement is present {len(present)} times, not once — the retry was not idempotent"
        return True, ""

    def _v_archived(self, args: list[str]) -> tuple[bool, str]:
        """archived — the folded node left the work view (archived in the same act)."""
        n = tree.find(self._node.id)
        return (True, "") if n is not None and n.folded else (False, "the node was not archived by the fold")

    def _v_atomic(self, args: list[str]) -> tuple[bool, str]:
        """atomic — the spec merge and the node archive were ONE commit (atomic, both directions)."""
        d = self._commit_count() - self._commits
        return (True, "") if d == 1 else (False, f"the fold spanned {d} commits, not one — not atomic both directions")

    def _v_half_applied(self, args: list[str]) -> tuple[bool, str]:
        """half-applied — after the crash, the delta is on disk but the node is not yet archived (the
        wedge precondition the retry must clear)."""
        cap, req = self._added
        c = spec.read_spec(self.root).capability(cap)
        on_disk = c is not None and c.requirement(req) is not None
        n = tree.find(self._node.id)
        return ((True, "") if on_disk and (n is None or not n.folded)
                else (False, "the crash did not leave the half-applied state the retry must clear"))

    def _v_retitled(self, args: list[str]) -> tuple[bool, str]:
        """retitled — a RENAMED requirement is present under the new title, absent under the old title,
        and, for a pure rename, carries the exact old body and scenarios under the new heading."""
        # Catches: a rename implementation that changes body/scenario text or leaves the old title live.
        cap, old, new = self._renamed
        c = spec.read_spec(self.root).capability(cap)
        old_req, new_req = c.requirement(old), c.requirement(new)
        if old_req is not None or new_req is None:
            return False, "the requirement was not moved from the old title to the new title"
        if not self._rename_modified:
            before_tail = "\n".join(self._rename_before.splitlines()[1:])
            after_tail = "\n".join(new_req.block.splitlines()[1:])
            if after_tail != before_tail:
                return False, "the pure rename changed the requirement body or scenarios"
        return True, ""

    def _v_remodeled(self, args: list[str]) -> tuple[bool, str]:
        """remodeled — a rename paired with a MODIFIED keyed on the new title lands the modified body."""
        # Catches: a fold that applies MODIFIED before resolving RENAMED targets.
        cap, _old, new = self._renamed
        req = spec.read_spec(self.root).capability(cap).requirement(new)
        return ((True, "") if req and _REMODELED in req.block
                else (False, "the MODIFIED keyed on the post-rename title did not land"))

    def _v_grew(self, args: list[str]) -> tuple[bool, str]:
        """grew — the fold created a capability that did not exist before."""
        cap = self._added[0]
        return ((True, "") if spec.read_spec(self.root).capability(cap) is not None
                else (False, f"the fold did not grow the {cap!r} capability"))

    def _v_gained(self, args: list[str]) -> tuple[bool, str]:
        """gained — the operator view gained the new capability as a top-level unit."""
        cap = self._added[0]
        return ((True, "") if any(ch.title == cap for ch in self._view.children)
                else (False, f"the view did not gain {cap!r} as a top-level unit"))

    def _v_vision(self, args: list[str]) -> tuple[bool, str]:
        """vision <present|derived|blank> — the view renders the authored vision; a planted capability's
        declared binding is derived; a machinery capability that declares none shows blank."""
        kind = args[0]
        if kind == "present":
            return ((True, "") if any("legibility" in s.lower() for s in self._view.vision)
                    else (False, "the view does not render the vision from intent.md"))
        child = {ch.title: ch for ch in self._view.children}
        if kind == "derived":
            lh = child.get("lighthouse")
            return ((True, "") if lh and any("legibility" in s.lower() for s in lh.vision)
                    else (False, "a planted capability's declared vision was not derived into the view"))
        if kind == "blank":
            bo = child.get("boiler")
            return ((True, "") if bo and bo.vision == []
                    else (False, "a machinery capability that declares no vision did not show blank"))
        return False, f"unknown vision subject {kind!r}"

    def _v_asbuilt(self, args: list[str]) -> tuple[bool, str]:
        """asbuilt — the view renders the as-built, derived from the spec; after a fold, the new
        requirement appears unedited."""
        if not self._view.asbuilt:
            return False, "the view renders no as-built"
        if self._added:
            cap, req = self._added
            child = next((ch for ch in self._view.children if ch.title == cap), None)
            if child is None or req not in child.asbuilt:
                return False, "the folded requirement does not appear in the derived as-built"
        return True, ""

    def _v_gap(self, args: list[str]) -> tuple[bool, str]:
        """gap — the view renders the gap between vision and as-built."""
        return (True, "") if self._view.gap else (False, "the view renders no gap")

    def _v_gap_is_work(self, args: list[str]) -> tuple[bool, str]:
        """gap-is-work — the gap surfaces the open work and excludes the decision awaiting the operator,
        proving the view reads open work through the tree's one reader, not every non-folded node."""
        # Catches: a view that re-walks the work tree itself and counts any non-folded node as gap,
        # surfacing a queue card (or a grilling hold) as wanted-but-not-built work.
        gap = "\n".join(self._view.gap)
        if _PROBE_WORK not in gap:
            return False, "the gap does not surface the open standing work"
        if _PROBE_CARD in gap:
            return False, ("the gap surfaces a decision awaiting the operator — the view is reading "
                           "every non-folded node, not the open work the tree's one reader yields")
        return True, ""

    def _v_readiness(self, args: list[str]) -> tuple[bool, str]:
        """readiness — the view renders the derived gated/watched standard list."""
        text = "\n".join(self._view.readiness)
        ok = "gated —" in text and "watched —" in text
        return (True, "") if ok else (False, "the readiness surface does not mark standards gated and watched")

    def _v_never_live(self, args: list[str]) -> tuple[bool, str]:
        """never-live — the view reports that no fenced crossing has folded yet, derived from an empty
        fenced-run trail rather than any other watched-evidence verdict."""
        line = next((r.lower() for r in self._view.readiness if "never-run-live" in r), "")
        ok = "fenced crossing" in line and "still unverified" in line and "green" not in line
        return (True, "") if ok else (False, "the never-run-live status is absent or implies green")

    def _v_live_trace(self, args: list[str]) -> tuple[bool, str]:
        """live-trace — once a fenced-run trace exists, the never-run-live line flips away."""
        text = "\n".join(self._view.readiness).lower()
        ok = "live-run-trace" in text and "fenced-run" in text and "never-run-live" not in text
        return (True, "") if ok else (False, "the fenced-run trace did not flip the live status")

    def _v_gap_split(self, args: list[str]) -> tuple[bool, str]:
        """gap-split — wanted-but-not-built gap and built-but-weak complexity debt render separately."""
        if not self._view.gap:
            return False, "the wanted-but-not-built gap is absent"
        if not self._view.complexity_debt:
            return False, "the complexity debt region is absent"
        overlap = set(self._view.gap) & set(self._view.complexity_debt)
        return (True, "") if not overlap else (False, f"gap and complexity debt are conflated: {sorted(overlap)}")

    def _v_structure(self, args: list[str]) -> tuple[bool, str]:
        """structure — the root's structural map is the architecture review's standing output, derived
        from the scan, not hand-authored."""
        bars = review.bars(review.review(_REAL))
        return ((True, "") if self._view.structure and self._view.structure == bars
                else (False, "the root's structural map is not the architecture review's derived output"))

    def _v_debt(self, args: list[str]) -> tuple[bool, str]:
        """debt — the root's complexity debt is the architecture review's backlog, derived from the
        scan."""
        debt = review.complexity_debt(review.review(_REAL))
        return ((True, "") if debt == self._view.complexity_debt
                else (False, "the root's complexity debt is not the architecture review's derived backlog"))

    def teardown(self) -> None:
        if self._prev_root is None:
            os.environ.pop("ENGINE_ROOT", None)
        else:
            os.environ["ENGINE_ROOT"] = self._prev_root
        shutil.rmtree(self.root, ignore_errors=True)
