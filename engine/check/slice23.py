"""Slice 23 — the OMP worker seam (role-assembly step 5): the worker runs at its fence, the long
history and grounds of past decisions greped just-in-time from `work/archive/`, the spec preloaded whole.

Acceptance (spec/worker, role-assembly steps 5–6): the worker's model transport runs with
its working directory = its worktree, so the harness auto-loads the fence's anchor and discovers its
skills and the worker greps `work/archive/` for past grounds from its own checkout; that history is
dropped from the prompt (greped just-in-time), while the spec capabilities, the glossary, and the depth
disciplines stay **preloaded whole** — the whole-picture keystone is intact. The scheduler forwards the
live injection point untouched, so the worker binds its fence while the architect's integrate uses the
repo-root call.

The OMP/GPT model **flip** (step 6) is the watched live experiment plus a spend decision, recorded in
`work/role-assembly/`, never faked here (the honest harness limit, slice-7-F1 precedent): the binary
and model the worker targets are asserted as scaffold — that they are named in one place and bound at
the fence — not run against a live model.
"""
from __future__ import annotations

import json
import os

from .harness import ok


def check(root: str) -> None:
    from .. import tree, grill, schedule, spec, transport, worker

    print("\nslice 23 — acceptance check  (the OMP worker seam: the worker runs at its fence, "
          "past grounds greped JIT from work/archive/)\n")

    os.environ["ENGINE_ROOT"] = root        # re-establish the shared root (slice 16 ran on its own)

    # a real archived node in the checkout, carrying a sentinel — the past-decision history the worker
    # must NOT inline; it greps work/archive/ for it just-in-time as the change needs
    TAIL = "<<ARCHIVE-GROUNDS — long history, greped JIT from work/archive/, never preloaded into the prompt>>"
    tree.atomic_write(os.path.join(root, "work", "archive", "0099-past-decision", "intent.md"),
                       f"# a past decision — its long grounds\n\n{TAIL}\n")

    handed = ("## ADDED — worker\n### Requirement: the worker fences its working directory\n"
              "The worker MUST run at its fence.\n#### Scenario: s\n- WHEN it builds\n- THEN it is fenced\n")
    ask = tree.file_intent("a change the worker builds at its fence")
    tree.atomic_write(os.path.join(ask.path, "grilling.md"),
                       grill._render(grill._Pass(0, [], "Build it at the fence.", handed)))

    ctx = worker.context(ask, root)
    prompt = worker.prompt(ask, ctx, root)

    # GREEN: the whole-picture keystone is intact — the spec is preloaded whole
    allcaps = {c.name for c in spec.read_spec(root).capabilities}
    ok(set(ctx.names) == allcaps and {"depth", "tree"} <= set(ctx.names),
       "the worker still holds the whole spec — every capability preloaded (the whole-picture keystone)")
    ok("### Requirement:" in prompt and "throwaway conversation" in prompt,
       "the spec capabilities and the glossary stay preloaded whole in the prompt")
    ok("depth standards" in prompt,
       "the depth standards stay foregrounded in the prompt — held every episode")

    # GREEN: the long history/grounds of past decisions is NOT inlined — it is greped JIT from the checkout
    ok(TAIL not in prompt,
       "the long history of past decisions is not inlined into the prompt — it carries no whole-picture stake")
    ok("work/archive/" in prompt and "spec/decisions/" not in prompt and "just-in-time" in prompt,
       "the prompt points the worker at work/archive/ in its checkout for a just-in-time grep, not spec/decisions/")

    # RED: the retired shape inlined the history; show that shape fails the gate the GREEN passes
    inlines_tail = lambda p: TAIL in p
    prefix_prompt = prompt + f"\n\nThe decisions:\n{TAIL}\n"   # the retired preloaded-decisions block
    ok(inlines_tail(prefix_prompt) and not inlines_tail(prompt),
       "RED→GREEN: the pre-fix prompt inlined the history; the live prompt points at work/archive/ instead")

    # the worker's live transport binds cwd = the fence — the scaffold §6 asserts without a live model
    fence = worker.worktree(ask, root)
    bound = transport.worker_transport(fence)
    ok(getattr(bound, "cwd", None) == fence,
       "the worker transport binds its working directory to the fence — it runs at its own checkout")
    argv = transport.worker_argv("PROMPT")
    ok(transport.WORKER_CMD in argv and transport.WORKER_MODEL in argv,
       "the worker targets its own harness binary and model, named in one place (the OMP/GPT flip point)")

    # apply, given no injected transport, runs the worker at its fence — asserted via a spy, no live model
    seen: dict[str, str] = {}

    def spy(cwd: str):
        seen["cwd"] = cwd
        return lambda _p: json.dumps({"report": "built it", "delta": handed})

    saved, worker.worker_transport = worker.worker_transport, spy
    try:
        worker.apply(ask, None, root)                 # transport=None → the live fence-binding path, spied
    finally:
        worker.worker_transport = saved
    ok(seen.get("cwd") == fence,
       "apply with no injected transport runs the worker at cwd = its fence (step 5, not faked)")

    # the scheduler forwards the live injection point untouched (None) so the worker binds its fence
    ok(schedule.Scheduler().transport is None,
       "the scheduler no longer collapses the live worker transport to the architect's repo-root call")

    worker.teardown(ask, root)
