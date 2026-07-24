---
id: T-155
title: Add one-command accountable Change handoff
status: Done
assignee: []
created_date: '2026-07-24 07:27'
updated_date: '2026-07-24 09:18'
labels: []
dependencies: []
references:
  - 'https://github.com/hypermemetic-ai/qq/pull/234'
documentation:
  - doc-90
modified_files:
  - README.md
  - bin/qq-handoff
  - bin/lib/qq-handoff.py
  - extensions/index.ts
  - extensions/qq-handoff.ts
  - skills/deliver-change/SKILL.md
  - tests/test-qq-handoff.sh
  - tests/test-qq-handoff-extension.sh
priority: high
type: feature
ordinal: 72000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Make transfer of an already aligned, already-created Change to a fresh accountable Pi session one direct command: `/handoff <Task-ID>`.

Add a fail-closed `bin/qq-handoff` engine and a thin globally mounted qq Pi command. The engine resolves the Task's unique existing linked Change checkout, verifies the alignment and topology rails, creates a fresh Pi tab in the Repository's persistent project home, submits a standard accountable-owner prompt naming the Task and attached plan, waits for the new session to reach working state, restores operator focus, and returns a structured receipt.

This Change does not create or align Tasks, branches, worktrees, plans, or pull requests. It does not fork conversation context, delegate bounded work, start a headless child, or add a generic Herdr agent lifecycle. It transfers accountability only after the owning session has already created and aligned the Change.

## Decision ledger

- Command surface `/handoff` backed by a tested qq engine, rather than a prompt template or CLI-only entry point — approved operator selection in the 2026-07-24 asked-and-answered alignment exchange.
- V1 accepts an existing Change only and refuses creation/alignment responsibilities — approved operator selection in the same exchange.
- The approved brief preceding those selections settles automatic unique-checkout resolution, fresh project-home Pi tab, standard Task/plan prompt, working-state confirmation, operator-focus restoration, and refusal of missing/ambiguous checkout, duplicate active owner, primary main, absent decision ledger/plan, or failed startup — same exchange.
- `decision-9` — Changes remain plain linked worktrees with accountable sessions in project home; no per-Change Herdr workspace is created.
- `T-148` and the root AGENTS.md Pi/Herdr boundary — Pi integration is qq scope and the mounted extension set is the activation surface; qq owns only its Herdr tenancy, not Herdr itself.

Use the attached approved plan. Realign before adding Change creation, context inheritance, automatic alignment, generalized session management, non-Pi agents, or cross-Repository handoff.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The globally mounted qq extension registers `/handoff <Task-ID>` and invokes a tested qq engine directly without an LLM or prompt-template intermediary.
- [x] #2 The engine resolves exactly one same-Repository linked non-main checkout containing the nonterminal Task and refuses missing, ambiguous, detached, primary-main, ledger-less, or plan-less candidates before creating a tab.
- [x] #3 The engine refuses another active Pi owner in the target checkout, creates one fresh Pi tab in the persistent project home, submits the standard accountable-owner prompt, confirms the new session is working, and restores the caller’s original focus.
- [x] #4 Startup failure cleanup is bounded and evidence-preserving, and success returns a machine-readable receipt naming Task, branch, checkout, workspace, tab, pane, agent, and observed state.
- [x] #5 V1 cannot create or align a Task, branch, worktree, plan, or pull request; cannot inherit conversation context; and cannot launch non-Pi or cross-Repository sessions.
- [x] #6 Deterministic tests cover every refusal, duplicate-owner detection, prompt contents, focus restoration, cleanup boundary, and successful lifecycle, followed by a fresh live Herdr/Pi handoff probe.
- [x] #7 README and methodology guidance document `/handoff` as the standard transfer step and distinguish accountable-session handoff from delegated child execution.
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented the fail-closed qq-handoff JSON engine and globally mounted direct /handoff command for existing aligned Changes. Deterministic refusal/transaction fixtures and the complete 32-test suite pass. A live Pi 0.81.1 / Herdr 0.7.5 probe reached a fresh working session, verified the fixed prompt and session receipt, restored exact caller focus, and retired only disposable resources. Fresh-context review findings were reproduced and fixed; the independent fix-delta review passed. Pull request: https://github.com/hypermemetic-ai/qq/pull/234.
<!-- SECTION:FINAL_SUMMARY:END -->
