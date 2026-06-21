"""The architecture review — the standing scan that keeps the system deep.

A periodic scan for deepening opportunities (ADR 0005), run as a standing
process, not a one-off: read live off the source tree every time, never a stored
report. It has two roles, and this module serves both from one scan:

- **The engine of deepening.** It surfaces god-files-in-the-making before they set —
  a module past the length signal, or one nearing it — each as a finding carrying its
  measure and a recommendation strength. This is the deepening backlog.
- **The operator view's "what the system is" upper levels.** The same scan
  renders the structural map of as-built reality — every module by length against the
  signal, debt marked — so the operator reads the shape of the system at a glance,
  without reading code. The review is *not a separate artifact*: its output is the
  operator view's as-built and gap (`view.operator_view`), kept honest between folds.

What it measures is **length** — what a module costs a worker's window — which the
re-grounding (ADR 0006) keeps as one **signal** of depth, not the criterion. Depth is
the criterion: a deep module, a lot of behavior behind a small interface. The
deeper, **model-driven red-flag scan** — the deletion test, the shallow-module and
information-leakage flags, testable-through-the-interface — is the depth assessment
this review is meant to grow, and it is **not yet built** (ADR 0006). That
shallowness is recorded here and in the operator's gap, never fabricated into a
verdict. Length is the lens this slice ships; the red flags are the lens it will grow.

The record it consults is the structured depth-decision `folding-conditions` gates with
(`conditions.accepted`) — one criterion at two scopes: the per-graph gate at the fold,
and this standing whole-tree scan — so a file the gate would raise a decision on is the
same file the review flags, by construction.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from . import conditions, graph

# A module within this margin of the length signal is a god-file in the making — flagged
# early so deepening pressure is felt before a split is painful. A starting value to
# tune, like the signal itself, not a deep question.
NEAR = int(conditions.SIGNAL * 0.8)
BAR = 20                                  # the visual bar's width, the signal full


@dataclass
class Module:
    """One source file the review measured, with its standing against the length signal.
    `status`: ok | nearing | over | exceeded | accepted. `over` is past the signal with no
    depth-decision (a deepening opportunity); `accepted` is past the signal but within a
    structured depth-decision's accepted length; `exceeded` is past the signal *and* materially
    past the length a depth-decision once accepted it at — a stale acceptance, the depth decision
    re-opened (ADR 0008). `bar` is that accepted length for accepted/exceeded, else None."""
    rel: str
    lines: int
    status: str
    bar: int | None = None


@dataclass
class Finding:
    """A deepening opportunity for the backlog. `strength` is the recommendation's
    weight — strong (assess/deepen now) or consider (watch it)."""
    subject: str
    lines: int
    kind: str            # past the length signal | nearing the length signal
    strength: str        # strong | consider
    note: str


@dataclass
class Review:
    modules: list[Module] = field(default_factory=list)   # the structural map, largest first
    findings: list[Finding] = field(default_factory=list)  # the deepening backlog


# The honest record that the depth lens beyond length is not yet built — surfaced in the
# operator's gap rather than hidden, the self-honesty the operator view is built to practice.
DEPTH_NOT_YET = ("the depth scan beyond length — the red flags, the deletion test — is not "
                 "yet built (ADR 0006); length is the signal shown here")


def review(root: str | None = None) -> Review:
    """Scan the source tree live and report. Reads every module's length, places it against
    the length signal, and gathers the ones over (no depth-decision), past a stale accepted bar
    (exceeded), or nearing it into the deepening backlog. A file within its depth-decision's
    accepted length shows on the map, marked, but is not in the backlog — its size is a recorded
    decision; a file that has outgrown that bar returns to the backlog (ADR 0008)."""
    src = os.path.join(root or graph._root(), "hyper")
    modules = [_module(rel, n, root) for rel, n in _sources(src)]
    modules.sort(key=lambda m: -m.lines)
    return Review(modules, [f for m in modules if (f := _finding(m))])


def bars(rv: Review) -> list[str]:
    """The structural map as a visual: each module a bar by length against the signal, debt
    marked. A picture of the system's shape that needs no code read to take in."""
    if not rv.modules:
        return ["(no modules found)"]
    w = max(len(m.rel) for m in rv.modules)
    return [f"{m.rel.ljust(w)}  {_bar(m.lines)}  {m.lines}/{conditions.SIGNAL}{_mark(m)}"
            for m in rv.modules]


def backlog(rv: Review) -> list[str]:
    """The deepening backlog as the operator reads it — the gap. Honest about a clean tree
    rather than inventing work, and honest that the depth lens beyond length is not yet built."""
    if not rv.findings:
        return [f"no deepening opportunities — every module is within the length signal "
                f"({conditions.SIGNAL} lines); " + DEPTH_NOT_YET]
    return [f"{f.subject}: {f.note} ({f.strength})" for f in rv.findings]


# ── internals ────────────────────────────────────────────────────────────────

def _module(rel: str, n: int, root: str | None) -> Module:
    """Place one module against the signal and its depth-decision. Past the signal it is
    `accepted` (within the recorded bar + margin), `exceeded` (a bar exists but the file outgrew
    it — the ratchet re-opened the decision, ADR 0008), or `over` (no bar at all). The accepted
    bar is consulted from `conditions` so the per-graph gate and this standing scan agree on one
    criterion. Within the signal it is `nearing` or `ok`."""
    canon = _canon(rel)
    if n <= conditions.SIGNAL:
        return Module(rel, n, "nearing" if n >= NEAR else "ok")
    bar = conditions.accepted_at(canon, root)
    if conditions.accepted(canon, n, root):
        return Module(rel, n, "accepted", bar)
    return Module(rel, n, "exceeded", bar) if bar is not None else Module(rel, n, "over")


def _canon(rel: str) -> str:
    """The file's path relative to the repo root (e.g. `hyper/foo.py`) — the form the
    structured depth-decision names, so the standing scan and the per-graph gate agree."""
    return os.path.join("hyper", rel).replace(os.sep, "/")


def _finding(m: Module) -> Finding | None:
    if m.status == "over":
        return Finding(m.rel, m.lines, "past the length signal", "strong",
                       f"{m.lines} lines, past the {conditions.SIGNAL}-line length signal — "
                       "assess its depth (no depth-decision accepts its size); length is the "
                       "context-cost signal, the red-flag depth scan is not yet built")
    if m.status == "exceeded":
        return Finding(m.rel, m.lines, "past its accepted bar", "strong",
                       f"{m.lines} lines, materially past the {m.bar}-line bar a depth-decision "
                       "accepted it at — the acceptance is stale; re-cut, deepen, or renew it at "
                       "the new length (acceptance ratchets, it does not silence later growth)")
    if m.status == "nearing":
        return Finding(m.rel, m.lines, "nearing the length signal", "consider",
                       f"{m.lines} lines, nearing the {conditions.SIGNAL}-line length signal — "
                       "a god-file in the making")
    return None


def _bar(n: int) -> str:
    filled = min(BAR, round(n / conditions.SIGNAL * BAR))
    return "█" * filled + "░" * (BAR - filled)


def _mark(m: Module) -> str:
    if m.status == "accepted":
        return f"  (depth accepted@{m.bar})"
    if m.status == "exceeded":
        return f"  ⚑ grew past its accepted bar of {m.bar} — decision re-opened"
    return {"over": "  ⚑ past the length signal — assess depth",
            "nearing": "  • nearing", "ok": ""}[m.status]


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
