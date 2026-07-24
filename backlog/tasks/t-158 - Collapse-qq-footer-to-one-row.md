---
id: T-158
title: Collapse qq footer to one row
status: In Progress
assignee: []
created_date: '2026-07-24 18:59'
updated_date: '2026-07-24 20:00'
labels: []
dependencies: []
documentation:
  - doc-95
modified_files:
  - extensions/qq-footer.ts
  - tests/test-qq-footer-extension.sh
type: enhancement
ordinal: 74000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Replace the current two-row qq footer with one row. Remove the session dollar-cost and subscription marker entirely. Preserve cwd, branch, session name, allowed extension statuses, context usage, active-provider quota bars, provider/model, and thinking level; combine them into the existing top row with right-aligned compact information.

Ownership boundary: extensions/qq-footer.ts, its focused test, and the durable Task/approved plan records. No quota-fetching, status-filtering, provider-auth, or Pi-core changes.

Decision ledger:
1. One-row footer; remove cost/subscription; preserve and merge all other current segments — asked-and-answered alignment exchange, 2026-07-24.
2. Keep the existing left identity/status grouping and right-align the compact usage/quota/model grouping — same asked-and-answered alignment exchange.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Footer renders exactly one row containing cwd/branch/session/status plus context usage/quota/provider/model/thinking, with compact information right-aligned
- [x] #2 No dollar cost or subscription marker is rendered
- [x] #3 Quota polling/parsing and status filtering behavior remain unchanged
- [ ] #4 Focused footer test and full native suite pass
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Delivered PR #238. The qq footer now renders one terminal row: cwd/branch/session/status remain left, while context usage, optional active-provider quota bars, and provider/model/thinking form the right-aligned compact group. Session dollar cost and the subscription marker were removed, together with their dead helpers and test harness data. Focused footer Check passed; full native suite passed 33/33 locally and GitHub shell-tests passed. Fresh-context review returned PASS with production nonblank LOC -27 and decision points -18; no same-fix-smaller regeneration was needed. Visual UAT was explicitly skipped by the operator in favor of deterministic render evidence. PR creation was briefly blocked by GitHub’s acknowledged Pull Requests incident and succeeded without changing the branch after the service recovered enough to accept it.

Reactivated after the post-finalization focused Check intermittently failed while waiting for the asynchronous fixture-backed quota repaint. This is the same timing-flake class recorded by T-149; T-158 remains open until the affected Check is made deterministic, rerun, and fresh-review accepted.
<!-- SECTION:FINAL_SUMMARY:END -->
