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
    from . import conversation, graph, render, view

    graph.raise_card("the intake box pulls torrents from nyaa")
    graph.file_intent("download the new Berserk episodes")

    print("\n  ── the resting face ──\n")
    for row in render.main_body(graph.read_graph(), 0):
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
