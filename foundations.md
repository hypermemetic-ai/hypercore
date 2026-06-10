# foundations

hypercore is a small graph for a human and an agent to think with together.

The graph is the model: nodes, relations between them, clusters of relations, and material attached to nodes.

The machine carries no memory between episodes of work. hypercore holds that memory outside the machine: the graph, not the running conversation, is the durable shared state. [machine]

The database is the source of truth.

The files on disk are a derived view of the database. They exist so a human can read the graph and git can track how it changes.

Intent is authored in the graph through the statement verbs; render is the files' only writer. The snapshot in git is the graph's durable form; the database file is a local working copy rebuilt from it with load. [machine]

The operator's attention is the scarcest resource in the system. The system spends it on judgment, never on filing. [machine]

The operator never performs graph maintenance. The machine files, links, and renders; the operator ratifies, vetoes, and redirects. An operator hand-tending the graph's bookkeeping is the earliest signal that ceremony has won. [machine]

The operator can read the system's state at a glance: the viewer shows who owns each statement and which work is open, without asking the machine. [machine]
