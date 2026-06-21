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

from . import graph, spec

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

def load(graph_dir: str) -> Delta | None:
    """The delta a graph carries, or None when it carries none (a missing delta)."""
    path = os.path.join(graph_dir, "delta.md")
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        return parse(f.read())


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
    """Why this delta cannot fold, or None when it folds clean."""
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
        present = cap.requirement(op.requirement.name) is not None
        if op.verb == "ADDED" and present:
            return f"ADDED requirement already exists: {op.requirement.name!r}"
        if op.verb in ("MODIFIED", "REMOVED") and not present:
            return f"{op.verb} requirement is absent: {op.requirement.name!r}"
    return None


# ── the fold (applies the delta; atomic with the commit, both directions) ─────

def fold(delta: Delta | None, root: str | None = None) -> None:
    """Apply the delta to the living spec and commit, or refuse — one act.

    Raises CannotFold if the folding condition is not met; on refusal the spec is
    untouched. A trivial delta folds and applies nothing.
    """
    sp = spec.read_spec(root)
    reason = check(delta, sp)
    if reason:
        raise CannotFold(reason)
    assert delta is not None  # check would have refused None
    touched = sorted({op.capability for op in delta.ops})
    for name in touched:
        path = spec.cap_path(name, root)
        base = open(path).read() if os.path.isfile(path) else _seed(name)
        graph.atomic_write(path, _apply(base,
                                        [o for o in delta.ops if o.capability == name]))
    if touched:
        paths = [spec.cap_path(n, root) for n in touched]
        graph.commit(paths, f"fold: {delta.subject or 'delta'} → {', '.join(touched)}")


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
