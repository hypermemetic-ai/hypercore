surfaced: 0

[CONTRACT]
When the depth gate trips at a fold, the architect raises a reasoned depth/length assessment of the flagged file read in its NEIGHBOURHOOD (callers, siblings, cross-module boundaries), carrying a lean and a flip, in place of the bare 're-cut / deepen / accept' template the gate emits today. The neighbourhood is seen by CONSULTING the standing architecture review's whole-tree read (the same depth_scan seam #8 builds), never a second scan. The assessment informs the settlement; the operator still settles; it does not gate the fold and leaves no extra watched trace. To route it, the fold gate now TYPES its outcomes additively (conditions.unmet keeps its string contract for every existing caller; a new typed verdict carries the reason plus its guard): the depth and vocabulary guards are escalating-guard decisions the operator settles, while the delta-does-not-apply and provenance-no-trail refusals are flat — raised verbatim, never dressed as a negotiable assessment. Builds on #8's seam; built second, after #8 folds.

[DELTA]
# delta — the neighborhood-aware depth assessment

## ADDED — folding-conditions
### Requirement: the gate types its outcome — an escalating-guard decision is distinct from a flat refusal
The fold gate MUST **type** each unmet outcome so the integrate path can tell an **escalating-guard
decision** the operator settles from a **flat refusal** that is never waveable. Today the gate flattens
every unmet condition to one opaque string, so the depth decision and the delta-does-not-apply refusal
are indistinguishable. The gate MUST expose a typed verdict — the unmet reason **and** its guard — where
the **depth** and **vocabulary** guards are escalating-guard decisions (the operator settles them:
re-cut / deepen / accept, or define / waive / dismiss) and the **delta-does-not-apply** and
**provenance-no-trail** guards are flat refusals (facts, the way a delta that does not apply is a fact),
which MUST NOT be dressed as negotiable. The typing MUST be **additive**: the existing string seam stays
(`conditions.unmet` keeps returning the first unmet reason as a string), so every current caller is
unbroken; the typed verdict carries the same reason with its guard and an `escalating` flag beside it,
computed in the one place the gate already evaluates its conditions, so the type is read, never
re-parsed from the string.

#### Scenario: the gate types its outcome — escalating-guard versus flat refusal
- WHEN the fold gate's typed verdict is read over material that trips the depth guard, the vocabulary
  guard, the delta-does-not-apply guard, or the provenance-no-trail guard
- THEN each verdict names its guard and marks the depth and vocabulary guards as escalating-guard
  decisions the operator settles, while the delta and provenance refusals are flat — never dressed as
  negotiable — and the plain string seam still returns the same reason for the unbroken existing callers

  ```check
  gate-type depth escalating
  gate-type vocabulary escalating
  gate-type delta flat
  gate-type provenance flat
  gate-type string-seam-intact
  ```

## ADDED — communication
### Requirement: a depth-gate trip raises a neighborhood-aware assessment; a flat refusal stays verbatim
When the architect integrates a worker hand-off and the fold gate raises the **depth** decision, the
architect MUST raise a **reasoned depth/length assessment of the flagged file read in its
neighborhood** — its callers, its siblings, the cross-module boundaries where a misplaced
responsibility would show — carrying a **lean** (the architect's recommendation) and a **flip** (the one
thing that would change it), in place of the bare *re-cut / deepen / accept* template the gate emits.
The neighborhood is seen by **consulting the standing architecture review's whole-tree read** — the
structural map and complexity debt it already computes, fed to the shared depth-assessment seam
(`a depth-gate trip raises a neighborhood-aware assessment` reads the same `depth_scan` seam the
standing scan does) — never by spinning up a second whole-tree scan. The assessment **informs** the
settlement, it does not make it and it does not gate the fold (the depth condition already holds it):
the operator still settles. It attaches **only** to the escalating-guard decision (the depth guard, and
by the same typing the vocabulary guard); a **flat refusal** — the delta does not apply, the provenance
no-trail — MUST be raised with its reason **verbatim**, never dressed as a negotiable assessment. It is
advisory prose and leaves **no extra watched trace** — the accepted-length record carries its own
provenance trail. The assessment's reasoning is **watched** (a model judgment); that it carries a lean
and a flip in place of the bare template for a depth trip, and that a flat refusal stays verbatim, is
gated below.

#### Scenario: a depth-gate trip raises a neighborhood-aware assessment; a flat refusal stays verbatim
- WHEN the architect integrates a worker hand-off that trips the depth gate, versus one that trips a
  flat refusal (a delta that does not apply)
- THEN the depth trip raises a reasoned depth/length assessment read in the flagged file's
  neighborhood, carrying a lean and a flip, in place of the bare re-cut/deepen/accept template; while
  the flat refusal's reason is raised verbatim, never dressed as a negotiable assessment

  ```check
  integrate depth-trip assessment-with-lean-flip
  integrate flat-refusal verbatim
  ```
