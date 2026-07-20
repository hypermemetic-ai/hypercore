---
id: doc-54
title: 'pi-sweep A — Task system (Backlog glue, board, guards)'
type: other
created_date: '2026-07-19 16:32'
updated_date: '2026-07-19 16:35'
tags:
  - research
---
# pi-sweep A — Task system: reconciled research report

**Owning task:** T-93 — Evaluate pi-ecosystem replacements for qq surfaces.
**Cluster:** A — Task system (Backlog.md glue, `qq-board`, edit guards).
**Research date:** 2026-07-19. **Overall confidence:** HIGH on keep verdicts; MEDIUM on package coexistence (nothing installed or runtime-tested).
**Settles:** No pi package or combination faithfully replaces qq's Task system; keep Backlog.md, `qq-board`, and both drift-net guards. Adoptable QoL: `@narumitw/pi-plan-mode`, optionally `@juicesharp/rpiv-todo`, opt-in `@narumitw/pi-goal`.
**Decision this informs:** any adoption is its own later Change with its own alignment; this document is evidence, not authorization.

## Owning-agent verification (2026-07-19)

Spot-checked before reconciliation: `@narumitw/pi-plan-mode` exists on the npm registry at 0.20.0 matching the report's claim; qq's guard/hybrid-lifecycle fidelity targets were confirmed against local source (`cockpit/pi/qq-backlog-guard.ts`, `bin/qq-board`). npm web pages 403'd during the sweep; registry API and catalog metadata corroborate versions.

## Cross-cluster adjudications

- **`cc-safety-net`:** rejected here as a backlog-guard replacement (wrong layer — Bash-only, and qq must allow Bash for the backlog CLI). That verdict stands *for this question only*; cluster G (doc-60) ranks it the #1 QoL trial as destructive-command defense-in-depth. The two verdicts answer different questions and do not conflict.
- **`@gotgenes/pi-permission-system`:** HOLD here (unproven decorated-path parity; Pi-only, so the Claude hook stays regardless). Cluster C (doc-56) independently holds permission packages as defense-in-depth inside a sandbox, not as the boundary. Consistent: it shrinks nothing today.
- **Plan-mode packages (`@narumitw/pi-plan-mode` vs Plannotator):** cluster F (doc-59) reached the same adopt-one-not-both conclusion independently. Consistent.

---

# Findings report — pi replacement for qq’s Task system

**Question:** Can maintained Pi-native capabilities or packages replace qq’s Backlog.md integration, Git/PR-derived status board, and edit guards—and which packages add useful task/plan QoL?

**Research snapshot:** 2026-07-19.  
**Overall confidence:** **HIGH** on the replacement decision; **MEDIUM** on package coexistence because nothing was installed or runtime-tested.

**Settled outcome:** No Pi package or package combination faithfully replaces qq’s Task system. Keep Backlog.md, `qq-board`, and both drift-net guards. The best additions are `@narumitw/pi-plan-mode`, optionally `@juicesharp/rpiv-todo`, and—when autonomous persistence is wanted—`@narumitw/pi-goal`. These additions replace nothing qq owns.

## Findings

### Overall verdict: keep Backlog.md + qq glue as-is

**HIGH — KEEP.**

Observed: qq’s system is unusually specific:

- Active Tasks remain untracked in the primary checkout, are updated through the Backlog CLI, then move into the Change checkout and land as tracked Done records in the same PR. That hybrid lifecycle is deliberate, not incidental. [Hybrid Task convention](</home/qqp/projects/qq/backlog/docs/doc-48 - Conventions-—-board-hygiene-Task-vocabulary-board-deep-links.md:62>)
- `qq-board` derives status from local branches, worktrees, `origin` refs, and merged GitHub PRs; preserves Done; degrades safely when `gh` fails or times out; and refuses to rewrite tracked records so the primary checkout remains fast-forwardable. It then refreshes `backlog board` in the terminal pane. [Reconciler implementation](/home/qqp/projects/qq/bin/qq-board:120), [reconciler checks](/home/qqp/projects/qq/tests/test-qq-board.sh:180)
- The Pi guard deterministically normalizes relative paths, `..`, `~`, leading `@`, `file://`, and Unicode spaces before blocking built-in `write`/`edit`, while allowing Bash so Backlog CLI operations and finalization moves remain possible. [Pi guard](/home/qqp/projects/qq/cockpit/pi/qq-backlog-guard.ts:10), [guard fixtures](/home/qqp/projects/qq/tests/test-qq-pi-backlog-guard.sh:58)
- The Claude hook enforces the same invariant on Claude’s structured edit/write path fields. [Claude hook](/home/qqp/projects/qq/bin/qq-claude-backlog-hook:11)

