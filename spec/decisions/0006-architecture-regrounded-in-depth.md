# ADR 0006 — the architecture re-grounded in depth (Ousterhout)

Status: machine-owned, awaiting ratification. [machine]

## Context

Slice 7 reconsiders the line-count budget and the slice-6 `check.py` split against John
Ousterhout's *A Philosophy of Software Design* (`spec/depth.md`, the depth synthesis), and —
the impression having held through a deep run — rebuilds hypercore's architectural constraint
around it (`archive/depth-regrounding/regrounding.md`, the slice-7 design). The budget named the enemy by its
**fingerprint** (length) rather than its **cause** (shallow, entangled, leaky structure),
and so made the fingerprint the crime: a line-count ceiling that fires without judgment is
the same mistake as *Clean Code*'s small-function floor — a number standing in for the
judgment of depth. Ousterhout's framework is a **judgment**; hypercore's enforcement must be
**mechanical**. The capability seam this runs along — `folding-conditions` (the per-graph
gate) beside `architecture-review` (the standing scan), ADR 0004/0005 — **survives**; only
the *criterion* it carries changes from length to depth. No capability boundary is re-cut.

## Decision

**Depth is the criterion; length is one signal of it; the red flags are the named symptoms.**

- **Length is demoted to a context-cost signal.** Length is kept for a reason Ousterhout does
  not address and that survives his objection — every line is context an agent must load, so
  length is a fair proxy for a module's *context cost* (hypercore's own concern), never for its
  *depth*. The old budget conflated the two; this separates them.
- **The gate raises a decision, never an auto-refusal on length.** A source file a graph grew
  past the **length signal** raises a **depth decision** — re-cut / deepen / accept-with-reason
  — held on the operator's queue, never a silent veto and never a silent pass. The
  non-negotiable facts (the delta applies; a behavior-changing graph carries a recorded loop)
  still auto-refuse; only the depth criterion becomes a judgment.
- **F2 — no hard length ceiling survives.** There is no second, higher number that auto-refuses.
  Any such number would re-commit the very error being removed and would force back the escape
  hatch this deletes; judgment plus the operator-decision carry the whole range. The
  anti-dilution guarantee still holds: over-signal material is *un-foldable* until the operator
  settles the depth decision — stronger than the old coincidental-ADR escape, not weaker.
- **The justification hole is closed by construction.** Because length no longer auto-refuses,
  the loose-substring escape hatch (`conditions.justified`) is **deleted**, not tightened, and
  replaced by a **structured depth-decision** record — a parseable `depth-decision: <path>
  accepted — …` line that names the exact file. A coincidental prose mention grants no exception
  because the record is the *decision*, not the *spelling*.
- **The worker is grounded in the depth disciplines, every episode.** The deep-module framework,
  strategic-over-tactical programming, and the red flags are assembled into the worker's prompt
  by construction, so the *primary* anti-complexity defense is **proactive** — the worker builds
  deep up front and the gate is a rarely-tripped backstop, not an operator-load generator.
- **F3 — the role is renamed `architect`; the capability stays `conversation`.** Putting the
  depth verdict at its gate exposed the operator-facing role as the holder of design judgment;
  it is renamed architect (communicating a design is part of designing it). The capability
  boundary — the operator-facing channel — is unchanged, so this is a rename, not a re-cut, and
  carries no new boundary ADR.
- **The slice-6 `check.py` split keeps, on locality.** The split produced six near-identical
  `sliceN` modules; on Ousterhout's terms that risked the over-decomposition / classitis charge.
  It keeps: each `sliceN` is a genuinely separate acceptance contract (a real seam, one per
  slice), partitioned along that existing seam — locality, not interface decomposition. The
  modules are independent test scripts, not shallow interfaces fronting hidden complexity.
- **F1 — the model-driven depth verdict is deferred.** The red-flag depth *assessment* (a
  model-driven standing scan) cannot be checked by the deterministic acceptance harness and is a
  real capability in its own right; cramming it in would itself be tactical. This slice ships the
  fully harness-testable mechanical scaffold and records the model-driven scan as the review's
  standing job to grow — the same self-honesty slice 6 used for the deletion test.

## Grounds

The seam hypercore already cut carries the resolution: the **mechanical gate**
(`folding-conditions`) keeps the non-negotiable facts and a single judgment that *raises a
decision*; the **judgment layer** (`architecture-review`) is where the red flags will live as a
standing scan. A judgment framework honored by a mechanical system without becoming the rule it
warns against means: the machine *triggers and surfaces* the judgment (length past the signal →
a decision), and a person *makes* it (the operator, with the model-driven verdict to grow). The
deepest move is proactive — design awareness engineered into the worker's context (the
incremental-complexity thesis turned on hypercore's own work) — so the gate rarely fires.

## Consequences

This ADR **supersedes in part** ADR 0004 (the 400-line auto-refusing ceiling and the
substring `justified` escape hatch — both removed) and ADR 0005 (the review "measures length"
as its standing job — length is now one signal, the red-flag depth scan the deferred job). The
boundary decisions of both — folding-conditions and architecture-review as their own
capabilities, one criterion at two scopes — stand. `conditions.BUDGET` becomes
`conditions.SIGNAL`; `conditions.justified` becomes the structured `conditions.accepted`. The
living spec carries deltas across `folding-conditions`, `architecture-review`, `conversation`
(the architect rename + the depth-judgment requirement), `worker` (the depth-disciplines
grounding), `self-model` (the operator view reads depth), and the glossary (the architect
rename + the Ousterhout terms). A future change that re-cuts these boundaries carries an ADR
superseding this one.
