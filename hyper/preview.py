"""A plain-text snapshot of the window's faces — the same renders the curses
window paints, flattened to stdout so the look can be seen without a TTY.

    python3 -m hyper --frame
"""
from __future__ import annotations

import os
import tempfile

WIDTH = 76


def run() -> int:
    real = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.environ["HYPER_ROOT"] = tempfile.mkdtemp(prefix="hyper-frame-")
    from . import conversation, graph, grill, render, view

    graph.raise_card("the intake box pulls torrents from nyaa")
    graph.file_intent("download the new Berserk episodes")

    print("\n  ── the resting face ──\n")
    for row in render.main_body(graph.read_graph(), 0, WIDTH):
        print("  " + _flat(row))
    print("  " + _flat(render.footer(conversation.MODEL_LABEL, "input", "", "", WIDTH)))

    # a grilling question on the queue: its lean and what would flip it, expanded
    held = graph.hold("absorb the seasonal anime tracker")
    graph.question(held.id,
                   "which tracker should the seasonal pulls follow?\n"
                   "lean: nyaa — it carries the releases you already use\n"
                   "flip: a private tracker you have an account on would change it",
                   awaiting=True)
    cards = graph.cards()
    sel = next(i for i, c in enumerate(cards) if grill.is_question(c))
    print("\n  ── grilling: one question, with the machine's lean ──\n")
    for row in render.main_body(graph.read_graph(), sel, WIDTH):
        print("  " + _flat(row))
    print("  " + _flat(render.footer(conversation.MODEL_LABEL, "browse", "", "", WIDTH)))

    # a worker on a thread: the live indicator the threads view shows while it runs
    graph.delegate(graph.standing()[0])
    print("\n  ── a worker on a thread (live) ──\n")
    for row in render.main_body(graph.read_graph(), -1, WIDTH):
        print("  " + _flat(row))
    print("  " + _flat(render.footer(conversation.MODEL_LABEL, "input", "", "", WIDTH)))

    print("\n  ── the operator view (root) ──\n")
    root = view.operator_view(root=real)
    for row in render.view_body(root, 0, WIDTH):
        print("  " + _flat(row))
    print("  " + _flat(render.footer(conversation.MODEL_LABEL, "view", "", "", WIDTH)))
    print()
    return 0


def _flat(row) -> str:
    return "".join(text for text, _style in row).rstrip()
