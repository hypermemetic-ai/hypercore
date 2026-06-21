# ADR 0004 — folding-conditions is its own capability

Status: machine-owned, awaiting ratification. [machine]

## Context

Slice 5 builds the disciplines that keep the model true as enforced folding conditions
(rebuild-spec §7, §9.5): a behavior-changing graph cannot fold without a recorded red→green
feedback loop (§7.2), and no source file a graph grows may cross a low line-count budget
without a decision (§7.1). ADR 0001 forecast "folding-conditions" as a later capability. The
seam had to be cut one way — a new top-level capability, or requirements folded into the
existing six — because it sets the operator view's top level (ADR 0002 set the
counter-precedent of folding behavior into existing capabilities when it has no surface of
its own; ADR 0003 cut a new capability when it owns a surface none of the others do).

## Decision

Folding-conditions is **its own capability** — the seventh top-level unit, the boundary ADR
0001 anticipated. The self-model already owns two folding conditions about the *delta* (a
missing or mismatched delta cannot fold; the merge is atomic, both directions). The new
conditions are about a different subject: the **material a worker produced** — the feedback
loop it ran and the source it grew — not the delta's spec-currency. That different subject is
the clean boundary. The self-model keeps the delta and the atomic merge; folding-conditions
owns the gates on the produced material, run at the archive stage before the merge.

The delta condition (§3.3) is re-checked in the gate so the archive stage gives one verdict,
but it remains owned by the self-model — the gate calls it, it is not moved.

## Grounds

Folding-conditions owns a surface the other capabilities do not: the structural gate on a
worker's material — its loop and its module sizes — a concern distinct from both the delta
(self-model) and the operator-facing coherence judgment (conversation). Folding it into the
self-model would mix "what the model is and how its delta merges" with "what discipline the
produced code must meet"; folding it into conversation would put a structural, model-free gate
inside the operator-facing role. A clean boundary stands here, as it did for the worker (ADR
0003) and unlike extraction (ADR 0002).

The line-count budget is **400 lines**, a starting value to tune (§11), not a deep question.
It is keyed to length because length is what a long file costs a worker's window whatever each
line means; it is set low so deepening pressure is felt early. The condition is scoped to the
files a graph itself touched — "the god-file cannot re-accrete one quiet edit at a time."

## Consequences

The operator view is seven units wide: `interface`, `graph`, `queue`, `conversation`,
`self-model`, `worker`, `folding-conditions`. The gate runs at `conversation.integrate`,
before `delta.fold`: an unmet condition raises a decision and the work stays live, rather than
folding. The acceptance harness (`hyper/check.py`) is itself approaching the budget and is the
first candidate for the per-slice split the discipline asks for, when a graph next touches it.
A future change that re-cuts these boundaries carries an ADR superseding this one.
