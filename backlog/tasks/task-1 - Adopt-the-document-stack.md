---
id: TASK-1
title: Adopt the document stack
status: Done
assignee: []
created_date: '2026-07-08 14:41'
updated_date: '2026-07-09 02:23'
labels: []
dependencies: []
priority: high
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Retire Understand-Anything (untrack .understand-anything/, drop plugin refs), rewrite methodology to the settled stack (codebase-memory MCP / backlog / openwiki / compound) and the single all-gated landing path, wire gate checks (registry check on test, openwiki refresh on format), seed this registry. Lands as feat/document-stack.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 No tracked .understand-anything/ and no plugin references in README/methodology/install
- [x] #2 Gate refuses a landing that does not touch backlog/ (once config is on main)
- [x] #3 Methodology documents the four-document stack and the herdr agent-comms primitives
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
AC#2 verified 2026-07-08 by the conductor, both directions, in a clean clone of main: a commit touching only README.md is REFUSED by bin/qq-registry-check.sh (exit 1, 'REFUSED: this landing does not touch backlog/'); a commit touching backlog/ PASSES (exit 0). The check is wired as the gate's commands.test in .no-mistakes.yaml and is read from origin/main, so it cannot be weakened by the branch under review — every landing today exercised its pass path. Document stack adopted: registry (backlog/), episodic docs (docs/solutions/ + CONCEPTS.md via compound), code graph (codebase-memory, operationalization tracked as TASK-18), openwiki (engine decision landed as TASK-7).
<!-- SECTION:NOTES:END -->
