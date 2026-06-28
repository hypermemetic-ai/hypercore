"""Pure render: the tree and the open thread become a frame of styled spans.

No terminal calls live here — the window paints what these functions return, so
every frame is testable without a TTY. A Span is (text, style); a Row is a list
of Spans; the window maps styles to curses attributes.
"""
from __future__ import annotations

import textwrap
from dataclasses import dataclass

from . import grill, tree
from .communication import Thread

# styles (the window owns their colors)
TITLE, HEAD, CARD, SEL, TAG, DIM, LIVE, REST, AWAIT, HINT, MODEL, YOU, SAY = (
    "title", "head", "card", "sel", "tag", "dim", "live", "rest", "await",
    "hint", "model", "you", "say",
)

Row = list
RGB = tuple[int, int, int]

LIGHT = "light"
SOFT_DARK = "soft-dark"


@dataclass(frozen=True)
class Ground:
    polarity: str
    ink: RGB
    paper: RGB


@dataclass(frozen=True)
class Hue:
    name: str
    meaning: str
    light: RGB
    dark: RGB
    reserved: bool = False

    def rgb(self, polarity: str) -> RGB:
        return self.dark if _polarity(polarity) == SOFT_DARK else self.light


@dataclass(frozen=True)
class StyleSpec:
    foreground: str
    attrs: tuple[str, ...] = ()
    state: str = ""


class Frame(list):
    """Rows plus the declared ground, palette, and style semantics they paint with.

    It subclasses list to preserve the old pure-render interface: existing checks and callers still
    see a list of rows of spans, while the frame carries the color data the window consumes.
    """

    def __init__(self, rows: list[Row], polarity: str = LIGHT):
        super().__init__(rows)
        self.polarity = _polarity(polarity)
        self.ground = ground(self.polarity)
        self.palette = palette()
        self.styles = styles()

    @property
    def rows(self) -> "Frame":
        return self

    def with_polarity(self, polarity: str) -> "Frame":
        return Frame(list(self), polarity)

    def toggled(self) -> "Frame":
        return self.with_polarity(SOFT_DARK if self.polarity == LIGHT else LIGHT)


def ground(polarity: str = LIGHT) -> Ground:
    pol = _polarity(polarity)
    if pol == SOFT_DARK:
        return Ground(pol, ink=(239, 231, 220), paper=(31, 29, 26))
    return Ground(pol, ink=(36, 32, 27), paper=(248, 241, 231))


def palette() -> dict[str, Hue]:
    return {
        "accent": Hue("accent", "section and label anchors", (121, 79, 13), (215, 179, 106)),
        "selection": Hue("selection", "the selected row", (15, 111, 123), (110, 211, 222)),
        "awaiting": Hue("awaiting", "awaiting operator decision", (138, 90, 0), (227, 182, 86)),
        "running": Hue("running", "running work", (32, 122, 82), (105, 196, 154)),
        "at-rest": Hue("at-rest", "standing work at rest", (91, 100, 108), (180, 184, 192)),
        "operator": Hue("operator", "operator words", (36, 95, 182), (143, 184, 255)),
        "muted": Hue("muted", "secondary text", (116, 112, 106), (172, 164, 155)),
        "alarm": Hue("alarm", "reserved alarm", (180, 35, 24), (255, 138, 128), reserved=True),
    }


def styles() -> dict[str, StyleSpec]:
    return {
        TITLE: StyleSpec("ink", ("bold",)),
        HEAD: StyleSpec("accent", ("bold",)),
        CARD: StyleSpec("ink"),
        SEL: StyleSpec("selection", ("bold",), "selected"),
        TAG: StyleSpec("accent", ("dim",)),
        DIM: StyleSpec("muted", ("dim",)),
        LIVE: StyleSpec("running", ("bold",), "running"),
        REST: StyleSpec("at-rest", (), "at-rest"),
        AWAIT: StyleSpec("awaiting", (), "awaiting"),
        HINT: StyleSpec("muted", ("dim",)),
        MODEL: StyleSpec("muted", ("dim",)),
        YOU: StyleSpec("operator", ("bold",)),
        SAY: StyleSpec("ink"),
    }


