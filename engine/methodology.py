"""The capability skills, single-sourced as `SKILL.md` artifacts from their spec slices.

An agent carries its specialization in **skills** (ADR 0009): the disciplines it routes to when the
work calls for them — the architect's `design-it-twice`, `architecture-review`, `grilling`, and
`coherence`, and the worker's `depth` — each a clean standalone capability with its own
`spec/<cap>.md`. This module renders each slice into a progressive-disclosure `SKILL.md`: the
metadata names *when* to load it, the body is the slice's methodology overview (its preamble) and its
disciplines (each requirement's statement), and the resource pointer is the slice itself for the full
requirements and their scenarios.

One render of one source into the skill channel, no hand-copy, so a sharpened slice reaches the next
agent with no second copy to drift. `channels` drives it on fold (role-assembly step 4) — the
registry the fold re-renders so a committed artifact can never disagree with its spec slice.

`depth` renders here exactly like the others (ADR 0019): an imported design discipline is a capability
like `design-it-twice` (ADR 0007), not a special type, so it dropped its bespoke `depth.py` render and
joined this one seam. `grilling` and `coherence` were likewise carved out of `conversation` into their
own slices (ADR 0013) rather than a requirement-subset render, which would have added a second copy of
the requirement set to drift. Each is one clean `spec/<cap>.md`; a new skill adds one line.
"""
from __future__ import annotations

import functools
import os

from . import graph, spec

# Where a methodology skill artifact lands, mirroring depth's: skills/<cap>/SKILL.md.
SKILL_DIR = "skills"

# The capability skills: capability slice → the authored *when to load it*. The body is
# single-sourced from the slice; only this operational framing is authored, and only the
# capabilities with a clean standalone slice are here. A new skill adds one line.
METHODOLOGIES = {
    "design-it-twice":
        "hypercore's design-it-twice methodology — design a load-bearing interface as a contest of "
        "isolated candidates, then pick or hybridize on depth, locality, and seam placement. Load "
        "when designing or judging a load-bearing interface decision.",
    "architecture-review":
        "hypercore's architecture-review methodology — the standing scan that keeps the system deep, "
        "surfacing god-files-in-the-making by the length signal against the depth-decision record. "
        "Load when assessing structural depth or reading the deepening backlog.",
    "grilling":
        "hypercore's grilling methodology — turn a filed ask into a ratified contract and spec delta "
        "by resolving what the spec and intent already settle and surfacing only the stake-bearing "
        "residue, one question at a time, each with a lean and a flip. Load when extracting intent "
        "from an ask or judging whether it is ready to become work.",
    "coherence":
        "hypercore's coherence methodology — the archive-gate judgment over a worker's hand-off: check "
        "it against the contract at the operator's altitude (not a code review) and against the depth "
        "bar, folding on a pass and raising a decision otherwise. Load when integrating or archiving "
        "a worker's result.",
    "depth":
        "hypercore's depth disciplines — build deep modules (a lot of behavior behind a small "
        "interface) and avoid the red flags of shallowness. Load when designing, building, or "
        "refining a module's interface or implementation.",
}

# The shipping repo — the fallback source, so the render works against a bare root (the harness plants
# a controlled slice into its root; a real fold there falls back to the repo's slice). Same idiom as depth.
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def skill(cap: str, root: str | None = None) -> str:
    """The `cap` methodology rendered as a SKILL.md, single-sourced from `spec/<cap>/spec.md`: the
    metadata (when to load), the slice's methodology overview, its disciplines (each requirement's
    statement, the scenarios left in the slice), and the pointer back to the slice for the full detail."""
    text = _read_slice(cap, root)
    return (
        "---\n"
        f"name: {cap}\n"
        f"description: {METHODOLOGIES[cap]}\n"
        "---\n\n"
        f"# {cap}\n\n"
        f"{_overview(text)}\n\n"
        "## The disciplines — what good looks like\n\n" + _bullets(_disciplines(text)) + "\n\n"
        "## Going deeper\n\n"
        f"The full requirements and their scenarios are `spec/{cap}.md`, this skill's single source.\n"
    )


def materialize(cap: str, root: str | None = None) -> str:
    """Write the `cap` methodology skill to disk and return its path — the render `channels` runs on
    fold so the artifact follows its slice. One skill per call."""
    path = os.path.join(root or graph._root(), SKILL_DIR, cap, "SKILL.md")
    graph.atomic_write(path, skill(cap, root))
    return path


def materializers() -> tuple:
    """One materializer per registered skill, for `channels.CHANNELS` — each a `(root) -> path`
    render, so the registry stays one flat list of single-skill renders and the fold re-derives
    every skill with no special case."""
    return tuple(functools.partial(materialize, cap) for cap in METHODOLOGIES)


def skill_path(cap: str) -> str:
    """The artifact's path relative to a root — `skills/<cap>/SKILL.md` — the form the harness checks."""
    return os.path.join(SKILL_DIR, cap, "SKILL.md")


# ── the render: a capability slice → its methodology overview and disciplines ──────────────

def _read_slice(cap: str, root: str | None) -> str:
    """The capability's spec slice — the project root first, the shipping repo as fallback."""
    here = spec.cap_path(cap, root)
    path = here if os.path.isfile(here) else os.path.join(_REPO, "spec", cap + ".md")
    return open(path, encoding="utf-8", errors="ignore").read()


def _overview(text: str) -> str:
    """The slice's preamble — the methodology prose between the `# <cap>` title and the first
    requirement. This is the 'how and why you do this well' the skill leads with."""
    lines = text.splitlines()
    start = 1 if lines and lines[0].startswith("# ") else 0
    out: list[str] = []
    for ln in lines[start:]:
        if ln.startswith(spec.REQ):
            break
        out.append(ln)
    return "\n".join(out).strip()


def _disciplines(text: str) -> list[str]:
    """One discipline per requirement: its name and its statement (the scenarios stay in the slice,
    reached through the pointer) — the durable 'what good looks like', single-sourced from the slice."""
    return [f"**{r.name}** — {_statement(r)}" for r in spec._requirements(text)]


def _statement(req: spec.Requirement) -> str:
    """A requirement's statement — the prose after its heading, up to its first scenario — as one line."""
    out: list[str] = []
    for ln in req.block.splitlines()[1:]:
        if ln.startswith("#### Scenario:"):
            break
        out.append(ln)
    return " ".join(ln.strip() for ln in out if ln.strip())


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {it}" for it in items)
