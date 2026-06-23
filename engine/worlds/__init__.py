"""Per-capability scenario worlds — the fixtures the scenario binding runs check blocks against.

A capability's `#### Scenario:` check block names domain verbs; the **World** for that capability is the
deep layer that turns each verb into an assertion over the real engine seams. The core
(`engine.scenario`) owns parsing, the runner, and the fold gate; this package owns the per-capability
fixtures — **one module each** — so no single file carries every capability's vocabulary. That is the
god-module the binding-contest's watched trigger named: the verb vocabulary is split along the
capability seam *before* it forms, never after.

`for_capability` is the one seam the core reaches the worlds through: it lazily imports
`engine.worlds.<capability>` (hyphens→underscores) and returns its `World`. The import is lazy so a
new world never risks an import cycle at load and the core depends on no world by name. A capability
with no world module yet resolves to the bare `World`, whose every verb is unknown — a check block
cannot run without the world that gives its verbs meaning, so an unmigrated capability fails honestly
rather than passing on an empty fixture.
"""
from __future__ import annotations

import importlib
import importlib.util


class World:
    """A scenario fixture's base: the `verb args` → `_v_<verb>` dispatch every world shares, and a
    no-op teardown a world overrides to drop whatever it planted. A capability's World subclass builds
    its fixture in `__init__` and provides the `_v_*` methods its scenarios name."""

    def do(self, verb: str, args: list[str]) -> tuple[bool, str]:
        m = getattr(self, f"_v_{verb}", None)
        return m(args) if m else (False, f"unknown scenario verb {verb!r}")

    def teardown(self) -> None:
        pass


def for_capability(capability: str) -> World:
    """The World for a capability — its fixture module lazily imported and instantiated, or the bare
    base when none is registered yet. `find_spec` distinguishes "no world module" (return the base)
    from a real import error inside a world (let it raise, surfacing as a red, not a silent pass)."""
    name = capability.replace("-", "_")
    if importlib.util.find_spec(f".{name}", __package__) is None:
        return World()
    return importlib.import_module(f".{name}", __package__).World()
