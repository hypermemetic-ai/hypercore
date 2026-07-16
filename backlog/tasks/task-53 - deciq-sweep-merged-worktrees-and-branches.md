---
id: TASK-53
title: 'deciq: sweep merged worktrees and branches'
status: To Do
assignee: []
created_date: '2026-07-16 03:57'
labels: []
dependencies: []
priority: medium
ordinal: 47000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Twelve registered worktrees on merged branches plus about 20 merged local branches have accumulated under `~/.herdr/worktrees/deciq`. One stalled unmerged worktree, `feat/task-22-logic-promotion`, also needs a disposition.

TASK-49's retire-at-source mechanism prevents recurrence going forward; this task is the one-time backlog.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Merged worktrees and branches are removed behind TASK-49's rails
- [ ] #2 The disposition of the unmerged feat/task-22-logic-promotion worktree is recorded
<!-- AC:END -->
