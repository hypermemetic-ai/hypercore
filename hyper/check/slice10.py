"""Slice 10 — item 2, build step 1: retire the worker.DEPTH smell (ADR 0009 §5 step 1).

Acceptance (assembly.md §6, ADR 0009): the worker's depth grounding is no longer a frozen
hand-compression of `research/aposd.md` in a Python constant — it is **rendered from aposd.md,
single-sourced**, so the moment the synthesis changes the grounding changes with it. A `depth`
**skill** artifact carries the same disciplines for the parked harness seam. The worker's
whole-spec grounding is untouched (the slice-4 keystone), and the worker still carries the depth
disciplines every episode (the slice-7 proactive defense), now *derived* rather than copied.

This drives the real render over a **planted** aposd.md — the harness writes a controlled source
into its root the way slice 9 plants decision files — pinning four properties:

1. **the frozen copy is gone** — `worker.DEPTH` no longer exists;
2. **derived, not authored** — the worker's prompt-side grounding and the skill both render the
   planted disciplines, and editing the planted aposd.md changes them (drift is impossible);
3. **single source, two channels** — prompt grounding and skill artifact render from the one file,
   and the skill materializes on disk (the one new mechanism) pointing back to its source;
4. **the keystone holds** — the worker's prompt still carries the whole spec, every capability.
"""
from __future__ import annotations

import os

from .harness import ok


def check(root: str) -> None:
    from .. import depth, graph, spec, worker

    print("\nslice 10 — acceptance check  (retire the worker.DEPTH smell)\n")

    # ── 1. the frozen copy is gone ────────────────────────────────────────────────────────
    ok(not hasattr(worker, "DEPTH"),
       "the frozen worker.DEPTH constant is retired — no hand-compression of aposd.md in code")

    # Plant a controlled aposd.md in the root: its two canonical lists, one item carrying a
    # sentinel, so a derived render must reproduce THIS source (not a frozen copy, not the
    # package fallback). Same idiom as slice 9 planting decision files into the root.
    NONCE = "ZQX-planted-principle"
    aposd = (
        "# A Philosophy of Software Design — synthesis (planted)\n\n"
        "## 2. The red flags\n\nFaithful list:\n\n"
        "1. **Shallow module** — interface nearly as complex as the implementation.\n"
        "2. **Information leakage** — the same knowledge in two places.\n\n"
        "(Also recurring: pass-through variables.)\n\n"
        "## 3. The design principles\n\nFaithful set:\n\n"
        "1. Modules should be deep.\n"
        f"2. {NONCE} — pull complexity downward.\n"
    )
    src = os.path.join(root, "research", "aposd.md")
    graph.atomic_write(src, aposd)

    # ── 2. the grounding is DERIVED from aposd.md, not authored ───────────────────────────
    g = depth.disciplines(root)
    ok("Shallow module" in g and "Information leakage" in g,
       "the depth grounding renders the red flags from aposd.md — derived, not a frozen copy")
    ok("Modules should be deep" in g and NONCE in g,
       "it renders the design principles too, including a planted sentinel — single-sourced")
    ok("**" not in g,
       "the render is clean prose, a true render of the source's lists, not raw markdown")

    # editing the one source changes the grounding in the same breath — there is no second copy
    graph.atomic_write(src, aposd.replace(NONCE, "EDITED-" + NONCE))
    ok("EDITED-" + NONCE in depth.disciplines(root),
       "editing aposd.md changes the grounding at once — drift between source and copy is impossible")

    # ── 3. the worker carries the disciplines every episode — now wired through the render ──
    ask = graph.file_intent("any worker episode")
    ctx = worker.context(ask, root)
    text = worker.prompt(ask, ctx)
    ok("Shallow module" in text and "Modules should be deep" in text,
       "the worker's prompt carries the depth disciplines by construction — the slice-7 defense, derived")
    ok(ctx.depth == depth.disciplines(root) and ctx.depth in text,
       "the disciplines are assembled into the context like the spec slice — no path runs a worker without them")

    # ── 4. the keystone: the worker still holds the WHOLE spec ─────────────────────────────
    caps = spec.read_spec(root).capabilities
    ok(caps and all(c.name in text for c in caps),
       "the worker still holds every capability — the slice-4 whole-spec keystone is untouched")

    # ── 5. the depth SKILL artifact — same source, materialized for the seam ──────────────
    sk = depth.skill(root)
    ok(sk.startswith("---") and "name: depth" in sk,
       "the depth skill is a progressive-disclosure SKILL.md — metadata, then the disciplines")
    ok("Shallow module" in sk and "Modules should be deep" in sk and "research/aposd.md" in sk,
       "the skill is single-sourced from aposd.md and points back to it for the full synthesis")
    path = depth.materialize(root)
    ok(os.path.isfile(path) and open(path).read() == sk,
       "the skill artifact materializes on disk — the one new mechanism, a static file a harness loads")
