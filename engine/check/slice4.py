"""Slice 4 — workers, with spec-scoped context: the fence, the routing, the hand-back.

Acceptance (spec/worker, ADR 0003): a worker is grounded in its capability's spec slice by
construction — holding the whole spec, not confined to the touched slice (ADR 0009); it
runs fenced in its own git worktree; and its raw output reaches the operator through no
path — the architect authors every operator-facing word and folds the refined delta.
Drives propose→apply→archive end to end with scripted transports over the real graph and a
real worktree.
"""
from __future__ import annotations

import json
import os
import subprocess

from .harness import ok, scripted


def check(root: str) -> None:
    from .. import conversation, delta, graph, grill, render, spec, worker

    print("\nslice 4 — acceptance check  (workers, with spec-scoped context)\n")

    # the propose-stage product, ratified: a spawned ask carrying a contract and a handed
    # delta that touches two existing capabilities (worker, conversation).
    handed = (
        "## ADDED — worker\n"
        "### Requirement: a worker checkpoints its progress\n"
        "The worker MUST record a checkpoint the architect can read.\n"
        "#### Scenario: a checkpoint\n- WHEN a worker pauses\n- THEN its progress is recorded\n\n"
        "## ADDED — conversation\n"
        "### Requirement: the architect names the worker in the record\n"
        "The architect MUST record which worker a result came from.\n"
        "#### Scenario: a hand-off\n- WHEN a result is archived\n- THEN the worker is named\n")
    ask = graph.file_intent("give workers a progress checkpoint")
    graph.atomic_write(os.path.join(ask.path, "grilling.md"), grill._render(grill._Pass(  # the ratified contract
        0, [], "Workers checkpoint progress, and the record names the worker.", handed)))

    # 1. the grounding, by construction: the whole spec, with the touched capabilities marked
    # as grounding — the worker is NOT slice-confined (ADR 0009)
    ctx = worker.context(ask)
    allcaps = {c.name for c in spec.read_spec(root).capabilities}
    ok(ctx.touched == {"worker", "conversation"},
       f"the touched capabilities are the worker's grounding ({', '.join(sorted(ctx.touched))})")
    ok(set(ctx.names) == allcaps and {"self-model", "graph"} <= set(ctx.names),
       "the context contains the whole spec, not only the touched slice — the worker is not slice-confined")
    prompt = worker.prompt(ask, ctx)
    ok("### Requirement:" in prompt and "throwaway operator-facing vessel" in prompt,
       "the grounding carries the touched capability specs and the glossary, by construction")
    ok("import " not in prompt and "curses" not in prompt,
       "the worker is grounded in the spec, never the code")

    # the keystone (ADR 0009): a handed delta that mis-names a capability does not
    # shrink the worker's context — it still holds the whole spec, so the rescan can catch the
    # mis-mapping. A slice-confined worker (context = {graph}) would have been blind to it.
    mis = graph.file_intent("a change whose handed delta mis-maps the capability")
    graph.atomic_write(os.path.join(mis.path, "grilling.md"), grill._render(grill._Pass(
        0, [], "mis-mapped contract.", "## ADDED — graph\n"
        "### Requirement: a mis-named requirement\nx\n#### Scenario: s\n- WHEN a\n- THEN b\n")))
    mctx = worker.context(mis)
    ok(mctx.touched == {"graph"} and {"worker", "conversation"} <= set(mctx.names),
       "a mis-mapped delta keeps the whole spec in the worker's context — its rescan can catch "
       "what the delta mis-named, where a slice-confined worker would be blind")

    # 2. the fence: a real worktree, separate from the main line
    tree = worker.worktree(ask, root)
    ok(os.path.isdir(tree) and os.path.join("work", "worktrees") in tree and tree != root,
       "the worker gets its own worktree under work/worktrees, separate from the main tree")
    listed = subprocess.run(["git", "worktree", "list", "--porcelain"], cwd=root,
                            capture_output=True, text=True).stdout
    ok(ask.id in listed, "the worktree is a real, registered git worktree")
    graph.delegate(ask)
    ok(graph.find(ask.id).is_live and ask.id in [n.id for n in graph.work()],
       "the delegated work goes live on the work view while the worker runs")

    # the worker builds and hands back a machine-facing result carrying raw prose
    SENTINEL = "<<RAW WORKER RAMBLE — walls of rambling text>>"
    result = worker.apply(ask, scripted(json.dumps({
        "report": "Implemented the checkpoint behind a red→green loop. " + SENTINEL,
        "delta": handed,
        "loop": {"command": "python3 -m engine --check",
                 "red": "asserted the checkpoint was absent — the loop failed",
                 "green": "added the checkpoint — the loop passed"}})), root)
    ok(SENTINEL in result.report, "the worker produced a raw, machine-facing report")

    # its own commit reached the record in its own tree, fenced from the main line
    on_branch = subprocess.run(["git", "log", "--oneline", f"worker/{ask.id}"], cwd=root,
                               capture_output=True, text=True).stdout
    off_main = subprocess.run(["git", "cat-file", "-e", "HEAD:RESULT.md"], cwd=root,
                              capture_output=True, text=True).returncode
    ok("worker: result" in on_branch and off_main != 0,
       "the worker's commit is in the record on its own branch, absent from the main line")

    # 3. archive: the architect coherence-checks and folds; the raw report leaks nowhere
    reply = conversation.integrate(ask, result, scripted(json.dumps({
        "coherent": True,
        "say": "Workers now checkpoint progress; it landed.",
        "card": None})), root)
    ok(reply.done, "the architect judged the result coherent and archived it")
    ok(SENTINEL not in reply.say, "the architect authored its own words, not the raw report")

    sp = spec.read_spec(root)
    ok(sp.capability("worker").requirement("a worker checkpoints its progress") is not None
       and sp.capability("conversation").requirement(
           "the architect names the worker in the record") is not None,
       "the refined delta folded into the spec in the same act")

    # the raw report has no operator-facing or durable home anywhere
    frame = "".join(t for row in render.main_body(graph.read_graph(), -1) for t, _s in row)
    nodefiles = ""
    for top in ("work",):                                    # graph nodes only — not the scratch fence
        for dp, dirs, fs in os.walk(os.path.join(root, top)):
            if "worktrees" in dirs:
                dirs.remove("worktrees")
            nodefiles += "".join(open(os.path.join(dp, fn)).read()
                                 for fn in fs if fn in ("intent.md", "grilling.md"))
    cards_text = "".join(c.text for c in graph.read_graph())
    ok(SENTINEL not in frame and SENTINEL not in nodefiles and SENTINEL not in cards_text,
       "the raw worker report reaches no card, no render, and no node — the leak path does not exist")

    ok(graph.find(ask.id).state == graph.DONE and ask.id not in [n.id for n in graph.work()],
       "the integrated work folded out of the work view")

    worker.teardown(ask, root)
    ok(not os.path.isdir(tree), "the fence is torn down once the result integrates")

    # the fold can grow a brand-new capability — the machinery the worker capability needed
    delta.fold(delta.parse(
        "## ADDED — scheduling\n"
        "### Requirement: the scheduler cuts the next seam while work remains\n"
        "The scheduler MUST keep building while any unblocked work remains.\n"
        "#### Scenario: work remains\n- WHEN a ready leaf exists\n- THEN a session takes it"),
        root)
    ok(spec.read_spec(root).capability("scheduling") is not None,
       "an ADDED requirement in an absent capability creates that capability on fold")
