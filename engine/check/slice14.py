"""Slice 14 — item 2, build step 4b: the grilling + coherence skills (role-assembly step 4b).

Acceptance: the architect's remaining methodologies — `grilling` (pre-work intent
extraction) and `coherence` (the archive-gate judgment) — are carved out of `communication` into their own
capabilities, each a clean standalone `spec/<cap>.md`, and render as skills through the SAME methodology
seam as `design-it-twice` / `architecture-review`: single-sourced from their slice and materialized by the fold.

Read against the real spec, seeded into a throwaway root the check mints itself — the slice-22 idiom — so
it sees the live carve without depending on a sibling slice to seed the shared root (slice 2's seeding
dissolved with the communication migration). No behavior changed, only the requirements' home moved.

1. **the carve** — grilling and coherence are their own capabilities, the moved requirements gone from
   communication and present verbatim in the new slices;
2. **registered + rendered** — both are methodologies that render a progressive-disclosure skill from their slice;
3. **materialized by the fold** — both skills land on disk through the channels registry.
"""
from __future__ import annotations

import os
import shutil
import tempfile

from .harness import ok


def check(_shared_root: str) -> None:
    from .. import channels, methodology, spec, tree

    print("\nslice 14 — acceptance check  (grilling + coherence carved and skilled)\n")

    # Seed a throwaway root with the real spec + glossary, so the render reads the live slices and every
    # rendered `spec/<cap>.md` pointer resolves within one self-consistent tree — self-seeded, the way
    # slice 22 does, so no sibling slice needs to seed the shared root for this one.
    root = tempfile.mkdtemp(prefix="engine-check-slice14-")
    repo = tree._DEFAULT_ROOT
    shutil.copytree(os.path.join(repo, "spec"), os.path.join(root, "spec"))
    shutil.copy(os.path.join(repo, "glossary.md"), os.path.join(root, "glossary.md"))

    # ── 1. the carve: grilling and coherence are their own capabilities ────────────────────
    sp = spec.read_spec(root)                          # the real spec, seeded into the throwaway root
    names = {c.name for c in sp.capabilities}
    ok({"grilling", "coherence"} <= names,
       "grilling and coherence are their own capabilities, carved from communication")
    conv = sp.capability("communication")
    moved = ["a filed ask is grilled before it becomes work",
             "grilling asks one question at a time, each carrying a lean",
             "the architect integrates the worker's hand-off",
             "the architect judges depth at the archive gate"]
    ok(conv is not None and all(conv.requirement(r) is None for r in moved),
       "the grilling and coherence requirements left communication — carved, not copied")
    ok(sp.capability("grilling").requirement("a filed ask is grilled before it becomes work") is not None
       and sp.capability("coherence").requirement("the architect integrates the worker's hand-off") is not None,
       "the moved requirements live in their new capabilities verbatim")

    # ── 2. both register and render through the existing methodology seam ──────────────────
    ok({"grilling", "coherence"} <= set(methodology.METHODOLOGIES),
       "grilling and coherence are registered methodologies — they render like design-it-twice")
    gk = methodology.skill("grilling", root)
    ok(gk.startswith("---") and "name: grilling" in gk and "spec/grilling.md" in gk
       and "**a filed ask is grilled before it becomes work**" in gk,
       "the grilling skill is a progressive-disclosure render of its carved slice, single-sourced")
    ck = methodology.skill("coherence", root)
    ok(ck.startswith("---") and "name: coherence" in ck and "spec/coherence.md" in ck
       and "**the architect integrates the worker's hand-off**" in ck,
       "the coherence skill is a progressive-disclosure render of its carved slice, single-sourced")
    ok("- WHEN a worker hands a result back" not in ck,
       "the skills carry the discipline statements but leave the scenarios in the slice")

    # ── 3. the fold materializes them through the channels registry ────────────────────────
    paths = channels.materialize(root)
    for cap in ("grilling", "coherence"):
        p = os.path.join(root, methodology.skill_path(cap))
        ok(os.path.isfile(p) and any(os.path.samefile(p, q) for q in paths),
           f"the {cap} skill materializes through the channels registry")