STATE_CUES = {
    "selected": ("▸",),
    "awaiting": ("awaiting",),
    "running": ("⟳", "running", "worker is on it"),
    "at-rest": ("at rest", "standing"),
}


def main_body(nodes: list[tree.Node], sel: int, width: int = 76,
              polarity: str = LIGHT) -> Frame:
    """The resting face of the system: the queue over the work."""
    rows: list[Row] = [[("hypercore", TITLE)], []]

    rows.append([("queue", HEAD)])
    cards = tree.cards(nodes)
    if not cards:
        rows.append([("  — nothing awaiting you —", DIM)])
    for i, c in enumerate(cards):
        chosen = i == sel
        rows.append([("  " + ("▸ " if chosen else "· "), SEL if chosen else AWAIT),
                     (_subject(c.text), SEL if chosen else CARD),
                     ("   awaiting · " + _card_label(c), AWAIT)])
        if chosen:
            rows.extend(_card_detail(c, width))

    rows.append([])
    rows.append([("work", HEAD)])
    items = tree.work(nodes)
    if not items:
        rows.append([("  — no standing work; system at rest —", REST)])
    for n in items:
        if n.is_live:
            rows.append([("  ⟳ ", LIVE), (_subject(n.text), CARD),
                         ("   running · a worker is on it", LIVE)])
        else:
            rows.append([("  · ", REST), (_subject(n.text), CARD),
                         ("   standing · at rest", REST)])

    return Frame(rows, polarity)


def _card_label(c: tree.Node) -> str:
    """A card's kind, named — read from the one authority (`grill.card_kind`), not guessed here."""
    return grill.card_kind(c)


def _card_detail(c: tree.Node, width: int) -> list[Row]:
    """The selected card, opened: a question shows its lean and what would flip it;
    a ratification shows the contract it endorses; any other card, its commands. The kind is read
    from `grill.card_kind`, the same authority the label reads — the render no longer infers it."""
    kind = grill.card_kind(c)
    if kind == "grilling question":
        rows = [[("      lean  ", DIM), (grill.lean_of(c), SAY)]]
        if grill.flip_of(c):
            rows.append([("      flips ", DIM), (grill.flip_of(c), TAG)])
        rows.append([("      [a] accept the lean   ·   type to answer", DIM)])
        return rows
    if kind == "ratification":
        rows: list[Row] = []
        for w in _wrap(grill.contract(c), width - 8):
            rows.append([("      ", SAY), (w, SAY)])
        rows.append([("      [a] ratify — spawns the work   ·   [c] cut", DIM)])
        return rows
    return [[("      [a] approve   [c] cut   [e] explain", DIM)]]


def converse_body(thread: Thread, width: int, explain_text: str | None = None,
                  polarity: str = LIGHT) -> Frame:
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
    return Frame(rows, polarity)


def view_body(node, sel: int, width: int, polarity: str = LIGHT) -> Frame:
    """One node of the operator view: vision beside as-built, readiness, gap, and complexity debt,
    then the children to drill into. `node` is a view.ViewNode (duck-typed to stay decoupled)."""
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
    block("readiness", getattr(node, "readiness", []), CARD)

    structure = getattr(node, "structure", None)         # the architecture review's map
    if structure:
        rows.append([("structure  ·  modules by length · the length signal", HEAD)])
        for line in structure:
            style = TAG if "⚑" in line else CARD         # debt marked, in line
            rows.append([("    ", style), (line, style)])
        rows.append([])

    block("gap", node.gap, TAG)
    block("complexity debt", getattr(node, "complexity_debt", []), TAG)

    if node.children:
        rows.append([("drill in", HEAD)])
        for i, child in enumerate(node.children):
            chosen = i == sel
            style = SEL if chosen else CARD
            rows.append([("  " + ("▸ " if chosen else "· "), style),
                         (child.title, style)])
    return Frame(rows, polarity)


def footer(model: str, mode: str, buffer: str, status: str, width: int, live_loop: bool = True) -> Row:
    """The bottom line: where the operator speaks, the model and loop status named at the right."""
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
    right = model if live_loop else f"{model} · not live loop"
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


def _polarity(polarity: str) -> str:
    return SOFT_DARK if polarity in (SOFT_DARK, "dark") else LIGHT
