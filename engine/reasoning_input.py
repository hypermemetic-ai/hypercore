"""Keystroke handling for the reasoning loop.

The window owns painting and global dispatch; this module owns the loop's local
keyboard grammar. It mutates the window state by duck type, so the curses window
does not grow a second copy of the loop rules.
"""
from __future__ import annotations

import curses

from . import reasoning, tree

ESC, ENTER, BACKSPACES = 27, (10, 13, curses.KEY_ENTER), (8, 127, curses.KEY_BACKSPACE)
LOOP_KEY = 12  # Ctrl-L


def open_loop(st, nodes) -> bool:
    """Open a loop only from a visible model working: the current thread or a live worker row."""
    loop = (reasoning.for_thread(st.thread, getattr(st, "thread_node_id", reasoning.ARCHITECT_THREAD))
            if st.mode == "converse" else reasoning.first_worker(nodes))
    if loop is None:
        return True
    st.loop = loop
    st.loop_return = st.mode if st.mode != "loop" else "browse"
    st.mode = "loop"
    st.buffer = ""
    return True


def loop_keys(st, ch: int) -> bool:
    loop = st.loop
    if loop is None:
        st.mode = st.loop_return or "browse"
        return True
    if ch == ESC:
        st.mode = st.loop_return or "browse"
        st.loop = None
        st.buffer = ""
    elif ch in (curses.KEY_UP, ord("k")):
        st.loop = reasoning.choose(loop, -1)
    elif ch in (curses.KEY_DOWN, ord("j")):
        st.loop = reasoning.choose(loop, 1)
    elif loop.read_only:
        _worker_loop_act(st, ch, loop)
    else:
        _thread_loop_act(st, ch, loop)
    return True


def loop_editing(st, ch: int) -> bool:
    if st.loop is None:
        st.mode = st.loop_return or "browse"
    elif ch == ESC:
        st.mode = "loop"
        st.buffer = ""
    elif ch in BACKSPACES:
        st.buffer = st.buffer[:-1]
    elif ch in ENTER:
        st.loop = reasoning.edit_step(st.loop, st.buffer)
        st.buffer = ""
        st.mode = "loop"
    elif 32 <= ch < 127:
        st.buffer += chr(ch)
    return True


def _thread_loop_act(st, ch: int, loop: reasoning.ReasoningLoop) -> None:
    if ch == ord("p"):
        st.loop = reasoning.prune_step(loop)
    elif ch == ord("e"):
        step = loop.selected_step()
        st.buffer = step.text if step else ""
        st.mode = "loop-edit"
    elif ch == ord("r"):
        st.loop = reasoning.reset_and_rerun(loop)


def _worker_loop_act(st, ch: int, loop: reasoning.ReasoningLoop) -> None:
    node = tree.find(loop.node_id)
    if node is None:
        st.loop = None
        st.mode = "browse"
    elif ch == ord("p"):
        st.loop = reasoning.node_act(loop, reasoning.PRUNE_NODE)
        tree.cut(node)
        st.loop = None
        st.mode = "browse"
    elif ch == ord("a"):
        tree.raise_card(f"re-ask {tree._subject(node.text)}", kind="decide", parent=node.id)
        st.loop = reasoning.node_act(loop, reasoning.REASK_NODE)
    elif ch == ord("r"):
        tree.recover(node)
        st.loop = reasoning.node_act(loop, reasoning.RERUN_NODE)
