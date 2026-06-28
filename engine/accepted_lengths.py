"""The accepted-length ledger's durable read.

The ledger is authored state, but reading its durable form is lower-level knowledge than either gate
that consults it. The depth gate writes through its single writer seam; the provenance gate compares the
working-tree ledger with the committed ledger. This module owns only the common read: the ledger path,
the accepted-line grammar, and the working-vs-committed views.

It deliberately imports no engine siblings. The gates rest on it; it never reaches back up to them.
"""
from __future__ import annotations

import os
import subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_ROOT = os.path.dirname(_HERE)
LEDGER = os.path.join("engine", "accepted-lengths.md")


def path(root: str | None = None) -> str:
    """The ledger file in a repo root. `ENGINE_ROOT` is honored for harness-rooted runs."""
    return os.path.join(_root(root), LEDGER)


def accepted_at(rel: str, root: str | None = None) -> int | None:
    """The highest accepted bar recorded for `rel`, or None when the ledger names no bound."""
    want = rel.replace(os.sep, "/")
    f = path(root)
    if not os.path.isfile(f):
        return None
    bars = [rec[1] for line in open(f, encoding="utf-8", errors="ignore")
            if (rec := record(line)) and rec[0] == want]
    return max(bars) if bars else None


def working_records(root: str | None = None) -> set[tuple[str, int]]:
    """Every accepted-length record visible in the working-tree ledger."""
    f = path(root)
    return records(open(f, encoding="utf-8", errors="ignore").read()) if os.path.isfile(f) else set()


def committed_records(root: str | None = None) -> set[tuple[str, int]]:
    """Every accepted-length record committed at HEAD."""
    return records(_committed_text(root))


def records(text: str) -> set[tuple[str, int]]:
    """Every parseable accepted-length line in `text`."""
    return {rec for line in text.splitlines() if (rec := record(line))}


def record(line: str) -> tuple[str, int] | None:
    """Parse one `accepted: <path> @<N> - ...` line to `(path, accepted_length)`, or None.

    A line is an accepted-length record only with the exact `accepted:` prefix and an `@<N>` token
    naming an integer length. A record with no `@<N>`, or prose that merely mentions a path, does not
    clear anything.
    """
    text = line.strip()
    if not text.lower().startswith("accepted:"):
        return None
    parts = text.split(":", 1)[1].split()
    if len(parts) < 2:
        return None
    rel = parts[0].rstrip(",").replace(os.sep, "/")
    for tok in parts[1:]:
        if (n := _accepted_length(tok)) is not None:
            return (rel, n)
    return None


def _committed_text(root: str | None) -> str:
    """The ledger text at HEAD, or empty when no ledger is committed."""
    r = subprocess.run(["git", "show", f"HEAD:{LEDGER}"], cwd=_root(root),
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def _accepted_length(token: str) -> int | None:
    """`@<N>` -> N; anything else -> None. Tolerant of trailing punctuation."""
    t = token.strip(",.—-").lower()
    digits = t[1:] if t.startswith("@") else ""
    return int(digits) if digits.isdigit() else None


def _root(root: str | None) -> str:
    return root or os.environ.get("ENGINE_ROOT", _DEFAULT_ROOT)
