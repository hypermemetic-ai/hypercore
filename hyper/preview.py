"""A plain-text snapshot of the window's face — the same render the curses
window paints, flattened to stdout so the look can be seen without a TTY.

    python3 -m hyper --frame
"""
from __future__ import annotations

import os
import tempfile

WIDTH = 64


def run() -> int:
    os.environ["HYPER_ROOT"] = tempfile.mkdtemp(prefix="hyper-frame-")
    from . import conversation, graph, render

    graph.raise_card("the intake box pulls torrents from nyaa")
    graph.file_intent("download the new Berserk episodes")

    print()
    for row in render.main_body(graph.read_graph(), 0):
        print("  " + _flat(row))
    print()
    print("  " + _flat(render.footer(conversation.MODEL_LABEL, "input", "", "", WIDTH)))
    print()
    return 0


def _flat(row) -> str:
    return "".join(text for text, _style in row).rstrip()
