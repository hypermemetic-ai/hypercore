# ADR 0020 — derive-on-fold generalized: the mechanical red-flag scan and the declared vision binding

Status: **operator-ratified arc** (2026-06-21) — the operator ratified moves 1 and 2 of the coherence
synthesis (`work/archive/coherence-audit/`), parking move 3 (the worker seam); the machine-side build is
below. [machine]

## Context

A coherence pass (`work/archive/coherence-audit/`) ran a natural experiment on the repo and found that the
one anti-drift mechanism wired to the fold — **derive-on-render** (`channels`, the skills and the anchor) —
never drifted, while every **hand-maintained restatement** of a derivable fact did (the README's check
count, dropped-symlink prose, stale docstrings) and several **structural red flags** sat unseen (a dead
state, a circular dependency, a hand-typed vision map). The methodology *names* the disciplines that would
catch the latter two classes (depth's red flags, the architecture review's scan) but had never *built* the
mechanical part nor *run* the judgment part. The synthesis: point the proven mechanism (derive, don't
hand-tend) at the rest, and build the spec'd-but-unrun mechanical scan.

This ADR is moves 1 (prevention — remove a hand-maintained surface) and 2 (detection — scan for what
cannot be derived away). Move 3 (wire `worker.run → integrate → fold` to the interface) stays parked as the
operator's sequencing call.

## Decision

**Move 2 — the mechanical red-flag scan (`architecture-review`).** The standing review grows the subset of
the depth red-flag scan a tool can read without judgment, run live every scan and surfaced in the
operator-view gap beside the length findings:

- **dead module-level symbols** — a name bound at module level and *used* nowhere in the package (read off
  the AST, so a mention in a docstring or comment is prose, not a use). Caught the dead `graph.PENDING`
  state — and on its first run, two symbols the manual audit had missed (`delta.load`, `render.Span`).
- **circular dependencies** — two modules that depend on each other (the structural signature of
  information leakage). Caught the `conversation ↔ grill` cycle.

The **broader rules the audit first proposed were dropped after a false-positive analysis**, and that is
itself a finding. A blanket "cross-module access to a `_private` name" rule fires on six de-facto-shared
package internals (`graph._root` and kin); a "dangling path reference" rule fires on legitimately-named
runtime artifacts, retired paths, and relative mentions. Shipping a noisy rule the operator learns to
ignore would violate the system's own "a discipline in the spec cannot be ignored." So the mechanical scan
ships only the two zero-false-positive rules; the model-driven *verdict* (shallow module, information
leakage, the deletion test) stays **judgment, still not built** (ADR 0006), recorded never fabricated. The
three concrete prose drifts a path rule would have caught (the README and `channels` symlink claims, the
`methodology` spec path) are fixed by hand in this same arc, because prose coherence is judgment, not a rule.

**Move 1 — remove the hand-maintained derived surfaces (prevention).**

- The README's hand-typed check count is dropped; `python3 -m engine --check` is its single source.
- The operator view's per-capability vision becomes a **declared binding**: each capability names the
  intent it realizes in its own spec slice (a `<!-- vision: ... -->` line), and the view reads it —
  replacing the hand-typed `TERMS` keyword map in `view.py`. A pure-machinery capability declares none and
  correctly shows **no** vision, distinct from a bug; a newly carved capability gets its vision with no edit
  to the view. The binding is render-invisible (filtered from the skill overview).

design-decision: operator-view vision binding → per-capability spec declaration — chosen over a render-time
semantic match (derived but non-deterministic) and a marker on the intent statements themselves (which
couples the authored vision to as-built structure, the one thing the system separates on purpose). The
binding lands with the as-built capability, the operator view's one writable region, where it belongs.

design-decision: the mechanical red-flag rule set → dead symbols and circular dependencies only — chosen
over the blanket `_private`-access and dangling-path rules the audit first sketched, which a measured
false-positive scan showed fire on shared package internals and on legitimately-named runtime and retired
paths; those noisy rules would teach the operator to ignore the scan. The judgment red flags stay the
not-yet-built model-driven verdict.

**The ride-along.** Dead code the scan flagged is cut (`graph.PENDING`, `delta.load`, `render.Span`); stale
docstrings are corrected (the `methodology` spec path, the harness slice range, the `conditions` length
anecdote framed as the prior epoch's god-file); the dropped `CLAUDE.md` symlink prose is removed from the
README and `channels` (ADR 0009 §4 was already amended). The model transport is named in the same arc
(ADR 0021), dissolving the cycle this scan flags.

## Grounds

This is the repo's **first red→green dogfood** of its own feedback-loop discipline — no `RESULT.md` or
`delta.md` had ever existed. The move-2 scan was built first: it went **red** on the live findings (dead
`PENDING`, the `conversation↔grill` cycle), and **green** once move 1, the ride-along, and the transport
naming cleared them (`engine/check/slice15`, the green half kept as a standing assertion). The drift was
never a quality lapse in the hand-build; it is the negative image of where derive-on-fold had not been
pointed. The system proved the mechanism; this generalizes it and builds the mechanical floor of the
disciplines it had only written down.

## Relation

- **Grows `architecture-review` (ADR 0005/0006)**: the standing scan gains the mechanical structural
  red-flag subset; the model-driven depth verdict it names stays not-yet-built.
- **Sharpens `self-model`**: the operator-view vision is a derived per-capability binding, not a hand-map —
  the as-built-and-gap-are-derived discipline pointed at the one surface still hand-tended.
- **Companion to ADR 0021** (the model transport named), whose extraction dissolves the circular dependency
  this scan flags.
- **Move 3 parked**: wiring `worker.run → integrate → fold` to the interface (the autonomy seam) stays the
  operator's sequencing call (`work/role-assembly/`); until it runs, the classes the mechanical scan does
  not reach are enforced by occasional manual coherence passes.
