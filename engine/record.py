"""The one record — how an act lands durably and reaches git, single-writer.

The graph is hypercore's source of truth, but *writing* it is a concern of its own: an act lands on
disk atomically the instant it is made, and the durable git commit follows behind, never gating the
act (intent §work). This module is that write layer, the floor the graph's mutations and the fold rest
on. It hides three things behind a small interface:

- **`atomic_write`** — replace a file in one step (write a temp beside it, `os.replace`), so a reader
  never sees a half-written act and a crash never leaves a torn file.
- **`commit`** — stage **exactly** the named paths and commit them, swallowing failure: the act is
  already on disk, so a failed commit loses nothing. The pathspec is passed after `--`, and a caller
  hands `commit` *its own act's files* (a node's folder, a moved pair, the touched spec files), never a
  shared parent like `work/` — `git add -A -- <dir>` stages the whole subtree under a pathspec, so a
  parent pathspec would sweep a sibling worker's uncommitted change into this commit. Exact paths plus
  the held line are what actually make the record single-writer.
- **single-writer (`serialized` / `LINE`)** — concurrent workers each build in their own fence (intent
  §62), but the git-touching acts that reach the shared line must not interleave, or two `git`
  invocations collide on the index. `serialized` holds the one line across a git-touching act — a
  reentrant in-process lock backed by a repo-level `flock`, so a second `python3 -m engine`, a stray
  `git`, or the operator's editor cannot race the index either. The slow build never runs under it, so
  the record stays consistent while the builds still overlap. `transact` extends the held line to span
  a write *and* its commit as one act, so no foreign temp or half-written sibling state is ever visible
  to a concurrent `git add`.

`_root` lives here too — where the record is rooted (the repo, or `ENGINE_ROOT` under the harness) —
because it is what `commit` writes against; the graph re-exports it so its callers read one façade.
"""
from __future__ import annotations

import contextlib
import fcntl
import functools
import os
import subprocess
import tempfile
import threading

_HERE = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_ROOT = os.path.dirname(_HERE)

# The one record is single-writer (intent §62): serializing the git-touching acts keeps concurrent
# workers from colliding on the index, while their slow builds run outside the line and overlap. The
# line is two locks held as one: an in-process reentrant lock (so threads of one engine serialize and a
# guarded act may nest `commit` within `transact`) backed by a repo-level `flock` (so a *second
# process* — another engine, a stray git, the operator's editor — cannot race the index either). The
# thread lock alone was the C1 lie: it serialized threads of one process and nothing else.
LINE = threading.RLock()

# The per-thread depth of the held line — the `flock` is acquired once at the outermost `serialized`
# entry and released at its exit, so a reentrant nested act (a `commit` inside a `transact`) does not
# re-lock or early-release the cross-process lock. Threaded because the file lock is per-thread.
_local = threading.local()


def _root() -> str:
    return os.environ.get("ENGINE_ROOT", _DEFAULT_ROOT)


def _lockfile(root: str) -> str:
    """The repo-level advisory lock the line holds across a git-touching act — one file per record,
    created on demand, never committed. `.git/` is the natural home: it exists for any record, the
    harness's throwaway roots `git init` it, and it is already ignored by the tree."""
    d = os.path.join(root, ".git")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "hypercore.line.lock")


@contextlib.contextmanager
def _held():
    """Hold the one line — the in-process lock always, and the repo-level `flock` once at the outer
    entry — so concurrent threads *and* concurrent processes reach the record one at a time. Reentrant:
    a nested guarded act (commit within transact) re-enters the thread lock and rides the already-held
    `flock` without re-acquiring it, so the cross-process lock spans exactly the outermost act."""
    with LINE:
        depth = getattr(_local, "depth", 0)
        fd = None
        if depth == 0:
            fd = os.open(_lockfile(_root()), os.O_RDWR | os.O_CREAT, 0o644)
            fcntl.flock(fd, fcntl.LOCK_EX)
            _local.fd = fd
        _local.depth = depth + 1
        try:
            yield
        finally:
            _local.depth -= 1
            if _local.depth == 0 and fd is not None:
                fcntl.flock(fd, fcntl.LOCK_UN)
                os.close(fd)
                _local.fd = None


def serialized(fn):
    """Run a git-touching act under the one record line, so concurrent crossings — threads and
    processes both — reach the record one at a time, never their builds. Reentrant: a guarded act may
    call `commit` within."""
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        with _held():
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
def transact(write, paths: list[str], message: str):
    """One git-touching act, the line held across its write *and* its commit. `write` performs the
    on-disk landing (atomic writes, a folder move) and returns whatever the caller needs; then `paths`
    are staged and committed in the same held line, so no sibling's uncommitted change or live temp is
    ever visible to this commit's `git add`. This is the single-writer guarantee made real: the window
    between landing and commit — where C1's `git add -A work` swept a foreign file — is closed because
    nothing else can touch the index until the act completes."""
    result = write()
    commit(paths, message)
    return result


@serialized
def commit(paths: list[str], message: str) -> None:
    try:
        subprocess.run(["git", "add", "-A", "--", *paths], cwd=_root(), check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "commit", "-m", message], cwd=_root(), check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass  # already on disk; a failed commit does not lose the act
