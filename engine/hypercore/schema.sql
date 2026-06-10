-- hypercore graph store (DuckDB)
--
-- Six things live here: nodes, relations between nodes, clusters of relations
-- (a named subgraph that stands for a repeatable meta-operation), material
-- (documents / code / scripts) attached to a node, and statements — which are
-- NOT nodes (structure: s_d4bd1b45). Statements are intent; they live in their
-- own store with their own index. Nodes reference them by id in props: `on`
-- (the statement a node is bound by) and `produces` (statements it produced).
--
-- Referential integrity is enforced in the Python layer (store.py), not by
-- foreign-key constraints, so inserts are order-independent and we avoid
-- DuckDB's FK limitations. The "-- nodes.id" style comments record the intent.

CREATE TABLE IF NOT EXISTS nodes (
  id         VARCHAR PRIMARY KEY,
  kind       VARCHAR NOT NULL,
  label      VARCHAR NOT NULL,
  props      JSON DEFAULT '{}',
  created_at TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS relations (
  id         VARCHAR PRIMARY KEY,
  src        VARCHAR NOT NULL,   -- nodes.id
  dst        VARCHAR NOT NULL,   -- nodes.id
  type       VARCHAR NOT NULL,
  props      JSON DEFAULT '{}',
  created_at TIMESTAMP DEFAULT current_timestamp
);

-- A cluster is a named set of relations: a subgraph that stands for a
-- repeatable meta-operation. v0 captures the *structure* (which relations
-- belong to it). Replaying / instantiating a cluster against fresh nodes is a
-- later capability and is deliberately not implemented yet.
CREATE TABLE IF NOT EXISTS clusters (
  id          VARCHAR PRIMARY KEY,
  name        VARCHAR NOT NULL,
  description VARCHAR,
  created_at  TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS cluster_relations (
  cluster_id  VARCHAR NOT NULL,   -- clusters.id
  relation_id VARCHAR NOT NULL,   -- relations.id
  PRIMARY KEY (cluster_id, relation_id)
);

-- A statement is one unit of intent: plain prose in the body, everything formal
-- in the envelope (statements-12). Statements are not nodes; the graph's nodes
-- reference them by id. Inter-statement structure (depends-on, ...) lives in
-- `links`, not in the relations table.
CREATE TABLE IF NOT EXISTS statements (
  id         VARCHAR PRIMARY KEY,
  text       VARCHAR NOT NULL,    -- the statement, plain prose
  owner      VARCHAR NOT NULL,    -- 'operator' | 'machine' (pending endorsement)
  segment    VARCHAR NOT NULL,    -- which intent file it renders into
  ord        INTEGER NOT NULL,    -- position within the segment
  links      JSON DEFAULT '[]',   -- [{"type": ..., "to": statements.id}]
  created_at TIMESTAMP DEFAULT current_timestamp
);

-- Material is a document or output (code, script, ...) attached to a node.
-- Either inline (body) or by reference (path).
CREATE TABLE IF NOT EXISTS material (
  id         VARCHAR PRIMARY KEY,
  node_id    VARCHAR NOT NULL,   -- nodes.id
  kind       VARCHAR NOT NULL,   -- 'document' | 'code' | 'script' | ...
  label      VARCHAR,
  lang       VARCHAR,            -- e.g. 'markdown', 'python'
  body       VARCHAR,            -- inline content
  path       VARCHAR,            -- or external reference
  created_at TIMESTAMP DEFAULT current_timestamp
);
