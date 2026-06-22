"""Slice 14 — item 2, build step 4b: the grilling + coherence skills (ADR 0013, role-assembly step 4b).

Acceptance (ADR 0009 §1 + ADR 0013): the architect's remaining methodologies — `grilling` (pre-work intent
extraction) and `coherence` (the archive-gate judgment) — are carved out of `conversation` into their own
capabilities, each a clean standalone `spec/<cap>/spec.md`, and render as skills through the SAME methodology
seam as `design-it-twice` / `architecture-review`: single-sourced from their slice and materialized by the fold.

Read against the real spec (seeded into the harness root by slice 2), so the check sees the live carve — no
behavior changed, only the requirements' home moved.

1. **the carve** — grilling and coherence are their own capabilities, the moved requirements gone from
   conversation and present verbatim in the new slices;
2. **registered + rendered** — both are methodologies that render a progressive-disclosure skill from their slice;
3. **materialized by the fold** — both skills land on disk through the channels registry.
"""
from __future__ import annotations

import os

from .harness import ok


def check(root: str) -> None:
    from .. import channels, methodology, spec

    print("\nslice 14 — acceptance check  (grilling + coherence carved and skilled)\n")

    # ── 1. the carve: grilling and coherence are their own capabilities ────────────────────
    sp = spec.read_spec()                              # the real spec, seeded into the harness root
    names = {c.name for c in sp.capabilities}
    ok({"grilling", "coherence"} <= names,
       "grilling and coherence are their own capabilities, carved from conversation (ADR 0013)")
    conv = sp.capability("conversation")
    moved = ["a filed ask is grilled before it becomes work",
             "grilling asks one question at a time, each carrying a lean",
             "the architect integrates the worker's hand-off",
             "the architect judges depth at the archive gate"]
    ok(conv is not None and all(conv.requirement(r) is None for r in moved),
       "the grilling and coherence requirements left conversation — carved, not copied")
    ok(sp.capability("grilling").requirement("a filed ask is grilled before it becomes work") is not None
       and sp.capability("coherence").requirement("the architect integrates the worker's hand-off") is not None,
       "the moved requirements live in their new capabilities verbatim")

    # ── 2. both register and render through the existing methodology seam ──────────────────
    ok({"grilling", "coherence"} <= set(methodology.METHODOLOGIES),
       "grilling and coherence are registered methodologies — they render like design-it-twice")
    gk = methodology.skill("grilling")
    ok(gk.startswith("---") and "name: grilling" in gk and "spec/grilling/spec.md" in gk
       and "**a filed ask is grilled before it becomes work**" in gk,
       "the grilling skill is a progressive-disclosure render of its carved slice, single-sourced")
    ck = methodology.skill("coherence")
    ok(ck.startswith("---") and "name: coherence" in ck and "spec/coherence/spec.md" in ck
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
