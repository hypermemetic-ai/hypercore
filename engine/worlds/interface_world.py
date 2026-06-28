"""The interface scenario world — the window's pure-frame render, driven through the real
`render.main_body` over an isolated tree.

The verbs name the interface's domain nouns — a frame built off the tree, the styled spans it returns,
the resting face with the queue over the work — never engine symbols or terminal calls, so a worker
rewriting the window has nothing in the scenario to tamper with to pass. The fixture seeds an isolated
`ENGINE_ROOT` git repo and reads the resting face as a pure function of the tree and a selection; the
check itself runs headless, with no TTY attached, which is the proof the render needs none.

Only the interface's **pure-frame** requirements are gated here — the render returns testable spans,
and the resting face shows the queue over the work. The window's other requirements are **watched**,
their honest home the running window (`python3 -m engine`): the operator acting at the keyboard, the
input loop never blocking on durable work (the off-loop threading communication also watches as *the
operator's act never makes them wait*), speaking from anywhere, and opening the operator view by key —
each a live keystroke-loop fact no headless fixture can express without faking a terminal. The root and
`ENGINE_ROOT` are restored and dropped on teardown.
"""
from __future__ import annotations

import os
import shutil
import tempfile

from .. import render, schedule, transport, tree
from ..scenario import _git                                  # the worlds share the core's git helper
from . import World as _Base


