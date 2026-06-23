"""Slice 8 — parallelism re-grounded: design-it-twice, the judgment use of the fence.

Acceptance (spec §9.8): concurrent workers advance one tree in isolation and each folds its
delta; and a load-bearing interface decision can be designed twice in parallel and compared.
This check drives both over the real tree, real fences, and a real node-record write,
deterministically with scripted transports — pinning the four properties that define the judgment use:

1. **concurrent isolation composes** — two workers hold two distinct fences at once, neither's
   material reaches the main line, and each folds its own delta into the one spec;
2. **the decision is designed twice, isolated** — a candidate per brief, each in its own fence,
   each design fenced from its siblings and the main line;
3. **the selection is machine-side** — the architect picks/hybridizes on depth/locality/seam and
   records a structured design-decision on the contest node; with no stake it raises no operator card,
   and the raw candidate designs reach no card or render beyond that node record;
4. **a stake-bearing difference re-enters grilling** — it raises a decision card parented to the
   node (the standing-guard floor, §5.1), carrying only the architect-authored stake.
"""
from __future__ import annotations

import json
import os
import subprocess

from .harness import LOOP, ok, scripted


def check(root: str) -> None:
    from .. import communication, design, tree, render, spec, worker

    print("\nslice 8 — acceptance check  (parallelism re-grounded: design-it-twice)\n")

    coherent = lambda: scripted(json.dumps({"coherent": True, "say": "it landed.", "card": None}))
    loop = LOOP                                      # the executable red→green loop the gate runs (keystone)

    def built(cap: str, report: str) -> str:
        return json.dumps({"report": report,
                           "delta": f"## ADDED — {cap}\n### Requirement: {cap} holds\n"
                                    f"The {cap} capability MUST hold.\n#### Scenario: s\n"
                                    f"- WHEN x\n- THEN y\n",
                           "loop": loop})

    def staged(text: str, cap: str, root: str) -> tree.Node:
        ask = tree.file_intent(text)
        tree.approve(tree.raise_card(
            f"contract.\n\ndelta:\n## ADDED — {cap}\n### Requirement: {cap} holds\n"
            f"The {cap} capability MUST hold.\n#### Scenario: s\n- WHEN x\n- THEN y\n",
            kind="decide", parent=ask.id))
        worker.worktree(ask, root)
        tree.dispatch(ask)
        return ask

    def log(branch: str) -> str:
        return subprocess.run(["git", "log", "--oneline", branch], cwd=root,
                              capture_output=True, text=True).stdout

    # ── 1. concurrent workers advance one tree in isolation, each folding its delta ──
    a = staged("concurrent work A", "alpha", root)
    b = staged("concurrent work B", "beta", root)
    ta, tb = worker._tree_path(a, root), worker._tree_path(b, root)
    ok(os.path.isdir(ta) and os.path.isdir(tb) and ta != tb,
       "two workers hold two distinct fences at once — concurrent, isolated")

    ra = worker.apply(a, scripted(built("alpha", "built A")), root)
    rb = worker.apply(b, scripted(built("beta", "built B")), root)
    ok("worker: result" in log(f"worker/{a.id}") and "worker: result" in log(f"worker/{b.id}"),
       "each worker's commit reaches the record on its own branch")
    off_main = subprocess.run(["git", "cat-file", "-e", "HEAD:RESULT.md"], cwd=root,
                              capture_output=True, text=True).returncode
    ok(off_main != 0, "neither fence's material reaches the main line — the fence holds for both")

    communication.integrate(a, ra, coherent(), root)
    communication.integrate(b, rb, coherent(), root)
    sp = spec.read_spec(root)
    ok(sp.capability("alpha") is not None and sp.capability("beta") is not None,
       "each worker folds its own delta into the one spec — concurrent advance, no interference")
    worker.teardown(a, root)
    worker.teardown(b, root)

    # ── 2. a load-bearing interface decision is designed twice, in isolation ──
    briefs = [("minimal", "Minimize the interface; pull complexity down inside."),
              ("flexible", "Maximize flexibility; make future variation cheap.")]

    def design_json(brief: str, hides: str) -> str:
        return json.dumps({"interface": f"{brief}: one entry over the hidden work",
                           "hides": hides, "seam": f"the {brief} seam, where the model varies",
                           "depth": "deleting it scatters the work across callers — it earns its keep"})

    dec = tree.file_intent("the shape of the candidate-comparison interface")
    cands = design.contest(dec, briefs, scripted(
        design_json("minimal", "the parallel fences"),
        design_json("flexible", "a pluggable comparison")), root)
    ok(len(cands) == 2 and cands[0].brief == "minimal" and cands[1].brief == "flexible",
       "the decision is designed twice — one candidate per brief")
    ok(cands[0].worktree != cands[1].worktree and all(os.path.isdir(c.worktree) for c in cands),
       "each candidate designs in its own fence — distinct, isolated worktrees coexisting")
    for c in cands:
        ok(f"candidate: {c.brief}" in log(f"worker/{dec.id}-{c.brief}"),
           f"the {c.brief} candidate's design commit is on its own branch")
    off_main = subprocess.run(["git", "cat-file", "-e", "HEAD:DESIGN.md"], cwd=root,
                              capture_output=True, text=True).returncode
    ok(off_main != 0, "the candidate designs are fenced from the main line")

    # the architect compares on depth/locality/seam — by construction in its selection prompt
    ok(all(ax in design._select_prompt(dec, cands) for ax in ("DEPTH", "LOCALITY", "SEAM PLACEMENT")),
       "the architect compares candidates on depth, locality, and seam placement by construction")
    for c in cands:
        worker.teardown(dec, root, tag=c.brief)

    # the selection is machine-side: a pick, recorded as a structured design-decision on the node
    sel = design.select(dec, cands, scripted(json.dumps({
        "chosen": "minimal", "hybrid": False,
        "reasoning": "minimal is deepest — the most behind the smallest interface; locality holds",
        "comparison": {"minimal": "deepest", "flexible": "wider surface for unproven variation"},
        "stake": None})))
    ok(sel.chosen == "minimal" and not sel.stake, "the architect picks machine-side, no stake")
    rec = design.record(dec, sel, root)
    text = open(rec).read()
    ok("design-decision:" in text and "→ minimal" in text and "[machine]" in text,
       "the pick is recorded as a structured design-decision on the node — the machine-side home")

    # ── 3. machine-side end to end: no stake → no operator card; raw designs do not leak ──
    SENTINEL = "<<RAW CANDIDATE DESIGN — machine-side only>>"
    dec2 = tree.file_intent("another load-bearing interface")
    before = len(tree.cards())
    sel2 = design.design_twice(dec2, briefs, scripted(
        design_json("minimal", SENTINEL),
        design_json("flexible", "the other shape"),
        json.dumps({"chosen": "hybrid", "hybrid": True,
                    "reasoning": "a hybrid is deepest across depth, locality, and seam",
                    "comparison": {"minimal": "deep", "flexible": "flexible"}, "stake": None})), root)
    ok(sel2.card is None and len(tree.cards()) == before,
       "no stake-bearing difference → no operator card; the pick stays machine-side")
    ok(not any(os.path.isdir(worker._tree_path(dec2, root, tag=b)) for b, _ in briefs),
       "the candidate fences are scratch — torn down once the pick is recorded")

    frame = "".join(t for row in render.main_body(tree.read_tree(), -1) for t, _s in row)
    nodefiles = ""
    for top in ("work",):                                    # tree nodes only — not the scratch fence
        for dp, dirs, fs in os.walk(os.path.join(root, top)):
            if "worktrees" in dirs:
                dirs.remove("worktrees")
            nodefiles += "".join(open(os.path.join(dp, fn)).read()
                                 for fn in fs if fn in ("intent.md", "grilling.md"))
    cards_text = "".join(c.text for c in tree.read_tree())
    ok(SENTINEL not in frame and SENTINEL not in nodefiles and SENTINEL not in cards_text,
       "the raw candidate designs reach no card, render, or node — only the machine-side record")

    # ── 4. a stake-bearing difference re-enters grilling (the standing-guard floor, §5.1) ──
    STAKE = "the two shapes differ in whether a re-opened contest is visible to you — your call"
    dec3 = tree.file_intent("an interface whose shapes differ behaviorally")
    sel3 = design.design_twice(dec3, briefs, scripted(
        design_json("minimal", SENTINEL),
        design_json("flexible", "the other shape"),
        json.dumps({"chosen": "flexible", "hybrid": False,
                    "reasoning": "flexible wins, but the shapes differ where you have a stake",
                    "comparison": {"minimal": "deep", "flexible": "deeper here"},
                    "stake": STAKE})), root)
    ok(sel3.card is not None and sel3.card.kind == "decide" and sel3.card.parent == dec3.id,
       "a stake-bearing difference re-enters grilling — a decision card parented to the node")
    ok(STAKE in sel3.card.text and SENTINEL not in sel3.card.text,
       "only the architect-authored stake crosses to the operator — never the raw candidate designs")
