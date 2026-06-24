"""The acceptance harness's shared kit — the bare assert-and-tally the scenario acceptance path is
written against.

This module holds only the tally every check shares: `ok` asserts one observation and prints its
verdict without raising, so a failed run reports the whole picture rather than stopping at the first
fault, and `reset`/`failures` bracket the run. The acceptance content itself is the capability
scenarios (`scenarios`), compiled from each `spec/<capability>.md` — the by-slice harness this kit
once served is gone, its last group migrated to its own scenarios.
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
