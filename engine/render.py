"""Pure render: the tree and the open thread become a frame of styled spans.

No terminal calls live here — the window paints what these functions return, so
every frame is testable without a TTY. A Span is (text, style); a Row is a list
of Spans; the window maps styles to curses attributes.
"""
from __future__ import annotations

import textwrap

from . import grill, tree
from .communication import Thread

# styles (the window owns their colors)
TITLE, HEAD, CARD, SEL, TAG, DIM, LIVE, HINT, MODEL, YOU, SAY = (
    "title", "head", "card", "sel", "tag", "dim", "live",
    "hint", "model", "you", "say",
)

Row = list


def main_body(nodes: list[tree.Node], sel: int, width: int = 76) -> list[Row]:
    """The resting face of the system: the queue over the work."""
    rows: list[Row] = [[("hypercore", TITLE)], []]

    rows.append([("queue", HEAD)])
    cards = tree.cards(nodes)
    if not cards:
        rows.append([("  — nothing awaiting you —", DIM)])
    for i, c in enumerate(cards):
        chosen = i == sel
        style = SEL if chosen else CARD
        rows.append([("  " + ("▸ " if chosen else "· "), style),
                     (_subject(c.text), style),
                     ("   " + _card_label(c), TAG)])
        if chosen:
            rows.extend(_card_detail(c, width))

    rows.append([])
    rows.append([("work", HEAD)])
    items = tree.work(nodes)
    if not items:
        rows.append([("  — no standing work —", DIM)])
    for n in items:
        if n.is_live:
            rows.append([("  ⟳ ", LIVE), (_subject(n.text), CARD),
                         ("   a worker is on it", LIVE)])
        else:
            rows.append([("  · ", CARD), (_subject(n.text), CARD)])

    return rows


def _card_label(c: tree.Node) -> str:
    """A card's weight, named: a grilling question, a ratification, or a decision."""
    if grill.is_question(c):
        return "question"
    if grill.is_entry(c):
        return "ratify"
    return c.kind


def _card_detail(c: tree.Node, width: int) -> list[Row]:
    """The selected card, opened: a question shows its lean and what would flip it;
    a view entry shows the contract the ratify endorses; a plain card, its commands."""
    if grill.is_question(c):
        rows = [[("      lean  ", DIM), (grill.lean_of(c), SAY)]]
        if grill.flip_of(c):
            rows.append([("      flips ", DIM), (grill.flip_of(c), TAG)])
        rows.append([("      [a] accept the lean   ·   type to answer", DIM)])
        return rows
    if grill.is_entry(c):
        rows: list[Row] = []
        for w in _wrap(grill.contract(c), width - 8):
            rows.append([("      ", SAY), (w, SAY)])
        rows.append([("      [a] ratify — spawns the work   ·   [c] cut", DIM)])
        return rows
    return [[("      [a] approve   [c] cut   [e] explain", DIM)]]


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


def view_body(node, sel: int, width: int) -> list[Row]:
    """One node of the operator view: vision beside as-built beside gap, then the
    children to drill into. `node` is a view.ViewNode (duck-typed to stay decoupled)."""
    rows: list[Row] = [[(f"operator view  ·  {node.title}", TITLE)], []]

    def block(label: str, lines: list[str], style: str) -> None:
        if not lines:
            return
        rows.append([(label, HEAD)])
        for line in lines:
            for w in _wrap(line, width - 8):
                rows.append([("    ", style), (w, style)])
        rows.append([])

    block("vision", node.vision, SAY)
    block("as-built", node.asbuilt, CARD)

    structure = getattr(node, "structure", None)         # the architecture review's map
    if structure:
        rows.append([("structure  ·  modules by length · the context-cost signal", HEAD)])
        for line in structure:
            style = TAG if "⚑" in line else CARD         # debt marked, in line
            rows.append([("    ", style), (line, style)])
        rows.append([])

    block("gap", node.gap, TAG)

    if node.children:
        rows.append([("drill in", HEAD)])
        for i, child in enumerate(node.children):
            chosen = i == sel
            style = SEL if chosen else CARD
            rows.append([("  " + ("▸ " if chosen else "· "), style),
                         (child.title, style)])
    return rows


def footer(model: str, mode: str, buffer: str, status: str, width: int) -> Row:
    """The bottom line: where the operator speaks, the model named at the right."""
    if status:
        left = status
    elif mode == "view":
        left = "view · ↑↓ select · →/enter drill · ←/esc up · type to speak"
    elif mode == "browse":
        left = "browse · ↑↓ select · a/c/e act · v view · esc or type to speak"
    elif mode == "answer":
        left = "answer › " + buffer + "▖" + "   esc cancels"
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
