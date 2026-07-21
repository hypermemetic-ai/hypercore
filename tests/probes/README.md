# Baseline capability probes

This directory is the stable citation surface for the external contracts that
the qq base batch must preserve. The probes are on-demand Checks, not part of
the non-recursive `tests/test-*.sh` CI glob. Each script is executable,
accepts no arguments, finds the Repository from its own checkout, writes a
UTC-dated capture under `tests/probes/evidence/`, and exits zero only when it
observes the expected boundary behavior.

| Contract | Probe or existing Check | Expected observable outcome | Evidence |
|---|---|---|---|
| Required CI green-gates `main` | [`probe-agent-cannot-merge-main.sh`](probe-agent-cannot-merge-main.sh), plus the `shell-tests` job in [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) | Live ruleset 18942749 is active on the default branch with no bypass actors, requires a PR and the GitHub Actions `shell-tests` status (integration 15368), and blocks deletion/non-fast-forward updates. The scratch PR's required Checks are green before C1 attempts its merge. The operator-only push restriction (classic protection, admin-read-only) is proven from the agent side by the specific "not authorized to push to this branch" line that C2 asserts within its GH013 rejection, not re-read here. | [`evidence/2026-07-17-c1-agent-cannot-merge-main.txt`](evidence/2026-07-17-c1-agent-cannot-merge-main.txt). |
| C1 — agent credentials cannot merge `main` | [`probe-agent-cannot-merge-main.sh`](probe-agent-cannot-merge-main.sh) | With `gh` authenticated as `qqp-bot`, the REST `PUT /pulls/{number}/merge` attempt — made with that same `qqp-bot` token, so no SSH identity check is needed (C1 never pushes to `main`; its scratch-branch push is allowed for any collaborator) — against a green, empty-commit scratch PR is rejected with HTTP 405 carrying the "not authorized to push to this branch" protected-ref denial (405 alone is not accepted). The PR is closed unmerged and its branch deleted. | [`evidence/2026-07-17-c1-agent-cannot-merge-main.txt`](evidence/2026-07-17-c1-agent-cannot-merge-main.txt). Historical baseline: T-37 observed HTTP 405 on green scratch PR #94. |
| C2 — agent credentials cannot push `main` | [`probe-agent-cannot-push-main.sh`](probe-agent-cannot-push-main.sh) | After confirming the git push identity resolves to `qqp-bot` through the repo-pinned `core.sshCommand`, a direct push of a harmless empty commit is rejected with GH013 carrying the specific "not authorized to push to this branch" denial, and the remote `main` SHA remains unchanged. The probe creates no scratch remote ref. | [`evidence/2026-07-17-c2-agent-cannot-push-main.txt`](evidence/2026-07-17-c2-agent-cannot-push-main.txt). Historical baseline: T-37 observed GH013. |
| C4 — parallel writers get separate worktrees | [`probe-parallel-worktrees.sh`](probe-parallel-worktrees.sh) | In a disposable local clone, Git registers two linked worktrees with distinct paths and Git administrative directories. Simultaneous writes to the same relative marker remain isolated, the invoking checkout is untouched, and both worktrees are removed. | [`evidence/2026-07-17-c4-parallel-worktrees.txt`](evidence/2026-07-17-c4-parallel-worktrees.txt). |
| C5 — PR handoff yields a usable URL | [`probe-pr-handoff-url.sh`](probe-pr-handoff-url.sh) | `gh pr create` prints the canonical URL for an empty-commit scratch PR. The URL resolves to the expected open PR, base, branch, and head SHA; after the probe closes the PR and deletes its branch, the URL still resolves to the closed PR. | [`evidence/2026-07-17-c5-pr-handoff-url.txt`](evidence/2026-07-17-c5-pr-handoff-url.txt). |
| C6 — delivery completes with Herdr absent | [`probe-delivery-without-herdr.sh`](probe-delivery-without-herdr.sh) and the full `tests/test-*.sh` Check suite | The probe removes every Herdr-containing directory from `PATH`, verifies `herdr` cannot resolve, and runs the complete shell Check suite successfully. CI has the same no-live-Herdr dependency by construction: its workflow only checks out the Repository and runs that suite; it neither installs nor invokes Herdr. | [`evidence/2026-07-17-c6-delivery-without-herdr.txt`](evidence/2026-07-17-c6-delivery-without-herdr.txt). |

## Running the probes

Local probes need no network or credentials:

```sh
bash tests/probes/probe-parallel-worktrees.sh
bash tests/probes/probe-delivery-without-herdr.sh
```

The remaining probes require network access, an `origin` remote for this
Repository, `gh` authenticated as `qqp-bot`, and the repo-pinned SSH identity:

```sh
bash tests/probes/probe-agent-cannot-merge-main.sh
bash tests/probes/probe-agent-cannot-push-main.sh
bash tests/probes/probe-pr-handoff-url.sh
```

The C1 command re-queries the agent-readable required-CI ruleset before it
attempts the merge, and deliberately uses the REST API for that attempt, never
`gh pr merge`.

## Mutation and cleanup safety

C1 and C5 branch from freshly fetched `origin/main`, create only an empty
commit, and use unique scratch branches and PRs. They close any open scratch
PR, delete its branch, and remove the temporary detached worktree on both the
expected path and failure paths. C2 attempts to update `main` with only an
empty commit and creates no scratch ref. If any protected mutation
unexpectedly succeeds, its probe prints `CRITICAL`, exits non-zero, and cleans
everything it can without rewriting `main`. All three network probes refuse
to begin while `gh` reports an identity other than `qqp-bot`.

Evidence filenames use the probe run's UTC date. Re-running a probe on the
same UTC date replaces that probe's capture; running it on a later date adds a
new dated capture.
