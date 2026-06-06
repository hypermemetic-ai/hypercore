# active-work

active work is a child node with the same reserved tree as any other node: `intent/`, plus
whatever node-local material its work needs beside that reserved tree.
active work is bounded by the parent intent statements whose reach includes it.
a work node may propose parent intent or parent material amendments without making those
amendments current.
until adoption accepts an amendment, the parent intent remains current.
adoption folds accepted child statements and material into the parent and records the work
node as history.
shelving records the work node as history without making its proposed amendments parent
truth.
a work node may be temporary, durable, adopted, shelved, abandoned, or indefinitely active.
purpose, rationale, proof state, route, sign-off, and adoption claims are recoverable as
intent or material within the work node; they are not universal required filenames.
root-directed active work lives directly under the root as `<NNN-slug>/`, as a sibling to
`home`, not under `home`.
the root active-work contract spans root child work nodes and grants them the general
ability to parent their own child work nodes unless their own contract narrows that
freedom.
signed legacy change folders may remain readable only to finish old work; they are not the
current work-node shape, and retained change-folder history is not required.

## machine
a sibling set of node-local work nodes is named with `NNN-slug` folders, with the ordinal
scoped to that sibling set.
new active work nodes live directly under the addressed node.
a new work node's frame lives under that work node's `intent/frame/`.
legacy signed frames under `intent/changes/<NNN-slug>/` remain readable to finish old work.
adopted work-node history is recorded under `intent/history/adopted/`.
shelved work-node history is recorded under `intent/history/shelved/`.
empty work-node history collections carry `.gitkeep` so the repository holds the collection
even when no retained record exists inside it.

---
endorsed by qqp-dev
