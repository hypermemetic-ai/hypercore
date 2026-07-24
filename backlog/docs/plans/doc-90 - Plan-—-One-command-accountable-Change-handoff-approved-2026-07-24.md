---
id: doc-90
title: Plan — One-command accountable Change handoff (approved 2026-07-24)
type: specification
created_date: '2026-07-24 07:27'
updated_date: '2026-07-24 07:28'
tags:
  - plan
  - handoff
  - pi
  - herdr
  - delivery
---
# Plan — One-command accountable Change handoff

- **Approved:** 2026-07-24 asked-and-answered operator alignment exchange
- **Owning Task:** T-155
- **Command:** `/handoff <Task-ID>`
- **Engine:** `bin/qq-handoff`

## Outcome

An accountable owner can transfer an already aligned, already-created Change
to a fresh accountable Pi session with one direct command. The transfer is
observable and fail closed: it resolves one existing Change checkout, verifies
its durable intent and topology, starts one fresh Pi tab in the Repository's
persistent project home, supplies a standard Task-and-plan handoff prompt,
confirms the new session is working, restores operator focus, and returns a
machine-readable receipt.

The command transfers accountability; it is not delegated execution. It does
not create intent, a Task, a plan, a branch, a worktree, a pull request, a
Herdr workspace, or a child run. The receiving Pi session becomes the ordinary
operator-facing accountable owner and follows `deliver-change` through PR
handoff.

## Why an engine and Pi command, not a prompt template

Native Pi prompt templates expand text. The installed
`pi-prompt-template-model` deterministic-step frontmatter can run a command,
but invocation arguments are substituted into prompt bodies rather than the
deterministic command configuration. A dynamic `/handoff T-155` template would
therefore require either an LLM intermediary or shell interpolation in a
lifecycle operation.

qq instead owns the lifecycle operation in one testable command engine. A thin
mounted Pi extension registers `/handoff`, validates its single Task-ID
argument, invokes the engine with structured arguments, and renders the result.
No model turn interprets or reconstructs the handoff.

## Settled boundary

The operator selected:

- `/handoff`, not `/handoff-change`, as the Pi surface;
- a direct Pi command over a tested qq engine, not CLI-only or a prompt
  template;
- existing Change only: V1 never creates or aligns work;
- automatic unique-checkout resolution;
- a fresh Pi tab in the existing persistent project home;
- a standard prompt derived from the Task and attached plan;
- working-state confirmation and restoration of the operator's original focus;
- refusal of missing or ambiguous checkout, duplicate active owner, primary
  `main`, absent decision ledger or approved plan, and failed startup.

`decision-9` remains authoritative: the target is a plain linked worktree and
the new interactive Pi tab lives in project home; no per-Change workspace is
created. T-148 and root `AGENTS.md` remain authoritative: Pi integration and qq's
Herdr tenancy are qq scope, but Herdr itself is external infrastructure.

## Public interface

### Engine

Use a narrow JSON engine interface consistent with qq's other lifecycle tools:

```text
qq-handoff inspect <Task-ID> --repo <path>
qq-handoff start <Task-ID> --repo <path>
```

`inspect` is read-only and returns the resolved candidate plus every rail. It
must not create, focus, start, prompt, close, or otherwise mutate Herdr state.
`start` reruns all rails immediately before mutation; an earlier inspect result
is never authority.

- stdout is one JSON object;
- diagnostics go to stderr;
- exit `0` means success;
- exit `2` means a safe rail refusal;
- exit `1` means an operational error whose receipt reports any created
  resources and cleanup disposition.

The Task ID is syntactically strict and passed as a structured argument. Paths,
labels, prompts, and shell commands are never assembled through evaluation or
unquoted shell interpolation.

### Pi command

The mounted qq extension registers:

```text
/handoff <Task-ID>
```

It requires an interactive root Pi session, passes the current Repository
context to `qq-handoff start`, parses the JSON receipt, and displays the result.
It performs no model call and contains no duplicate lifecycle logic. Missing,
extra, or malformed arguments refuse before engine execution.

## Resolution and preflight rails

Given the caller's Repository context and Task ID:

1. Resolve the Repository root, Git common directory, sole primary `main`
   checkout, and persistent project-home workspace using current qq/Git/Herdr
   evidence. Refuse unrelated or ambiguous topology.
2. Enumerate linked worktrees in that Repository. Exclude the primary checkout,
   detached checkouts, `main`, missing paths, and other repositories.
3. Locate the exact active Task ID in each candidate's Backlog Task records.
   Require exactly one candidate. V1 deliberately refuses Tasks already present
   across multiple branches/checkouts or only on primary `main`; it does not
   guess from branch names, timestamps, labels, or plan prose.
4. Require Task status `To Do` or `In Progress`, a non-empty Description decision
   ledger (the explicit value `none` remains valid), and at least one attached
   Backlog `plans` document that resolves inside the candidate checkout.
5. Require a named non-main branch and an accessible worktree. Dirt is allowed
   and must be preserved: formalized Tasks and plans commonly begin uncommitted.
   The engine never cleans, resets, switches, stages, commits, or stashes.
6. Inspect project-home panes and refuse any existing live Pi agent whose cwd or
   foreground cwd is the target checkout. This prevents two simultaneous
   accountable owners. Shells and historical terminal metadata are not enough
   to claim ownership, but ambiguous process/agent evidence refuses rather than
   guesses.
7. Require the invoking pane/tab to be identifiable in the persistent project
   home so focus can be restored deterministically.

`inspect` returns the normalized Task title, Task path, attached plan paths,
branch, checkout, common directory, home workspace, caller tab/pane, duplicate
owner evidence, and per-rail results.

## Fresh-session prompt

