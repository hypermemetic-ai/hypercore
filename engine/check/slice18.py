"""Slice 18 — failure paths recover the node and tear the fence down (C2, H3).

Acceptance (spec/schedule §off-path-failure, spec/worker §fence): a worker crossing that does NOT
integrate is the *steady-state* path, not an edge — every folding-condition block, coherence fail, and
malformed model reply returns not-done. The prior code tore the fence down only on `reply.done`, so on
every refusal the worktree and branch **leaked** and the node sat `IN_FLIGHT` forever — not standing,
not a card, dropped on the next restart (research C2). This slice drives a worker down each refusal
path and a worker whose model returns garbage (H3), asserting:

1. **the fence is torn down on a refusal** — no leaked worktree dir, no leaked branch, on the
   non-done path. *RED if teardown is gated behind `reply.done`.*
2. **the node recovers off IN_FLIGHT** — it returns to standing (its decision card blocks re-dispatch),
   never stranded in flight with no live worker. *RED if the node is left IN_FLIGHT.*
3. **a malformed model reply is a failure, not a silent no-op success** — an empty/unparseable reply
   does not fold a no-op as a clean success; it takes the failure path and recovers. *RED if the
   empty-reply→done fallback folds.*
4. **the loop keeps serving and the fence is gone** — driven through the real scheduler, a refusing
   worker raises its decision and the scheduler is idle with no leaked fence.
"""
from __future__ import annotations

import os
import subprocess
import tempfile

from .harness import ok


def _init(prefix: str) -> str:
    root = tempfile.mkdtemp(prefix=prefix)
    for cfg in (["init", "-q"], ["config", "user.email", "c@h"], ["config", "user.name", "c"]):
        subprocess.run(["git", *cfg], cwd=root, check=True)
    return root


