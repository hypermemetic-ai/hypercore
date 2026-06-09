# structure

A node is a thing in the graph. It has a kind, a label, and free-form properties.

A relation is a directed, typed link from one node to another.

A cluster is a named set of relations: a subgraph that stands for a repeatable operation.

Material is a document, a piece of code, or a script attached to a node.

The intent lives at the root, as the markdown files there. Everything else in the repository is material.

The engine is material. It is the implementation that stores and serves the graph.

An operation, when it runs, produces a graph of its work plan, stored as a file with a diagram, with its material stored alongside. This is intended, not yet built.
