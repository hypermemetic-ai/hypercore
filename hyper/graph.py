"""The durable graph: nodes on disk, read live, written atomically and committed.

The graph is hypercore's one source of truth. The queue (cards) and the
standing work (threads) are both *views* computed by reading the nodes — never
lists kept in sync, so nothing can go stale. Every mutation writes one node
file atomically and commits it; the act lands on disk at once and the commit
follows behind.

A node carries one operation (intent.md's four: ask, decide, do, check) plus a
statement's endorsement state. A node "awaiting you" is a card on the queue; a
"standing" node is work on a thread.
"""
from __future__ import annotations

import os
import subprocess
import tempfile
import time
import uuid
from dataclasses import dataclass

_HERE = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_ROOT = os.path.dirname(_HERE)

# States read by the views. "awaiting you" -> queue; "standing" -> threads.
AWAITING = "awaiting you"
STANDING = "standing"
MARKER = "[machine]"


def _root() -> str:
    return os.environ.get("HYPER_ROOT", _DEFAULT_ROOT)


def _nodes_dir() -> str:
    return os.path.join(_root(), "work", "nodes")


@dataclass
class Node:
    id: str
    kind: str          # ask | decide | do | check | statement
    state: str
    owner: str         # operator | machine
    text: str          # the ask or statement, plain prose
    machine: bool      # carries the [machine] marker
    created: float

    @property
    def is_card(self) -> bool:
        return self.state == AWAITING

    @property
    def is_standing(self) -> bool:
        return self.state == STANDING


# ── reading ────────────────────────────────────────────────────────────────

def read_graph() -> list[Node]:
    d = _nodes_dir()
    if not os.path.isdir(d):
        return []
    out = []
    for name in os.listdir(d):
        if name.endswith(".md"):
            out.append(_read(os.path.join(d, name)))
    return sorted(out, key=lambda n: n.created)


def cards(nodes: list[Node] | None = None) -> list[Node]:
    return [n for n in (read_graph() if nodes is None else nodes) if n.is_card]


def standing(nodes: list[Node] | None = None) -> list[Node]:
    return [n for n in (read_graph() if nodes is None else nodes) if n.is_standing]


def find(node_id: str) -> Node | None:
    return next((n for n in read_graph() if n.id == node_id), None)


# ── mutations (each lands one node file and commits it) ──────────────────────

def file_intent(ask: str) -> Node:
    """Record the operator's captured intent as standing work on the graph."""
    n = _new("ask", STANDING, "operator", ask, machine=False)
    _persist(n, f"file intent: {_subject(ask)}")
    return n


def raise_card(statement: str, kind: str = "decide") -> Node:
    """Put a machine-owned statement or decision on the operator's queue."""
    n = _new(kind, AWAITING, "machine", statement, machine=True)
    _persist(n, f"raise {kind}: {_subject(statement)}")
    return n


def approve(node: Node) -> Node:
    """Endorse: the marker drops and the card leaves the queue."""
    node.machine = False
    node.owner = "operator"
    node.state = "endorsed" if node.kind == "statement" else "settled"
    _persist(node, f"approve: {_subject(node.text)}")
    return node


def cut(node: Node) -> None:
    """Remove the words: the node file leaves (recoverable from git)."""
    path = _path(node.id)
    if os.path.exists(path):
        os.remove(path)
    _commit([path], f"cut: {_subject(node.text)}")


# ── on-disk form (legible markdown, one file per node) ───────────────────────

def _new(kind, state, owner, text, machine) -> Node:
    return Node(uuid.uuid4().hex[:6], kind, state, owner, text.strip(),
                machine, time.time())


def _path(node_id: str) -> str:
    return os.path.join(_nodes_dir(), f"{node_id}.md")


def _read(path: str) -> Node:
    with open(path) as f:
        raw = f.read()
    meta, body = {}, raw
    if raw.startswith("---\n"):
        end = raw.find("\n---\n", 4)
        if end != -1:
            for line in raw[4:end].splitlines():
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip()
            body = raw[end + 5:]
    text = body.strip()
    machine = text.endswith(MARKER)
    if machine:
        text = text[: -len(MARKER)].strip()
    return Node(
        id=os.path.splitext(os.path.basename(path))[0],
        kind=meta.get("kind", "ask"),
        state=meta.get("state", STANDING),
        owner=meta.get("owner", "machine"),
        text=text,
        machine=machine,
        created=float(meta.get("created", "0") or 0),
    )


def _persist(node: Node, message: str) -> None:
    d = _nodes_dir()
    os.makedirs(d, exist_ok=True)
    body = node.text + (f"\n\n{MARKER}" if node.machine else "")
    raw = (f"---\nkind: {node.kind}\nstate: {node.state}\n"
           f"owner: {node.owner}\ncreated: {node.created:.0f}\n---\n{body}\n")
    fd, tmp = tempfile.mkstemp(dir=d)
    with os.fdopen(fd, "w") as f:
        f.write(raw)
    os.replace(tmp, _path(node.id))           # atomic; the act lands here
    _commit([_path(node.id)], message)        # durability follows behind


def _commit(paths: list[str], message: str) -> None:
    try:
        subprocess.run(["git", "add", *paths], cwd=_root(), check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "commit", "-m", message], cwd=_root(), check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass  # already on disk; a failed commit does not lose the act


def _subject(text: str) -> str:
    return " ".join(text.split())[:50]
