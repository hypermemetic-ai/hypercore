"""Pure render: the graph and the open thread become a frame of styled spans.

No terminal calls live here — the window paints what these functions return, so
every frame is testable without a TTY. A Span is (text, style); a Row is a list
of Spans; the window maps styles to curses attributes.
"""
from __future__ import annotations

import textwrap

from . import graph
from .conversation import Thread

# styles (the window owns their colors)
TITLE, HEAD, CARD, SEL, TAG, DIM, LIVE, HINT, MODEL, YOU, SAY = (
    "title", "head", "card", "sel", "tag", "dim", "live",
    "hint", "model", "you", "say",
)

Span = tuple
Row = list


def main_body(nodes: list[graph.Node], sel: int) -> list[Row]:
    """The resting face of the system: the queue over the threads."""
    rows: list[Row] = [[("hypercore", TITLE)], []]

    rows.append([("queue", HEAD)])
    cards = graph.cards(nodes)
    if not cards:
        rows.append([("  — nothing awaiting you —", DIM)])
    for i, c in enumerate(cards):
        chosen = i == sel
        style = SEL if chosen else CARD
        rows.append([("  " + ("▸ " if chosen else "· "), style),
                     (_subject(c.text), style),
                     ("   " + c.kind, TAG)])
        if chosen:
            rows.append([("      [a] approve   [c] cut   [e] explain", DIM)])

    rows.append([])
    rows.append([("threads", HEAD)])
    work = graph.standing(nodes)
    if not work:
        rows.append([("  — no standing work —", DIM)])
    for n in work:
        rows.append([("  · ", CARD), (_subject(n.text), CARD)])

    return rows


def converse_body(thread: Thread, width: int, explain_text: str | None = None) -> list[Row]:
    """An open thread: the turns of one conversation."""
    rows: list[Row] = [[("hypercore  ·  thread", TITLE)], []]
    turns = list(thread.turns)
    if explain_text:
        turns = turns + [("machine", explain_text)]
    for who, text in turns:
        if who == "operator":
            for j, line in enumerate(_wrap(text, width - 6)):
                rows.append([("  you  " if j == 0 else "       ", YOU), (line, YOU)])
        else:
            for line in _wrap(text, width - 6):
                rows.append([("       ", SAY), (line, SAY)])
        rows.append([])
    return rows


def footer(model: str, mode: str, buffer: str, status: str, width: int) -> Row:
    """The bottom line: where the operator speaks, the model named at the right."""
    if status:
        left = status
    elif mode == "browse":
        left = "browse · ↑↓ select · a/c/e act · esc or type to speak"
    elif mode == "converse":
        left = "› " + buffer + "▖" + "   esc closes the thread"
    else:
        left = "› " + buffer + "▖" if buffer else "‹ type to speak ›"
    right = model
    pad = max(1, width - _len(left) - len(right) - 2)
    return [(" " + left, HINT), (" " * pad, HINT), (right + " ", MODEL)]


def _subject(text: str) -> str:
    first = text.strip().splitlines()[0] if text.strip() else ""
    return first[:72]


def _wrap(text: str, width: int) -> list[str]:
    out: list[str] = []
    for para in text.splitlines() or [""]:
        out.extend(textwrap.wrap(para, max(8, width)) or [""])
    return out


def _len(s: str) -> int:
    return len(s)
