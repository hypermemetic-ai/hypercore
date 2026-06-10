"""Command line tool for hypercore."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from .server import serve
from .store import Store

# The intent files live at the repository root; the engine is one level down.
INTENT_ROOT = Path(__file__).resolve().parents[2]

# The segments whose intent is a list of statements, and so is graph-native:
# ingested from these files into statement nodes, then rendered back out.
SEGMENTS = ("foundations", "structure", "statements", "endorsement", "work")

# A machine-owned statement carries this marker at its end in the derived view
# (see endorsement.md). The marker is envelope, not prose: ingest strips it into
# the node's owner prop, render writes it back. The operator endorses with the
# endorse verb; render then drops the marker.
OWNER_MARKER = " [machine]"

# The graph's durable, git-tracked form. The DuckDB file is ignored by git, so
# every mutating verb rewrites this snapshot alongside the markdown views;
# `load` rebuilds a local database from it without loss.
GRAPH_SNAPSHOT = INTENT_ROOT / "engine" / "graph.json"


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    try:
        return args.func(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m hypercore",
        description="Store and explore a small graph.",
    )
    parser.add_argument(
        "--db",
        default="hypercore.duckdb",
        help="DuckDB file to use. Default: hypercore.duckdb.",
    )
    subparsers = parser.add_subparsers(dest="command")

    init = subparsers.add_parser("init", help="Create the database if needed.")
    init.set_defaults(func=cmd_init)

    add_node = subparsers.add_parser("add-node", help="Add one node.")
    add_node.add_argument("--kind", required=True, help="Node kind.")
    add_node.add_argument("--label", required=True, help="Node label.")
    add_node.add_argument("--id", help="Node id. A short id is made if omitted.")
    add_node.add_argument("--props", type=json_object, help="JSON object.")
    add_node.set_defaults(func=cmd_add_node)

    add_relation = subparsers.add_parser(
        "add-relation",
        help="Add one relation between two nodes.",
    )
    add_relation.add_argument("--src", required=True, help="Source node id.")
    add_relation.add_argument("--dst", required=True, help="Destination node id.")
    add_relation.add_argument("--type", required=True, help="Relation type.")
    add_relation.add_argument(
        "--id",
        help="Relation id. A short id is made if omitted.",
    )
    add_relation.add_argument("--props", type=json_object, help="JSON object.")
    add_relation.set_defaults(func=cmd_add_relation)

    add_cluster = subparsers.add_parser(
        "add-cluster",
        help="Add a cluster, which is a named set of relations.",
    )
    add_cluster.add_argument("--name", required=True, help="Cluster name.")
    add_cluster.add_argument("--description", help="Short description.")
    add_cluster.add_argument(
        "--relation",
        action="append",
        default=[],
        help="Relation id to include. Use more than once for more relations.",
    )
    add_cluster.add_argument(
        "--id",
        help="Cluster id. A short id is made if omitted.",
    )
    add_cluster.set_defaults(func=cmd_add_cluster)

    add_material = subparsers.add_parser(
        "add-material",
        help="Attach material to one node.",
    )
    add_material.add_argument("--node", required=True, help="Node id.")
    add_material.add_argument("--kind", required=True, help="Material kind.")
    add_material.add_argument("--label", help="Material label.")
    add_material.add_argument("--lang", help="Language, such as markdown or python.")
    add_material.add_argument("--body", help="Inline text body.")
    add_material.add_argument("--path", help="Path to external material.")
    add_material.add_argument(
        "--id",
        help="Material id. A short id is made if omitted.",
    )
    add_material.set_defaults(func=cmd_add_material)

    neighbors = subparsers.add_parser(
        "neighbors",
        help="Show nearby nodes and reached relations as JSON.",
    )
    neighbors.add_argument("--node", required=True, help="Starting node id.")
    neighbors.add_argument(
        "--depth",
        type=int,
        default=1,
        help="How many hops to walk. Default: 1.",
    )
    neighbors.add_argument(
        "--direction",
        choices=("in", "out", "both"),
        default="both",
        help="Walk incoming, outgoing, or both directions. Default: both.",
    )
    neighbors.set_defaults(func=cmd_neighbors)

    path = subparsers.add_parser(
        "path",
        help="Show the shortest directed path as JSON.",
    )
    path.add_argument("--from", dest="src", required=True, help="Source node id.")
    path.add_argument("--to", dest="dst", required=True, help="Destination node id.")
    path.set_defaults(func=cmd_path)

    cluster = subparsers.add_parser(
        "cluster",
        help="Show one cluster's subgraph as JSON.",
    )
    cluster.add_argument("cluster", help="Cluster id or exact name.")
    cluster.set_defaults(func=cmd_cluster)

    graph = subparsers.add_parser("graph", help="Show the whole graph as JSON.")
    graph.set_defaults(func=cmd_graph)

    demo = subparsers.add_parser("demo", help="Create a small demo graph.")
    demo.set_defaults(func=cmd_demo)

    ingest = subparsers.add_parser(
        "ingest",
        help="Bootstrap an empty database from the intent files.",
    )
    ingest.set_defaults(func=cmd_ingest)

    render = subparsers.add_parser(
        "render",
        help="Write the derived views from the graph: intent files and snapshot.",
    )
    render.set_defaults(func=cmd_render)

    load = subparsers.add_parser(
        "load",
        help="Rebuild the local database from the snapshot (engine/graph.json).",
    )
    load.add_argument(
        "--replace",
        action="store_true",
        help="Allow replacing a non-empty database.",
    )
    load.set_defaults(func=cmd_load)

    add_statement = subparsers.add_parser(
        "add-statement",
        help="Add one statement to a segment and rewrite the views.",
    )
    add_statement.add_argument(
        "--segment", required=True, choices=SEGMENTS, help="Segment to add to."
    )
    add_statement.add_argument(
        "--text", required=True, help="The statement, plain prose."
    )
    add_statement.add_argument(
        "--after", help="Statement id to insert after. Default: end of segment."
    )
    add_statement.add_argument(
        "--owner",
        choices=("machine", "operator"),
        default="machine",
        help="Who stands behind it. Default: machine, pending endorsement.",
    )
    add_statement.set_defaults(func=cmd_add_statement)

    amend = subparsers.add_parser(
        "amend",
        help="Rewrite one statement's text and rewrite the views.",
    )
    amend.add_argument("id", help="Statement id.")
    amend.add_argument("--text", required=True, help="The new text.")
    amend.add_argument(
        "--by",
        choices=("machine", "operator"),
        default="machine",
        help="Who is amending. Amending takes ownership. Default: machine.",
    )
    amend.set_defaults(func=cmd_amend)

    strike = subparsers.add_parser(
        "strike",
        help="Remove one statement and rewrite the views.",
    )
    strike.add_argument("id", help="Statement id.")
    strike.add_argument(
        "--by",
        choices=("machine", "operator"),
        default="machine",
        help="Who is striking. The machine never strikes operator-owned intent.",
    )
    strike.set_defaults(func=cmd_strike)

    endorse = subparsers.add_parser(
        "endorse",
        help="Take machine-owned statements on as the operator.",
    )
    endorse.add_argument("ids", nargs="+", help="Statement ids.")
    endorse.set_defaults(func=cmd_endorse)

    work_open = subparsers.add_parser(
        "work-open",
        help="Open an execution graph against a node.",
    )
    work_open.add_argument(
        "--on", required=True, help="Node whose intent spawns the work."
    )
    work_open.add_argument("--label", required=True, help="What the work is.")
    work_open.add_argument(
        "--fold-when",
        required=True,
        dest="fold_when",
        help="The folding condition, declared at open.",
    )
    work_open.add_argument(
        "--check",
        required=True,
        choices=("machine", "operator"),
        help="machine: recorded checks must pass to fold. "
        "operator: folding spends operator judgment.",
    )
    work_open.set_defaults(func=cmd_work_open)

    work_add = subparsers.add_parser(
        "work-add",
        help="Add a step, candidate, check, or result to open work.",
    )
    work_add.add_argument("work", help="Work id.")
    work_add.add_argument(
        "--kind",
        required=True,
        choices=("step", "candidate", "check", "result"),
        help="What kind of work node this is.",
    )
    work_add.add_argument("--label", required=True, help="What it is.")
    work_add.add_argument("--props", type=json_object, help="JSON object.")
    work_add.set_defaults(func=cmd_work_add)

    work_check = subparsers.add_parser(
        "work-check",
        help="Record a check's outcome.",
    )
    work_check.add_argument("check", help="Check node id.")
    work_check.add_argument(
        "--outcome", required=True, choices=("pass", "fail"), help="The outcome."
    )
    work_check.set_defaults(func=cmd_work_check)

    work_fold = subparsers.add_parser(
        "work-fold",
        help="Fold an execution graph into the node that spawned it.",
    )
    work_fold.add_argument("work", help="Work id.")
    work_fold.add_argument(
        "--abandoned",
        action="store_true",
        help="Fold as abandoned: no result, no checks required.",
    )
    work_fold.add_argument(
        "--operator-confirms",
        action="store_true",
        dest="operator_confirms",
        help="Record the operator's judgment for an operator-checked fold.",
    )
    work_fold.set_defaults(func=cmd_work_fold)

    status = subparsers.add_parser(
        "status",
        help="Where things stand: pending endorsements, open work, recent folds.",
    )
    status.set_defaults(func=cmd_status)

    show = subparsers.add_parser("show", help="One node, human-legible.")
    show.add_argument("node", help="Node id.")
    show.set_defaults(func=cmd_show)

    serve_cmd = subparsers.add_parser("serve", help="Serve the browser view.")
    serve_cmd.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind. Default: 127.0.0.1.",
    )
    serve_cmd.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind. Default: 8000.",
    )
    serve_cmd.set_defaults(func=cmd_serve)

    return parser


def json_object(text: str) -> dict:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc
    if not isinstance(value, dict):
        raise argparse.ArgumentTypeError("must be a JSON object")
    return value


def print_json(value) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def cmd_init(args) -> int:
    with Store(args.db):
        pass
    print(f"initialized {args.db}")
    return 0


def cmd_add_node(args) -> int:
    with Store(args.db) as store:
        print(store.add_node(args.kind, args.label, id=args.id, props=args.props))
    return 0


def cmd_add_relation(args) -> int:
    with Store(args.db) as store:
        print(
            store.add_relation(
                args.src,
                args.dst,
                args.type,
                id=args.id,
                props=args.props,
            )
        )
    return 0


def cmd_add_cluster(args) -> int:
    with Store(args.db) as store:
        print(
            store.add_cluster(
                args.name,
                description=args.description,
                relations=args.relation,
                id=args.id,
            )
        )
    return 0


def cmd_add_material(args) -> int:
    with Store(args.db) as store:
        print(
            store.add_material(
                args.node,
                args.kind,
                label=args.label,
                lang=args.lang,
                body=args.body,
                path=args.path,
                id=args.id,
            )
        )
    return 0


def cmd_neighbors(args) -> int:
    with Store(args.db, read_only=True) as store:
        print_json(store.neighbors(args.node, args.depth, args.direction))
    return 0


def cmd_path(args) -> int:
    with Store(args.db) as store:
        print_json(store.shortest_path(args.src, args.dst))
    return 0


def cmd_cluster(args) -> int:
    with Store(args.db, read_only=True) as store:
        print_json(store.cluster_graph(args.cluster))
    return 0


def cmd_graph(args) -> int:
    with Store(args.db, read_only=True) as store:
        print_json(store.graph())
    return 0


def cmd_demo(args) -> int:
    with Store(args.db) as store:
        store.clear()
        nodes = {
            "source": store.add_node(
                "dataset",
                "Source data",
                id="source",
                props={"format": "csv"},
            ),
            "transform": store.add_node(
                "process",
                "Transform",
                id="transform",
                props={"runtime": "python"},
            ),
            "sink": store.add_node(
                "dataset",
                "Sink data",
                id="sink",
                props={"format": "parquet"},
            ),
            "spec": store.add_node(
                "spec",
                "Pipeline spec",
                id="spec",
                props={"status": "demo"},
            ),
        }
        relations = {
            "source_feeds_transform": store.add_relation(
                "source",
                "transform",
                "feeds",
                id="source_feeds_transform",
            ),
            "transform_writes_sink": store.add_relation(
                "transform",
                "sink",
                "writes",
                id="transform_writes_sink",
            ),
            "spec_governs_transform": store.add_relation(
                "spec",
                "transform",
                "governs",
                id="spec_governs_transform",
            ),
        }
        cluster = store.add_cluster(
            "source to sink build",
            description="Relations that move source data through the transform.",
            relations=[
                "source_feeds_transform",
                "transform_writes_sink",
            ],
            id="build_flow",
        )
        material = {
            "source_note": store.add_material(
                "source",
                "document",
                label="Source note",
                lang="markdown",
                body="# Source data\n\nDemo input for graph traversal.\n",
                id="source_note",
            ),
            "transform_script": store.add_material(
                "transform",
                "script",
                label="Transform script",
                lang="python",
                body=(
                    "def transform(rows):\n"
                    "    return [dict(row, cleaned=True) for row in rows]\n"
                ),
                id="transform_script",
            ),
        }
    print_json(
        {
            "database": args.db,
            "nodes": nodes,
            "relations": relations,
            "cluster": cluster,
            "material": material,
        }
    )
    return 0


def parse_intent(path: Path) -> tuple[str, list[tuple[str, str]]]:
    """Split one intent file into its title and its (statement, owner) pairs.

    Each statement is one blank-line-separated paragraph. The leading `# ...`
    heading, if present, is the title. A statement ending with the owner marker
    is machine-owned; the marker is stripped here and re-added by render. This
    is the one place that reads the derived view back in, while the files are
    still where intent is authored.
    """
    blocks = [b.strip() for b in path.read_text(encoding="utf-8").split("\n\n")]
    blocks = [b for b in blocks if b]
    title = path.stem
    statements: list[tuple[str, str]] = []
    for index, block in enumerate(blocks):
        if index == 0 and block.startswith("#"):
            title = block.lstrip("#").strip()
            continue
        text = " ".join(line.strip() for line in block.splitlines())
        owner = "operator"
        if text.endswith(OWNER_MARKER):
            text = text[: -len(OWNER_MARKER)].rstrip()
            owner = "machine"
        statements.append((text, owner))
    return title, statements


def cmd_ingest(args) -> int:
    """Bootstrap an empty database from the intent files.

    Builds hypercore's own node, a node per segment, and a node per statement.
    Once statements exist, the graph is authored with the statement verbs and
    ingest refuses to run: re-reading the derived view would erase ids and
    semantic relations. A local database is rebuilt from the snapshot instead.
    """
    loaded: dict[str, list[str]] = {}
    machine_owned: list[str] = []
    with Store(args.db) as store:
        existing = store.con.execute(
            "SELECT count(*) FROM nodes WHERE kind = 'statement'"
        ).fetchone()[0]
        if existing:
            print(
                f"{existing} statement nodes already exist. The graph is "
                "authored with the statement verbs now (add-statement, amend, "
                "strike, endorse); ingest only bootstraps an empty database. "
                "To rebuild a local database from the snapshot, run: "
                "python -m hypercore load",
                file=sys.stderr,
            )
            return 1
        store.clear()
        store.add_node(
            "node",
            "hypercore",
            id="hypercore",
            props={"role": "root", "intent": "organizing-document.md"},
        )
        store.add_material(
            "hypercore", "code", label="the engine", lang="python", path="engine"
        )
        for seg in SEGMENTS:
            title, statements = parse_intent(INTENT_ROOT / f"{seg}.md")
            store.add_node(
                "segment", title, id=seg, props={"title": title, "renders_to": f"{seg}.md"}
            )
            store.add_relation("hypercore", seg, "contains", id=f"hypercore-contains-{seg}")
            ids: list[str] = []
            for ordinal, (text, owner) in enumerate(statements, start=1):
                sid = f"{seg}-{ordinal}"
                store.add_node(
                    "statement",
                    text,
                    id=sid,
                    props={"ord": ordinal, "segment": seg, "owner": owner},
                )
                store.add_relation(seg, sid, "contains", id=f"{seg}-contains-{ordinal}")
                ids.append(sid)
                if owner == "machine":
                    machine_owned.append(sid)
            loaded[seg] = ids
        views = write_views(store)
    # The operator must be informed of machine-owned intent (statements.md), so
    # the summary names it rather than burying it in props.
    print_json(
        {
            "database": args.db,
            "counts": {seg: len(ids) for seg, ids in loaded.items()},
            "statements": loaded,
            "machine_owned": machine_owned,
            **views,
        }
    )
    return 0


def render_files(graph: dict) -> list[str]:
    """Write the intent files from the graph: the derived, human-legible view.

    Source of truth is the graph. A wrong rendering is fixed here, never by
    editing the file on disk.
    """
    by_id = {node["id"]: node for node in graph["nodes"]}
    contained = defaultdict(list)
    for relation in graph["relations"]:
        if relation["type"] == "contains":
            contained[relation["src"]].append(relation["dst"])

    written: list[str] = []
    for seg in SEGMENTS:
        segment = by_id.get(seg)
        if segment is None:
            continue
        statements = [
            by_id[dst]
            for dst in contained.get(seg, [])
            if by_id.get(dst, {}).get("kind") == "statement"
        ]
        statements.sort(key=lambda node: node["props"].get("ord", 0))
        lines = [f"# {segment['props'].get('title', seg)}", ""]
        for statement in statements:
            label = statement["label"]
            if statement["props"].get("owner") == "machine":
                label += OWNER_MARKER
            lines.append(label)
            lines.append("")
        text = "\n".join(lines).rstrip() + "\n"
        (INTENT_ROOT / f"{seg}.md").write_text(text, encoding="utf-8")
        written.append(f"{seg}.md")
    return written


def write_views(store: Store) -> dict:
    """Rewrite everything derived from the graph: intent files and snapshot.

    Every mutating verb ends here, so the views never lag the graph and git
    always tracks the graph's durable form.
    """
    rendered = render_files(store.graph())
    snapshot = store.dump()
    GRAPH_SNAPSHOT.write_text(
        json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return {"rendered": rendered, "snapshot": "engine/graph.json"}


def cmd_render(args) -> int:
    with Store(args.db, read_only=True) as store:
        views = write_views(store)
    print_json({"database": args.db, **views})
    return 0


def cmd_load(args) -> int:
    if not GRAPH_SNAPSHOT.exists():
        raise ValueError(f"no snapshot at {GRAPH_SNAPSHOT}")
    data = json.loads(GRAPH_SNAPSHOT.read_text(encoding="utf-8"))
    with Store(args.db) as store:
        existing = store.con.execute("SELECT count(*) FROM nodes").fetchone()[0]
        if existing and not args.replace:
            raise ValueError(
                f"database has {existing} nodes; re-run with --replace to "
                "rebuild it from the snapshot"
            )
        store.load(data)
    print_json(
        {
            "database": args.db,
            "loaded": {table: len(rows) for table, rows in data.items()},
        }
    )
    return 0


def fetch_node(store: Store, id: str, kind: str | None = None) -> dict:
    row = store.con.execute(
        "SELECT id, kind, label, props FROM nodes WHERE id = ?", [id]
    ).fetchone()
    if row is None:
        raise ValueError(f"node '{id}' does not exist")
    props = row[3]
    node = {
        "id": row[0],
        "kind": row[1],
        "label": row[2],
        "props": json.loads(props) if isinstance(props, str) else (props or {}),
    }
    if kind is not None and node["kind"] != kind:
        raise ValueError(f"'{id}' is a {node['kind']}, not a {kind}")
    return node


def segment_statements(store: Store, seg: str) -> list[dict]:
    statements = [
        node
        for node in store.graph()["nodes"]
        if node["kind"] == "statement" and node["props"].get("segment") == seg
    ]
    statements.sort(key=lambda node: node["props"].get("ord", 0))
    return statements


def renumber_segment(store: Store, seg: str) -> None:
    """Make a segment's ords 1..n again. Ids never change; only the ordering
    prop is the machine's bookkeeping to keep tidy."""
    for ordinal, statement in enumerate(segment_statements(store, seg), start=1):
        if statement["props"].get("ord") != ordinal:
            store.update_node(statement["id"], props_patch={"ord": ordinal})


