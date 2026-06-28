"""The architecture-review scenario world — the standing scan's verdicts, driven through the real
`review` over a planted scan tree and over hypercore's own source.

The verbs name the modules the way the review surfaces them — `giant.py`, `consumer.ORPHAN`,
`ring_a ↔ ring_b` — never engine symbols or paths-into-the-code, so a worker rewriting the review has
nothing in the scenario to tamper with to pass. Two fixtures back them: a throwaway **scan tree** the
fixture verbs plant source into (`module`/`accept`/`dead-symbol`/`used`/`cycle`), read by the
behaviour verbs (`scan`/`debt`/`map`/`mark`/`flag`/`no-flag`); and hypercore's own tree, read by the
`view` verbs that assert the operator view's upper levels ARE the review's output. The scan tree is
dropped on teardown; the `view`/`clean` verbs read live and own no fixture.

The lengths the verbs key off are derived from the live `conditions.SIGNAL`, so the fixtures track the
signal rather than freezing a number: `past-signal` clears it, `near-signal` sits in the warning band,
`within-signal` is clear. An accepted length is recorded straight into the scan tree's record (the
reader's input) — the writer seam's ratchet is folding-conditions' scenario, not this one's.
"""
from __future__ import annotations

import os
import shutil
import tempfile

from .. import conditions, render, review, tree, view
from . import World as _Base

_REAL = tree._DEFAULT_ROOT                                  # hypercore's own source — the view verbs read it live


