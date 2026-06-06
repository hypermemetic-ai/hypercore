# structure

every node is two trees: intent under `intent/`, and material under `material/`; a project
is a node, and the root corpus is a node.
the intent is divided into segments; there is no universal taxonomy, so each node picks
segments that fit its work.
the organizing document names this node's segments and how the intent is divided.
each segment has one intent document holding that segment's current intended state.
material is either leaf code or child nodes housed by this node.
a child node is a governed node housed in its parent's material, with its own `intent/` and
`material/`, and nests to any depth.
childness is bounded freedom: the parent's intent bounds the child only through statements
whose reach includes that child.
a parent intent statement defines its own reach: node-local, a named child, all direct
children, descendants, or a named class of child.
any parent segment that houses a child states the contract the child must satisfy.
a node holds only its own corpus; only the statements whose reach includes the child cross
between parent and child.
`intent/` holds `machine-statements/`, current segment documents, and history collections.
`material/` holds leaf material, durable child nodes, and active work nodes.
legacy change folders under `intent/changes/` may remain readable while old signed work is
being finished; retained legacy change-folder archives are not required by the current
structure, and new work does not depend on them.
active work is a child node under `material/`, not a special folder type under intent.
adopted and shelved work-node history is recorded under `intent/history/adopted/` and
`intent/history/shelved/`.
archived legacy nested child-change collections may be read if present, but they are not
the current structure and no new work builds on them.
the intent documents hold only the current statements; history holds why each one is there;
the material carries the checks that keep them true.

## machine
every document is a markdown (.md) file.
the organizing document is `intent/organizing-document.md`.
each segment's intent document is `intent/<segment>.md`.
each segment's machine statements are in `intent/machine-statements/<segment>.md`.
the methodology prose is materialized in `material/hypercore.md`.
a child node is inlined at `material/<name>/` unless a machine statement settles it as an
external reference.
`material/check.sh` checks every node in the tree -- the root and each child node, a child
node being any directory holding both `intent/` and `material/`.

---
endorsed by qqp-dev
