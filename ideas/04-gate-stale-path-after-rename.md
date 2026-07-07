# Gate silently stuck after a repo rename — `no-mistakes init` repairs it

**Status:** _root cause found + one-command repair; wire rename → gate-refresh._

## Symptom
`git push no-mistakes <branch>` **succeeds** (`* [new branch] …`) but no pipeline
runs and no PR ever opens — you sit waiting on a review that never starts.
`no-mistakes status` from the repo says *"repo not initialized."* Looks stalled;
it's actually a dead registration, and the push "success" hides it.

## Root cause
The `hypercore → qq-ac → qq` renames moved the repo directory but never updated the
**no-mistakes gate registration**. The gate stored the repo's working-tree path (in
`~/.no-mistakes/state.sqlite`, table `repos`) and the gate bare repo's
`remote.origin.url` under the *original* identity — `/home/qqp/projects/hypercore`
and `…/hypercore.git`. On every push the notify-push hook `chdir`s to that path to
configure the run's worktree git identity and dies:

```
configure worktree git identity: … chdir /home/qqp/projects/hypercore: no such file or directory
```

notify-push exits 1 → no run is created. But the ref push itself already landed, so
the failure is **silent to the pusher** — only a `remote:` warning line hints at it.
Every branch on that gate is affected at once (this blocked both the methodology
push and the parallel `herdr-pull-agent` push).

## The repair (verified)
Run from the repo at its current path:

```
no-mistakes init      # idempotent: "refreshes the bare repo, repairs the no-mistakes
                      # remote, records the repo in the DB" — corrects path + origin
                      # URL in the SAME gate repo (hash unchanged)
no-mistakes rerun     # trigger the branch that was already pushed
```

After init, `status` shows the correct `repo /home/qqp/projects/qq` +
`remote …/qq.git`, and the already-pushed branch reruns. One `init` fixes every
branch on that gate (it unblocked the parallel session too).

## Prevention
- **Add "refresh the gate" to the repo rename/move checklist:** any no-mistakes repo
  that is renamed or moved needs `no-mistakes init` at the new path. The `qq-ac`
  reframe re-registered the Claude Code plugin but missed the gate — same class of
  miss.
- **Make the trap loud (upstream ask):** a notify-push that fails should not leave
  `git push` looking successful. A `no-mistakes doctor` check that flags a
  registered repo path which no longer exists would have caught this instantly.

_(2026-07-06)_
