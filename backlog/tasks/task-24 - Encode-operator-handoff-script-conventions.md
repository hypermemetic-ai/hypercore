---
id: TASK-24
title: Encode operator-handoff script conventions
status: Done
assignee:
  - task-24-operator-handoff-conventions
created_date: '2026-07-09 14:41'
updated_date: '2026-07-09 14:41'
labels:
  - docs
  - parallel-ok
  - hitl
dependencies: []
priority: medium
ordinal: 21000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Nothing in skills/ or the methodology says how to hand a reserved step back to the operator; the only guidance was the global 'minimize operator effort' preference, which states the goal and not the mechanics. Two failures on 2026-07-09 while staging a branch-deletion script: (1) the scratchpad path is ~90 chars, the terminal wrapped it, and the wrapped path failed to resolve; (2) 'read -p' prompts hit EOF in the non-interactive '!' shell and 'set -e' exited the script AFTER it printed five green verification lines, so it looked like it had worked while deleting nothing. Encode the rules in qq-methodology.md as a floor behavior, not a skill: a floor rule applies whenever you hand something back, whereas a skill must be invoked to help.
<!-- SECTION:DESCRIPTION:END -->
