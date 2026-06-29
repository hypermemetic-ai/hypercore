"""Pure render: the tree and the open thread become a frame of styled spans.

No terminal calls live here — the window paints what these functions return, so
every frame is testable without a TTY. A Span is (text, style); a Row is a list
of Spans; the window maps styles to curses attributes.
"""
from __future__ import annotations

import textwrap
from dataclasses import dataclass

from . import card_render, reasoning, tree
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


PULSE_GLYPHS = ("◉", "◎")
STATE_GLYPHS = {
    "awaiting": "?",
    "running": PULSE_GLYPHS[0],
    "at-rest": "○",
}
STATE_CUES = {
    "selected": ("▸",),
    "awaiting": (STATE_GLYPHS["awaiting"], "awaiting"),
    "running": (*PULSE_GLYPHS, "running", "worker is on it"),
    "at-rest": (STATE_GLYPHS["at-rest"], "at rest", "standing"),
}


def main_body(nodes: list[tree.Node], sel: int, width: int = 76,
              polarity: str = LIGHT, tick: int = 0, confirm_card: str = "") -> Frame:
    """The resting face of the system: the queue over the work."""
    rows: list[Row] = [[("hypercore", TITLE)], []]

    rows.append([("queue", HEAD)])
    cards = tree.cards(nodes)
    if not cards:
        rows.append([("  — nothing awaiting you —", DIM)])
    for i, c in enumerate(cards):
        chosen = i == sel
        rows.append([("  ? ", AWAIT),
                     ("▸ " if chosen else "  ", SEL if chosen else DIM),
                     (_subject(c.text), SEL if chosen else CARD),
                     ("   awaiting · " + _card_label(c), AWAIT)])
        if chosen:
            rows.extend(_card_detail(c, width, confirm=(confirm_card == c.id)))

    rows.append([])
    rows.append([("work", HEAD)])
    work_rows = _work_rows(nodes, tick)
    if not work_rows:
        rows.append([("  — no standing work; system at rest —", REST)])
    rows.extend(work_rows)

    return Frame(rows, polarity)


def _work_rows(nodes: list[tree.Node], tick: int) -> list[Row]:
    """Render open work as an indented tree; closed descendants become scent on the owner row."""
    kids = _children_by_parent(nodes)
    visible = [n for n in nodes if _visible_work(n)]
    visible_ids = {n.id for n in visible}
    roots = [n for n in visible if n.parent not in visible_ids]
    rows: list[Row] = []

    def walk(n: tree.Node, depth: int) -> None:
        rows.append(_work_row(n, depth, tick, _scent(n, kids, visible_ids)))
        for child in kids.get(n.id, []):
            if child.id in visible_ids:
                walk(child, depth + 1)

    for n in sorted(roots, key=lambda x: (x.created, x.id)):
        walk(n, 0)
    return rows


def _work_row(n: tree.Node, depth: int, tick: int, scent: str) -> Row:
    state = "running" if n.is_live else "at-rest"
    style = LIVE if n.is_live else REST
    glyph = _running_glyph(tick) if n.is_live else STATE_GLYPHS[state]
    meta = "running · worker is on it" if n.is_live else "standing · at rest"
    if scent:
        meta += " · " + scent
    return [("  " + "  " * depth + glyph + " ", style),
            (_subject(n.text), CARD),
            ("   " + meta, style)]


