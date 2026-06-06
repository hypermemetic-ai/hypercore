# structure

every node has one reserved tree: intent under `intent/`; a project is a node, and the
root corpus is a node.
everything else in the node is node-local material: leaf material, durable child nodes,
active work nodes, adapter materialization, checks, CLIs, and settled external references.
the intent is divided into segments; there is no universal taxonomy, so each node picks
segments that fit its work.
the organizing document names this node's segments and how the intent is divided.
each segment has one intent document holding that segment's current intended state.
a child node is a governed directory or settled linked entry point with its own `intent/`,
and nests to any depth.
a child node does not need a `material/` directory.
childness is bounded freedom: the parent's intent bounds the child only through statements
whose reach includes that child.
a parent intent statement defines its own reach: node-local, a named child, all direct
children, descendants, or a named class of child.
any parent segment that houses a child states the contract the child must satisfy.
a node holds only its own corpus; only the statements whose reach includes the child cross
between parent and child.
`intent/` holds `machine-statements/`, current segment documents, and history collections.
node-local material outside `intent/` holds leaf material, durable child nodes, and active
work nodes.
legacy change folders under `intent/changes/` may remain readable while old signed work is
being finished; retained legacy change-folder archives are not required by the current
structure, and new work does not depend on them.
active work is a child node directly under the addressed node, not a special folder type
under intent.
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
the methodology prose is materialized in `hypercore.md`.
a child node is inlined at `<name>/` unless a machine statement settles a mount path there
as an external reference.
`check.sh` checks every current node in the tree -- the root and each child node, a child
node being any directory or settled linked entry point holding `intent/`.

---
endorsed by qqp-dev
