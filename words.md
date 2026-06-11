# words

## from the queue . 2026-06-11

operator (2026-06-11): I'm told a slice is waiting for acceptance but I don't see an acceptance card. what gives?

machine (2026-06-11): nothing waits — you already accepted it. the execution-graphs slice was approved on its card at 16:37 (c9b028b) and the card left then. what told you otherwise was the graph's own root node in the work view: I never folded graph-machinery when the acceptance landed, so its stale "awaits acceptance" kept standing. folded now (23aad96) — the first graph to reach its fold — and it has left the work view and the brief. no machinery was missing, only the edit; if a fold lags acceptance a second time, the seam earns its mechanics.

operator (2026-06-11): let's do it now, once is proof enough

machine (2026-06-11): built (1a25eb1) — the fold now rides the acceptance: a graph's acceptance card carries `graph: <name>`, and your y lands one commit that both retires the card and folds the root. no fold can lag again. verified in a throwaway clone; plain cards accept exactly as before. the slice awaits your acceptance on the queue — and a running hyper executes its launch-time code, so relaunch to carry it.

