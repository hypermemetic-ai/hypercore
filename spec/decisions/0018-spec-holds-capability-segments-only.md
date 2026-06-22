# ADR 0018 — `spec/` holds capability segments only; the glossary rises to root

Status: **operator-directed** (2026-06-21) — the operator named the smell (`spec/` mixed three
kinds of thing and the README needed a three-part explanation to describe its contents) and chose
the cut; the machine-side mechanism is below. Depth's normalization into a capability is ADR 0019. [machine]

## Context

ADR 0014 made capabilities flat files and, in the same move, declared that `spec/glossary.md` and
`spec/depth.md` simply "sit among the capability segments as the flat documents they are." A
coherence pass found that resolution asserted the confusion away rather than dissolving it: `spec/`
held **three different kinds of thing** — the capability segments (the as-built living spec), the
**glossary** (the ubiquitous language that governs intent, spec, and code alike), and **`depth.md`**
(an imported design philosophy distilled into a grounding source, 332 lines, dwarfing every ~60-line
capability) — plus the `decisions/` directory. The tell: `README.md` needed a three-part sentence to
say what was in `spec/`. A directory that needs a paragraph to explain its contents is mixing types.

The operator rejected re-housing the strays in a `docs/` tree: in hypercore's own ontology the spec
is **not documentation** — it is the *model* (the as-built counterpart to `intent.md`'s vision), and
the ADRs are the *decision record*. `docs/` would flatten the very vision/as-built/gap ontology the
self-model is built on.

## Decision

**`spec/` holds capability segments only.** What was mixed in resolves two ways — one resident
leaves, the other was never a different type:

- **The glossary rises to the root** (`glossary.md`). It is the ubiquitous language — it governs
  `intent.md`, the spec, and the code, not the spec alone — so it stands at the front door beside the
  vision, with the lone importance that placement carries, not filed under one of the things it
  governs.
- **`depth` becomes a capability segment** — not a third type, and not exiled. The disciplines stay
  in `spec/depth.md`, rewritten from essay-form into the requirement-and-scenario shape every other
  capability uses, because depth is the *same kind of thing* as `design-it-twice`: imported Ousterhout
  discipline made a capability (ADR 0007). Nothing forced it to be special. The 332-line synthesis is
  the *grounding document*, and a grounding document is **provenance** (ADR 0010/0012): archived with
  the depth-regrounding arc, cited not depended on — not a standing fixture in `spec/`. (Settled in
  ADR 0019.)

`spec/` is thereafter the twelve capability segments and `decisions/`. The rule ADR 0014 reached for
("folders bear material; flat files are documents") is joined by the cut it missed: **`spec/` is the
model; the language is not the model, and an imported discipline is a capability, not a third type.**

## Grounds

Each thing now lives where its kind says it should: the model in `spec/` (depth included, a capability
like `design-it-twice`), the language at the root it spans, the synthesis in the archive where
provenance lives. The README no longer needs a paragraph to explain a directory. No behavior changes from the
glossary move — `engine/spec.py` is the one place that knows the on-disk shape; it now reads
`glossary.md` from the root, `sp.glossary` is unchanged, and the worker grounding and every
acceptance check see the same system (the harness is green).

## Consequences

- `spec/glossary.md` → `glossary.md` (root). `engine/spec.py` reads it from the root; the slice-2
  seed copies it in beside the spec and intent. **Supersedes ADR 0014** on the placement of the
  cross-cutting segments (its single-file-folder dissolution stands).
- Depth's normalization (`spec/depth.md` rewritten as a capability + the synthesis to `work/archive/`)
  lands in **ADR 0019**, which also **amends ADR 0010** (the synthesis was promoted *into*
  `spec/depth.md`; it now returns to provenance while the disciplines stay as the capability).
- Frozen records (ADRs 0001–0017, the archived arcs) keep their `spec/glossary.md` / `spec/depth.md`
  references as written — historical, not live.
