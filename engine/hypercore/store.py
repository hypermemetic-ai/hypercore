"""DuckDB-backed graph storage for hypercore."""

from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
import uuid

import duckdb


SCHEMA_PATH = Path(__file__).with_name("schema.sql")


class Store:
    """Wrap one DuckDB connection."""

    def __init__(self, path: str = "hypercore.duckdb", read_only: bool = False):
        self.path = path
        self.read_only = read_only
        self.con = duckdb.connect(path, read_only=read_only)
        if read_only:
            return

        self.con.execute(SCHEMA_PATH.read_text(encoding="utf-8"))
        self._load_duckpgq()
        self._create_property_graph()

    def close(self) -> None:
        self.con.close()

    def __enter__(self) -> "Store":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def add_node(
        self,
        kind: str,
        label: str,
        id: str | None = None,
        props: dict | None = None,
        id_prefix: str = "n_",
    ) -> str:
        node_id = id or self._new_id(id_prefix, "nodes")
        self._ensure_new("nodes", node_id)
        self.con.execute(
            "INSERT INTO nodes (id, kind, label, props) VALUES (?, ?, ?, ?)",
            [node_id, kind, label, self._json(props)],
        )
        return node_id

    def add_relation(
        self,
        src: str,
        dst: str,
        type: str,
        props: dict | None = None,
        id: str | None = None,
    ) -> str:
        relation_id = id or self._new_id("r_", "relations")
        self._ensure_new("relations", relation_id)
        self._ensure_exists("nodes", src, "source node")
        self._ensure_exists("nodes", dst, "destination node")
        self.con.execute(
            """
            INSERT INTO relations (id, src, dst, type, props)
            VALUES (?, ?, ?, ?, ?)
            """,
            [relation_id, src, dst, type, self._json(props)],
        )
        return relation_id

    def add_cluster(
        self,
        name: str,
        description: str | None = None,
        relations: list[str] | None = None,
        id: str | None = None,
    ) -> str:
        cluster_id = id or self._new_id("c_", "clusters")
        relation_ids = relations or []
        self._ensure_new("clusters", cluster_id)
        for relation_id in relation_ids:
            self._ensure_exists("relations", relation_id, "relation")

        self.con.execute("BEGIN")
        try:
            self.con.execute(
                "INSERT INTO clusters (id, name, description) VALUES (?, ?, ?)",
                [cluster_id, name, description],
            )
            for relation_id in relation_ids:
                self.con.execute(
                    """
                    INSERT INTO cluster_relations (cluster_id, relation_id)
                    VALUES (?, ?)
                    """,
                    [cluster_id, relation_id],
                )
            self.con.execute("COMMIT")
        except Exception:
            self.con.execute("ROLLBACK")
            raise
        return cluster_id

    def add_material(
        self,
        node_id: str,
        kind: str,
        label: str | None = None,
        lang: str | None = None,
        body: str | None = None,
        path: str | None = None,
        id: str | None = None,
    ) -> str:
        material_id = id or self._new_id("m_", "material")
        self._ensure_new("material", material_id)
        self._ensure_exists("nodes", node_id, "node")
        self.con.execute(
            """
            INSERT INTO material (id, node_id, kind, label, lang, body, path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [material_id, node_id, kind, label, lang, body, path],
        )
        return material_id

    def add_statement(
        self,
        text: str,
        segment: str,
        ord: int,
        owner: str = "machine",
        links: list[dict] | None = None,
        id: str | None = None,
    ) -> str:
        """Add one statement to the statement store. Statements are not nodes."""
        statement_id = id or self._new_id("s_", "statements")
        self._ensure_new("statements", statement_id)
        self.con.execute(
            """
            INSERT INTO statements (id, text, owner, segment, ord, links)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [statement_id, text, owner, segment, ord, self._json_list(links)],
        )
        return statement_id

    def update_statement(
        self,
        id: str,
        text: str | None = None,
        owner: str | None = None,
        ord: int | None = None,
        links: list[dict] | None = None,
    ) -> None:
        self._ensure_exists("statements", id, "statement")
        sets, params = [], []
        for column, value in (
            ("text", text),
            ("owner", owner),
            ("ord", ord),
            ("links", self._json_list(links) if links is not None else None),
        ):
            if value is not None:
                sets.append(f"{column} = ?")
                params.append(value)
        if sets:
            self.con.execute(
                f"UPDATE statements SET {', '.join(sets)} WHERE id = ?",
                params + [id],
            )

    def delete_statement(self, id: str) -> dict:
        """Delete a statement; returns its envelope so the caller can report
        the loss, including any links other statements held to it."""
        statement = self.statement(id)
        if statement is None:
            raise ValueError(f"statement '{id}' does not exist")
        linked_by = [
            s["id"]
            for s in self.statements()
            if any(link.get("to") == id for link in s["links"])
        ]
        self.con.execute("DELETE FROM statements WHERE id = ?", [id])
        statement["linked_by"] = linked_by
        return statement

    def statement(self, id: str) -> dict | None:
        row = self.con.execute(
            "SELECT id, text, owner, segment, ord, links FROM statements WHERE id = ?",
            [id],
        ).fetchone()
        return self._statement_dict(row) if row else None

    def statements(self, segment: str | None = None) -> list[dict]:
        """The statement store, ordered. The statements' own index."""
        sql = "SELECT id, text, owner, segment, ord, links FROM statements"
        params: list = []
        if segment is not None:
            sql += " WHERE segment = ?"
            params.append(segment)
        sql += " ORDER BY segment, ord, id"
        return [
            self._statement_dict(row)
            for row in self.con.execute(sql, params).fetchall()
        ]

    def statement_references(self, id: str) -> dict:
        """The reverse index: graph nodes that reference this statement.

        A node is `bound` by the statement when its props carry `on: id`, and
        `produced` it when `produces` contains the id. Statements left the
        graph (s_d4bd1b45), so this query answers what edges used to.
        """
        bound, produced = [], []
        for node in self.graph()["nodes"]:
            props = node.get("props", {})
            if props.get("on") == id:
                bound.append(node)
            if id in (props.get("produces") or []):
                produced.append(node)
        return {"bound": bound, "produced": produced}

    def statement_consequences(self, id: str) -> dict:
        """A statement's blast radius: what striking it would touch.

        Computed *before* any answer is rendered, so the decision is made
        with the breakage in view (s_070617cf): open work anchored on it
        loses its intent; folded work that produced it is left pointing at
        nothing; statements linking to it lose their target.
        """
        refs = self.statement_references(id)
        anchors_open = [
            n for n in refs["bound"]
            if (n.get("props") or {}).get("status") != "folded"
        ]
        anchors_folded = [
            n for n in refs["bound"]
            if (n.get("props") or {}).get("status") == "folded"
        ]
        linked_by = [
            s for s in self.statements()
            if any(link.get("to") == id for link in s["links"])
        ]
        return {
            "anchors_open": anchors_open,
            "anchors_folded": anchors_folded,
            "produced": refs["produced"],
            "linked_by": linked_by,
        }

    def record_decision(
        self,
        action: str,
        target: str,
        text: str | None = None,
        grounds: str | None = None,
        actor: str = "operator",
    ) -> str:
        """One row in the decision record: the answer, its grounds, its
        moment (s_565ca729). Written by endorse/amend/strike everywhere —
        the decision must survive the statement it answered."""
        decision_id = self._new_id("d_", "decisions")
        self.con.execute(
            """
            INSERT INTO decisions (id, action, target, text, grounds, actor)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [decision_id, action, target, text, grounds, actor],
        )
        return decision_id

    def decisions(self) -> list[dict]:
        """The decision record, oldest first."""
        rows = self.con.execute(
            """
            SELECT id, action, target, text, grounds, actor, created_at
            FROM decisions ORDER BY created_at, id
            """
        ).fetchall()
        return [
            {
                "id": r[0],
                "action": r[1],
                "target": r[2],
                "text": r[3],
                "grounds": r[4],
                "actor": r[5],
                "created_at": r[6].isoformat() if r[6] is not None else None,
            }
            for r in rows
        ]

    def dump_statements(self) -> dict:
        """The statement store as one JSON-ready dict: its durable form."""
        rows = self.con.execute(
            """
            SELECT id, text, owner, segment, ord, links, created_at
            FROM statements ORDER BY segment, ord, id
            """
        ).fetchall()
        statements = []
        for row in rows:
            statement = self._statement_dict(row)
            statement["created_at"] = (
                row[6].isoformat() if row[6] is not None else None
            )
            statements.append(statement)
        return {"statements": statements}

    def load_statements(self, data: dict) -> None:
        """Replace the statement store's contents with a dumped snapshot."""
        self.con.execute("DELETE FROM statements")
        for row in data.get("statements", []):
            self.con.execute(
                """
                INSERT INTO statements (id, text, owner, segment, ord, links, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    row["id"],
                    row["text"],
                    row["owner"],
                    row["segment"],
                    row["ord"],
                    self._json_list(row.get("links")),
                    row.get("created_at"),
                ],
            )

    def update_node(
        self,
        id: str,
        label: str | None = None,
        props_patch: dict | None = None,
    ) -> None:
        """Change a node's label and/or merge a patch into its props.

        A patch key set to None removes that key.
        """
        self._ensure_exists("nodes", id, "node")
        if label is not None:
            self.con.execute("UPDATE nodes SET label = ? WHERE id = ?", [label, id])
        if props_patch:
            row = self.con.execute(
                "SELECT props FROM nodes WHERE id = ?", [id]
            ).fetchone()
            props = self._parse_json(row[0])
            props.update(props_patch)
            props = {k: v for k, v in props.items() if v is not None}
            self.con.execute(
                "UPDATE nodes SET props = ? WHERE id = ?", [self._json(props), id]
            )

    def delete_node(self, id: str) -> dict:
        """Delete a node, its material, and every relation touching it.

        Returns what went with it, so the caller can report the loss rather
        than silently orphan the graph around it.
        """
        self._ensure_exists("nodes", id, "node")
        relations = self._relation_dicts(
            self.con.execute(
                "SELECT id, src, dst, type, props FROM relations WHERE src = ? OR dst = ?",
                [id, id],
            ).fetchall()
        )
        relation_ids = [relation["id"] for relation in relations]
        if relation_ids:
            placeholders = ",".join("?" for _ in relation_ids)
            self.con.execute(
                f"DELETE FROM cluster_relations WHERE relation_id IN ({placeholders})",
                relation_ids,
            )
            self.con.execute(
                f"DELETE FROM relations WHERE id IN ({placeholders})",
                relation_ids,
            )
        material_ids = [
            row[0]
            for row in self.con.execute(
                "SELECT id FROM material WHERE node_id = ?", [id]
            ).fetchall()
        ]
        self.con.execute("DELETE FROM material WHERE node_id = ?", [id])
        self.con.execute("DELETE FROM nodes WHERE id = ?", [id])
        return {"relations": relations, "material": material_ids}

    def dump(self) -> dict:
        """The whole store as one JSON-ready dict, bodies included.

        This is the durable form of the graph: deterministic, diffable, and
        loadable back without loss. The DuckDB file is only a working copy.
        """

        def rows(sql: str) -> list[dict]:
            cursor = self.con.execute(sql)
            columns = [d[0] for d in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

        data = {
            "nodes": rows(
                "SELECT id, kind, label, props, created_at FROM nodes ORDER BY id"
            ),
            "relations": rows(
                "SELECT id, src, dst, type, props, created_at FROM relations ORDER BY id"
            ),
            "clusters": rows(
                "SELECT id, name, description, created_at FROM clusters ORDER BY id"
            ),
            "cluster_relations": rows(
                """
                SELECT cluster_id, relation_id FROM cluster_relations
                ORDER BY cluster_id, relation_id
                """
            ),
            "material": rows(
                """
                SELECT id, node_id, kind, label, lang, body, path, created_at
                FROM material ORDER BY id
                """
            ),
            "decisions": rows(
                """
                SELECT id, action, target, text, grounds, actor, created_at
                FROM decisions ORDER BY created_at, id
                """
            ),
        }
        for table in data.values():
            for row in table:
                if "props" in row:
                    row["props"] = self._parse_json(row["props"])
                if row.get("created_at") is not None:
                    row["created_at"] = row["created_at"].isoformat()
        return data

    def load(self, data: dict) -> None:
        """Replace the store's contents with a dumped snapshot."""
        self.clear()
        for row in data.get("nodes", []):
            self.con.execute(
                "INSERT INTO nodes (id, kind, label, props, created_at) VALUES (?, ?, ?, ?, ?)",
                [
                    row["id"],
                    row["kind"],
                    row["label"],
                    self._json(row.get("props")),
                    row.get("created_at"),
                ],
            )
        for row in data.get("relations", []):
            self.con.execute(
                "INSERT INTO relations (id, src, dst, type, props, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                [
                    row["id"],
                    row["src"],
                    row["dst"],
                    row["type"],
                    self._json(row.get("props")),
                    row.get("created_at"),
                ],
            )
        for row in data.get("clusters", []):
            self.con.execute(
                "INSERT INTO clusters (id, name, description, created_at) VALUES (?, ?, ?, ?)",
                [row["id"], row["name"], row.get("description"), row.get("created_at")],
            )
        for row in data.get("cluster_relations", []):
            self.con.execute(
                "INSERT INTO cluster_relations (cluster_id, relation_id) VALUES (?, ?)",
                [row["cluster_id"], row["relation_id"]],
            )
        for row in data.get("material", []):
            self.con.execute(
                """
                INSERT INTO material (id, node_id, kind, label, lang, body, path, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    row["id"],
                    row["node_id"],
                    row["kind"],
                    row.get("label"),
                    row.get("lang"),
                    row.get("body"),
                    row.get("path"),
                    row.get("created_at"),
                ],
            )
        # Older snapshots predate the decision record; absence loads as empty.
        for row in data.get("decisions", []):
            self.con.execute(
                """
                INSERT INTO decisions (id, action, target, text, grounds, actor, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    row["id"],
                    row["action"],
                    row["target"],
                    row.get("text"),
                    row.get("grounds"),
                    row.get("actor", "operator"),
                    row.get("created_at"),
                ],
            )

    def neighbors(
        self,
        node: str,
        depth: int = 1,
        direction: str = "both",
    ) -> dict:
        if depth < 0:
            raise ValueError("depth must be zero or greater")
        self._ensure_exists("nodes", node, "node")
        edge_sql = self._edge_sql(direction)
        params = [node, node, depth]

        node_rows = self.con.execute(
            f"""
            WITH RECURSIVE walk(node_id, distance, node_path, relation_path) AS (
              SELECT ?, 0, list_value(?), []::VARCHAR[]
              UNION ALL
              SELECT e.to_id,
                     w.distance + 1,
                     list_append(w.node_path, e.to_id),
                     list_append(w.relation_path, e.id)
              FROM walk w
              JOIN ({edge_sql}) e ON e.from_id = w.node_id
              WHERE w.distance < ?
                AND NOT list_contains(w.node_path, e.to_id)
            ),
            nearest AS (
              SELECT node_id, min(distance) AS distance
              FROM walk
              GROUP BY node_id
            )
            SELECT n.id, n.kind, n.label, n.props, nearest.distance
            FROM nearest
            JOIN nodes n ON n.id = nearest.node_id
            ORDER BY nearest.distance, n.id
            """,
            params,
        ).fetchall()

        relation_rows = self.con.execute(
            f"""
            WITH RECURSIVE walk(node_id, distance, node_path, relation_path) AS (
              SELECT ?, 0, list_value(?), []::VARCHAR[]
              UNION ALL
              SELECT e.to_id,
                     w.distance + 1,
                     list_append(w.node_path, e.to_id),
                     list_append(w.relation_path, e.id)
              FROM walk w
              JOIN ({edge_sql}) e ON e.from_id = w.node_id
              WHERE w.distance < ?
                AND NOT list_contains(w.node_path, e.to_id)
            )
            SELECT DISTINCT r.id, r.src, r.dst, r.type, r.props
            FROM relations r
            JOIN (
              SELECT DISTINCT unnest(relation_path) AS relation_id
              FROM walk
              WHERE len(relation_path) > 0
            ) reached ON reached.relation_id = r.id
            ORDER BY r.id
            """,
            params,
        ).fetchall()

        return {
            "node": node,
            "depth": depth,
            "direction": direction,
            "nodes": [
                {
                    "id": row[0],
                    "kind": row[1],
                    "label": row[2],
                    "props": self._parse_json(row[3]),
                    "distance": row[4],
                }
                for row in node_rows
            ],
            "relations": self._relation_dicts(relation_rows),
        }

    def shortest_path(self, src: str, dst: str) -> dict:
        self._ensure_exists("nodes", src, "source node")
        self._ensure_exists("nodes", dst, "destination node")
        pgq_rows = self.con.execute(
            f"""
            FROM GRAPH_TABLE (hg MATCH p = ANY SHORTEST
              (a:nodes)-[e:relations]->{{1,8}}(b:nodes)
              WHERE a.id = {self._sql_literal(src)}
                AND b.id = {self._sql_literal(dst)}
              COLUMNS (
                a.label AS src_label,
                b.label AS dst_label,
                element_id(p) AS path_id
              ));
            """
        ).fetchall()
        if not pgq_rows:
            return {
                "src": src,
                "dst": dst,
                "found": False,
                "nodes": [],
                "relations": [],
            }

        path_row = self.con.execute(
            """
            WITH RECURSIVE paths(node_id, depth, node_path, relation_path) AS (
              SELECT ?, 0, list_value(?), []::VARCHAR[]
              UNION ALL
              SELECT r.dst,
                     p.depth + 1,
                     list_append(p.node_path, r.dst),
                     list_append(p.relation_path, r.id)
              FROM paths p
              JOIN relations r ON r.src = p.node_id
              WHERE p.depth < 8
                AND NOT list_contains(p.node_path, r.dst)
            )
            SELECT node_path, relation_path
            FROM paths
            WHERE node_id = ?
            ORDER BY depth
            LIMIT 1
            """,
            [src, src, dst],
        ).fetchone()

        pgq = pgq_rows[0]
        node_ids = path_row[0] if path_row else [src, dst]
        relation_ids = path_row[1] if path_row else []
        return {
            "src": src,
            "dst": dst,
            "found": True,
            "nodes": node_ids,
            "relations": relation_ids,
            "pgq": {
                "src_label": pgq[0],
                "dst_label": pgq[1],
                "path_id": pgq[2],
            },
        }

    def graph(self) -> dict:
        node_rows = self.con.execute(
            "SELECT id, kind, label, props FROM nodes ORDER BY id"
        ).fetchall()
        relation_rows = self.con.execute(
            "SELECT id, src, dst, type, props FROM relations ORDER BY id"
        ).fetchall()
        cluster_rows = self.con.execute(
            "SELECT id, name, description FROM clusters ORDER BY id"
        ).fetchall()
        cluster_relation_rows = self.con.execute(
            """
            SELECT cluster_id, relation_id
            FROM cluster_relations
            ORDER BY cluster_id, relation_id
            """
        ).fetchall()
        material_rows = self.con.execute(
            """
            SELECT id, node_id, kind, label, lang, path, body IS NOT NULL AS has_body
            FROM material
            ORDER BY node_id, id
            """
        ).fetchall()

        relation_ids_by_cluster = defaultdict(list)
        for cluster_id, relation_id in cluster_relation_rows:
            relation_ids_by_cluster[cluster_id].append(relation_id)

        material_by_node = defaultdict(list)
        for row in material_rows:
            material_by_node[row[1]].append(
                {
                    "id": row[0],
                    "kind": row[2],
                    "label": row[3],
                    "lang": row[4],
                    "path": row[5],
                    "has_body": bool(row[6]),
                }
            )

        return {
            "nodes": [
                {
                    "id": row[0],
                    "kind": row[1],
                    "label": row[2],
                    "props": self._parse_json(row[3]),
                }
                for row in node_rows
            ],
            "relations": self._relation_dicts(relation_rows),
            "clusters": [
                {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "relations": relation_ids_by_cluster[row[0]],
                }
                for row in cluster_rows
            ],
            "material": dict(material_by_node),
        }

    def material_body(self, material_id: str) -> str | None:
        row = self.con.execute(
            "SELECT body FROM material WHERE id = ?",
            [material_id],
        ).fetchone()
        if row is None:
            raise ValueError(f"material '{material_id}' does not exist")
        return row[0]

    def cluster_graph(self, cluster: str) -> dict:
        graph = self.graph()
        cluster_data = self._find_cluster(graph["clusters"], cluster)
        relation_ids = set(cluster_data["relations"])
        relations = [
            relation
            for relation in graph["relations"]
            if relation["id"] in relation_ids
        ]
        node_ids = {relation["src"] for relation in relations}
        node_ids.update(relation["dst"] for relation in relations)
        nodes = [node for node in graph["nodes"] if node["id"] in node_ids]
        material = {
            node_id: graph["material"].get(node_id, [])
            for node_id in sorted(node_ids)
        }
        return {
            "cluster": cluster_data,
            "nodes": nodes,
            "relations": relations,
            "material": material,
        }

    def clear(self) -> None:
        self.con.execute("BEGIN")
        try:
            self.con.execute("DROP PROPERTY GRAPH IF EXISTS hg;")
            for table in (
                "cluster_relations",
                "material",
                "clusters",
                "relations",
                "nodes",
                "statements",
                "decisions",
            ):
                self.con.execute(f"DROP TABLE IF EXISTS {table}")
            self.con.execute(SCHEMA_PATH.read_text(encoding="utf-8"))
            self._create_property_graph()
            self.con.execute("COMMIT")
        except Exception:
            self.con.execute("ROLLBACK")
            raise

    def _load_duckpgq(self) -> None:
        install_error = None
        try:
            self.con.execute("INSTALL duckpgq FROM community;")
        except Exception as exc:
            install_error = exc
        try:
            self.con.execute("LOAD duckpgq;")
        except Exception as exc:
            if install_error is not None:
                raise RuntimeError(
                    "could not load duckpgq after install failed: "
                    f"{install_error}; load error: {exc}"
                ) from exc
            raise

    def _create_property_graph(self) -> None:
        self.con.execute("DROP PROPERTY GRAPH IF EXISTS hg;")
        self.con.execute(
            """
            CREATE PROPERTY GRAPH hg
              VERTEX TABLES (nodes)
              EDGE TABLES (relations SOURCE KEY (src) REFERENCES nodes (id)
                                     DESTINATION KEY (dst) REFERENCES nodes (id));
            """
        )

    def _json(self, value: dict | None) -> str:
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise ValueError("props must be a JSON object")
        return json.dumps(value, sort_keys=True, separators=(",", ":"))

    def _parse_json(self, value):
        if value is None:
            return {}
        if isinstance(value, (dict, list)):
            return value
        return json.loads(value)

    def _json_list(self, value: list | None) -> str:
        if value is None:
            value = []
        if not isinstance(value, list):
            raise ValueError("links must be a JSON list")
        return json.dumps(value, sort_keys=True, separators=(",", ":"))

    def _statement_dict(self, row) -> dict:
        links = row[5]
        if not isinstance(links, list):
            links = json.loads(links) if links else []
        return {
            "id": row[0],
            "text": row[1],
            "owner": row[2],
            "segment": row[3],
            "ord": row[4],
            "links": links,
        }

    def _sql_literal(self, value: str) -> str:
        return "'" + value.replace("'", "''") + "'"

    def _new_id(self, prefix: str, table: str) -> str:
        while True:
            candidate = f"{prefix}{uuid.uuid4().hex[:8]}"
            if not self._exists(table, candidate):
                return candidate

    def _exists(self, table: str, id: str) -> bool:
        return (
            self.con.execute(
                f"SELECT 1 FROM {table} WHERE id = ? LIMIT 1",
                [id],
            ).fetchone()
            is not None
        )

    def _ensure_exists(self, table: str, id: str, name: str) -> None:
        if not self._exists(table, id):
            raise ValueError(f"{name} '{id}' does not exist")

    def _ensure_new(self, table: str, id: str) -> None:
        if self._exists(table, id):
            raise ValueError(f"{table[:-1]} '{id}' already exists")

    def _edge_sql(self, direction: str) -> str:
        if direction == "out":
            return "SELECT id, src AS from_id, dst AS to_id FROM relations"
        if direction == "in":
            return "SELECT id, dst AS from_id, src AS to_id FROM relations"
        if direction == "both":
            return """
            SELECT id, src AS from_id, dst AS to_id FROM relations
            UNION ALL
            SELECT id, dst AS from_id, src AS to_id FROM relations
            """
        raise ValueError("direction must be 'in', 'out', or 'both'")

    def _relation_dicts(self, rows) -> list[dict]:
        return [
            {
                "id": row[0],
                "src": row[1],
                "dst": row[2],
                "type": row[3],
                "props": self._parse_json(row[4]),
            }
            for row in rows
        ]

    def _find_cluster(self, clusters: list[dict], cluster: str) -> dict:
        for item in clusters:
            if item["id"] == cluster:
                return item
        for item in clusters:
            if item["name"] == cluster:
                return item
        raise ValueError(f"cluster '{cluster}' does not exist")
