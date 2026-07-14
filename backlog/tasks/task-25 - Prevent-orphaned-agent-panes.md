---
id: TASK-25
title: Prevent orphaned agent panes
status: In Progress
assignee:
  - '@codex'
created_date: '2026-07-14 01:52'
updated_date: '2026-07-14 02:16'
labels:
  - methodology
  - herdr
dependencies: []
documentation:
  - doc-34
modified_files:
  - README.md
  - bin/qq-openwiki-activate
  - cockpit/README.md
  - skills/agent-messaging/SKILL.md
  - skills/code-review/SKILL.md
  - skills/deliver-change/SKILL.md
  - skills/research/SKILL.md
  - tests/test-qq-openwiki-activate.sh
  - backlog/tasks/task-25 - Prevent-orphaned-agent-panes.md
  - backlog/docs/plans/doc-34 - Plan-—-Prevent-orphaned-agent-panes.md
  - backlog/docs/plans/assets/doc-34/plan-spec.json
  - backlog/docs/plans/assets/doc-34/plan.bpmn
  - backlog/docs/plans/assets/doc-34/plan.png
priority: high
ordinal: 22000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Temporary reviewer and researcher panes have no teardown owner, and OpenWiki activation starts its maintainer beside an unused worktree placeholder. Eliminate both orphan-panel paths without changing accountable or operator-owned pane retention.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The spawning agent owns each temporary delegate pane through its result and required follow-up, then closes it, verifies it is absent, and reports cleanup failure.
- [ ] #2 Review and research keep delegates alive only while retry, context-gap, or exact-delta follow-up remains; their terminal paths perform cleanup.
- [ ] #3 Terminal Change guidance preserves the accountable and operator-created panes while excluding completed temporary delegates from retained inspection context.
- [ ] #4 Focused validation covers Skill syntax, concise policy consistency, and a disposable live delegate cleanup without disturbing other panes.
- [ ] #5 A missing OpenWiki maintainer starts inside the worktree's returned placeholder, is detected and given its stable name, and later wake-ups target that same pane.
- [ ] #6 OpenWiki launch or detection failure leaves the placeholder recoverable; focused regression and live checks prove no extra pane remains and the maintainer is undisturbed.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Assign temporary delegate-pane ownership in agent-messaging. 2. Add terminal cleanup to review and research. 3. Reconcile Change-retention wording. 4. Launch and name OpenWiki maintainers in the returned placeholder. 5. Validate Skills, activation regressions, and live pane lifecycles. 6. Review and deliver one green pull request.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented delegate ownership and terminal review/research cleanup, narrowed retained-pane guidance, and launched missing OpenWiki maintainers in the returned idle placeholder. Review found busy-pane and optional-session detection gaps; both were fixed and the exact delta passed review. All repository tests, 18 BPMN tests, four changed-Skill validators, static checks, live single-pane startup, reviewer teardown, and operator UAT passed.
<!-- SECTION:NOTES:END -->
