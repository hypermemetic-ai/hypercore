# ADR 0002 — intent extraction folds into conversation and queue

Status: machine-owned, awaiting ratification. [machine]

## Context

Slice 3 builds intent extraction by grilling: the floor, the
one-question-at-a-time interview, the four products, and the gate that holds work
until the operator ratifies the view entry. ADR 0001 anticipated this behavior as a
sixth capability ("later slices add ... grilling/extraction"). The seam had to be
cut one way or the other — a new top-level capability, or requirements folded into
the existing five — because it sets the operator view's top level.

## Decision

Intent extraction is **not** its own capability. Its requirements fold into the two
capabilities that already own the surfaces it acts on:

- **conversation** — the floor and the grilling interview: the architect
  resolves every decision it can, surfaces the residual stake-bearing ones one at a
  time, and produces the contract and the spec delta.
- **queue** — the grilling question card (carrying its lean and what would flip it)
  and the gate: work does not spawn until the view entry is ratified.

The operator made this call during the slice's own grilling, superseding ADR 0001's
expectation of a sixth capability.

## Grounds

Grilling has no surface of its own: it speaks through the architect and lands
on the queue. A sixth capability would duplicate those two boundaries rather than
draw a new one, and split one coherent behavior across a seam checks could not stand
on. The five-capability spine of ADR 0001 holds; this ADR records that extraction was
placed within it, not beside it.

## Consequences

The operator view stays five units wide. The fold machinery (slice 2) is unchanged:
the slice-3 delta only ADDS requirements to existing capabilities, which `delta.fold`
already applies — no new-capability path is needed. A future change that does spin
extraction out into its own capability carries an ADR superseding this one.
