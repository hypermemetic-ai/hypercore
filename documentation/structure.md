# structure

every node is two trees: the intent under documentation/, and the code that materializes it under implementation/; a project is a node, and the root corpus is a node.
the intent is divided into segments; there is no universal taxonomy, so each node picks segments that fit its work.
the organizing document names this node's segments and how the intent is divided.
each segment has one intent document holding that segment's current intended state.
a segment is materialized either by leaf code or by a child node.
a child node is itself a node — its own two trees, its own changes, governed by this same loop — and nests to any depth.
the parent segment a child node materializes is that child's contract; the child's intent must satisfy it.
a node holds only its own corpus; the contract is the whole of what crosses between a parent and a child.
documentation/ holds machine-statements/; documentation/changes/ holds the changes in flight and archive/.
machine-statements/ holds the machine's statements, one document per segment, out of the orient path.
a change in flight is a folder directly under changes/; archive/ is a reserved name there and holds changes folded in.
the intent documents hold only the current statements; the archive holds why each one is there; the code carries the checks that keep them true.

## machine
every document is a markdown (.md) file.
the organizing document is documentation/organizing-document.md.
each segment's intent document is documentation/<segment>.md.
each segment's machine statements are in documentation/machine-statements/<segment>.md.
the methodology prose is materialized in implementation/hypercore.md.
a child node is inlined at implementation/<name>/ unless a machine statement settles it as an external reference.
check.sh checks every node in the tree — the root and each child node, a child node being any directory holding both documentation/ and implementation/.

---
endorsed by abacus-git
