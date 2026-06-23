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

The skills were the first targets — the architect's four methodologies and the worker's `depth`, each
rendered by `methodology` from its capability slice into both the harness-neutral `skills/` and the
`.claude/skills/` location stock Claude Code discovers (role-assembly step 4; depth normalized into a
capability); and the minimal shared **agents file** (`anchor`, step 3) is the always-on
anchor both roles load, reached through a derived `CLAUDE.md` bridge that imports it (`@AGENTS.md`),
because Claude Code reads `CLAUDE.md`, not a bare `AGENTS.md` — the bridge first dropped as redundant,
reinstated as a derived import once the harness fact was verified. The registry is the only
place that knows the set.
"""
from __future__ import annotations

from . import anchor, methodology

# The static channels, in render order — each a `(root) -> path` render of one artifact from the spec.
# `methodology.materializers()` splices in one render per capability skill per mirrored location (the
# architect's four methodologies and the worker's `depth`, into `skills/` and `.claude/skills/`);
# `anchor.materialize` writes the shared agents file; `anchor.bridge_materialize` writes the `CLAUDE.md`
# import that lands the anchor where Claude Code reads it. New channels append here.
CHANNELS = (*methodology.materializers(), anchor.materialize, anchor.bridge_materialize)


def materialize(root: str | None = None) -> list[str]:
    """Regenerate every static channel from source; return the artifact paths written. The fold's
    render step — called by `delta.fold` so the derived artifacts follow the spec with no second
    step to remember and no window in which a committed artifact disagrees with its source."""
    return [render(root) for render in CHANNELS]
