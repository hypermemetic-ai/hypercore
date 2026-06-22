# ADR 0011 — the graph on disk is the folder, not the node

Status: **operator-directed** (2026-06-21) — the operator named the smell (the repo carries no
representation of the graph, and the on-disk form was unsettled — three sources disagreed) and
chose the shape (the intent's own §work law); the machine-side execution below awaits ratification.
[machine]

## Context

The repo holds `intent.md` (the vision), `spec/` (the living capability specs), and `hyper/` (the
engine) — but **no representation of the graph**, the thing `intent.md` calls the model. The
construction work had leaked into `next-work.md` (a stored work-queue, which §work L110 forbids:
"the work schedule is a view, not a stored list") and into orphan material with no node to hang on.

Investigating the on-disk form surfaced that **three sources disagree on what the graph-on-disk
even is**:

- **`intent.md` §work (the ratified law)** — a graph is a *folder*: "A folder holds one execution
  graph; the unit on disk is the graph, not the single node" (L112). Open graphs sit in the parent's
  `work/`; "the act that folds it moves it to `archive/`" (L116). Decomposition is as-needed and
  sparse (L106), and open siblings are isolated, meeting "only through folding conditions" (L108).
- **`hyper/graph.py` (the as-built engine)** — a *node* is the unit on disk: flat files at
  `work/nodes/<id>.md` with a `state:` field. There is **no `archive/`**; folding flips the field to
  `done` and the file never moves. This contradicts L112 and L116 directly.
- **The epoch-2 backup** — `work/<slug>/graph.md` folders plus `archive/<slug>/`, an earlier, flatter
  encoding the current intent has since refined.

A research pass across ~25 systems (OpenSpec, Kiro, spec-kit, Backlog.md, dstask, git-bug, Maildir,
HTN/Bazel/Airflow, SQL hierarchy models) was run to decide the form with an open mind, alongside
reasoning from the intent's own §work.

## Decision

**The graph on disk is the folder, not the node — the intent's §work law, adopted verbatim.**

- An **execution graph is a directory**: it carries its intent document (its ask = its current
  intended reality), its operations, and its attached material.
- **Open graphs live in the parent's `work/`; folding moves the folder to `archive/`** — one atomic,
  legible operation (`git mv`), with the result landing as material in the parent (L116). Neither
  `work/` nor `archive/` exists empty.
- **Decomposition is as-needed and sparse** (L106): a child graph is a nested folder only at a real
  fold seam, never a tree drawn ahead. An operation earns a node on two grounds only — it crossed the
  operator–machine boundary, or the fold's trust rests on it; everything else is `do`, absorbed
  (L114).
- **Views are computed live by scanning the tree** — the queue and the ready frontier are read fresh
  each time, never a list kept in sync (L110). This **retires `next-work.md`**.

## Grounds

- **The intent already specifies this**, and the repo was in violation of it. L112/L116/L106/L108
  describe the graph-as-folder with `work/`→`archive/` folding, sparse decomposition, and isolated
  siblings. Adopting it is obeying our own ratified law, not inventing a structure.
- **OpenSpec — the near-twin — proves the shape at production.** Its `changes/<name>/` folders fold by
  `apply-delta + move to changes/archive/`, and its views are a folder scan; its delta and view
  semantics are already in `spec/glossary.md`. Adopting its folder-and-move lifecycle is the path of
  least invention.
- **The weight of precedent, read against our constraints, converges here.** Where the field
  decomposes deeply it does so by *reference* (HTN, Bazel; Airflow *removed* containment-style
  SubDAGs for concurrency deadlocks and lost single-view) — but our decomposition is *sparse and
  as-needed* (L106), so that motivation does not bite. The one real objection — git-worktree merges
  penalize directory-moves that race a concurrent in-folder edit — is neutralized by §work's own
  design: siblings are isolated (L108) and a graph folds only once its work is done, so the
  folder-move never races an edit inside it.

## Consequences

- **`hyper/graph.py` is superseded** in its on-disk layout. It makes the node the unit
  (`work/nodes/<id>.md`), has no `archive/`, and folds by field-flip — a direct violation of
  L112/L116. It must be reworked to the graph-folder form (or replaced), with the acceptance harness
  (`spec/graph.md` scenarios, the `hyper/check` slices that pin it) updated to assert the
  folder-and-move shape. This is **the first finding the dogfooding surfaces** — the engine bends to
  the structure, not the reverse.
- **`next-work.md` is retired**: standing work becomes graph folders under `work/`, the frontier
  computed; its current content migrates onto the nodes whose asks it records (and folds to
  `archive/` where the work is already done).
- **`research/` — corrected by ADR 0012.** This ADR first read research as unaffected; ADR 0012
  reverses that — provenance *is* graph material, so the root `research/` is dissolved and each note
  lands on its work graph. Independent of this ADR's graph-shape decision.
- The machine's first framing of this fork (directory-move vs field-flip as a binary) was
  mis-bundled; the corrected, *separable* axes are decomposition-edge (containment, at the graph
  grain) and lifecycle transition (directory-move). Recorded so it is not re-litigated.

## Relation

Independent of ADR 0010 (research provenance). Supersedes `hyper/graph.py`'s on-disk layout
(`work/nodes/<id>.md`); the engine's read-live / atomic-write / commit-behind mechanics
(`spec/graph.md`) stand — only the on-disk *shape* moves from node-as-unit to graph-as-folder.
