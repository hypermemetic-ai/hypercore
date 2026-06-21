# ADR 0003 — the worker is its own capability; a fold can create a capability

Status: machine-owned, awaiting ratification. [machine]

## Context

Slice 4 builds the worker (rebuild-spec §6, §9.4): the system-facing half of the
conversationalist/worker split, fenced in its own worktree and grounded in its
capability's spec slice. ADR 0001 forecast "workers" as a later capability; ADR 0002
set the counter-precedent of folding a new behavior into the existing five rather than
widening the operator view. The seam had to be cut one way, because it sets the operator
view's top level.

## Decision

The worker is **its own capability** — the sixth top-level unit. The operator made this
call during the slice's grilling, against the lean's flip (fold into `conversation`).

The grounds the operator weighed: the worker owns a surface none of the five do — OS
isolation and the git-worktree fence, spec-scoped context, a system-facing audience — so
a clean boundary stands here in a way it did not for extraction (ADR 0002), which had no
surface of its own and spoke only through the conversationalist. Folding the worker into
`conversation` would have placed the system-facing role inside the operator-facing one —
the single capability it least belongs to, since the worker is defined by *not* being the
conversationalist.

A second decision follows from the first: a delta that ADDS a requirement in a capability
that does not yet exist now **creates** that capability on fold. ADR 0001 forecast that
the decomposition would grow by adding capabilities; this is the machinery that lets a
fold do so. A MODIFIED or REMOVED requirement in an absent capability is still a mismatch
and cannot fold.

## Grounds

The five-capability spine of ADR 0001 holds; this widens it to six along the boundary
ADR 0001 itself anticipated. Making capability-creation a fold operation keeps the rule
that the living spec is never separately edited — even the system's own growth into a new
capability happens as a fold carrying its delta, not as a hand edit.

## Consequences

The operator view is six units wide: `interface`, `graph`, `queue`, `conversation`,
`self-model`, `worker`. The conversation capability keeps the operator-facing contract
(a raw worker output never reaches the operator) and gains the integrate requirement; the
worker capability owns the system-facing behavior. A future change that re-cuts these
boundaries carries an ADR superseding this one.
