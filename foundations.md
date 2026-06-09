# foundations

hypercore is a small graph for a human and an agent to think with together.

The graph is the model: nodes, relations between them, clusters of relations, and material attached to nodes.

The database is the source of truth.

The files on disk are a derived view of the database. They exist so a human can read the graph and git can track how it changes.

The derived view is never read back into the database. A wrong rendering is fixed in the renderer, not on disk.

Material is the thing reality can contradict.

Every material corresponds to an intent.

Intent is the written model of what a part of hypercore is meant to be.

Intent carries current meaning, not every historical reason a statement exists.

If needed ground is absent from both intent and material, it is not assumed.
