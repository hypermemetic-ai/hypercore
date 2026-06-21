---
kind: ask
state: folded
owner: operator
created: 2026-06-21
folded: 2026-06-21
---
# repo-structure — where the graph lives (folded)

The operator named a structural smell: `research/`, `skills/`, and `next-work.md` sat at the root
as peers of `intent.md` / `spec/` / `hyper/`, and the repo carried **no representation of the
graph** — the model `intent.md` calls the source of truth. Investigation (the cold backup's epoch-2
`work/`+`archive/`, an OpenSpec-shaped reading, a 25-system research pass) plus reasoning from
`intent.md` §work settled where each piece belongs and what the graph on disk is.

## folding condition — met

The decision is recorded and ratified, and the repo obeys its own §structure:

- **`research/` stays as cited provenance** (ADR 0010) — it informs decisions; nothing standing
  depends on it. The load-bearing synthesis graduated to `spec/depth.md`.
- **the graph on disk is the folder, not the node** (ADR 0011) — `intent.md` §work verbatim, backed
  by OpenSpec and the research pass. `work/` (open) + `archive/` (folded) now exist.
- **`next-work.md` is retired** — its forward work became the live graph (`work/`); its history is
  in the ADRs and git.

## material

- ADR 0010 — research is provenance; the standing artifacts stand alone.
- ADR 0011 — the graph on disk is the folder, not the node. Spawned the open arc
  `work/graph-on-disk/` (conform the engine).
