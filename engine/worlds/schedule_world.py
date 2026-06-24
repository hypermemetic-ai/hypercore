"""The schedule scenario world — the autonomous loop driven through the real `Scheduler` over a
seeded, isolated tree.

The verbs name the loop's domain nouns — the ready work, a worker in flight, its fence, the fold, a
failure surfaced as a decision — never engine symbols, so a worker rewriting `schedule` has nothing in
the scenario to tamper with to pass. The fixture is an isolated, git-backed `ENGINE_ROOT` (so
`tree.file_intent`, `tree.ready`, the fences, and the fold assemble exactly as in production) and the
real `schedule.Scheduler` runs over it with a prompt-routing scripted transport: a build prompt is
matched to its node by a token in the ask and answered with that node's delta — held on an event when a
scenario watches two builds in flight at once, raised mid-build when it drives a failure — while the
architect's coherence prompt is answered coherent. The root and `ENGINE_ROOT` are restored and dropped
on teardown, any held build released first, so no worker thread outlives the fixture.

The single-writer line the concurrency scenario rests on is proven at the record-mechanism level —
exact-path commits, the cross-holder `flock`, slug reservation — as watched invariants exercised from
outside (`engine/check/scenarios.py`): the scenario here gates the *behavior* (two workers advance and
each folds its own delta into the one spec), the watched invariants gate the *mechanism* that makes it
true by construction, the way a fixture cannot honestly fake a second OS process racing the index.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import threading
import time

from .. import schedule, spec, tree, worker
from ..scenario import _git                                  # the worlds share the core's git helper
from . import World as _Base

_TOKENS = ["ALPHAMARK", "BETAMARK", "GAMMAMARK", "DELTAMARK"]  # a distinct token per ready ask; none a substring of another
_CAPS = ["alpha", "beta", "gamma", "delta"]                  # the capability each ready worker folds
_COHERENT = json.dumps({"coherent": True, "say": "it landed.", "card": None})


def _built(cap: str) -> str:
    """A worker's hand-off: a report and a delta adding a fresh capability, so each ready node folds
    its own delta into the one spec with no two contending for the same capability."""
    return json.dumps({"report": f"built {cap}",
                       "delta": (f"## ADDED — {cap}\n### Requirement: {cap} holds\n"
                                 f"The {cap} capability MUST hold.\n#### Scenario: s\n- WHEN x\n- THEN y\n")})


class World(_Base):
    """A scenario's fixture: an isolated, git-backed `ENGINE_ROOT` the real `Scheduler` runs over.
    The setup verbs file the ready work (`ready` / `blocked` / `blocked-sibling` / `failing`); the
    action verbs run the loop (`run` to completion, `dispatch held` + `release` to watch two builds in
    flight, `step` for one pass); the assertion verbs read the fences, the fold, the ready work, and a
    failure surfaced as a decision."""

    def __init__(self):
        self._prev_root = os.environ.get("ENGINE_ROOT")
        self.root = tempfile.mkdtemp(prefix="scenario-schedule-")
        os.environ["ENGINE_ROOT"] = self.root              # the tree seams read the ambient root; restored on teardown
        for cmd in (("init", "-q"), ("config", "user.email", "scenario@hypercore"),
                    ("config", "user.name", "scenario")):
            _git(self.root, *cmd)
        self._nodes: dict[str, tree.Node] = {}
        self._mapping: dict[str, str] = {}                 # build token → capability the worker folds
        self._fail: set[str] = set()                       # tokens whose worker errs mid-build
        self._hold: threading.Event | None = None          # set while a scenario holds builds in flight
        self._sched: schedule.Scheduler | None = None

    # ── the prompt-routing transport ────────────────────────────────────────────
    def _transport(self):
        """The one transport every role calls: the architect's coherence pass is answered coherent; a
        worker build is matched to its node by the token in its ask — raised when the token is a
        failure, held until release when a build is held, else answered with that node's delta."""
        def t(prompt: str) -> str:
            if "archiving a worker" in prompt:
                return _COHERENT
            for token, cap in self._mapping.items():
                if token in prompt:
                    if token in self._fail:
                        raise RuntimeError("the worker hit an error mid-build")
                    if self._hold is not None:
                        self._hold.wait(timeout=10)
                    return _built(cap)
            return _built("misc")
        return t

    def _file(self, label: str, token: str, cap: str, fail: bool = False) -> tree.Node:
        node = tree.file_intent(f"schedule the {token or label} work")
        self._nodes[label] = node
        if token:
            self._mapping[token] = cap
            if fail:
                self._fail.add(token)
        return node

    # ── setup verbs ──────────────────────────────────────────────────────────────
    def _v_ready(self, args: list[str]) -> tuple[bool, str]:
        """ready <N> — file N independent ready asks, each its own standing leaf with nothing blocking."""
        for i in range(int(args[0])):
            self._file(str(i), _TOKENS[i], _CAPS[i])
        return True, ""

    def _v_blocked(self, args: list[str]) -> tuple[bool, str]:
        """blocked — file one ask blocked on an open decision child, so no ready work exists for it."""
        parent = self._file("blocked", "", "")
        tree.raise_card("an open question only you can settle", kind="decide", parent=parent.id)
        return True, ""

    def _v_blocked_sibling(self, args: list[str]) -> tuple[bool, str]:
        """blocked-sibling — a blocked parent (open decision child) beside a clear ready sibling leaf."""
        parent = self._file("blocked", "", "")
        tree.raise_card("an open question only you can settle", kind="decide", parent=parent.id)
        self._file("sibling", "SIBMARK", "sib")
        return True, ""

    def _v_failing(self, args: list[str]) -> tuple[bool, str]:
        """failing — two ready asks: one good worker, one whose worker errs before handing back."""
        self._file("good", "GOODMARK", "good")
        self._file("bad", "FAILMARK", "bad", fail=True)
        return True, ""

    # ── action verbs ─────────────────────────────────────────────────────────────
    def _v_run(self, args: list[str]) -> tuple[bool, str]:
        """run — run the loop to completion over the current tree, each ready node built and folded."""
        self._sched = schedule.Scheduler(transport=self._transport(), root=self.root, limit=2)
        self._drain()
        return True, ""

    def _v_step(self, args: list[str]) -> tuple[bool, str]:
        """step — one non-blocking pass over the current tree."""
        self._sched = schedule.Scheduler(transport=self._transport(), root=self.root, limit=2)
        self._sched.step()
        return True, ""

    def _v_dispatch(self, args: list[str]) -> tuple[bool, str]:
        """dispatch held — one pass that dispatches the ready work with the builds held in flight; the
        pass MUST return at once (off the operator's path) with both workers running."""
        if args[0] != "held":
            return False, f"unknown dispatch mode {args[0]!r}"
        self._hold = threading.Event()
        self._sched = schedule.Scheduler(transport=self._transport(), root=self.root, limit=2)
        t0 = time.time()
        self._sched.step()
        if time.time() - t0 > 2.0:
            return False, "the pass blocked on a held build — the loop did not run off the operator's path"
        if len(self._sched.running) != 2:
            return False, f"the pass dispatched {len(self._sched.running)} workers, expected 2"
        return True, ""

    def _v_release(self, args: list[str]) -> tuple[bool, str]:
        """release — release the held builds and drain the loop to completion."""
        if self._hold is not None:
            self._hold.set()
        self._drain()
        return True, ""

    # ── assertion verbs ──────────────────────────────────────────────────────────
    def _v_folded(self, args: list[str]) -> tuple[bool, str]:
        """folded <N|good|sibling> — N ready nodes (or the named one) integrated and left the work
        view, each delta folded into the one spec — work moved with no operator act."""
        a = args[0]
        if a.isdigit():
            for i in range(int(a)):
                if not self._cap(_CAPS[i]):
                    return False, f"the {_CAPS[i]} delta did not fold into the one spec"
                if not self._is_folded(self._nodes[str(i)]):
                    return False, f"the node for {_CAPS[i]} did not leave the work view"
            return True, ""
        named = {"good": ("good", "good"), "sibling": ("sib", "sibling")}
        if a not in named:
            return False, f"unknown folded subject {a!r}"
        cap, label = named[a]
        if not self._cap(cap):
            return False, f"the {a} delta did not fold into the one spec"
        return ((True, "") if self._is_folded(self._nodes[label])
                else (False, f"the {a} node did not leave the work view"))

    def _v_flight(self, args: list[str]) -> tuple[bool, str]:
        """flight <N> — N nodes are in flight at the same time — the ready work consumed concurrently."""
        n = int(args[0])
        if not self._wait(lambda: self._live_count() == n):
            return False, f"expected {n} nodes in flight at once, saw {self._live_count()}"
        return True, ""

    def _v_fences(self, args: list[str]) -> tuple[bool, str]:
        """fences distinct — each in-flight worker builds in its own distinct, live worktree."""
        if args[0] != "distinct":
            return False, f"unknown fences assertion {args[0]!r}"
        nodes = [tree.find(i) for i in self._sched.running]
        paths = [worker._tree_path(n, self.root) for n in nodes if n]
        if not self._wait(lambda: all(os.path.isdir(p) for p in paths)):
            return False, "a worker is not building in its own worktree"
        if len(paths) < 2 or len(set(paths)) != len(paths):
            return False, "the fences are not distinct"
        return True, ""

    def _v_off_main(self, args: list[str]) -> tuple[bool, str]:
        """off-main — no fence's material reaches the main line while it builds (the fence holds)."""
        rc = subprocess.run(["git", "cat-file", "-e", "HEAD:RESULT.md"], cwd=self.root,
                            capture_output=True).returncode
        return (True, "") if rc != 0 else (False, "a fence's material reached the main line")

    def _v_rests(self, args: list[str]) -> tuple[bool, str]:
        """rests — the loop dispatched no worker and is idle (nothing was ready)."""
        return ((True, "") if not self._sched.running
                else (False, "the scheduler dispatched a worker with no ready work"))

    def _v_unready(self, args: list[str]) -> tuple[bool, str]:
        """unready blocked — the blocked node is absent from the ready work the scheduler reads."""
        if args[0] != "blocked":
            return False, f"unknown unready subject {args[0]!r}"
        bid = self._nodes["blocked"].id
        return ((True, "") if bid not in {n.id for n in tree.ready()}
                else (False, "the blocked node is in the ready work"))

    def _v_idle(self, args: list[str]) -> tuple[bool, str]:
        """idle blocked — no worker ran on the blocked node; it never went in flight."""
        if args[0] != "blocked":
            return False, f"unknown idle subject {args[0]!r}"
        b = self._nodes["blocked"]
        if b.id in self._sched.running:
            return False, "a worker ran on the blocked node"
        st = tree.find(b.id)
        return (True, "") if st and st.state != tree.IN_FLIGHT else (False, "the blocked node went in flight")

    def _v_decision(self, args: list[str]) -> tuple[bool, str]:
        """decision raised — the failed worker's node carries a could-not-complete decision card."""
        if args[0] != "raised":
            return False, f"unknown decision assertion {args[0]!r}"
        bad = self._nodes["bad"]
        cards = [c for c in tree.cards()
                 if c.parent == bad.id and c.kind == "decide" and "could not complete" in c.text]
        return (True, "") if cards else (False, "no could-not-complete decision was raised on the failed node")

    def _v_fence(self, args: list[str]) -> tuple[bool, str]:
        """fence gone — the failed worker's fence is torn down (no leaked worktree)."""
        if args[0] != "gone":
            return False, f"unknown fence assertion {args[0]!r}"
        bad = self._nodes["bad"]
        return ((True, "") if not os.path.isdir(worker._tree_path(bad, self.root))
                else (False, "the failed worker's fence leaked"))

    def _v_recovered(self, args: list[str]) -> tuple[bool, str]:
        """recovered — the failed node left IN_FLIGHT — not stranded in flight with no live worker."""
        bad = self._nodes["bad"]
        st = tree.find(bad.id)
        return (True, "") if st and st.state != tree.IN_FLIGHT else (False, "the failed node is stranded in flight")

    def _v_loop(self, args: list[str]) -> tuple[bool, str]:
        """loop idle — the scheduler survived the failure and is idle (it kept serving, never crashed)."""
        if args[0] != "idle":
            return False, f"unknown loop assertion {args[0]!r}"
        return (True, "") if self._sched.running == [] else (False, "the scheduler is not idle after the failure")

    def _v_total(self, args: list[str]) -> tuple[bool, str]:
        """total — dispatch was total: every node the scheduler dispatched resolved to exactly one
        terminal — folded, or escalated as a decision card on it — and none is left in flight with no
        live worker. The one positive invariant the per-node assertions above each witness half of."""
        running = set(self._sched.running)
        for node in tree.read_tree():
            if node.is_live and node.id not in running:
                return False, f"a node is stranded in flight with no live worker: {node.id}"
        cards = tree.cards()
        for label, node in self._nodes.items():
            st = tree.find(node.id)
            folded = st is not None and st.folded
            escalated = any(c.parent == node.id and c.kind == "decide" for c in cards)
            if folded == escalated:                          # exactly one terminal — never both, never neither
                return False, (f"the {label} node did not reach exactly one terminal "
                               f"(folded={folded}, escalated={escalated})")
        return True, ""

    # ── internals ────────────────────────────────────────────────────────────────
    def _cap(self, name: str) -> bool:
        return spec.read_spec(self.root).capability(name) is not None

    def _is_folded(self, node: tree.Node) -> bool:
        return any(n.id == node.id and n.folded for n in tree.read_tree())

    def _live_count(self) -> int:
        return len([n for n in tree.read_tree() if n.is_live])

    def _wait(self, cond, timeout: float = 8.0) -> bool:
        end = time.time() + timeout
        while time.time() < end and not cond():
            time.sleep(0.01)
        return cond()

    def _drain(self) -> None:
        for _ in range(400):
            self._sched.step()
            if not self._sched.running:
                return
            time.sleep(0.02)

    def teardown(self) -> None:
        if self._hold is not None:
            self._hold.set()                               # release any held build so no thread outlives the fixture
        if self._sched is not None:
            try:
                self._drain()
            except Exception:
                pass
        if self._prev_root is None:
            os.environ.pop("ENGINE_ROOT", None)
        else:
            os.environ["ENGINE_ROOT"] = self._prev_root
        shutil.rmtree(self.root, ignore_errors=True)
