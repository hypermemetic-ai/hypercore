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
    _slice4(root)
    _slice5(root)

    print()
    if _fails:
        print(f"  {_fails} FAILED\n")
        return 1
    print("  all checks pass — slices 1–5 meet their acceptance checks\n")
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


def _slice4(root: str) -> None:
    """Acceptance (spec §9.4): a worker is grounded in its capability's spec slice by
    construction — holding the whole spec, not confined to the touched slice (rebuild-spec
    §4.1, §6.4); it runs fenced in its own git worktree; and its raw output reaches the
    operator through no path — the conversationalist authors every operator-facing word
    and folds the refined delta. Drives propose→apply→archive end to end with scripted
    transports over the real graph and a real worktree."""
    import json

    from . import conversation, delta, graph, render, spec, worker

    print("\nslice 4 — acceptance check  (workers, with spec-scoped context)\n")

    # the propose-stage product, ratified: a spawned ask carrying a contract and a handed
    # delta that touches two existing capabilities (worker, conversation).
    handed = (
        "## ADDED — worker\n"
        "### Requirement: a worker checkpoints its progress\n"
        "The worker MUST record a checkpoint the conversationalist can read.\n"
        "#### Scenario: a checkpoint\n- WHEN a worker pauses\n- THEN its progress is recorded\n\n"
        "## ADDED — conversation\n"
        "### Requirement: the conversationalist names the worker in the record\n"
        "The conversationalist MUST record which worker a result came from.\n"
        "#### Scenario: a hand-off\n- WHEN a result is archived\n- THEN the worker is named\n")
    ask = graph.file_intent("give workers a progress checkpoint")
    graph.approve(graph.raise_card(
        "Workers checkpoint progress, and the record names the worker.\n\ndelta:\n" + handed,
        kind="decide", parent=ask.id))                    # the ratified contract

    # 1. the grounding, by construction: the whole spec, with the touched capabilities marked
    # as grounding — the worker is NOT slice-confined (rebuild-spec §4.1, §6.4)
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

    # the keystone (rebuild-spec §6.4): a handed delta that mis-names a capability does not
    # shrink the worker's context — it still holds the whole spec, so the rescan can catch the
    # mis-mapping. A slice-confined worker (context = {graph}) would have been blind to it.
    mis = graph.file_intent("a change whose handed delta mis-maps the capability")
    graph.approve(graph.raise_card(
        "mis-mapped contract.\n\ndelta:\n## ADDED — graph\n"
        "### Requirement: a mis-named requirement\nx\n#### Scenario: s\n- WHEN a\n- THEN b\n",
        kind="decide", parent=mis.id))
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
       "the delegated work goes live on the threads view while the worker runs")

    # the worker builds and hands back a machine-facing result carrying raw prose
    SENTINEL = "<<RAW WORKER RAMBLE — walls of rambling text>>"
    result = worker.apply(ask, scripted(json.dumps({
        "report": "Implemented the checkpoint behind a red→green loop. " + SENTINEL,
        "delta": handed,
        "loop": {"command": "python3 -m hyper --check",
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

    # 3. archive: the conversationalist coherence-checks and folds; the raw report leaks nowhere
    reply = conversation.integrate(ask, result, scripted(json.dumps({
        "coherent": True,
        "say": "Workers now checkpoint progress; it landed.",
        "card": None})), root)
    ok(reply.done, "the conversationalist judged the result coherent and archived it")
    ok(SENTINEL not in reply.say, "the conversationalist authored its own words, not the raw report")

    sp = spec.read_spec(root)
    ok(sp.capability("worker").requirement("a worker checkpoints its progress") is not None
       and sp.capability("conversation").requirement(
           "the conversationalist names the worker in the record") is not None,
       "the refined delta folded into the spec in the same act")

    # the raw report has no operator-facing or durable home anywhere
    frame = "".join(t for row in render.main_body(graph.read_graph(), -1) for t, _s in row)
    ndir = os.path.join(root, "work", "nodes")
    nodefiles = "".join(open(os.path.join(ndir, n)).read() for n in os.listdir(ndir))
    cards_text = "".join(c.text for c in graph.read_graph())
    ok(SENTINEL not in frame and SENTINEL not in nodefiles and SENTINEL not in cards_text,
       "the raw worker report reaches no card, no render, and no node — the leak path does not exist")

    ok(graph.find(ask.id).state == graph.DONE and ask.id not in [n.id for n in graph.work()],
       "the integrated work folded out of the threads view")

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


def _slice5(root: str) -> None:
    """Acceptance (spec §9.5): a graph that hands back a behavior change with no recorded
    red→green loop, or one that grows a source file past the line-count budget, cannot fold —
    the folding conditions refuse it and return a decision, leaving the spec untouched; a
    result that meets every condition folds, and a file over budget folds only when a decision
    record justifies it. Drives the conditions through the real integrate path and real
    worktrees."""
    import json

    from . import conditions, conversation, graph, spec, worker

    print("\nslice 5 — acceptance check  (the folding conditions)\n")

    cap = "folding-conditions"
    req = lambda name: spec.read_spec(root).capability(cap) and \
        spec.read_spec(root).capability(cap).requirement(name)
    coherent = lambda: scripted(json.dumps({"coherent": True, "say": "it landed.", "card": None}))

    def delta_for(name: str) -> str:
        return (f"## ADDED — {cap}\n### Requirement: {name}\nThe gate MUST hold.\n"
                f"#### Scenario: s\n- WHEN a fold is attempted\n- THEN the gate runs\n")

    def staged(text: str, name: str):
        ask = graph.file_intent(text)
        graph.approve(graph.raise_card("contract.\n\ndelta:\n" + delta_for(name),
                                       kind="decide", parent=ask.id))
        worker.worktree(ask, root)
        graph.delegate(ask)
        return ask

    def godfile(tree: str) -> None:
        graph.atomic_write(os.path.join(tree, "hyper", "giant.py"),
                           "# a shallow god-file\n" + "x = 0\n" * (conditions.BUDGET + 60))

    # 1. a behavior change handed back with no recorded loop cannot fold
    ask = staged("a behavior change handed back with no loop", "a loopless change is gated")
    result = worker.apply(ask, scripted(json.dumps({
        "report": "did the work, no harness",
        "delta": delta_for("a loopless change is gated"),
        "loop": {"command": "", "red": "", "green": ""}})), root)         # no recorded loop
    reply = conversation.integrate(ask, result, coherent(), root)
    ok(reply.card is not None and not reply.done,
       "a behavior change with no recorded red→green loop cannot fold")
    ok(req("a loopless change is gated") is None, "the refused fold leaves the spec untouched")
    ok(graph.find(ask.id).is_live, "the work stays live with a decision raised, not folded")
    worker.teardown(ask, root)

    # 2. a graph that grows a source file past the budget cannot fold (loop + delta both fine,
    # so the budget is what bites)
    ask = staged("a change that grows a god-file", "a god-file is gated")
    godfile(worker._tree_path(ask, root))
    result = worker.apply(ask, scripted(json.dumps({
        "report": "grew a giant module",
        "delta": delta_for("a god-file is gated"),
        "loop": {"command": "run", "red": "failed", "green": "passed"}})), root)
    blocked = conditions.unmet(result, root)
    ok(blocked is not None and "budget" in blocked and "giant.py" in blocked,
       f"the budget condition catches the god-file the graph grew ({conditions.BUDGET}-line ceiling)")
    reply = conversation.integrate(ask, result, coherent(), root)
    ok(reply.card is not None and not reply.done, "a graph that grows a god-file cannot fold")
    ok(req("a god-file is gated") is None, "the refused fold leaves the spec untouched")
    worker.teardown(ask, root)

    # 3. a result that meets every condition folds — a recorded loop, an in-budget module
    ask = staged("a clean behavior change", "a clean change folds")
    result = worker.apply(ask, scripted(json.dumps({
        "report": "did the work behind a loop",
        "delta": delta_for("a clean change folds"),
        "loop": {"command": "python3 -m hyper --check", "red": "absent", "green": "present"}})), root)
    ok(conditions.unmet(result, root) is None,
       "a recorded loop and an in-budget module meet every folding condition")
    reply = conversation.integrate(ask, result, coherent(), root)
    ok(reply.done and req("a clean change folds") is not None,
       "the met conditions let the delta fold into the spec")
    worker.teardown(ask, root)

    # 4. a file over budget folds when a decision record justifies it (the ADR escape hatch)
    graph.atomic_write(os.path.join(spec.spec_dir(root), "decisions", "0099-giant-justified.md"),
                       "# ADR 0099\n\nhyper/giant.py is allowed over the budget here.\n")
    ask = staged("a justified large module", "a justified module folds")
    godfile(worker._tree_path(ask, root))
    result = worker.apply(ask, scripted(json.dumps({
        "report": "grew a justified module",
        "delta": delta_for("a justified module folds"),
        "loop": {"command": "run", "red": "failed", "green": "passed"}})), root)
    ok(conditions.unmet(result, root) is None,
       "a file over budget but named in a decision record clears the budget condition")
    reply = conversation.integrate(ask, result, coherent(), root)
    ok(reply.done and req("a justified module folds") is not None, "the justified exception folds")
    worker.teardown(ask, root)

    # 5. the delta condition is part of the same gate: a delta that will not apply is caught
    # as a decision, not an uncaught CannotFold
    ask = staged("a change carrying a delta that will not apply", "unused")
    result = worker.apply(ask, scripted(json.dumps({
        "report": "built it",
        "delta": "## MODIFIED — folding-conditions\n### Requirement: nonexistent\nx\n",
        "loop": {"command": "run", "red": "failed", "green": "passed"}})), root)
    reply = conversation.integrate(ask, result, coherent(), root)
    ok(reply.card is not None and not reply.done,
       "a delta that will not apply is caught by the gate as a decision, not a crash")
    worker.teardown(ask, root)
