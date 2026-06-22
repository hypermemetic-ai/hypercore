"""Slice 2 — the self-model: the living spec, the delta, the fold, the operator view.

Acceptance (spec §9.2): a behavior-changing graph carries a delta, folds, and the delta
is present in spec/; a missing/mismatched delta fails to fold; the operator view renders
the vision (from intent.md) beside the as-built and gap from the spec. Run against
hypercore's own self-model, copied in.
"""
from __future__ import annotations

import os
import shutil
import subprocess

from .harness import ok


def check(root: str) -> None:
    from .. import delta, graph, spec, view

    src = graph._DEFAULT_ROOT
    shutil.copytree(os.path.join(src, "spec"), os.path.join(root, "spec"))
    shutil.copyfile(os.path.join(src, "intent.md"), os.path.join(root, "intent.md"))
    shutil.copyfile(os.path.join(src, "glossary.md"), os.path.join(root, "glossary.md"))
    graph.commit([os.path.join(root, "spec"), os.path.join(root, "intent.md"),
                  os.path.join(root, "glossary.md")],
                 "seed: hypercore's own spec and vision")

    print("\nslice 2 — acceptance check  (self-hosted on hypercore's own spec)\n")

    # the seed spec self-hosts: distilled from intent.md, capability-segmented
    sp = spec.read_spec()
    names = [c.name for c in sp.capabilities]
    ok({"interface", "graph", "queue", "conversation", "self-model"} <= set(names),
       f"the seed spec carries hypercore's capabilities ({', '.join(names)})")
    ok("throwaway operator-facing vessel" in sp.glossary,
       "the glossary defines thread as the throwaway operator-facing vessel")
    ok("Open question: the name" in sp.glossary,
       "the glossary flags the open 'operator view' naming question")

    # a behavior-changing graph carries a delta, folds, and the delta lands in spec/
    d = delta.parse(
        "# delta — the queue order is the machine's claim\n\n"
        "## ADDED — queue\n"
        "### Requirement: the order is the machine's claim about attention\n"
        "The order MUST carry each card's cost of delay.\n\n"
        "#### Scenario: a card waits\n"
        "- WHEN a decision is shown\n"
        "- THEN it wears what its delay costs\n")
    ok(not d.trivial and d.ops[0].verb == "ADDED", "a delta parses its ADDED op")
    delta.fold(d)
    landed = spec.read_spec().capability("queue").requirement(
        "the order is the machine's claim about attention")
    ok(landed is not None, "folding the delta lands the requirement in spec/")

    # a mismatched delta cannot fold (MODIFIES an absent requirement)
    try:
        delta.fold(delta.parse("## MODIFIED — queue\n### Requirement: nonexistent\nx\n"))
        ok(False, "a mismatched delta fails to fold")
    except delta.CannotFold:
        ok(True, "a mismatched delta fails to fold")

    # a missing delta cannot fold; a trivial delta folds and applies nothing
    try:
        delta.fold(None)
        ok(False, "a missing delta fails to fold")
    except delta.CannotFold:
        ok(True, "a missing delta fails to fold")
    before = [r.name for r in spec.read_spec().capability("queue").requirements]
    delta.fold(delta.parse("# delta — trivial (no behavior change)"))
    after = [r.name for r in spec.read_spec().capability("queue").requirements]
    ok(before == after, "a trivial delta folds and changes nothing")

    # the operator view renders vision (from intent.md) beside as-built and gap
    v = view.operator_view()
    ok(any("legibility" in line.lower() for line in v.vision),
       "the view renders the vision from intent.md")
    ok(any("queue" in line for line in v.asbuilt) and v.gap,
       "the view renders the as-built and the gap from the spec")
    queue_node = next(c for c in v.children if c.title == "queue")
    ok("the order is the machine's claim about attention" in queue_node.asbuilt,
       "the view's as-built is derived — the folded requirement appears, unedited")

    # the per-capability vision is a DERIVED binding (ADR 0020), not a hand-typed map: a capability
    # declares the intent it realizes in its own spec slice (`<!-- vision: ... -->`), so a newly
    # carved capability gets its vision with NO edit to view.py — and one that declares none (pure
    # machinery) correctly shows no vision, distinct from a bug.
    graph.atomic_write(os.path.join(root, "spec", "lighthouse.md"),
        "# lighthouse\n<!-- vision: legibility -->\n\nA planted capability.\n\n"
        "### Requirement: it shines\n#### Scenario: night\n- WHEN dark\n- THEN light\n")
    graph.atomic_write(os.path.join(root, "spec", "boiler.md"),
        "# boiler\n\nA planted machinery capability, declaring no vision.\n\n"
        "### Requirement: it heats\n#### Scenario: cold\n- WHEN cold\n- THEN warm\n")
    v2 = view.operator_view()
    lh = next(c for c in v2.children if c.title == "lighthouse")
    bo = next(c for c in v2.children if c.title == "boiler")
    ok(any("legibility" in s.lower() for s in lh.vision),
       "a newly-carved capability's declared vision is derived — no edit to view.py")
    ok(bo.vision == [],
       "a capability that declares no vision shows none — pure machinery, distinct from a bug")

    # every requirement carries at least one scenario — the mechanical floor of requirement↔scenario
    # coverage (ADR 0020). The deeper overclaim (a requirement whose prose claims more than its
    # scenarios cover — the atomic-fold case) stays the model-driven judgment scan, not-yet-built.
    uncovered = [r.name for c in spec.read_spec().capabilities
                 for r in c.requirements if not r.scenarios]
    ok(not uncovered, f"every requirement carries a scenario (uncovered: {uncovered})")

    # the fold is committed to the durable record, atomic with the spec change
    log = subprocess.run(["git", "log", "--oneline"], cwd=root,
                         capture_output=True, text=True).stdout
    ok("fold:" in log, "folding commits the spec change to the durable record")
