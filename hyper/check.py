"""Slice 1 acceptance check — the operator's path, run headlessly.

It drives operator ↔ conversationalist ↔ queue with a *scripted* transport (no
LLM, so the loop is deterministic and fast) over the *real* graph, and asserts
the graph — not a story. The live conversationalist is exercised by running the
window; this is the evidence you can watch.

    python3 -m hyper --check

Acceptance (spec §9.1): open a thread, converse, file intent that lands as work
on the graph (or get a question answered), the thread closes on satisfaction,
and durability lives on the graph — re-reading shows the work, no resumed thread.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile

_fails = 0


def ok(cond: bool, label: str) -> None:
    global _fails
    mark = "PASS" if cond else "FAIL"
    if not cond:
        _fails += 1
    print(f"  [{mark}] {label}")


def scripted(*replies):
    q = list(replies)
    return lambda _prompt: q.pop(0)


def run() -> int:
    root = tempfile.mkdtemp(prefix="hyper-check-")
    os.environ["HYPER_ROOT"] = root
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "check@hypercore"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "check"], cwd=root, check=True)

    from . import conversation, graph, render
    from .conversation import Thread, speak, explain

    print(f"\nslice 1 — acceptance check  ({root})\n")

    # 1. file intent: it lands as standing work, the thread closes on satisfaction.
    # (The ask is below the floor — its second scripted reply grills nothing — so it
    # files straight through; grilling itself is slice 3's check.)
    t = Thread()
    r = speak(t, "download the new berserk episodes", scripted(
        '{"say":"Filing that as standing work.","file":"download the new Berserk '
        'episodes","done":true}',
        '{"questions":[]}'))
    ok(r.filed is not None, "speaking files intent")
    ok(not t.open, "the thread closes on satisfaction")
    ok(len(graph.standing()) == 1, "the intent is standing work on the graph")

    # 2. durability is the graph's, not the thread's: re-read fresh, no resume
    fresh = graph.read_graph()
    ok(len(graph.standing(fresh)) == 1, "re-reading the graph shows the work")
    ok(not os.path.isdir(os.path.join(root, "threads")),
       "no thread is persisted — durability lives only on the graph")

    # 3. a question is answered, nothing is filed
    before = len(graph.read_graph())
    t2 = Thread()
    r2 = speak(t2, "what are you?", scripted(
        '{"say":"I am hypercore\'s conversationalist.","done":true}'))
    ok(r2.filed is None and r2.card is None, "a question files nothing")
    ok(not t2.open and len(graph.read_graph()) == before, "the question thread closes, graph unchanged")

    # 4. a real judgment returns to the queue as a card
    t3 = Thread()
    r3 = speak(t3, "where should the intake box pull from?", scripted(
        '{"say":"Put that to your queue.","card":"the intake box pulls torrents '
        'from nyaa","done":true}'))
    ok(r3.card is not None and len(graph.cards()) == 1, "a judgment raises a card on the queue")
    card = graph.cards()[0]
    ok(card.machine and card.is_card, "the card is machine-owned and awaiting the operator")

    # 5. explain tells the story; the card stays on the queue
    story = explain(card, scripted('{"say":"nyaa carries the releases; lean nyaa."}'))
    ok(bool(story) and len(graph.cards()) == 1, "explain returns a story and leaves the card standing")

    # 6. approve endorses and the card leaves the queue
    graph.approve(card)
    ok(len(graph.cards()) == 0, "approve clears the card from the queue")
    endorsed = graph.find(card.id)
    ok(endorsed is not None and not endorsed.machine, "the endorsed node drops its [machine] marker")

    # 7. cut removes the words: the node file leaves
    doomed = graph.raise_card("a statement to cut")
    ok(len(graph.cards()) == 1, "a fresh card appears on the queue")
    graph.cut(doomed)
    ok(graph.find(doomed.id) is None, "cut removes the node from the graph")

    # 8. the render is pure and total over this state (no TTY)
    rows = render.main_body(graph.read_graph(), 0)
    ok(isinstance(rows, list) and rows and rows[0][0][0] == "hypercore", "the main screen renders")

    # 9. durable state is version-controlled
    log = subprocess.run(["git", "log", "--oneline"], cwd=root,
                         capture_output=True, text=True).stdout.strip().splitlines()
    ok(len(log) >= 4, f"every act committed to the durable record ({len(log)} commits)")

    _slice2(root)
    _slice3(root)

    print()
    if _fails:
        print(f"  {_fails} FAILED\n")
        return 1
    print("  all checks pass — slices 1–3 meet their acceptance checks\n")
    return 0


def _slice2(root: str) -> None:
    """Acceptance (spec §9.2): a behavior-changing graph carries a delta, folds,
    and the delta is present in spec/; a missing/mismatched delta fails to fold;
    the operator view renders the vision (from intent.md) beside the as-built and
    gap from the spec. Run against hypercore's own self-model, copied in."""
    from . import delta, graph, spec, view

    src = graph._DEFAULT_ROOT
    shutil.copytree(os.path.join(src, "spec"), os.path.join(root, "spec"))
    shutil.copyfile(os.path.join(src, "intent.md"), os.path.join(root, "intent.md"))
    graph.commit([os.path.join(root, "spec"), os.path.join(root, "intent.md")],
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

    # the fold is committed to the durable record, atomic with the spec change
    log = subprocess.run(["git", "log", "--oneline"], cwd=root,
                         capture_output=True, text=True).stdout
    ok("fold:" in log, "folding commits the spec change to the durable record")


def _slice3(root: str) -> None:
    """Acceptance (spec §9.3): a filed ask above the floor is grilled — its residual
    decisions surface as questions one at a time, each with the machine's lean; the
    gate holds work until the operator ratifies the view entry; the pass yields a
    foldable spec delta. A below-floor ask files straight to standing work."""
    import json

    from . import delta, grill, graph, spec
    from .conversation import Thread, speak

    print("\nslice 3 — acceptance check  (intent extraction by grilling)\n")
    base = len(graph.standing())

    # an above-floor ask: the conversationalist files, the floor finds two stakes
    t = Thread()
    r = speak(t, "set up the berserk download", scripted(
        '{"say":"Let me pin two things down first.","file":"download new Berserk '
        'episodes","done":false}',
        '{"questions":[{"q":"which quality tier?","lean":"1080p","flip":"a tight disk '
        'budget"},{"q":"keep seeding after?","lean":"yes, to ratio 2.0","flip":"a '
        'metered connection"}]}'))
    ok(r.filed is None and r.grilling is not None, "an above-floor ask is held, not filed")
    ok(len(graph.standing()) == base, "the gate holds: no standing work while grilling")
    qcards = [c for c in graph.cards() if grill.is_question(c)]
    ok(len(qcards) == 1, "one grilling question is on the queue at a time")
    ok(grill.lean_of(qcards[0]) == "1080p" and bool(grill.flip_of(qcards[0])),
       "the question card carries the machine's lean and what would flip it")

    # accept the lean on the first; the second surfaces, still gated
    grill.advance(qcards[0], grill.lean_of(qcards[0]))
    qcards = [c for c in graph.cards() if grill.is_question(c)]
    ok(len(qcards) == 1 and grill.question_of(qcards[0]).startswith("keep seeding"),
       "answering one question surfaces the next")
    ok(len(graph.standing()) == base, "the work stays gated through the interview")

    # answer the last in the operator's own words: the pass yields the entry + delta
    products = json.dumps({
        "entry": "A recurring pull of new Berserk episodes from nyaa at 1080p, "
                 "seeding to ratio 2.0.",
        "delta": ("## ADDED — conversation\n"
                  "### Requirement: a download arc names its source\n"
                  "The arc MUST record where it pulls from.\n"
                  "#### Scenario: an arc is set up\n"
                  "- WHEN a download arc is filed\n- THEN its source is named")})
    entry = grill.advance(qcards[0], "no — delete it once I have watched it",
                          scripted(products))
    ok(grill.is_entry(entry) and "1080p" in grill.contract(entry),
       "the resolved pass raises the view entry — the contract to ratify")
    ok(len(graph.standing()) == base, "the gate holds until the entry is ratified")

    # the fourth product is a well-formed, foldable spec delta
    d = delta.parse("# delta — the pass's product\n\n" + grill.delta_of(entry))
    ok(not d.trivial and delta.check(d, spec.read_spec()) is None,
       "the pass's spec delta is well-formed and folds clean")

    # ratifying the view entry is the gate: the held ask spawns, the queue clears
    grill.ratify(entry)
    ok(len(graph.standing()) == base + 1, "ratifying the view entry spawns the work")
    ok(not [c for c in graph.cards() if c.parent],
       "ratifying clears the grilling pass from the queue")

    # a below-floor ask: the floor finds no residual stake, so it files straight through
    t2 = Thread()
    r2 = speak(t2, "downloads should land in /mnt/media", scripted(
        '{"say":"Noted and filed.","file":"downloads land in /mnt/media","done":true}',
        '{"questions":[]}'))
    ok(r2.filed is not None and r2.grilling is None, "a below-floor ask files directly")
    ok(len(graph.standing()) == base + 2, "the below-floor ask is standing work, ungrilled")
