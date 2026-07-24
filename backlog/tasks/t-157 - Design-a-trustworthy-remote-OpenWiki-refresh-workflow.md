---
id: T-157
title: Design a trustworthy remote OpenWiki refresh workflow
status: In Progress
assignee: []
created_date: '2026-07-24 18:53'
updated_date: '2026-07-24 21:00'
labels: []
dependencies: []
documentation:
  - doc-95
  - doc-96
  - doc-97
type: spike
ordinal: 73000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Research and specify the smallest upstream-first mechanism that makes OpenWiki remotely refreshed, provenance-visible, and useful between updates without inventing an unproven page-dependency subsystem. Reconcile the workflow with the role-model finding that OpenWiki maintenance is a specialized assignment/capability under existing roles, not evidence for a librarian or custodian role.

This Change is evidence and an approved implementation/rollout plan only. It does not mutate GitHub settings or secrets, install or pin a runtime, run inference, add the refresh workflow, enable automated merge, or refresh generated OpenWiki pages.

Decision ledger:
- Approved research boundary, semantic contract, method, success evidence, and non-goals — doc-95, approved by the operator's “proceed” instruction in the project-home accountable session on 2026-07-24.
- Proceed with the smallest serious upstream-first OpenWiki mechanism after verifying upstream's actual model — operator instruction “proceed” following the 2026-07-24 upstream-rationale exchange.
- Start with upstream's global Git-delta plus surgical model impact-plan behavior; do not build deterministic per-page invalidation before operating evidence shows it is needed — operator instruction “proceed” following the recommendation in the same exchange.
- Target relevant post-land refreshes with daily/manual recovery rather than laptop-bound exact-time scheduling — asked-and-answered operator direction in the 2026-07-24 OpenWiki trust exchange.
- Generated documentation-only refreshes may use a narrowly constrained automated-merge exception after exact identity, scope, freshness, validation, and review rails — operator selected “Narrow auto-merge” in the 2026-07-24 alignment questionnaire.
- Do not use metered inference. Use existing subscription entitlement; Kimi Code's durable membership key is the smallest remote path, while OpenAI Codex OAuth state durability is deferred — operator disposition on 2026-07-24 after provider research.
- Use one methodology-scoped `qq-openwiki` GitHub App, initially installed only on qq, rather than one App per Repository — operator question and follow-up disposition on 2026-07-24.
- Use immediate latest-main recheck plus a repository receipt and automatic repair instead of repository-wide strict checks or a merge queue. A rare slipped race may briefly lag, but status must report stale and trigger replacement — operator selected “Recheck and repair” on 2026-07-24.
- Describe this as the production freshness mechanism with a cautious rollout, not as a fixed-duration experiment — operator instruction on 2026-07-24.
- Research/design precedes runtime and settings mutation because the required upstream interrupted/truncation fixes are not yet available together in an immutable release — operator “proceed” after the release gap was presented.
- Approve the production freshness mechanism and rollout in doc-97 after its receipt, independent review, latest-main recheck, detectable slipped-race staleness, and automatic repair behavior were explained directly — operator “Yeah, I approve it, that’s good” on 2026-07-24.
- Generation owns coalescing as a level-triggered latest-state worker: serialize without cancellation, treat events as wake-ups, fetch latest main after acquiring the slot, and discard stale output at final recheck — operator selected “Latest-state worker” after the review convergence breaker on 2026-07-24.
- Scope serialization to generation only. Read-only semantic reviews may rarely overlap generation or another review after an earlier freshness gate; exact later gates prevent stale publication/merge, and this bounded quota trade-off is preferred over a durable cross-workflow coordinator — operator selected “Generation only” on 2026-07-24.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A cited, confidence-tagged report verifies upstream release/main freshness semantics, trigger customization, provider/model/effort and remote-auth options, automated-merge mechanics, and known gaps from primary sources and safe probes
- [ ] #2 The approved implementation plan explains the receipt/recheck/automatic-repair mechanism and defines exact provenance semantics, remote triggers, single-writer behavior, narrow merge rails, synchronization, failure handling, rollout acceptance, operating signals, and rollback
- [ ] #3 The role-model consequence is explicit: generation is an implementer assignment, semantic checking supplies reviewer evidence, and no librarian/custodian role is created absent a residual Actor-level invariant
- [ ] #4 The Change mutates no GitHub setting or secret, performs no inference, installs or pins no runtime, adds no production workflow, and does not hand-edit or regenerate openwiki/
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Verify current upstream release/main behavior and release gates for successful/interrupted/no-change updates, surgical impact planning, custom triggers, provider/model/effort controls, and output confinement.
2. Compare GitHub-hosted subscription authentication options against durable secret state and smallest-system constraints without making inference calls or changing settings.
3. Specify the core receipt/recheck/automatic-repair mechanism, remote post-land and recovery triggers, single-writer/coalescing, narrow App authority, status/synchronization boundary, failure recovery, operating signals, and rollback.
4. Reconcile role semantics: generation is an implementer assignment, independent semantic assessment supplies reviewer evidence, and App/schedule/branch/provider are workflow properties rather than a new role.
5. Deliver one cited research document and one approved implementation/rollout plan; verify Backlog records and receive fresh-context review. No runtime or machine-setting mutation belongs to this Change.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-07-24 research disposition (doc-96): reject OpenWiki 0.2.3; wait for a release containing #365 and #457; preserve upstream global-delta surgical updates; add only a thin global receipt/status layer; use Kimi Code subscription with Extra Usage disabled; defer remote Codex OAuth state machinery.

2026-07-24 approved mechanism (doc-97): one methodology-scoped qq-openwiki App initially installed only on qq; relevant post-land generation with daily/manual recovery; one fixed branch; independent fresh OpenWiki semantic assessment; immediate base recheck; and provenance-visible automatic repair if the final non-atomic merge interval slips. The guarantee is detectable, self-repairing staleness—not impossible lag.

Approved rollout: land an inactive foundation, operate remote generation with operator-owned merge until acceptance cases pass, then enable only the App's exact guarded merge. No fixed-duration or dollar-budget experiment remains.

2026-07-24 review convergence disposition: GitHub concurrency ordering is not treated as newer-wins. The operator selected the generation layer as owner: one non-cancelling serialized latest-state worker, wake-up events rather than ordered source assignments, current-status preflight, and final stale-output discard. Semantic reviews are uncancelled and exact-base/head gated.

2026-07-24 provider-overlap disposition: serialization covers generation only. Read-only semantic reviews may overlap after becoming obsolete post-gate; exact later gates prevent publication or merge. The operator preferred that quota trade-off to a cross-workflow semaphore or combined coordinator.
<!-- SECTION:NOTES:END -->