def cmd_add_statement(args) -> int:
    with Store(args.db) as store:
        fetch_node(store, args.segment, kind="segment")
        statements = segment_statements(store, args.segment)
        if args.after:
            ords = {s["id"]: s["props"].get("ord", 0) for s in statements}
            if args.after not in ords:
                raise ValueError(
                    f"'{args.after}' is not a statement in segment '{args.segment}'"
                )
            ord_value = ords[args.after] + 0.5
        elif statements:
            ord_value = statements[-1]["props"].get("ord", 0) + 1
        else:
            ord_value = 1
        sid = store.add_node(
            "statement",
            args.text,
            id_prefix="s_",
            props={"segment": args.segment, "ord": ord_value, "owner": args.owner},
        )
        store.add_relation(args.segment, sid, "contains")
        renumber_segment(store, args.segment)
        views = write_views(store)
    print_json({"id": sid, "segment": args.segment, "owner": args.owner, **views})
    return 0


def cmd_amend(args) -> int:
    with Store(args.db) as store:
        node = fetch_node(store, args.id, kind="statement")
        previous_owner = node["props"].get("owner", "operator")
        store.update_node(args.id, label=args.text, props_patch={"owner": args.by})
        views = write_views(store)
    out = {"id": args.id, "owner": args.by, **views}
    if args.by == "machine" and previous_owner == "operator":
        out["note"] = (
            "operator-owned statement amended by the machine; "
            "it is machine-owned until endorsed again"
        )
    print_json(out)
    return 0


