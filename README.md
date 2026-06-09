# hypercore

hypercore is a small graph for a human and an agent to think with together. It
holds **nodes**, **relations** between them, **clusters** (named sets of
relations that stand for a repeatable operation), and **material** (documents,
code, and scripts) attached to nodes.

The database is the source of truth. Everything you can read on disk — this
folder included — is a derived, human-legible view of it.

## The intent lives here, at the root

Read it first. It is written as plain, falsifiable statements.

- [`organizing-document.md`](organizing-document.md) — the segments, named.
- [`foundations.md`](foundations.md) — why hypercore exists.
- [`structure.md`](structure.md) — nodes, relations, clusters, material.
- [`statements.md`](statements.md) — what makes a statement worth keeping.
- [`endorsement.md`](endorsement.md) — who stands behind a statement.

## The engine is material

The implementation is tucked away in [`engine/`](engine/): the DuckDB store, the
command-line tool, and the browser viewer. You only open it to run something.

```sh
cd engine
../.venv/bin/python -m hypercore demo     # build a small demo graph
../.venv/bin/python -m hypercore serve    # view it at http://127.0.0.1:8000/
```

See [`engine/README.md`](engine/README.md) for the full command list and the
(load-bearing) environment notes.
