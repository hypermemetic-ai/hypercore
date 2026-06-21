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

# States read by the views. "awaiting you" -> queue; "standing"/"in flight" -> threads.
AWAITING = "awaiting you"
STANDING = "standing"        # ready work, no worker on it yet — the ready frontier
IN_FLIGHT = "in flight"      # a worker is on it: still work, now live on its thread
DONE = "done"               # folded: the worker's result integrated and left the views
GRILLING = "grilling"        # an ask held while its grilling pass runs: not work, not a card
PENDING = "pending"          # a grilling question waiting its turn, one at a time
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
    parent: str = ""   # the relation: a grilling question/entry points at its ask

    @property
    def is_card(self) -> bool:
        return self.state == AWAITING

    @property
    def is_standing(self) -> bool:
        return self.state == STANDING

    @property
    def is_live(self) -> bool:
        return self.state == IN_FLIGHT


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
    """The ready frontier: standing work no worker has taken yet."""
    return [n for n in (read_graph() if nodes is None else nodes) if n.is_standing]


def work(nodes: list[Node] | None = None) -> list[Node]:
    """The threads view: every unit of work, standing or in flight; DONE has left it."""
    pool = read_graph() if nodes is None else nodes
    return [n for n in pool if n.state in (STANDING, IN_FLIGHT)]


def find(node_id: str) -> Node | None:
    return next((n for n in read_graph() if n.id == node_id), None)


def children(parent_id: str, nodes: list[Node] | None = None) -> list[Node]:
    """The nodes hung off a parent — a grilling pass's questions and view entry."""
    pool = read_graph() if nodes is None else nodes
    return [n for n in pool if n.parent == parent_id]


# ── mutations (each lands one node file and commits it) ──────────────────────

def file_intent(ask: str) -> Node:
    """Record the operator's captured intent as standing work on the graph."""
    n = _new("ask", STANDING, "operator", ask, machine=False)
    _persist(n, f"file intent: {_subject(ask)}")
    return n


def raise_card(statement: str, kind: str = "decide", parent: str = "") -> Node:
    """Put a machine-owned statement or decision on the operator's queue."""
    n = _new(kind, AWAITING, "machine", statement, machine=True, parent=parent)
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
    commit([path], f"cut: {_subject(node.text)}")


# ── grilling: an ask held, its questions surfaced one at a time, then spawned ──

def hold(ask: str) -> Node:
    """Hold the operator's ask while its grilling pass runs — owner's words, not work."""
    n = _new("ask", GRILLING, "operator", ask, machine=False)
    _persist(n, f"hold ask: {_subject(ask)}")
    return n


def question(parent_id: str, text: str, awaiting: bool) -> Node:
    """A machine-owned grilling question on `parent_id`; on the queue or waiting its turn."""
    n = _new("ask", AWAITING if awaiting else PENDING, "machine", text,
             machine=True, parent=parent_id)
    _persist(n, f"grill: {_subject(text)}")
    return n


def resolve(node: Node, answer: str) -> Node:
    """Settle a grilling question with the operator's answer; it leaves the queue."""
    node.text = f"{node.text}\n\nanswered: {answer.strip()}"
    node.machine = False
    node.owner = "operator"
    node.state = "settled"
    _persist(node, f"answer: {_subject(answer)}")
    return node


def surface(node: Node) -> Node:
    """Bring the next pending question onto the queue — one question at a time."""
    node.state = AWAITING
    _persist(node, f"surface: {_subject(node.text)}")
    return node


def spawn(node: Node) -> Node:
    """The ratified ask becomes standing work; the grilling pass is over."""
    node.state = STANDING
    _persist(node, f"spawn work: {_subject(node.text)}")
    return node


# ── delegation: a worker takes a node, runs, and its result integrates ────────

def delegate(node: Node) -> Node:
    """A worker takes a standing ask: it goes live (in flight) while the worker runs.
    The live state is what the threads view shows a session on; nothing else changes."""
    node.state = IN_FLIGHT
    _persist(node, f"delegate: {_subject(node.text)}")
    return node


def integrated(node: Node) -> Node:
    """The worker's result folded in: the work is done and leaves the threads view. The
    delta reached the spec in the same fold; this only records that the work completed."""
    node.state = DONE
    _persist(node, f"integrate: {_subject(node.text)}")
    return node


# ── durable write (the act lands atomically; the commit follows behind) ──────
# Shared by every durable write — the graph and the living spec both land here,
# so the "atomic replace, then commit" mechanism lives in exactly one place.

def atomic_write(path: str, text: str) -> None:
    d = os.path.dirname(path)
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d)
    with os.fdopen(fd, "w") as f:
        f.write(text)
    os.replace(tmp, path)                      # atomic; the act lands here


def commit(paths: list[str], message: str) -> None:
    try:
        subprocess.run(["git", "add", *paths], cwd=_root(), check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "commit", "-m", message], cwd=_root(), check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass  # already on disk; a failed commit does not lose the act


# ── on-disk form (legible markdown, one file per node) ───────────────────────

def _new(kind, state, owner, text, machine, parent="") -> Node:
    return Node(uuid.uuid4().hex[:6], kind, state, owner, text.strip(),
                machine, time.time(), parent)


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
        parent=meta.get("parent", ""),
    )


def _persist(node: Node, message: str) -> None:
    body = node.text + (f"\n\n{MARKER}" if node.machine else "")
    rel = f"parent: {node.parent}\n" if node.parent else ""
    raw = (f"---\nkind: {node.kind}\nstate: {node.state}\n"
           f"owner: {node.owner}\ncreated: {node.created:.0f}\n{rel}---\n{body}\n")
    atomic_write(_path(node.id), raw)         # the act lands at once
    commit([_path(node.id)], message)         # durability follows behind


def _subject(text: str) -> str:
    return " ".join(text.split())[:50]
