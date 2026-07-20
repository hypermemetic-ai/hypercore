---
id: T-101
title: Adopt @narumitw/pi-plan-mode as terminal plan mode
status: To Do
assignee: []
created_date: '2026-07-19 16:42'
updated_date: '2026-07-19 18:41'
labels: []
dependencies: []
documentation:
  - doc-54
  - doc-59
  - doc-63
priority: medium
type: chore
ordinal: 33000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
QoL adoption (evidence: doc-54, doc-59 — both clusters converged). Terminal-native read-only exploration, structured operator questions, stored plans, fail-closed Bash filtering. Plans must live in the pi session, never under backlog/. Do not install Plannotator alongside it; do not treat it as a source of alignment decisions (interaction surface only).

Decision ledger:
- pi-plan-mode as default over Plannotator (shortlist for visual annotation needs): doc-54/doc-59, ticketed per operator instruction in the T-93 follow-up session.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Installed and exercised on a real planning task; command/flag collisions with qq skills checked
- [ ] #2 No plan artifacts land under backlog/; ratchet baselines unaffected or updated
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Superseded by T-107 at batch wrap-up 2026-07-19: the operator reviewed the raw round-2 findings (doc-63) directly and folded all open evaluations into one operator-facing task.
<!-- SECTION:NOTES:END -->

## Comments

<!-- COMMENTS:BEGIN -->
created: 2026-07-19 18:05
---
Paused at batch alignment 2026-07-19: operator distrusts the sweep-era package findings; a fresh de-biased research round (no prior candidates/verdicts, outcome-evidence-only rule) is running before this ticket is approved.
---
<!-- COMMENTS:END -->
