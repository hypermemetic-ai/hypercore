---
id: TASK-11
title: >-
  Gate visibility: kill the invisible waiting; vertical pipeline view on the
  right
status: To Do
assignee: []
created_date: '2026-07-08 15:53'
updated_date: '2026-07-08 21:02'
labels:
  - parallel-ok
dependencies:
  - TASK-10
priority: high
ordinal: 11000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Operator (07-08): runs 'take forever while being completely invisible - drives me crazy'; the current view 'is basically pointless - should be more fleshed out and visible as a vertical pipeline on the right.' Two parts. (1) Latency: ADDRESSED 07-08 via task-13 (keep+retune decision on task-10): agent-owns-run consent model, auto_fix.review 3, v1.34 (surfaces live step activity in axi status), --skip ci until real CI; parked states are now the landing agent's to answer and show as blocked in herdr — the invisible-hang class is gone (measured: sub-minute park handling vs 14h orphaned park before). (2) Visibility: STILL OPEN — a live vertical pipeline surface on the right (cockpit/herdr pane) rendering axi status — all 9 steps with state/durations/findings and an unmissable PARKED indicator — replacing the one-line qq-phase merge as the primary gate view.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Gate progress is visible ambiently (no polling) including parked-for-decision states
- [ ] #2 A right-side vertical pipeline view exists in the cockpit and is wired by qq-activate/herdr config
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Surface overlap with TASK-8 — see its notes; coordinate via herdr or sequence after it.
<!-- SECTION:NOTES:END -->
