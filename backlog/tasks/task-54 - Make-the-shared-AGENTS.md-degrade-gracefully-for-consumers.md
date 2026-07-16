---
id: TASK-54
title: Make the shared AGENTS.md degrade gracefully for consumers
status: To Do
assignee: []
created_date: '2026-07-16 03:57'
labels: []
dependencies: []
priority: medium
ordinal: 48000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
`AGENTS.md` is symlinked into consumer projects and mandates surfaces they lack: `REVIEW.md` in deciq and deciq-logic, `openwiki/` in deciq-logic, and codebase-memory-mcp in both. Either add the surfaces to consumers, make the canonical text conditional ("where present"), or split project-conditional sections out of the shared file.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A settled approach lands
- [ ] #2 Consumer-project sessions no longer receive mandates they cannot follow
<!-- AC:END -->
