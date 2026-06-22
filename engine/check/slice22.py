"""Slice 22 — the external-conformance gate: the channels match the field standard and resolve.

The engine's other checks certify one invariant: a rendered artifact **matches its spec source** (the
fold re-renders, so a committed channel cannot drift). They never certify the two invariants that live
*outside* the spec — that the artifacts **conform to the harness's field standard** and that their
**pointers resolve**. Those are exactly the gaps that let the targeting defect ship: a skill can match
its slice perfectly and still land where no harness reads it, or carry a `spec/<cap>.md` pointer that a
rename has silently broken. This slice closes that meta-gap, over the *rendered* artifacts:

1. **frontmatter schema** — each rendered `SKILL.md` carries a `name` (lowercase/digit/hyphen, ≤64,
   equal to its directory) and a non-empty `description` (≤1024), the documented Claude Code hard limits;
2. **discovery location** — the skills materialize into `.claude/skills/<cap>/SKILL.md` (where stock
   Claude Code discovers project skills) and a `CLAUDE.md` bridge imports the anchor with `@AGENTS.md`
   (Claude Code reads `CLAUDE.md`, not a bare `AGENTS.md`) — the assertion that, had it existed, would
   have caught the targeting defect by construction rather than in a panel;
3. **links resolve** — every `spec/<cap>.md` pointer a rendered artifact carries, and the `@AGENTS.md`
   import target, names a file that exists, so a moved slice fails here loudly instead of silently.

The red→green this slice records is the targeting defect itself. The discovery-location assertion is
**RED** against a root materialized the old way (skills only in root `skills/`, no `CLAUDE.md` bridge)
and **GREEN** against one materialized by the current channels (the `.claude/skills/` mirror and the
bridge present). The check drives both halves so the loop is real, not narrated: it reconstructs the
old render in a throwaway tree, asserts the gate fails it, then asserts the gate passes the live render —
the same dogfood discipline slice 15 ran on the red-flag scan.

The honest limit, recorded not faked (the same one `anchor.py` keeps): this gate asserts the channels
land *where* the harness reads and conform to its *documented schema*. Whether a live `claude -p` session
actually loads them is the operator's watched evidence — an A/B measurement, never a thing a headless
check can assert.
"""
from __future__ import annotations

import os
import re
import shutil
import tempfile

from .harness import ok

NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")          # Claude Code: lowercase/digit/hyphen, ≤64
DESC_MAX = 1024                                       # Claude Code: description non-empty, ≤1024


def _frontmatter(text: str) -> dict:
    """The `key: value` pairs of a SKILL.md's leading `---`-fenced YAML block — flat, one level, which
    is all a skill's frontmatter is. Returns {} if the block is absent or unterminated."""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    out: dict = {}
    for line in text[4:end].splitlines():
        if ": " in line:
            k, v = line.split(": ", 1)
            out[k.strip()] = v.strip()
    return out


def _schema_errors(cap: str, text: str) -> list[str]:
    """The frontmatter-schema violations of one rendered skill, against the documented Claude Code
    limits — empty list when it conforms. The check the field's frontmatter validators run, inlined so
    the gate has no external dependency and asserts exactly the limits the harness enforces."""
    fm = _frontmatter(text)
    errs: list[str] = []
    name = fm.get("name", "")
    if not name:
        errs.append("missing name")
    elif not NAME_RE.match(name):
        errs.append(f"name {name!r} is not lowercase/digit/hyphen ≤64")
    elif name != cap:
        errs.append(f"name {name!r} != directory {cap!r}")
    desc = fm.get("description", "")
    if not desc:
        errs.append("missing description")
    elif len(desc) > DESC_MAX:
        errs.append(f"description {len(desc)} chars > {DESC_MAX}")
    return errs


def _pointers(text: str) -> list[str]:
    """The repo-relative file pointers a rendered artifact carries — backtick-quoted `spec/<cap>.md`
    paths and `@AGENTS.md` import targets — the links the gate must confirm resolve."""
    return re.findall(r"`(spec/[\w./-]+\.md)`", text) + re.findall(r"(?m)^@([\w./-]+)\s*$", text)


