---
id: T-156
title: Add qq ecosystem update assessment prompt
status: In Progress
assignee: []
created_date: '2026-07-24 14:29'
updated_date: '2026-07-24 16:35'
labels: []
dependencies: []
documentation:
  - doc-91
  - doc-92
modified_files:
  - .gitignore
  - .pi/prompts/update.md
priority: high
type: enhancement
ordinal: 73000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a project-local `/update` Pi prompt that inventories the complete decision-relevant qq runtime ecosystem rather than trusting update notifications, verifies primary release evidence, and assesses each candidate against qq's current architecture, problems, direction, simplification opportunities, extension overlap, compatibility, and operational risk. Run the first assessment in this Change and retain one cited research report. Do not install updates or enact follow-up architecture changes in this Change.

## Decision ledger

- Project-local `.pi/prompts/update.md` registered as `/update`: asked-and-answered alignment exchange on 2026-07-24; the operator approved the recommended project-local, source-controlled surface.
- Inventory Pi core, all installed Pi packages, Herdr, first-class qq-integrated runtime owners, and dependencies implicated by a material compatibility, security, migration, overlap, or simplification edge instead of relying on notifications: approved plan doc-91, with the decision-relevant boundary clarified by the confirmed review finding.
- Assessment recommends update, hold, test, replace, remove, or no action but performs no ecosystem upgrade without separate approval: asked-and-answered alignment exchange on 2026-07-24.
- Current Change contains the prompt and one cited assessment only; actual upgrades or architectural follow-ups require separately approved Changes: same approved exchange.
- Invoking `/update` is standing authorization for that cycle's governance-required Task, Change, plan/research evidence, Checks, independent review, and pull-request handoff only; it never authorizes merge or assessed ecosystem/runtime mutation: decision-13.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Project-local /update is discovered by Pi and expands into the approved assessment workflow.
- [ ] #2 Each run inventories Pi core, every installed Pi package, Herdr, and other current qq-integrated runtimes without treating notifications as complete.
- [ ] #3 The workflow verifies primary release evidence and assesses qq opportunities, solved problems, simplifications, territory overlap, compatibility, migration cost, and risk.
- [ ] #4 The workflow produces an explicit per-component recommendation and does not install or update software without separate operator approval.
- [ ] #5 The first current-state cycle is preserved as one cited, confidence-tagged Backlog research report attached to this Task.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Relevant checks pass and fresh-context review finds no unresolved in-scope defect.
- [ ] #2 One green pull request is handed to the operator; the agent does not merge it.
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add the tracked project prompt and the narrow `.gitignore` exception required for Pi discovery.
2. Verify prompt discovery and that its instructions cover complete inventory, primary evidence, qq implications, overlap, simplification, risks, and explicit non-mutation.
3. Run the workflow against current installed/runtime state; delegate decision-grade evidence collection and preserve one Backlog research report.
4. Review and verify the Change, then deliver one green pull request without applying any ecosystem updates.
<!-- SECTION:PLAN:END -->