def cmd_strike(args) -> int:
    with Store(args.db) as store:
        node = fetch_node(store, args.id, kind="statement")
        owner = node["props"].get("owner", "operator")
        if owner == "operator" and args.by != "operator":
            raise ValueError(
                "the machine never strikes operator-owned intent; "
                "re-run with --by operator if this is the operator's decision"
            )
        removed = store.delete_node(args.id)
        renumber_segment(store, node["props"].get("segment", ""))
        views = write_views(store)
    semantic = [r for r in removed["relations"] if r["type"] != "contains"]
    print_json(
        {
            "struck": args.id,
            "label": node["label"],
            "semantic_relations_lost": semantic,
            **views,
        }
    )
    return 0


def cmd_endorse(args) -> int:
    endorsed: list[str] = []
    already: list[str] = []
    with Store(args.db) as store:
        for sid in args.ids:
            node = fetch_node(store, sid, kind="statement")
            if node["props"].get("owner") == "operator":
                already.append(sid)
            else:
                store.update_node(sid, props_patch={"owner": "operator"})
                endorsed.append(sid)
        views = write_views(store)
    print_json({"endorsed": endorsed, "already_operator_owned": already, **views})
    return 0


def cmd_work_open(args) -> int:
    with Store(args.db) as store:
        fetch_node(store, args.on)
        wid = store.add_node(
            "work",
            args.label,
            id_prefix="w_",
            props={
                "status": "open",
                "on": args.on,
                "fold_when": args.fold_when,
                "check": args.check,
            },
        )
        store.add_relation(wid, args.on, "spawned-by")
        views = write_views(store)
    print_json(
        {
            "id": wid,
            "on": args.on,
            "check": args.check,
            "fold_when": args.fold_when,
            **views,
        }
    )
    return 0


