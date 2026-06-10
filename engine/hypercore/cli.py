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

# The segments whose intent is a list of statements: ingested from these files
# into the statement store, then rendered back out. Statements are not nodes
# (structure: s_d4bd1b45); they live beside the graph, not in it.
SEGMENTS = ("foundations", "structure", "statements", "endorsement", "work")

# A machine-owned statement carries this marker at its end in the derived view
# (see endorsement.md). The marker is envelope, not prose: ingest strips it into
# the node's owner prop, render writes it back. The operator endorses with the
# endorse verb; render then drops the marker.
OWNER_MARKER = " [machine]"

# The durable, git-tracked forms: the graph and the statement store, each its
# own snapshot. The DuckDB file is ignored by git, so every mutating verb
# rewrites both snapshots alongside the markdown views; `load` rebuilds a local
# database from them without loss.
GRAPH_SNAPSHOT = INTENT_ROOT / "engine" / "graph.json"
STATEMENTS_SNAPSHOT = INTENT_ROOT / "engine" / "statements.json"

# The operation alphabet (work: s_3729cb59). A member of an execution graph is
# one operation of these five kinds; its products are material on the operation
# node, never a node kind of their own. The alphabet does not grow — named
# clusters of operations are the compounds that do (s_e4f503c9).
# derive was cut 2026-06-10 (s_88dc042e) until its purpose is understood;
# it never appeared in any graph, so nothing renders it.
OPERATIONS = ("frame", "gather", "generate", "test", "commit")

# Relations carry the combinators. `--on` wires an operation to what it acts
# on with its kind's own combinator; every other kind consumes its target
# through the causal link, depends-on. `contains` is work membership — which
# folder an operation belongs to — not a combinator.
COMBINATORS = {
    "frame": "reframes",
    "test": "tests",
    "commit": "commits",
}


