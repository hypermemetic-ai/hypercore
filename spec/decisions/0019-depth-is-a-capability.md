# ADR 0019 — depth is a capability, like design-it-twice

Status: **operator-directed** (2026-06-21) — the operator rejected treating depth as a separate type
("I really don't see what's so different between depth and design-it-twice or grilling"); the
machine-side normalization is below. [machine]

## Context

ADR 0018 set out to make `spec/` capability-segments-only and first proposed *exiling* the depth
disciplines to `intent.md`. Pressed on why, a sharper question surfaced and was settled first: the
skills and the worker grounding are **derived from the spec**, so a spec edit changes agent behavior —
the operator asked whether the spec should *represent* behavior or *cause* it. The resolution: for an
LLM agent the "code" is natural-language instructions in the same medium as the spec, so a faithful
render is just reformatting and the derive-by-construction discipline (no second copy, zero drift,
ADR 0009/0010) holds. **The operator accepted the derived equivalence** — the spec coherently
represents *and*, for the agent-facing surfaces, drives. (Where an agent surface must one day *diverge*
from the description — the parked multi-model worker seam — that becomes its own decision; it does not
bite while the renders are faithful reformats.)

With the equivalence accepted, depth had no reason to be special. Depth was a **grounding document**
(`spec/depth.md`, a 332-line essay) rendered by a **bespoke `depth.py`** into the worker's prompt and
a `depth` skill — a second render path beside the architect's `methodology` seam, and a "third type"
in `spec/`. But `design-it-twice` is the precedent that dissolves every claimed difference: it is the
*same kind of thing* — imported Ousterhout discipline (ADR 0007) — and it is an ordinary capability
rendered by the standard seam. "External knowledge" (so is design-it-twice), "grounds the worker not
the architect" (a wiring detail — the worker holds the whole spec), "needs the 332-line synthesis"
(that is provenance the capability cites, exactly as design-it-twice cites the book) — none survives.

## Decision

**Depth is a capability segment, rendered like every other.** Concretely:

- `spec/depth.md` is rewritten from essay-form into a capability — an overview and five
  requirement-and-scenario disciplines (deep modules; information hiding not leakage; strategic over
  tactical; errors defined out of existence; the red flags as judgment not thresholds).
- It is registered in `methodology.METHODOLOGIES` and rendered to `skills/depth/SKILL.md` by the one
  `methodology` seam (the render generalized from "the architect's methodologies" to **capability
  skills**, since depth is the worker's). **`depth.py` is deleted** — its bespoke extraction, the
  separate `channels` entry, and the worker's separate depth injection all retire.
- The worker is still **held to depth every episode**: it holds the whole spec (depth included), and
  `worker.prompt` foregrounds the `depth` capability ahead of the ask — the slice-7 proactive defense,
  now with no special machinery.
- The full **synthesis** moves to `work/archive/depth-regrounding/depth-synthesis.md` as provenance,
  cited not depended on.

## Grounds

The shape now matches the thing: an imported discipline made a system requirement is a capability,
the same as `design-it-twice`, so it renders through the same seam and lives in the same place. This
is a **net deletion** — a whole module (`depth.py`), a special `channels` case, and a bespoke worker
field all gone — which is the right direction for a system whose first law is legibility. Nothing
built is lost: the worker's every-episode depth grounding and the `depth` skill both survive, now as
ordinary consequences of depth being a capability. The acceptance harness is green; `slice10`/`slice11`
(which pinned the bespoke path) now pin depth through the standard capability and methodology checks.

## Relation

- **Amends ADR 0010**: the synthesis was promoted *into* `spec/depth.md` as a standing source; it now
  returns to provenance (archived), while the disciplines stay as the `spec/depth.md` capability.
- **Amends ADR 0009**: depth was the worker's special single-source channel (`depth.py`, the first
  `channels` target); it is now a capability skill rendered by `methodology` like the architect's four.
  `worker.DEPTH`'s retirement stands.
- **Completes ADR 0018**: with depth a capability and the glossary at the root, `spec/` is capability
  segments only.
- A future need for an agent surface to *diverge* from its spec description (the multi-model seam)
  reopens the derive-vs-checked question this ADR settled in favor of derive; it carries its own ADR.
