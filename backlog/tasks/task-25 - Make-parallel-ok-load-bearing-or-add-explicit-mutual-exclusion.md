---
id: TASK-25
title: Make parallel-ok load-bearing or add explicit mutual exclusion
status: To Do
assignee: []
created_date: '2026-07-09 14:41'
labels:
  - tooling
  - parallel-ok
  - hitl
dependencies: []
priority: high
ordinal: 22000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Reported from the meeting-reviewer session, 2026-07-09, and re-verified against the review base and this branch: the 'parallel-ok' label is decorative. It appears in 15 backlog task files at review base b4433d250dff9492e15ed3e268a7e1c3fa79344b and 20 in this branch after TASK-24 through TASK-28, with two qq-methodology.md prose references and 0 matches in bin/ or skills/ ('rg -n parallel-ok bin skills' returns nothing). bin/qq-frontier drops a task when that task itself is claimed (a task-<id> branch exists), but two UNCLAIMED tasks that collide on the same files are both eligible and can be dispatched into the same wave. That leaves two bad workarounds: a false dependency edge, which over-serializes and inverts priority, or conductor prose, which nothing checks. The reporter described a historical TASK-11/TASK-7/TASK-8 collision, but this repo only verifies TASK-11's recorded surface overlap with TASK-8; unverified collision counts should not become the design basis. Decide: make 'parallel-ok' actually load-bearing, or add a first-class mutex/exclusive-with field that qq-frontier reads and a wave dispatcher honors. A triage invariant the methodology enforces in prose and nothing enforces in code is worse than no label.
<!-- SECTION:DESCRIPTION:END -->
