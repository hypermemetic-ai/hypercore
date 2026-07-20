---
id: T-100
title: Trial cc-safety-net as destructive-command defense-in-depth
status: To Do
assignee: []
created_date: '2026-07-19 16:42'
updated_date: '2026-07-19 17:49'
labels: []
dependencies: []
documentation:
  - doc-60
priority: medium
type: chore
ordinal: 32000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Top QoL trial from the sweep (evidence: doc-60; doc-54's rejection was for the guard question only). Trial npm:cc-safety-net in isolation (pi --no-extensions -e) per doc-60's adoption checks. Keep worktree relaxation disabled. This is defense-in-depth, not a sandbox or network boundary.

Decision ledger:
- Trial candidate and procedure: doc-60, ticketed per operator instruction in the T-93 follow-up session.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Destructive reset/checkout/removal variants blocked while normal temporary-file and branch operations remain usable, with evidence
- [ ] #2 Behavior under qq's tmux/herdr environment verified; adopt/discard verdict recorded
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Dropped at batch alignment 2026-07-19: operator judged no demonstrated need ('drop it, I haven't come across a real need for this yet'). Destructive-command defense-in-depth may be revisited if a real incident or near-miss motivates it.
<!-- SECTION:NOTES:END -->
