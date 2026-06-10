# foundations

hypercore is a small graph for a human and an agent to think with together.

The graph is the model: nodes, relations between them, clusters of relations, and material attached to nodes.

The machine carries no memory between episodes of work. hypercore holds that memory outside the machine: the graph, not the running conversation, is the durable shared state.

The database is the source of truth.

The files on disk are a derived view of the database. They exist so a human can read the graph and git can track how it changes.

Intent is authored through the statement verbs; render is the files' only writer. The snapshot in git is the durable form of both the graph and the statement store; the database file is a local working copy rebuilt from it with load.

The operator's attention is the scarcest resource in the system. The system spends it on judgment, never on filing.

The operator never performs graph maintenance. The machine files, links, and renders; the operator ratifies, vetoes, and redirects. An operator hand-tending the graph's bookkeeping is the earliest signal that ceremony has won.

The operator can read the system's state at a glance: the viewer shows who owns each statement and which work is open, without asking the machine.

The viewer is where the operator acts, not only reads: the loop is visible live as operations land, whatever awaits operator judgment is summoned front and center, and endorsing, judging, and folding can be done there directly.

The operator's interface is a queue of decisions. A decision arrives with the context to decide it, the options on the table, and what each option entails: what it unblocks, what it breaks, what keeps running unbacked, and what reversing it later would cost.

Conversation and structured decisions are one channel: every decision accepts a free-form answer, free words land in the same ledger, and the machine's moves between decisions read back as a digest.

Whether work is done now, decomposed into subgraphs, deferred, or declined is itself a queued decision, and every decision records its grounds at the moment it is made.

The viewer is comfortable to live in: dark by default and easy on the eyes, readable, and live — changes to the graph appear as they are made, without the operator refreshing.

The viewer keeps itself current: it watches a cheap fingerprint of the store and re-derives the whole view when the graph moves. Staleness is the machine's to notice, never the operator's to manage.
