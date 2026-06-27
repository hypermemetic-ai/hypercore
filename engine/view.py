"""The operator view — the operator's render of the self-model.

A recursive tree that sets, at every altitude, the **vision** (authored, from
`intent.md`) beside the **as-built** (derived from the living spec), the
**readiness** surface, the **gap**, and **complexity debt**. Everything but the
vision is derived here and now from the live sources, never hand-tended: read
`intent.md`, `spec/`, the work tree, and the architecture review fresh and the
view is current by construction.

The vision is whole, not stored per capability; a capability's vision is a live
slice of `intent.md` — the statements that name it. The upper levels' "what the
system is" and the complexity debt are the standing output of the architecture
review (`review`, §7.4): the root's structural map of the modules by length against the
length signal is its as-built, and the review's findings are the complexity debt the
operator reads. The gap is wanted-but-not-built work: open work plus the review's honest
not-yet-built depth judgment, never the built-but-weak debt list.
"""
from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass, field

from . import tree, review, spec, scenario

GAP = ("unbuilt", "not yet built", "not-yet")
COMPLEXITY = ("shallow", "complexity debt")


@dataclass
class ViewNode:
    title: str
    vision: list[str] = field(default_factory=list)
    asbuilt: list[str] = field(default_factory=list)
    readiness: list[str] = field(default_factory=list)
    structure: list[str] = field(default_factory=list)   # the review's module map (root only)
    gap: list[str] = field(default_factory=list)
    complexity_debt: list[str] = field(default_factory=list)
    children: list["ViewNode"] = field(default_factory=list)


def operator_view(root: str | None = None) -> ViewNode:
    sp = spec.read_spec(root)
    intent = _read_intent(root)
    rv = review.review(root)
    status = _live_status(root)
    caps = [_capability_node(c, intent, root, status) for c in sp.capabilities]

    return ViewNode(
        title="hypercore",
        vision=[f"{title}: {stmts[0]}" for title, stmts in intent if stmts],
        asbuilt=[f"{c.name} — {len(c.requirements)} requirements"
                 for c in sp.capabilities],
        readiness=[status] + _readiness(sp.capabilities, root),
        structure=review.bars(rv),                       # what the system is, as a picture
        gap=_gap(root) + review.gap(),
        complexity_debt=review.complexity_debt(rv),
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


def _capability_node(cap: spec.Capability, intent, root: str | None, status: str) -> ViewNode:
    cls = dict(scenario.classification(cap.name, root))
    return ViewNode(
        title=cap.name,
        vision=_vision_for(cap.name, intent, root)[:6],
        asbuilt=[r.name for r in cap.requirements],
        readiness=[status] + _readiness([cap], root),
        gap=[r.name for r in cap.requirements if _is_gap(r.block)],
        complexity_debt=[r.name for r in cap.requirements if _is_complexity_debt(r.block)],
        children=[_requirement_node(cap.name, r, cls.get(r.name, "watched"), status)
                  for r in cap.requirements],
    )


def _requirement_node(cap: str, req: spec.Requirement, status: str, live: str) -> ViewNode:
    return ViewNode(
        title=req.name,
        asbuilt=req.scenarios or ["(no scenario)"],
        readiness=[live, f"{status} — {cap}: {req.name}"],
        gap=[req.name] if _is_gap(req.block) else [],
        complexity_debt=[req.name] if _is_complexity_debt(req.block) else [],
    )


def _readiness(caps: list[spec.Capability], root: str | None) -> list[str]:
    return [f"{kind} — {cap.name}: {req}"
            for cap in caps
            for req, kind in scenario.classification(cap.name, root)]


def _live_status(root: str | None) -> str:
    if _has_watched_trace(root):
        return "live-run-trace — watched evidence present; the first autonomous run left a trace"
    return "never-run-live — autonomy seam built; first autonomous run still unverified"


def _has_watched_trace(root: str | None) -> bool:
    base = root or tree._root()
    tracked = subprocess.run(["git", "ls-files", "work"], cwd=base, capture_output=True, text=True)
    if tracked.returncode == 0:
        return any(line.endswith(".verdict.md") for line in tracked.stdout.splitlines())
    work = os.path.join(base, "work")
    if not os.path.isdir(work):
        return False
    for dirpath, dirs, files in os.walk(work):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        if any(f.endswith(".verdict.md") for f in files):
            return True
    return False


def _gap(root: str | None) -> list[str]:
    open_work = _open_work(root)
    return open_work or ["no wanted-but-not-built gap — no open work"]


def _open_work(root: str | None) -> list[str]:
    base = os.path.join(root or tree._root(), "work")
    if not os.path.isdir(base):
        return []
    out = []
    for dirpath, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        if f"{os.sep}archive{os.sep}" in dirpath + os.sep:
            continue
        if "intent.md" in files and not _done(os.path.join(dirpath, "intent.md")):
            out.append(_intent_subject(os.path.join(dirpath, "intent.md")))
    return out


def _intent_subject(path: str) -> str:
    text = open(path, encoding="utf-8", errors="ignore").read()
    if text.startswith("---\n") and "\n---\n" in text[4:]:
        text = text[text.find("\n---\n", 4) + 5:]
    return " ".join(text.replace(tree.MARKER, "").split())[:120]


def _done(path: str) -> bool:
    return any(line.strip() == f"state: {tree.DONE}" for line in open(path, encoding="utf-8", errors="ignore"))


def _is_gap(block: str) -> bool:
    low = block.lower()
    return any(mark in low for mark in GAP)


def _is_complexity_debt(block: str) -> bool:
    low = block.lower()
    return any(mark in low for mark in COMPLEXITY)


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
    path = os.path.join(root or tree._root(), "intent.md")
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
