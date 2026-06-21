"""The architecture review — the standing scan that keeps the system deep.

A periodic scan for deepening opportunities (rebuild-spec §7.4), run as a standing
process, not a one-off: read live off the source tree every time, never a stored
report. It has two roles, and this module serves both from one scan:

- **The engine of deepening.** It surfaces god-files-in-the-making before they set —
  a module over the line-count budget, or one nearing it — each as a finding carrying
  its measure and a recommendation strength. This is the deepening backlog.
- **The operator view's "what the system is" upper levels (§4.2).** The same scan
  renders the structural map of as-built reality — every module against the budget,
  debt marked — so the operator reads the shape of the system at a glance, without
  reading code. The review is *not a separate artifact*: its output is the operator
  view's as-built and gap (`view.operator_view`), kept honest between folds.

The budget it scans against is the one `folding-conditions` gates with (`conditions.
BUDGET`) and the same decision-record escape hatch (`conditions.justified`) — one
budget at two scopes: the per-graph gate at the fold, and this standing whole-tree
scan. Length is what a module costs a worker's window, so length is what is measured;
the deeper structural judgments the review is meant to grow — the deletion test, seam
analysis, testable-through-the-interface — are not yet built, and that shallowness is
recorded in this capability's own spec rather than fabricated into the operator's gap.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from . import conditions, graph

# A module within this margin of the budget is a god-file in the making — flagged
# early so deepening pressure is felt before a split is painful. A starting value to
# tune (§11), like the budget itself, not a deep question.
NEAR = int(conditions.BUDGET * 0.8)
BAR = 20                                  # the visual bar's width, the budget full


@dataclass
class Module:
    """One source file the review measured, with its standing against the budget.
    `status`: ok | nearing | over | justified — `over` is unjustified debt."""
    rel: str
    lines: int
    status: str


@dataclass
class Finding:
    """A deepening opportunity for the backlog. `strength` is the recommendation's
    weight — strong (deepen now) or consider (watch it)."""
    subject: str
    lines: int
    kind: str            # over budget | nearing budget
    strength: str        # strong | consider
    note: str


@dataclass
class Review:
    modules: list[Module] = field(default_factory=list)   # the structural map, largest first
    findings: list[Finding] = field(default_factory=list)  # the deepening backlog


def review(root: str | None = None) -> Review:
    """Scan the source tree live and report. Reads every module's length, places it
    against the budget, and gathers the unjustified ones over or nearing it into the
    deepening backlog. A justified over-budget file shows on the map, marked, but is
    not debt — its size is a recorded decision."""
    src = os.path.join(root or graph._root(), "hyper")
    modules = [Module(rel, n, _status(rel, n, root)) for rel, n in _sources(src)]
    modules.sort(key=lambda m: -m.lines)
    return Review(modules, [f for m in modules if (f := _finding(m))])


def bars(rv: Review) -> list[str]:
    """The structural map as a visual: each module a bar against the budget, debt
    marked. A picture of the system's shape that needs no code read to take in."""
    if not rv.modules:
        return ["(no modules found)"]
    w = max(len(m.rel) for m in rv.modules)
    return [f"{m.rel.ljust(w)}  {_bar(m.lines)}  {m.lines}/{conditions.BUDGET}{_mark(m.status)}"
            for m in rv.modules]


def backlog(rv: Review) -> list[str]:
    """The deepening backlog as the operator reads it — the gap. Honest about a clean
    tree rather than inventing work."""
    if not rv.findings:
        return ["no deepening opportunities — every module is within the budget"]
    return [f"{f.subject}: {f.note} ({f.strength})" for f in rv.findings]


# ── internals ────────────────────────────────────────────────────────────────

def _status(rel: str, n: int, root: str | None) -> str:
    if n > conditions.BUDGET:
        return "justified" if conditions.justified(rel, root) else "over"
    return "nearing" if n >= NEAR else "ok"


def _finding(m: Module) -> Finding | None:
    if m.status == "over":
        return Finding(m.rel, m.lines, "over budget", "strong",
                       f"{m.lines} lines, over the {conditions.BUDGET}-line budget — "
                       "deepen it; no decision justifies its size")
    if m.status == "nearing":
        return Finding(m.rel, m.lines, "nearing budget", "consider",
                       f"{m.lines} lines, nearing the {conditions.BUDGET}-line budget — "
                       "a god-file in the making")
    return None


def _bar(n: int) -> str:
    filled = min(BAR, round(n / conditions.BUDGET * BAR))
    return "█" * filled + "░" * (BAR - filled)


def _mark(status: str) -> str:
    return {"over": "  ✗ over budget", "justified": "  (justified)",
            "nearing": "  • nearing", "ok": ""}[status]


def _sources(src: str) -> list[tuple[str, int]]:
    """Every .py under the source tree, as (path-relative-to-src, line count). Recurses
    into subpackages (the per-slice check/), skips bytecode."""
    out: list[tuple[str, int]] = []
    for dirpath, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in files:
            if f.endswith(".py"):
                full = os.path.join(dirpath, f)
                out.append((os.path.relpath(full, src), _count(full)))
    return sorted(out)


def _count(path: str) -> int:
    with open(path, encoding="utf-8", errors="ignore") as f:
        return sum(1 for _ in f)
