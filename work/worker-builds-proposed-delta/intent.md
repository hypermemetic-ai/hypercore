---
kind: ask
state: standing
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
