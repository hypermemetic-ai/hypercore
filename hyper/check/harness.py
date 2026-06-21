"""The acceptance harness's shared kit — the bare assert-and-tally and the scripted
transport every slice check is written against.

The harness is itself under the deep-module discipline it exercises: the slice checks
are one module each (`slice1` … `slice6`), so no single file grows past the line-count
budget the architecture review now scans for (the per-slice split ADR 0004 anticipated).
This module holds only what they all share.
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
    order, so a check drives the real graph and the real conditions without an LLM."""
    q = list(replies)
    return lambda _prompt: q.pop(0)
