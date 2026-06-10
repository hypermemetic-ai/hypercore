# structure

A node is a thing in the graph.

Intent starts work; material is what the work makes. Finished material must provably map back onto the intent that started it. [machine]

A relation links one node to another and says what the link means. [machine]

The intent lives at the root, as the markdown files there. Everything else in the repository is material. [machine]

The engine is material. It is the implementation that stores and serves the graph. [machine]

Nodes are operations. Intent statements are not nodes: they live in their own store with their own index. An operation points to the statements it produces and is bound by the statements it acts under; both are references the operation carries, not edges to statement nodes. [machine]
