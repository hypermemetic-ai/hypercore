---
kind: ask
state: standing
owner: operator
created: 1782355621
---
Two sessions working *on* hypercore — coding assistants editing this repo as architect/engineer — ran concurrently against one shared working tree and committed directly to `main`, and clobbered each other: interleaved commits, overwritten edits to the same files (`engine/worker.py`, `engine/accepted-lengths.md`), and a muddled state that forced a hard reset to the last clean baseline.

hypercore fences its own *workers* from each other — each builds in its own git worktree, the shared line is single-writer (`engine/record.py`) — but there is no equivalent isolation for the *sessions operating on hypercore*. That asymmetry is the gap: the system protects its parallel workers and leaves its parallel editors unprotected.

Prevent concurrent on-hypercore sessions from conflicting: isolate a session's work the way a worker's is (its own worktree, never the shared main tree directly), or otherwise make concurrent work-on-hypercore safe so two sessions cannot clobber each other's edits or interleave half-finished commits on `main`. Contributing factor to surface in grilling: committing directly to `main` from an interactive session, rather than building on a branch/worktree and integrating, is part of what made the collision possible.
