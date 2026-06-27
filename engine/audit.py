"""The standing drift sweep — the committed tree audited against its own sources, live.

The sibling of the architecture review (`review`): that scan keeps the system **deep** between folds;
this one keeps it **coherent** between folds. It catches the drift a hand-driven fold introduces when
it lands a spec change but skips a step the engine's own fold would have run — the failure mode of
semi-freehanded work, which the scenario gate cannot see because the gate checks each mechanism over a
fixture, never the **committed artifact** the live tree actually carries. Two invariants over
hypercore's own repository:

  - **channel drift** — every derived static channel (`channels`) on disk equals a fresh render from
    the live spec. `channels` promises a committed channel "can no more drift from its source than the
    spec from a folded delta", but that holds only while the fold's render step runs; a fold driven by
    hand that skips it leaves a stale `SKILL.md` no check sees, because `channels`' gated scenarios
    prove the render *mechanism* over a fixture, never the *committed file*. This re-runs the fold's own
    `channels.materialize` into a throwaway tree and diffs, so the sweep can no more drift from the
    channel set than the fold can — it *is* the fold's render, asked whether anything would change.

  - **archival hygiene** — every execution-tree folder under a `work/` (and its nested `archive/`)
    carries its `intent.md` (`tree`: a tree is a folder carrying its ask), and no `work/` or `archive/`
    container sits empty (intent §work: neither exists empty), so a hand-moved fold cannot leave a tree
    without its ask, nor an empty husk the next reader trips on.

Both are facts about the live repository, not behaviors over a fixture — so, like `build_reaches_main`,
they are proven from outside a fold and asserted by the acceptance harness over the real tree. Each
returns the empty list when the tree is current; a regression fills it, and the harness goes red on it.
"""
from __future__ import annotations

import os
import shutil
import tempfile

from . import channels

# Children of a `work/` that hold trees but are not themselves trees: the archive nesting and the git
# worktree pool (`tree`, `worker`). A directory under a `work/` with either name is never a tree folder.
_CONTAINERS = ("archive", "worktrees")

# Pruned from the work-tree walk: a worktree pool is a full repo checkout (its own nested `work/` is not
# this tree's), and the caches are not trees. Hidden dirs (`.git`) are pruned separately.
_PRUNE = ("worktrees", "__pycache__")


def channel_drift(root: str) -> list[str]:
    """Repo-relative paths of committed channels that disagree with a fresh render from the live spec —
    empty when the derived tree is current. Renders through the fold's own `channels.materialize` into a
    throwaway tree carrying a copy of the live spec, then diffs each rendered artifact against the
    committed one, so the sweep reuses the exact render the fold runs and cannot drift from the channel
    set the fold knows."""
    staging = tempfile.mkdtemp(prefix="hc-audit-")
    try:
        shutil.copytree(os.path.join(root, "spec"), os.path.join(staging, "spec"))
        drift = []
        for fresh_path in channels.materialize(staging):
            rel = os.path.relpath(fresh_path, staging)
            if _read(os.path.join(root, rel)) != _read(fresh_path):
                drift.append(rel)
        return sorted(drift)
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def tree_hygiene(root: str) -> list[str]:
    """Archival-hygiene violations over the live work tree — empty when it is well-formed. Every tree
    folder (a directory under a `work/` or its `archive/`, barring the `archive`/`worktrees` containers)
    must carry its `intent.md`, and no `work/` or `archive/` container may sit empty."""
    out = []
    for work in _work_dirs(root):
        here = os.path.relpath(work, root)
        trees = [d for d in _subdirs(work) if d not in _CONTAINERS]
        archive = os.path.join(work, "archive")
        archived = _subdirs(archive) if os.path.isdir(archive) else []

        if not trees and not archived:
            out.append(f"{here}/ — empty work container (no open tree, no archive)")
        if os.path.isdir(archive) and not archived:
            out.append(f"{os.path.relpath(archive, root)}/ — empty archive container")
        for d in trees:
            if not os.path.isfile(os.path.join(work, d, "intent.md")):
                out.append(f"{os.path.join(here, d)}/ — tree folder missing its intent.md")
        for d in archived:
            if not os.path.isfile(os.path.join(archive, d, "intent.md")):
                out.append(f"{os.path.relpath(os.path.join(archive, d), root)}/ — folded tree missing its intent.md")
    return sorted(out)


def _work_dirs(root: str) -> list[str]:
    """Every `work/` container in the live tree — the top one and each nested under a tree folder —
    never descending into a worktree pool (a full checkout whose own `work/` is not this tree's)."""
    dirs = []
    for dirpath, dirnames, _ in os.walk(os.path.join(root, "work")):
        dirnames[:] = [d for d in dirnames if d not in _PRUNE and not d.startswith(".")]
        if os.path.basename(dirpath) == "work":
            dirs.append(dirpath)
    return dirs


def _subdirs(path: str) -> list[str]:
    return sorted(e for e in os.listdir(path)
                  if os.path.isdir(os.path.join(path, e)) and e != "__pycache__" and not e.startswith("."))


def _read(path: str) -> str | None:
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return None