def role_defaults(kind: str) -> dict:
    """Who proposes, executes, judges, and decides — a property on each
    operation, not an operation of its own (s_81c38173). The machine drives
    the verbs, so it proposes and executes by default; only a test carries a
    judge, and a commit's decide belongs to the operator, non-delegably."""
    roles = {"propose": "machine", "execute": "machine"}
    if kind == "test":
        roles["judge"] = "machine"
    if kind == "commit":
        roles["decide"] = "operator"
    return roles


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
    amend.add_argument(
        "--grounds",
        help="Why, in the decider's words — recorded with the decision.",
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
    strike.add_argument(
        "--grounds",
        help="Why, in the decider's words — recorded with the decision.",
    )
    strike.set_defaults(func=cmd_strike)

    endorse = subparsers.add_parser(
        "endorse",
        help="Take machine-owned statements on as the operator.",
    )
    endorse.add_argument("ids", nargs="+", help="Statement ids.")
    endorse.add_argument(
        "--grounds",
        help="The operator's why, recorded with the decision.",
    )
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
        help="Add one operation to open work.",
    )
    work_add.add_argument("work", help="Work id.")
    work_add.add_argument(
        "--kind",
        required=True,
        choices=OPERATIONS,
        help="Which of the five operations this is.",
    )
    work_add.add_argument("--label", required=True, help="What it is.")
    work_add.add_argument(
        "--on",
        dest="target",
        help="The operation this one acts on: a test tests it, a commit "
        "commits it (must be a generate), a frame reframes it (must be a "
        "frame); any other kind depends on it.",
    )
    work_add.add_argument(
        "--needs",
        action="append",
        default=[],
        help="Operation whose product this one consumes: a depends-on "
        "causal link. Use more than once for more.",
    )
    work_add.add_argument(
        "--under",
        help="Parent operation this one decomposes from (decomposes-into).",
    )
    work_add.add_argument(
        "--roles",
        type=json_object,
        help="Who proposes/executes/judges/decides, merged over the "
        "kind's defaults. A commit's decide is the operator's, always.",
    )
    work_add.add_argument("--props", type=json_object, help="JSON object.")
    work_add.set_defaults(func=cmd_work_add)

    work_check = subparsers.add_parser(
        "work-check",
        help="Record a test operation's verdict.",
    )
    work_check.add_argument("test", help="Test operation id.")
    work_check.add_argument(
        "--verdict", required=True, choices=("pass", "fail"), help="The verdict."
    )
    work_check.add_argument("--grounds", help="What the verdict rests on.")
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

    Builds hypercore's own node and fills the statement store, one statement
    per paragraph. Once statements exist, intent is authored with the statement
    verbs and ingest refuses to run: re-reading the derived view would erase
    ids and links. A local database is rebuilt from the snapshots instead.
    """
    loaded: dict[str, list[str]] = {}
    machine_owned: list[str] = []
    with Store(args.db) as store:
        existing = store.con.execute(
            "SELECT count(*) FROM statements"
        ).fetchone()[0]
        if existing:
            print(
                f"{existing} statements already exist. Intent is authored with "
                "the statement verbs now (add-statement, amend, strike, "
                "endorse); ingest only bootstraps an empty database. To "
                "rebuild a local database from the snapshots, run: "
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
            _, statements = parse_intent(INTENT_ROOT / f"{seg}.md")
            ids: list[str] = []
            for ordinal, (text, owner) in enumerate(statements, start=1):
                sid = f"{seg}-{ordinal}"
                store.add_statement(text, seg, ordinal, owner=owner, id=sid)
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


def render_files(statements: list[dict]) -> list[str]:
    """Write the intent files from the statement store: the derived,
    human-legible view.

    Source of truth is the store. A wrong rendering is fixed here, never by
    editing the file on disk.
    """
    by_segment = defaultdict(list)
    for statement in statements:
        by_segment[statement["segment"]].append(statement)

    written: list[str] = []
    for seg in SEGMENTS:
        segment_statements = sorted(by_segment[seg], key=lambda s: s["ord"])
        lines = [f"# {seg}", ""]
        for statement in segment_statements:
            text = statement["text"]
            if statement["owner"] == "machine":
                text += OWNER_MARKER
            lines.append(text)
            lines.append("")
        text = "\n".join(lines).rstrip() + "\n"
        (INTENT_ROOT / f"{seg}.md").write_text(text, encoding="utf-8")
        written.append(f"{seg}.md")
    return written


# A folder holds one execution graph; the unit on disk is the graph, not the
# single node (work.md). The whole tree is derived: rebuilt on every verb,
# never hand-edited, and the fold is reflected here as it is in the database.
WORK_ROOT = INTENT_ROOT / "work"

MATERIAL_EXT = {"markdown": "md", "python": "py", "json": "json"}


def render_work_folders(store: Store) -> list[str]:
    """Write the execution graphs as browsable folders: one per work, an
    index over them, and every inline material body as its own file."""
    import shutil

    graph = store.graph()
    statements_by_id = {s["id"]: s for s in store.statements()}
    works = [n for n in graph["nodes"] if n["kind"] == "work"]
    works.sort(
        key=lambda w: (
            w["props"].get("status") != "open",
            w["props"].get("folded_at", ""),
            w["id"],
        )
    )

    if WORK_ROOT.exists():
        shutil.rmtree(WORK_ROOT)
    WORK_ROOT.mkdir()

    def statement_line(sid: str) -> str:
        statement = statements_by_id.get(sid)
        if statement is None:
            return f"`{sid}`"
        return f"`{sid}` — \"{clip(statement['text'], 90)}\""

    index = ["# work — the execution graphs", ""]
    written = ["work/README.md"]
    for work in works:
        props = work["props"]
        status = props.get("status", "open")
        index.append(
            f"- [`{work['id']}`]({work['id']}/README.md) **{status}** — "
            f"{work['label']}"
        )
        written.append(f"work/{work['id']}/README.md")
        folder = WORK_ROOT / work["id"]
        folder.mkdir()

        members = work_members(graph, work["id"])
        by_id = {node["id"]: node for node in graph["nodes"]}
        lines = [
            f"# {work['label']}",
            "",
            f"`{work['id']}` · **{status}** · check: {props.get('check')}",
            "",
            f"on: {statement_line(props.get('on', ''))}",
            f"fold when: {props.get('fold_when')}",
        ]
        if props.get("folded_at"):
            lines.append(f"folded: {props['folded_at']}")
        produces = props.get("produces") or []
        if produces:
            lines.append("produces:")
            lines.extend(f"- {statement_line(sid)}" for sid in produces)

        # Operations in alphabet order, the graph each work is made of.
        kind_order = {kind: i for i, kind in enumerate(OPERATIONS)}
        members.sort(
            key=lambda m: (kind_order.get(m["kind"], 99), m["kind"], m["id"])
        )
        current_kind = None
        for member in members:
            if member["kind"] != current_kind:
                current_kind = member["kind"]
                lines.extend(["", f"## {current_kind}", ""])
            mprops = member["props"]
            roles = mprops.get("roles") or {}
            role_text = ", ".join(f"{k}: {v}" for k, v in sorted(roles.items()))
            line = f"- `{member['id']}` {member['label']}"
            if role_text:
                line += f"  ({role_text})"
            lines.append(line)
            if member["kind"] == "test":
                verdict = mprops.get("verdict", "open")
                grounds = mprops.get("grounds")
                lines.append(
                    f"  - verdict: **{verdict}**"
                    + (f" — {grounds}" if grounds else "")
                )
            for relation in graph["relations"]:
                if relation["src"] == member["id"] and relation["type"] != "contains":
                    other = by_id.get(relation["dst"])
                    label = f" \"{clip(other['label'], 60)}\"" if other else ""
                    lines.append(
                        f"  - {relation['type']} -> `{relation['dst']}`{label}"
                    )

        # Material: the products. Inline bodies become files in the folder.
        material_lines = []
        for node in [work] + members:
            for item in graph["material"].get(node["id"], []):
                where = node["id"] if node is not work else "the work"
                detail = item.get("label") or item.get("path") or item["id"]
                if item.get("has_body"):
                    ext = MATERIAL_EXT.get(item.get("lang"), "txt")
                    filename = f"{item['id']}.{ext}"
                    (folder / filename).write_text(
                        store.material_body(item["id"]) or "", encoding="utf-8"
                    )
                    written.append(f"work/{work['id']}/{filename}")
                    material_lines.append(
                        f"- [{detail}]({filename}) ({item['kind']}) — on {where}"
                    )
                else:
                    target = item.get("path")
                    link = f" → `{target}`" if target else ""
                    material_lines.append(
                        f"- {detail} ({item['kind']}){link} — on {where}"
                    )
        if material_lines:
            lines.extend(["", "## material", ""])
            lines.extend(material_lines)

        (folder / "README.md").write_text(
            "\n".join(lines).rstrip() + "\n", encoding="utf-8"
        )

    (WORK_ROOT / "README.md").write_text(
        "\n".join(index).rstrip() + "\n", encoding="utf-8"
    )
    return written


def write_views(store: Store) -> dict:
    """Rewrite everything derived: intent files, work folders, and both
    snapshots.

    Every mutating verb ends here, so the views never lag and git always
    tracks the durable forms of the graph and the statement store.
    """
    rendered = render_files(store.statements())
    rendered.extend(render_work_folders(store))
    GRAPH_SNAPSHOT.write_text(
        json.dumps(store.dump(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    STATEMENTS_SNAPSHOT.write_text(
        json.dumps(store.dump_statements(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "rendered": rendered,
        "snapshot": ["engine/graph.json", "engine/statements.json"],
    }


def cmd_render(args) -> int:
    with Store(args.db, read_only=True) as store:
        views = write_views(store)
    print_json({"database": args.db, **views})
    return 0


def cmd_load(args) -> int:
    if not GRAPH_SNAPSHOT.exists():
        raise ValueError(f"no snapshot at {GRAPH_SNAPSHOT}")
    if not STATEMENTS_SNAPSHOT.exists():
        raise ValueError(
            f"no statement store at {STATEMENTS_SNAPSHOT}; statements left "
            "the graph (s_d4bd1b45) and load needs both snapshots"
        )
    data = json.loads(GRAPH_SNAPSHOT.read_text(encoding="utf-8"))
    statement_data = json.loads(STATEMENTS_SNAPSHOT.read_text(encoding="utf-8"))
    with Store(args.db) as store:
        existing = store.con.execute("SELECT count(*) FROM nodes").fetchone()[0]
        existing += store.con.execute(
            "SELECT count(*) FROM statements"
        ).fetchone()[0]
        if existing and not args.replace:
            raise ValueError(
                f"database has {existing} nodes and statements; re-run with "
                "--replace to rebuild it from the snapshots"
            )
        store.load(data)
        store.load_statements(statement_data)
    print_json(
        {
            "database": args.db,
            "loaded": {
                **{table: len(rows) for table, rows in data.items()},
                "statements": len(statement_data.get("statements", [])),
            },
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


def fetch_statement(store: Store, id: str) -> dict:
    statement = store.statement(id)
    if statement is None:
        raise ValueError(f"statement '{id}' does not exist")
    return statement


def renumber_segment(store: Store, seg: str) -> None:
    """Make a segment's ords 1..n again. Ids never change; only the ordering
    is the machine's bookkeeping to keep tidy."""
    for ordinal, statement in enumerate(store.statements(segment=seg), start=1):
        if statement["ord"] != ordinal:
            store.update_statement(statement["id"], ord=ordinal)


