"""The architecture review — the standing scan that keeps the system deep.

A periodic scan for deepening opportunities (rebuild-spec §7.4), run as a standing
process, not a one-off: read live off the source tree every time, never a stored
report. It has two roles, and this module serves both from one scan:

- **The engine of deepening.** It surfaces god-files-in-the-making before they set —
  a module past the length signal, or one nearing it — each as a finding carrying its
  measure and a recommendation strength. This is the deepening backlog.
- **The operator view's "what the system is" upper levels (§4.2).** The same scan
  renders the structural map of as-built reality — every module by length against the
  signal, debt marked — so the operator reads the shape of the system at a glance,
  without reading code. The review is *not a separate artifact*: its output is the
  operator view's as-built and gap (`view.operator_view`), kept honest between folds.

What it measures is **length** — what a module costs a worker's window — which the
re-grounding (ADR 0006) keeps as one **signal** of depth, not the criterion. Depth is
the criterion: a deep module, a lot of behavior behind a small interface. The
deeper, **model-driven red-flag scan** — the deletion test, the shallow-module and
information-leakage flags, testable-through-the-interface — is the depth assessment
this review is meant to grow, and it is **not yet built** (slice 7, F1). That
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
# tune (§11), like the signal itself, not a deep question.
NEAR = int(conditions.SIGNAL * 0.8)
BAR = 20                                  # the visual bar's width, the signal full


@dataclass
class Module:
    """One source file the review measured, with its standing against the length signal.
    `status`: ok | nearing | over | accepted — `over` is length past the signal with no
    depth-decision (a deepening opportunity); `accepted` is past the signal but a structured
    depth-decision records it accepted."""
    rel: str
    lines: int
    status: str


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
                 "yet built (rebuild-spec §7.4, ADR 0006); length is the signal shown here")


def review(root: str | None = None) -> Review:
    """Scan the source tree live and report. Reads every module's length, places it against
    the length signal, and gathers the ones over (no depth-decision) or nearing it into the
    deepening backlog. A depth-accepted file shows on the map, marked, but is not in the
    backlog — its size is a recorded decision."""
    src = os.path.join(root or graph._root(), "hyper")
    modules = [Module(rel, n, _status(rel, n, root)) for rel, n in _sources(src)]
    modules.sort(key=lambda m: -m.lines)
    return Review(modules, [f for m in modules if (f := _finding(m))])


def bars(rv: Review) -> list[str]:
    """The structural map as a visual: each module a bar by length against the signal, debt
    marked. A picture of the system's shape that needs no code read to take in."""
    if not rv.modules:
        return ["(no modules found)"]
    w = max(len(m.rel) for m in rv.modules)
    return [f"{m.rel.ljust(w)}  {_bar(m.lines)}  {m.lines}/{conditions.SIGNAL}{_mark(m.status)}"
            for m in rv.modules]


def backlog(rv: Review) -> list[str]:
    """The deepening backlog as the operator reads it — the gap. Honest about a clean tree
    rather than inventing work, and honest that the depth lens beyond length is not yet built."""
    if not rv.findings:
        return [f"no deepening opportunities — every module is within the length signal "
                f"({conditions.SIGNAL} lines); " + DEPTH_NOT_YET]
    return [f"{f.subject}: {f.note} ({f.strength})" for f in rv.findings]


# ── internals ────────────────────────────────────────────────────────────────

def _status(rel: str, n: int, root: str | None) -> str:
    if n > conditions.SIGNAL:
        return "accepted" if conditions.accepted(_canon(rel), root) else "over"
    return "nearing" if n >= NEAR else "ok"


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
    if m.status == "nearing":
        return Finding(m.rel, m.lines, "nearing the length signal", "consider",
                       f"{m.lines} lines, nearing the {conditions.SIGNAL}-line length signal — "
                       "a god-file in the making")
    return None


def _bar(n: int) -> str:
    filled = min(BAR, round(n / conditions.SIGNAL * BAR))
    return "█" * filled + "░" * (BAR - filled)


def _mark(status: str) -> str:
    return {"over": "  ⚑ past the length signal — assess depth",
            "accepted": "  (depth accepted)",
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