Generate the receiving prompt from fixed qq text plus verified paths and Task
identity. It must instruct the new session to:

- take accountable ownership of the named Change and Task;
- treat the work as aligned and not restart grilling;
- verify branch/checkout and preserve existing dirt;
- read `AGENTS.md`, `CONCEPTS.md`, the exact owning Task, every attached approved
  plan, and the triggered Skills;
- implement only the Task's approved scope and stop on a new consequential
  decision or boundary crossing;
- follow `deliver-change`, including fresh-context review and green Checks,
  through ordinary PR handoff and watch setup;
- never merge;
- report in its own tab rather than using the originating session as a routine
  relay.

Do not copy the originating conversation, summaries, hidden context, or model
state. Durable Task/plan/source evidence is the handoff seam.

## Start transaction and focus behavior

`start` performs these steps in order:

1. Capture the caller's current workspace, tab, and pane.
2. Re-run all inspect rails.
3. Create one no-focus tab in the home workspace at the target checkout. Use a
   bounded label derived from the Task ID/title.
4. Start the canonical `pi` executable through `herdr agent start` with a unique
   bounded agent name and wait for interactive readiness.
5. Submit the fixed handoff prompt through `herdr agent prompt`.
6. Wait for an observed `working` state after submission.
7. Restore the original tab/pane focus even if Herdr focused the new tab during
   prompt submission.
8. Re-inspect the new agent and return the receipt.

Focus restoration is an invariant, not best effort. The command must not leave
the operator moved merely because a handoff succeeded.

## Failure and cleanup rules

- Failure before tab creation changes nothing.
- If tab creation succeeds but Pi startup fails before a live agent exists,
  close only that newly created tab, verify closure, restore focus, and report
  the cleanup evidence.
- Once Pi may be live or a prompt may have been accepted, do not close or kill
  the tab on uncertainty. Preserve tab/pane/session identifiers, restore focus,
  return an error receipt, and let the operator inspect the evidence.
- Never close, rename, focus, prompt, or otherwise modify pre-existing tabs or
  agents except restoring the exact caller focus.
- Timeouts are bounded. A timeout is not proof that a start or prompt failed;
  subsequent inspection determines whether cleanup is safe.

A successful receipt names at least: schema/version, action, Task ID/title/path,
branch, checkout, home workspace, tab, pane, agent name, Pi session identity
when available, observed state, prompt submission, focus restoration, and
cleanup disposition.

## Implementation surfaces

- `bin/qq-handoff` — lifecycle engine; shell or a small language helper may be
  used, but all parsing and mutation must be structured and bounded.
- `extensions/qq-handoff.ts` — `/handoff` registration and JSON rendering only.
- `extensions/index.ts` — mount registration.
- `tests/test-qq-handoff.sh` — deterministic engine topology/lifecycle fixtures.
- `tests/test-qq-handoff-extension.sh` — command argument, execution, and
  rendering harness.
- Existing extension-mount, shell, prose-ratchet, and Repository Checks as
  affected.
- `README.md` and `skills/deliver-change/SKILL.md` — usage and methodology
  placement. Source Changes do not trigger OpenWiki maintenance.

Prefer installed Herdr's documented `workspace`, `tab`, `pane`, and `agent`
commands. Do not drive terminals with raw key injection when `agent start`,
`agent prompt`, and `agent wait` provide structured lifecycle surfaces.

## Checks

### Deterministic engine fixtures

Prove:

- malformed Task IDs and argument combinations refuse;
- no Task candidate, primary-only Task, two candidates, detached/main candidate,
  foreign Repository, terminal Task, missing/empty ledger, missing/unresolved
  plan, missing project home, and ambiguous caller focus all refuse before
  mutation;
- explicit `decision ledger: none` is accepted;
- dirty target checkout is preserved byte-for-byte;
- existing active Pi owner refuses;
- success calls Herdr in the required order, uses the resolved checkout and home
  workspace, submits the exact bounded prompt, observes `working`, restores
  focus, and emits the complete receipt;
- pre-agent startup failure closes only the new tab and verifies cleanup;
- uncertain/live-agent failure preserves the tab and reports identifiers;
- malicious titles, paths, Task content, and Herdr JSON cannot inject commands,
  escape the Repository, corrupt JSON, or bypass rails;
- `inspect` performs no mutating Herdr call.

### Extension fixtures

Prove:

- `/handoff` registers exactly once through `extensions/index.ts`;
- zero, extra, malformed, or option-like arguments refuse without execution;
- one valid Task ID invokes `qq-handoff start` with structured args and current
  Repository context;
- exit `0`, refusal `2`, malformed JSON, and operational error `1` render
  distinct truthful outcomes;
- non-interactive contexts refuse.

### Fresh integration evidence

Run applicable Repository Checks and fresh-context review. Then perform one live
probe on the exact installed qq extension and Herdr/Pi versions using an
approved disposable or real aligned Change whose checkout has no existing Pi
owner. Verify the new tab's cwd, fresh Pi session identity, submitted prompt,
working transition, caller-focus restoration, and structured receipt. Retire
only disposable probe resources with explicit ownership and safe rails; never
close an actual receiving session merely to make the Check tidy.

## Non-goals

- Creating or aligning Tasks, plans, branches, worktrees, Changes, or PRs.
- Choosing scope, intent, models, or implementation approaches.
- Forking/cloning the current Pi session or conversation.
- Delegated/headless execution, subagent lifecycle, or bounded ticket fan-out.
- Generic Herdr session management, non-Pi agents, remote/cross-Repository
  handoff, scheduling, queues, retries, or automatic takeover.
- Closing the originating session or the receiving session after handoff.
- Making Herdr infrastructure part of qq ownership beyond its existing tenancy.
