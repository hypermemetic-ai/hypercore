# work

Work happens as a graph. A node expresses an intent, and carrying it out grows a graph of further nodes: the steps, the candidates, the checks, the result.

That growing graph is an execution graph. It is a dynamically composed workflow, not a fixed template.

A folder holds one execution graph. The unit on disk is the execution graph, not the single node.

When the work is done, the execution graph folds into the node whose intent spawned it. The result becomes that node's material, and the steps become its history.

Folding preserves relations. A folded graph keeps its nodes and the relations between them, so the history reads as the graph it was, not a flat log.

A folding condition is what makes a graph ready to fold. Its intent is met, or it is abandoned. Until then the graph stays open.

Trust in a folded graph comes from the checks at its boundary, not from the competence of whatever ran inside. An unchecked fold is a hope, not a result.

Error compounds through composition. The weaker a graph's checks, the shallower it must stay before folding.

Folding is reflected in both places. The database records the fold, and the filesystem view follows it.

An operation is one move on the problem state, of six kinds: frame, gather, derive, generate, test, commit. Work is made of operations.

The alphabet of operations never grows. Named clusters of operations are the compounds that grow freely; decomposition is how a compound expands, not a primitive.

An operation earns a node when it crosses the operator–machine boundary or when a fold depends on its standing; reasoning that stays inside one party is absorbed into the operations it serves. The graph is a commitment ledger, not a trace of everything thought.

Derive is on probation: as of 2026-06-10 no derive operation has been recorded. A multi-step projection worth checking independently of the verdict it feeds is a derive and is recorded as one. If derive stays unused through inference-heavy work, the operator decides whether it folds into test and gather. [machine]
