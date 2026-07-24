---
id: doc-97
title: Trustworthy remote OpenWiki refresh — implementation and rollout plan
type: other
created_date: '2026-07-24 19:35'
updated_date: '2026-07-24 21:00'
tags:
  - plan
  - openwiki
  - github-actions
  - rollout
---
# Trustworthy remote OpenWiki refresh — implementation and rollout plan

**Owning Task:** T-157
**Evidence:** doc-96
**Status:** Approved by the operator in the project-home accountable session on 2026-07-24 after the receipt/recheck/automatic-repair mechanism was explained in conversation.
**Boundary:** This plan authorizes later implementation Changes only after their own alignment. T-157 itself remains research/design and performs no activation.

## Outcome

After relevant Changes land on `main`, GitHub-hosted automation assesses the global source delta with upstream OpenWiki, proposes only affected documentation, obtains an independent fresh-run semantic check plus ordinary CI, and narrowly merges the generated-only PR through one reusable `qq-openwiki` GitHub App. Daily and manual triggers recover missed or failed work. A small attestation and status command make freshness visible without making OpenWiki authoritative or globally unavailable.

Source and fresh Checks remain authoritative. `current` means only “the last relevant source window was successfully assessed and the recorded generated-doc tree is intact.” It never means every claim is true.

## Core freshness mechanism

The workflow makes staleness detectable and self-repairing rather than pretending merge is perfectly atomic:

1. A relevant `main` change starts a refresh from source commit **A**.
2. OpenWiki generates a one-commit documentation PR. That same commit contains a qq receipt stating that the docs were assessed from **A**, with the workflow run, OpenWiki version, provider/model/effort, and docs-tree hash.
3. A separate fresh process checks the proposed documentation and ordinary CI checks the exact PR head.
4. Immediately before merge, the App asks GitHub whether `main` is still **A**. If main has advanced, it does not merge; it discards the obsolete proposal and regenerates from current main.
5. A tiny race remains between that last query and GitHub completing the merge. If main becomes **B** in that instant, the receipt still truthfully says **A**. The status comparator therefore reports the wiki `stale`, never `current`.
6. The push of **B** starts the replacement refresh automatically. Daily and manual triggers recover cases where the push-triggered run was missed or failed.

The guarantee is therefore honest and observable: the wiki may briefly lag, but stale output cannot present itself as current and repair does not depend on the operator's laptop.

## Entry gates

Implementation must not activate generation until all gates pass:

1. Pin the first immutable OpenWiki release containing upstream interrupted-run completion status from #365 and truncated-tool-call failure from #457. Re-inspect the released code and metadata schema; never pin moving `main` for unattended runs.
2. Verify the operator's Kimi Code membership model entitlement without enabling Extra Usage. Prefer `k3-256k`; if unavailable, explicitly approve and pin `kimi-for-coding` as the subscription fallback.
3. Prove, against a local capture server and without inference, the exact provider endpoint, model field, tool-call transport, and absence/presence of reasoning effort. For `k3-256k`, the smallest initial posture is no custom effort field: Kimi documents omitted effort as `high`. Do not claim `xhigh`/`max` unless it is actually transported and observed.
4. Create one methodology-scoped `qq-openwiki` GitHub App, install it only on `hypermemetic-ai/qq` for the initial rollout, and add the App—not a user—to the existing classic `main` push restriction. Give it no ruleset bypass.
5. Complete mock/dry-run refusal tests before placing Kimi or App credentials in Actions.

A missing gate leaves refresh manual and operator-owned; it does not justify a local patch of an unsafe upstream release.

## Repository surfaces

Later implementation Changes add or revise only these operator-owned surfaces plus tests:

