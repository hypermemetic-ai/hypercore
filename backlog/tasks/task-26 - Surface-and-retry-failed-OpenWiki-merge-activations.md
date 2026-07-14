---
id: TASK-26
title: Surface and retry failed OpenWiki merge activations
status: In Progress
assignee:
  - '@codex'
created_date: '2026-07-14 03:01'
updated_date: '2026-07-14 03:10'
labels: []
dependencies: []
documentation:
  - doc-35
priority: high
ordinal: 23000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
From the 2026-07-13 architecture review: qq-openwiki-activate writes its dedupe marker (action: dispatching) before herdr dispatch and is invoked from the browser protocol handler with no visible stderr, so a failed dispatch permanently blackholes the merge with no operator signal.
Operator-settled decisions: failed dispatch rewrites the marker to a retryable failed state that the next activation retries; every ActivationError raises a herdr desktop notification (herdr notification show, as qq-herdr-pull does).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A dispatch failure after marker creation leaves a marker state that a subsequent activation retries instead of ignoring
- [ ] #2 A completed dispatch still dedupes: already-dispatched merges remain ignored
- [ ] #3 Every ActivationError surfaced from the protocol-handler entry path raises a herdr desktop notification
- [ ] #4 tests/test-qq-openwiki-activate.sh covers failed-dispatch retry and notification emission
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Encode explicit failed-marker retry while retaining completed dispatch dedupe.
2. Surface every protocol-entry ActivationError through a Herdr desktop notification.
3. Add regression coverage that fails on the old retry and notification behavior.
4. Run focused and repository Checks, independent review, strict plan conformance, Task finalization, and one-PR delivery.
<!-- SECTION:PLAN:END -->