def work_members(store: Store, work_id: str) -> list[dict]:
    graph = store.graph()
    by_id = {node["id"]: node for node in graph["nodes"]}
    return [
        by_id[relation["dst"]]
        for relation in graph["relations"]
        if relation["type"] == "contains"
        and relation["src"] == work_id
        and relation["dst"] in by_id
    ]


def cmd_work_add(args) -> int:
    with Store(args.db) as store:
        work = fetch_node(store, args.work, kind="work")
        if work["props"].get("status") != "open":
            raise ValueError(
                f"work '{args.work}' is {work['props'].get('status')}, not open"
            )
        props = dict(args.props or {})
        props["work"] = args.work
        nid = store.add_node(args.kind, args.label, id_prefix="wn_", props=props)
        store.add_relation(args.work, nid, "contains")
        views = write_views(store)
    print_json({"id": nid, "kind": args.kind, "work": args.work, **views})
    return 0


def cmd_work_check(args) -> int:
    with Store(args.db) as store:
        fetch_node(store, args.check, kind="check")
        store.update_node(args.check, props_patch={"outcome": args.outcome})
        views = write_views(store)
    print_json({"id": args.check, "outcome": args.outcome, **views})
    return 0


def cmd_work_fold(args) -> int:
    with Store(args.db) as store:
        work = fetch_node(store, args.work, kind="work")
        props = work["props"]
        if props.get("status") != "open":
            raise ValueError(
                f"work '{args.work}' is {props.get('status')}, not open"
            )
        folded_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        if args.abandoned:
            store.update_node(
                args.work,
                props_patch={"status": "abandoned", "folded_at": folded_at},
            )
            views = write_views(store)
            print_json({"id": args.work, "status": "abandoned", **views})
            return 0

        members = work_members(store, args.work)
        checks = [m for m in members if m["kind"] == "check"]
        results = [m for m in members if m["kind"] == "result"]
        if props.get("check") == "machine":
            if not checks:
                raise ValueError(
                    "no checks recorded: an unchecked fold is a hope, not a result"
                )
            unpassed = [c["id"] for c in checks if c["props"].get("outcome") != "pass"]
            if unpassed:
                raise ValueError(f"checks not passing: {', '.join(unpassed)}")
        elif not args.operator_confirms:
            raise ValueError(
                "this folding condition spends operator judgment; "
                "re-run with --operator-confirms to record it"
            )
        if not results:
            raise ValueError(
                "no result node: fold needs a result to become material, "
                "or fold with --abandoned"
            )

        lines = [
            f"# {work['label']}",
            "",
            f"folded: {folded_at}",
            f"fold when: {props.get('fold_when')}",
            "",
            "## results",
        ]
        lines.extend(f"- {r['label']}" for r in results)
        if checks:
            lines.extend(["", "## checks"])
            lines.extend(
                f"- {c['props'].get('outcome', 'pending')}: {c['label']}"
                for c in checks
            )
        history = [m for m in members if m["kind"] in ("step", "candidate")]
        if history:
            lines.extend(["", "## history"])
            lines.extend(f"- {m['kind']}: {m['label']}" for m in history)
        material_id = store.add_material(
            props["on"],
            "result",
            label=work["label"],
            lang="markdown",
            body="\n".join(lines) + "\n",
        )
        patch: dict = {"status": "folded", "folded_at": folded_at}
        if props.get("check") == "operator":
            patch["operator_confirmed"] = True
        store.update_node(args.work, props_patch=patch)
        views = write_views(store)
    print_json(
        {
            "id": args.work,
            "status": "folded",
            "on": props["on"],
            "material": material_id,
            **views,
        }
    )
    return 0