- `bin/qq-openwiki-refresh`: CI-safe single-run wrapper; separate from the existing local OAuth-oriented `bin/qq-openwiki`.
- `bin/qq-openwiki-status`: read-only freshness/status comparator with explicit safe sync mode.
- `.github/workflows/openwiki-refresh.yml`: assessment, generation, validation, attestation, and PR publication.
- `.github/workflows/openwiki-review.yml`: exact-identity gate, fresh semantic assessment, ordinary-check verification, and guarded App merge.
- `openwiki/.qq-refresh.json`: one small versioned qq attestation.
- `openwiki-maintainer` Skill and recurring documentation: describe the remote post-land assignment and exact App-only merge exception; source Changes still never invoke OpenWiki maintenance.

Do not add a page dependency map, content database, persistent runner, external queue, OAuth state store, native repository auto-merge, merge queue, or repository-wide strict-check requirement.

## Trigger and single-writer contract

`openwiki-refresh.yml` runs on:

- every `push` to `main`, followed by an in-job relevant-path classifier;
- one off-hour daily `schedule` recovery;
- `workflow_dispatch` with an optional reason, never an arbitrary source SHA.

A change is relevant when the source window includes anything outside generated `openwiki/**`, or includes the operator-owned `openwiki/INSTRUCTIONS.md`. A generated-doc merge containing only allowed generated paths and attestation/metadata is irrelevant and exits before credentials or inference.

Generation is a level-triggered latest-state worker. All push/schedule/manual events are wake-up signals into one `qq-openwiki-generate` group with `cancel-in-progress: false`; GitHub ordering is irrelevant because whichever queued run survives fetches and processes latest `main` only after it acquires the serialized slot. Every wake-up exits before inference when the latest source commit is already attested current. A run that becomes stale while generating finishes but discards its result at the final latest-main check; the queued survivor then processes the newest state.

Semantic review deliberately has no concurrency-cancellation group: a delayed older `workflow_run` must never cancel the review for the current head. The App-created PR independently starts ordinary `pull_request` CI, while semantic review starts only from the refresh workflow's successful `workflow_run` completion. Every review independently requires its recorded source base and PR head to remain current before loading provider credentials and again before merge; obsolete reviews therefore exit without affecting the current review.

Serialization applies to generation only. A read-only semantic review may overlap generation or another review if it becomes obsolete after its pre-credential gate. Exact later gates prevent it from publishing or merging, but it may consume subscription quota. The operator explicitly accepts that bounded overlap rather than adding a cross-workflow semaphore or combined coordinator.

The generated head is fixed at `openwiki/update`. Obsolete runs cannot pass review or merge.

## Generation pipeline

The refresh workflow uses only a read-only `GITHUB_TOKEN` until PR publication:

1. After acquiring the generation slot, fetch and check out latest `origin/main` with full history. The triggering event SHA is never the generation source. Exit before credentials when the latest commit is already attested current.
2. Classify the source window from the last completed receipt to latest main. For only generated paths, record a no-op workflow result and exit before loading provider credentials.
3. Install the exact gated OpenWiki release and immutable-SHA Actions. Disable OpenWiki telemetry and LangSmith tracing.
4. Run `bin/qq-openwiki-refresh` with the Kimi Code subscription key, OpenAI-compatible endpoint `https://api.kimi.com/coding/v1`, and pinned entitled model. The wrapper retains the existing repository-wide lock and confines the run to an isolated fresh-main worktree.
5. Compare the pre/post trees. Allow only generated `openwiki/**` Markdown, upstream `.last-update.json`, and qq `.qq-refresh.json`. Require `openwiki/INSTRUCTIONS.md`, root instruction files, workflows, source, Backlog, and every other path byte-identical.
6. Run deterministic checks: OpenWiki exit/completion status, planned-write completeness supplied by the gated release, Markdown/link validation, no conflict markers, no symlinks or non-regular generated files, no secrets, and exact tree-hash recomputation.
7. On semantic no-change, still advance the assessed source cursor and write a new qq attestation. Use upstream behavior if the gated release gains a successful no-change cursor; otherwise the wrapper updates `.last-update.json` only under an exact tested version/schema contract. This prevents repeated subscription assessment of the same source window.
8. Immediately re-fetch main. If superseded, discard the result. Otherwise mint a one-commit `openwiki/update` branch whose parent is the assessed main SHA, force-with-lease it with a short-lived App token, and create or update one PR against `main`.

