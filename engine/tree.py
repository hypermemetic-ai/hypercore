"""The durable tree: execution trees as folders on disk, read live, written atomically, committed.

The tree is hypercore's one source of truth. A tree is a **folder** — intent.md §work L112: "the
unit on disk is the tree, not the single node." Its `intent.md` carries the ask or statement and
its state; material and child trees sit alongside; while a grilling pass runs, the pass lives in
`grilling.md` within the folder (resumable across episodes — `grill.py` owns it). Open trees live
under `work/`; folding **moves** the folder into that work/'s own `archive/`, one level down so the
live work sits at the front of the tree (intent §work) — location is itself state and
cannot disagree with the record.

The queue (cards) and the standing work are **views** computed by scanning the tree (L110),
never lists kept in sync. A "card" is a tree awaiting the operator — never a stored card file
(Design B): a machine-owned decision the operator must settle, or a held ask whose grilling
has surfaced a question. Every mutation writes one `intent.md` atomically and commits it; a fold or a
cut moves or removes the folder. The act lands on disk at once; the commit follows behind.
"""
from __future__ import annotations

import os
import re
import shutil
import time
from dataclasses import dataclass

# The durable-write floor the tree rests on — atomic write, exact-path commit, the write→commit
# transaction, and the single-writer line that lets concurrent workers fold without colliding on the
# record (intent §62). Re-exported so the tree's callers read one façade: `tree.atomic_write`,
# `tree.commit`, `tree.transact`, `tree.serialized`, `tree._root`.
from .record import _DEFAULT_ROOT, _root, atomic_write, commit, serialized, transact

# States. A tree under archive/ is folded whatever its field says — location is authoritative.
AWAITING = "awaiting you"    # a card on the queue: a decision to settle, or a surfaced question
STANDING = "standing"        # ready work: standing, no worker yet
IN_FLIGHT = "in flight"      # a worker is on it: still work, now live
DONE = "done"               # folded: integrated and moved to work/archive/
GRILLING = "grilling"        # an ask held while its grilling pass runs: not work, not a card
MARKER = "[machine]"


@dataclass
class Node:
    id: str            # the folder name (a legible slug, globally unique)
    kind: str          # ask | decide | do | check | statement
    state: str
    owner: str         # operator | machine
    text: str          # the ask or statement, plain prose (the intent.md body, marker stripped)
    machine: bool      # carries the [machine] marker
    created: float
    parent: str = ""   # the enclosing tree's id, derived from folder location ("" if top-level)
    path: str = ""     # the tree's folder on disk

    @property
    def folded(self) -> bool:
        # Location is authoritative: a tree is folded once its folder sits under an archive/.
        return f"{os.sep}archive{os.sep}" in self.path + os.sep

    @property
    def is_card(self) -> bool:
        return self.state == AWAITING and not self.folded

    @property
    def is_standing(self) -> bool:
        return self.state == STANDING and not self.folded

    @property
    def is_live(self) -> bool:
        return self.state == IN_FLIGHT and not self.folded

    @property
    def has_delta(self) -> bool:
        # Build-readiness is a bare fact about the node's **own folder**: it carries `delta.md`, the
        # architect-proposed delta. A trivial (empty) `delta.md` still counts — the proposal was made;
        # only a never-proposed node (no `delta.md` at all) is held. No import into the tree to read it.
        return os.path.isfile(os.path.join(self.path, "delta.md"))


# ── reading: scan work/ (its archive/ nested) recursively for tree folders ──

def read_tree() -> list[Node]:
    out: list[Node] = []
    _scan(os.path.join(_root(), "work"), "", out)
    return sorted(out, key=lambda n: n.created)


def _scan(base: str, parent: str, out: list[Node]) -> None:
    """Scan a work/ directory: each child folder with an intent.md is a tree (recurse into
    its own work/); the lone `archive/` holds the folded siblings (same parent), tucked one
    level down so the live work sits at the front of the tree."""
    if not os.path.isdir(base):
        return
    for name in sorted(os.listdir(base)):
        folder = os.path.join(base, name)
        intent = os.path.join(folder, "intent.md")
        if os.path.isfile(intent):
            node = _read(intent, parent)
            out.append(node)
            _scan(os.path.join(folder, "work"), node.id, out)       # its open children + their archive
        elif name == "archive":
            _scan(folder, parent, out)                              # folded siblings, one level down


def cards(nodes: list[Node] | None = None) -> list[Node]:
    return [n for n in (read_tree() if nodes is None else nodes) if n.is_card]


def standing(nodes: list[Node] | None = None) -> list[Node]:
    """The standing work the operator sees; `ready` narrows it to the ready work."""
    return [n for n in (read_tree() if nodes is None else nodes) if n.is_standing]


def ready(nodes: list[Node] | None = None) -> list[Node]:
    """The ready work (intent §110): standing work with nothing open beneath it — the same
    readiness that gates spawning gates scheduling, read live, so a node blocked on an open child is
    not taken and nothing in the schedule can go stale."""
    pool = read_tree() if nodes is None else nodes
    open_states = (STANDING, IN_FLIGHT, GRILLING, AWAITING)
    blocked = {n.parent for n in pool if n.parent and not n.folded and n.state in open_states}
    return [n for n in pool if n.is_standing and n.id not in blocked and n.has_delta]


