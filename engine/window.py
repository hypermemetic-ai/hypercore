"""The window: the operator's whole world. Keyboard-only, fullscreen,
high-contrast. A thin paint-and-input layer over the tree and the
architect — it holds nothing that isn't about the screen or the
keyboard. Heavy work (summoning the architect) runs off the input loop
so keystrokes never block, the rule the old window broke first.
"""
from __future__ import annotations

import curses
import threading
from dataclasses import dataclass, field

from . import communication, conditions, tree, grill, render, schedule, transport, view
from .communication import Thread

ESC, ENTER, BACKSPACES = 27, (10, 13, curses.KEY_ENTER), (8, 127, curses.KEY_BACKSPACE)
SPIN = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"


@dataclass
class State:
    mode: str = "input"            # input | browse | converse | view | answer
    buffer: str = ""
    sel: int = 0
    thread: Thread | None = None
    explain_text: str | None = None
    pending: "Async | None" = None
    tick: int = 0
    view_path: list[int] = field(default_factory=list)  # drill-down into the view
    view_sel: int = 0
    answer_id: str = ""            # the grilling question being answered, if any
    polarity: str = render.LIGHT


class Async:
    """Run a slow call off the input loop; the window polls .done."""

    def __init__(self, fn):
        self.result = None
        self.done = False
        threading.Thread(target=self._run, args=(fn,), daemon=True).start()

    def _run(self, fn):
        try:
            self.result = fn()
        except Exception as e:  # surfaced as the architect's reply
            self.result = e
        finally:
            self.done = True


def run() -> None:
    curses.wrapper(_main)


def _main(scr) -> None:
    curses.curs_set(0)
    try:
        curses.set_escdelay(25)
    except Exception:
        pass
    _init_colors()
    scr.timeout(80)
    st = State()
    sched = schedule.Scheduler()       # the autonomous loop runs off this thread (intent §60/§62)
    sched.start()
    try:
        while True:
            nodes = tree.read_tree()
            _paint(scr, st, nodes, sched.live)
            ch = scr.getch()
            if st.pending is not None:
                st.tick += 1
                if st.pending.done:
                    _land(st, st.pending.result)
                    st.pending = None
                continue
            if ch == -1:
                continue
            if not _dispatch(scr, st, ch, nodes):
                return
    finally:
        sched.stop()


# ── input dispatch ───────────────────────────────────────────────────────────

def _dispatch(scr, st: State, ch: int, nodes) -> bool:
    if ch == 17:  # Ctrl-Q quits from anywhere
        return False
    if ch == 20:  # Ctrl-T toggles the window's soft polarity from anywhere
        st.polarity = render.SOFT_DARK if st.polarity == render.LIGHT else render.LIGHT
        return True
    if st.mode == "view":
        return _view_keys(st, ch)
    if st.mode == "answer":
        return _answering(st, ch)
    if st.mode == "browse":
        return _browse(st, ch, nodes)
    return _typing(st, ch)


def _view_keys(st: State, ch: int) -> bool:
    """Navigate the operator-view tree: select, drill in, climb out."""
    node = view.resolve(view.operator_view(), st.view_path)
    last = max(0, len(node.children) - 1)
    if ch in (ord("q"),):
        return False
    if ch in (curses.KEY_UP, ord("k")):
        st.view_sel = max(0, st.view_sel - 1)
    elif ch in (curses.KEY_DOWN, ord("j")):
        st.view_sel = min(last, st.view_sel + 1)
    elif node.children and ch in (curses.KEY_RIGHT, *ENTER):
        st.view_path.append(st.view_sel)
        st.view_sel = 0
    elif ch in (ESC, curses.KEY_LEFT, *BACKSPACES):
        if st.view_path:
            st.view_path.pop()
            st.view_sel = 0
        else:
            st.mode = "browse"
    return True


