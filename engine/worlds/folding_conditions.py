"""The folding-conditions scenario world — the four verbs `spec/folding-conditions.md`'s check blocks
name, turned into a real verdict from the `conditions` gate over a planted fixture.

The verbs name domain nouns, never engine symbols or paths-into-the-code, so a worker rewriting the
engine has nothing in the scenario to tamper with to pass. `grow` and `accept` plant material; `gate`
and `spec` read the real gate's verdict on it. The fixture is a throwaway fence (a two-commit git
worktree, so the gate's touched-file diff is well defined) and a throwaway store (where the
accepted-length record lives) — both dropped on teardown.

This is the first world; each migrating capability adds its own module beside it, extending the
vocabulary one verb at a time as its first scenario needs it (`spec/depth.md`'s locality discipline).
"""
from __future__ import annotations

import os
import shutil
import tempfile
from dataclasses import dataclass

from .. import conditions
from ..scenario import _git, _write                          # the worlds share the core's git/write helpers
from . import World as _Base


@dataclass
class _Result:
    """The synthetic hand-off the verbs assert against — the real `conditions` gate reads exactly
    these three fields (its delta, its touched material, its fence)."""
    report: str
    delta: str
    worktree: str


class World(_Base):
    """A scenario's fixture: a throwaway fence (a two-commit git worktree, so the gate's touched-file
    diff is well defined) and a throwaway store (where the accepted-length record lives). The fixture
    verbs plant material; the assertion verbs read the real gate's verdict over it."""

    def __init__(self):
        self.cap = "folding-conditions"
        self.root = tempfile.mkdtemp(prefix="scenario-root-")          # the durable store lives under here
        self.fence = tempfile.mkdtemp(prefix="scenario-fence-")
        for d in (self.root, self.fence):                             # both git-backed: the store commits, the fence diffs
            for cmd in (("init", "-q"), ("config", "user.email", "scenario@hypercore"),
                        ("config", "user.name", "scenario")):
                _git(d, *cmd)
        _write(os.path.join(self.fence, ".keep"), "")
        _git(self.fence, "add", "-A"); _git(self.fence, "commit", "-qm", "base")     # the fork base (HEAD~1)
        self._dirty = self._final = False

    # fixture verbs ───────────────────────────────────────────────────────────
    def _v_grow(self, args: list[str]) -> tuple[bool, str]:
        """grow <path> <past-signal|within-signal|N> — the tree's commit grows a source file to a length."""
        path, n = args[0], self._lines(args[1])
        _write(os.path.join(self.fence, path), f"# scenario fixture: {path}\n" + "x = 0\n" * (n - 1))
        self._dirty = True
        return True, ""

    def _v_accept(self, args: list[str]) -> tuple[bool, str]:
        """accept <path> <@N|none> — record an accepted length through the one writer seam
        (`conditions.accept`, which ratchets: a re-accept at the same or a lower length is a no-op). A
        bare `none` record names no bound and is planted directly, since the writer seam cannot express
        one — that malformed record is exactly what the reader must reject."""
        path, bound = args[0], args[1]
        if bound == "none":
            f = os.path.join(self.root, "engine", "accepted-lengths.md")
            _write(f, (open(f, encoding="utf-8").read() if os.path.isfile(f) else "")
                   + f"accepted: {path} — accepted with no stated length\n")
        else:
            conditions.accept(path, int(bound.lstrip("@")), "deep behind a small interface", self.root)
        return True, ""

    # assertion verbs ───────────────────────────────────────────────────────────
    def _v_gate(self, args: list[str]) -> tuple[bool, str]:
        """gate <held|folds> [because <word> …] [names <path> …] — the real gate's verdict on the
        planted material: held (a folding condition refuses) or folds (every condition met)."""
        reason = self._verdict()
        if args[0] in ("held", "holds"):
            return (self._reason(args[1:], reason) if reason is not None
                    else (False, "expected the gate to hold, but every condition was met"))
        if args[0] in ("folds", "clears"):
            return (True, "") if reason is None else (False, f"expected a fold, but the gate held: {reason}")
        return False, f"unknown gate verdict {args[0]!r}"

    def _v_spec(self, args: list[str]) -> tuple[bool, str]:
        """spec <untouched|folds> — the merge guarantee. `untouched`: a refused condition holds the
        fold, so the delta never reaches the spec. `folds`: every condition met, the delta is free to land."""
        reason = self._verdict()
        if args[0] == "untouched":
            return (True, "") if reason is not None else (False, "expected the spec untouched, but the gate cleared")
        if args[0] == "folds":
            return (True, "") if reason is None else (False, f"expected the delta to fold, but the gate held: {reason}")
        return False, f"unknown spec state {args[0]!r}"

    def _reason(self, args: list[str], reason: str) -> tuple[bool, str]:
        low, i = reason.lower(), 0
        while i < len(args) - 1:
            key, val = args[i], args[i + 1]
            if key == "because" and val.replace("-", " ").lower() not in low:
                return False, f"the gate held but its reason lacks {val!r}: {reason}"
            if key == "names" and val not in reason:
                return False, f"the gate held but its reason does not name {val!r}: {reason}"
            i += 2 if key in ("because", "names") else 1
        return True, ""

    def _verdict(self) -> str | None:
        self._finalize()
        return conditions.material_unmet(_Result("scenario fixture", self._delta(), self.fence), self.root)

    def _delta(self) -> str:
        return (f"# delta — scenario fixture\n## ADDED — {self.cap}\n"
                "### Requirement: scenario fixture\nfixture\n#### Scenario: s\n- WHEN x\n- THEN y\n")

    def _finalize(self) -> None:
        if not self._final:
            _git(self.fence, "add", "-A")
            _git(self.fence, "commit", "-q", *(() if self._dirty else ("--allow-empty",)), "-m", "tip")
            self._final = True

    @staticmethod
    def _lines(spec_: str) -> int:
        return {"past-signal": conditions.SIGNAL + 60,
                "within-signal": max(1, conditions.SIGNAL - 100)}.get(spec_, None) or int(spec_)

    def teardown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)
        shutil.rmtree(self.fence, ignore_errors=True)
