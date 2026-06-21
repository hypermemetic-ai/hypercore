---
kind: ask
state: standing
owner: operator
created: 2026-06-21
---
# graph-on-disk — conform the engine to the folder shape

Rework `hyper/graph.py` and the contracts that pin it from **node-as-unit** (`work/nodes/<id>.md`,
flat files related only by a `parent:` link, fold = a state field flipped to `done`) to
**graph-as-folder**: a graph is a directory carrying its `intent.md`, its material, and — only
where the work spawns a child graph — nested `work/` and `archive/`. Folding moves the folder from
`work/` to `archive/` (`git mv`), the result landing as material in the parent.

This is ADR 0011's execution: the engine bends to `intent.md` §work (L112 — "the unit on disk is
the graph, not the single node"; L116 — the fold moves the folder), not the reverse. This very
directory tree is the first instance, created by hand because hypercore does not yet operate its
own graph; conforming the engine makes the as-built read *this* truth instead of the empty
`work/nodes/`.

## folding condition

`hyper/graph.py` reads, writes, and folds the folder structure (open graphs under `work/`, the fold
moving a folder to `archive/`, `archive/` real); `spec/graph/spec.md`'s scenarios and the
`hyper/check` slices assert the folder-and-move shape (no `work/nodes/<id>.md`); and the full
acceptance harness is green (`python3 -m hyper --check`).

## open seams (cut as the work reaches them, not drawn ahead)

- **read/write** — scan `work/` and `archive/` recursively for `intent.md`; compute the views (queue,
  ready frontier) live from their state, never a stored list (L110).
- **fold** — `integrated` moves the folder rather than flipping a field; `archive/` exists and is real.
- **cards & grilling in the folder model** — the genuine design tension ADR 0011 flags: the engine
  carries fine-grained nodes today (a card, a grilling question, their states), but L112 says the
  unit on disk is the *graph*. Resolve how a transient node lives inside a graph folder before
  rewriting — this is the deep question, not a detail.
- **the contracts** — `spec/graph/spec.md` and the `hyper/check` slices that pin the node-as-unit
  layout, updated to the folder-and-move shape.
