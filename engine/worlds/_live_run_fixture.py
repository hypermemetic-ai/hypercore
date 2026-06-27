"""Fixture support for the self-model live-run scenarios.

The self-model world is already the broadest fixture in the suite. The live-run scenarios need a
specific sequence — cut a worker worktree, apply a scripted worker hand-off, integrate it, then read
the verdict trace — so that setup lives here as one named helper instead of stretching the world with
another mini-crossing.
"""
from __future__ import annotations

from .. import communication, provenance, transport, tree, worker
from . import scripted

_LIVE_CAP = "demo-live-run"
_LIVE_REQ = "a fenced crossing leaves the live-run trace"


def plant_non_fenced_trace(root: str) -> None:
    node = tree.file_intent("a watched mechanism leaves evidence")
    provenance.commit_verdict(node, "watched-demo", "a watched mechanism left a trace", root)


def fold_fenced_crossing(root: str) -> tuple[bool, str]:
    node = tree.file_intent("a fenced crossing folds")
    worker.worktree(node, root)
    try:
        tree.dispatch(node)
        result = worker.apply(node, scripted(transport.emit(
            worker.WORKER_SCHEMA, {"report": "built it", "delta": _live_delta()})), root)
        reply = communication.integrate(node, result, scripted(transport.emit(
            communication.COHERENCE_SCHEMA, {"coherent": True, "say": "it landed.", "card": None})),
            root)
        return (True, "") if reply.done else (False, "the fenced crossing did not fold")
    finally:
        worker.teardown(node, root)


def _live_delta() -> str:
    return (f"## ADDED — {_LIVE_CAP}\n### Requirement: {_LIVE_REQ}\n"
            "A fenced crossing MUST leave the trace the live-run signal reads.\n"
            "#### Scenario: folded\n- WHEN it folds\n- THEN the trace is present\n")
