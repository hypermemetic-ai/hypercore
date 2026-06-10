# work

Work happens as a graph. A node expresses an intent, and carrying it out grows a graph of further nodes: the steps, the candidates, the checks, the result.

That growing graph is an execution graph. It is a dynamically composed workflow, not a fixed template.

A folder holds one execution graph. The unit on disk is the execution graph, not the single node.

When the work is done, the execution graph folds into the node whose intent spawned it. The result becomes that node's material, and the steps become its history.

Folding preserves relations. A folded graph keeps its nodes and the relations between them, so the history reads as the graph it was, not a flat log.

A folding condition is what makes a graph ready to fold. Its intent is met, or it is abandoned. Until then the graph stays open.

A folding condition is machine-checkable or it spends operator judgment. Which of the two it is must be declared when the graph opens. [machine]

Trust in a folded graph comes from the checks at its boundary, not from the competence of whatever ran inside. An unchecked fold is a hope, not a result. [machine]

Error compounds through composition. The weaker a graph's checks, the shallower it must stay before folding. [machine]

Folding is reflected in both places. The database records the fold, and the filesystem view follows it.

An operation is one move on the problem state, of six kinds: frame, gather, derive, generate, test, commit. Work is made of operations.

The alphabet of operations never grows. Named clusters of operations are the compounds that grow freely; decomposition is how a compound expands, not a primitive.

Who proposes, executes, judges, and decides is a property on each operation, not an operation of its own. The decision to commit belongs to whoever owns the consequences and cannot be delegated. [machine]

Relations between operations carry the combinators. depends-on is the causal link from a consumer to what it consumes; tests, commits, and reframes bind a test, commit, or frame to what it acts on; decomposes-into expands a compound into its parts. Work membership stays contains, which is bookkeeping, not a combinator. [machine]

Execution graphs and folding were built in their first form, and the operation alphabet was named before its machinery, so the language existed before the machinery did. The work loop now speaks the alphabet: operations as nodes, combinators as relations, roles as props. [machine]
