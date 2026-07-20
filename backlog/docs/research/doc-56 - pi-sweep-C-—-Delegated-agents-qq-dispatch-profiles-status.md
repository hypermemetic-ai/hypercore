---
id: doc-56
title: 'pi-sweep C — Delegated agents (qq-dispatch, profiles, status)'
type: other
created_date: '2026-07-19 16:33'
updated_date: '2026-07-19 16:35'
tags:
  - research
---
# pi-sweep C — Delegated agents: reconciled research report

**Owning task:** T-93 — Evaluate pi-ecosystem replacements for qq surfaces.
**Cluster:** C — Delegated agents (`qq-dispatch`, `codex-profiles/`, `qq-status`, delegate-batch/code-review/research mechanics).
**Research date:** 2026-07-19. **Overall confidence:** HIGH on package capabilities; MEDIUM on the proposed pi-subagents + Landstrip composition until piloted.
**Settles:** The single largest shrink opportunity found in this sweep. Target: `pi-subagents` (orchestration, strict JSON-Schema completion) + Landstrip (OS sandbox via its child-binary wrapper hook), retaining thin qq adapters for process-tree cleanup and herdr stage publishing. Retire `codex-profiles/` and most of `qq-dispatch` only after the 10-point pilot below passes.
**Decision this informs:** a pilot Change, then a migration Change — each with its own alignment; this document is evidence, not authorization.

## Owning-agent verification (2026-07-19)

Spot-checked before reconciliation: `PI_SUBAGENT_PI_BINARY` confirmed in pi-subagents source (`src/runs/shared/pi-spawn.ts:6,139`); package at 0.35.1, MIT. Landstrip peer dependency `^0.80.6` on `@earendil-works/pi-coding-agent` confirmed via npm registry — covers pi 0.80.10 exactly.

## Cross-cluster adjudications

- **Permission packages** (`@gotgenes/pi-permission-system` et al.): held here as defense-in-depth *inside* Landstrip, never the primary boundary. Consistent with doc-54's HOLD, which additionally notes they do not shrink qq's guards today.
- **`pi-herdr-subagents`:** doc-57 shortlists it for visible async children. Sequencing note: it owns child panes, so evaluate it only *after* the delegation-runner decision lands — two packages owning child lifecycle is a conflict class this sweep deliberately declines to resolve by stacking them.
- **`@quintinshaw/pi-dynamic-workflows`:** QoL adopt here is for high-fanout research/review where the process trust boundary is unnecessary; does not interact with doc-57's messaging verdicts.

---

# Findings report

**Question:** What maintained Pi ecosystem combination can replace qq’s delegated-agent stack while preserving role isolation, sandbox enforcement, structured completion, and stage-boundary status publishing?

**Overall confidence:** **High** on package capabilities and comparative verdicts; **medium** on the proposed Pi Subagents + Landstrip integration until it is exercised against qq’s acceptance cases.

**Research date:** July 19, 2026.

**What is settled:** No single package is a faithful drop-in. The strongest target is:

> **`pi-subagents` for orchestration and structured output, plus Landstrip behind its child-binary wrapper hook for OS enforcement, while retaining thin qq-owned adapters for process-tree cleanup and Herdr business-stage publishing.**

Do not retire the current implementation immediately. Pilot the combination first, then shrink it.

## Recommended target

### `pi-subagents` + Landstrip — **ADOPT through a controlled pilot**