def work(nodes: list[Node] | None = None) -> list[Node]:
    """The work view: every unit of work, standing or in flight; folded has left it."""
    pool = read_tree() if nodes is None else nodes
    return [n for n in pool if n.state in (STANDING, IN_FLIGHT) and not n.folded]


def find(node_id: str) -> Node | None:
    return next((n for n in read_tree() if n.id == node_id), None)


def children(parent_id: str, nodes: list[Node] | None = None) -> list[Node]:
    """The child trees nested in a parent's work/ (its archive/ included once folded)."""
    pool = read_tree() if nodes is None else nodes
    return [n for n in pool if n.parent == parent_id]


def proposed_delta(node: Node) -> str | None:
    """The node's architect-proposed delta, read from its own folder's `delta.md`. Three states the
    readiness check and the worker's handed-delta read distinguish: **None** when the file is absent
    (never proposed — the node is held out of the ready work), **""** when it is empty (a trivial
    proposal — still proposed, build-ready), and the delta text when it is a real one. No import into
    the tree to read it; the proposal is a fact about the folder the tree owns."""
    path = os.path.join(node.path, "delta.md")
    if not node.path or not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        return f.read()


# ── mutations (each lands one intent.md and commits; a fold/cut moves the folder) ──

def file_intent(ask: str, delta: str = "") -> Node:
    """Record the operator's captured intent as standing work — a new top-level tree, landing its
    `intent.md` and its architect-proposed `delta.md` in **one** act so the node and its proposal never
    disagree (`tree.propose` is the writer for a proposal landed later). A trivial proposal is an empty
    `delta`; the node is build-ready either way."""
    return _create(ask, "ask", STANDING, "operator", machine=False, delta=delta,
                   message=f"file intent: {_subject(ask)}")


def propose(node: Node, text: str) -> None:
    """The one writer of a node's proposed delta: land `delta.md` in the node's folder as an atomic
    write committed under the held line, staging exactly the node's own folder (the `_persist` transact
    pattern). After it the node carries a proposed delta and reads as build-ready; the architect's
    resolved or below-floor propose stage reaches the worker through this one seam."""
    transact(lambda: atomic_write(os.path.join(node.path, "delta.md"), text),
             [node.path], f"propose: {_subject(node.text)}")


def raise_card(statement: str, kind: str = "decide", parent: str = "") -> Node:
    """Put a machine-owned statement or decision on the queue — a tree awaiting the operator,
    nested in `parent`'s work/ when one is given (the decision lives where it arose), else top-level."""
    return _create(statement, kind, AWAITING, "machine", machine=True, parent=parent,
                   message=f"raise {kind}: {_subject(statement)}")


def hold(ask: str) -> Node:
    """Hold the operator's ask while its grilling pass runs — the tree exists, not yet work."""
    return _create(ask, "ask", GRILLING, "operator", machine=False,
                   message=f"hold ask: {_subject(ask)}")


def spawn(node: Node) -> Node:
    """The ratified ask becomes standing work; the grilling pass is over."""
    node.state = STANDING
    _persist(node, f"spawn work: {_subject(node.text)}")
    return node


def approve(node: Node) -> Node:
    """Endorse: the marker drops, the card leaves the queue, and the settled decision folds."""
    node.machine = False
    node.owner = "operator"
    node.state = "endorsed" if node.kind == "statement" else "settled"
    _persist(node, f"approve: {_subject(node.text)}")
    return _fold(node, f"settle: {_subject(node.text)}")


def cut(node: Node) -> None:
    """Remove the words: the tree's folder leaves (recoverable from git). Held as one act and staged
    at exactly the removed folder — `git add -A -- <folder>` stages that subtree's deletions and
    nothing else, so a cut never sweeps a sibling's uncommitted work (C1)."""
    path = node.path
    transact(lambda: shutil.rmtree(path) if os.path.isdir(path) else None,
             [path], f"cut: {_subject(node.text)}")


def dispatch(node: Node) -> Node:
    """A worker takes a standing ask: it goes live (in flight) while the worker runs."""
    node.state = IN_FLIGHT
    _persist(node, f"dispatch: {_subject(node.text)}")
    return node


def archive_in_place(node: Node) -> list[str]:
    """Land the node's DONE state and move its folder into archive/ **without its own commit**, and
    return the move's two path endpoints (source, dest) for the caller to stage (H1). This is the node
    half of the transactional fold: `delta.fold` calls it *inside* its one held act so the spec change
    and the node's archive land in a single commit — atomic, both directions — rather than two separate
    acts a crash could split (the wedge). Idempotent: a node already folded returns its current path and
    moves nothing, so a retry completes cleanly; the DONE intent.md is written before the move so the
    archived folder carries the final state."""
    if node.folded:
        return [node.path]
    node.state = DONE
    atomic_write(os.path.join(node.path, "intent.md"), _render(node))
    return _relocate(node)