def _browse(st: State, ch: int, nodes) -> bool:
    cards = tree.cards(nodes)
    if ch in (ord("q"),):
        return False
    if ch in (curses.KEY_UP, ord("k")):
        st.sel = max(0, st.sel - 1)
    elif ch in (curses.KEY_DOWN, ord("j")):
        st.sel = min(max(0, len(cards) - 1), st.sel + 1)
    elif ch == ESC:
        st.mode = "input"
    elif ch == ord("v"):
        st.mode = "view"
        st.view_path = []
        st.view_sel = 0
    elif cards and ch == ord("a"):
        card = cards[st.sel]
        kind = grill.card_kind(card)                  # the one authority, not inferred here
        if kind == "ratification":                    # the gate: ratify spawns work
            grill.ratify(card)
        elif kind == "grilling question":             # accept the machine's lean
            st.pending = Async(lambda c=card: grill.advance(c, grill.lean_of(c)))
        else:
            node = tree.find(card.parent) if card.parent else None
            if node is not None and communication.has_held_build(node):
                st.pending = Async(lambda n=node: communication.settle_held(n))   # override the watched flake: re-fold the held build, no rebuild
            else:
                conditions.accept_length(card.text)    # a length decision records its length; else a no-op
                tree.approve(card)
        st.sel = 0
    elif cards and ch == ord("c"):
        tree.cut(cards[st.sel])
        st.sel = 0
    elif cards and ch == ord("e"):
        card = cards[st.sel]
        st.mode = "converse"
        st.thread = Thread()
        st.explain_text = None
        st.pending = Async(lambda: communication.explain(card))
    elif cards and grill.is_question(cards[st.sel]) and 32 <= ch < 127:
        st.mode = "answer"                            # answer the question in its own words
        st.answer_id = cards[st.sel].id
        st.buffer = chr(ch)
    elif 32 <= ch < 127:  # any other key starts speaking
        st.mode = "input"
        st.buffer = chr(ch)
    return True


def _answering(st: State, ch: int) -> bool:
    """Type an answer to the selected grilling question; Enter sends it to the pass."""
    if ch == ESC:
        st.buffer, st.answer_id, st.mode = "", "", "browse"
    elif ch in BACKSPACES:
        st.buffer = st.buffer[:-1]
    elif ch in ENTER:
        answer, qid = st.buffer.strip(), st.answer_id
        st.buffer, st.answer_id, st.mode = "", "", "browse"
        node = tree.find(qid)
        if answer and node is not None:
            st.pending = Async(lambda: grill.advance(node, answer))
    elif 32 <= ch < 127:
        st.buffer += chr(ch)
    return True


def _typing(st: State, ch: int) -> bool:
    if ch == ESC:
        st.buffer = ""
        st.mode = "browse" if st.mode == "input" else "input"
        st.thread = None
        st.explain_text = None
        return True
    if ch in BACKSPACES:
        st.buffer = st.buffer[:-1]
    elif ch in ENTER:
        text = st.buffer.strip()
        st.buffer = ""
        if text:
            if st.thread is None or not st.thread.open:
                st.thread = Thread()
            st.mode = "converse"
            thread = st.thread
            st.pending = Async(lambda: communication.speak(thread, text))
    elif 32 <= ch < 127:
        st.buffer += chr(ch)
    return True


def _land(st: State, result) -> None:
    """Integrate a finished off-loop call back into the screen."""
    if isinstance(result, communication.Reply):
        if result.done:                       # satisfied: the thread closes
            st.mode = "input"
            st.thread = None
        else:
            st.mode = "converse"
    elif isinstance(result, str):             # an explain story
        st.explain_text = result
    elif isinstance(result, tree.Node):      # a grilling step; the re-read shows it
        pass
    elif isinstance(result, Exception):       # an error becomes a visible reply
        if st.thread:
            st.thread.add("machine", f"(the architect could not answer: {result})")


# ── painting ──────────────────────────────────────────────────────────────────

def _paint(scr, st: State, nodes, live_loop: bool = True) -> None:
    h, w = scr.getmaxyx()
    if st.mode == "converse":
        rows = render.converse_body(st.thread or Thread(), w, st.explain_text, st.polarity)
    elif st.mode == "view":
        node = view.resolve(view.operator_view(), st.view_path)
        rows = render.view_body(node, st.view_sel, w, st.polarity)
    else:
        rows = render.main_body(nodes, st.sel, w, st.polarity)
    _apply_frame_theme(rows)
    scr.bkgd(" ", _BG_ATTR)
    scr.erase()
    for y, row in enumerate(rows):
        if y >= h - 1:
            break
        _paint_row(scr, y, 2, row, w)
    status = ""
    if st.pending is not None:
        status = SPIN[st.tick % len(SPIN)] + " the machine is thinking"
    foot = render.footer(transport.MODEL_LABEL, st.mode, st.buffer, status, w, live_loop=live_loop)
    _paint_row(scr, h - 1, 0, foot, w)
    scr.noutrefresh()
    curses.doupdate()


