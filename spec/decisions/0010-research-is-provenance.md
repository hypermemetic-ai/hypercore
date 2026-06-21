# ADR 0010 — research is provenance; the standing artifacts stand alone

Status: **operator-directed** (2026-06-21) — the operator named the smell and chose the shape (the
depth source's home, this ADR's scope); the machine-side execution below awaits ratification.
[machine]

## Context

The operator named a structural smell: the repo had begun to **lean explicitly on documents
external to the repo proper**, and on `research/` as if it were load-bearing. Two distinct leans:

- **A genuinely external dependency.** The README's entry point and ~40 citations across `hyper/`,
  `spec/`, and the ADRs pointed at `~/Documents/rebuild-spec-1.md` (the bootstrap methodology spec)
  by section number — a document no clone could read. `hyper/depth.py` and ADR 0009 cited
  `rebuild-spec §N` for behavior; the README's "Start here" listed two `~/Documents` files before
  `intent.md`. A clone could not follow its own front door.
- **`research/` load-bearing at runtime.** `hyper/depth.py` *read* `research/aposd.md` live each
  fold and rendered the worker's depth grounding from it (ADR 0009's single-sourcing). So
  `research/aposd.md` was not work product that *informed* a decision — it was infrastructure the
  system *ran on*, filed under `research/` as if it were a note: one file wearing two hats, the
  durable synthesis the system stands on and a research artifact.

Research is work product: it **informs** decisions, but the decisions and their practical
manifestation are what stand, and they must stand alone.

## Decision

**A standing artifact may *cite* research as provenance; it may not *depend* on it. The bootstrap
scaffold is retired; the load-bearing synthesis is promoted out of `research/`.**

- **The discipline.** Citing research as a footnote is fine — delete the research and the decision
  still reads and still holds. *Depending* on it is not: reading a research file at runtime, or
  pinning acceptance to a research doc's section number, leaves the standing artifact unable to
  stand without it. `research/` (`regrounding.md`, `context-files.md`, `assembly.md`) stays as
  honest provenance the ADRs and README *cite*; nothing in `hyper/`, `spec/`, or the ADRs *depends*
  on it.
- **`rebuild-spec` is retired.** It was the bootstrap doc; what the repo needed from it is now
  present in `intent.md` (the vision), `spec/` (the living capability specs), and the ADRs (the
  decisions). Every `rebuild-spec §N` citation was repointed to its in-repo home or dropped where
  the prose already stood; the two acceptance-by-section citations (`slice7` → `regrounding.md §9`,
  `conditions` → `§7.2`) were repointed to ADR 0006 / `spec/folding-conditions`. The `~/Documents`
  pointers left the committed README for an uncommitted local note.
- **The depth synthesis is promoted to `spec/depth.md`.** The single source `hyper/depth.py`
  renders from moves out of `research/` (where it read as work product) into the living spec (where
  it reads as the standing methodology it is). `spec.read_spec` loads only capability folders and
  the glossary, so this does not perturb the worker's preloaded spec; `depth.py` reads
  `spec/depth.md` directly, exactly as it read `research/aposd.md`. Its slice-7 process scaffolding
  (the "what phase 2 grills" framing) shed into provenance; the synthesis and its epistemic status
  stand.

## Grounds

The discipline is intent.md's own — "durable state in version-controlled files," "what the operator
can read is the source of truth" — applied to the boundary between research and the standing record:
a clone is the unit of truth, so anything the system reads or is judged against must be inside it.
The smell was a category error, not a duplication: `research/aposd.md` was doing the synthesis's
*informing* job and the system's *running* job under one name, so promoting it to `spec/depth.md`
(content) while leaving `regrounding.md` in `research/` (provenance) puts each in the home its job
names. Single-sourcing is untouched — only the source's location and label move.

## Consequences

`research/aposd.md` → `spec/depth.md`; `hyper/depth.py`, `hyper/check/slice10.py`, `worker`,
`conditions`, `glossary`, and `spec/worker` repointed at it; `skills/depth/SKILL.md` regenerated.
`rebuild-spec` and the `~/Documents` references are gone from the committed repo (`LOCAL.md`,
gitignored, holds the parked-harness and backup pointers). This ADR **supersedes in part ADR 0009**:
its single-sourcing channel stands, but the source it named (`research/aposd.md`) is now
`spec/depth.md`. The acceptance harness is unchanged in substance — `slice10` plants its controlled
source at the new path and stays green (slices 1–10 pass). A future change that lets a standing
artifact depend on `research/` again carries an ADR superseding this one.
