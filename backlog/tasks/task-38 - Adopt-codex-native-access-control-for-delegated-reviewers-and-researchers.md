---
id: TASK-38
title: Adopt codex-native access control for delegated reviewers and researchers
status: In Progress
assignee: []
created_date: '2026-07-14 18:44'
labels: []
dependencies: []
priority: medium
ordinal: 35000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
A spawned rim-migration reviewer re-entered the code-review skill and tried to delegate again: it pattern-matched the review task to the skill, and the brief line forbidding unrelated Skills and further delegation did not bite because the reviewer judged code-review related. The prose guard failed; the read-only sandbox (mechanical) is what stopped the recursion.

Replace the pane-based temporary-delegate procedure for review and research delegates with codex-native access control, owned entirely by the vendor: codex exec with skills.include_instructions=false and skills.bundled.enabled=false (skills never enter the delegate context, fails closed for future skills), --sandbox read-only (OS-enforced), and -o so the CLI itself writes the final report deterministically. No owned launcher, profiles, panes, or auth plumbing; process exit is delegate retirement.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 skills/code-review/SKILL.md launches its reviewer via the canonical codex exec command (skills excluded, read-only sandbox, CLI-written report file) with no agent-messaging pane lifecycle
- [ ] #2 skills/research/SKILL.md launches its researcher through the same canonical mechanism
- [ ] #3 A delegate launched by the canonical command reports no Skills in its context (probe returns NONE)
- [ ] #4 An end-to-end canonical review of a seeded-bug scratch repository returns the material finding in the -o report file
<!-- AC:END -->
