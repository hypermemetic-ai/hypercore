"""Slice 16 — the autonomy seam: the scheduler consumes the ready frontier.

Acceptance (spec/schedule, intent §60/§62/§110): a ratified ask is *built*, not left standing while
the system idles. `graph.ready` computed the frontier; this slice builds the loop that consumes it —
`worker.run` (delegate → build fenced → integrate → fold), wired off the operator's path and driven by
the scheduler. The check drives the real scheduler, the real graph, real fences, and a real fold over
a scripted transport (no LLM — the honest harness limit: a live `claude` loading is the watched
evidence, never faked here), pinning the four properties that close the §60 defect:

1. **continuous** — a standing ask is taken, built, integrated, and folds, with no operator act; the
   §60 defect (idle with unblocked work) cannot occur, and the system rests only on a decision;
2. **concurrent on one record** — two ready nodes run two workers at once in distinct fences, neither's
   build blocks the other, and each folds its own delta into the one spec (the single-writer line);
3. **readiness gates scheduling** — a standing node blocked on an open child is not in the frontier and
   is not taken (intent §110);
4. **off the operator's path / failure as a decision** — `step` returns at once while builds run, and a
   worker that errs returns a decision card on its node while the loop keeps serving the rest.

This is run on its own isolated root, not the shared check root: the scheduler consumes the *whole*
graph's frontier, so it must not reach into the sibling slices' leftover standing work.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import threading
import time

from .harness import ok


def check(_shared_root: str) -> None:
    from .. import graph, schedule, spec, worker

    print("\nslice 16 — acceptance check  (the autonomy seam: the scheduler runs the frontier)\n")

    root = tempfile.mkdtemp(prefix="engine-check-slice16-")
    os.environ["ENGINE_ROOT"] = root                 # isolate: the scheduler reads the whole frontier
    for cfg in (["init", "-q"], ["config", "user.email", "c@h"], ["config", "user.name", "c"]):
        subprocess.run(["git", *cfg], cwd=root, check=True)

    loop = {"command": "python3 -m engine --check", "red": "absent — failed", "green": "present — passed"}

    def built(cap: str) -> str:
        return json.dumps({"report": f"built {cap}",
                           "delta": f"## ADDED — {cap}\n### Requirement: {cap} holds\n"
                                    f"The {cap} capability MUST hold.\n#### Scenario: s\n"
                                    f"- WHEN x\n- THEN y\n", "loop": loop})

    coherent = json.dumps({"coherent": True, "say": "it landed.", "card": None})

    def transport_for(mapping, hold=None, fail=frozenset()):
        """A prompt-keyed scripted transport, safe under concurrency: the architect's coherence pass
        is answered coherent; a worker build is matched to its capability by a token in its ask. `hold`
        blocks a build until released (to observe two in flight at once); `fail` raises mid-build."""
        def t(prompt: str) -> str:
            if "archiving a worker" in prompt:
                return coherent
            for token, cap in mapping.items():
                if token in prompt:
                    if token in fail:
                        raise RuntimeError("the worker hit an error mid-build")
                    if hold is not None:
                        hold.wait(timeout=10)
                    return built(cap)
            return built("misc")
        return t

    def wait_until(cond, timeout=8.0) -> bool:
        end = time.time() + timeout
        while time.time() < end and not cond():
            time.sleep(0.01)
        return cond()

    def drain(sched) -> None:
        for _ in range(400):
            sched.step()
            if not sched.running:
                return
            time.sleep(0.02)

    live = lambda: [n for n in graph.read_graph() if n.is_live]
    folded = lambda i: any(n.id == i and n.folded for n in graph.read_graph())

    # ── 1 & 2. continuous + concurrent + off the operator's path ──────────────────────────────────
    # Two standing asks, both held in their builds at once, so we can see them in flight together —
    # concurrency — while `step` returns at once — off the operator's path. Releasing lets each
    # integrate and fold its own delta into the one spec — continuity, end to end.
    release = threading.Event()
    a = graph.file_intent("schedule the ALPHAMARK work")
    b = graph.file_intent("schedule the BETAMARK work")
    sched = schedule.Scheduler(
        transport=transport_for({"ALPHAMARK": "alpha", "BETAMARK": "beta"}, hold=release),
        root=root, limit=2)

    t0 = time.time()
    sched.step()                                     # dispatches both; the builds block on `release`
    ok(time.time() - t0 < 2.0 and len(sched.running) == 2,
       "step dispatches the frontier and returns at once — two workers run, off the operator's path")
    ok(wait_until(lambda: len(live()) == 2),
       "both ready nodes go in flight at the same time — the frontier is consumed concurrently (§62)")
    ta, tb = worker._tree_path(a, root), worker._tree_path(b, root)
    ok(wait_until(lambda: os.path.isdir(ta) and os.path.isdir(tb)) and ta != tb,
       "each worker builds in its own fence — distinct, isolated worktrees coexisting")
    off_main = subprocess.run(["git", "cat-file", "-e", "HEAD:RESULT.md"], cwd=root,
                              capture_output=True, text=True).returncode
    ok(off_main != 0, "neither fence's material reaches the main line while it builds")

    release.set()                                    # let both finish: integrate, fold, tear down
    drain(sched)
    sp = spec.read_spec(root)
    ok(sp.capability("alpha") is not None and sp.capability("beta") is not None,
       "each worker folds its own delta into the one spec — concurrent advance, serialized integration")
    ok(folded(a.id) and folded(b.id),
       "both asks integrated and left the work view — work moved with no operator act (§60 continuity)")

    # ── 3. readiness gates scheduling: a node blocked on an open child is not taken (§110) ─────────
    parent = graph.file_intent("a parent ask with a question beneath it")
    graph.raise_card("an open question only you can settle", kind="decide", parent=parent.id)
    ok(parent.id not in {n.id for n in graph.ready()},
       "a standing node blocked on an open child is absent from the ready frontier (§110)")
    idle = schedule.Scheduler(transport=transport_for({}), root=root, limit=2)
    idle.step()
    ok(parent.id not in idle.running and not idle.running,
       "the scheduler runs no worker on the blocked node, and rests — not idle-with-work, a decision")

    # ── 4. off-path failure: a worker that errs returns a decision and the loop keeps serving ──────
    good = graph.file_intent("schedule the GOODMARK work")
    bad = graph.file_intent("schedule the FAILMARK work")
    sched2 = schedule.Scheduler(
        transport=transport_for({"GOODMARK": "good", "FAILMARK": "bad"}, fail={"FAILMARK"}),
        root=root, limit=2)
    sched2.step()
    drain(sched2)
    ok(spec.read_spec(root).capability("good") is not None,
       "a good worker folds while its sibling fails — the loop kept serving the rest, no crash")
    fail_cards = [n for n in graph.cards() if n.parent == bad.id and n.kind == "decide"]
    ok(bool(fail_cards) and "could not complete" in fail_cards[0].text,
       "a worker that cannot complete returns as a decision on its node — never a silent stall")
    ok(sched2.running == [],
       "the loop survived the failure and is idle — a fault never stopped the scheduler")
