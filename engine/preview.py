"""A plain-text snapshot of the window's faces — the same renders the curses
window paints, flattened to stdout so the look can be seen without a TTY.

    python3 -m engine --frame
"""
from __future__ import annotations

import os
import tempfile

WIDTH = 76


def run() -> int:
    real = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.environ["ENGINE_ROOT"] = tempfile.mkdtemp(prefix="engine-frame-")
    from . import tree, grill, render, transport, view

    tree.raise_card("the intake box pulls torrents from nyaa")
    tree.file_intent("download the new Berserk episodes")

    print("\n  ── the resting face ──\n")
    for row in render.main_body(tree.read_tree(), 0, WIDTH):
        print("  " + _flat(row))
    print("  " + _flat(render.footer(transport.MODEL_LABEL, "input", "", "", WIDTH)))

    # a grilling question on the queue: its lean and what would flip it, expanded
    held = tree.hold("absorb the seasonal anime tracker")
    grill._save(held, grill._Pass(0, [{
        "q": "which tracker should the seasonal pulls follow?",
        "lean": "nyaa — it carries the releases you already use",
        "flip": "a private tracker you have an account on would change it",
        "answer": ""}], "", ""))
    cards = tree.cards()
    sel = next(i for i, c in enumerate(cards) if grill.is_question(c))
    print("\n  ── grilling: one question, with the machine's lean ──\n")
    for row in render.main_body(tree.read_tree(), sel, WIDTH):
        print("  " + _flat(row))
    print("  " + _flat(render.footer(transport.MODEL_LABEL, "browse", "", "", WIDTH)))

    # a worker on a thread: the live indicator the threads view shows while it runs
    tree.dispatch(tree.standing()[0])
    print("\n  ── a worker on a thread (live) ──\n")
    for row in render.main_body(tree.read_tree(), -1, WIDTH):
        print("  " + _flat(row))
    print("  " + _flat(render.footer(transport.MODEL_LABEL, "input", "", "", WIDTH)))

    # the operator view root, with the architecture review's standing output: the
    # structural map of as-built reality (modules by length against the signal, debt marked)
    # and the complexity debt as the gap — the system's shape read without reading code.
    print("\n  ── the operator view (root) · the architecture review's map ──\n")
    root = view.operator_view(root=real)
    for row in render.view_body(root, 0, WIDTH):
        print("  " + _flat(row))
    print("  " + _flat(render.footer(transport.MODEL_LABEL, "view", "", "", WIDTH)))
    print()
    return 0


def _flat(row) -> str:
    return "".join(text for text, _style in row).rstrip()
