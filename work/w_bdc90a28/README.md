# statements leave the graph

`w_bdc90a28` · **folded** · check: machine

on: `s_d4bd1b45` — "Nodes are operations. Intent statements are not nodes: they live in their own store with …"
fold when: graph.json holds no statement or segment nodes; statements live in a git-tracked store with envelope (id, text, owner, segment, order); operations and work reference statements by id, and show answers the reverse direction (statement to referencing nodes); every existing verb, render, load, and the viewer work unchanged
folded: 2026-06-10T07:59:34+00:00

## check

- `wn_19ef184c` graph.json holds no statement or segment nodes (kinds: node, work, step, check, candidate, result)
- `wn_37f527f7` verbs, render, load, ingest, traversals, and viewer verified in a throwaway copy: statement cycle round-trips byte-identical; work cycle folds with material on the work node; /api/graph serves graph plus store
- `wn_b62bb2c0` show on a statement answers the reverse direction: bound work, producing work, links both ways, material via the bound work
- `wn_bace3a36` statements.json holds all 51 statements with envelope: id, text, owner, segment, ord, links, created_at

## result

- `wn_d15d98dc` statements live beside the graph: statements table + statements.json, nodes reference them via on/produces props, show answers the reverse index, all verbs and views unchanged

## step

- `wn_4f3f1afd` statements table added to schema; store grows statement CRUD, dump/load, and the reverse index (statement_references)
- `wn_6aa98a1d` verbs rewired: statement verbs speak to the store; work-open binds by id; work-fold attaches material to the work node; render reads the store; load reads both snapshots
- `wn_c8557eb8` one-time migration: 51 statements moved with envelope and 2 depends-on links; spawned-by relations became on/produces props; m_cca715e7 rehomed to w_423ff83b; statement and segment nodes deleted

## material

- [statements leave the graph](m_d318801f.md) (result) — on the work