def clip(text: str, width: int) -> str:
    return text if len(text) <= width else text[: width - 1] + "…"


def cmd_status(args) -> int:
    with Store(args.db, read_only=True) as store:
        graph = store.graph()
    nodes = graph["nodes"]
    pending = [
        n
        for n in nodes
        if n["kind"] == "statement" and n["props"].get("owner") == "machine"
    ]
    pending.sort(key=lambda n: (n["props"].get("segment", ""), n["props"].get("ord", 0)))
    works = [n for n in nodes if n["kind"] == "work"]
    open_work = [w for w in works if w["props"].get("status") == "open"]
    folded = [w for w in works if w["props"].get("status") in ("folded", "abandoned")]
    folded.sort(key=lambda w: w["props"].get("folded_at", ""), reverse=True)

    print(f"pending endorsement ({len(pending)}):")
    for n in pending:
        print(f"  {n['id']:<16} {clip(n['label'], 72)}")
    if not pending:
        print("  (none)")
    print()
    print(f"open work ({len(open_work)}):")
    for w in open_work:
        print(f"  {w['id']:<16} {clip(w['label'], 72)}")
        print(f"  {'':<16} on {w['props'].get('on')}  check: {w['props'].get('check')}")
        print(f"  {'':<16} fold when: {clip(w['props'].get('fold_when', ''), 64)}")
    if not open_work:
        print("  (none)")
    print()
    print("recent folds:")
    for w in folded[:5]:
        print(
            f"  {w['id']:<16} {w['props'].get('status')}  "
            f"{clip(w['label'], 64)}"
        )
    if not folded:
        print("  (none)")
    return 0


