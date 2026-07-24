---
id: doc-96
title: Remote OpenWiki freshness and automation — upstream-first workflow evidence
type: other
created_date: '2026-07-24 19:14'
updated_date: '2026-07-24 21:00'
tags:
  - research
  - openwiki
  - github-actions
  - provenance
---
# Remote OpenWiki freshness and automation — upstream-first workflow evidence

**Owning Task:** T-157
**Investigation cut:** 2026-07-24 19:08 UTC
**Overall confidence:** HIGH for inspected release/source/GitHub behavior; MEDIUM for unproven prospective bot and provider setup.
**Settles:** the safe release gate, smallest provenance addition, provider recommendation, GitHub automation shape, and rollout evidence needed before automated merge. No settings, secrets, installations, workflows, or paid calls were changed.

## Findings

### 1. Do not deploy npm `openwiki@0.2.3`

- **[HIGH, observed]** Npm `latest` remains `0.2.3`. Its late-failure path can persist success-shaped `.last-update.json` after partial output, causing later clean same-HEAD runs to skip. Upstream merged `status: complete|interrupted` handling in [PR #365](https://github.com/langchain-ai/openwiki/pull/365), but it was unreleased at the investigation cut. [0.2.3 catch path](https://github.com/langchain-ai/openwiki/blob/1a7c9fe16df4ac12a41cad85a252a9b9c93b2c3e/src/agent/index.ts#L316-L343) · [main fix](https://github.com/langchain-ai/openwiki/blob/2a0fe7feb5d9588666325825f93dc633b510a652/src/agent/index.ts#L325-L380)
- **[HIGH, observed]** A separate silent-completeness defect remains open: truncated streamed tool calls can leave planned writes missing without failing the run. [PR #457](https://github.com/langchain-ai/openwiki/pull/457) adds the guard but is open; [PR #459](https://github.com/langchain-ai/openwiki/pull/459) separately exposes output-token limits.
- **[HIGH, recommendation]** Gate unattended refresh on the first immutable upstream release containing both #365 and #457. Pin the release and every Action; do not pin an arbitrary moving `main` commit for unattended generation.

### 2. Preserve upstream’s update model; add one modest qq attestation

- **[HIGH, observed]** Upstream already supplies the important incremental behavior. One global Git window is passed to a model that must build `source change → docs affected → edit needed`, touch only inaccurate pages, observe a small-change page budget, and permit a no-op. This was deliberately strengthened by a maintainer in [commit f396412](https://github.com/langchain-ai/openwiki/commit/f396412230b504392d8255b5deeb069584874837). No evidence shows maintainers considered and rejected deterministic page provenance.
- **[HIGH, observed]** `.last-update.json` is a global diff cursor and coarse run marker, not a trust attestation. It lacks provider, effort, output hash, assessed-page set, dependency set, workflow run, PR, and merge identity. A successful assessment that changes no wiki bytes normally leaves the old cursor, causing the same source window to be assessed again. [0.2.3 metadata](https://github.com/langchain-ai/openwiki/blob/1a7c9fe16df4ac12a41cad85a252a9b9c93b2c3e/src/agent/utils.ts#L142-L192) · [main metadata](https://github.com/langchain-ai/openwiki/blob/2a0fe7feb5d9588666325825f93dc633b510a652/src/agent/utils.ts#L176-L206)
- **[HIGH, recommendation]** Add no page dependency graph. A thin qq wrapper writes `openwiki/.qq-refresh.json` only after a successful assessment, including semantic no-change: schema, source commit/time, workflow run URL/id, pinned OpenWiki version, provider/model, requested/transported/effective effort, outcome `changed|no-change`, docs-tree hash, and changed-page list. Failure or cancellation writes no completed attestation.
- **[HIGH, recommendation]** `current` remains a modest global claim: the attested run completed and no relevant non-generated path differs from its source commit. It authorizes orientation, never truth. Compare paths rather than `HEAD == sourceCommit`, because the generated docs merge necessarily advances HEAD. Ignore generated `openwiki/**` except re-include the operator-owned `openwiki/INSTRUCTIONS.md`. `stale` means a relevant landed path changed; `unknown` means remote, ancestry, marker, or run evidence is missing or contradictory.
- **[HIGH, observed]** Upstream mechanically confines agent filesystem writes to `openwiki/`, but `INSTRUCTIONS.md` is inside that boundary. qq must post-check an exact allowlist and require `INSTRUCTIONS.md` unchanged. Existing custom CI workflow files are preserved in 0.2.3. [PR #285](https://github.com/langchain-ai/openwiki/pull/285)

### 3. Use the Kimi Code subscription for remote refresh; do not add token billing or OAuth state machinery

- **[HIGH, operator disposition]** Straight metered API inference is outside the workflow. The operator requires existing subscription entitlement; Anthropic subscription is rolling out of use, leaving Kimi Code and OpenAI Codex subscription paths.
- **[HIGH, observed]** Kimi Code officially supports durable console-created API keys against both OpenAI-compatible `https://api.kimi.com/coding/v1` and Anthropic-compatible `https://api.kimi.com/coding/` endpoints. Calls consume membership quota, not Open Platform pay-as-you-go balance, provided Extra Usage remains disabled. All keys share weekly, rolling five-hour, and monthly subscription quotas. [membership](https://www.kimi.com/code/docs/en/kimi-code/membership.html) · [models/protocols](https://www.kimi.com/code/docs/en/kimi-code/models) · [authentication distinction](https://www.kimi.com/code/docs/en/kimi-code/faq.html)
- **[HIGH, observed]** Kimi currently offers `k3-256k` and `k3` to Moderato-and-above members; `k3-256k` has the same model results within 256K while consuming less quota. K3 accepts `low|high|max`, defaults to `high`, and maps client `xhigh` to `max`. Lower tiers retain `kimi-for-coding`. Exact entitlement is account-specific and unproven until activation. [Kimi model configuration](https://www.kimi.com/code/docs/en/kimi-code/models)
- **[HIGH, observed]** T-97 already proved qq's existing Kimi Code key through OpenWiki's OpenAI-compatible provider using `kimi-for-coding`. Current OpenWiki main supports a generic OpenAI-compatible base URL/model and an Anthropic custom base URL/model, but it does not expose reasoning effort. Its pinned `@langchain/openai` can transport a compatible field after a small validated seam.
- **[HIGH, recommendation]** First deployment choice: `k3-256k` through the OpenAI-compatible endpoint with its provider-documented default `high` effort, falling back to `kimi-for-coding` with thinking on only if the subscription lacks K3. This avoids an unsupported OpenWiki effort patch; use explicit `xhigh`→K3 `max` only in a later measured comparison or after upstream exposes the field. Before inference, prove exact request shape against a local capture server and perform a non-generating entitlement/auth probe if the service permits one. Record configured model, effective server model where exposed, requested/transported/effective effort, quota-limit failures, and whether Extra Usage is disabled.
- **[HIGH, observed]** OpenAI Codex OAuth still rotates mutable refresh state into `~/.openwiki/.env`. Ephemeral runners cannot durably carry that state without a secret-write service, encrypted state store, or manual reauthentication. That machinery is larger and more privileged than the refresh workflow. Keep Codex subscription remote-auth durability as a separate follow-up, not a hidden dependency of this workflow. [OpenWiki OAuth persistence](https://github.com/langchain-ai/openwiki/blob/2a0fe7feb5d9588666325825f93dc633b510a652/src/agent/openai-chatgpt-oauth.ts#L520-L545)

### 4. The narrow automated merge needs a bot identity and a current-base rail

- **[HIGH, observed]** `hypermemetic-ai/qq` currently has auto-merge disabled, read-only default Actions permissions, no Actions secrets, and an active `main` ruleset requiring a pull request plus `shell-tests`. Required checks are loose (`strict_required_status_checks_policy=false`). There is no ruleset bypass. Current settings were read through the GitHub API without mutation.
- **[HIGH, observed]** A PR made with `GITHUB_TOKEN` does not provide unattended ordinary CI: current GitHub behavior places its `pull_request` runs in approval-required state, while most other token-created events are suppressed. A GitHub App installation token or fine-grained PAT creates ordinary events. [GitHub token-trigger behavior](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
- **[HIGH, recommendation]** Use one dedicated repository-installed `qq-openwiki` GitHub App with only metadata/read, checks/Actions read, contents read/write, and pull-request read/write. Give it no ruleset bypass. Exact identity is bot + `openwiki/update` head + `main` base + one commit parented by the fetched main SHA. Add the App to the existing classic main restriction only.
- **[HIGH, operator disposition]** Treat relevant `push`, `workflow_dispatch`, and off-hour daily recovery as wake-up signals for one level-triggered latest-state generator. Serialize with `cancel-in-progress: false`; whichever queued run survives fetches latest main only when it starts, exits if that source is already current, and discards stale output at the final recheck. This makes GitHub's unordered concurrency harmless while keeping one generation at a time. Semantic reviews remain uncancelled and may rarely overlap generation or one another after passing an earlier exact-head gate; later gates prevent stale publication or merge, and the operator accepts that subscription-quota trade-off instead of a cross-workflow semaphore. The App-created PR starts ordinary CI; semantic review starts only after successful generation `workflow_run` and has no cancellation group. Each review's exact base/head gates make delayed obsolete reviews exit without cancelling the current review. Before review credentials, publish, and merge, require latest main, exact diff allowlist, exact attestation, and force-with-lease on the fixed branch. A branch published just before runner failure cannot pass successful-run evidence and cannot merge.
- **[HIGH, observed]** REST merge accepts an expected head SHA but not an expected base SHA. With loose required checks, main can advance after the final validation and a stale generated PR can still merge. Strict checks or a merge queue would close this race but impose repository-wide coordination machinery. [REST merge](https://docs.github.com/en/rest/pulls/pulls#merge-a-pull-request) · [strict checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#require-status-checks-to-pass-before-merging)
- **[HIGH, operator disposition]** The workflow uses recheck-and-repair rather than strict checks or a merge queue. The App checks latest main immediately before guarded REST merge. If the small race still occurs, the path comparator immediately reports the attestation stale and the main push schedules a replacement refresh. This is proportionate for derived documentation and changes no global PR policy.
- **[HIGH, recommendation]** Ordinary `shell-tests` and a separate exact-head, read-only fresh-context `openwiki-review` must pass. The review samples every touched page, plausible untouched pages, source claims, provenance, links, and scope. One workflow that generates, pre-checks, and merges its own unverified PR head is insufficient.

### 5. Local consumption should expose status without making OpenWiki a universal gate

- **[HIGH, recommendation]** Add `qq-openwiki-status`. In the sole clean, non-diverged primary main checkout it checks/fetches remote state and may fast-forward only; otherwise it refuses mutation. In linked Change worktrees it never rebases, merges, resets, or switches. It reports whether the branch contains the attestation and whether branch changes make the wiki stale for that Change.
- **[HIGH, recommendation]** Humans and agents see source SHA/time, local and remote `current|stale|unknown`, latest run outcome, provider/model/effort, pinned version, and run URL. `current` authorizes derived orientation only; `stale` permits cautious navigation with source verification; `unknown` authorizes no freshness claim. A failed later run is visible without erasing the last successful attestation.
- **[HIGH, observed]** At the investigation cut, local OpenWiki metadata pointed to `0863c6b` while primary main was `054d79e`, with hundreds of later non-generated paths. The current qq wiki is globally stale under this contract.

### 6. No librarian or custodian role follows

- **[HIGH, conclusion]** Normalize OpenWiki into an existing role plus assignment, Skill, workflow, resources, and triggers. The fixed branch, schedule/push event, provider, single-writer behavior, code review, and attestation are procedural properties. They establish no residual Actor-level authority, accountability, independence, evidence, or lifecycle invariant requiring a new role.
- **[HIGH, conclusion]** Generation is a constrained implementer-role assignment; the independent semantic assessment supplies reviewer-role evidence; the App is a workflow identity rather than a methodology role. Revise the `openwiki-maintainer` Skill from “scheduled/on-demand only, never self-merge” to the approved remote post-land assignment and exact App-only merge exception while source Changes still never invoke it.

## Operational acceptance and rollback

Before enabling App-issued merge, run the remote generator with operator-owned merge and demonstrate one localized Change, one cross-cutting Change, semantic no-change, a two-merge burst, a failed/cancelled generation, and daily/manual recovery. Extra Usage stays disabled; each source commit gets at most one generation attempt plus one recovery attempt; a run stops after **60 minutes** without a PR or terminal recovery result.

Operate and record:

- land→PR and land→merge latency (target: at least 90% within 30 and 90 minutes respectively);
- model calls, tokens where exposed, and subscription-quota impact per successful source commit;
- no-change assessments and repeated calls (target: zero repeated subscription assessment);
- touched-page precision (target: at least 90%);
- sampled material stale claims and omissions (target: zero);
- latest-state coalescing under a two-merge burst;
- one failed/cancelled generation and daily/manual recovery;
- wrong bot/head/base, outside-scope, immutable-instructions, obsolete-head, and false-attestation refusal;
- operator burden (target: at most 30 minutes/week after setup).

After activation, immediately disable automated merge and generation on secret/log exposure, wrong identity, outside-allowlist or `INSTRUCTIONS.md` mutation, false completed attestation, silent missing planned write, ordinary-Change auto-merge, material stale claim, repeated unrecovered failure, or unexpected paid Extra Usage. A slipped stale-base race is not an emergency: status must report stale and the recovery trigger must replace it. Close unsafe generated PRs, revoke App/provider credentials when compromised, preserve evidence, and revert generated docs only through an ordinary PR.

## Disposition

| Option | Disposition |
|---|---|
| Adopt `0.2.3` as-is | Reject. |
| Configure upstream | Use for triggers, pinning, provider, telemetry-off, output confinement, and surgical impact behavior. |
| Thin qq adapter | Use for one global attestation/status comparator plus exact App/scope rails and recheck-and-repair freshness. No page map. |
| Upstream capability | Wait for #365+#457 in a release. Consider explicit effort only after a measured quality need; consider upstreaming successful no-change/provenance later. |

## Sources

- OpenWiki [0.2.3 release](https://github.com/langchain-ai/openwiki/releases/tag/0.2.3), [update source](https://github.com/langchain-ai/openwiki/tree/1a7c9fe16df4ac12a41cad85a252a9b9c93b2c3e/src/agent), [PR #365](https://github.com/langchain-ai/openwiki/pull/365), [PR #457](https://github.com/langchain-ai/openwiki/pull/457), [PR #459](https://github.com/langchain-ai/openwiki/pull/459), [PR #285](https://github.com/langchain-ai/openwiki/pull/285), and [surgical prompt commit](https://github.com/langchain-ai/openwiki/commit/f396412230b504392d8255b5deeb069584874837).
- OpenAI [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol) and [model guidance](https://developers.openai.com/api/docs/guides/model-guidance?model=gpt-5.6), used only to verify the rejected metered route and the deferred Codex target.
- Kimi Code [membership](https://www.kimi.com/code/docs/en/kimi-code/membership.html), [model and protocol configuration](https://www.kimi.com/code/docs/en/kimi-code/models), [third-party authentication](https://www.kimi.com/code/docs/en/third-party-tools/other-coding-agents.html), and [FAQ](https://www.kimi.com/code/docs/en/kimi-code/faq.html).
- GitHub [workflow triggers](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow), [concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency), [cache security](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching#restrictions-for-accessing-a-cache), [REST pull-request merge](https://docs.github.com/en/rest/pulls/pulls#merge-a-pull-request), and [ruleset status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#require-status-checks-to-pass-before-merging).
- qq local source and records: `openwiki/.last-update.json`, `openwiki/INSTRUCTIONS.md`, `bin/qq-openwiki`, T-97, and current read-only GitHub repository settings.

## Remaining activation-time facts

1. Confirm the operator's current Kimi plan entitlement. Prefer `k3-256k` at its documented default `high`; otherwise pin `kimi-for-coding` with thinking on. This is a model entitlement fact, not authorization for paid Extra Usage. Explicit K3 `max` remains a measured follow-up, not a hidden patch.
2. Create one methodology-scoped `qq-openwiki` GitHub App and install it only on qq for the initial rollout. The same App may later be installed on deliberately selected adopting repositories; it is not one App per repository.
3. Organization-level inherited Actions policy/secret inventory returned 403 and requires an organization administrator if later evidence makes it material.
