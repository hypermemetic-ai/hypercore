# ADR 0015 — the engine package is named `engine`, not `hyper`

Status: **operator-directed** (2026-06-21) — the operator named the smell (a load-bearing
directory name that was never a decision on record) and chose the rename; the machine-side
execution below is the mechanism. [machine]

## Context

The engine — the Python package that *is* hypercore's implementation — was named `hyper`,
run as `python3 -m hyper`. The name had **usages everywhere and grounds nowhere**: no ADR, no
spec line, no glossary entry recorded why the package was `hyper` and not `hypercore`, `core`,
or `engine`. A coherence pass traced every standalone `hyper` token in the repo and found only
references, never a justification — the name was a silent truncation of `hypercore`.

That is a direct violation of two of the system's own laws. **Legibility is king**: an operator
opening the repo meets `hyper/` beside the system `hypercore` and must guess whether they are the
same thing or two things. **One name means one concept** (`glossary.md`): `hyper` and `hypercore`
read as the same word for, ambiguously, the engine and the whole system. The operator flagged it
as the one provable instance of the deeper worry — a load-bearing name chosen without them and
never put on record (its likeliest origin was bleed from a prior epoch, which makes recording it
*now* the point).

## Decision

**The engine package is `engine`.** It is run as `python3 -m engine` and `python3 -m engine
--check`. `engine` says what the thing is — the implementation of the system named `hypercore` —
and cannot be confused with the system itself. The internal root knob `HYPER_ROOT` becomes
`ENGINE_ROOT` to match.

The name is now a decision, not an accident; a future rename carries an ADR superseding this one.

## Grounds

`engine` is descriptive and unambiguous, and it is already the word the README and glossary use
for this package ("the engine"). The rename is a pure relocation of the package name: imports are all
relative and the entry point is the package itself, so the model the system runs is unchanged —
only the word at the front door changes, from a truncation that needed guessing to a name that
reads itself.

## Consequences

- `hyper/` → `engine/` (the directory, all modules, the `python3 -m engine` entry point, the
  `ENGINE_ROOT` knob). The acceptance harness (`python3 -m engine --check`) is green across all
  14 slices after the rename, including the architecture review that scans the package directory
  by name and the depth-decision fixtures that mirror it.
- Generated channels re-materialize with the new name: `AGENTS.md` now names `python3 -m engine
  --check`; the skills carry no package reference and are unchanged.
- **Historical records are kept as written.** ADRs 0001–0014 and the archived arcs reference
  `hyper/<file>.py` as the package was then named; those are frozen records (the ADR 0010/0012
  frozen-provenance precedent), not live pointers, and are not rewritten. A reference to `hyper/`
  in a record dated on or before 2026-06-21 denotes today's `engine/`.
