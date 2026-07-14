---
id: TASK-32
title: Phase 1 — Establish the deterministic floor (CI and hooks)
status: Done
assignee: []
created_date: '2026-07-14 05:10'
updated_date: '2026-07-14 07:17'
labels: []
dependencies: []
documentation:
  - doc-38
priority: high
ordinal: 29000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add the missing deterministic enforcement layer per doc-38 Phase 1: a GitHub Actions workflow running both existing test suites, Claude Code project hooks enforcing the hard mandates, and removal of the three sentence-grep policy tests whose prose coverage the hooks replace.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A GitHub Actions workflow runs the BPMN pipeline node tests (Node >=20, QQ_BPMN_SKIP_RENDER=1) on every pull request and push to main
- [x] #2 The same workflow runs the shell suite (tests/test-*.sh) and fails on any test failure
- [x] #3 Claude Code project hooks block agent-issued 'gh pr merge' and direct Edit/Write to managed Backlog markdown (excluding plan asset bundles), with behavior covered by a shell test
- [x] #4 tests/test-grilling.sh, tests/test-bpmn-plans.sh, and tests/test-openwiki-maintainer.sh are deleted and nothing references them
- [x] #5 All remaining local tests pass and the CI workflow is green on this Change's pull request
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented by delegated codex (gpt-5.6-sol) with operator-side contributions; hardened through five fresh-context review rounds (wrapper unwrapping incl. exec/time/redirections, heredoc quoting/expansion semantics, arithmetic-shift exclusion, plans-only asset exemption, XDG handling). Two findings declined by owner as outside the guard's well-meaning-drift threat model (case-pattern ')' inside $(), quoted redirection operator as option value): the guard is a drift-net, not a security boundary — determined evasion is backstopped by the operator merge gate; enabling GitHub branch protection on main is recommended as the hard backstop. Hook schema verified against current Claude Code docs. Local evidence: guard behavior suite (30+ scenarios), full shell suite, BPMN suite 16/0 all pass.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
First CI workflow (both test suites on every PR and push to main), deterministic PreToolUse hooks enforcing 'only the operator merges' and 'managed Backlog markdown via CLI' with a defensive command/path parser and comprehensive behavior tests, and the three sentence-grep policy tests deleted in favor of that behavior coverage.
<!-- SECTION:FINAL_SUMMARY:END -->