class World(_Base):
    """A scenario's fixture: a throwaway scan tree the fixture verbs plant `engine/*.py` into, and the
    real `review` read over it (and, for the `view` verbs, over hypercore's own tree). The review is
    memoised per scan and dropped whenever a plant changes the tree, so a scenario reads one coherent
    scan."""

    def __init__(self):
        self.scan = tempfile.mkdtemp(prefix="scenario-review-")
        self._rv: review.Review | None = None
        self._depth_result = None

    # ── fixture verbs: plant the scan tree ──────────────────────────────────────
    def _v_module(self, args: list[str]) -> tuple[bool, str]:
        """module <file.py> <past-signal|near-signal|within-signal|N> — plant a source file at a length."""
        name, n = args[0], self._lines(args[1])
        body = f"# scenario fixture: {name}\n" + "x = 0\n" * max(0, n - 1)
        self._write(name, body)
        return True, ""

    def _v_accept(self, args: list[str]) -> tuple[bool, str]:
        """accept <file.py> @N — record an accepted length for the file (the reader's input the review
        consults, the same record `folding-conditions` gates with), written straight into the scan
        tree's `engine/accepted-lengths.md`."""
        name, bound = args[0], int(args[1].lstrip("@"))
        f = os.path.join(self.scan, "engine", "accepted-lengths.md")
        prior = open(f, encoding="utf-8").read() if os.path.isfile(f) else ""
        tree.atomic_write(f, prior + f"accepted: engine/{name} @{bound} — deep behind a small interface.\n")
        self._rv = None
        return True, ""

    def _v_dead_symbol(self, args: list[str]) -> tuple[bool, str]:
        """dead-symbol <module> <NAME> — plant a module binding <NAME> at top level, read by nobody."""
        module, name = args[0], args[1]
        self._write(f"{module}.py", f"{name} = 99            # bound, read by nobody\n")
        return True, ""

    def _v_used(self, args: list[str]) -> tuple[bool, str]:
        """used <module> <name> — plant a definer of <name> and a consumer that reads it across the
        seam, so the conservative scan raises no dead-symbol flag on a symbol that is actually used."""
        module, name = args[0], args[1]
        self._write(f"{module}.py", f"def {name}():\n    return 1\n")
        self._write(f"{module}_use.py", f"from . import {module}\n\n\ndef use():\n    return {module}.{name}()\n")
        return True, ""

    def _v_cycle(self, args: list[str]) -> tuple[bool, str]:
        """cycle <a> <b> — plant two modules that import each other (a circular dependency)."""
        a, b = args[0], args[1]
        self._write(f"{a}.py", f"from . import {b}\n\nA = 1\n")
        self._write(f"{b}.py", f"from . import {a}\n\nB = 1\n")
        return True, ""

    def _v_symbol_clash(self, args: list[str]) -> tuple[bool, str]:
        """symbol-clash — the false-positive guard: a module that imports a SYMBOL whose name matches a
        sibling module (`from .defs import widget`, while a module `widget` also exists and imports the
        consumer back) raises NO import-cycle flag. A real cycle needs two modules each importing the
        other; here the binding edge is to `defs`, not to the symbol's namesake module, so no cycle
        exists — the exact shape that made `from .transport import render` forge a false cycle."""
        self._write("defs.py", "widget = 1            # a symbol sharing a sibling module's name\n")
        self._write("client.py", "from .defs import widget\n\nC = widget\n")
        self._write("widget.py", "from . import client\n\nW = 1\n")
        cycles = [fl.subject for fl in review.red_flags(self.scan) if fl.rule == "import cycle"]
        return (True, "") if not cycles else (False, f"a symbol/module name clash forged a false cycle: {cycles}")

    def _v_layer(self, args: list[str]) -> tuple[bool, str]:
        """layer <ledger|depth-gate|provenance-gate|no-cycle> ... — read hypercore's own static
        import graph and assert the ledger/provenance layering contract."""
        graph = review.import_graph(_REAL)
        subject = args[0]
        if subject == "no-cycle":
            a, b = _module(args[1]), _module(args[2])
            if a not in graph or b not in graph:
                return False, f"cannot read layer cycle for {args[1:3]!r}: graph has {sorted(graph)}"
            cyclic = _reaches(graph, a, b) and _reaches(graph, b, a)
            return (False, f"{a} and {b} are still mutually reachable in the static graph") if cyclic else (True, "")

        mod = _module(subject)
        if mod not in graph:
            return False, f"{subject} ({mod}) is absent from the engine graph"
        claim = args[1]
        if claim == "leaf":
            deps = graph[mod]
            return (True, "") if not deps else (False, f"{mod} is not a leaf; it imports {sorted(deps)}")
        if claim == "rests-on-ledger":
            deps = graph[mod]
            if _LEDGER not in deps:
                return False, f"{mod} does not import the accepted-length ledger at module scope"
            if mod in graph.get(_LEDGER, set()):
                return False, f"the ledger imports back up to {mod}"
            return True, ""
        if claim == "declares-layer":
            deferred = review.deferred_imports(mod, _REAL)
            if deferred:
                return False, f"{mod} still hides sibling imports below module scope: {sorted(deferred)}"
            deps = graph[mod]
            return (True, "") if deps else (False, f"{mod} still reads as a static leaf")
        return False, f"unknown layer claim {claim!r}"

    # ── behaviour verbs: the review's verdict over the planted scan ──────────────
    def _v_scan(self, args: list[str]) -> tuple[bool, str]:
        """scan measures <file.py> — the live scan includes the module, measured fresh with a real length."""
        if args[0] != "measures":
            return False, f"unknown scan assertion {args[0]!r}"
        m = self._module_named(args[1])
        if m is None:
            return False, f"the scan did not measure {args[1]!r}"
        return (True, "") if m.lines > 0 else (False, f"{args[1]} measured at {m.lines} lines")

    def _v_debt(self, args: list[str]) -> tuple[bool, str]:
        """debt <file.py> <strong|consider|none> [word …] — the complexity-debt finding: its
        recommendation strength (carrying the module's live line count) and any words its note must
        name, or `none` (clear of the backlog)."""
        name, want, words = args[0], args[1], args[2:]
        f = next((fd for fd in self._review().findings if fd.subject == name), None)
        if want == "none":
            return (True, "") if f is None else (False, f"expected {name} clear of the backlog, but it is a {f.strength} finding")
        if f is None:
            return False, f"expected a {want} finding for {name}, but it is not in the backlog"
        if f.strength != want:
            return False, f"expected {name} a {want} finding, but it is {f.strength!r}"
        m = self._module_named(name)
        if m is not None and f.lines != m.lines:
            return False, f"the finding's line count ({f.lines}) is not {name}'s live length ({m.lines})"
        missing = [w for w in words if w.lower() not in f.note.lower()]
        return (True, "") if not missing else (False, f"the finding for {name} does not name {missing}: {f.note!r}")

    def _v_map(self, args: list[str]) -> tuple[bool, str]:
        """map <file.py> <over|exceeded|accepted|nearing|ok> — the module's standing on the structural
        map; an accepted/exceeded module carries the bar it was judged against."""
        name, want = args[0], args[1]
        m = self._module_named(name)
        if m is None:
            return False, f"{name} is not on the structural map"
        if m.status != want:
            return False, f"expected {name} {want!r} on the map, but it is {m.status!r}"
        if want in ("accepted", "exceeded") and m.bar is None:
            return False, f"the {want} module names no bar"
        return True, ""

    def _v_mark(self, args: list[str]) -> tuple[bool, str]:
        """mark <file.py> <word …> — the visual map's mark for the module names each word, so the
        operator reads its standing at a glance (a stale acceptance reads `grew … re-opened`)."""
        name, words = args[0], args[1:]
        line = next((b for b in review.bars(self._review()) if b.split() and b.split()[0] == name), None)
        if line is None:
            return False, f"{name} has no bar on the map"
        low = line.lower().replace("-", " ")
        missing = [w for w in words if w.replace("-", " ").lower() not in low]
        return (True, "") if not missing else (False, f"the map mark for {name} lacks {missing}: {line!r}")

    def _v_flag(self, args: list[str]) -> tuple[bool, str]:
        """flag <dead|cycle> <subject …> — a mechanical red flag of the rule names the subject: a dead
        module-level symbol (`<module>.<NAME>`), or a cycle between the two named modules (either order)."""
        rule = _RULE.get(args[0])
        if rule is None:
            return False, f"unknown red-flag rule {args[0]!r}"
        flags = [fl for fl in review.red_flags(self.scan) if fl.rule == rule]
        if rule == "dead symbol":
            return (True, "") if any(fl.subject == args[1] for fl in flags) else (
                False, f"no dead-symbol flag for {args[1]!r} (found {[fl.subject for fl in flags]})")
        pair = set(args[1:3])
        return (True, "") if any(set(fl.subject.split(" ↔ ")) == pair for fl in flags) else (
            False, f"no import-cycle flag for {pair} (found {[fl.subject for fl in flags]})")

    def _v_no_flag(self, args: list[str]) -> tuple[bool, str]:
        """no-flag <dead|cycle> <subject> — the conservative guarantee: a symbol used across the seam
        (or a clean pair) raises no flag — no false positive."""
        rule = _RULE.get(args[0])
        if rule is None:
            return False, f"unknown red-flag rule {args[0]!r}"
        raised = any(fl.subject == args[1] for fl in review.red_flags(self.scan) if fl.rule == rule)
        return (False, f"expected no {args[0]} flag for {args[1]!r}, but one was raised") if raised else (True, "")

    def _v_clean(self, args: list[str]) -> tuple[bool, str]:
        """clean — a tree with no dead symbols and no cycles reports a clean structural scan, and STILL
        records the model-driven depth judgment as not-yet-built — a clean scan, never a fabricated
        depth verdict. Read over a throwaway clean tree, so the claim does not lean on the planted one."""
        d = tempfile.mkdtemp(prefix="scenario-clean-")
        try:
            tree.atomic_write(os.path.join(d, "engine", "plain.py"), '"""a plain module — no module-level names, no imports."""\n')
            backlog = review.backlog(review.review(d))
            line = " ".join(backlog)
            ok = ("no dead symbols, no circular imports" in line and review.DEPTH_NOT_YET in backlog)
            return (True, "") if ok else (False, f"a clean tree did not report a clean, unfabricated scan: {line!r}")
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def _v_depth_scan(self, args: list[str]) -> tuple[bool, str]:
        """depth-scan <built|consults-map|finding-has-lean-flip> — drive the model-depth seam with a
        scripted transport. The import is deliberately inside the verb: the carried world exists at the
        fork base, but `engine.depth_scan` does not, so base-red proves the seam was absent."""
        from .. import depth_scan

        want = args[0] if args else ""
        if want == "built":
            if "not yet built" in review.DEPTH_NOT_YET.lower():
                return False, "the review gap still says the model-driven depth scan is not yet built"
            if "built" not in review.DEPTH_NOT_YET.lower() or "watched" not in review.DEPTH_NOT_YET.lower():
                return False, f"the review gap does not name the built watched scan: {review.DEPTH_NOT_YET!r}"
            return (True, "") if callable(getattr(depth_scan, "assess", None)) else (
                False, "engine.depth_scan exposes no assess seam")

        assessment, prompt = self._depth_assessment(depth_scan)
        if want == "consults-map":
            if "facade.py" not in prompt or "ghost.py" in prompt:
                return False, "the prompt did not consult exactly the handed review map"
            if assessment.targets != ("facade.py",):
                return False, f"the assessment targets were not filtered through the map: {assessment.targets!r}"
            return True, ""
        if want == "finding-has-lean-flip":
            found = next((f for f in assessment.findings if f.subject == "facade.py"), None)
            if found is None:
                return False, "the assessment returned no finding for the mapped target"
            missing = [name for name in ("lean", "flip") if not getattr(found, name)]
            return (True, "") if not missing else (False, f"the finding lacks {missing}")
        return False, f"unknown depth-scan assertion {want!r}"

    # ── the operator view: the review's output read over hypercore's own tree ────
    def _v_view(self, args: list[str]) -> tuple[bool, str]:
        """view <renders-map|complexity-debt-derived|no-source> — the operator view's upper levels ARE
        the review's output, read over hypercore's own tree: the visual structural map (`renders-map`),
        the complexity debt derived from the review, read with no source code (`no-source`)."""
        what = args[0]
        v = view.operator_view(root=_REAL)
        if what == "renders-map":
            return (True, "") if v.structure and any("█" in ln for ln in v.structure) else (
                False, "the operator view root renders no visual structural map")
        if what == "complexity-debt-derived":
            missing = [ln for ln in review.complexity_debt(review.review(_REAL)) if ln not in v.complexity_debt]
            return ((True, "") if not missing else
                    (False, f"the complexity debt is not the review's backlog ({len(missing)} lines absent)"))
        if what == "no-source":
            text = "".join(t for row in render.view_body(v, 0, 76) for t, _s in row)
            ok = ("operator view" in text and "█" in text and f"/{conditions.SIGNAL}" in text
                  and "from ." not in text and "import os" not in text and "def " not in text)
            return (True, "") if ok else (False, "the map reads as source, not the system's shape")
        return False, f"unknown view assertion {what!r}"

    # ── internals ───────────────────────────────────────────────────────────────
    def _write(self, rel: str, body: str) -> None:
        tree.atomic_write(os.path.join(self.scan, "engine", rel), body)
        self._rv = None                                    # the scan changed — re-read on the next assertion

    def _review(self) -> review.Review:
        if self._rv is None:
            self._rv = review.review(self.scan)
        return self._rv

    def _module_named(self, name: str) -> review.Module | None:
        return next((m for m in self._review().modules if m.rel == name), None)

    def _depth_assessment(self, depth_scan):
        if self._depth_result is None:
            self._write("facade.py", "# scenario fixture: facade.py\n" + "x = 0\n" * (conditions.SIGNAL + 59))
            rv = self._review()
            tree.atomic_write(os.path.join(self.scan, "engine", "ghost.py"),
                              "# written after the review map was computed\nGHOST = 1\n")
            seen: list[str] = []

            def scripted(prompt: str) -> str:
                seen.append(prompt)
                return _depth_reply(depth_scan)

            self._depth_result = (depth_scan.assess(["facade.py", "ghost.py"], rv, scripted), seen[0])
        return self._depth_result

    @staticmethod
    def _lines(spec_: str) -> int:
        return {"past-signal": conditions.SIGNAL + 60,
                "near-signal": int(conditions.SIGNAL * 0.85),     # in the warning band (≥ 0.8·signal), below it
                "within-signal": max(1, conditions.SIGNAL // 2)}.get(spec_) or int(spec_)

    def teardown(self) -> None:
        shutil.rmtree(self.scan, ignore_errors=True)


_RULE = {"dead": "dead symbol", "cycle": "import cycle"}    # the domain word → the review's rule name
_LEDGER = "accepted_lengths"
_LAYER = {"ledger": _LEDGER, "depth-gate": "conditions", "provenance-gate": "provenance"}


def _module(name: str) -> str:
    return _LAYER.get(name, name)


def _reaches(graph: dict[str, set[str]], start: str, target: str, seen: set[str] | None = None) -> bool:
    seen = set() if seen is None else seen
    if start in seen:
        return False
    seen.add(start)
    for nxt in graph.get(start, set()):
        if nxt == target or _reaches(graph, nxt, target, seen):
            return True
    return False


def _depth_reply(depth_scan) -> str:
    from .. import transport
    return transport.emit(depth_scan.ASSESSMENT_SCHEMA, {
        "findings": [{
            "subject": "facade.py",
            "red_flag": "shallow module",
            "evidence": "the handed map marks one large facade target with no deeper seam",
            "lean": "split the interface around the hidden decision",
            "flip": "if callers use one stable operation and the complexity is truly hidden",
        }, {
            "subject": "ghost.py",
            "red_flag": "deletion test",
            "evidence": "this row should be ignored because ghost.py is absent from the handed map",
            "lean": "ignore it",
            "flip": "if it appears on the review map",
        }],
        "lean": "deepen facade.py",
        "flip": "facade.py already hides a stable abstraction",
    })
