"""The derived static channels, materialized on fold — the render step the fold gained.

Each role is grounded across three derived channels: a minimal **agents file**, on-demand
**skills**, and the per-episode **prompt**. The prompt is *live* — assembled fresh every episode by
`worker.prompt`/`communication`, so it never goes stale and is never materialized. The other two are
**static artifacts an external harness auto-loads**, so unlike the live-rendered operator view they
cannot be read live: they must be written to disk, and regenerated whenever their source changes.

This module is that regeneration — the single registry of the static channels and the one act,
`materialize`, that re-renders every one from the spec. The fold calls it (`delta.fold`) so the
artifacts follow the spec in the same act that lands the spec change: a committed channel can no more
drift from the spec it derives from than the spec can drift from a folded delta — the by-construction
guarantee `delta.fold` gives the spec and the operator view gives the self-model, pointed at one more
target.

The skills were the first targets — the roles' methodologies, including the worker's own discipline and
`depth`, each rendered by `methodology` from its capability slice into both the harness-neutral
`skills/` and the `.claude/skills/` location stock Claude Code discovers (role-assembly step 4; depth
normalized into a capability); and the minimal shared **agents file** (`anchor`, step 3) is the always-on
anchor both roles load, reached through a derived `CLAUDE.md` bridge that imports it (`@AGENTS.md`),
because Claude Code reads `CLAUDE.md`, not a bare `AGENTS.md` — the bridge first dropped as redundant,
reinstated as a derived import once the harness fact was verified. The registry is the only
place that knows the set.
"""
from __future__ import annotations

import json
import os
import subprocess

from . import anchor, methodology

# The static channels, in render order — each a `(root) -> path` render of one artifact from the spec.
# `methodology.materializers()` splices in one render per capability skill per mirrored location (the
# roles' methodology skills, including the worker's own discipline and `depth`, into `skills/` and
# `.claude/skills/`);
# `anchor.materialize` writes the shared agents file; `anchor.bridge_materialize` writes the `CLAUDE.md`
# import that lands the anchor where Claude Code reads it. New channels append here.
CHANNELS = (*methodology.materializers(), anchor.materialize, anchor.bridge_materialize)


def materialize(root: str | None = None) -> list[str]:
    """Regenerate every static channel from source; return the artifact paths written. The fold's
    render step — called by `delta.fold` so the derived artifacts follow the spec with no second
    step to remember and no window in which a committed artifact disagrees with its source."""
    return [render(root) for render in CHANNELS]


def materialize_fresh(import_root: str, render_root: str) -> list[str]:
    """Regenerate `render_root`'s static channels in a fresh interpreter imported from `import_root`.
    This is the registry-agnostic seam: the subprocess imports the on-disk engine at `import_root`, so
    every module-level registry is the one that tree defines, while `ENGINE_ROOT` names the tree whose
    spec and artifacts are read and written."""
    r = subprocess.run(["python3", "-m", "engine", "--materialize"], cwd=import_root,
                       env={**os.environ, "ENGINE_ROOT": render_root},
                       capture_output=True, text=True)
    if r.returncode != 0:
        detail = (r.stderr or r.stdout or "no subprocess detail").strip()
        raise RuntimeError(f"channel materialization failed in the merged tree: {detail}")
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"channel materialization returned unreadable paths: {r.stdout!r}") from e


def materialize_merged(root: str) -> list[str]:
    """Regenerate the on-disk tree's static channels in a fresh interpreter and return the paths it
    wrote. A code-bearing fold calls this after replaying verified engine bytes, so the render imports
    the just-replayed modules and sees their module-level registries instead of this process's frozen
    imports. Spec-only folds keep the cheaper in-process `materialize` path."""
    return materialize_fresh(root, root)
