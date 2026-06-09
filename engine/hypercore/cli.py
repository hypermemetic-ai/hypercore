"""Command line tool for hypercore."""

from __future__ import annotations

import argparse
import json
import sys

from .server import serve
from .store import Store


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


def cmd_serve(args) -> int:
    serve(args.db, host=args.host, port=args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
