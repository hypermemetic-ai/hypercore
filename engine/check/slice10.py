"""Slice 10 — item 2, build step 1: retire the worker.DEPTH smell (ADR 0009 §5 step 1).

Acceptance (ADR 0009): the worker's depth grounding is no longer a frozen
hand-compression of `spec/depth.md` in a Python constant — it is **rendered from spec/depth.md,
single-sourced**, so the moment the synthesis changes the grounding changes with it. A `depth`
**skill** artifact carries the same disciplines for the parked harness seam. The worker's
whole-spec grounding is untouched (the slice-4 keystone), and the worker still carries the depth
disciplines every episode (the slice-7 proactive defense), now *derived* rather than copied.

This drives the real render over a **planted** spec/depth.md — the harness writes a controlled
source into its root the way slice 9 plants decision files — pinning four properties:

1. **the frozen copy is gone** — `worker.DEPTH` no longer exists;
2. **derived, not authored** — the worker's prompt-side grounding and the skill both render the
   planted disciplines, and editing the planted spec/depth.md changes them (drift is impossible);
3. **single source, two channels** — prompt grounding and skill artifact render from the one file,
   and the skill materializes on disk (the one new mechanism) pointing back to its source;
4. **the keystone holds** — the worker's prompt still carries the whole spec, every capability.
"""
from __future__ import annotations

import os

from .harness import ok


def check(root: str) -> None:
    from .. import graph, methodology, spec, worker

    print("\nslice 10 — acceptance check  (depth is a capability, foregrounded for the worker)\n")

    # ── 1. the frozen copy is gone ────────────────────────────────────────────────────────
    ok(not hasattr(worker, "DEPTH"),
       "the frozen worker.DEPTH constant is retired — no hand-compression of the disciplines in code")

    # Plant a controlled depth capability slice carrying a sentinel discipline, so a derived render
    # (the worker's prompt and the depth skill) must reproduce THIS slice — the slice-12 idiom.
    NONCE = "ZQX-planted-principle"
    planted = (
        "# depth\n\n"
        f"Planted depth overview — {NONCE}: build deep modules behind small interfaces.\n\n"
        "### Requirement: a planted depth discipline\n"
        f"The worker MUST hold the planted discipline — {NONCE}-stmt — building deep up front.\n"
        "#### Scenario: a module is built\n"
        "- WHEN a worker builds a module\n- THEN the planted discipline applies\n"
    )
    src = spec.cap_path("depth", root)
    graph.atomic_write(src, planted)

    # ── 2. depth is a capability in the model, like the others (ADR 0019) ──────────────────
    ok(spec.read_spec(root).capability("depth") is not None,
       "depth is a capability segment — read from spec/depth.md by content, no longer a special type")

    # ── 3. the worker's prompt foregrounds the depth disciplines every episode ─────────────
    ask = graph.file_intent("any worker episode")
    text = worker.prompt(ask, worker.context(ask, root))
    ok(NONCE in text and NONCE + "-stmt" in text,
       "the worker's prompt foregrounds the depth capability by construction — the slice-7 defense, derived")

    # editing the one source changes the worker's grounding at once — there is no second copy
    graph.atomic_write(src, planted.replace(NONCE, "EDITED-" + NONCE))
    text2 = worker.prompt(ask, worker.context(ask, root))
    ok("EDITED-" + NONCE in text2,
       "editing the depth slice changes the worker's grounding at once — drift between source and copy is impossible")

    # ── 4. the keystone: the worker still holds the WHOLE spec ─────────────────────────────
    caps = spec.read_spec(root).capabilities
    ok(caps and all(c.name in text2 for c in caps),
       "the worker still holds every capability — the slice-4 whole-spec keystone is untouched")

    # ── 5. the depth SKILL renders through the standard methodology seam ───────────────────
    sk = methodology.skill("depth", root)
    ok(sk.startswith("---") and "name: depth" in sk and "EDITED-" + NONCE in sk,
       "the depth skill renders from the same slice through the methodology seam — single-sourced, like the others")
    path = methodology.materialize("depth", root)
    ok(os.path.isfile(path) and open(path).read() == sk,
       "the depth skill artifact materializes on disk — a render of its slice, no second copy")
