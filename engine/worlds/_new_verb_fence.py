"""A synthetic fence for the new-verb adequacy scenarios — the fixture that proves the hardened gate
draws the one distinction it must: a brand-new domain verb whose red→green tests the *behavior*, not
merely that the *verb appeared*.

The fence's tip adds a planted capability (`widget`), its scenario naming a **new** verb
(`widget-present`), and that verb's **world fixture** — all absent at the base. The base/tip differ in a
real code behavior (the length signal, lowered base→tip), so a *real* fixture (one that asserts the
behavior) is red at the base and green at the tip, while a *vacuous* fixture (one that asserts nothing)
is green at both. The real gate runs over this fence: with the base run carrying the tip's fixture, the
vacuous verb is caught (green at the base too → no transition → **held**) and the real verb still folds.
Without the carry the vacuous verb would ride base-red (verb unknown) → tip-green and clear the gate
having tested nothing — the hole this node closes. This is heavyweight (a real engine at two commits, the
gate's own checkouts beneath it), so it lives here rather than swelling `self_model_world` past the
length signal, the way `build_reaches_main` is held off the harness for the same reason.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile

from .. import scenario, tree, worker

_REAL = tree._DEFAULT_ROOT                                  # a real, runnable engine + spec to copy into the fence

# The tip adds these three, all absent at the base: the capability, its scenario naming the new verb, and
# the verb's fixture. The verb reads a real code behavior (the lowered length signal) so a real fixture
# transitions red→green; a vacuous one asserts nothing and is green at both ends.
_WIDGET_SPEC = (
    "# widget\n\nA planted capability whose new verb the gate must vouch for.\n\n"
    "### Requirement: the widget verb tests the lowered signal\n"
    "#### Scenario: the new widget verb runs\n"
    "- WHEN the planted new verb runs at a checkout\n- THEN it asserts the lowered length signal\n\n"
    "  ```check\n  widget-present\n  ```\n")

_REAL_VERB = (
    "from .. import conditions\nfrom . import World as _Base\n\n\n"
    "class World(_Base):\n"
    "    def _v_widget_present(self, args):\n"
    "        return (True, \"\") if conditions.SIGNAL < 450 else (False, \"the length signal is not lowered\")\n")

_VACUOUS_VERB = (
    "from . import World as _Base\n\n\n"
    "class World(_Base):\n"
    "    def _v_widget_present(self, args):\n"
    "        return True, \"\"  # asserts nothing — the hollow oracle the gate must refuse\n")

_DELTA = ("# delta — grow widget\n## ADDED — widget\n"
          "### Requirement: the widget verb tests the lowered signal\nThe widget MUST hold.\n")


def run_gate(mode: str) -> str | None:
    """Build a fence for `mode` (`'real'` or `'vacuous'`) and run the **real** scenario gate over it,
    returning its verdict — None when the gate folds, a reason string when it holds. The gate guard is
    cleared for the call so the nested gate genuinely runs: the planted capability is disjoint from any
    gate-calling scenario, so clearing it cannot recurse. The fence is dropped on the way out."""
    fence = _build(mode)
    guard = os.environ.pop(scenario._GATE_GUARD, None)
    try:
        return scenario.gate(worker.WorkerResult("built it", _DELTA, fence), fence)
    finally:
        if guard is not None:
            os.environ[scenario._GATE_GUARD] = guard
        shutil.rmtree(fence, ignore_errors=True)


def _build(mode: str) -> str:
    """A git fence with a real engine + spec at two commits: base lacks the widget capability and its
    verb and carries the unlowered signal; tip adds both and lowers the signal. The new verb's fixture
    is `mode`'s — real or vacuous."""
    f = tempfile.mkdtemp(prefix="new-verb-fence-")
    for c in (("init", "-q"), ("config", "user.email", "nv@hypercore"), ("config", "user.name", "nv")):
        subprocess.run(["git", *c], cwd=f, check=True, stdout=subprocess.DEVNULL)
    for d in ("engine", "spec"):
        shutil.copytree(os.path.join(_REAL, d), os.path.join(f, d), ignore=shutil.ignore_patterns("__pycache__"))
    _set_signal(f, 500); _commit(f, "base — the behavior absent, no widget verb")
    _write(os.path.join(f, "spec", "widget.md"), _WIDGET_SPEC)
    _write(os.path.join(f, "engine", "worlds", "widget_world.py"), _REAL_VERB if mode == "real" else _VACUOUS_VERB)
    _set_signal(f, 400); _commit(f, "tip — the new widget verb and the lowered signal")
    return f


def _set_signal(fence: str, n: int) -> None:
    p = os.path.join(fence, "engine", "conditions.py")
    text = open(p, encoding="utf-8").read()
    open(p, "w", encoding="utf-8").write(re.sub(r"^SIGNAL = \d+", f"SIGNAL = {n}", text, count=1, flags=re.MULTILINE))


def _write(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def _commit(fence: str, msg: str) -> None:
    subprocess.run(["git", "add", "-A"], cwd=fence, check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-q", "-m", msg], cwd=fence, check=True, stdout=subprocess.DEVNULL)
