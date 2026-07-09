---
id: TASK-27
title: 'Frontier order has no queue head, only ordinal ties'
status: To Do
assignee: []
created_date: '2026-07-09 14:41'
labels:
  - tooling
  - parallel-ok
  - hitl
dependencies: []
priority: medium
ordinal: 24000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Reported from the meeting-reviewer session, 2026-07-09, and verified by reading bin/qq-frontier and running it against the review base and this branch: bin/qq-frontier sorts by (priority rank, ordinal), so equal-priority tasks break ties on ordinal and there is no way to say 'this task is the head of the queue' except by hand-tuning ordinals. The reporter's concrete TASK-6/TASK-12 example was stale: at the review base and in this branch, TASK-6 is Done with priority medium and ordinal 6000, while TASK-12 is Done with no priority field and ordinal 10000, so neither task appears on the frontier. The current HEAD frontier shows the actual contract: high tasks order by ordinal (TASK-11 at 11000, TASK-22 at 19000, TASK-25 at 22000), then medium tasks order by ordinal (TASK-9 at 9000 before later medium ordinals). Decide whether the registry should express queue order directly, or whether ordinal-as-order is the contract and the conductor must stop writing prose that contradicts it.
<!-- SECTION:DESCRIPTION:END -->