def cmd_show(args) -> int:
    with Store(args.db, read_only=True) as store:
        graph = store.graph()
    by_id = {node["id"]: node for node in graph["nodes"]}
    node = by_id.get(args.node)
    if node is None:
        raise ValueError(f"node '{args.node}' does not exist")

    def name(node_id: str) -> str:
        other = by_id.get(node_id)
        if other is None:
            return node_id
        return f"{node_id} \"{clip(other['label'], 56)}\""

    head = f"{node['id']}  {node['kind']}"
    owner = node["props"].get("owner")
    if owner:
        head += f"  ({owner}-owned)"
    print(head)
    print(f"  \"{node['label']}\"")
    extras = {k: v for k, v in sorted(node["props"].items()) if k != "owner"}
    if extras:
        print("  " + "  ".join(f"{k}: {v}" for k, v in extras.items()))
    outs = [r for r in graph["relations"] if r["src"] == args.node]
    ins = [r for r in graph["relations"] if r["dst"] == args.node]
    print("  out:")
    contains_out = [r for r in outs if r["type"] == "contains"]
    for relation in (r for r in outs if r["type"] != "contains"):
        print(f"    {relation['type']} -> {name(relation['dst'])}")
    if len(contains_out) > 8:
        print(f"    contains -> {len(contains_out)} nodes")
    else:
        for relation in contains_out:
            print(f"    contains -> {name(relation['dst'])}")
    if not outs:
        print("    (none)")
    print("  in:")
    for relation in ins:
        print(f"    {relation['type']} <- {name(relation['src'])}")
    if not ins:
        print("    (none)")
    material = graph["material"].get(args.node, [])
    print("  material:")
    for item in material:
        detail = item.get("label") or item.get("path") or ""
        lang = f", {item['lang']}" if item.get("lang") else ""
        print(f"    {item['id']} ({item['kind']}{lang}) {detail}")
    if not material:
        print("    (none)")
    return 0


def cmd_serve(args) -> int:
    serve(args.db, host=args.host, port=args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
