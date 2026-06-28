---
kind: ask
state: standing
owner: operator
created: 1782672341
---
Interface slice 2 — the work renders as the tree, with scent and glyph-first state. The work view stops being a flat list: the standing work renders as the tree it is, each node's children nested beneath the node whose ask spawned them, and the view holds several foci at once because the work runs concurrently. A folded node is never an opaque dot — it shows a scent of what it holds (how many children, its shape, and whether what is under it passed or failed), so the operator reads where to look without unfolding it. A node's state reads from its glyph first, color only amplifying what the glyph already says; and motion is spent on one thing — a single slow pulse on running work, stillness everywhere else.

Folding condition: spec/interface.md carries the two requirements (the work renders as the tree with a scent on every folded node; state reads from the glyph first with a single slow pulse on running work) with their scenarios; the gated checks (the nested tree render, the folded-node scent, the glyph-first state read, the running-pulse marker) go red→green, and the slow pulse animating on running work is confirmed watched on the running window; python3 -m engine --check is green.
