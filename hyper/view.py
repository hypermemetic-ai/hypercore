"""The operator view — the operator's render of the self-model.

A recursive tree that sets, at every altitude, the **vision** (authored, from
`intent.md`) beside the **as-built** (derived from the living spec) and the **gap**
between them. Everything but the vision is derived here and now from the two
sources, never hand-tended: read `intent.md` and `spec/` fresh and the view is
current by construction.

The vision is whole, not stored per capability; a capability's vision is a live
slice of `intent.md` — the statements that name it. The gap render is deliberately
coarse at this slice: per capability it surfaces the debt the spec marks on itself;
at the root it gathers that debt and names what the architecture review (a later
slice) will deepen. Being honest about its own shallowness is the debt-marking the
view is meant to do.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from . import graph, spec

DEBT = ("NOTE:", "unbuilt", "shallow")

# How the whole vision is sliced per capability — the terms each one speaks in.
TERMS = {
    "interface": ("interface", "window", "screen", "keyboard"),
    "graph": ("graph", "node", "durable", "version-controlled"),
    "queue": ("queue", "card", "decision", "approve", "endorse"),
    "conversation": ("thread", "conversationalist", "conversation", "speak"),
    "self-model": ("model of the system", "state at a glance", "source of truth",
                   "self-model", "as-built"),
}


@dataclass
class ViewNode:
    title: str
    vision: list[str] = field(default_factory=list)
    asbuilt: list[str] = field(default_factory=list)
    gap: list[str] = field(default_factory=list)
    children: list["ViewNode"] = field(default_factory=list)


def operator_view(root: str | None = None) -> ViewNode:
    sp = spec.read_spec(root)
    intent = _read_intent(root)
    caps = [_capability_node(c, intent) for c in sp.capabilities]

    debt = [f"{c.title}: {g}" for c in caps for g in c.gap]
    return ViewNode(
        title="hypercore",
        vision=[f"{title}: {stmts[0]}" for title, stmts in intent if stmts],
        asbuilt=[f"{c.name} — {len(c.requirements)} requirements"
                 for c in sp.capabilities],
        gap=debt + ["the full gap is the architecture review's to draw — unbuilt"],
        children=caps,
    )


def resolve(node: ViewNode, path: list[int]) -> ViewNode:
    """Follow a drill-down path from a node, stopping at the deepest reachable."""
    for i in path:
        if 0 <= i < len(node.children):
            node = node.children[i]
        else:
            break
    return node


def _capability_node(cap: spec.Capability, intent) -> ViewNode:
    return ViewNode(
        title=cap.name,
        vision=_vision_for(cap.name, intent)[:6],
        asbuilt=[r.name for r in cap.requirements],
        gap=[r.name for r in cap.requirements if _is_debt(r.block)],
        children=[ViewNode(title=r.name, asbuilt=r.scenarios or ["(no scenario)"])
                  for r in cap.requirements],
    )


def _is_debt(block: str) -> bool:
    return any(mark in block for mark in DEBT)


def _vision_for(cap: str, intent) -> list[str]:
    terms = TERMS.get(cap, (cap,))
    return [stmt for _title, stmts in intent for stmt in stmts
            if any(t in stmt.lower() for t in terms)]


def _read_intent(root: str | None) -> list[tuple[str, list[str]]]:
    """Each `## ` section of intent.md as (title, [statements])."""
    path = os.path.join(root or graph._root(), "intent.md")
    if not os.path.isfile(path):
        return []
    sections: list[tuple[str, list[str]]] = []
    title, buf = None, []
    for line in open(path).read().splitlines():
        if line.startswith("## "):
            if title is not None:
                sections.append((title, _statements(buf)))
            title, buf = line[3:].strip(), []
        elif title is not None:
            buf.append(line)
    if title is not None:
        sections.append((title, _statements(buf)))
    return sections


def _statements(lines: list[str]) -> list[str]:
    text = "\n".join(lines)
    return [" ".join(p.split()) for p in text.split("\n\n") if p.strip()]