A failure before publication writes no completed receipt to the branch. If a runner fails or is cancelled after publication but before GitHub records workflow success, the candidate branch may exist, but `workflow_run` review refuses its non-successful run evidence and nothing can merge.

## Attestation and freshness semantics

`openwiki/.qq-refresh.json` is deterministic JSON with schema version 1 and these fields:

- `source.commit` and `source.committedAt`;
- `completedAt`;
- `workflow.runId`, `runAttempt`, and canonical run URL;
- exact `openwiki.version`;
- `provider.id`, endpoint host, configured model, observed model when exposed, requested effort, transported effort, and effective effort or `unknown`;
- `outcome`: `changed` or `no-change`;
- sorted `changedPages`;
- `docsTreeSha256`, computed from sorted path/NUL/bytes records for tracked `openwiki/**/*.md`, including immutable `INSTRUCTIONS.md` and excluding both mutable metadata JSON files.

The marker is complete only after a successful assessment and all generation checks. It is never written as complete on `finally`, cancellation, or best-effort cleanup.

`qq-openwiki-status` returns:

- `current`: marker/schema/tree are valid; its source commit is an ancestor of the assessed branch; no relevant path differs between marker source and branch;
- `stale`: valid marker, but a relevant later change exists or the docs-tree hash differs;
- `unknown`: missing/invalid marker, unavailable ancestry/remote evidence, incomplete upstream metadata, provider/run contradiction, or unsupported schema/version.

The command prints source SHA/time, local and remote state, latest run outcome when available, pinned version, provider/model/effort, and run URL. It states that source and Checks remain authoritative.

In linked Change worktrees it never switches, merges, rebases, resets, or writes. In the sole clean, non-diverged primary `main` checkout, explicit `--sync` may fetch and fast-forward only; otherwise it refuses. A Change branch can report “wiki current at base, stale for this Change” without mutating the branch.

## Independent review and guarded merge

The App-created same-repository PR triggers ordinary CI. A completed `openwiki-refresh.yml` `workflow_run` triggers `openwiki-review.yml`, which proceeds only when the named refresh concluded successfully and identifies the exact fixed-branch PR. Before any secret is loaded, the review workflow requires:

- exact App author/installation identity;
- base `main`, head `openwiki/update`;
- exactly one head commit whose parent equals the recorded assessed base;
- changed paths confined to generated OpenWiki Markdown and the two metadata files;
- immutable `openwiki/INSTRUCTIONS.md` and workflow/source paths;
- valid attestation matching the head bytes and run evidence;
- recorded assessed base equal to latest `main` before loading provider credentials.

The semantic review is a fresh, isolated OpenWiki process. It takes the generated docs from the PR head but restores the pre-generation upstream cursor from the commit parent, then independently assesses the same source window in a temporary worktree. It may not publish edits. Approval requires a successful complete run with no additional Markdown change and a matching no-change assessment. Any suggested change fails review and returns the PR to generation/recovery; it is never silently folded into the same reviewed commit.

The merge job then requires `shell-tests` and `openwiki-review` success for the exact head SHA, no pending/failing check, no review thread, and a final latest-main recheck. Only then does it mint a new short-lived App token and call the REST merge endpoint with the expected head SHA.

The repository's native auto-merge setting remains off. Required checks remain non-strict. If main has advanced at the final recheck, do not merge; supersede the PR and schedule replacement. If main races after the recheck but before REST merge, the merge may land, but status immediately reports stale and the resulting main push schedules repair. This recheck-and-repair behavior is deliberate for derived documentation.

## Failure and recovery

