"""The derived static channels, materialized on fold — the render step the fold gained.

Each role is grounded across three derived channels (ADR 0009): a minimal **agents file**, on-demand
**skills**, and the per-episode **prompt**. The prompt is *live* — assembled fresh every episode by
`worker.prompt`/`conversation`, so it never goes stale and is never materialized. The other two are
**static artifacts an external harness auto-loads**, so unlike the live-rendered operator view they
cannot be read live: they must be written to disk, and regenerated whenever their source changes.

This module is that regeneration — the single registry of the static channels and the one act,
`materialize`, that re-renders every one from the spec. The fold calls it (`delta.fold`) so the
artifacts follow the spec in the same act that lands the spec change: a committed channel can no more
drift from the spec it derives from than the spec can drift from a folded delta — the by-construction
guarantee `delta.fold` gives the spec and the operator view gives the self-model, pointed at one more
target (ADR 0009 §3, the one new mechanism).

The skills were the first targets — the architect's four methodologies and the worker's `depth`, each
rendered by `methodology` from its capability slice (role-assembly step 4; depth normalized into a
capability in ADR 0019); and the minimal shared **agents file** (`anchor`, step 3) is the last static
channel — the always-on anchor both roles auto-load, derived like the rest (one `AGENTS.md` serves
both roles, the `CLAUDE.md` symlink dropped as redundant — ADR 0009 §4). The registry is the only
place that knows the set.
"""
from __future__ import annotations

from . import anchor, methodology

# The static channels, in render order — each a `(root) -> path` render of one artifact from the spec.
# `methodology.materializers()` splices in one render per capability skill (the architect's four
# methodologies and the worker's `depth`); `anchor` is the shared agents file. New channels append here.
CHANNELS = (*methodology.materializers(), anchor.materialize)


def materialize(root: str | None = None) -> list[str]:
    """Regenerate every static channel from source; return the artifact paths written. The fold's
    render step — called by `delta.fold` so the derived artifacts follow the spec with no second
    step to remember and no window in which a committed artifact disagrees with its source."""
    return [render(root) for render in CHANNELS]
