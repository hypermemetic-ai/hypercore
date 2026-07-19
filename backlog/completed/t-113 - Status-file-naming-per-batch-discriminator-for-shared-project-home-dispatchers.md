---
id: T-113
title: >-
  Status-file naming: per-batch discriminator for shared project-home
  dispatchers
status: Done
assignee: []
created_date: '2026-07-19 21:10'
updated_date: '2026-07-19 21:59'
labels: []
dependencies: []
priority: medium
type: bug
ordinal: 45000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Found live in the 2026-07-19 pi-sweep wave-1 batch: two dispatchers (pi-sweep wave 1 and the T-107 follow-on) both ran from the qq project home and both derived the same detail file /tmp/qq-delegates/home/qqp/projects/qq/wM.status per delegate-batch's scheme (<dispatcher-workspace-id>.status). The second dispatcher's rewrite silently replaced the first's live surface. doc-43's 'one dispatcher owns one file — single-writer by construction' is false when sibling dispatchers share the project home.

Verified workaround, converged on independently by both dispatchers: a per-batch discriminator in the filename (wM-pi-sweep-w1.status, wM-t107-followon.status); the prefix+d popup renders every *.status in the directory, so both surfaces coexist.

Fix: amend skills/delegate-batch/SKILL.md (and a note in doc-43) so the status filename is <workspace-id>-<batch-label>.status, with the batch label the dispatcher's own recognizer; declare the popup's multi-file rendering the intended shape.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 delegate-batch's status-file path scheme carries a per-batch discriminator; doc-43 collision note recorded
- [ ] #2 Two concurrent dispatcher surfaces verified coexisting in the prefix+d popup
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Closed moot 2026-07-19: the operator broadened decision-3 to retire the delegation status logic entirely — detail files included — with deletion now under T-116. A namespacing fix for a deleted surface is waste; no Change shipped. The live collision it addressed dies with the surface.
<!-- SECTION:FINAL_SUMMARY:END -->
