---
id: TASK-52
title: 'deciq-logic: recover or retire the stranded task-22 work'
status: To Do
assignee: []
created_date: '2026-07-16 03:57'
labels: []
dependencies: []
priority: high
ordinal: 46000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The orphaned standalone clone at `~/.herdr/worktrees/deciq-logic/task-22` holds the only copy of four unpushed commits (through `afbcb85`) on `feat/task-22-publish-workflow`. Push the branch or explicitly decline it in the owning Backlog task, then remove the clone. Decide whether deciq-logic gets a persistent herdr home and board tab now that it has a board and in-flight work.

Do not delete the clone before pushing or recording an explicit decline: it is the only copy.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The four commits are pushed, or their decline is recorded in the owning Backlog task
- [ ] #2 The orphaned standalone clone is removed after the recovery or decline disposition
- [ ] #3 The persistent herdr home and board-tab decision is recorded
<!-- AC:END -->
