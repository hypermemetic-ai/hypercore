---
id: TASK-60
title: Decide whether the system context diagram earns a place
status: Done
assignee: []
created_date: '2026-07-16 16:43'
updated_date: '2026-07-16 17:09'
labels: []
dependencies: []
priority: low
type: spike
ordinal: 53000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
From Ideas doc-1 (2026-07-12 11:09): "the system context diagram was the only tolerable one. figure out why and whether we can justify including it."

Context: TASK-55 removed BPMN and diagram tooling entirely; doc-17/doc-18 hold the diagram research; the OpenWiki formerly carried generated diagrams. Investigate what made the system context diagram tolerable where others failed (scope? stability? abstraction level?), and produce a recommendation with criteria: include it (where, generated how, maintained by whom) or leave diagrams out. Read-only research; decision is the operators.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The analysis explains why the system context diagram outperformed the other diagrams, grounded in the repo history and docs
- [x] #2 A concrete include-or-omit recommendation with maintenance cost is recorded for operator disposition
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Research doc: doc-47. The 2026-07-12 note refers to the TASK-6 smoke-test judging: the C4 system context render (5 boxes, 6 edges, one screen) was the only C4 figure without a recorded defect, and its facts survived four days of churn that invalidated same-day container-level facts. Recommendation: if included, a hand-maintained Mermaid flowchart in README.md maintained through ordinary PRs — never a generated pipeline (every one built here died within days); omission equally defensible (README/quickstart prose already carries the orientation). Re-evaluation criteria recorded. Decision is the operator's.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Why-tolerable explained with recovered render evidence and churn analysis; include-or-omit recommendation with standing cost and flip criteria recorded in doc-47 for operator disposition.
<!-- SECTION:FINAL_SUMMARY:END -->
