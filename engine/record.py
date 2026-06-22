"""The one record — how an act lands durably and reaches git, single-writer.

The graph is hypercore's source of truth, but *writing* it is a concern of its own: an act lands on
disk atomically the instant it is made, and the durable git commit follows behind, never gating the
act (intent §work). This module is that write layer, the floor the graph's mutations and the fold rest
on. It hides three things behind a small interface:

- **`atomic_write`** — replace a file in one step (write a temp beside it, `os.replace`), so a reader
  never sees a half-written act and a crash never leaves a torn file.
- **`commit`** — stage the named paths and commit them, swallowing failure: the act is already on
  disk, so a failed commit loses nothing. `-A` is scoped to the given paths, so concurrent commits to
  different paths never sweep each other's work into one commit.
- **single-writer (`serialized` / `LINE`)** — concurrent workers each build in their own fence (intent
  §62), but the git-touching acts that reach the shared line must not interleave, or two `git`
  invocations collide on the index. `serialized` holds the one lock across a git-touching act; the slow
  build never runs under it, so the record stays consistent while the builds still overlap.

`_root` lives here too — where the record is rooted (the repo, or `ENGINE_ROOT` under the harness) —
because it is what `commit` writes against; the graph re-exports it so its callers read one façade.
"""
from __future__ import annotations

import functools
import os
import subprocess
import tempfile
import threading

_HERE = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_ROOT = os.path.dirname(_HERE)

# The one record is single-writer (intent §62): serializing the git-touching acts keeps concurrent
# workers from colliding on the index, while their slow builds run outside the lock and overlap.
LINE = threading.RLock()


def _root() -> str:
    return os.environ.get("ENGINE_ROOT", _DEFAULT_ROOT)


def serialized(fn):
    """Run a git-touching act under the one record lock, so concurrent crossings reach the record one
    at a time, never their builds. Reentrant — a guarded act may call `commit` within."""
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        with LINE:
            return fn(*args, **kwargs)
    return wrapped


def atomic_write(path: str, text: str) -> None:
    d = os.path.dirname(path)
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d)
    with os.fdopen(fd, "w") as f:
        f.write(text)
    os.replace(tmp, path)                      # atomic; the act lands here


@serialized
def commit(paths: list[str], message: str) -> None:
    try:
        subprocess.run(["git", "add", "-A", *paths], cwd=_root(), check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "commit", "-m", message], cwd=_root(), check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass  # already on disk; a failed commit does not lose the act
