"""The worker scenario world — the system-facing half of the split, exercised over the real
`worker.context`/`prompt`/`worktree`/`apply` and `communication.integrate` seams.

The verbs name what the worker *is*, never the engine symbols beneath: `spawn <cap>…` files an ask
whose handed delta names those capabilities and assembles the grounding; `grounding <property>` reads
that grounding (the whole spec preloaded, the named capabilities marked, the depth standards
foregrounded, the long past-decision grounds *not* inlined but pointed at in `work/archive/`);
`sharpen` rewrites the depth slice so `grounding renders` can prove the standards are single-sourced,
not a frozen copy; `fence off-main`/`fence binds-cwd` prove the worktree isolation and
the at-fence transport; `build` runs the whole crossing so `leak none` proves the raw report reaches
no operator path and `integrates` proves the refined delta folds.

Each block runs against an isolated root seeded with the real spec (so the grounding assembles exactly
as in production). `build`/`fence` use a throwaway capability the delta touches, so the scenario gate
stays inert — the worker capability's own red→green is the gate's concern, not the fixture's.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile

from .. import communication, grill, render, spec, transport, tree, worker
from ..scenario import _git
from . import World as _Base, scripted

_REAL = tree._DEFAULT_ROOT
_DEMO = "demo-worker"                                       # a throwaway capability with no scenarios — the gate stays inert
_DEMO_REQ = "the worker's refined delta integrates"

# The framework tokens the depth grounding must foreground every episode, and the code tokens it must
# never carry — the worker holds the spec, not raw code (slice-4/7 properties, named as domain checks).
_DEPTH_FRAMEWORK = ("deep modules", "downward", "strategic", "red flags", "shallow module", "depth standards")
_SPEC_MARKERS = ("### Requirement:", "throwaway conversation")
_CODE_TOKENS = ("import ", "curses")


class World(_Base):
    def __init__(self):
        self._prev_root = os.environ.get("ENGINE_ROOT")
        self.root = tempfile.mkdtemp(prefix="scenario-worker-")
        os.environ["ENGINE_ROOT"] = self.root
        for cmd in (("init", "-q"), ("config", "user.email", "scenario@hypercore"),
                    ("config", "user.name", "scenario")):
            _git(self.root, *cmd)
        shutil.copytree(os.path.join(_REAL, "spec"), os.path.join(self.root, "spec"),
                        ignore=shutil.ignore_patterns("__pycache__"))
        g = os.path.join(_REAL, "glossary.md")
        if os.path.isfile(g):
            shutil.copy(g, os.path.join(self.root, "glossary.md"))
        _git(self.root, "add", "-A"); _git(self.root, "commit", "-qm", "base")
        self.node = self.ctx = self.prompt = self.reply = None
        # Sentinels the worker's grounding is read against. They are world-owned and never authored into
        # a check block — the block's own text is part of the spec the worker's grounding carries, so a
        # sentinel named there would appear in the prompt via the spec and defeat the assertion.
        self.raw = "<<RAW-WORKER-PROSE-Rx4 — machine-facing, must reach no operator path>>"
        self.grounds = "<<JIT-ARCHIVE-GROUNDS-Zx9 — long past-decision history, greped JIT, never preloaded>>"
        self.nonce = "<<DEPTH-SOURCE-NONCE-Qz7 — proves the depth grounding is rendered from its slice>>"

    # ── fixture verbs ────────────────────────────────────────────────────────
    def _v_spawn(self, args: list[str]) -> tuple[bool, str]:
        """spawn <cap>… — file an ask whose handed delta names these capabilities, and assemble the
        worker's grounding (its context and prompt) over the whole seeded spec."""
        self.node = self._stage(self._handed(args))
        self._assemble()
        return True, ""

    def _v_sharpen(self, args: list[str]) -> tuple[bool, str]:
        """sharpen — rewrite the depth slice with a world-owned sentinel, so the grounding rendering it
        (`grounding renders`) proves the standards are read from `spec/depth.md`, not a frozen copy."""
        tree.atomic_write(spec.cap_path("depth", self.root),
            "# depth\n\n"
            "Build deep modules behind small interfaces; pull complexity downward; strategic over "
            f"tactical, with the red flags of a shallow module foregrounded — {self.nonce}.\n\n"
            "### Requirement: a sharpened depth discipline\n"
            "The worker MUST hold the sharpened discipline, building deep up front.\n"
            "#### Scenario: a module is built\n- WHEN a worker builds a module\n- THEN the discipline applies\n")
        if self.node is None:
            self.node = self._stage(self._handed(["worker"]))
        self._assemble()
        return True, ""

    def _v_plant_grounds(self, args: list[str]) -> tuple[bool, str]:
        """plant-grounds — write a past decision carrying the world-owned grounds sentinel into the
        checkout's `work/archive/`, the long history the worker greps just-in-time and must NOT inline."""
        tree.atomic_write(os.path.join(self.root, "work", "archive", "0099-past-decision", "intent.md"),
                          f"# a past decision — its long grounds\n\n{self.grounds}\n")
        return True, ""

    def _v_build(self, args: list[str]) -> tuple[bool, str]:
        """build — run the whole crossing: a worker hands back a raw report and a refined delta at its
        fence, and the architect coherence-checks and folds it."""
        self.node = self._stage(self._demo_delta())
        worker.worktree(self.node, self.root)
        tree.dispatch(self.node)
        result = worker.apply(self.node, scripted(json.dumps(
            {"report": "built it. " + self.raw, "delta": self._demo_delta()})), self.root)
        self.reply = communication.integrate(self.node, result, scripted(json.dumps(
            {"coherent": True, "say": "it landed.", "card": None})), self.root)
        return True, ""

    # ── assertion verbs ──────────────────────────────────────────────────────
    def _v_grounding(self, args: list[str]) -> tuple[bool, str]:
        """grounding <property> — read the worker's assembled grounding. Properties: `whole-spec`,
        `marks <cap>…`, `carries-spec`, `carries-depth`, `holds-no-code`, `omits-grounds`,
        `points-to-archive`, `renders` (the last two read the world's planted sentinels)."""
        if self.ctx is None:
            return False, "grounding read before spawn/sharpen"
        prop = args[0]
        if prop == "whole-spec":
            allcaps = {c.name for c in spec.read_spec(self.root).capabilities}
            return ((True, "") if allcaps and set(self.ctx.names) == allcaps
                    else (False, f"context is not the whole spec; missing {sorted(allcaps - set(self.ctx.names))}"))
        if prop == "marks":
            want = set(args[1:])
            return ((True, "") if self.ctx.touched == want
                    else (False, f"grounding marks {sorted(self.ctx.touched)}, expected {sorted(want)}"))
        if prop == "carries-spec":
            return self._needs(_SPEC_MARKERS)
        if prop == "carries-depth":
            return self._needs(_DEPTH_FRAMEWORK)
        if prop == "holds-no-code":
            leaked = [t for t in _CODE_TOKENS if t in self.prompt]
            return (True, "") if not leaked else (False, f"the grounding carries code tokens {leaked}, not spec")
        if prop == "omits-grounds":
            return ((True, "") if self.grounds not in self.prompt
                    else (False, "the long past-decision grounds were inlined into the prompt"))
        if prop == "points-to-archive":
            p = self.prompt
            return ((True, "") if "work/archive/" in p and "just-in-time" in p and "spec/decisions/" not in p
                    else (False, "the prompt does not point the worker at work/archive/ for a just-in-time grep"))
        if prop == "renders":
            return ((True, "") if self.nonce in self.prompt
                    else (False, "the sharpened depth slice did not render into the grounding — a frozen copy?"))
        return False, f"unknown grounding property {prop!r}"

    def _v_fence(self, args: list[str]) -> tuple[bool, str]:
        """fence <off-main|binds-cwd> — the worktree isolation, and that the worker's transport runs
        with its working directory bound to its own checkout."""
        prop = args[0]
        if prop == "off-main":
            node = self._stage(self._demo_delta())
            fence = worker.worktree(node, self.root)
            tree.dispatch(node)
            worker.apply(node, scripted(json.dumps({"report": "built", "delta": self._demo_delta()})), self.root)
            on_branch = subprocess.run(["git", "log", "--oneline", f"worker/{node.id}"], cwd=self.root,
                                       capture_output=True, text=True).stdout
            off_main = subprocess.run(["git", "cat-file", "-e", "HEAD:RESULT.md"], cwd=self.root,
                                      capture_output=True, text=True).returncode
            distinct = os.path.isdir(fence) and fence != self.root and os.path.join("work", "worktrees") in fence
            if not distinct:
                return False, "the fence is not a distinct worktree under work/worktrees"
            if "worker: result" not in on_branch:
                return False, "the worker's commit is not on its own branch"
            return (True, "") if off_main != 0 else (False, "the worker's result leaked onto the main line")
        if prop == "binds-cwd":
            node = self._stage(self._demo_delta())
            fence = worker.worktree(node, self.root)
            if getattr(transport.worker_transport(fence), "cwd", None) != fence:
                return False, "the worker transport is not bound to the fence's working directory"
            seen: dict[str, str] = {}

            def spy(cwd: str):
                seen["cwd"] = cwd
                return scripted(json.dumps({"report": "built", "delta": self._demo_delta()}))

            saved, worker.worker_transport = worker.worker_transport, spy
            try:
                worker.apply(node, None, self.root)        # transport=None → the live fence-binding path
            finally:
                worker.worker_transport = saved
            return (True, "") if seen.get("cwd") == fence else (False, "apply did not run the worker at its fence cwd")
        return False, f"unknown fence property {prop!r}"

    def _v_leak(self, args: list[str]) -> tuple[bool, str]:
        """leak none — the worker's raw report reaches no card, no render, and no node; the only words
        that cross to the operator are the ones the architect authored."""
        if args[0] != "none":
            return False, f"unknown leak assertion {args[0]!r}"
        nodes = tree.read_tree()
        frame = "".join(t for row in render.main_body(nodes, -1) for t, _s in row)
        files = ""
        for dp, dirs, fs in os.walk(os.path.join(self.root, "work")):
            if "worktrees" in dirs:
                dirs.remove("worktrees")                   # the scratch fence is not a node
            files += "".join(open(os.path.join(dp, fn), encoding="utf-8").read()
                             for fn in fs if fn in ("intent.md", "grilling.md"))
        cards = "".join(c.text for c in nodes)
        return ((False, "the raw worker report reached a card, a render, or a node")
                if self.raw in frame or self.raw in files or self.raw in cards else (True, ""))

    def _v_integrates(self, args: list[str]) -> tuple[bool, str]:
        """integrates — the architect folded the worker's refined delta, and the work left the work view."""
        if self.reply is None:
            return False, "integrates read before build"
        cap = spec.read_spec(self.root).capability(_DEMO)
        if not self.reply.done:
            return False, "the coherent result did not fold"
        if cap is None or cap.requirement(_DEMO_REQ) is None:
            return False, "the refined delta did not reach the spec"
        if self.node.id in [n.id for n in tree.work()]:
            return False, "the integrated work did not leave the work view"
        return True, ""

    # ── internals ────────────────────────────────────────────────────────────
    def _assemble(self) -> None:
        self.ctx = worker.context(self.node, self.root)
        self.prompt = worker.prompt(self.node, self.ctx, self.root)

    def _needs(self, tokens) -> tuple[bool, str]:
        missing = [t for t in tokens if t not in self.prompt]
        return (True, "") if not missing else (False, f"the grounding is missing {missing}")

    def _stage(self, handed: str) -> tree.Node:
        node = tree.file_intent("a worker builds a change")
        tree.atomic_write(os.path.join(node.path, "grilling.md"),
                          grill._render(grill._Pass(0, [], "contract.", handed)))
        return node

    def _handed(self, caps: list[str]) -> str:
        return "".join(
            f"## ADDED — {c}\n### Requirement: a worker probe on {c}\n"
            f"The worker MUST hold {c}.\n#### Scenario: s\n- WHEN it runs\n- THEN {c} holds\n"
            for c in caps)

    def _demo_delta(self) -> str:
        return (f"## ADDED — {_DEMO}\n### Requirement: {_DEMO_REQ}\n"
                "The worker MUST hand back a refined delta that integrates.\n"
                "#### Scenario: s\n- WHEN it hands back\n- THEN it integrates\n")

    def teardown(self) -> None:
        if self._prev_root is None:
            os.environ.pop("ENGINE_ROOT", None)
        else:
            os.environ["ENGINE_ROOT"] = self._prev_root
        shutil.rmtree(self.root, ignore_errors=True)         # the fences live under the root — gone with it
