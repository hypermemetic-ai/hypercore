"""The operator view — the operator's render of the self-model.

A recursive tree that sets, at every altitude, the **vision** (authored, from
`intent.md`) beside the **as-built** (derived from the living spec) and the **gap**
between them. Everything but the vision is derived here and now from the two
sources, never hand-tended: read `intent.md` and `spec/` fresh and the view is
current by construction.

The vision is whole, not stored per capability; a capability's vision is a live
slice of `intent.md` — the statements that name it. The upper levels' "what the
system is" and the deepening backlog are the standing output of the architecture
review (`review`, §7.4): the root's structural map of the modules by length against the
length signal is its as-built, and the review's findings are the gap the operator reads. Per
capability the gap still surfaces the debt the spec marks on itself; the review
gathers the system-wide deepening work at the root.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

from . import graph, review, spec

DEBT = ("NOTE:", "unbuilt", "shallow")


@dataclass
class ViewNode:
    title: str
    vision: list[str] = field(default_factory=list)
    asbuilt: list[str] = field(default_factory=list)
    structure: list[str] = field(default_factory=list)   # the review's module map (root only)
    gap: list[str] = field(default_factory=list)
    children: list["ViewNode"] = field(default_factory=list)


def operator_view(root: str | None = None) -> ViewNode:
    sp = spec.read_spec(root)
    intent = _read_intent(root)
    rv = review.review(root)
    caps = [_capability_node(c, intent, root) for c in sp.capabilities]

    cap_debt = [f"{c.title}: {g}" for c in caps for g in c.gap]
    return ViewNode(
        title="hypercore",
        vision=[f"{title}: {stmts[0]}" for title, stmts in intent if stmts],
        asbuilt=[f"{c.name} — {len(c.requirements)} requirements"
                 for c in sp.capabilities],
        structure=review.bars(rv),                       # what the system is, as a picture
        gap=review.backlog(rv) + cap_debt,               # the deepening backlog, then per-cap debt
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


def _capability_node(cap: spec.Capability, intent, root: str | None) -> ViewNode:
    return ViewNode(
        title=cap.name,
        vision=_vision_for(cap.name, intent, root)[:6],
        asbuilt=[r.name for r in cap.requirements],
        gap=[r.name for r in cap.requirements if _is_debt(r.block)],
        children=[ViewNode(title=r.name, asbuilt=r.scenarios or ["(no scenario)"])
                  for r in cap.requirements],
    )


def _is_debt(block: str) -> bool:
    return any(mark in block for mark in DEBT)


def _vision_for(cap: str, intent, root: str | None) -> list[str]:
    """The vision a capability realizes: the `intent.md` statements that speak its terms — where
    the capability *declares* those terms itself, in a `<!-- vision: ... -->` line in its spec
    slice (authored at carve time, the binding landing with the as-built where it belongs). A
    capability that declares none — pure machinery like `folding-conditions` or
    `architecture-review` — correctly shows no vision, distinct from a bug; nothing here is
    hand-mapped, so a newly carved capability gets its vision with no edit to this module."""
    terms = _vision_terms(cap, root)
    if not terms:
        return []
    return [stmt for _title, stmts in intent for stmt in stmts
            if any(t in stmt.lower() for t in terms)]


def _vision_terms(cap: str, root: str | None) -> list[str]:
    """The terms a capability's spec slice declares it realizes — the `<!-- vision: a, b, c -->`
    line in its preamble — lowered and split. The binding lives with the as-built capability, the
    operator view's one writable region, not in a table this module has to hand-tend and drift."""
    path = spec.cap_path(cap, root)
    if not os.path.isfile(path):
        return []
    text = open(path, encoding="utf-8", errors="ignore").read()
    m = re.search(r"<!--\s*vision:\s*(.+?)\s*-->", text)
    return [t.strip().lower() for t in m.group(1).split(",") if t.strip()] if m else []


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
