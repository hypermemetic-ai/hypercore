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

    # 1. file intent: it lands as standing work, the thread closes on satisfaction
    t = Thread()
    r = speak(t, "download the new berserk episodes", scripted(
        '{"say":"Filing that as standing work.","file":"download the new Berserk '
        'episodes","done":true}'))
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

    print()
    if _fails:
        print(f"  {_fails} FAILED\n")
        return 1
    print("  all checks pass — slice 1 meets its acceptance check\n")
    return 0
