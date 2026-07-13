---
id: TASK-20
title: Correct Herdr message submission instruction
status: Done
assignee:
  - '@codex'
created_date: '2026-07-13 03:29'
updated_date: '2026-07-13 03:30'
labels: []
dependencies: []
modified_files:
  - skills/agent-messaging/SKILL.md
ordinal: 17000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The agent-messaging Skill tells agents to follow herdr agent send with an incomplete herdr pane run invocation. Correct the instruction so a typed prompt is submitted as a Codex turn.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The Skill names a valid Herdr command that submits the already typed prompt with Enter.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Replace the invalid pane-run instruction with the explicit Enter key command, then validate the Skill and inspect the exact diff.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Changed the submission step from the invalid/incomplete pane-run invocation to herdr pane send-keys <pane-id> Enter. Herdr 0.7.3 help confirms that syntax; skill-creator quick_validate and git diff --check pass.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Corrected the agent-messaging Skill to submit typed prompts with Herdr's explicit Enter-key command. Herdr syntax help, Skill validation, and diff checks pass.
<!-- SECTION:FINAL_SUMMARY:END -->