def _branch_exists(root: str, branch: str) -> bool:
    return subprocess.run(["git", "rev-parse", "--verify", "--quiet", branch],
                          cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def check(_shared_root: str) -> None:
    from .. import tree, worker

    print("\nslice 18 — acceptance check  (failure paths recover the node, the fence never leaks)\n")

    # ── 1 & 2. a folding-condition refusal recovers the node and tears the fence down ────────────────
    # A behavior-changing delta with NO loop is refused by `conditions.unmet` — the common refusal. The
    # worker crossing returns not-done; the fence must be gone and the node must have left IN_FLIGHT.
    root = _init("engine-check-s18a-")
    os.environ["ENGINE_ROOT"] = root
    tree.commit([os.path.join(root, "spec")], "seed: empty spec") if os.path.isdir(
        os.path.join(root, "spec")) else None

    node = tree.file_intent("a worker whose result cannot fold")
    no_loop = (
        '{"report": "built it", '
        '"delta": "## ADDED — newcap\\n### Requirement: it holds\\nThe newcap MUST hold.\\n'
        '#### Scenario: s\\n- WHEN x\\n- THEN y\\n", '
        '"loop": {"command": "", "red": "", "green": ""}}')          # behavior change, no loop → refuse
    reply = worker.run(node, transport=lambda _p: no_loop, root=root)
    ok(not reply.done, "a behavior-changing result with no loop is refused — the crossing returns not-done")
    fence = worker._tree_path(node, root)
    ok(not os.path.isdir(fence),
       "the fence is torn down on a refusal — no leaked worktree (C2)")
    ok(not _branch_exists(root, worker._branch(node)),
       "the worker branch is deleted on a refusal — no leaked branch (C2)")
    after = tree.find(node.id)
    ok(after is not None and after.state != tree.IN_FLIGHT,
       "the node leaves IN_FLIGHT on a refusal — not stranded in flight with no live worker (C2)")
    cards = [c for c in tree.cards() if c.parent == node.id]
    ok(bool(cards),
       "a decision card is raised on the node — the refusal is recoverable, not a silent drop")

    # ── 3. a malformed model reply is a failure, not a silent no-op success (H3) ─────────────────────
    # A reply with no JSON object is the dangerous case: the old lenient parse degraded it to
    # {"say": raw, "done": True} → empty report/delta/loop → a trivial delta that `unmet` passes → a
    # no-op folded as a clean success, indistinguishable from a real minimal result. The worker now
    # reads its hand-off STRICTLY (`parse_object`): a malformed reply raises at apply, BEFORE coherence
    # is ever consulted — so the guard is not incidental to the coherence parse happening to fail.
    from ..transport import MalformedReply
    root = _init("engine-check-s18b-")
    os.environ["ENGINE_ROOT"] = root
    garbage = tree.file_intent("a worker whose model returns garbage")
    apply_raised = False
    try:
        worker.context(garbage, root)                                # grounding ok
        worker.apply(garbage, transport=lambda _p: "prose, not a JSON object at all", root=root)
    except MalformedReply:
        apply_raised = True
    ok(apply_raised,
       "a reply with no JSON object raises MalformedReply at apply — not a foldable no-op (H3)")

    # and end to end through the crossing: the malformed reply recovers the node and tears the fence
    # down (the C2 path), never folding a silent success.
    garbage2 = tree.file_intent("another worker whose model returns nothing structured")
    raised = False
    try:
        reply2 = worker.run(garbage2, transport=lambda _p: "still no object here", root=root)
        done = reply2.done
    except MalformedReply:
        raised, done = True, False
    ok(raised and not done,
       "a malformed model reply takes the failure path through the crossing — never a clean fold (H3)")
    g2 = tree.find(garbage2.id)
    ok(g2 is not None and g2.state != tree.IN_FLIGHT,
       "a worker whose model fails recovers off IN_FLIGHT — the fence's failure is not a silent success")
    ok(not os.path.isdir(worker._tree_path(garbage2, root)),
       "the fence is torn down when the model reply is malformed — no leak on the error path (H3+C2)")

    # ── 4. through the real scheduler: a refusing worker is a decision, the fence is gone, loop idle ──
    from .. import schedule
    root = _init("engine-check-s18c-")
    os.environ["ENGINE_ROOT"] = root
    n = tree.file_intent("a scheduled worker whose result cannot fold")
    sched = schedule.Scheduler(transport=lambda _p: no_loop, root=root, limit=1)
    sched.step()
    for _ in range(400):
        sched.step()
        if not sched.running:
            break
        import time
        time.sleep(0.02)
    ok(sched.running == [], "the scheduler is idle after the refusal — the loop survived and kept serving")
    ok(not os.path.isdir(worker._tree_path(n, root)),
       "no fence leaks through the scheduler on a refusal — steady-state failure leaves no debris (C2)")
    nn = tree.find(n.id)
    ok(nn is not None and nn.state != tree.IN_FLIGHT,
       "the scheduled node recovers off IN_FLIGHT — never stranded across the scheduler's life")

    # ── 5. a crash-stranded IN_FLIGHT node (no live worker) is recovered on the next step (C2) ───────
    # Simulate a process killed mid-crossing: a node IN_FLIGHT on disk with no worker thread. A fresh
    # scheduler's step must return it to standing, never leave it a lie or drop it silently on restart.
    root = _init("engine-check-s18d-")
    os.environ["ENGINE_ROOT"] = root
    stranded = tree.file_intent("a node a crash left in flight")
    tree.dispatch(stranded)                                         # IN_FLIGHT on disk, no live worker
    ok(tree.find(stranded.id).state == tree.IN_FLIGHT, "the node is in flight on disk before recovery")
    fresh = schedule.Scheduler(transport=lambda _p: no_loop, root=root, limit=0)  # limit 0: only recover
    fresh.step()
    rs = tree.find(stranded.id)
    ok(rs is not None and rs.state != tree.IN_FLIGHT,
       "a crash-stranded IN_FLIGHT node with no live worker is recovered to standing on the next step (C2)")
