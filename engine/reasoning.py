"""The live reasoning loop as one small model.

The loop is deliberately an account to act on, not a truth oracle. This module
owns that distinction: thread loops are steerable at the step grain, worker
loops are read-only traces with node-grain acts, and every loop carries the same
caveat about trusting the change an act makes rather than the story's polish.
"""
from __future__ import annotations

from dataclasses import dataclass, replace

from . import tree
from .communication import Thread

ARCHITECT_THREAD = "architect-thread"
FENCED_WORKER = "fenced-worker"

PRUNE_STEP = "prune step"
EDIT_STEP = "edit step"
RESET_AND_RERUN = "reset and rerun"

PRUNE_NODE = "prune node"
REASK_NODE = "re-ask node"
RERUN_NODE = "rerun node"

CAVEAT = (
    "trust is in what acting changes, not in how convincing the account reads; "
    "a model's account of its own reasoning can be a confabulation"
)


@dataclass(frozen=True)
class Step:
    text: str


@dataclass(frozen=True)
class ReasoningLoop:
    source: str
    node_id: str
    subject: str
    steps: tuple[Step, ...]
    selected: int = 0
    effect: str = ""

    @property
    def read_only(self) -> bool:
        return self.source == FENCED_WORKER

    @property
    def actions(self) -> tuple[str, ...]:
        if self.read_only:
            return (PRUNE_NODE, REASK_NODE, RERUN_NODE)
        return (PRUNE_STEP, EDIT_STEP, RESET_AND_RERUN)

    def selected_step(self) -> Step | None:
        if not self.steps:
            return None
        return self.steps[min(max(0, self.selected), len(self.steps) - 1)]


def for_thread(thread: Thread | None, node_id: str = ARCHITECT_THREAD) -> ReasoningLoop | None:
    """Open the architect thread's loop when a visible thread exists."""
    if thread is None:
        return None
    steps = tuple(Step(text) for who, text in thread.turns if who == "machine" and text.strip())
    if not steps:
        steps = (Step("the architect is shaping a reply from this thread"),)
    return ReasoningLoop(ARCHITECT_THREAD, node_id, "architect thread", steps)


def for_node(node: tree.Node | None) -> ReasoningLoop | None:
    """Open a worker trace only for live worker nodes; at-rest nodes have no model working."""
    if node is None or not node.is_live:
        return None
    subject = tree._subject(node.text)
    steps = (
        Step(f"worker is carrying node: {subject}"),
        Step("trace is read-only; act on the node, never inside the worker session"),
    )
    return ReasoningLoop(FENCED_WORKER, node.id, subject, steps)


def first_worker(nodes: list[tree.Node]) -> ReasoningLoop | None:
    return next((loop for n in nodes if (loop := for_node(n)) is not None), None)


def choose(loop: ReasoningLoop, offset: int) -> ReasoningLoop:
    if not loop.steps:
        return loop
    return replace(loop, selected=max(0, min(len(loop.steps) - 1, loop.selected + offset)))


def prune_step(loop: ReasoningLoop) -> ReasoningLoop:
    if loop.read_only or not loop.steps:
        return loop
    steps = loop.steps[:loop.selected] + loop.steps[loop.selected + 1:]
    return replace(loop, steps=steps, selected=max(0, min(loop.selected, len(steps) - 1)),
                   effect="step pruned; the thread shape changed")


def edit_step(loop: ReasoningLoop, text: str) -> ReasoningLoop:
    if loop.read_only or not loop.steps:
        return loop
    steps = list(loop.steps)
    steps[loop.selected] = Step(text.strip() or steps[loop.selected].text)
    return replace(loop, steps=tuple(steps), effect="step edited; the thread shape changed")


def reset_and_rerun(loop: ReasoningLoop) -> ReasoningLoop:
    if loop.read_only:
        return loop
    step = Step("reset and rerun requested from the edited thread shape")
    return replace(loop, steps=(step,), selected=0, effect="thread reset and rerun")


def node_act(loop: ReasoningLoop, action: str) -> ReasoningLoop:
    """Record that a worker action is node-grain; the window performs the tree mutation."""
    if not loop.read_only or action not in loop.actions:
        return loop
    return replace(loop, effect=f"{action}; worker trace left read-only")