def _paint_row(scr, y: int, x: int, row, w: int) -> None:
    col = x
    for text, style in row:
        if col >= w - 1:
            break
        text = text[: w - 1 - col]
        try:
            scr.addstr(y, col, text, _ATTR.get(style, curses.A_NORMAL))
        except curses.error:
            pass
        col += len(text)


_ATTR: dict[str, int] = {}
_BG_ATTR = curses.A_NORMAL
_THEME_KEY = None


def _init_colors() -> None:
    try:
        curses.start_color()
    except curses.error:
        pass


def _apply_frame_theme(frame: render.Frame) -> None:
    """Map the frame's declared RGB theme to curses pairs; never use terminal-default -1 colors."""
    global _ATTR, _BG_ATTR, _THEME_KEY
    key = _theme_key(frame)
    if key == _THEME_KEY:
        return
    try:
        curses.start_color()
        colors = _color_numbers(frame)
        attrs: dict[str, int] = {}
        for pair, (style, spec) in enumerate(frame.styles.items(), start=1):
            fg = colors.get(spec.foreground, colors["ink"])
            bg = colors["paper"]
            attr = _attr_flags(spec)
            try:
                curses.init_pair(pair, fg, bg)
                attrs[style] = curses.color_pair(pair) | attr
            except curses.error:
                attrs[style] = attr
        _ATTR = attrs
        _BG_ATTR = _ATTR.get(render.CARD, curses.A_NORMAL)
    except curses.error:
        _ATTR = {style: _attr_flags(spec) for style, spec in frame.styles.items()}
        _BG_ATTR = curses.A_NORMAL
    _THEME_KEY = key


def _theme_key(frame: render.Frame):
    return (frame.polarity, frame.ground, tuple((name, hue.rgb(frame.polarity), hue.reserved)
                                               for name, hue in frame.palette.items()))


def _color_numbers(frame: render.Frame) -> dict[str, int]:
    rgb = {"paper": frame.ground.paper, "ink": frame.ground.ink}
    rgb.update({name: hue.rgb(frame.polarity) for name, hue in frame.palette.items()})
    names = list(rgb)
    if _can_define(len(names)):
        try:
            out: dict[str, int] = {}
            for i, name in enumerate(names):
                slot = 16 + i
                curses.init_color(slot, *_curses_rgb(rgb[name]))
                out[name] = slot
            return out
        except curses.error:
            pass
    return {name: _nearest_basic(value) for name, value in rgb.items()}


def _can_define(count: int) -> bool:
    return bool(curses.has_colors()
                and curses.can_change_color()
                and getattr(curses, "COLORS", 0) >= 16 + count)


def _curses_rgb(rgb: render.RGB) -> tuple[int, int, int]:
    return tuple(round(channel * 1000 / 255) for channel in rgb)


def _nearest_basic(rgb: render.RGB) -> int:
    basics = {
        curses.COLOR_BLACK: (0, 0, 0),
        curses.COLOR_RED: (205, 49, 49),
        curses.COLOR_GREEN: (13, 188, 121),
        curses.COLOR_YELLOW: (229, 229, 16),
        curses.COLOR_BLUE: (36, 114, 200),
        curses.COLOR_MAGENTA: (188, 63, 188),
        curses.COLOR_CYAN: (17, 168, 205),
        curses.COLOR_WHITE: (229, 229, 229),
    }
    return min(basics, key=lambda n: _distance(rgb, basics[n]))


def _distance(a: render.RGB, b: render.RGB) -> int:
    return sum((x - y) ** 2 for x, y in zip(a, b))


def _attr_flags(spec: render.StyleSpec) -> int:
    attr = curses.A_NORMAL
    if "bold" in spec.attrs:
        attr |= curses.A_BOLD
    if "dim" in spec.attrs:
        attr |= curses.A_DIM
    return attr
