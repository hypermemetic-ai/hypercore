---
id: T-125
title: Decide qq's standing agent web-access adoption
status: To Do
assignee: []
created_date: '2026-07-21 01:38'
updated_date: '2026-07-21 01:39'
labels: []
dependencies: []
ordinal: 54000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Operator request (2026-07-21 alignment exchange): a proper research round, codex-handled, to determine the most natural web-access adoption for qq agents. Triggered by the T-121 latency-toolkit research needing live web access. Candidates: pi-web-access (installed 2026-07-21, zero-config Exa + Codex-auth reuse), @juicesharp/rpiv-web-tools (family-consistent with pinned rpiv@1.20.0 set, needs provider key or self-hosted backend), other pi.dev web packages, or curl-only (no package). Constraints: both packages register web_search (collision); delegate egress is open (decision-8). Evaluation lens (operator-settled 2026-07-21): the deliberately-small-machinery / smallest-resulting-system doctrine applies to qq's OWN surfaces, not to an adopted extension — judge candidates on architecture quality: clean abstractions, provider fallback design, failure handling, security posture, maintenance trajectory. Feature breadth is not a demerit when well-architected. Decision ledger: research round + codex execution = operator direction, 2026-07-21 exchange; well-architected-over-small lens for extensions = same exchange.
<!-- SECTION:DESCRIPTION:END -->