Inference: packages found in the catalog manage session todos, their own Markdown/JSON/SQLite records, or general permissions. None reads Backlog.md records, implements qq’s hybrid tracked/untracked convention, derives status from all four Git/PR surfaces, or renders `backlog board`. Combining them only creates a second task source of truth.

| Candidate | Backlog.md fidelity | Git/PR truth + terminal board | Edit-guard fidelity | Verdict |
|---|---:|---:|---:|---|
| Native Pi | None | None | Extension hook API only | Keep qq |
| `rpiv-todo` | None | None | None | Adopt as QoL only |
| `pi-task` | Own Markdown store | None | None | Reject |
| `pi-goal` | Session state | None | None | Adopt as QoL only |
| `pi-plan-mode` | Session plan | None | Plan-mode safety only | Adopt as QoL only |
| Plannotator | Own plan file | None | Plan-phase restriction only | Shortlist as QoL |
| `@gotgenes/pi-permission-system` | None | None | Partial Pi-only fit | Hold |
| `cc-safety-net` | None | None | Wrong surface—Bash only | Reject |

### Pi 0.80.10 native capabilities

**HIGH — NOT A REPLACEMENT.**

Observed: Pi intentionally omits built-in todos, plan mode, permission prompts, subagents, and background Bash. Its built-in tools are only `read`, `bash`, `edit`, `write`, `grep`, `find`, and `ls`; workflow behavior belongs in extensions and packages. [Pi design principles](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/usage.md#design-principles)

Pi ships example source for a session-replayed todo overlay, plan mode, protected paths, and a permission gate. These are examples rather than installed product capabilities. The todo example has a simple session checklist; the plan example uses a read-only phase and `[DONE:n]` tracking. Neither knows Backlog.md or Git/PR Task truth. [Todo example](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/todo.ts), [plan-mode example](https://github.com/earendil-works/pi/tree/main/packages/coding-agent/examples/extensions/plan-mode)

Inference: Pi’s `tool_call` hook is the correct native mechanism for qq’s 65-line guard, but core Pi does not make that guard, board, or reconciler unnecessary.

### `@juicesharp/rpiv-todo`

**HIGH — ADOPT AS OPTIONAL QoL; REJECT AS TASK-SYSTEM REPLACEMENT.**

Observed: version 1.20.0, published 2026-06-15, MIT, roughly 20K monthly downloads. It provides a live terminal overlay, dependency-aware pending/in-progress/completed todos, `/todos`, and replay from the Pi session branch across reload and compaction. The active monorepo has about 495 stars, recent package commits, and focused lifecycle, rendering, configuration, command, and session-isolation tests. Its Pi peer declaration is broad rather than a documented minimum. [Package](https://pi.dev/packages/%40juicesharp/rpiv-todo), [source and tests](https://github.com/juicesharp/rpiv-mono/tree/main/packages/rpiv-todo)

Inference: this is the strongest lightweight execution-checklist package. It complements a durable qq Task: Backlog records intent and delivery status; `rpiv-todo` exposes the current session’s smaller execution steps.

Residual qq must keep: Backlog.md, `qq-board`, both guards, and the complete hybrid Task lifecycle.

### `@mjasnikovs/pi-task`

**HIGH — REJECT.**

Observed: version 0.18.34, published 2026-07-18, AGPL-3.0-only, Pi ≥0.80, about 19.9K monthly downloads. It is a five-phase spec-orchestration pipeline—refine, research, grill, compose, critique—persisting `.pi-tasks/TASK_NNNN.md`. Engineering signals are strong: 434 commits and 1,637 tests across 107 files. However, its own task records are explicitly hand-editable, automatic commits default on, and its unauthenticated remote server defaults on. [Package and configuration](https://pi.dev/packages/%40mjasnikovs/pi-task), [repository](https://github.com/mjasnikovs/pi-task)

Inference: “Task” here means a resumable specification pipeline, not qq’s durable Task record. The extra storage, automatic commits, and remote control surface would duplicate or alter qq’s operator-owned workflow.

Residual: every qq surface remains; `.pi-tasks` becomes an additional source of state.

### `@narumitw/pi-goal`

**HIGH — ADOPT AS OPT-IN QoL; NOT A REPLACEMENT.**

Observed: version 0.20.0, published 2026-07-18, MIT, Pi ≥0.80.6, about 15.8K monthly downloads. It persists a session-scoped goal through compaction, continues from Pi’s settled boundary, supports token budgets, and requires explicit evidence for completion or a blocker recurring across three consecutive goal turns. Experimental ordered queues are disabled by default. Its active monorepo has about 169 stars, 919 commits, repository-wide checks, and 68 releases. [Package](https://pi.dev/packages/%40narumitw/pi-goal), [maintained monorepo](https://github.com/narumiruna/pi-extensions)

Inference: it supplies a useful autonomy/liveness layer absent from qq without creating a project Task store. Adopt it for long-running work, initially leaving the experimental queue off.

Residual: all durable Task, board, reconciliation, and guard behavior remains in qq.

### `@narumitw/pi-plan-mode`

**HIGH — ADOPT AS THE DEFAULT PLAN-MODE QoL.**

Observed: version 0.20.0, published 2026-07-18, MIT, Pi ≥0.80.6, zero runtime dependencies, about 8.1K monthly downloads. It provides terminal-native read-only exploration, structured operator questions, stored implementation-ready plans, explicit implement/finalize transitions, and fail-closed Bash filtering. Extension/custom tools are disabled during planning unless the operator opts them in. The package is test-covered in the same actively released monorepo as `pi-goal`. [Package](https://pi.dev/packages/%40narumitw/pi-plan-mode), [source](https://github.com/narumiruna/pi-extensions/tree/main/extensions/pi-plan-mode)

Caveat: its own documentation correctly notes that tests/builds can create artifacts and that this is extension-level risk reduction, not an OS sandbox.

Inference: this is a clean fit for qq’s terminal/operator-owned posture. It should store plans in the Pi session, not under `backlog/`, and does not compete with durable Tasks.

Residual: every qq Task-system surface.

### `@plannotator/pi-extension`

**HIGH on functionality; MEDIUM on choosing it for qq — SHORTLIST AS AN ALTERNATIVE TO TERMINAL PLAN MODE.**

Observed: version 0.23.1, published 2026-07-12, MIT OR Apache-2.0, Pi ≥0.74, about 28.8K monthly downloads. It offers browser-based plan annotation and approval, plan diffs, Markdown annotation, and local code/PR review. The repository has about 7.1K stars, 843 commits, 125 releases, active issues/PRs, and tests. [Pi package](https://pi.dev/packages/%40plannotator/pi-extension), [repository](https://github.com/backnotprop/plannotator)

Its Pi documentation says write/edit are restricted to the selected plan file during planning, but later clarifies Bash remains unrestricted and relies on the planning prompt. Thus it is not a general Backlog guard. Any selected plan file must remain outside `backlog/`.

Inference: shortlist it when visual annotation and plan-diff review materially matter. For qq’s normal terminal workflow, `@narumitw/pi-plan-mode` is smaller and more deterministic. Do not install both plan modes without testing command/flag ownership.

Residual: all qq surfaces.

### `@gotgenes/pi-permission-system`

**MEDIUM — HOLD; DO NOT RETIRE EITHER qq GUARD.**

Observed: version 20.8.0, published 2026-07-18, MIT, about 25.4K monthly downloads. It is actively maintained, fail-closed, extensively tested, and supports tool-, Bash-, MCP-, skill-, external-directory-, and path-level allow/ask/deny rules. Per-tool `write`/`edit` path matching covers referenced paths, cwd-normalized absolute paths, and canonical symlink targets. The repository has about 94 stars, 23 open issues, three PRs, and a substantial test tree. [Package](https://pi.dev/packages/%40gotgenes/pi-permission-system), [source and tests](https://github.com/gotgenes/pi-packages/tree/main/packages/pi-permission-system)

A cross-cutting `path` deny on `backlog/**` would be too strong because it would also prevent legitimate Backlog CLI and finalization Bash operations. Per-tool `write`/`edit` rules are the plausible configuration.

Unresolved fidelity: its documented normalization does not establish handling of leading `@`, `file://`, or Unicode-space decoration—the exact fixtures qq deliberately tests. It also covers only Pi, leaving Claude untouched.

Inference: adopt this only if qq wants a broader permission system for unrelated reasons. Keep `qq-backlog-guard.ts` alongside it unless and until the existing fixture suite proves exact parity. On present evidence it shrinks nothing.

Residual: `qq-board`, Backlog coupling, Claude hook, and—pending parity proof—the Pi guard.

### `cc-safety-net`

**HIGH — REJECT AS A BACKLOG GUARD REPLACEMENT.**

Observed: version 1.0.6, published 2026-06-15, MIT, about 10K monthly downloads. It is a well-maintained cross-harness semantic analyzer for destructive shell and Git commands, with CI, code coverage, custom rule tests, about 1.5K stars, and few open issues. [Package](https://pi.dev/packages/cc-safety-net), [repository](https://github.com/kenryu42/cc-safety-net)

Its enforcement surface is Bash command analysis. Custom rules describe command, subcommand, and literal blocked arguments; they do not intercept direct Pi/Claude `write` or `edit` path calls. qq must deliberately allow Bash access to Backlog CLI and `mv`, making this the wrong layer for the managed-Markdown invariant.

Residual: every qq surface. It may be useful as separate destructive-command defense, but that is outside this Task-system decision.

### Other permission candidates

- **MEDIUM — `pi-permission-system`: HOLD behind the gotgenes fork.** It supports deterministic action/resource rules such as path-qualified `write`/`edit` and has tests, but has lower current adoption, less explicit canonical-path coverage, and the same unverified decorated-path/Claude gaps. [Package](https://pi.dev/packages/pi-permission-system), [repository](https://github.com/MasuRii/pi-permission-system)

- **MEDIUM — `pi-permission-modes`: HOLD.** It offers modes, protected symlink-aware paths, Bash analysis, and optional Linux sandboxing, but is very young and lightly adopted. Its stock YOLO mode bypasses protected paths, and linked-worktree sandbox limitations are particularly relevant to qq. Exact `@`/`file://`/Unicode normalization was not established. [Package](https://pi.dev/packages/pi-permission-modes), [repository](https://github.com/wynainfo/pi-permission-modes)

- **HIGH — `pi-approval-guardian`: REJECT for this invariant.** It explicitly documents Pi-compatible `~`, `@`, `file://`, Unicode-space, canonical-path, and symlink normalization—the closest decorated-path coverage found. However, covered calls are decided by an isolated LLM reviewer, and its own documentation says decisions are probabilistic. That is not equivalent to qq’s deterministic path boundary and introduces provider latency. [Package](https://pi.dev/packages/pi-approval-guardian)

### Other task, plan, and board candidates

- **HIGH — `@tintinweb/pi-tasks`: SHORTLIST as a richer alternative to `rpiv-todo`, not alongside it.** Version 0.7.1, MIT, early release, roughly 2.5K monthly downloads; about 139 stars, 47 commits, five issues, ten PRs, and a test directory. It adds Claude-style task tools, dependencies, file locking, session/project stores, a widget, background-process tracking, and optional subagent execution. Default session storage is reasonably isolated, but project mode creates a second `.pi/tasks` project ledger. [Package](https://pi.dev/packages/%40tintinweb/pi-tasks?name=web), [repository](https://github.com/tintinweb/pi-tasks)

- **HIGH — `pi-board`: REJECT.** It is a browser Kanban/sprint product backed by `.pi/board.db`, with manual statuses and no Backlog/Git/PR derivation. Maintenance/adoption signals are weak: version 1.0.5 from April, about 78 monthly downloads, zero stars, no visible test tree, and catalog license metadata is unknown although the page footer says MIT. [Package](https://pi.dev/packages/pi-board), [repository](https://github.com/JPBallares/pi-board)

- **HIGH — `@pedro_klein/pi-todo`: HOLD.** It has a good terminal TUI, repo scoping, due dates, and PR-review capture, but version 0.2.0 has low adoption and stores independent JSON under `~/.config/todo/`. GitHub integration fetches PR metadata for review items; it does not derive Task status from branches or merged PRs. [Package](https://pi.dev/packages/%40pedro_klein/pi-todo)

- **HIGH — `@dreki-gg/pi-plan-mode`: REJECT FOR CURRENT qq.** It has an ambitious committed `.taskman/plans` ledger with plans, tasks, initiatives, dependency projection, reconciliation, model handoff, prototypes, and tests. It is also extremely new—eight repository commits and no stars at inspection—and introduces a second durable planning/task hierarchy. [Package](https://pi.dev/packages/%40dreki-gg/pi-plan-mode), [repository](https://github.com/jalbarrang/pi-plan-mode)

- **HIGH — `@nklisch/pi-agile-workflow`: REJECT WITHIN THIS SCOPE.** It is a fresh, MIT, cross-harness Markdown work substrate with a browser board and 887-commit repository history, but its `.work/{active,backlog,releases,archive}` hierarchy is explicitly a Backlog replacement, not integration. Evaluate it only as a separate product/storage migration. [Package](https://pi.dev/packages/%40nklisch/pi-agile-workflow), [repository](https://github.com/nklisch/skills)

- **HIGH — `taskplane`: REJECT WITHIN THIS SCOPE.** It is a maintained multi-agent orchestration system with worktrees, checkpoint commits, `PROMPT.md`/`STATUS.md`, dependency waves, automated merges, and a web dashboard. It replaces much more of qq’s delivery workflow while still not using Backlog or PR-derived Task status. [Package](https://pi.dev/packages/taskplane), [repository](https://github.com/HenryLach/taskplane)

- **HIGH — `pi-beads-extension`: REJECT.** Version 0.1.0 with low adoption; it integrates the external Beads CLI/store rather than Backlog.md. [Package](https://pi.dev/packages/pi-beads-extension)

- **MEDIUM — catalog screen-outs:** `@0xkobold/pi-task`, `pi-kanban`, `@pi-unipi/kanboard`, `@dustinbyrne/kb`, `board-agent`, `@micka33/pi-tasks`, `@heyhuynhgiabuu/pi-task`, `pi-todo-list`, and `@jerryan/pi-todo-lite` were also screened. Each uses its own SQLite/JSON/Markdown/GitHub/multi-agent task model or offers a smaller session todo implementation with weaker maintenance/adoption signals than the shortlisted packages. None claimed Backlog.md integration or qq-compatible Git/PR reconciliation.

## QoL additions

Recommended adoption order:

1. **ADOPT `@narumitw/pi-plan-mode`** for terminal-native, operator-steered planning before mutation.

2. **ADOPT `@juicesharp/rpiv-todo` optionally** for a visible, compaction-safe session execution checklist. Keep its meaning explicitly subordinate to the durable qq Task.

3. **ADOPT `@narumitw/pi-goal` opt-in** for work that should continue until evidence-backed completion. Leave experimental ordered queues disabled initially.

4. **SHORTLIST Plannotator instead of—not in addition to—the default plan mode** when browser annotation, plan diffs, or visual code review justify its larger surface.

5. **SHORTLIST `@tintinweb/pi-tasks` instead of `rpiv-todo`** only if shared session lists, file locking, background-process state, or dependency DAG execution are required.

No permission package is recommended specifically to shrink qq today.

## Sources

- [qq reconciler](/home/qqp/projects/qq/bin/qq-board:120), [hybrid convention](</home/qqp/projects/qq/backlog/docs/doc-48 - Conventions-—-board-hygiene-Task-vocabulary-board-deep-links.md:62>), and [qq guard tests](/home/qqp/projects/qq/tests/test-qq-pi-backlog-guard.sh:58) settled the actual fidelity target.
- [Pi usage/design documentation](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/usage.md#design-principles), [package documentation](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md), and shipped [todo](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/todo.ts)/[plan](https://github.com/earendil-works/pi/tree/main/packages/coding-agent/examples/extensions/plan-mode) examples settled native capability boundaries. Context7’s `/earendil-works/pi` coverage corroborated these API facts; canonical Pi sources are cited here.
- The linked Pi catalog pages settled registry versions, dates, downloads, install forms, license metadata, manifests, README behavior, and declared compatibility.
- The linked GitHub repositories settled source layout, test presence, maintenance activity, releases, and issue/PR signals.

## Gaps

- Direct npmjs package pages returned HTTP 403 during the sweep. Registry-backed metadata and full README content from Pi’s catalog, plus repository manifests/source, were used instead.
- Research was deliberately read-only: packages were not installed, so Pi 0.80.10 runtime compatibility, command collisions, widget layout coexistence, and multiple `tool_call` handler ordering remain untested.
- Exact decorated-path parity for `@gotgenes/pi-permission-system`, upstream `pi-permission-system`, and `pi-permission-modes` is unresolved because their documentation/source did not establish all of `@`, `file://`, and Unicode-space behavior.
- A few catalog releases were newer than cached repository manifests or visible GitHub releases by one version. Catalog metadata was treated as authoritative for publication state and repositories as authoritative for source/test structure.
- Download, star, issue, and package counts are a live 2026-07-19 snapshot. The catalog changed during the investigation as new packages were indexed; very new packages do not yet have meaningful maintenance history.
