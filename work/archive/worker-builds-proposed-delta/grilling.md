surfaced: 0

[CONTRACT]
A worker only ever applies a delta the architect proposed. The guarantee is enforced at the worker boundary: `worker.run` refuses any node that carries no architect-proposed delta — it raises one parented decision card (propose one, abandon, or change the ask) and builds nothing, the node staying standing and blocked rather than going live. Because the boundary is total, the silent author-from-scratch fallback is deleted, not guarded: `worker._touched` no longer returns every capability and `worker.prompt` no longer tells the worker to author the delta from a full scan, so the builder can never author its own delta or the scenarios that clear its own fold. Every node that can be built carries an architect-proposed delta whatever door it entered: a below-floor ask now files to standing work carrying the architect's propose product (contract and delta), skipping only the operator interview; a hand-authored standing node carries one as material. A delta the architect proposed and judged trivial still builds; only a delta never proposed is refused. A worker still authors its scenario fixtures — that new-verb adequacy stays `gate-vouches-for-the-new-verb`'s, untouched.

[DELTA]
## ADDED — worker
### Requirement: a worker only ever applies an architect-proposed delta
A worker MUST be handed a node that carries an **architect-proposed delta** — the propose stage is the
architect's, never the worker's. `worker.run` MUST refuse, at the worker boundary **before it dispatches
the node**, any node that carries no architect-proposed delta (no resolved propose product, the
`grill.entry_of` reachability): it raises **one** parented decision card on the operator's queue — naming
that the node carries no architect-proposed delta and the operator's fork (propose one, abandon, or
change the ask) — and **builds nothing**, leaving the node standing and blocked on that card rather than
going live. This boundary is the **one place** the guarantee is enforced, so every door into a worker is
covered alike — the autonomous scheduler and the bare hand-driven `worker.run(tree.find(id))` the
totality requirement names. Because the boundary refuses a node with no proposed delta, the worker's
grounding assembly is **total**: there is no author-from-scratch path left. The former fallback —
`worker._touched` returning every capability and `worker.prompt` telling the worker to author the delta
from the full scan when none was handed — is **deleted, not guarded**: with the boundary total,
`worker._touched` of an empty delta names no capability, and the worker never authors its own delta nor
the scenarios that would clear its own fold. A delta the architect proposed and judged **trivial** (a
valid no-op, `delta.Delta.trivial`) is still a proposed delta and still builds; only a delta **never
proposed** is refused. (The scenario's verbs: `no-delta dispatched` runs `worker.run` on a node carrying
no propose product; `surfaces decision` asserts exactly one parented decision card naming the missing
architect-proposed delta; `builds nothing` asserts the node neither folded nor went live; `fallback
gone` asserts `worker._touched` of an empty delta names no capability — the deleted branch.)

#### Scenario: a node with no architect-proposed delta surfaces and builds nothing
- WHEN a worker crossing is run on a node that carries no architect-proposed delta
- THEN `worker.run` raises one parented decision card naming the missing architect-proposed delta and
  builds nothing — the node stays standing, not live and not folded — and the author-from-scratch
  fallback in `worker._touched`/`worker.prompt` is gone, so an empty delta names no capability to scan

  ```check
  no-delta dispatched
  surfaces decision
  builds nothing
  fallback gone
  ```

## MODIFIED — grilling
### Requirement: a filed ask is grilled before it becomes work
An ask that opens real choices MUST pass a grilling floor before spawning work: the architect resolves
every decision it can from the living spec and intent, and only a residual decision the operator has a
stake in keeps the ask above the floor. An ask whose every decision is already determined files straight
to standing work without an operator interview — but the architect still **proposes its delta**: a
below-floor ask files as standing work carrying the architect's propose product (the contract and the
spec delta), authored with no question surfaced, so it is buildable yet **never reaches a worker without
an architect-proposed delta**. The propose stage is the architect's on every door; only the operator
interview is skipped below the floor. The floor is a standing guard, not a front gate — the same test
re-fires whenever a stake-bearing choice surfaces mid-work.

#### Scenario: above the floor
- WHEN a filed ask leaves a stake-bearing decision open after the machine resolves
  what it can from intent and the spec
- THEN the ask is held and grilled, and no standing work exists for it yet

  ```check
  ask above-floor
  held grilled
  standing none
  ```

#### Scenario: below the floor
- WHEN every decision a filed ask needs is already determined by intent or the spec
- THEN it files directly as standing work, carrying the architect's proposed delta (its propose
  product), with no operator interview surfaced

  ```check
  ask below-floor
  filed standing
  proposed delta
  ```
