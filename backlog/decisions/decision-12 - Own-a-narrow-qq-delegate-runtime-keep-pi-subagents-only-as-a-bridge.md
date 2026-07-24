---
id: decision-12
title: Own a narrow qq delegate runtime; keep pi-subagents only as a bridge
date: '2026-07-24 07:11'
status: accepted
---
## Context

qq's production delegated workflows use a much narrower contract than the
installed `pi-subagents` package provides. `code-review` and `delegate-batch`
each launch one canonical role into one assigned worktree with fresh context,
an exact completion schema, explicit no-acceptance semantics, asynchronous
lifecycle evidence, hard timeout and cleanup, and contract-preserving resume.
They do not need generic agent discovery, chain graphs, dynamic fan-out,
scheduling, model-routing authority, sharing, or watchdog orchestration.

The installed `pi-subagents` 0.35.1 violates that narrow contract in two proven
ways. A child can recover from a tool error and submit valid terminal
`structured_output`, yet the parent later reclassifies the completed run as the
earlier error. Async resume can also reject or alter persisted acceptance and
structured-output metadata. Fresh local prototypes established that upstream
commit `f1540b09283a1c176a0c721878453c6382ecd399` contains the needed acceptance
and single-run schema foundations, and that one small additional recovery
patch makes a successful terminal `structured_output` result supersede earlier
recovered tool failures. The prototype passed 278 targeted execution tests and
20 resume tests.

No maintained external replacement met qq's combined completion, confinement,
lifecycle, cleanup, role-context, and ownership requirements. At the same time,
qq already owns the difficult host boundary in `bin/qq-dispatch`: worktree
validation, Landstrip policy selection, timeout, process-tree cleanup, runtime
directories, and observation. The remaining qq-specific launcher is therefore
substantially narrower than the general-purpose package.

## Decision

Use a qq-controlled GitHub fork of `pi-subagents`, based exactly on upstream
commit `f1540b09283a1c176a0c721878453c6382ecd399`, as an immediate bridge. Carry
only the bounded terminal structured-output recovery patch, pin Pi to an
immutable fork commit, and migrate qq's one-step delegated workflows from
one-step chains to true single runs so the persisted recovery descriptor owns
the complete schema and acceptance contract.

The fork is not qq's long-term delegation foundation. Build a narrow qq-owned
delegate runtime around the contract qq actually uses: canonical trusted roles,
one child per invocation, fresh role context, one assigned worktree, exact
structured completion, asynchronous lifecycle evidence and notification, hard
timeout and process-tree cleanup, and contract-preserving status, stop, wait,
and resume. Reuse `bin/qq-dispatch` and Landstrip as the replaceable confinement
driver. Retire the fork once the qq runtime passes the same contract suite and
all production callers and observation assembly have migrated.

The operator approved this bridge-and-replace direction in the 2026-07-24
asked-and-answered alignment exchange. Existing dispositions remain in force:
Landstrip provides the decision-8 drift-net with open delegate network egress;
decision-10 keeps persisted Pi session JSONL as the sole agent-content
observation seam; and T-152/doc-88 keeps role and execution-profile authority
in qq rather than in a delegate package.

## Consequences

- qq temporarily accepts maintenance of one exact fork delta instead of waiting
  for an upstream release, but upgrades only deliberately and never tracks a
  moving branch or package tag.
- The bridge Change must reproduce both defects before the repair, prove
  terminal success and invalid-output failure after it, and prove that resume
  preserves role, cwd, session, schema, acceptance, timeout, and output
  contract.
- Production skills use the narrow single-run call shape. Chains, generic
  fan-out, schedulers, generic agent discovery, model fallback/routing, and
  similar general-purpose features are not requirements for the qq runtime.
- The qq runtime must fail closed on unknown or untrusted role occupancy and on
  missing or malformed completion/lifecycle metadata. It does not weaken
  Landstrip confinement, cleanup, timeout, or owner verification of a
  completion envelope.
- Lifecycle status and notification may be live, but agent content remains in
  persisted session JSONL only. This decision does not dispose of the separate
  Change-attribution question under decision-10 and does not mutate observer
  ledger findings.
- The bridge and its replacement are separate Changes with separate owning
  Tasks and fresh review. The bridge may land first without committing qq to
  preserve the fork's internal APIs or artifact format beyond the migration
  window.
