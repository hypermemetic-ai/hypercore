---
id: doc-93
title: Plan — upstream pi-subagents and researcher-only Context7 spike
type: specification
created_date: '2026-07-24 17:50'
updated_date: '2026-07-24 17:50'
---
**Owning Task:** T-154.3

## Outcome

Decide whether qq should keep pi-subagents as its vendor-owned delegated-execution runtime instead of building T-154.2's narrow replacement, and prove whether Context7 can be available only to researcher children through its native Pi extension without any MCP server.

## Governing dispositions

- Operator chose an isolated upstream spike before changing production.
- Operator chose Context7 for researchers, not reviewers.
- This explicitly reopens T-154.2's current destination decision for evidence; it does not reverse it before the spike reports.
- T-154.1's immutable production pin and recovery semantics remain the rollback baseline.

## Change boundary

One child Task/Change under T-154. No production package/config/runtime mutation; no global install, API key, login, MCP process, or merge. Use isolated clones/prefixes and public Context7 rate limits. Durable outputs are the experiment harness/evidence, a cited decision report, review, and PR handoff.

## Experiments

1. Rebase/cherry-pick qq's terminal structured-output recovery patch onto the latest reviewed upstream pi-subagents commit; inspect the complete delta.
2. Run upstream's full suite and qq's black-box delegation contract against the candidate.
3. Exercise the capabilities that could change qq's design: FleetView, parallel and expanded fleets, chains, worktree fan-out, async completion/wait/steer/resume/append-step, artifact/output isolation, progress, schedules, and watchdogs.
4. Map each proven capability to qq machinery it could replace, shrink, or leave distinct—especially T-154.2, qq-status/cockpit detail, lifecycle notification, role policy, observation, and confinement.
5. Trial official `@upstash/context7-pi` in the isolated runtime as a researcher-child-only extension. Prove `resolve-library-id`, `query-docs`, and `/c7-docs` are available to the researcher and absent from the accountable parent and reviewer. Use public/IP limits only; do not create or request a key.
6. Compare child-local extension loading on the pinned production bridge and upstream candidate; treat inability to scope the extension as a product finding, not permission for a global install.
7. Produce a decision matrix and recommendation: retain vendor runtime, adapt/fork, or proceed with narrow replacement; and adopt native researcher-only Context7 or remove it.

## Success evidence

- Exact upstream and patch provenance.
- Existing recovery and qq delegation contracts remain green.
- Every claimed new capability has a recorded live probe, not README inference.
- Concrete deletion/shrinkage map with ownership boundaries.
- Context7 is demonstrated without MCP and without reviewer/parent exposure, or the limitation is proven.
- Fresh independent review; one green PR; no production mutation.

## Non-goals

Production upgrade, T-154.2 implementation, role/model-routing changes, new security claims, observer content-seam changes, global Context7 installation, credentials/private docs, or automatic recommendation enactment.