def cmd_add_statement(args) -> int:
    with Store(args.db) as store:
        statements = store.statements(segment=args.segment)
        if args.after:
            ords = {s["id"]: s["ord"] for s in statements}
            if args.after not in ords:
                raise ValueError(
                    f"'{args.after}' is not a statement in segment '{args.segment}'"
                )
            ord_value = ords[args.after] + 1
            for statement in statements:
                if statement["ord"] >= ord_value:
                    store.update_statement(
                        statement["id"], ord=statement["ord"] + 1
                    )
        elif statements:
            ord_value = statements[-1]["ord"] + 1
        else:
            ord_value = 1
        sid = store.add_statement(
            args.text, args.segment, ord_value, owner=args.owner
        )
        renumber_segment(store, args.segment)
        views = write_views(store)
    print_json({"id": sid, "segment": args.segment, "owner": args.owner, **views})
    return 0


def cmd_amend(args) -> int:
    with Store(args.db) as store:
        statement = fetch_statement(store, args.id)
        previous_owner = statement["owner"]
        store.update_statement(args.id, text=args.text, owner=args.by)
        store.record_decision(
            "amend",
            args.id,
            text=statement["text"],
            grounds=args.grounds,
            actor=args.by,
        )
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
        statement = fetch_statement(store, args.id)
        if statement["owner"] == "operator" and args.by != "operator":
            raise ValueError(
                "the machine never strikes operator-owned intent; "
                "re-run with --by operator if this is the operator's decision"
            )
        # The blast radius, computed before the strike lands: the machine
        # surfaces this to the operator as part of the decision, not after
        # it (s_070617cf).
        consequences = store.statement_consequences(args.id)
        removed = store.delete_statement(args.id)
        renumber_segment(store, statement["segment"])
        store.record_decision(
            "strike",
            args.id,
            text=statement["text"],
            grounds=args.grounds,
            actor=args.by,
        )
        views = write_views(store)
    print_json(
        {
            "struck": args.id,
            "text": statement["text"],
            "links_lost": removed["links"],
            "linked_by_lost": removed["linked_by"],
            "breaks": {
                "open_work_loses_its_anchor": [
                    f"{n['id']} {n['label']}"
                    for n in consequences["anchors_open"]
                ],
                "folded_record_points_at_nothing": [
                    f"{n['id']} {n['label']}"
                    for n in (
                        consequences["anchors_folded"]
                        + consequences["produced"]
                    )
                ],
                "statements_lose_their_link_target": [
                    s["id"] for s in consequences["linked_by"]
                ],
            },
            **views,
        }
    )
    return 0


