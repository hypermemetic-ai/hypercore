"""The depth disciplines, single-sourced from the synthesis — no frozen copy.

The worker is grounded in the depth disciplines every episode (ADR 0006/0009): the
deep-module criterion, strategic-over-tactical, and the red flags of shallowness. Those
disciplines have **one home** — `spec/depth.md`, the faithful synthesis of Ousterhout's
*A Philosophy of Software Design* — and this module is their single render into the
channels that carry them: the worker's prompt-side grounding today (`disciplines`), and a
`depth` **skill** artifact (`skill`/`materialize`) for when the harness seam lands and the
worker loads skills natively.

This kills the `worker.DEPTH` smell ADR 0009 names: a hand-compression of the synthesis
frozen in a Python constant was a second copy that drifted the moment the synthesis was
sharpened. Here the disciplines are *derived* from spec/depth.md's two canonical lists — the
**design principles** (§3, the positive disciplines to build toward) and the **red flags**
(§2, the symptoms to build away from) — so the moment spec/depth.md changes, every channel
that carries them changes with it. It is the operator view's discipline pointed at one more
target: the as-built is derived, only the vision is authored, and a derived channel cannot
drift from its source.
"""
from __future__ import annotations

import os
import re

from . import graph

# The disciplines' one home, relative to a root. The render reads it live (like the spec),
# never caches — so a sharpened synthesis is in the next worker's grounding with no second step.
SOURCE = os.path.join("spec", "depth.md")

# The repo this ships in — the fallback source. The depth disciplines are hypercore's own
# methodology, present even when a project root carries no `spec/depth.md` of its own (the
# acceptance harness runs against a bare temp root), so the package's spec/depth.md backs the
# render when the root has none. A project root takes precedence, which is what lets the harness
# plant a controlled source and prove the render is derived from it.
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_ITEM = re.compile(r"^\d+\.\s+(.*)")          # a numbered list item: "1. <text>"

# Where the materialized skill artifact lands (the one new mechanism, ADR 0009 §3): a static
# file an external harness auto-loads, regenerated from source by the fold's render step.
SKILL_PATH = os.path.join("skills", "depth", "SKILL.md")


def disciplines(root: str | None = None) -> str:
    """The worker's prompt-side depth grounding, rendered from aposd.md — what replaces the
    retired `worker.DEPTH` constant. The positive disciplines first (build toward the criterion),
    then the red flags (build away from the symptoms), both single-sourced; the header is the only
    authored part, and it is operational framing, not restated content."""
    principles, red_flags = _lists(root)
    return (
        "The depth disciplines — you are held to these; build deep up front, so your work folds "
        "without tripping the depth gate. hypercore's standing engineering disciplines, "
        "single-sourced from spec/depth.md (Ousterhout, A Philosophy of Software Design):\n\n"
        "Build toward these (the design principles):\n" + _bullets(principles) + "\n\n"
        "Build away from these (the red flags of shallowness):\n" + _bullets(red_flags)
    )


def skill(root: str | None = None) -> str:
    """The `depth` skill — the same disciplines rendered as a progressive-disclosure SKILL.md for
    a harness that loads skills natively (ADR 0009 §5). The metadata names *when* to load it (the
    ~50-token level), the body is the disciplines (single-sourced), and the resource pointer is
    spec/depth.md itself for the full reasoning. Created now for the parked harness seam."""
    principles, red_flags = _lists(root)
    return (
        "---\n"
        "name: depth\n"
        "description: hypercore's depth disciplines — build deep modules (a lot of behavior "
        "behind a small interface) and avoid the red flags of shallowness. Load when designing, "
        "building, or refining a module's interface or implementation.\n"
        "---\n\n"
        "# Depth — build deep modules\n\n"
        "You are held to these standing disciplines; build deep up front so your work folds "
        "without tripping the depth gate.\n\n"
        "## Build toward these — the design principles\n\n" + _bullets(principles) + "\n\n"
        "## Build away from these — the red flags of shallowness\n\n" + _bullets(red_flags) + "\n\n"
        "## Going deeper\n\n"
        "The full synthesis — the reasoning behind each discipline, the *Clean Code* contrast, and "
        "the epistemic status — is `spec/depth.md`, this skill's single source.\n"
    )


def materialize(root: str | None = None) -> str:
    """Write the depth skill artifact to disk and return its path. The one new mechanism ADR 0009
    names: unlike the live-rendered operator view, a skill is a static file an external harness
    auto-loads, so it must be *materialized*. The fold's render step regenerates it from source
    (build step 2); here it is the artifact created for the seam, single-sourced like the rest."""
    path = os.path.join(root or graph._root(), SKILL_PATH)
    graph.atomic_write(path, skill(root))
    return path


# ── the render: spec/depth.md's two canonical lists → the disciplines ─────────

def _lists(root: str | None) -> tuple[list[str], list[str]]:
    """The (design principles, red flags) of the synthesis — its two canonical numbered lists,
    extracted from the one source. These *are* the disciplines; everything else in spec/depth.md
    is the reasoning that justifies them."""
    text = open(_source(root), encoding="utf-8", errors="ignore").read()
    return _numbered(_section(text, "design principles")), _numbered(_section(text, "red flags"))


def _source(root: str | None) -> str:
    """spec/depth.md, the disciplines' one home — the project root first, the shipping repo as fallback."""
    here = os.path.join(root or graph._root(), SOURCE)
    return here if os.path.isfile(here) else os.path.join(_REPO, SOURCE)


def _section(text: str, title: str) -> list[str]:
    """The body lines of the `## ` section whose heading carries `title` — from after its heading
    to the next `## `. Anchored on the heading's words, not its number, so renumbering the
    synthesis does not silently empty the render."""
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines)
                  if ln.startswith("## ") and title in ln.lower()), None)
    if start is None:
        return []
    end = next((j for j in range(start + 1, len(lines)) if lines[j].startswith("## ")), len(lines))
    return lines[start + 1:end]


def _numbered(body: list[str]) -> list[str]:
    """The numbered list items in a section body, each as one clean line — wrapped continuation
    lines (indented under an item) folded back in, markdown emphasis stripped. Non-item prose
    (the section's intro, a trailing aside) is skipped: only `1. …` lines start an item."""
    items: list[str] = []
    for ln in body:
        m = _ITEM.match(ln)
        if m:
            items.append(m.group(1).strip())
        elif items and ln.strip() and ln[:1] in " \t":   # an indented wrap of the current item
            items[-1] += " " + ln.strip()
    return [_plain(it) for it in items]


def _plain(s: str) -> str:
    return s.replace("**", "").replace("*", "")


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {it}" for it in items)
