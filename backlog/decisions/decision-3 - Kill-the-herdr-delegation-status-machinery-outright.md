---
id: decision-3
title: Kill the delegation status machinery outright
date: '2026-07-19 19:41'
status: accepted
---
## Context

The T-94 pilot (2026-07-19) found the herdr delegation-status glass — stage
tokens, pane presence, notifications — fragile under nested confinement, and
the pilot's adopt/hold fork did not depend on it. The operator settled the
kill asked-and-answered the same day: 'kill the herdr machinery. I'm
confident.' This record was minted in PR #151 as a stub; its scope was pinned
only by citation in T-94's ledger and T-95's removal scope.

Later that day the T-113 / T-115(b) status-file namespacing fix forced the
question the stub left open: does the kill cover the plain detail-file
protocol (/tmp/qq-delegates *.status files and the prefix+d popup) that
T-95's text had kept as 'the ambient record'? Operator disposition
(2026-07-19, T-115 retarget exchange): yes — retire the status logic
entirely, detail files included, and delete the detail-file surface now
rather than at T-95. Operator evidence: the popup has never been used, and
pi-intercom (T-109, PR #152) already carries live delegate state on ask.

## Decision

Kill the delegation status machinery outright — both halves:

1. The herdr glass: qq-status's herdr report/notify paths, stage tokens,
   pane presence. Removal remains parked with T-95 (T-94 HOLD).
2. The plain detail-file protocol: /tmp/qq-delegates detail files, the
   prefix+d popup renderer (cockpit/herdr config), delegate-batch's
   status-surface reporting section, and qq-status's detail-file write path.
   Deleted now under T-116.

T-95's 'detail-file protocol stays as the ambient record' text is superseded.
Delegate visibility going forward: transcripts and pi-intercom for live
state; pi-subagents native artifacts/widgets become the story when T-95
un-parks.

## Consequences

- The accepted loss widens from out-of-transcript blocked-delegate
  notification to all out-of-transcript delegate status until T-95 lands.
  Accepted: the surface never gated dispatch and was never read.
- T-113 closed moot. T-115 landed whole in PR #155 minutes before this
  disposition; T-116's deletion therefore reverts its status-file additions
  (delegate-batch namespacing, qq-status --batch-label, the doc-43 amendment,
  tests/test-qq-status.sh pins) together with the rest of the surface.
  T-116 owns the deletion.
- In-flight dispatches are unaffected: the surface never gates dispatch, the
  envelope contract, or the completion wake, and qq-status keeps publishing
  to herdr until T-95.
- openwiki/ operations and workflows pages describe the surface; refresh
  flagged for the wiki maintainer.