def _running_glyph(tick: int) -> str:
    return PULSE_GLYPHS[(max(0, tick) // 8) % len(PULSE_GLYPHS)]


def _visible_work(n: tree.Node) -> bool:
    return n.state in (tree.STANDING, tree.IN_FLIGHT) and not n.folded


def _children_by_parent(nodes: list[tree.Node]) -> dict[str, list[tree.Node]]:
    kids: dict[str, list[tree.Node]] = {}
    for n in nodes:
        if n.parent:
            kids.setdefault(n.parent, []).append(n)
    for children in kids.values():
        children.sort(key=lambda n: (n.created, n.id))
    return kids


def _scent(n: tree.Node, kids: dict[str, list[tree.Node]], visible_ids: set[str]) -> str:
    hidden = [(d, level) for d, level in _descendants(n.id, kids) if d.id not in visible_ids]
    if not hidden:
        return ""
    child_count = len(kids.get(n.id, []))
    max_depth = max(level for _d, level in hidden)
    leaves = sum(1 for d, _level in hidden if not kids.get(d.id))
    return (f"scent · {_plural(child_count, 'child')} · "
            f"shape {max_depth} deep / {_plural(leaves, 'leaf')} · {_rollup(d for d, _level in hidden)}")


def _descendants(parent: str, kids: dict[str, list[tree.Node]]) -> list[tuple[tree.Node, int]]:
    out: list[tuple[tree.Node, int]] = []

    def walk(node_id: str, level: int) -> None:
        for child in kids.get(node_id, []):
            out.append((child, level))
            walk(child.id, level + 1)

    walk(parent, 1)
    return out


def _rollup(nodes) -> str:
    found = list(nodes)
    failed = any(n.state == tree.AWAITING or "fail" in n.state.lower() for n in found)
    passed = any(n.folded or n.state in (tree.DONE, "settled", "endorsed") for n in found)
    if failed and passed:
        return "mixed"
    if failed:
        return "failed"
    if passed:
        return "passed"
    return "open"


def _plural(n: int, word: str) -> str:
    irregular = {"child": "children", "leaf": "leaves"}
    plural = irregular.get(word, word + "s")
    return f"{n} {word if n == 1 else plural}"


def _card_label(c: tree.Node) -> str:
    """A card's kind, named — read from the one authority (`grill.card_kind`), not guessed here."""
    return card_render.label(c)


def _card_detail(c: tree.Node, width: int, confirm: bool = False) -> list[Row]:
    """The selected card, opened through the card row leaf."""
    return card_render.detail(c, width, confirm)


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


def reasoning_loop_body(loop: reasoning.ReasoningLoop, width: int,
                        polarity: str = LIGHT) -> Frame:
    """One surface over one model's working: steerable thread or read-only worker trace."""
    source = "architect thread" if loop.source == reasoning.ARCHITECT_THREAD else "fenced worker trace"
    rows: list[Row] = [[("reasoning loop", TITLE)], []]
    rows.append([("scope", HEAD), (f"  node {loop.node_id} · {source} · {loop.subject}", CARD)])
    rows.append([])
    rows.append([("limit", HEAD)])
    for line in _wrap(reasoning.CAVEAT, width - 8):
        rows.append([("    ", HINT), (line, HINT)])
    rows.append([])

    rows.append([("account", HEAD)])
    if loop.read_only:
        rows.append([("    read-only trace · no step edit · no mid-run injection", MODEL)])
    for i, step in enumerate(loop.steps, start=1):
        chosen = i - 1 == loop.selected
        style = SEL if chosen else CARD
        prefix = f"  {i:02d} "
        for j, line in enumerate(_wrap(step.text, width - len(prefix) - 2)):
            rows.append([(prefix if j == 0 else "     ", style), (line, style)])
    if not loop.steps:
        rows.append([("    no steps remain; reset and rerun can rebuild the thread shape", HINT)])
    rows.append([])

    rows.append([("acts", HEAD)])
    for action in loop.actions:
        rows.append([("    ", TAG), (action, TAG)])
    if loop.effect:
        rows.append([])
        rows.append([("changed", HEAD), (f"  {loop.effect}", CARD)])
    return Frame(rows, polarity)


def footer(model: str, mode: str, buffer: str, status: str, width: int, live_loop: bool = True) -> Row:
    """The bottom line: where the operator speaks, the model and loop status named at the right."""
    if status:
        left = status
    elif mode == "view":
        left = "view · ↑↓ select · →/enter drill · ←/esc up · type to speak"
    elif mode == "loop":
        left = "loop · ↑↓ step · p prune · e edit · r rerun · a re-ask · esc back"
    elif mode == "loop-edit":
        left = "edit step › " + buffer + "▖" + "   enter saves · esc cancels"
    elif mode == "browse":
        left = "browse · ↑↓ · enter detail · a/c/e · v view · esc/type speak"
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
