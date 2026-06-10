# hypercore

hypercore is a small graph for a human and an agent to think with together. It
holds **nodes**, **relations** between them, **clusters** (named sets of
relations that stand for a repeatable operation), and **material** (documents,
code, and scripts) attached to nodes.

The database is the source of truth. Everything you can read on disk — this
folder included — is a derived, human-legible view of it.

hypercore is itself a node in this graph. Its own node points to this intent and
to the engine as its material, so the model is recursive: hypercore is described
by the same structure it describes. The intent statements are nodes too, so their
connections can be labelled and studied. `hypercore ingest` builds that picture
from the files; `hypercore render` writes the files back from it.

## The intent lives here, at the root

Read it first. It is written as plain, falsifiable statements. A statement
ending in `[machine]` was authored by the machine and awaits the operator:
endorse it by deleting the marker, amend it, or strike it.

- [`organizing-document.md`](organizing-document.md) — the segments, named.
- [`foundations.md`](foundations.md) — why hypercore exists.
- [`structure.md`](structure.md) — nodes, the intent and material they point to, recursion.
- [`statements.md`](statements.md) — what makes a statement worth keeping.
- [`endorsement.md`](endorsement.md) — who stands behind a statement.
- [`work.md`](work.md) — execution graphs and folding.

## The engine is material

The implementation is tucked away in [`engine/`](engine/): the DuckDB store, the
command-line tool, and the browser viewer. You only open it to run something.

```sh
cd engine
../.venv/bin/python -m hypercore status   # pending endorsements, open work, recent folds
../.venv/bin/python -m hypercore show ID  # one node, human-legible
../.venv/bin/python -m hypercore serve    # view it at http://127.0.0.1:8000/

# the graph is authored with verbs; every one rewrites the files and snapshot
../.venv/bin/python -m hypercore endorse ID [ID...]
../.venv/bin/python -m hypercore add-statement --segment SEG --text "..."
../.venv/bin/python -m hypercore amend ID --text "..." [--by operator]
../.venv/bin/python -m hypercore strike ID [--by operator]

# work runs as execution graphs that fold back into the node that spawned them;
# their members are operations of the six kinds, wired by combinator relations
../.venv/bin/python -m hypercore work-open --on ID --label "..." \
    --fold-when "..." --check machine|operator
../.venv/bin/python -m hypercore work-add WID --kind frame|gather|derive|generate|test|commit \
    --label "..." [--on ID] [--needs ID] [--under ID] [--roles JSON]
../.venv/bin/python -m hypercore work-check TID --verdict pass|fail [--grounds "..."]
../.venv/bin/python -m hypercore work-fold WID [--operator-confirms | --abandoned]

../.venv/bin/python -m hypercore load     # rebuild a local db from engine/graph.json
```

The durable form of the graph is [`engine/graph.json`](engine/graph.json),
committed to git; the DuckDB file is a local working copy. The markdown at the
root is rendered, never hand-edited.

See [`engine/README.md`](engine/README.md) for the full command list and the
(load-bearing) environment notes.