`pi-subagents` is the best-maintained delegation substrate found. Version 0.35.1 was published July 18, has substantial adoption, active releases, unit/integration/E2E tests, MIT licensing, and development against Pi 0.80.10. It launches separate Pi child processes and supports fresh context, role-specific prompts, extension/tool restrictions, JSON-Schema completion, timeouts, background execution, persistent event artifacts, worktrees, budgets, model routing, steering, and resume. [Catalog](https://pi.dev/packages/pi-subagents), [repository](https://github.com/nicobailon/pi-subagents), [package metadata](https://github.com/nicobailon/pi-subagents/blob/main/package.json)

Its documented `PI_SUBAGENT_PI_BINARY` hook permits a wrapper in place of the normal Pi executable. Its source also identifies the child role through `PI_SUBAGENT_CHILD_AGENT`. That creates a clean composition point for a qq-owned wrapper that selects a Landstrip policy by role. [Spawn implementation](https://raw.githubusercontent.com/nicobailon/pi-subagents/main/src/runs/shared/pi-spawn.ts), [argument/environment implementation](https://raw.githubusercontent.com/nicobailon/pi-subagents/main/src/runs/shared/pi-args.ts)

Landstrip provides the enforcement that Pi and Pi Subagents intentionally lack: whole-process isolation using Landlock/seccomp on Linux, Seatbelt on macOS, and LPAC AppContainer on Windows. Its Pi package runs full Pi workers inside the sandbox and prevents the agent from widening the outer policy. Current `pi-landstrip` 0.17.30 explicitly supports Pi `>=0.80.6 <0.81.0`, covering 0.80.10. It is Apache-2.0, actively released, tested, and cross-platform, but is much newer and less adopted than Pi Subagents. [Catalog](https://pi.dev/packages/pi-landstrip), [repository](https://github.com/landstrip/landstrip), [Pi integration README](https://github.com/landstrip/landstrip/blob/main/packages/pi-landstrip/README.md)

The composition is an inference from two documented interfaces, not a prepackaged integration. It should be piloted with a wrapper that:

- Reads `PI_SUBAGENT_CHILD_AGENT`.
- Selects reviewer/researcher read-only policies or implementer workspace-write policy.
- Discovers and exposes the Git worktree, common Git directory, and worktree Git directory.
- Fails closed if Landstrip is unavailable.
- Retains qq’s outer GNU `timeout -k 10` or equivalent process-group supervisor until descendant cleanup is proven.
- Preserves compatible final-output and diagnostic artifacts where existing workflows depend on them.

### Fidelity to qq guarantees

| qq behavior | Target fidelity | Residual qq work |
|---|---|---|
| Fresh implementer/reviewer/researcher | Strong, if every agent explicitly uses fresh context and prompt replacement | Define and test role manifests |
| Separate process/session | Strong | Avoid in-process/fork defaults |
| No inherited skills/context | Strong, configurable | Set `inheritSkills:false`, `inheritProjectContext:false`, controlled extensions |
| Reviewer/researcher read-only OS boundary | Strong in design through Landstrip | Author and test fail-closed policies |
| Implementer worktree and Git metadata writes | Achievable | Preserve qq’s Git-directory discovery |
| MCP off/on by role | Achievable through role extension configuration | Preserve explicit allowlists and network policy |
| Structured Completion Envelope | Better: strict JSON Schema can reject prose or malformed results | Encode qq’s envelope fields and semantic rules |
| Timeout and wedged-child handling | Partial | Pi Subagents signals only its direct child; keep qq’s process-tree supervisor |
| Empty-success rejection | Achievable through required schema | Add explicit non-empty/result constraints |
| Machine-readable events and artifacts | Strong | Compatibility adapter only if old paths/formats matter |
| Stage-boundary status publishing | Not provided | Retain qq’s business-stage bridge |
| Owner verification before success | Not an orchestration feature | Retain in skills/workflow |
| Durable owner-managed worktrees | Partial | Keep qq’s lifecycle rules rather than adopting package defaults blindly |

Pi Subagents explicitly warns that its tool restrictions are not an OS sandbox. Its timeout implementation escalates signals to the direct spawned child but does not establish the same process-tree guarantee as qq’s existing supervisor. Landstrip addresses authority, but Linux/macOS orphan teardown under the combined wrapper remains unverified.

## Consequences for current qq surfaces

### `bin/qq-dispatch` — **SHRINK, do not immediately retire**

Replace most orchestration with Pi Subagents, but retain a small, auditable component for:

- Role-to-Landstrip policy selection.
- Worktree/Git-directory discovery.
- Fail-closed sandbox startup.
- Process-group timeout and descendant cleanup.
- Any required artifact compatibility.

Retirement becomes reasonable only after tests show that the selected wrapper/runtime reliably terminates all descendants and emits all required evidence.

### `codex-profiles/` — **RETIRE after the pilot passes**

Move role definitions into Pi Subagents agent manifests plus Landstrip policies. Preserve explicitly:

- Fresh context.
- Full system-prompt replacement.
- Skills and project-context inheritance disabled.
- Reviewer/researcher read-only policy.
- Implementer Git/worktree access.
- MCP/extension allowlists.

The profile symlink verification can disappear only when the replacement has an equally fail-closed policy-loading check.

### `bin/qq-status` — **KEEP, potentially shrink**

Pi Subagents supplies execution liveness, widgets, run states, alerts, logs, `status.json`, and `events.jsonl`. It does not understand qq’s business stages—envelope received, owner verified, review, PR, blocked, failed—or who owns each transition.

Retain qq-status’s stage vocabulary, atomic/monotonic publication, Herdr integration, TTL behavior, and terminal cleanup. A small bridge can consume Pi Subagents lifecycle events, but it should publish only mechanical states. Operator-owned verification and delivery boundaries must remain explicit.

### `delegate-batch`, `code-review`, and `research` skills — **REWRITE mechanics, preserve judgment**

Change their dispatch syntax and completion parsing to Pi Subagents with strict schemas. Keep:

- Work Order construction.
- Worktree ownership.
- Fresh reviewer/researcher requirements.
- Completion Envelope semantics.
- Source and Check verification.
- Owner-only stage transitions.
- Review/research acceptance judgment.

Structured output improves transport correctness; it does not establish that the work is true or complete.

## Candidate findings

### Native Pi subagent example — **HOLD as reference, reject as production replacement**

Pi 0.80.10’s maintained example already uses separate `pi --mode json -p --no-session` processes and supports single, parallel, and chained agents with streaming JSON and abort handling. It is valuable as the canonical mechanism reference. [Native example](https://github.com/earendil-works/pi/tree/main/packages/coding-agent/examples/extensions/subagent)

It has no OS sandbox, strict completion schema, hard wall-clock/process-tree timeout, or external stage publisher. It also does not disable normal skills and context discovery by default.

Pi itself expressly has no built-in permission system: extensions and tools run with the launcher’s permissions, and whole-process containment is recommended for hostile or untrusted work. [Official Pi repository](https://github.com/earendil-works/pi), [extension API](https://pi.dev/docs/latest/extensions), [RPC API](https://pi.dev/docs/latest/rpc)

**Confidence:** High.

### `pi-landstrip` alone — **SHORTLIST, but insufficient alone**

This is the closest single package to replacing the Codex sandbox profiles. It offers genuine whole-agent containment, fresh RPC workers, foreground/background runs, resume, policy-controlled roles, and lifecycle visibility.

It lacks Pi Subagents’ strict JSON-Schema completion, richer run artifacts, and documented hard wall timeout. Its rapid releases, narrow Pi-minor constraint, and modest adoption warrant a controlled rollout.

**Confidence:** High on enforcement; medium on operational maturity.

### `@gotgenes/pi-subagents` — **REJECT as qq substrate**

This package has strong typed APIs, lifecycle events, background UI, steering, resume, and turn limits, but runs children as isolated sessions inside the same Pi runtime. That is context isolation, not a process or authority boundary. No equivalent OS sandbox, process-tree timeout, or strict completion schema was established. [Catalog](https://pi.dev/packages/%40gotgenes/pi-subagents)

**Confidence:** High.

### `@tintinweb/pi-subagents` — **REJECT as substrate; hold its UX ideas**

It offers rich fleet views, worktrees, scheduling, memory, events, and fresh-context options, but also uses Pi SDK sessions in-process. Its own documentation says extension exclusion is not a sandbox. [Catalog](https://pi.dev/packages/%40tintinweb/pi-subagents)

**Confidence:** High.

### `pi-multiagent` — **HOLD for graph-shaped workflows**

It uses persistent child Pi processes and has a useful authority graph, role catalog, status/result protocol, messaging, cancellation, and artifacts. It deliberately avoids inheriting the parent transcript and normal project context. Adoption and maintenance evidence are materially weaker than Pi Subagents, and no OS sandbox or strict completion schema was established. [Catalog](https://pi.dev/packages/pi-multiagent), [repository](https://github.com/Tiziano-AI/pi-multiagent)

**Confidence:** Medium.

### `pi-crew` — **HOLD for experimentation; reject for the security boundary**

It has durable manifests, teams, workflows, worktrees, artifacts, and unusually extensive tests. Its README also states that it is almost entirely AI-generated, has limited human review, is not hardened or audited, and executes dynamic scripts with Pi’s authority. [Catalog](https://pi.dev/packages/pi-crew)

**Confidence:** High.

### `@quintinshaw/pi-dynamic-workflows` — **ADOPT as optional QoL, reject as enforcement**

This is a strong option for high-fanout research and review: JSON-Schema results with bounded repair, retries, persistent journals, checkpoints, live status, judge panels, and real-Pi E2E testing. Version 3.2.0 supports Pi 0.80.10.

Its sessions are in-memory, and its Node VM is explicitly for determinism rather than security. Use it only where qq’s delegated-process trust boundary is unnecessary or where its agents are themselves launched through an approved containment layer. [Catalog](https://pi.dev/packages/%40quintinshaw/pi-dynamic-workflows), [repository](https://github.com/QuintinShaw/pi-dynamic-workflows)

**Confidence:** High.

### Permission packages — **HOLD as defense in depth**

`@gotgenes/pi-permission-system`, `pi-permission-system`, and `pi-permission-modes` provide useful allow/ask/deny policies for tools, commands, MCP, skills, and paths. They do not confine Pi extensions or the entire child process. `pi-permission-modes` confines Bash but handles direct file tools separately and has worktree limitations. [Gotgenes package](https://pi.dev/packages/%40gotgenes/pi-permission-system), [permission-system package](https://pi.dev/packages/pi-permission-system), [permission modes](https://pi.dev/packages/pi-permission-modes)

Use one only for policy clarity and accidental-action prevention inside Landstrip, not as the primary sandbox.

**Confidence:** High.

### `pi-claude-sandbox` — **REJECT**

It kernel-sandboxes Bash, but not Pi’s entire process or direct Read/Write/Edit operations. Adoption is low, and its documentation anticipates possible deprecation. [Catalog](https://pi.dev/packages/pi-claude-sandbox)

**Confidence:** High.

### `pi-herdr-subagents` — **HOLD as Herdr-specific QoL**

It offers dedicated panes, asynchronous execution, status widgets, and process/pane lifecycle management. It could improve live operator visibility, but it neither supplies the security boundary nor replaces qq’s business-stage protocol. Combining it with another subagent runner may also create competing ownership of child processes. [Catalog](https://pi.dev/packages/pi-herdr-subagents)

**Confidence:** High.

### `pi-ultra-subagents` and smaller variants — **REJECT**

`pi-ultra-subagents` has subprocess RPC workers and an explicit finish tool, but adoption and maintenance evidence are weak, and it does not close the sandbox, timeout, or stage-publication gaps. [Catalog](https://pi.dev/packages/pi-ultra-subagents)

The catalog’s other subagent variants—`pi-sub-agent`, `pi-subagentura`, `pi-open-agents`, `pi-submarine`, `@danchamorro/pi-subagents`, `@johnnywu/pi-subagents`, `pi-subagents-j0k3r`, and `@yzlin/pi-subagents`—were screened. They provide variations on panes, background runs, persistence, or forks but have less evidence than the shortlisted packages and retain the same enforcement gap.

**Confidence:** Medium to high.

## Quality-of-life additions worth taking

From Pi Subagents itself:

- Strict JSON-Schema Completion Envelopes.
- Parallel fan-out/fan-in and dynamic chains.
- Background runs with persistent event artifacts.
- Model routing, fallback, and cost tracking.
- Turn, tool, spawn, and time budgets.
- Watchdogs, steering, and resume.
- Acceptance-ledger and runtime-verification patterns.

Separately:

- **`pi-mcp-adapter` — adopt where MCP is useful.** It provides a lazy single proxy and config discovery, reducing context pressure. MCP servers must still remain inside the child’s sandbox and network policy. [Catalog](https://pi.dev/packages/pi-mcp-adapter)
- **Dynamic Workflows — adopt selectively** for large research/review fan-out, journaled replay, checkpoints, and multi-judge synthesis.
- **Herdr Subagents — evaluate only for pane UX**, after choosing which runner owns child lifecycle.

## Required pilot checks

Before removing any current guarantee, demonstrate:

1. Reviewer and researcher cannot modify the repository, Git metadata, temporary escape paths, or invoke an unapproved network route.
2. Implementer can modify only the assigned worktree and required Git administrative directories.
3. Child skills, project context, and extensions do not leak unless explicitly allowed.
4. Invalid, missing, and empty completion payloads fail.
5. Timeout kills Pi, Landstrip, tools, MCP servers, and deliberately orphaned descendants.
6. SIGINT/SIGTERM and Herdr pane closure produce bounded cleanup.
7. Stage publishing remains monotonic and operator verification cannot be bypassed.
8. Foreground/background runs leave auditable final output, events, diagnostics, exit cause, and policy identity.
9. Worktree resume cannot attach from an unrelated working directory.
10. Landstrip absence or unsupported-kernel behavior fails closed.

## Gaps and uncertainties

- The proposed Pi Subagents/Landstrip composition was source-inspected but not installed or executed, as required by the brief.
- Whole descendant teardown under the composed wrapper is not documented for Linux/macOS. Retaining qq’s process-group timeout is therefore necessary.
- Landstrip is actively maintained but comparatively young and fast-moving; its Pi compatibility range should be pinned and tested on every Pi upgrade.
- Package download counts, release dates, and repository statistics are point-in-time signals, not proof of correctness.
- Secondary catalog candidates were screened through their catalog pages, repositories, and READMEs; only the leading orchestration and enforcement candidates received source-level mechanism inspection.
- Context7 corroborated Pi Subagents’ typed delegation and schema capabilities, but primary package source and documentation controlled the conclusions.
