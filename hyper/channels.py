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

`depth` is the first and, today, only target. The minimal shared agents file (role-assembly step 3)
and the architect's methodology skills (step 4) join `CHANNELS` as their steps land — each its own
module's `materialize`, the registry the only place that knows the set.
"""
from __future__ import annotations

from . import depth

# The static channels, in render order. Each renders its artifact from the spec and returns the path
# written; new channels (the agents file, the architect's skills) append here as their steps land.
CHANNELS = (depth.materialize,)


def materialize(root: str | None = None) -> list[str]:
    """Regenerate every static channel from source; return the artifact paths written. The fold's
    render step — called by `delta.fold` so the derived artifacts follow the spec with no second
    step to remember and no window in which a committed artifact disagrees with its source."""
    return [render(root) for render in CHANNELS]
