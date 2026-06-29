"""Fixture support for the interface reasoning-loop scenarios."""
from __future__ import annotations

from dataclasses import dataclass

from .. import reasoning, render, tree, window
from ..communication import Thread


@dataclass
class Fixture:
    thread_loop: reasoning.ReasoningLoop | None = None
    worker_loop: reasoning.ReasoningLoop | None = None
    thread_rows: render.Frame | None = None
    worker_rows: render.Frame | None = None

    def loop_thread(self) -> tuple[bool, str]:
        thread = Thread()
        thread.add("operator", "shape this work")
        thread.add("machine", "first account step from the architect")
        thread.add("machine", "second account step from the architect")
        state = window.State(mode="converse", thread=thread, thread_node_id="architect-thread-node")
        window._dispatch(None, state, window.reasoning_input.LOOP_KEY, tree.read_tree())
        self.thread_loop = state.loop
        if self.thread_loop is None:
            return False, "the architect thread did not open a loop"
        self.thread_rows = render.reasoning_loop_body(self.thread_loop, 76)
        return True, ""

    def loop_worker(self) -> tuple[bool, str]:
        node = tree.file_intent("worker node with a live model working")
        tree.dispatch(node)
        state = window.State(mode="browse")
        window._dispatch(None, state, window.reasoning_input.LOOP_KEY, tree.read_tree())
        self.worker_loop = state.loop
        if self.worker_loop is None:
            return False, "the live worker node did not open a loop"
        self.worker_rows = render.reasoning_loop_body(self.worker_loop, 76)
        return True, ""

    def opens_on_working(self) -> tuple[bool, str]:
        if self.thread_loop is None:
            return False, "the architect's working thread did not open a loop"
        if self.worker_loop is None:
            return False, "the fenced worker's live trace did not open a loop"
        at_rest = tree.file_intent("at-rest node with no model working")
        state = window.State(mode="browse")
        window._dispatch(None, state, window.reasoning_input.LOOP_KEY, [at_rest])
        return ((True, "") if state.loop is None
                else (False, "an at-rest node with no model working opened a loop"))

    def one_surface(self) -> tuple[bool, str]:
        if self.thread_rows is None or self.worker_rows is None:
            return False, "the reasoning loops were not rendered"
        thread_text = _frame_text(self.thread_rows)
        worker_text = _frame_text(self.worker_rows)
        if "reasoning loop" not in thread_text or "reasoning loop" not in worker_text:
            return False, "one or both loops were not painted as the reasoning-loop surface"
        if "architect-thread-node" not in thread_text:
            return False, "the architect thread loop is not scoped to its node"
        if self.worker_loop and self.worker_loop.node_id not in worker_text:
            return False, "the worker trace loop is not scoped to its node"
        return ((True, "") if type(self.thread_rows) is type(self.worker_rows) is render.Frame
                else (False, "the thread and worker trace used divergent surface types"))

    def thread_steerable(self) -> tuple[bool, str]:
        loop = self.thread_loop
        if loop is None:
            return False, "no architect thread loop was opened"
        for action in (reasoning.PRUNE_STEP, reasoning.EDIT_STEP, reasoning.RESET_AND_RERUN):
            if action not in loop.actions:
                return False, f"the thread loop does not offer {action!r}"
        pruned = reasoning.prune_step(loop)
        edited = reasoning.edit_step(loop, "operator-shaped step")
        rerun = reasoning.reset_and_rerun(edited)
        if len(pruned.steps) >= len(loop.steps):
            return False, "pruning a step did not change the thread shape"
        if not any(step.text == "operator-shaped step" for step in edited.steps):
            return False, "editing a step did not change the thread shape"
        return ((True, "") if rerun.effect == "thread reset and rerun"
                else (False, "reset and rerun did not reshape the thread"))

    def trace_read_only(self) -> tuple[bool, str]:
        loop = self.worker_loop
        if loop is None:
            return False, "no worker trace loop was opened"
        if not loop.read_only:
            return False, "the worker trace is not read-only"
        forbidden = {reasoning.PRUNE_STEP, reasoning.EDIT_STEP, reasoning.RESET_AND_RERUN} & set(loop.actions)
        if forbidden:
            return False, f"the worker trace offers step-grain steering: {sorted(forbidden)}"
        needed = {reasoning.PRUNE_NODE, reasoning.REASK_NODE, reasoning.RERUN_NODE}
        if set(loop.actions) != needed:
            return False, f"the worker trace actions are {loop.actions}, not the node-grain set"
        if reasoning.edit_step(loop, "injected edit") != loop:
            return False, "a worker trace accepted a step edit"
        text = _frame_text(self.worker_rows or render.reasoning_loop_body(loop, 76))
        return ((True, "") if "no mid-run injection" in text and "read-only trace" in text
                else (False, "the rendered worker trace does not state its read-only boundary"))

    def trust_from_acting(self) -> tuple[bool, str]:
        loop = self.worker_loop
        if loop is None:
            return False, "no worker trace loop was opened"
        text = _frame_text(self.worker_rows or render.reasoning_loop_body(loop, 76)).lower()
        for cue in ("trust is in what acting changes", "confabulation", "prune node", "re-ask node", "rerun node"):
            if cue not in text:
                return False, f"the trust surface is missing {cue!r}"
        return True, ""


def _frame_text(rows) -> str:
    return "\n".join("".join(text for text, _style in row) for row in rows)
