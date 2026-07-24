---
id: doc-95
title: T-157 trustworthy remote OpenWiki refresh workflow — approved research plan
type: specification
created_date: '2026-07-24 18:53'
updated_date: '2026-07-24 20:16'
---
# T-157 — trustworthy remote OpenWiki refresh workflow research plan

**Owning Task:** T-157
**Status:** Approved by the operator in the project-home accountable session on 2026-07-24.
**Change boundary:** Research, recommendation, and implementation-plan capture only; no runtime, workflow, repository-setting, credential, paid-inference, or generated-wiki mutation.

## Intended outcome

Specify the smallest upstream-first workflow that makes OpenWiki remotely refreshed, provenance-visible, and useful between updates. Start from upstream's actual global Git-delta and surgical page-impact behavior rather than adding deterministic page invalidation without evidence. Return a decision-grade provider/authentication disposition and a implementation plan with observable rollout evidence and rollback.

## Semantic contract

A recurring domain, dedicated Skill or agent name, schedule, branch/worktree, single-writer lock, or task-specific lifecycle does not independently justify a role. Normalize a candidate into an existing role plus its assignment, Skill, workflow, resources, and triggers; admit a new role only if substitution still violates a residual Actor-level authority, accountability, independence, evidence, or lifecycle invariant. OpenWiki maintenance is therefore treated as a specialized workflow/capability under an existing role unless this investigation proves such a residual invariant.

## Investigation

1. Verify current OpenWiki release and `main` semantics for surgical update planning, no-change assessment, successful/interrupted/partial runs, metadata, output confinement, custom CI triggers, and pending release fixes.
2. Compare GitHub-hosted inference paths against the operator's preference for GPT-5.6 Sol with explicitly verified xhigh effort: ChatGPT/Codex subscription OAuth, metered OpenAI API, the previously proven OpenAI-compatible Kimi path, and any smaller safe alternative. Trace credential persistence/rotation, model/effort transport, cost visibility, and failure behavior. Make no paid calls and mutate no settings or secrets.
3. Verify GitHub Actions and GitHub pull-request mechanics required for relevant post-land plus daily/manual recovery triggers, latest-main coalescing, one generated branch, CI execution, exact bot authority, narrow auto-merge, stale-base refusal, and recursion avoidance.
4. Define an honest provenance/status contract. Separate generator checkpoint metadata from qq's trust claim; name exactly what a successful attestation proves and what remains model-derived. Define human and agent visibility plus safe primary-main synchronization without automatic mutation of linked Change worktrees.
5. Define the workflow's operational evidence: update latency, provider/model/effort acknowledgement, subscription-quota use, touched-page precision, stale-claim and omission rate, no-change behavior, supersession under multiple landed Changes, failure recovery, and rollback.
6. Compare adopt-as-is, configure upstream, thin qq adapter, and upstream-capability options. Apply smallest-resulting-system and do not recommend page-level provenance/invalidation before evidence demonstrates that upstream's surgical global-delta model is insufficient.

## Success evidence

- Every load-bearing claim cites current primary documentation/source or an explicit gap.
- Release and current-main differences are separated.
- Provider/authentication options include durable secret-state and explicit effort evidence, not model-name inference.
- Auto-merge authority and failure containment are specified against current Repository settings without changing them.
- The implementation plan names exact Checks, rollout gates, operating signals, stop conditions, and rollback.
- Repository records pass applicable Checks and fresh-context review.

## Non-goals

No GitHub setting, ruleset, Actions secret, provider credential, paid inference, local installation, runtime pin, production workflow, auto-merge activation, OpenWiki refresh, generated `openwiki/` edit, or deterministic page dependency graph belongs to this Change.
