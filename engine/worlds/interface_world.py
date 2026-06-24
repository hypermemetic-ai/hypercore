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

from .. import render, tree
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
        self.rows = None

    # ── action verbs ──────────────────────────────────────────────────────────────
    def _v_card(self, args: list[str]) -> tuple[bool, str]:
        """card — raise one machine-owned card and one piece of standing work, so the rendered frame
        carries real queue and work content, not an empty surface."""
        tree.raise_card("a real fork the operator must reason through", kind="decide")
        tree.file_intent("a standing piece of work")
        return True, ""

    def _v_render(self, args: list[str]) -> tuple[bool, str]:
        """render — build the resting face for the current tree and a selection, as a pure function;
        the call runs with no terminal, so a returned frame is itself the off-a-TTY proof."""
        self.rows = render.main_body(tree.read_tree(), 0)
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

    def teardown(self) -> None:
        if self._prev_root is None:
            os.environ.pop("ENGINE_ROOT", None)
        else:
            os.environ["ENGINE_ROOT"] = self._prev_root
        shutil.rmtree(self.root, ignore_errors=True)
