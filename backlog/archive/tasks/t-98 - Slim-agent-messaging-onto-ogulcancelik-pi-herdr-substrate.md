---
id: T-98
title: Slim agent-messaging onto @ogulcancelik/pi-herdr substrate
status: To Do
assignee: []
created_date: '2026-07-19 16:42'
updated_date: '2026-07-19 19:40'
labels: []
dependencies: []
documentation:
  - doc-57
priority: medium
type: task
ordinal: 30000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Evidence: doc-57. Adopt @ogulcancelik/pi-herdr (herdr author's official pi package, bundled skill) as the generic herdr command surface; reduce skills/agent-messaging to qq-specific semantics only: live cross-runtime agent discovery, AGENT from=<terminal-id> addressing, literal-send rules, sender existence verification, current-pane caller resolution, operator notifications, unrouteable-message handling. Topology scripts qq-herdr-home/pull/snap stay as-is (doc-57 KEEP verdicts).

Decision ledger:
- Substrate adoption and the skill's retained-semantics list: doc-57, ticketed per operator instruction in the T-93 follow-up session.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 agent-messaging contains only the qq protocol overlay; generic herdr command instruction defers to the bundled pi-herdr skill
- [ ] #2 Messaging smoke check across a pi and a non-pi agent passes; ratchet baselines updated
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
DIES 2026-07-19 as moot per T-107 disposition (operator, this session): pi-intercom ADOPTED as the inter-agent transport, replacing herdr keystroke injection rather than slimming the skill onto the herdr substrate. T-98's premise — herdr remains the transport — no longer holds. The agent-messaging reshape (qq overlay + intercom transport + herdr operator notifications + legacy herdr-send for codex delegates until T-95) is new Change work spun out of T-107, not this ticket.
<!-- SECTION:NOTES:END -->

## Comments

<!-- COMMENTS:BEGIN -->
created: 2026-07-19 18:41
---
HELD 2026-07-19 pending T-107's messaging evaluation: if a broker/file transport replaces herdr keystroke injection, this slim is moot or reshaped. Removed from the dispatch batch (doc-62).
---
<!-- COMMENTS:END -->
