---
id: T-154
title: Own reliable delegated execution
status: To Do
assignee: []
created_date: '2026-07-24 07:12'
updated_date: '2026-07-24 07:15'
labels: []
dependencies: []
documentation:
  - doc-89
priority: high
type: feature
ordinal: 69000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Deliver qq-owned, reliable delegated execution in two bounded Changes: first restore the production contract with an immutable pinned bridge fork, then replace that bridge with a narrow qq-owned single-agent runtime built around the contract qq actually uses.

## Decision ledger

- `decision-12` — the operator approved an exact `pi-subagents` fork as an immediate bridge, true single-run production calls, and a narrow qq-owned runtime as the destination.
- `decision-8` — delegate network egress remains open beneath the pinned Landstrip drift-net; this work does not add a confidentiality or hostile-code boundary.
- `decision-10` — persisted Pi session JSONL remains the sole agent-content observation seam; lifecycle metadata may be live but content capture may not.
- `T-152` / `doc-88` — canonical role and execution-profile authority belongs to qq, not to the delegate package; untrusted same-name definitions may not occupy canonical roles.

The approved implementation plan is attached as a Backlog plan document. Each child Task owns one Change and must stop on any new consequential decision or boundary expansion.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The pinned bridge restores strict terminal structured completion and contract-preserving resume for production delegation.
- [ ] #2 A narrow qq-owned delegate runtime replaces the bridge without weakening confinement, lifecycle evidence, cleanup, or completion semantics.
- [ ] #3 The fork and pi-subagents-specific production coupling are retired only after the replacement passes the shared contract suite.
<!-- AC:END -->
