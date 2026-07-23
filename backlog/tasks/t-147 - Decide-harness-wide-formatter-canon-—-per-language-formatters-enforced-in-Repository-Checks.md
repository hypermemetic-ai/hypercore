---
id: T-147
title: >-
  Decide harness-wide formatter canon — per-language formatters enforced in
  Repository Checks
status: To Do
assignee: []
created_date: '2026-07-23 02:13'
updated_date: '2026-07-23 02:14'
labels: []
dependencies: []
documentation:
  - doc-83
ordinal: 67000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Origin: the 2026-07-22 deciq incident (pi-lens turn-end autoformat restore-loop blocked qq-change land three times; root cause confirmed in pi-lens source: bash restore recipes re-queue deferred formatting). Operator direction (accountable project-home session, 2026-07-22): make formatting canon harness-wide, covering Python (linked projects), with the operator making the call after reading a plain-language primer (attached guide doc). Parked window: opens when the operator chooses; the T-142 observer arc continues meanwhile.

Decision ledger: pursuing canon rather than disabling autoformat — operator direction, asked-and-answered exchange 2026-07-22; harness-wide scope incl. Python — same exchange; windowing (parked with briefing attached) — operator answer, same exchange. The canon choices themselves (tools, per-repo scope, defaults vs config, deciq offer timing) — OPEN, pending the operator's canon window. The upstream pi-lens fix was declined by the operator (no issue filed); the restore-loop residue is covered by canon conformity + write-in-primary doctrine (T-144) + the land rail.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Operator decision recorded: canon tools per language and per-Repository scope
- [ ] #2 Each adopted canon: one-time reformat commit plus Check gate landed in that Repository
- [ ] #3 pi-lens autoformat verified consistent with adopted canon (edit-time and check-time agree)
- [ ] #4 deciq restore-loop disposition recorded (canon conformity + doctrine + rail, per the primer)
<!-- AC:END -->
