---
kind: ask
state: folded
owner: operator
created: 2026-06-21
folded: 2026-06-21
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
- **cards & grilling in the folder model** — RESOLVED (design-it-twice, operator held the legibility
  stake): **the graph folder is the on-disk unit; the queue and ready frontier are computed views,
  not stored card/question files.** A grilling pass lives durably *within* its graph folder
  (resumable across episodes), and the queue is derived by scanning folder state. The deeper rewrite
  of `grill.py`/`conversation.py` (the per-question node model collapses into per-graph pass-state)
  is the cost, paid for L110/L112/L114 faithfulness.
- **the contracts** — `spec/graph/spec.md` and the `hyper/check` slices that pin the node-as-unit
  layout, updated to the folder-and-move shape.

## design-decision

design-decision: nodes-in-the-graph-folder → the graph folder is the on-disk unit (Design B) —
the queue/frontier are computed views over folder state, not stored card/question files; a grilling
pass lives durably within its folder. Chosen over relocating each node into the folder as its own
file (Design A), which keeps the node as the on-disk unit (tension with L112) and stores cards (a
dent in L110). Operator-ratified on the legibility stake (what `tree work/` shows). [machine]

## result — folded

The engine is folder-native. `hyper/graph.py` reads/writes/folds graphs as folders (computed views,
`work/`→`archive/` fold-as-move); `hyper/grill.py` carries the grilling pass in `grilling.md` (the
held graph is the card); `conversation`/`window`/`render` needed no change (they already drove
grilling through `grill`'s predicates). Contracts updated: `spec/graph/spec.md` asserts the
folder-and-move shape, `hyper/check/slice1` pins it (the standing work is a folder, an approved
decision folds to `archive/`), and `slice4`/`slice8` plant the handed delta in `grilling.md` and scan
graph nodes (not the scratch fence). **All slices 1–10 green (139 checks).** The engine reads
hypercore's own graph: `graph-on-disk` + `role-assembly` standing, `repo-structure` +
`depth-regrounding` folded — and this arc folds itself, by the mechanism it built.
