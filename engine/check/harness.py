"""The acceptance harness's shared kit — the bare assert-and-tally and the scripted
transport every slice check is written against.

The harness is itself under the deep-module discipline it exercises: the slice checks
are one module each (`slice1` … `slice15`), so no single file grows past the length signal
the architecture review scans for — a split along the per-slice seam (locality), not
classitis. This module holds
only what they all share.
"""
from __future__ import annotations

_fails = 0


def reset() -> None:
    global _fails
    _fails = 0


def ok(cond: bool, label: str) -> None:
    """Assert one observation and tally it; print the verdict, never raise — so a
    failed check reports the whole picture rather than stopping at the first fault."""
    global _fails
    if not cond:
        _fails += 1
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")


def failures() -> int:
    return _fails


def scripted(*replies):
    """A deterministic stand-in for the model transport: hand back the queued replies in
    order, so a check drives the real tree and the real conditions without an LLM."""
    q = list(replies)
    return lambda _prompt: q.pop(0)


# A genuinely executable red→green loop for the harness — the feedback-loop gate now EXECUTES the
# command (the keystone), so a fold's loop can no longer be inert prose. Every worker fence commits
# RESULT.md at its tip (HEAD) and not at its fork base (HEAD~1), so this command FAILS at the base
# (red) and PASSES at the tip (green) — a real transition the gate can run, keyed to material the
# worker actually committed. A slice testing something other than the loop itself uses this as its
# loop so its non-trivial delta folds through the real gate.
LOOP = {"command": "test -f RESULT.md",
        "red": "RESULT.md absent at the fork base — the behavior was not yet built",
        "green": "RESULT.md present at the tip — the worker's result is committed"}
