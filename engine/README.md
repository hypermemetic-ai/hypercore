# engine

The implementation behind hypercore: a DuckDB-backed graph store, a command-line
tool, and a small browser viewer. hypercore's intent lives at the repository
root; this folder is material. Run everything from here.

## Run

```sh
# uses the project virtualenv at ../.venv (Python 3.12)
../.venv/bin/python -m hypercore demo                       # build a demo graph
../.venv/bin/python -m hypercore graph                      # whole graph as JSON
../.venv/bin/python -m hypercore neighbors --node source --depth 2
../.venv/bin/python -m hypercore path --from source --to sink
../.venv/bin/python -m hypercore serve                      # http://127.0.0.1:8000/
```

Query commands print JSON (readable by both humans and agents). Mutation
commands — `add-node`, `add-relation`, `add-cluster`, `add-material` — print the
new id. `--db PATH` chooses the database file (default `hypercore.duckdb`).

Intent and work have their own verbs: `add-statement` / `amend` / `strike` /
`endorse` for statements, `work-open` / `work-add` / `work-check` / `work-fold`
for execution graphs, `status` / `show` to navigate. Statements are **not
nodes** (structure: s_d4bd1b45): they live in their own store with their own
index, and graph nodes reference them by id — `on` for the statement a node is
bound by, `produces` for statements it produced. `show <statement-id>` answers
the reverse direction. Every mutating verb rewrites the root markdown and both
snapshots — `graph.json` (the graph) and `statements.json` (the statement
store), the durable, git-tracked forms; the `.duckdb` file is ignored by git
and rebuilt from them with `load`. `ingest` only bootstraps an empty database
from the files.

The viewer opens the database **read-only**. Change the graph with the CLI, then
refresh the browser.

## Environment — do not change, do not re-derive

These were established empirically; changing them reintroduces crashes.

- **Python 3.12.** The project venv (`../.venv`) is 3.12. Python 3.13/3.14 with
  the duckpgq community build **segfault on `LOAD`**.
- **duckdb == 1.4.1** (pinned in `requirements.txt`). 1.5.0/1.5.1 **segfault on
  `LOAD duckpgq`**; 1.5.2/1.5.3 have **no duckpgq build**.
- **DuckPGQ** powers `path` (shortest path). It loads with
  `INSTALL duckpgq FROM community;` then `LOAD duckpgq;` — already cached, so it
  works offline. `LOAD duckpgq` runs on every connection that uses graph queries.

## Layout

- `hypercore/` — the Python package: `store.py` (the store), `cli.py` /
  `__main__.py` (the command-line tool), `schema.sql` (the data model, the
  source of truth), `server.py` (the viewer's server).
- `web/` — the browser viewer (Cytoscape.js from a CDN; no build step).
- `requirements.txt` — the one dependency, `duckdb`.
