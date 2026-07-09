---
id: TASK-14
title: 'Backlog board: compact card labels — kill the TASK- prefix noise'
status: To Do
assignee: []
created_date: '2026-07-08 17:30'
updated_date: '2026-07-08 21:02'
labels:
  - parallel-ok
dependencies: []
priority: low
ordinal: 12000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Operator (07-08): the board makes poor use of horizontal space — 'TASK-x' eats most of a card while the prefix adds no information when task is the only type. Want a dense scheme that keeps cards real small: bare id plus a super-shortened label (single word, consonant-skeleton, aggressive abbreviation — survey prior art: tracker key schemes, tmux window naming, abbreviation algorithms). Avenues to evaluate: Backlog.md config (custom/empty id prefix?), board rendering options, an upstream feature request/PR to MrLesk/Backlog.md, or a thin qq-side board wrapper. ALSO (07-08, same cockpit-surface concern): backlog-board was launched via 'herdr agent start', so it shows up in herdr's agents list and eats sidebar space although it is not an agent — find the non-agent way to run a utility pane (plain pane launch, an exclude flag, or a herdr feature request) so the sidebar stays reserved for actual agents. Capture only — not addressed yet.
<!-- SECTION:DESCRIPTION:END -->

## Outcome

<!-- SECTION:NOTES:BEGIN -->
DECLINED by the operator, 2026-07-08: "I've decided not to customize the board. It's ownership surface for a purely cosmetic concern." The work was completed and passed the gate (PR #12); the PR was closed unmerged and the branch left in place per the unlanded-work rule. Two findings from it were kept: herdr's non-agent pane pattern (pane split + send-text + Enter) will be reused by the planned TASK-19 bin/qq-gate-view, and the board's apparent staleness is cross-branch resolution (backlog/config.yml check_active_branches), not a rendering problem — see docs/solutions/2026-07-08-silent-failure-and-the-gate-branch-contract.md.
<!-- SECTION:NOTES:END -->
