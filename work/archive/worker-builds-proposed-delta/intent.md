---
kind: ask
state: done
owner: operator
created: 2026-06-24
---
# worker-builds-proposed-delta — a worker only ever applies an architect-proposed delta

The crossing is meant to be **propose (architect) → apply (worker) → archive (architect)**, one
delta end to end (`spec/worker.md`). But a worker dispatched on a node that carries **no** delta
silently falls back to authoring the delta itself from a full scan (`worker._touched` returns every
capability; `worker.prompt` tells it "author it from the full scan"). That fallback:

- **triggers invisibly** — it engages whenever a node reaches dispatch with no grilling artifacts:
  a **below-floor ask** (`grill.consider` files it straight to work with no delta — `spec/grilling.md`
  intends exactly this: "files straight to standing work, ungrilled"), or a **hand-authored standing
  node** (an `intent.md` that never went through grilling). No card, no decision — it just builds.
- **breaks the anti-self-judging invariant** — with no handed delta the worker authors its own
  scenarios (its delta carries `#### Scenario:` blocks with `check` fences), so the builder writes the
  very oracle that clears its own fold. The whole design rests on the *architect* authoring scenarios
  ("the builder never authors the check that clears it" — `spec/coherence.md`, `engine/scenario.py`).

The operator's intent: a worker must never silently author its own delta. A node that reaches a worker
without an architect-proposed delta must surface, not build.

## the integrity stack (one of three composable nodes)
hypercore's self-verification rests on one claim — the description is the test, and the builder cannot
fake the verdict. It can fail three independent ways, each its own node; none subsumes another, and a
short-circuit at any layer defeats the whole:
- **proposer** — did the architect author the check (WHEN/THEN + verbs), or the builder? — *this node*
- **run** — did the mechanism actually run and leave a trail, or is the record hand-faked? — `a-record-a-load-bearing`
- **adequacy** — when it ran, did the check test the property, or a builder-authored proxy? — `gate-vouches-for-the-new-verb`
This node owns the **proposer** layer: that the *delta and its scenarios* come from the architect, not the
worker. It does **not** reach below the verb — even fully built, the worker still authors the scenario
*fixtures* (the `_v_<verb>` world methods) under the architect's verb names, and that artifact's adequacy
is `gate-vouches-for-the-new-verb`'s, not this node's. So scope the claim precisely: a worker authors no
*delta*; it may still author *fixtures*, which the adequacy node gates. The three touch shared seams
(`spec/worker.md`, the scenario gate in `conditions`/`scenario`): each must **ADD** its own requirement
rather than co-MODIFY a shared one (two MODIFYs of one requirement clobber at fold), or be sequenced on
another's tip — so three concurrent fences compose.

## The interface decision to design
Where in the system is the guarantee "a worker only ever applies an architect-proposed delta"
enforced, and what becomes of an ask that today reaches work with no delta (the below-floor ask, and
the hand-authored standing node)? The candidate seams in play: the grilling pass
(`grill.consider`/`grill.products`), the readiness predicate (`tree.ready`, which gates both spawning
and scheduling), and the worker boundary (`worker.run`/`worker.context`). Distinguish a delta that was
*never proposed* (the failure to catch) from one the architect proposed and judged *trivial* (a valid
no-op proposal — `delta.Delta.trivial`). The author-from-scratch fallback should be made unreachable
and deleted, not merely guarded.

## folding condition
- a worker never silently authors its own delta: a node reaching a worker with no architect-proposed
  delta surfaces (a decision or an equivalent visible state) and builds nothing; the author-from-scratch
  branches in `worker._touched`/`worker.prompt` are deleted;
- every node that *can* be built carries an architect-proposed delta (whatever door it entered through —
  including the below-floor ask), with the propose stage owned by the architect, not the worker;
- the touched capabilities (`spec/worker.md`, `spec/grilling.md`, and any seam the chosen design moves)
  carry the change with its scenarios, and `python3 -m engine --check` is green.

## Note — a suggestion from a prior grilling pass, not settled
Grilling surfaced that this node's guarantee (a worker only applies an architect-proposed delta) keeps
the operator's *touch* with the system only if the autonomous build is **legible** — the proposed plan
must reach the operator's eye through the view, not sit in a `grilling.md` they must hunt for. So
legibility lives in the view (`operator-view-readiness`), and a blocking approval gate is the wrong tool
(the operator wants to *see*, not *approve*). Leaning **view first, then this**, so removing the silent
author-from-scratch fallback never opens a window of autonomy the operator cannot see. Design work
remains; weigh in grilling, do not treat as a settled requirement. (See the matching note on
`operator-view-readiness`.)

## AX cross-reference — the orientation-cost symptom (machine, 2026-06-27)
An agent-experience sweep of the worker prompt measured this fallback's other face. With no handed
delta `worker._touched` foregrounds **every** capability body in full, so the assembled prompt is
~38,884 tokens (the whole spec) against ~12,275 for a one-capability change — the orientation cost
peaks exactly when the worker has the least direction. That length is a **symptom**; the load-bearing
defect is the one this node already owns — with no architect-proposed delta the worker authors its own
scenarios, so the builder writes the oracle that clears its own fold. Reachability confirmed both ways
the body names: the below-floor ask (`grill.consider` → `tree.file_intent`, no `grilling.md`, no
delta) and the hand-authored standing node. So the fix stays **delete the branch**, not shrink the
prompt: once every buildable node carries an architect-proposed delta, the no-delta foregrounding is
unreachable and goes with it. Touches the same seams as `work/worker-prompt-leads-with-the-task` and
`work/worker-disciplines-become-a-loadable-skill` (`worker.py`, `spec/worker.md`) — each ADDs a
distinct requirement rather than co-MODIFYing a shared one.
