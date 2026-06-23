"""Slice 8 — residue: the concurrent-isolation half, awaiting the concurrency seam's one home.

The design-it-twice half of this slice — the contest, candidates-design-not-implement, the
machine-side selection and recorded pick, and a stake-bearing difference re-entering grilling — has
migrated to `design-it-twice`'s own executable scenarios (`spec/design-it-twice.md`,
`engine/worlds/design_it_twice_world.py`). The selection-prompt-names-the-three-axes invariant is a
watched check in `engine/check/scenarios.py`.

What stays is assertion #1: **concurrent workers advance one tree in isolation, each folding its own
delta**. This is not design-it-twice's own behavior — it is the cross-cutting single-writer-line proof,
the same promise described in `spec/worker.md` ("concurrent workers advance the tree in isolation") and
`spec/schedule.md` ("work runs concurrently on one record") and proved again in slice 17. It stays
by-slice until that concurrency proof is given one executable home (the open seam decision), at which
point this file dissolves like the others. Driven over the real tree, real fences, and a real
node-record write, deterministically with scripted transports.
"""
from __future__ import annotations

import json
import os
import subprocess

from .harness import ok, scripted


def check(root: str) -> None:
    from .. import communication, tree, spec, worker

    print("\nslice 8 — acceptance check  (residue: concurrent isolation, each worker folds its delta)\n")

    coherent = lambda: scripted(json.dumps({"coherent": True, "say": "it landed.", "card": None}))

    def built(cap: str, report: str) -> str:
        return json.dumps({"report": report,
                           "delta": f"## ADDED — {cap}\n### Requirement: {cap} holds\n"
                                    f"The {cap} capability MUST hold.\n#### Scenario: s\n"
                                    f"- WHEN x\n- THEN y\n"})

    def staged(text: str, cap: str, root: str) -> tree.Node:
        ask = tree.file_intent(text)
        tree.approve(tree.raise_card(
            f"contract.\n\ndelta:\n## ADDED — {cap}\n### Requirement: {cap} holds\n"
            f"The {cap} capability MUST hold.\n#### Scenario: s\n- WHEN x\n- THEN y\n",
            kind="decide", parent=ask.id))
        worker.worktree(ask, root)
        tree.dispatch(ask)
        return ask

    def log(branch: str) -> str:
        return subprocess.run(["git", "log", "--oneline", branch], cwd=root,
                              capture_output=True, text=True).stdout

    # ── concurrent workers advance one tree in isolation, each folding its delta ──
    a = staged("concurrent work A", "alpha", root)
    b = staged("concurrent work B", "beta", root)
    ta, tb = worker._tree_path(a, root), worker._tree_path(b, root)
    ok(os.path.isdir(ta) and os.path.isdir(tb) and ta != tb,
       "two workers hold two distinct fences at once — concurrent, isolated")

    ra = worker.apply(a, scripted(built("alpha", "built A")), root)
    rb = worker.apply(b, scripted(built("beta", "built B")), root)
    ok("worker: result" in log(f"worker/{a.id}") and "worker: result" in log(f"worker/{b.id}"),
       "each worker's commit reaches the record on its own branch")
    off_main = subprocess.run(["git", "cat-file", "-e", "HEAD:RESULT.md"], cwd=root,
                              capture_output=True, text=True).returncode
    ok(off_main != 0, "neither fence's material reaches the main line — the fence holds for both")

    communication.integrate(a, ra, coherent(), root)
    communication.integrate(b, rb, coherent(), root)
    sp = spec.read_spec(root)
    ok(sp.capability("alpha") is not None and sp.capability("beta") is not None,
       "each worker folds its own delta into the one spec — concurrent advance, no interference")
    worker.teardown(a, root)
    worker.teardown(b, root)
