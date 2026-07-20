---
id: T-107
title: Settle open pi-ecosystem evaluations
status: Done
assignee: []
created_date: '2026-07-19 18:41'
updated_date: '2026-07-19 19:58'
labels: []
dependencies: []
priority: medium
type: task
ordinal: 39000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Open evaluations carved out of the pi-sweep batch at alignment (2026-07-19). Evidence base: doc-63 (de-biased round, empty adoption set under strict gates — the operator judged the gates too strict and will dispose these interactively). Each item ends in adopt / trial / drop with evidence.

1. Agent messaging (HOLDS T-98). Current transport is fragile by construction: herdr pane run synthetic keystrokes — operator observes routine typed-but-not-sent failures; no correlation/ack protocol (skills/agent-messaging admits it). Walk the operator through candidates: pi-intercom (local IPC broker; native correlated ask/reply; pi-only), pi-messenger (file-based rooms — the only candidate a non-pi agent could join; its task/crew hierarchy must be filtered out), pi-link (WebSocket link network; newest, thinnest attestation), @ogulcancelik/pi-herdr (T-98's pick — maintains the keystroke transport rather than fixing it). Note: after T-95 all delegates are pi children, so a pi-only transport may suffice; codex delegates exist until then. Deliverable: per-candidate disposition + agent-messaging's future; T-98 unholds or dies.
2. TUI file-tree/diff browsing — operator: 'VERY compelling', warrants a deeper dedicated round: pi-files-widget, pi-slopchop, fresh discovery; hands-on trials, not just literature.
3. fff — answer 'best in class for what it does?'; its only miss was the exact-version gate. Trial candidate.
4. statusline — answer 'is @narumitw/pi-statusline the strongest candidate?' vs @pi-vault/pi-status and fresh discovery.
5. rpiv-todo — operator-marked interesting; trial evaluation.
6. Folded-in dispositions: T-101 (pi-plan-mode) and T-102 (codebase-index pilot; note its named challenger was never assessed — the pilot is the only direct evidence path).

Decision ledger:
- Items 1-5 and the one-open-task shape: operator instructions, asked-and-answered alignment exchange, 2026-07-19 alignment session ('take all the opens and make them their own task').
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Every numbered item has a recorded adopt/trial/drop disposition with evidence
- [x] #2 Messaging item resolves T-98 (unhold as-is, reshape, or close)
- [x] #3 File-browsing round includes hands-on trials, literature alone insufficient
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
FINAL LEDGER (operator, 2026-07-19, settler session, third exchange) — ALL ITEMS DISPOSED:
1. pi-intercom ADOPT / pi-messenger DROP / pi-link DROP / pi-herdr DROP; T-98 dead (archived). Delivery: messaging-reshape Change.
2. files-widget ADOPT (operator's preferred browser — DISPLACES yazi as the UI surface; retiring yazi's shell machinery (qqy/qqbr/qqroot, prefix+f popups, parent-shell cwd) is consequential and NOT settled here — own task, needs alignment), slopchop ADOPT (all-files scope = local PR diff; GitHub demoted), pi-diff-review DROP.
3. fff ADOPT additive as steady state (data: 5/6 tool selection, exact rg parity, no staleness, negligible cold-start; override only if future session logs show drift to built-ins).
4. pi-footer ADOPT; narumitw DROP.
5. rpiv-todo ADOPT.
6. pi-plan-mode DROP (T-101 stays dead); T-108 minted (codebase-index pilot, structural-first).
NEW DIRECTION (operator): make the GitHub merge-console piece terminal-friendly — minted as its own evaluation task.
<!-- SECTION:NOTES:END -->
