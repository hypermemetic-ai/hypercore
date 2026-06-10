# organizing document

hypercore keeps its intent at the root, in segments. Each segment is one markdown file.

- **foundations**: why hypercore exists and the properties it protects.
- **structure**: nodes, the intent and material a node points to, and that hypercore is itself a node.
- **statements**: what a statement is and what makes one worth keeping.
- **endorsement**: who stands behind a statement.
- **work**: how work runs as an execution graph and folds back into the node that spawned it.

hypercore is a node, and these segments are the parts it contains. Each segment's statements are nodes too. The graph is authored with the statement verbs (`add-statement`, `amend`, `strike`, `endorse`); the engine writes these files from it with `python -m hypercore render`. `ingest` only bootstraps an empty database, and `load` rebuilds one from the snapshot.

This document names the current division. It is not a taxonomy for every future node.
