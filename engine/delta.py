"""The delta and the fold — how behavior change reaches the living spec.

A behavior-changing graph carries a delta (ADDED / MODIFIED / REMOVED
requirements); a trivial graph carries one with no ops and so says so. Folding a
graph applies its delta to `spec/` and commits, in one act: the spec never merges
unless the graph folds, and the graph never folds unless the delta merges. The
folding condition lives here — a missing delta or one that does not apply cleanly
to the current spec cannot fold — so drift is structurally impossible, not a thing
discipline must prevent.

On disk a delta is `delta.md` in a graph's folder:

    # delta — <subject>

    ## ADDED — <capability>
    ### Requirement: <name>
    <prose>
    #### Scenario: ...

    ## MODIFIED — <capability>
    ### Requirement: <name>
    ...

    ## REMOVED — <capability>
    ### Requirement: <name>

A delta with no `## VERB — capability` sections is trivial and applies nothing. An
ADDED requirement in a capability that does not yet exist *creates* that capability —
how the self-model grows a new top-level unit as the work reveals one (ADR 0001
forecast this; the worker capability is the first). MODIFIED or REMOVED in an absent
capability is still a mismatch and cannot fold.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from . import channels, graph, spec

VERBS = ("ADDED", "MODIFIED", "REMOVED")


class CannotFold(Exception):
    """The folding condition refused the fold; the spec is left untouched."""


@dataclass
class Op:
    verb: str
    capability: str
    requirement: spec.Requirement


@dataclass
class Delta:
    subject: str = ""
    ops: list[Op] = field(default_factory=list)

    @property
    def trivial(self) -> bool:
        return not self.ops


# ── reading ──────────────────────────────────────────────────────────────────

def parse(text: str) -> Delta:
    subject, verb, cap, block = "", None, None, []
    ops: list[Op] = []

    def flush() -> None:
        if verb and cap and block:
            ops.append(Op(verb, cap, spec._req(block)))

    for line in text.splitlines():
        if line.startswith("# delta"):
            subject = line[len("# delta"):].lstrip(" —-").strip()
        elif line.startswith("## "):
            flush()
            block = []
            head = line[3:]
            v, _, c = head.partition("—") if "—" in head else head.partition(" ")
            verb = v.strip().upper() if v.strip().upper() in VERBS else None
            cap = c.strip() or None
        elif line.startswith(spec.REQ):
            flush()
            block = [line]
        elif block:
            block.append(line)
    flush()
    return Delta(subject, ops)


# ── the folding condition ─────────────────────────────────────────────────────

def check(delta: Delta | None, sp: spec.Spec) -> str | None:
    """Why this delta cannot fold, or None when it folds clean. An ADDED requirement that already
    exists **identically** is not a conflict but an *already-applied* op — the fold is idempotent, so a
    retry after a crash that landed the spec change but not the archive completes rather than wedging
    (H1). An ADDED whose requirement exists with *different* content is a genuine conflict and refuses."""
    if delta is None:
        return "missing delta: a graph must carry a delta to fold"
    for op in delta.ops:
        if op.verb not in VERBS:
            return f"unknown verb {op.verb!r}"
        cap = sp.capability(op.capability)
        if cap is None:
            if op.verb != "ADDED":
                return f"{op.verb} in an absent capability: {op.capability!r}"
            continue  # ADDED into an absent capability creates it on fold
        existing = cap.requirement(op.requirement.name)
        if op.verb == "ADDED" and existing is not None and not _same(existing, op.requirement):
            return f"ADDED requirement already exists: {op.requirement.name!r}"
        if op.verb in ("MODIFIED", "REMOVED") and existing is None:
            return f"{op.verb} requirement is absent: {op.requirement.name!r}"
    return None


def _same(a: spec.Requirement, b: spec.Requirement) -> bool:
    """Two requirement blocks are the same applied state — compared on normalized text so a re-applied
    ADDED (the idempotent-retry case) reads as already-present, not a conflict."""
    return a.block.strip() == b.block.strip()


# ── the fold (applies the delta; atomic with the commit, both directions) ─────

@graph.serialized
def fold(delta: Delta | None, root: str | None = None, node=None) -> None:
    """Apply the delta to the living spec, archive the node, and commit — **one act, atomic in both
    directions** (spec.self-model). Raises CannotFold if the folding condition is not met; on refusal
    the spec is untouched.

    The spec change *and* the node's archive land in **one commit** under the one held line, so the
    record never shows the spec merged without the node archived (or the reverse) — the H1 wedge, where
    a crash between two separate acts left the delta in the spec but the node un-archived and the retry
    hit a permanent CannotFold, cannot occur. The whole act is **idempotently retryable**: a crash
    after the on-disk spec write but before the commit leaves an already-applied delta, which `check`
    now reads as already-present (not a conflict), so the retry re-renders identically, moves the node,
    and commits once. Serialized on the one record: concurrent folds land one at a time, never
    interleaving their spec writes, while their builds ran in parallel. A trivial delta with a node
    still archives it (the fold of a no-op-delta graph)."""
    sp = spec.read_spec(root)
    reason = check(delta, sp)
    if reason:
        raise CannotFold(reason)
    assert delta is not None  # check would have refused None

    def land() -> list[str]:
        touched = sorted({op.capability for op in delta.ops})
        for name in touched:
            path = spec.cap_path(name, root)
            base = open(path).read() if os.path.isfile(path) else _seed(name)
            graph.atomic_write(path, _apply(base, [o for o in delta.ops if o.capability == name]))
        # The render step: every fold re-derives the static channels (skills, the agents file) from
        # the spec, so a committed artifact cannot drift from its source (ADR 0009 §3). Idempotent: an
        # unchanged source re-renders identically and re-staging no-ops, so a retry is safe.
        rendered = channels.materialize(root)
        paths = [spec.cap_path(n, root) for n in touched] + rendered
        if node is not None:
            paths += graph.archive_in_place(node)      # the node's DONE write + folder move, same act
        return paths

    touched = ", ".join(sorted({op.capability for op in delta.ops})) or "channels"
    subject = delta.subject or (graph._subject(node.text) if node is not None else "delta")
    # `land` returns the exact paths it wrote (spec files, rendered channels, the node's move
    # endpoints); `transact` stages precisely those in the one held commit — atomic, both directions.
    graph.transact(land, None, f"fold: {subject} → {touched}")


def _seed(name: str) -> str:
    """The base for a capability the fold is creating: only its name. The machine does
    not invent the rich prose of a hand-authored capability — the header states what it
    is and the delta's requirements carry the rest; the architecture review fills it in."""
    return f"# {name}\n"


def _apply(text: str, ops: list[Op]) -> str:
    """Splice one capability file: preamble kept, requirement blocks edited by name."""
    lines = text.splitlines()
    first = next((i for i, ln in enumerate(lines) if ln.startswith(spec.REQ)), len(lines))
    preamble = "\n".join(lines[:first]).rstrip()
    reqs = spec._requirements(text)
    blocks = {r.name: r.block for r in reqs}
    order = [r.name for r in reqs]
    for op in ops:
        n = op.requirement.name
        if op.verb == "REMOVED":
            blocks.pop(n, None)
            order = [x for x in order if x != n]
        else:  # ADDED or MODIFIED
            if n not in blocks:
                order.append(n)
            blocks[n] = op.requirement.block
    body = "\n".join(blocks[n].rstrip() + "\n" for n in order)
    return preamble + "\n\n" + body
