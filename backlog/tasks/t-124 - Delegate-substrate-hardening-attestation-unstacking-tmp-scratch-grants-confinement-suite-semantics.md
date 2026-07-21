---
id: T-124
title: 'Delegate substrate hardening: attestation unstacking, /tmp scratch grants, confinement-suite semantics'
status: In Progress
assignee: []
created_date: '2026-07-20 19:40'
labels: []
dependencies:
  - T-95
priority: high
type: task
ordinal: 54000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Production hardening for the T-95 substrate, from owner-verified findings in its first two production dispatches (T-121 ticket 1 and the AC#3 probes):

1. **Stacked attestation fails every run.** pi-subagents' inferred acceptance contract (writer-shaped "Acceptance Contract" prompt + final-message fenced acceptance-report) conflicts with qq's strict completion-envelope schema: children emit the envelope via structured_output, never a final fenced report, so runs end "rejected"/nonzero despite complete, verified work. Fix: manifests declare `acceptance: {level: none, reason}` — qq acceptance is the envelope schema + owner verification against the tree + fresh-context review.
2. **Confined children cannot create scratch repos.** Engine tests `git init` under mktemp dirs; policies grant no /tmp writes. Fix: every role policy grants /tmp writes EXCEPT a recursive deny of the delegate runtime root (protects sibling run dirs, staged auth, envelope captures; auth.json denyWrite stands).
3. **/dev/fd process substitution cannot pass Landlock** (owner probe: unfixable at policy level). Engine scripts/tests using `< <(...)` fail inside confined children. Fix is semantic, not policy: skills document that a child's confined suite run is best-effort; the binding green is the owner's native rerun + CI, which the workflow already requires.

Decision ledger:
- Findings and remedies 1–3: owner-verified live evidence, 2026-07-20 (policies rendered and probed natively; run 90f9c79e artifacts; /dev/fd policy-grant probes).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A production dispatch ends without the spurious attestation rejection, envelope intact
- [ ] #2 Confined implementer can run tmp-repo engine tests; sibling runtime-root writes stay denied fresh
- [ ] #3 Skills state the confinement-suite semantics (best-effort child run; owner native rerun + CI bind)
<!-- AC:END -->
