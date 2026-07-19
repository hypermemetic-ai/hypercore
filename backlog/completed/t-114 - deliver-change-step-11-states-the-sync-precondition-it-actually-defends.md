---
id: T-114
title: deliver-change step 11 states the sync precondition it actually defends
status: Done
assignee: []
created_date: '2026-07-19 21:11'
updated_date: '2026-07-19 21:59'
labels: []
dependencies: []
priority: medium
type: bug
ordinal: 46000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Found live twice on 2026-07-19 (pi-sweep wave 1 and T-107 follow-on dispatchers, independently): step 11's strict precondition — every untracked entry must be a managed Task record under backlog/tasks/ — blocks every primary-checkout sync during doc-heavy work, because qq's own conventions keep untracked managed Backlog markdown under backlog/docs/, backlog/decisions/, and backlog/archive/ too (sweep research docs, decision records, archived tasks). Both dispatchers deviated with the same hand-verified substitute check: (a) zero tracked modifications, (b) every untracked entry is managed Backlog markdown (the classes the conventions deliberately keep in the primary checkout), (c) zero overlap between the incoming merge diff and untracked paths — the exact clobber failure mode Git's own ff-refusal already guards.

Fix: rewrite deliver-change step 11's precondition to state that check (tracked-clean + managed-classes + zero merge-diff overlap) instead of the tasks-only text, keeping the no-repair rule and the exclusive-use coordination.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Step 11 precondition names the managed Backlog markdown classes and the zero-overlap check
- [ ] #2 Guard text keeps the never-repair-the-checkout rule verbatim
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Closed as duplicate 2026-07-19: the fix ships as T-115(a) — T-115 minted minutes after this ticket to carry the same step-11 precondition rewrite. No separate Change; delivery tracked on T-115.
<!-- SECTION:FINAL_SUMMARY:END -->
