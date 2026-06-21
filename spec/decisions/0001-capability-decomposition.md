# ADR 0001 — the seed capability decomposition

Status: machine-owned, awaiting ratification. [machine]

## Context

The living spec is segmented by capability — "a coherent slice of system behavior,
named in the domain's own words." The seed, distilled from `intent.md` and the
slice-1 code, must carve the system into capabilities once; this carving is the
spine of the self-model and what the operator's view is built on, so it is hard to
reverse and is recorded here rather than left implicit.

## Decision

Five capabilities, taking their names from `intent.md`'s own nouns:

- **interface** — the window: keyboard-only, fullscreen, never blocking on durable
  work; the operator's whole surface.
- **graph** — the durable model: nodes on disk, read live, written atomically and
  committed; the one source of truth.
- **queue** — the decision surface: cards as a view of awaiting nodes; approve / cut
  / explain; weight matching the call.
- **conversation** — the throwaway thread and the architect: one session,
  closed on satisfaction, landing one consequence on the graph.
- **self-model** — the living spec, the delta, the fold, and the operator view: the
  system's maintained model of itself.

## Grounds

These five are where checks can stand: each is a coherent behavior slice with a
clean boundary to the others, and together they cover what slices 1 and 2 built
with no overlap. They map one-to-one onto `intent.md`'s vocabulary, so the operator
reads the spec in their own language. The decomposition is expected to grow — later
slices add capabilities (workers, grilling/extraction, folding-conditions,
architecture-review, parallelism) rather than reshaping these — which is why the
seam is cut here and named.

## Consequences

The operator view's top level is these five units. The gap render measures
`intent.md` against this set, so unbuilt vision (the later slices) reads as gap
until its capability appears. A future change that needs to re-cut these boundaries
carries an ADR superseding this one.
