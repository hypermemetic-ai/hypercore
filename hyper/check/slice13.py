"""Slice 13 — item 2, build step 3: the minimal shared AGENTS.md anchor (ADR 0009 §0/§4, role-assembly step 3).

Acceptance (ADR 0009): the agents file is a single **minimal shared anchor, non-inferable content only** —
the check command, the build/hand-back convention, and a pointer to the skills — materialized on fold like
every derived channel, with `CLAUDE.md` a symlink to it. The skills index is *derived* from the registry, so
it cannot drift; the operational lines are the authored non-inferable residue. (Whether the file helps a live
model is the A/B the field warns to run before leaning on it — a measurement, not a check; ADR 0009 §6.)

1. **minimal and non-inferable** — the anchor carries the check command and the hand-back convention, and
   nothing inferable: no per-capability requirements, no code, no identity prose;
2. **the skills index is derived** — every registered skill is listed, pulled from the registry, not hand-typed;
3. **the fold materializes it + the symlink** — a fold writes the anchor through the channels registry and
   `CLAUDE.md` is a symlink to `AGENTS.md`;
4. **drift is impossible** — a newly registered skill appears in the anchor by construction.
"""
from __future__ import annotations

import os

from .harness import ok


def check(root: str) -> None:
    from .. import anchor, channels, delta, methodology

    print("\nslice 13 — acceptance check  (the minimal shared AGENTS.md anchor)\n")

    art = os.path.join(root, anchor.PATH)
    link = os.path.join(root, anchor.SYMLINK)
    for p in (art, link):
        if os.path.lexists(p):
            os.remove(p)

    # ── 1. minimal and non-inferable ──────────────────────────────────────────────────────
    text = anchor.agents_file(root)
    ok(anchor.CHECK in text, "the anchor carries the non-inferable check command")
    ok("for the machine" in text and "operator-facing word" in text,
       "the anchor carries the build/hand-back convention")
    ok("### Requirement:" not in text and "import " not in text and "You are hypercore" not in text,
       "the anchor is minimal — no per-capability requirements, no code, no identity prose")

    # ── 2. the skills index is derived from the registry, not hand-listed ──────────────────
    ok("`depth`" in text and all(f"`{name}`" in text for name in methodology.METHODOLOGIES),
       "the anchor's skills index lists every registered skill — derived from the registries")

    # ── 3. the fold materializes the anchor + the CLAUDE.md symlink ────────────────────────
    delta.fold(delta.parse("# delta — trivial (no behavior change)"), root)
    ok(os.path.isfile(art) and open(art, encoding="utf-8").read() == text,
       "the fold materializes the anchor on disk — a pure render through the channels registry")
    ok(os.path.islink(link) and os.readlink(link) == anchor.PATH,
       "CLAUDE.md is a symlink to AGENTS.md — one source, both roles (ADR 0009 §4)")
    ok(anchor.materialize in channels.CHANNELS,
       "the anchor is registered in the channels registry beside the skills")

    # ── 4. drift is impossible: a newly registered skill appears in the anchor ─────────────
    methodology.METHODOLOGIES["__planted__"] = "a planted methodology — load when testing drift."
    try:
        ok("`__planted__`" in anchor.agents_file(root),
           "a newly registered skill appears in the anchor index by construction — it cannot drift")
    finally:
        del methodology.METHODOLOGIES["__planted__"]

    # the anchor never clobbers a real CLAUDE.md an operator authored
    os.remove(link)
    with open(link, "w", encoding="utf-8") as f:
        f.write("# a real CLAUDE.md the operator wrote\n")
    anchor.materialize(root)
    ok(not os.path.islink(link) and "operator wrote" in open(link, encoding="utf-8").read(),
       "a real CLAUDE.md is left untouched — the materializer cannot eat hand-written content")
