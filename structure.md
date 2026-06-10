# structure

A node is a thing in the graph.

Intent is the written model of what the node is meant to be. Material is what the node actually made, the thing reality can contradict.

A relation is a directed, typed link from one node to another.

A cluster is a named set of relations: a subgraph that stands for a repeatable operation.

The intent lives at the root, as the markdown files there. Everything else in the repository is material.

The engine is material. It is the implementation that stores and serves the graph.

Nodes are operations. Intent statements are not nodes: they live in their own store with their own index. An operation points to the statements it produces and is bound by the statements it acts under; both are references the operation carries, not edges to statement nodes.