def cmd_endorse(args) -> int:
    endorsed: list[str] = []
    already: list[str] = []
    with Store(args.db) as store:
        for sid in args.ids:
            statement = fetch_statement(store, sid)
            if statement["owner"] == "operator":
                already.append(sid)
            else:
                store.update_statement(sid, owner="operator")
                # The verb records the operator's word from conversation;
                # the decision is theirs either way (endorsement.md).
                store.record_decision(
                    "endorse",
                    sid,
                    text=statement["text"],
                    grounds=args.grounds,
                    actor="operator",
                )
                endorsed.append(sid)
        views = write_views(store)
    print_json({"endorsed": endorsed, "already_operator_owned": already, **views})
    return 0


def cmd_work_open(args) -> int:
    with Store(args.db) as store:
        # Work is usually bound by a statement (its `on` is the bound-by
        # reference of s_d4bd1b45), but a node's intent can spawn work too.
        if store.statement(args.on) is None:
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
        # Every work happens inside the standing frame: the root's product is
        # the problem space, every work's precondition. The causal link keeps
        # the root in the graph rather than an island beside it.
        root = root_node(store)
        if root is not None:
            store.add_relation(wid, root["id"], "depends-on")
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


def work_members(graph: dict, work_id: str) -> list[dict]:
    by_id = {node["id"]: node for node in graph["nodes"]}
    return [
        by_id[relation["dst"]]
        for relation in graph["relations"]
        if relation["type"] == "contains"
        and relation["src"] == work_id
        and relation["dst"] in by_id
    ]


def root_node(store: Store) -> dict | None:
    for node in store.graph()["nodes"]:
        if node["props"].get("role") == "root":
            return node
    return None