- **Interrupted/truncated/provider failure:** no complete marker or merge; keep the last successful marker on main; daily/manual/new-push recovery retries from current main.
- **Quota/auth/entitlement failure:** do not retry blindly. Report the category and next quota reset where available; wait for recovery or operator correction. Extra Usage remains disabled.
- **Transient provider 5xx/overload:** at most two bounded retries with backoff inside one run.
- **Superseded run:** never cancel it by concurrency ordering. Let it reach the final latest-main check, discard its stale output, and let the queued latest-state worker proceed. Never publish or merge the obsolete result.
- **Review disagreement:** leave a failed exact-head check and stop. One later recovery attempt may regenerate; a second disagreement requires operator inspection.
- **Stale-base race after recheck:** report stale and repair on the automatically triggered successor; do not treat it as credential compromise.
- **Credential or scope violation:** disable workflows/merge, close unsafe PRs, revoke the affected App/Kimi credential, preserve logs, and revert generated content only by ordinary reviewed PR.

## Operational acceptance and rollback

Before enabling App-issued merge, keep generated PR merges operator-owned and demonstrate:

- one localized source Change and one cross-cutting Change;
- one semantic no-change assessment that advances the receipt without repeating inference;
- a two-merge burst where stale in-progress work is discarded and the surviving queued worker processes latest main;
- one failed or cancelled generation followed by daily or manual recovery;
- refusal of wrong bot/head/base, outside-scope edits, `INSTRUCTIONS.md` mutation, obsolete heads, false attestation, and ordinary-Change auto-merge;
- no secret in logs, artifacts, or caches and no paid Extra Usage.

Subscription safeguards remain operational limits, not a spending experiment: Extra Usage stays disabled; each source commit gets at most one generation and one fresh semantic review; one automatic regeneration may follow review disagreement; each workflow stops after 60 minutes; quota exhaustion waits for reset instead of purchasing usage.

After automated merge is enabled, monitor these operating signals:

- land→PR normally within 30 minutes and land→merge within 90 minutes;
- zero repeated assessment of an already completed source window;
- touched pages remain precise and sampled material claims have no stale assertion or omission;
- status, supersession, no-change, failure, and recovery remain correct;
- operator intervention remains exceptional rather than routine.

Immediately disable automated merge on a false `current` result, scope escape, instructions mutation, ordinary-Change merge, secret exposure, silent missing planned write, or repeated semantic-review disagreement. Retain the last successful receipt on main, preserve evidence, and choose among prompt/provider repair, continued operator-merged documentation PRs, or retirement. Do not add page-level invalidation unless evidence specifically identifies impact selection as the failure.

## Delivery sequence

Each sequence item is a separate aligned Change and one PR:

1. **Inactive foundation:** pin/re-inspect upstream; implement the wrapper, receipt/status comparator, local capture tests, no-change cursor contract, deterministic validation, and documentation. Land no secrets or active workflow.
2. **Operator-merged rollout:** create and install the methodology App through operator input; add credentials; enable remote push/schedule/manual generation, but keep merge operator-owned while exercising the operational acceptance cases above.
3. **Automated operation:** after those cases pass and the enabling Change receives fresh-context review and sign-off, enable only the exact App merge job. Continue monitoring the named operating signals and rollback triggers.
4. **Revision or retirement:** change the mechanism or revoke its credentials only through an ordinary reviewed Change, except immediate credential revocation during an incident.

Every Change uses GitHub Flow, applicable fresh Checks, the code-review Skill, and user acceptance where behavior becomes externally visible.

## Role-model consequence

No librarian or custodian role is created. Normalize first:

- the generation model performs a constrained **implementer-role assignment** using the OpenWiki maintenance capability;
- the fresh semantic assessment supplies **reviewer-role evidence**;
- the `qq-openwiki` App is a workflow identity and constrained merger, not a methodology role;
- schedule, fixed branch, provider key, worktree, generated-file ownership, and recurrence are workflow/resources/triggers, not role invariants;
- operator accountability and source/Checks authority are unchanged.

A future role proposal must still demonstrate a residual Actor-level authority, accountability, independence, evidence, or lifecycle invariant after those procedural properties are normalized.