class World(_Base):
    """A scenario's fixture: an isolated, git-backed `ENGINE_ROOT` the resting face renders over.
    `card` puts one node on the queue so the frame has content; `render` builds the main body as a pure
    function; the assertion verbs read the span shape and the empty resting face."""

    def __init__(self):
        self._prev_root = os.environ.get("ENGINE_ROOT")
        self.root = tempfile.mkdtemp(prefix="scenario-interface-")
        os.environ["ENGINE_ROOT"] = self.root              # the tree seams read the ambient root; restored on teardown
        for cmd in (("init", "-q"), ("config", "user.email", "scenario@hypercore"),
                    ("config", "user.name", "scenario")):
            _git(self.root, *cmd)
        self.frame: render.Frame | None = None
        self.rows = None
        self.footers: dict[str, render.Row] = {}
        self._loops: list[schedule.Scheduler] = []
        self.arc_parent: tree.Node | None = None
        self.arc_child: tree.Node | None = None

    # ── action verbs ──────────────────────────────────────────────────────────────
    def _v_card(self, args: list[str]) -> tuple[bool, str]:
        """card — raise one machine-owned card and one piece of standing work, so the rendered frame
        carries real queue and work content, not an empty surface."""
        tree.raise_card("a real fork the operator must reason through", kind="decide")
        tree.file_intent("a standing piece of work")
        return True, ""

    def _v_render(self, args: list[str]) -> tuple[bool, str]:
        """render — build the resting face, or a loop-status footer, as a pure function."""
        if args:
            if len(args) != 2 or args[1] not in ("footer-live", "footer-not-live"):
                return False, f"unknown render target {' '.join(args)!r}"
            sched = self._holder() if args[0] == "holder" else self._peer()
            if sched is None:
                return False, f"no {args[0]} loop exists"
            self.footers[args[0]] = render.footer(transport.MODEL_LABEL, "input", "", "", 76,
                                                  live_loop=sched.live)
            text = "".join(t for t, _s in self.footers[args[0]])
            if args[1] == "footer-live":
                return ((True, "") if "not live loop" not in text
                        else (False, "the lease holder footer is marked not-live"))
            return ((True, "") if "not live loop" in text
                    else (False, "the non-holding footer does not show it is not the live loop"))
        self.frame = render.main_body(tree.read_tree(), 0)
        self.rows = self.frame
        return True, ""

    def _v_arc(self, args: list[str]) -> tuple[bool, str]:
        """arc — plant a concurrent work arc: a parent with nested open work, one hidden folded
        result under it for scent, one running branch, and an awaiting card for state-glyph reads."""
        parent = tree.file_intent("root arc that spawned child work")
        child = tree._create("nested at-rest child work", "ask", tree.STANDING, "operator", False,
                             parent=parent.id, message="plant nested child work")
        running = tree._create("running child branch", "ask", tree.STANDING, "operator", False,
                               parent=parent.id, message="plant running child work")
        tree.dispatch(running)
        folded = tree._create("passed folded child result", "ask", tree.STANDING, "operator", False,
                              parent=parent.id, message="plant folded child result")
        tree.archive_in_place(folded)
        tree.raise_card("an awaiting decision the operator must settle", kind="decide")
        self.arc_parent = parent
        self.arc_child = child
        self.frame = render.main_body(tree.read_tree(), 0)
        self.rows = self.frame
        return True, ""

    def _v_loops(self, args: list[str]) -> tuple[bool, str]:
        """loops 2 — open two scheduler loops over the same tree and let one take the lease."""
        if args[0] != "2":
            return False, f"unknown loop count {args[0]!r}"
        self._loops = [schedule.Scheduler(root=self.root, limit=0),
                       schedule.Scheduler(root=self.root, limit=0)]
        for sched in self._loops:
            sched.step()
        return (True, "") if self._holder() and self._peer() else (False, "the loops did not split live/non-live")

    def _v_states(self, args: list[str]) -> tuple[bool, str]:
        """states — build a frame carrying the node states that spend state hues."""
        tree.raise_card("an awaiting decision the operator must settle", kind="decide")
        running = tree.file_intent("a running worker slice")
        tree.dispatch(running)
        tree.file_intent("a standing at-rest slice")
        self.frame = render.main_body(tree.read_tree(), 0)
        self.rows = self.frame
        return True, ""

    # ── assertion verbs ───────────────────────────────────────────────────────────
    def _v_spans(self, args: list[str]) -> tuple[bool, str]:
        """spans — the frame is a list of rows of (text, style) spans, every span a pair of strings,
        computed without any terminal call (the function touches no TTY)."""
        if not isinstance(self.rows, list) or not self.rows:
            return False, "the render returned no rows"
        for row in self.rows:
            if not isinstance(row, list):
                return False, "a frame row is not a list of spans"
            for span in row:
                if not (isinstance(span, tuple) and len(span) == 2
                        and isinstance(span[0], str) and isinstance(span[1], str)):
                    return False, f"a span is not a (text, style) pair: {span!r}"
        return ((True, "") if self.rows[0][0][0] == "hypercore"
                else (False, "the frame does not open on the system's resting face"))

    def _v_ground(self, args: list[str]) -> tuple[bool, str]:
        """ground — the frame carries explicit ink and paper RGB data, with no terminal default slot."""
        frame = self._frame()
        if frame is None:
            return False, "no frame has been rendered"
        if frame.polarity != render.LIGHT:
            return False, f"the default frame polarity is {frame.polarity!r}, not light"
        if not (_rgb(frame.ground.ink) and _rgb(frame.ground.paper)):
            return False, f"the ground is not explicit RGB data: {frame.ground!r}"
        if frame.ground.ink == frame.ground.paper:
            return False, "the ground's ink and paper are the same color"
        if frame.ground.ink != render.ground(render.LIGHT).ink or frame.ground.paper != render.ground(render.LIGHT).paper:
            return False, "the frame ground is not the declared warm-ink/off-white default"
        return True, ""

    def _v_palette(self, args: list[str]) -> tuple[bool, str]:
        """palette — the frame carries a small named palette with exactly one reserved alarm hue."""
        frame = self._frame()
        if frame is None:
            return False, "no frame has been rendered"
        if not frame.palette or len(frame.palette) > 8:
            return False, f"the palette is not the small named set: {list(frame.palette)}"
        bad = [name for name, hue in frame.palette.items()
               if hue.name != name or not _rgb(hue.light) or not _rgb(hue.dark)]
        if bad:
            return False, f"the palette has unnamed or non-RGB hues: {bad}"
        reserved = [name for name, hue in frame.palette.items() if hue.reserved]
        if reserved != ["alarm"]:
            return False, f"the reserved hue is {reserved}, not the single alarm hue"
        spenders = [style for style, spec in frame.styles.items() if spec.foreground == "alarm"]
        return ((True, "") if not spenders
                else (False, f"the alarm hue is already spent by styles: {spenders}"))

    def _v_polarity(self, args: list[str]) -> tuple[bool, str]:
        """polarity — toggling returns the soft-dark ground and preserves palette meanings."""
        frame = self._frame()
        if frame is None:
            return False, "no frame has been rendered"
        dark = frame.toggled()
        if dark.ground.polarity != render.SOFT_DARK:
            return False, f"the toggled frame is {dark.ground.polarity!r}, not soft-dark"
        if dark.ground == frame.ground:
            return False, "the toggled frame did not flip its ground"
        return ((True, "") if dark.palette == frame.palette
                else (False, "toggling polarity changed the named palette"))

    def _v_empty(self, args: list[str]) -> tuple[bool, str]:
        """empty — at rest with nothing awaiting and no standing work, the queue reads its empty line
        and the work reads its empty line, with the queue shown above the work (queue over work)."""
        heads = [i for i, row in enumerate(self.rows) if row and row[0] == ("queue", render.HEAD)]
        works = [i for i, row in enumerate(self.rows) if row and row[0] == ("work", render.HEAD)]
        if not heads or not works:
            return False, "the resting face does not show the queue and the work headings"
        if heads[0] > works[0]:
            return False, "the work is shown above the queue — the resting face must show the queue over the work"
        text = "".join(t for row in self.rows for t, _s in row)
        if "nothing awaiting you" not in text:
            return False, "an empty queue does not read 'nothing awaiting you'"
        return ((True, "") if "no standing work" in text
                else (False, "an empty work list does not read 'no standing work'"))

    def _v_redundant(self, args: list[str]) -> tuple[bool, str]:
        """redundant — every state-hued span shares its row with that state's glyph or word."""
        frame = self._frame()
        if frame is None:
            return False, "no state frame has been rendered"
        plain = "\n".join("".join(text for text, _style in row) for row in frame).lower()
        for word in ("awaiting", "running", "at rest"):
            if word not in plain:
                return False, f"stripping color leaves {word!r} illegible"
        seen: set[str] = set()
        for y, row in enumerate(frame):
            row_text = " ".join(text for text, _style in row).lower()
            for _text, style in row:
                state = frame.styles.get(style, render.StyleSpec("ink")).state
                if not state:
                    continue
                seen.add(state)
                cues = render.STATE_CUES.get(state, ())
                if not any(cue.lower() in row_text for cue in cues):
                    return False, f"row {y} carries {state!r} as color without a redundant cue"
        needed = {"awaiting", "running", "at-rest"}
        return ((True, "") if needed <= seen
                else (False, f"the state frame did not carry state hues for {sorted(needed - seen)}"))

    def _v_nested(self, args: list[str]) -> tuple[bool, str]:
        """nested — the work rows render parent before child, and the child is indented beneath it."""
        if self.rows is None or self.arc_parent is None or self.arc_child is None:
            return False, "no arc frame has been rendered"
        parent_i = _row_index(self.rows, "root arc that spawned child work")
        child_i = _row_index(self.rows, "nested at-rest child work")
        if parent_i is None or child_i is None:
            return False, "the parent or nested child is missing from the work view"
        if parent_i > child_i:
            return False, "the child rendered before the parent"
        parent_indent = _indent(self.rows[parent_i])
        child_indent = _indent(self.rows[child_i])
        return ((True, "") if child_indent > parent_indent
                else (False, "the child is not indented under its parent"))

    def _v_scent(self, args: list[str]) -> tuple[bool, str]:
        """scent — the folded branch is summarized on the parent row: child count, shape, and result."""
        if self.rows is None:
            return False, "no arc frame has been rendered"
        row = _row_text(next((r for r in self.rows if "root arc that spawned child work" in _row_text(r)), []))
        if not row:
            return False, "the folded branch's parent row is missing"
        for cue in ("scent", "3 children", "shape", "passed"):
            if cue not in row:
                return False, f"the folded branch scent is missing {cue!r}: {row!r}"
        if "·" == row.strip()[:1]:
            return False, "the folded branch is an opaque dot"
        return True, ""

    def _v_glyph_first(self, args: list[str]) -> tuple[bool, str]:
        """glyph-first — each node state has a distinct leading glyph with color ignored."""
        frame = self._frame()
        if frame is None:
            return False, "no state frame has been rendered"
        glyphs: dict[str, str] = {}
        for row in frame:
            state = _node_state(frame, row)
            if state:
                glyphs.setdefault(state, _leading_glyph(row))
        needed = {"awaiting", "running", "at-rest"}
        missing = needed - set(glyphs)
        if missing:
            return False, f"the frame is missing state rows for {sorted(missing)}"
        if any(not glyphs[state] for state in needed):
            return False, f"a state row has no leading glyph: {glyphs}"
        if len({glyphs[state] for state in needed}) != len(needed):
            return False, f"state glyphs are not distinct: {glyphs}"
        expected = {"awaiting": "?", "at-rest": "○"}
        for state, glyph in expected.items():
            if glyphs[state] != glyph:
                return False, f"{state} reads from {glyphs[state]!r}, not the glyph {glyph!r}"
        return ((True, "") if glyphs["running"] in render.PULSE_GLYPHS
                else (False, f"running reads from {glyphs['running']!r}, not the pulse glyph"))

    def _v_pulse(self, args: list[str]) -> tuple[bool, str]:
        """pulse — exactly running rows carry the pulse marker."""
        frame = self._frame()
        if frame is None:
            return False, "no state frame has been rendered"
        for y, row in enumerate(frame):
            text = _row_text(row)
            has_pulse = any(g in text for g in render.PULSE_GLYPHS)
            is_running = _node_state(frame, row) == "running"
            if has_pulse != is_running:
                return False, f"row {y} pulse={has_pulse} running={is_running}: {text!r}"
        return True, ""

    def _v_footer_live(self, args: list[str]) -> tuple[bool, str]:
        """footer-live — the rendered footer does not mark the lease holder as non-live."""
        text = "".join(t for t, _s in self.footers.get("holder", []))
        return ((True, "") if "not live loop" not in text
                else (False, "the lease holder footer is marked not-live"))

    def _v_footer_not_live(self, args: list[str]) -> tuple[bool, str]:
        """footer-not-live — the rendered footer marks the non-holder as not the live loop."""
        text = "".join(t for t, _s in self.footers.get("peer", []))
        return ((True, "") if "not live loop" in text
                else (False, "the non-holding footer does not show it is not the live loop"))

    def _holder(self) -> schedule.Scheduler | None:
        return next((s for s in self._loops if s.live), None)

    def _peer(self) -> schedule.Scheduler | None:
        return next((s for s in self._loops if not s.live), None)

    def _frame(self) -> render.Frame | None:
        return self.frame if isinstance(self.frame, render.Frame) else None

    def teardown(self) -> None:
        for sched in self._loops:
            sched.stop()
        if self._prev_root is None:
            os.environ.pop("ENGINE_ROOT", None)
        else:
            os.environ["ENGINE_ROOT"] = self._prev_root
        shutil.rmtree(self.root, ignore_errors=True)


def _rgb(value) -> bool:
    return (isinstance(value, tuple) and len(value) == 3
            and all(isinstance(c, int) and 0 <= c <= 255 for c in value))


def _row_text(row) -> str:
    return "".join(text for text, _style in row)


def _row_index(rows, needle: str) -> int | None:
    return next((i for i, row in enumerate(rows) if needle in _row_text(row)), None)


def _indent(row) -> int:
    text = _row_text(row)
    return len(text) - len(text.lstrip(" "))


def _leading_glyph(row) -> str:
    text = _row_text(row).lstrip()
    return text[:1]


def _node_state(frame: render.Frame, row) -> str:
    row_text = _row_text(row).lower()
    states = {frame.styles.get(style, render.StyleSpec("ink")).state for _text, style in row}
    if "running" in states:
        return "running"
    if "awaiting" in states and "awaiting" in row_text:
        return "awaiting"
    if "at-rest" in states and ("at rest" in row_text or "standing" in row_text):
        return "at-rest"
    return ""