def cmd_work_add(args) -> int:
    with Store(args.db) as store:
        work = fetch_node(store, args.work, kind="work")
        if work["props"].get("status") != "open":
            raise ValueError(
                f"work '{args.work}' is {work['props'].get('status')}, not open"
            )
        roles = role_defaults(args.kind)
        roles.update(args.roles or {})
        if args.kind == "commit" and roles.get("decide") != "operator":
            raise ValueError(
                "the decision to commit belongs to the operator and cannot "
                "be delegated (s_81c38173)"
            )
        # Resolve the combinators before creating anything, so a refused
        # relation never leaves a half-wired operation behind.
        relations: list[tuple[str, str, str]] = []  # (src or "", type, dst)
        if args.target:
            target = fetch_node(store, args.target)
            combinator = COMBINATORS.get(args.kind, "depends-on")
            if combinator == "commits" and target["kind"] != "generate":
                raise ValueError(
                    "a commit binds the candidate a generate put forward; "
                    f"'{args.target}' is a {target['kind']}, not a generate"
                )
            if combinator == "reframes" and target["kind"] != "frame":
                raise ValueError(
                    "a frame reframes a prior frame; "
                    f"'{args.target}' is a {target['kind']}, not a frame"
                )
            relations.append(("", combinator, args.target))
        for needed in args.needs:
            fetch_node(store, needed)
            relations.append(("", "depends-on", needed))
        if args.under:
            fetch_node(store, args.under)
            relations.append((args.under, "decomposes-into", ""))

        props = dict(args.props or {})
        props["work"] = args.work
        props["roles"] = roles
        nid = store.add_node(args.kind, args.label, id_prefix="wn_", props=props)
        store.add_relation(args.work, nid, "contains")
        wired = []
        for src, type_, dst in relations:
            store.add_relation(src or nid, dst or nid, type_)
            wired.append({"src": src or nid, "type": type_, "dst": dst or nid})
        views = write_views(store)
    print_json(
        {
            "id": nid,
            "kind": args.kind,
            "work": args.work,
            "roles": roles,
            "relations": wired,
            **views,
        }
    )
    return 0


def cmd_work_check(args) -> int:
    with Store(args.db) as store:
        fetch_node(store, args.test, kind="test")
        patch: dict = {"verdict": args.verdict}
        if args.grounds:
            patch["grounds"] = args.grounds
        store.update_node(args.test, props_patch=patch)
        views = write_views(store)
    print_json({"id": args.test, "verdict": args.verdict, **views})
    return 0


def fold_work(
    store: Store,
    work_id: str,
    *,
    operator_confirms: bool = False,
    abandoned: bool = False,
) -> dict:
    """Fold one open work; the gate and the settlement live here so the CLI
    and the viewer's /api/fold spend the same checks."""
    work = fetch_node(store, work_id, kind="work")
    props = work["props"]
    if props.get("status") != "open":
        raise ValueError(
            f"work '{work_id}' is {props.get('status')}, not open"
        )
    folded_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    if abandoned:
        store.update_node(
            work_id,
            props_patch={"status": "abandoned", "folded_at": folded_at},
        )
        return {"id": work_id, "status": "abandoned"}

    graph = store.graph()
    members = work_members(graph, work_id)
    tests = [m for m in members if m["kind"] == "test"]
    commits = [m for m in members if m["kind"] == "commit"]
    if props.get("check") == "machine":
        if not tests:
            raise ValueError(
                "no test operations: an unchecked fold is a hope, not a result"
            )
        unpassed = [t["id"] for t in tests if t["props"].get("verdict") != "pass"]
        if unpassed:
            raise ValueError(f"tests without a pass verdict: {', '.join(unpassed)}")
    elif not operator_confirms:
        raise ValueError(
            "this folding condition spends operator judgment; "
            "re-run with --operator-confirms to record it"
        )
    if not commits:
        raise ValueError(
            "no commit operation: fold needs a settlement to become "
            "material, or fold with --abandoned"
        )

    def with_material(node: dict) -> str:
        ids = [m["id"] for m in graph["material"].get(node["id"], [])]
        return node["label"] + (f"  (material: {', '.join(ids)})" if ids else "")

    lines = [
        f"# {work['label']}",
        "",
        f"folded: {folded_at}",
        f"fold when: {props.get('fold_when')}",
        "",
        "## commits",
    ]
    lines.extend(f"- {with_material(c)}" for c in commits)
    if tests:
        lines.extend(["", "## tests"])
        lines.extend(
            f"- {t['props'].get('verdict', 'open')}: {t['label']}"
            for t in tests
        )
    # Everything else is the history: the frames, gathers, and generates
    # the work moved through (and any pre-alphabet kinds).
    history = [m for m in members if m["kind"] not in ("test", "commit")]
    if history:
        lines.extend(["", "## history"])
        lines.extend(f"- {m['kind']}: {m['label']}" for m in history)
    # The fold's material lives on the work node itself: statements are
    # not nodes and cannot carry material. `show` on the spawning
    # statement finds this work — and its material — by reverse reference.
    material_id = store.add_material(
        work_id,
        "result",
        label=work["label"],
        lang="markdown",
        body="\n".join(lines) + "\n",
    )
    patch: dict = {"status": "folded", "folded_at": folded_at}
    if props.get("check") == "operator":
        patch["operator_confirmed"] = True
    store.update_node(work_id, props_patch=patch)
    return {
        "id": work_id,
        "status": "folded",
        "on": props["on"],
        "material": material_id,
    }


