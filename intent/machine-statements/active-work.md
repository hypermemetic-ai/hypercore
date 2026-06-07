# active-work -- machine statements

a sibling set of node-local work nodes is named with `NNN-slug` folders, with the ordinal
scoped to that sibling set.
new active work nodes live directly under the addressed node.
a new work node's frame lives under that work node's `intent/frame/`.
adopted work-node history is recorded under `intent/history/adopted/`.
shelved work-node history is recorded under `intent/history/shelved/`.
empty work-node history collections carry `.gitkeep` so the repository holds the collection
even when no retained record exists inside it.