def recover(node: Node) -> Node:
    """Return a live node to standing when its worker crossing did not integrate — a refusal, a
    failed coherence judgment, a malformed model reply, or an error mid-build (C2). The node leaves
    IN_FLIGHT so it is not a lie (no live worker is on it) and not silently dropped on a restart; the
    decision card the refusal raised is parented to it, so `ready` excludes it (a node blocked on an
    open child is not taken) until the operator settles the recovery. Idempotent on an already-folded
    node — a node that did integrate is not pulled back out."""
    if node.folded or node.state == DONE:
        return node
    node.state = STANDING
    _persist(node, f"recover: {_subject(node.text)}")
    return node


# ── on-disk form: one folder per tree, its intent.md the legible record ─────

@serialized
def _create(text, kind, state, owner, machine, parent="", message="", delta=None) -> Node:
    """Reserve a slug and land the new tree's intent.md as **one** act on the held line (C3). The
    slug is read off the live tree (`_slug`) and the folder written under the same line, so the
    read-the-taken-set → write-the-folder window is closed: two concurrent creations — two failing
    workers both raising a recovery card, say — can never compute the same slug and overwrite each
    other's folder. Persisting under the same line that read the taken set is the reservation. An
    architect-proposed `delta` lands in the same act when one is given, so a node and its proposal
    are written together and never disagree."""
    n = _new(text, kind, state, owner, machine, parent)
    _persist(n, message, delta)
    return n


def _new(text, kind, state, owner, machine, parent="") -> Node:
    slug = _slug(text)
    base = _child_base(parent) if parent else os.path.join(_root(), "work")
    return Node(slug, kind, state, owner, text.strip(), machine, time.time(),
                parent, os.path.join(base, slug))


def _child_base(parent_id: str) -> str:
    """The work/ of the parent tree — where a child tree is born."""
    p = find(parent_id)
    if p:
        return os.path.join(p.path, "work")
    return os.path.join(_root(), "work")       # orphaned parent: fall back to top-level


def _slug(text: str) -> str:
    words = re.findall(r"[a-z0-9]+", text.lower())
    base = "-".join(words[:5]) or "node"
    taken = {n.id for n in read_tree()}
    slug, i = base, 2
    while slug in taken:
        slug, i = f"{base}-{i}", i + 1
    return slug


def _read(path: str, parent: str) -> Node:
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
    folder = os.path.dirname(path)
    return Node(
        id=os.path.basename(folder),
        kind=meta.get("kind", "ask"),
        state=meta.get("state", STANDING),
        owner=meta.get("owner", "machine"),
        text=text,
        machine=machine,
        created=_ts(meta.get("created", "0")),
        parent=parent,
        path=folder,
    )


def _render(node: Node) -> str:
    """The node's intent.md text — front-matter and body, the marker re-appended for a machine node.
    One place the on-disk form lives, so `_persist` and the archive write never drift apart."""
    body = node.text + (f"\n\n{MARKER}" if node.machine else "")
    return (f"---\nkind: {node.kind}\nstate: {node.state}\n"
            f"owner: {node.owner}\ncreated: {node.created:.0f}\n---\n{body}\n")


def _relocate(node: Node) -> list[str]:
    """Move the node's folder into its work/'s archive/ and return the move's two endpoints
    — the source (now deleted) and the dest (now present). The bare move, no commit: the caller stages
    these exact endpoints, never the shared `.../work` parent (C1). One place the fold's move lives."""
    src = node.path
    dest = os.path.join(os.path.dirname(src), "archive", os.path.basename(src))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.move(src, dest)
    node.path = dest
    return [src, dest]


def _persist(node: Node, message: str, delta: str | None = None) -> None:
    # The write and its commit are one held act (`transact`): the line spans atomic_write → commit, so
    # no sibling's uncommitted change or live temp is visible to this commit's `git add`. The pathspec
    # is exactly this node's own folder — never a shared parent — so the commit stages only its own act.
    # An architect-proposed `delta` (when given) lands beside the intent.md in the same act, so a node
    # is never written build-ready yet deltaless, nor the reverse.
    def write() -> None:
        atomic_write(os.path.join(node.path, "intent.md"), _render(node))
        if delta is not None:
            atomic_write(os.path.join(node.path, "delta.md"), delta)
    transact(write, [node.path], message)


def _fold(node: Node, message: str) -> Node:
    """Move a tree's folder into archive/ as one held, exact-path act (intent §work) — the
    standalone fold (`approve`'s settle). The transactional delta-fold archives the node *inside* its
    own act via `archive_in_place`; this is the fold with no delta beside it."""
    if node.folded:
        return node
    transact(lambda: _relocate(node), None, message)
    return node


def _ts(s: str) -> float:
    """Lenient timestamp read: an epoch float, an ISO date, or 0 — so hand-authored trees
    (which carry a legible `created: YYYY-MM-DD`) and engine-written ones both read."""
    s = s.strip()
    try:
        return float(s)
    except ValueError:
        try:
            return time.mktime(time.strptime(s[:10], "%Y-%m-%d"))
        except ValueError:
            return 0.0


def _subject(text: str) -> str:
    return " ".join(text.split())[:50]
