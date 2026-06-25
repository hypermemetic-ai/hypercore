---
kind: ask
state: standing
owner: operator
created: 1782355621
---
Two coding-assistant sessions working *on* hypercore ran concurrently and clobbered each other,
forcing a hard reset. The first read blamed the *sessions* — two editors on one working tree, raw
commits to `main` — and pointed at fencing the editor the way a worker is fenced. Investigation
reframed it. The durable-write floor already holds across processes (`engine/record.py`: the line is
an in-process lock backed by a repo-level `flock`, so a second `python3 -m engine`, a stray `git`, or
the operator's editor cannot race the index), and the head-end acts — file intent, grill, ratify —
land as node-scoped serialized commits, so two foreground sessions filing different asks are already
safe.

The worry is not a session writing out of place — it is **the system writing in itself**. Every
window starts its own autonomous loop (`window.py`: `schedule.Scheduler()` then `start()`), so two
windows run two schedulers over one tree, and the loop's orchestration invariants are true per process
and false across processes. This does not merely fail to coordinate; it corrupts. `_recover_stranded`
resets any in-flight node not in *this* scheduler's threads, so one loop yanks the other's live work
back to standing — deterministic, every poll. And `step` double-dispatches a still-standing node
across the read→IN_FLIGHT window, putting two fenced workers on one ask.

Make the system's self-writing single-instance: exactly one autonomous loop runs against a tree,
elected by a held repo-level lease — the `flock` shape the record already uses, held for the loop's
life, self-healing when its holder dies. A second window stays a full operator window — browse, file,
grill, ratify, all parallel-safe — minus the loop. That one change restores the invariants
`_recover_stranded` and `dispatch` already assume. Out of scope: fencing editor sessions in their own
worktrees, and the raw-`git`-to-`main` path a session takes *around* the engine — the engine guards
its own door; a session that walks around it is a separate concern, not this one.
