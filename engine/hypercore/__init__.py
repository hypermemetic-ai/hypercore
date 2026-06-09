"""hypercore: a small graph store for humans and agents.

It stores nodes, relations, clusters as named sets of relations, and material
attached to nodes. DuckDB backs the store so the graph can be queried quickly.
"""

from .store import Store

__all__ = ["Store"]
