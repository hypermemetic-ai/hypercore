# ADR 0005 — architecture-review is its own capability

Status: machine-owned, awaiting ratification. [machine]

## Context

Slice 6 builds the architecture review render (rebuild-spec §7.4, §9.6): the standing scan
for deepening opportunities that produces the operator view's "what the system is" upper
levels and the deepening backlog. ADR 0001 forecast "architecture-review" as a later
capability — the last of the boundaries it anticipated. The seam had to be cut one way,
because it sets the operator view's top level: a new top-level capability, or requirements
folded into the existing seven (ADR 0002 set the counter-precedent of folding behavior into
existing capabilities when it owns no surface of its own; ADR 0003 and ADR 0004 each cut a new
capability when it owns a surface none of the others do).

## Decision

Architecture-review is **its own capability** — the eighth top-level unit, the boundary ADR
0001 anticipated. The candidate it had to be weighed against was the self-model, since the
review's output is the operator view, which the self-model owns.

The grounds it owns a surface none of the others do: the **standing scan of the actual code**.
The self-model derives the as-built from the *living spec* (requirements); folding-conditions
gates *one graph's* produced material at the fold, scoped to that graph's diff. The
architecture review derives the structural truth — module depth, debt — from the *code*, across
the *whole standing tree*, continuously. That is a different subject from both: not the spec,
not one graph's material, but the system's standing shape. The self-model keeps the view
machinery (how vision/as-built/gap render); architecture-review owns the scan that supplies the
upper levels' structural as-built and the deepening backlog. The relationship mirrors
folding-conditions ↔ self-model: there, the per-graph gate beside the delta and merge; here,
the standing whole-tree scan beside the view render.

## Grounds

Folding the review into the self-model would mix "what the model is and how it renders" with
"the standing structural assessment of the code" — two subjects at two scopes. A clean boundary
stands here, as it did for the worker (ADR 0003) and folding-conditions (ADR 0004), and unlike
extraction (ADR 0002), which spoke only through surfaces the existing capabilities already owned.

One budget, two scopes: the line-count budget lives in `folding-conditions` (the per-graph gate
at the fold). The architecture review consults the same budget and the same decision-record
escape hatch for its standing whole-tree scan, rather than defining a second budget — so a file
the gate would refuse is the same file the review flags, by construction. The "nearing budget"
threshold (80% of the budget) is the review's own, a starting value to tune (§11) like the
budget itself. The review's depth is deliberately shallow at this slice — it measures length,
the mechanical part; the deletion test and seam analysis it is meant to grow are recorded as
unbuilt in its own spec, the same self-honesty the operator view is built to practice.

## Consequences

The operator view is eight units wide: `interface`, `graph`, `queue`, `conversation`,
`self-model`, `worker`, `folding-conditions`, `architecture-review`. The self-model's "operator
view renders vision beside as-built and gap" requirement is modified to record that the upper
levels' as-built and the deepening backlog are the architecture review's standing output. The
acceptance harness `hyper/check.py`, which ADR 0004 named as the first candidate for the
per-slice split the discipline asks for, was split into the per-slice `hyper/check/` package as
part of this slice — the first deepening work the review surfaced, landed so the review can
report the real tree honestly clean. A future change that re-cuts these boundaries carries an
ADR superseding this one.