def _materialize_old_way(root: str) -> None:
    """Reconstruct the pre-fix render: the five skills in the bare root `skills/` only, no
    `.claude/skills/` mirror and no `CLAUDE.md` bridge — the targeting defect, rebuilt so the gate can
    be shown RED against it. This is the recorded red half of the loop, driven, not described."""
    from .. import anchor, methodology
    for cap in methodology.METHODOLOGIES:
        methodology.materialize(cap, root, skill_dir="skills")
    anchor.materialize(root)                          # AGENTS.md only — no CLAUDE.md bridge


def _discovery_ok(root: str) -> bool:
    """The discovery-location invariant the targeting fix established: every skill is present under
    `.claude/skills/<cap>/SKILL.md` (where Claude Code discovers them) and a `CLAUDE.md` bridge imports
    the anchor (`@AGENTS.md`). Returns the verdict so the check can assert it on both halves of the loop."""
    from .. import anchor, methodology
    skills_landed = all(
        os.path.isfile(os.path.join(root, methodology.skill_path(cap, os.path.join(".claude", "skills"))))
        for cap in methodology.METHODOLOGIES)
    bridge = os.path.join(root, anchor.BRIDGE_PATH)
    bridge_imports = os.path.isfile(bridge) and "@AGENTS.md" in open(bridge).read()
    return skills_landed and bridge_imports


def check(_shared_root: str) -> None:
    from .. import channels, graph, methodology

    print("\nslice 22 — acceptance check  (the external-conformance gate: the channels conform and resolve)\n")

    root = tempfile.mkdtemp(prefix="engine-check-slice22-")
    # Seed the throwaway root with the real spec + glossary, so the render reads the live slices and
    # every rendered `spec/<cap>.md` pointer resolves within one self-consistent tree — a faithful fold.
    repo = graph._DEFAULT_ROOT
    shutil.copytree(os.path.join(repo, "spec"), os.path.join(root, "spec"))
    shutil.copy(os.path.join(repo, "glossary.md"), os.path.join(root, "glossary.md"))

    # ── the red→green loop: the targeting defect, caught by the discovery-location assertion ───────
    # RED — the old render (root `skills/` only, no bridge): the gate fails it, as it would have failed
    # the system before the targeting fix. GREEN — the live channels (the mirror + the bridge).
    _materialize_old_way(root)
    ok(not _discovery_ok(root),
       "RED: the pre-fix render (root skills/ only, no CLAUDE.md bridge) fails the discovery gate")

    channels.materialize(root)                        # the live fold: mirror to .claude/skills + bridge
    ok(_discovery_ok(root),
       "GREEN: the live channels land skills in .claude/skills/ and bridge the anchor via @AGENTS.md")

    # ── frontmatter schema: each rendered skill meets the documented Claude Code hard limits ───────
    for cap in methodology.METHODOLOGIES:
        text = open(os.path.join(root, methodology.skill_path(cap))).read()
        errs = _schema_errors(cap, text)
        ok(not errs, f"{cap}: frontmatter conforms to the SKILL.md schema"
           + (f" (violations: {errs})" if errs else ""))

    # ── links resolve: every rendered pointer names a file that exists ─────────────────────────────
    artifacts = [os.path.join(root, methodology.skill_path(cap)) for cap in methodology.METHODOLOGIES]
    artifacts += [os.path.join(root, "AGENTS.md"), os.path.join(root, "CLAUDE.md")]
    broken: list[str] = []
    for art in artifacts:
        body = open(art).read()
        for ptr in _pointers(body):
            if not os.path.isfile(os.path.join(root, ptr)):
                broken.append(f"{os.path.basename(art)} → {ptr}")
    ok(not broken, "every rendered pointer (spec/<cap>.md, @AGENTS.md) resolves"
       + (f" (broken: {broken})" if broken else ""))

    # The slice must render against a populated spec — guard the check itself isn't vacuously green.
    ok(graph and methodology.METHODOLOGIES, "the gate ran over the real skill set (not an empty roster)")
