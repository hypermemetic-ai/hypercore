"""The architect's design methodologies, single-sourced as skills from their capability slices.

The architect carries its specialization in **skills** (ADR 0009): the design methodologies it
routes to when the work calls for them — `design-it-twice` (judge a load-bearing interface as a
contest of isolated candidates) and `architecture-review` (the standing depth scan) — each a clean
standalone capability with its own `spec/<cap>/spec.md`. This module renders each slice into a
progressive-disclosure `SKILL.md`: the metadata names *when* to load it, the body is the slice's
methodology overview (its preamble) and its disciplines (each requirement's statement), and the
resource pointer is the slice itself for the full requirements and their scenarios.

It is `depth.py` for the architect: one render of one source into the skill channel, no hand-copy,
so a sharpened slice reaches the next architect with no second copy to drift. `channels` drives it on
fold (role-assembly step 4) exactly as it drives the worker's `depth` skill — the registry the fold
re-renders so a committed artifact can never disagree with its spec slice.

`grilling` and the coherence judgment (the architect's other methodologies, ADR 0009 §1) are *not*
here: they live as requirements inside `conversation`, not as a standalone slice, so they have no
`spec/<cap>/spec.md` to render. Skilling them needs either a `grilling` slice carved from
`conversation` or a requirement-subset render — a follow-up recorded on the work graph, not hacked in.
"""
from __future__ import annotations

import functools
import os

from . import graph, spec

# Where a methodology skill artifact lands, mirroring depth's: skills/<cap>/SKILL.md.
SKILL_DIR = "skills"

# The architect's methodology skills: capability slice → the authored *when to load it*. The body is
# single-sourced from the slice; only this operational framing is authored (like depth's header), and
# only the capabilities with a clean standalone slice are here. New methodologies add one line.
METHODOLOGIES = {
    "design-it-twice":
        "hypercore's design-it-twice methodology — design a load-bearing interface as a contest of "
        "isolated candidates, then pick or hybridize on depth, locality, and seam placement. Load "
        "when designing or judging a load-bearing interface decision.",
    "architecture-review":
        "hypercore's architecture-review methodology — the standing scan that keeps the system deep, "
        "surfacing god-files-in-the-making by the length signal against the depth-decision record. "
        "Load when assessing structural depth or reading the deepening backlog.",
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
        f"# {cap} — an architect methodology\n\n"
        f"{_overview(text)}\n\n"
        "## The disciplines — what good looks like\n\n" + _bullets(_disciplines(text)) + "\n\n"
        "## Going deeper\n\n"
        f"The full requirements and their scenarios are `spec/{cap}/spec.md`, this skill's single source.\n"
    )


def materialize(cap: str, root: str | None = None) -> str:
    """Write the `cap` methodology skill to disk and return its path — the render `channels` runs on
    fold so the artifact follows its slice. One skill per call, like `depth.materialize`."""
    path = os.path.join(root or graph._root(), SKILL_DIR, cap, "SKILL.md")
    graph.atomic_write(path, skill(cap, root))
    return path


def materializers() -> tuple:
    """One materializer per registered methodology, for `channels.CHANNELS` to splice in beside
    `depth.materialize` — each a `(root) -> path` render, so the registry stays one flat list of
    single-skill renders and the fold re-derives every architect skill with no special case."""
    return tuple(functools.partial(materialize, cap) for cap in METHODOLOGIES)


def skill_path(cap: str) -> str:
    """The artifact's path relative to a root — `skills/<cap>/SKILL.md` — the form the harness checks."""
    return os.path.join(SKILL_DIR, cap, "SKILL.md")


# ── the render: a capability slice → its methodology overview and disciplines ──────────────

def _read_slice(cap: str, root: str | None) -> str:
    """The capability's spec slice — the project root first, the shipping repo as fallback."""
    here = spec.cap_path(cap, root)
    path = here if os.path.isfile(here) else os.path.join(_REPO, "spec", cap, "spec.md")
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
