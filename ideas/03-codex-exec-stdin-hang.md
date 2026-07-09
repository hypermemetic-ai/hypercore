# `codex exec` hangs on stdin — always pass `< /dev/null`

**Superseded 2026-07-08 by TASK-8** (worker-pane Build path,
`docs/plans/2026-07-08-orchestrate-codex-panes.md`): orchestrate no longer has
a headless `codex exec` path, so the `< /dev/null` rule below no longer applies
to orchestrate handoffs. The rationale still applies to background side-quest
`codex exec` invocations, including the detached `/idea` subprocess described in
`ideas/01-btw-ideas-skill.md`; this is not a blanket "redirect never needed"
repeal.

**Status:** _known footgun + one-line fix; wire it into `orchestrate`._

## The bug
`codex exec "<prompt>"` (codex-cli 0.142.5) reads stdin and concatenates it onto
the prompt arg. It prints `Reading additional input from stdin...` and blocks until
EOF. Launched non-interactively — a background job, a subshell, any `orchestrate`
handoff — stdin is an inherited-but-never-closed pipe, so it waits **forever** and
never starts the task. It reads as "Codex is slow / the model is stuck"; it's
actually hung before the first token.

Not the priority tier, not `--json`, not the prompt: a trivial
`codex exec "Reply with exactly: ok"` hangs identically across plain / `--json` /
`-c service_tier=default`. (Cost a hung Handoff-1 run plus a parallel diagnostic
chasing tier/json red herrings — all three probes stuck on the same stdin read.)

## The fix
Close stdin. `codex exec "<prompt>" < /dev/null` returns in ~3.7s (verified). The
`Reading additional input from stdin...` line still prints, hits EOF immediately,
and proceeds. For long briefs, prefer a prompt file + closed stdin (also dodges
shell-quoting hell):

```
codex exec --sandbox danger-full-access --skip-git-repo-check "$(cat brief.prompt)" < /dev/null
```

## Where to wire it (so it never recurs)
- **`skills/orchestrate/SKILL.md` step 3 (Build)** — the `codex exec` and
  `codex exec resume --last` handoff lines must show `< /dev/null` (ideally the
  prompt-file pattern). Today they don't, so every handoff is one open stdin away
  from hanging.
- Optional: a thin `bin/qq-codex` wrapper that always appends `< /dev/null` and
  takes the prompt from a file/arg, so the conductor can't forget — orchestrate
  calls `qq-codex` instead of raw `codex exec`.

_(2026-07-06)_
