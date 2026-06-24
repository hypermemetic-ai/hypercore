---
kind: ask
state: folded
owner: operator
created: 2026-06-23
folded: 2026-06-23
---
# dispatch-totality — gate "every dispatched worker resolves to exactly one terminal"

`schedule` already promises a worker "never silently dropping the node" — two negatives, untestable.
The actor-model reading sharpens it to a positive invariant: **dispatch is total — every worker the
scheduler spawns resolves to exactly one terminal (folded or escalated); no node sits in flight
without a live worker.** This is xstate's `invoke` totality (onDone xor onError), the property a
hand-rolled loop loses first. This move sharpens the requirement's prose to that claim **and** authors
the executable scenario that gates it: the architect authors the WHEN/THEN and the check block, so the
side that does not build it owns the oracle (`grilling` / `scenario-gate`).

## open decision — red→green or regression guard
Whether the engine already satisfies totality — then the scenario is a **watched→gated regression
guard**, green on arrival, kept as a standing assertion the way `slice15`'s green half is — or a gap
exists, then it is a real **red→green** build (an in-flight node *can* strand on a worker that errs
between dispatch and resolve). **Lean:** inspect `engine/schedule.py` + `engine/worker.py` first; the
spec's existing "never dropping the node" suggests it is largely met, so likely a regression guard —
but wiring an end-to-end seam is exactly where hypercore has twice found latent bugs the harness never
exercised (the slice-16 integrate-transport drop). **Flip:** inspection finds a worker that faults
between dispatch and resolve leaves the node wedged in flight — a real bug and a genuine red→green.
This is the residue whose answer needs the code, which is why this child is the lean to execute first. [machine]

## folding condition
- the schedule requirement's prose carries the totality invariant, and a `#### Scenario:` with an
  executable check block gates it — red→green if a gap is found and built, a green standing assertion
  if already met (recorded honestly as such, never faked);
- `python3 -m engine --check` is green. [machine]

## result — built, green, awaiting acceptance (2026-06-23)

Inspection resolved the residue: the engine is **already total**, so this is a **green regression
guard**, not a red→green — recorded honestly (the self-model's watched→gated discipline, never faked),
no transition manufactured. The proof, traced in the engine:
- `worker.run` (`engine/worker.py`) dispatches at entry and tears the fence down in a `finally`; on a
  refused/incoherent integrate or any exception it `recover`s the node to standing — so on every exit
  the node is folded or recovered, never left in flight.
- `Scheduler._work` (`engine/schedule.py`) escalates a faulting worker to a `decide` card; the
  recovered node then carries an open decision child, so `tree.ready` will not re-dispatch it.
- `_recover_stranded` catches the one bypass — a process killed mid-crossing — returning a node left
  in flight with no live thread to standing.

What landed (the delta, hand-applied — the build has been hand-authored throughout this repo):
- `spec/schedule.md` — the failure requirement sharpened **in place** to the dispatch-is-total
  invariant (replacing "never crashing and never silently dropping the node"); a new
  `#### Scenario: dispatch is total` gates it.
- `engine/worlds/schedule_world.py` — the `total` verb: over the mixed good+failing run, every
  dispatched node reaches exactly one terminal (folded XOR escalated) and none is stranded in flight.
- `engine/schedule.py` — the module docstring sharpened to match (coherence).

`python3 -m engine --check` is green; schedule reads **4 gated, 0 watched**. Folding condition met.
Awaiting the operator's acceptance to fold (apply the delta + archive the node); not committed. [machine]