def cmd_work_fold(args) -> int:
    with Store(args.db) as store:
        result = fold_work(
            store,
            args.work,
            operator_confirms=args.operator_confirms,
            abandoned=args.abandoned,
        )
        views = write_views(store)
    print_json({**result, **views})
    return 0


def clip(text: str, width: int) -> str:
    return text if len(text) <= width else text[: width - 1] + "…"


def cmd_status(args) -> int:
    with Store(args.db, read_only=True) as store:
        graph = store.graph()
        statements = store.statements()
    nodes = graph["nodes"]
    segment_order = {seg: index for index, seg in enumerate(SEGMENTS)}
    pending = [s for s in statements if s["owner"] == "machine"]
    pending.sort(key=lambda s: (segment_order.get(s["segment"], 99), s["ord"]))
    works = [n for n in nodes if n["kind"] == "work"]
    open_work = [w for w in works if w["props"].get("status") == "open"]
    folded = [w for w in works if w["props"].get("status") in ("folded", "abandoned")]
    folded.sort(key=lambda w: w["props"].get("folded_at", ""), reverse=True)

    print(f"pending endorsement ({len(pending)}):")
    for s in pending:
        print(f"  {s['id']:<16} {clip(s['text'], 72)}")
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


def show_statement(
    statement: dict, statements: list[dict], references: dict, graph: dict
) -> int:
    """One statement, human-legible: envelope, links, and the reverse index —
    the graph nodes that reference it (s_d4bd1b45)."""
    by_id = {s["id"]: s for s in statements}

    print(f"{statement['id']}  statement  ({statement['owner']}-owned)")
    print(f"  \"{statement['text']}\"")
    print(f"  ord: {statement['ord']}  segment: {statement['segment']}")

    print("  links:")
    shown = False
    for link in statement["links"]:
        other = by_id.get(link.get("to"))
        text = f" \"{clip(other['text'], 56)}\"" if other else ""
        print(f"    {link.get('type')} -> {link.get('to')}{text}")
        shown = True
    for other in statements:
        for link in other["links"]:
            if link.get("to") == statement["id"]:
                print(
                    f"    {link.get('type')} <- {other['id']} "
                    f"\"{clip(other['text'], 56)}\""
                )
                shown = True
    if not shown:
        print("    (none)")

    def node_line(node: dict) -> str:
        line = f"{node['id']} \"{clip(node['label'], 56)}\""
        status = node["props"].get("status")
        if status:
            line += f"  ({node['kind']}, {status})"
        material = graph["material"].get(node["id"], [])
        if material:
            line += "  material: " + ", ".join(m["id"] for m in material)
        return line

    print("  bound:")
    for node in references["bound"]:
        print(f"    {node_line(node)}")
    if not references["bound"]:
        print("    (none)")
    print("  produced by:")
    for node in references["produced"]:
        print(f"    {node_line(node)}")
    if not references["produced"]:
        print("    (none)")
    return 0


def cmd_show(args) -> int:
    with Store(args.db, read_only=True) as store:
        graph = store.graph()
        statement = store.statement(args.node)
        if statement is not None:
            return show_statement(
                statement,
                store.statements(),
                store.statement_references(args.node),
                graph,
            )
    by_id = {node["id"]: node for node in graph["nodes"]}
    node = by_id.get(args.node)
    if node is None:
        raise ValueError(f"'{args.node}' is neither a node nor a statement")

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
