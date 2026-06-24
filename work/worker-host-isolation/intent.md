---
kind: ask
state: standing
owner: operator
created: 2026-06-24
---
# worker-host-isolation — the worker fence must actually isolate the host (PRIORITY)

**The system's core safety claim is currently false.** intent.md §74 promises "the worker's own
worktree is writable, the rest of the host read-only" — an OS-enforced fence, "not a convention a
worker could break by accident." The README records this as the honest limit: the OS fence is
**unbuilt**, and whether a live worker stays in its fence is "watched evidence the first autonomous
run confirms."

The first autonomous run happened (2026-06-24) and confirmed the worst case: **the worker was not
isolated at all.** A live `omp`/gpt-5.5 worker, dispatched on `vocabulary-check` with its cwd set to
its worktree, edited the **main tree** — it wrote a real vocabulary-check build into 11 tracked files
(`engine/conditions.py`, `engine/scenario.py`, `engine/transport.py`,
`engine/worlds/folding_conditions_world.py`, `spec/folding-conditions.md`, `spec/communication.md`,
the derived skills) and a new `engine/vocabulary.py`. cwd is a starting directory, not a fence; a
coding agent reaches the whole filesystem. The leaked build is preserved as evidence at
`scratchpad/leaked-into-main/` (it was reverted from main, never committed).

Why this is the priority, ahead of the other parked findings:
- A worker that can write `main` and the engine's own gate code makes every downstream guarantee
  conditional on the worker's goodwill. The `a-record-a-load-bearing` provenance gate explicitly
  scopes *out* "a role with write access to the repo and the gate itself" as unwinnable — and that
  write access is exactly what every worker has today. Provenance rests on an isolation that does not
  exist; isolation is the foundation the other fixes stand on.
- Concurrency safety (intent §62, §74) assumes workers cannot touch each other's trees or the main
  line. Untested and, by this evidence, unfounded.

The decision to design (parked for grilling next session): what enforces the fence — an OS sandbox
(bubblewrap / a container / seccomp / namespaces / a read-only bind-mount of the host with the
worktree the one writable path), where it wraps the worker's transport (`transport.worker_transport`
sets cwd today — it must set a real jail), and what stays in scope (the net stays open per §74; the
filesystem and the shared `.git` are what must be fenced). The honest-limit framing in the README is
updated by whatever lands here.

## folding condition
- a live worker cannot write any path outside its own worktree: an attempt to modify the main tree,
  a sibling's worktree, or the host fails at the OS level, not by convention — demonstrated by a
  worker that tries to write `main` and cannot;
- the worker's own worktree stays writable and the shared git object store reachable so its commits
  still reach the record (§74);
- `spec/worker.md` (and any capability the chosen mechanism touches) carries the change with its
  scenarios; the README's honest-limit note is corrected; `python3 -m engine --check` is green.

## parked beside this (for a later session, do not start until isolation lands)
- `a-record-a-load-bearing` — provenance gate (grilled + ratified, contract+delta on its node).
- `worker-builds-proposed-delta` — kill the worker's author-from-scratch fallback (design contest
  still owed; the earlier design-decision.md is a retracted hand-fabrication kept as evidence).
- `vocabulary-check`, `operator-view-readiness` — original open asks, never grilled.
