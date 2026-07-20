---
id: doc-55
title: 'pi-sweep B — Change delivery (qq-pr-watch, qq-change)'
type: other
created_date: '2026-07-19 16:33'
updated_date: '2026-07-19 16:35'
tags:
  - research
---
# pi-sweep B — Change delivery: reconciled research report

**Owning task:** T-93 — Evaluate pi-ecosystem replacements for qq surfaces.
**Cluster:** B — Change delivery (`qq-pr-watch`, `qq-change`, deliver-change rails).
**Research date:** 2026-07-19. **Overall confidence:** HIGH for qq contracts and the absence of a faithful replacement; MEDIUM for third-party package ranking (nothing installed).
**Settles:** No package is a drop-in. Keep `qq-change` (land and retire). `qq-pr-watch` is shrinkable to a small session-scoped pi extension poller, but only after a tested replacement exists — otherwise keep. Shortlist `@robhowley/pi-merge-ready` as advisory readiness UX. Operator merge stays an invariant; no merge automation.
**Decision this informs:** any adoption/rewrite is its own later Change with its own alignment; this document is evidence, not authorization.

## Owning-agent verification (2026-07-19)

Both contract corrections verified against source:

- `bin/qq-pr-watch:53` queries only `--json state,url` — the watcher observes terminal PR state, not checks/reviews. Readiness is a separate deliver-change step.
- The deliver-change/qq-pr-watch divergence is real: `skills/deliver-change/SKILL.md:110` prescribes a 5-second poll, while `bin/qq-pr-watch:21` enforces `--interval <30-60>`. **Incidental drift finding** — the skill and the command have diverged; record for a future fix, independent of any adoption decision.

## Cross-cluster adjudications

- `@robhowley/pi-merge-ready` shortlist touches deliver-change step 7 only; no overlap with other clusters' verdicts.
- Worktree-cleanup packages screened here are distinct from the delegation-substrate worktree lifecycle in doc-56; neither changes the other's verdicts.

---

# Findings report — qq Change delivery

**Question:** What maintained Pi-native capability or published package best replaces qq’s PR terminal-disposition watcher and Change landing/retirement bookkeeping, and what additional PR/CI QoL is available?

**Overall confidence:** **HIGH** for qq’s actual contracts, the Pi/GitHub CLI baseline, and the absence of a faithful landing/retirement replacement; **MEDIUM** for third-party package ranking because packages were not installed and several are very young.

## What the research settles

No published Pi package is a drop-in replacement for the complete Change-delivery cluster.

| qq surface | Verdict | Best available basis | Residual qq responsibility |
|---|---|---|---|
| PR terminal-disposition watch | **Shrink; conditionally retire** | Official Pi extension API plus `gh pr view` polling | A small session-scoped poller remains necessary; no package has exact semantics |
| PR readiness diagnostics | **Shortlist** | `@robhowley/pi-merge-ready` | qq’s delivery policy, final authoritative checks, and terminal wake |
| `qq-change land` | **Keep** | Plain `gh` and `git` are only primitives, not a replacement | All checkout-selection, mergedness, cleanliness, inspect/dry-run, and ff-only rails |
| `qq-change retire` | **Keep as-is** | No ecosystem candidate | Entire Herdr/worktree/branch ownership protocol |
| Merge automation | **Reject** | — | Operator merge remains an intentional invariant |

The best maintained combination is therefore official Pi plus GitHub CLI for watching, optionally `@robhowley/pi-merge-ready` for readiness UX, while retaining `qq-change`.

## Contract corrections discovered

**[HIGH] The watcher does not watch checks or reviews.** `qq-pr-watch` asks GitHub only for `state,url`, accepts `OPEN`, `MERGED`, or `CLOSED`, and emits one completion result after leaving `OPEN`. Its structured envelope and exit statuses come from `qq-engine`. See [qq-pr-watch](/home/qqp/projects/qq/bin/qq-pr-watch:51) and [qq-engine](/home/qqp/projects/qq/bin/lib/qq-engine.sh:24).

Readiness is a separate `deliver-change` step using `statusCheckRollup`; the subsequent watcher again observes only terminal PR state. Moreover, the skill specifies five-second polling with “no owned machinery,” while `qq-pr-watch` permits only 30–60 seconds. This is evidence that the standalone command and current procedure have already diverged. See [deliver-change](/home/qqp/projects/qq/skills/deliver-change/SKILL.md:89).

**[HIGH] `land` does not retire a worktree or session.** It verifies a GitHub merge, proves the merge commit is in freshly fetched `origin/main`, validates the one primary `main` checkout, and fast-forwards it. Retirement is exclusively the separate `retire` verb. See [qq-change land](/home/qqp/projects/qq/bin/qq-change:130).

**[HIGH] `retire` is not generic abandoned-branch cleanup.** It requires the branch to be proven contained in `origin/main`. Unmerged closed/rejected Changes are preserved until their disposition is explicitly realigned. See [qq-change retire](/home/qqp/projects/qq/bin/qq-change:240).

## Candidate findings

### Official Pi 0.80.10 extension API plus GitHub CLI — **ADOPT as the watcher basis**

**Observed facts.** Pi extensions can start long-lived resources after session lifecycle events, run external commands, clean up at `session_shutdown`, and inject a custom message into the same session with `triggerTurn: true` and `deliverAs: "followUp"` or `"steer"`. Pi’s documentation explicitly describes external CI integrations and event-driven messages. It does not expose a built-in declarative scheduler, persistent PR watcher, or background-job registry. [Pi extensions documentation](https://pi.dev/docs/latest/extensions), [Pi SDK documentation](https://pi.dev/docs/latest/sdk), [Pi RPC documentation](https://pi.dev/docs/latest/rpc).

GitHub CLI provides the necessary observations but not the complete watch:

- `gh pr view --json` exposes `state`, `mergedAt`, `mergeCommit`, `reviewDecision`, `statusCheckRollup`, and related fields. [GitHub CLI `pr view`](https://cli.github.com/manual/gh_pr_view)
- `gh pr checks --watch` waits for checks, not subsequent merge or close disposition. [GitHub CLI `pr checks`](https://cli.github.com/manual/gh_pr_checks)
- `gh run watch` watches one workflow run, not a PR lifecycle. [GitHub CLI `run watch`](https://cli.github.com/manual/gh_run_watch)

**Assessment. [HIGH]** A session-scoped Pi extension can reproduce the exact useful semantics: poll one exact PR; clear its timer before delivery; emit one structured same-session message for either `MERGED` or `CLOSED`; and clean up on session shutdown. This removes the Bash engine and process-output adaptation.

It is not a zero-code native feature. The timer, exact-once state, error handling, and inspect/status command still have to live somewhere. Therefore:

- Retire `bin/qq-pr-watch` only after this Pi-native replacement has a fresh test demonstrating both terminal states and exactly one same-session wake.
- If zero owned code is the requirement, keep the existing small watcher. No maintained package currently meets that stricter requirement.

**Fidelity:** Full potential fidelity for terminal watching; no coverage of `qq-change land` or `retire`.

**Residual:** A small owned Pi poller plus all Change bookkeeping.

### `@robhowley/pi-merge-ready` — **SHORTLIST for readiness QoL; reject as terminal-watch replacement**

Version 0.12.0 was published July 17, 2026. It is MIT-licensed, actively developed in the `pi-userland` monorepo, and has a substantial package-specific test tree covering status, GitHub behavior, commands, watch mode, supervisor state, and child-session handling. [Pi catalog entry](https://pi.dev/packages/%40robhowley/pi-merge-ready), [source and tests](https://github.com/robhowley/pi-userland/tree/main/packages/pi-merge-ready).

It offers:

- Exact PR URL targeting and JSON readiness output.
- Consolidated checks, conflicts, draft state, requested changes, unresolved required conversations, and review state.
- A foreground watch/repair loop.
- A detached supervisor UI that can launch isolated headless Pi sessions for bounded repairs.
- Fail-closed handling of ambiguous GitHub status.

**Fidelity. [HIGH]**

- PR readiness: strong improvement over manually interpreting `statusCheckRollup`.
- Terminal disposition: recognizes merged/closed lifecycle, but does not document an exactly-once structured wake into the original accountable session after operator disposition.
- Landing and retirement: none.

Its detached supervisor and child sessions are not equivalent to waking the original accountable delivery session. Its normal watch is oriented toward making a PR merge-ready, not waiting after handoff for an operator to merge or close it.

**Residual:** The complete terminal wake contract and all `qq-change` behavior.

**Compatibility. [MEDIUM]** Its wildcard Pi peer range does not prove exact 0.80.10 compatibility. The APIs it appears to use exist locally, but that remains untested.

### `pi-session-context` — **HOLD**

This is the closest packaged watcher conceptually. Its `monitor_mr` tool targets a GitHub PR and polls for comments, required approvals, merged state, and closed state; `monitor_pipeline` watches GitHub Actions runs. [Pi catalog entry](https://pi.dev/packages/pi-session-context?page=37), [source repository](https://github.com/it-ony/pi-session-context).

**Observed fidelity. [MEDIUM]**

- Merged PRs can auto-prompt the session, but only with `auto_prompt_merged: true`.
- Closed PRs produce a notification but not an automatic prompt.
- It watches approval and comment activity in addition to terminal disposition.
- It does not promise qq’s single structured completion envelope.
- Private GitHub use relies on direct token configuration rather than the already-authenticated `gh` path.

Thus it cannot replace the requirement that both `MERGED` and `CLOSED` wake the accountable agent exactly once.

**Health and compatibility concerns. [LOW]** Version 1.2.0 was published July 8, 2026, and the repository is active but small. Its package manifest has no test script and declares the older `@mariozechner/pi-coding-agent` and `@sinclair/typebox` peer namespaces, whereas the local Pi installation is under `@earendil-works` and uses the newer TypeBox package. Runtime compatibility is unresolved.

**Residual:** Closed-state wake, exact-once/structured semantics, authenticated-`gh` integration, and all landing/retirement behavior.

### `@davecodes/pi-routines` — **REJECT for Change disposition**

`pi-routines` is a capable general scheduler with GitHub polling, persisted routine definitions, history, templates, and a Node test suite. Its declared Pi ≥0.75.3 and Node ≥22 requirements nominally fit the local runtime. [Pi catalog entry](https://pi.dev/packages/%40davecodes/pi-routines), [source repository](https://github.com/Davidcreador/pi-routines).

Source inspection shows several fidelity failures in its GitHub poller:

- The first successful poll seeds a cursor without firing.
- Closed-PR discovery is limited to the latest 30 results.
- Events are keyed by PR number, but routines cannot filter for one exact PR number.
- Branch filters apply to pushes, not PR closures.
- Queue-before-cursor persistence provides at-least-once rather than exact-once behavior.
- A cursor falling outside the retrieved window advances without replay.
- Each routine firing starts a normal LLM turn.

See its [GitHub poller source](https://github.com/Davidcreador/pi-routines/blob/main/src/github-poller.ts).

**Assessment. [HIGH]** This is useful generic automation but materially weaker and broader than `qq-pr-watch`. It can miss the desired closure, fire for unrelated PRs, or duplicate delivery after interruption.

The catalog reports 0.5.1 while the inspected repository/release metadata still showed 0.4.x in places, which adds provenance uncertainty.

### Worktree and branch packages — **REJECT as `qq-change` replacements**

The strongest generic candidates were:

- [`@pandi-coding-agent/worktree`](https://pi.dev/packages/%40pandi-coding-agent/worktree): confirmation, dirty/locked worktree checks, and optional force.
- [`@zenobius/pi-worktrees`](https://pi.dev/packages/%40zenobius/pi-worktrees): avoids the current/main worktree and confirms destructive operations.
- [`@lanquarden/pi-dev-worktrees`](https://pi.dev/packages/%40lanquarden/pi-dev-worktrees): worktree switching/removal via the separate `wtp` tool.
- [`@carter-mcalister/pi-worktrunk`](https://pi.dev/packages/%40carter-mcalister/pi-worktrunk): wrapper around external Worktrunk.
- [`pi-worktree`](https://pi.dev/packages/pi-worktree) and [`pi-worktrees`](https://pi.dev/packages/pi-worktrees): generic managed creation/removal.

**Assessment. [HIGH]** None knows qq’s ownership protocol:

- Exact Herdr work-session identity.
- Live-agent absence.
- Exactly one tab and the recorded placeholder pane.
- Operator focus outside the retiring session.
- Workspace-absent ownership proof and interrupted-retirement recovery.
- Exact registered checkout and symbolic branch identity.
- Fresh `origin/main` ancestry proof.
- Unforced removal only.
- `git branch -d` only, with partial-state reporting if deletion refuses.
- Inspect/dry-run and qq’s structured refusal envelope.

Some candidates expose `--force` or use `branch -D`, directly opposing qq’s contract. Packages that automatically clean worktrees created by their own delegation runs—such as `pi-crew`, `pi-subagents`, `pi-prompt-workflows`, and `pi-workflow-engine`—do not adopt or safely retire an existing Herdr-owned Change and fall under the brief’s delegation exclusion.

Plain `gh pr merge --delete-branch` is also unsuitable: it performs the merge rather than leaving that decision to the operator and cannot enforce linked-worktree or Herdr retirement rails. [GitHub CLI `pr merge`](https://cli.github.com/manual/gh_pr_merge).

## `qq-change` fidelity verdict

### `land` — **KEEP**

**[HIGH]** All underlying operations are ordinary `gh` and `git`, but the value lies in their composition:

1. Resolve exactly one registered primary `main` checkout.
2. Confirm symbolic `HEAD`.
3. Require GitHub `MERGED` plus a merge OID.
4. Freshly fetch `origin/main`.
5. Prove GitHub’s merge OID is reachable from it.
6. Permit only `backlog/tasks/*` as untracked contamination.
7. Offer inspect/dry-run.
8. Fast-forward only.
9. Re-prove the merge OID is now in `HEAD`.

Inlining these into prose would shrink file count while weakening reproducibility and refusal behavior. No package supplies a safer user-facing abstraction.

### `retire` — **KEEP AS-IS**

**[HIGH]** The retirement command is repository- and Herdr-policy enforcement, not a generic worktree convenience. Its idempotence and interrupted-state handling are precisely the parts absent from package managers. Removing it would transfer a large destructive protocol into conversational instructions.

Splitting `land` and `retire` into separate files could improve ownership boundaries, but package adoption does not justify deleting either semantic contract.

## Catalog screen

The live Pi catalog was searched across GitHub, PR, CI, merge, branch, worktree, delivery, workflow, background, and watch terms. Beyond the serious candidates above:

- PR inspection/UI only: [`@gwynnnplaine/pi-github`](https://pi.dev/packages/%40gwynnnplaine/pi-github), archived [`pi-github`](https://pi.dev/packages/pi-github), [`@ryan_nookpi/pi-extension-open-pr`](https://pi.dev/packages/%40ryan_nookpi/pi-extension-open-pr), [`@yusukeshib/pi-pr-link`](https://pi.dev/packages/%40yusukeshib/pi-pr-link), and [`@arvoretech/pi-git-review`](https://pi.dev/packages/%40arvoretech/pi-git-review). None supplies lifecycle wake or retirement.
- Broader PR babysitting/review: [`pi-diffwarden`](https://pi.dev/packages/pi-diffwarden) and [`pi-pr-review`](https://pi.dev/packages/pi-pr-review). These address review/fix loops, not disposition bookkeeping.
- Delivery/autonomy frameworks: [`@kimuson/pi-ralph`](https://pi.dev/packages/%40kimuson/pi-ralph), [`pi-stack-ops`](https://pi.dev/packages/pi-stack-ops), [`patchmill`](https://pi.dev/packages/patchmill), [`pi-gauntlet`](https://pi.dev/packages/pi-gauntlet), and [`pi-autopilot`](https://pi.dev/packages/pi-autopilot). Their broader autonomy or merge assumptions conflict with qq’s operator-owned GitHub Flow.
- Git conveniences: [`@aprimediet/git-workflow`](https://pi.dev/packages/%40aprimediet/git-workflow) and [`@senad-d/branchme`](https://pi.dev/packages/%40senad-d/branchme). They help create branches, commits, pushes, or PRs but do not cover terminal disposition or safe retirement.
- Generic background execution: [`@zackify/pi-bg-tasks`](https://pi.dev/packages/%40zackify/pi-bg-tasks) and [`pi-unified-exec`](https://pi.dev/packages/pi-unified-exec). They manage processes but do not provide a durable exact-PR event contract.

## QoL additions

### Merge-readiness diagnostics — **SHORTLIST**

`@robhowley/pi-merge-ready` is the strongest current addition. It replaces no destructive qq machinery but offers a materially better view of why a PR is not ready and a bounded repair loop. A cautious adoption would use it as an advisory check in `deliver-change` step 7 while retaining the authoritative `gh pr view` fields and operator merge rule.

### Ambient PR/CI footer — **HOLD or use the lighter fallback**

[`pi-fancy-footer`](https://pi.dev/packages/pi-fancy-footer) is the best maintained ambient UI: PR number, Actions state, unresolved review threads, and early workflow-failure visibility. It has tests, MIT licensing, and an active July 15 release. However, its current package requires Node ≥24, while this environment is Node 22.22.3, so it is not currently compatible. [Source repository](https://github.com/mavam/pi-fancy-footer).

[`pi-pr-status`](https://pi.dev/packages/pi-pr-status?page=40) offers a lighter footer with PR link, pass/fail/pending checks, unresolved comments, and 30-second polling. It is MIT-licensed and advertises tests, but version 0.3.0 has not been updated since February 16 and declares no precise Pi 0.80.10 compatibility. [Source repository](https://github.com/bruno-garcia/pi-pr-status). **HOLD** pending a temporary-run compatibility probe.

Neither footer wakes an idle accountable session.

### GitHub-native parallel review — **OPTIONAL SHORTLIST**

[`pi-pr-review`](https://pi.dev/packages/pi-pr-review) provides parallel focused review passes, validated findings, machine-readable output, and optional GitHub comment/approval publication. Version 1.11.0 declares Pi ≥0.80.5 and Node ≥20 and has an explicit test suite. [Source repository](https://github.com/10ego/pi-pr-review).

It overlaps qq’s existing fresh-context `code-review` procedure rather than replacing nothing: qq supplies Change intent, threat-model orientation, read-only isolation, and owner verification, while this package adds multi-pass and GitHub publication UX. It merits a separate pilot only if those GitHub-side capabilities are desired.

### Pipeline/comment/approval notifications — **HOLD**

`pi-session-context` offers useful event-driven CI, review-comment, and approval notifications absent from qq. Its compatibility and exact delivery semantics should be resolved before adoption; it should not be introduced merely to replace the terminal watcher.

No merge-automation package is recommended. Automatic merge would conflict with qq’s explicit operator decision boundary.

## Implications for `deliver-change`

If the recommended direction is adopted:

- Step 7 may use `merge_ready_status` as an advisory diagnostic, but should retain the explicit GitHub fields and final source-of-truth inspection.
- Step 9 should name a precise session-scoped Pi watcher contract: exact PR, both `MERGED` and `CLOSED`, exactly one structured follow-up, error visibility, and shutdown cleanup. Until such a watcher is proven, retain `qq-pr-watch`.
- Steps 10–11—the merge-OID ancestry proof, primary-main synchronization, and explicit retirement rails—should remain unchanged.
- Do not replace retirement with package worktree cleanup or `gh pr merge --delete-branch`.

## Sources

Sources that materially shaped the conclusions:

- qq source contracts: [qq-pr-watch](/home/qqp/projects/qq/bin/qq-pr-watch:1), [qq-change](/home/qqp/projects/qq/bin/qq-change:1), [deliver-change](/home/qqp/projects/qq/skills/deliver-change/SKILL.md:1), and [code-review](/home/qqp/projects/qq/skills/code-review/SKILL.md:1).
- Official Pi documentation: [extensions](https://pi.dev/docs/latest/extensions), [SDK](https://pi.dev/docs/latest/sdk), [RPC](https://pi.dev/docs/latest/rpc), and [packages](https://pi.dev/docs/latest/packages).
- Official GitHub CLI manuals: [`pr view`](https://cli.github.com/manual/gh_pr_view), [`pr checks`](https://cli.github.com/manual/gh_pr_checks), [`run watch`](https://cli.github.com/manual/gh_run_watch), and [`pr merge`](https://cli.github.com/manual/gh_pr_merge).
- Package catalog and source repositories linked in the findings above.
- Context7 was used to cross-check Pi messaging/lifecycle APIs and GitHub CLI watch behavior; owner documentation is cited above.

## Gaps

- No package was installed or executed, as required by the brief. Exact Pi 0.80.10 runtime behavior remains unproven for all third-party packages.
- npm package pages returned HTTP 403. Version, license, dependency, and install metadata therefore came from Pi’s npm-backed catalog and repository package manifests.
- `pi-session-context` source retrieval was incomplete, and its manifest lacks a test script. Its old package namespaces are a material unresolved compatibility risk.
- Catalog, raw source, and GitHub cache occasionally disagreed on very recent versions—most notably `pi-routines` and cached `pi-merge-ready` views. Current catalog releases were used, but this reduces package-ranking confidence.
- No private-repository or branch-protection fixture was exercised, so GraphQL permissions and required-review behavior remain unverified.
- Pi’s lack of a built-in scheduler is an evidence-of-absence conclusion from the complete 0.80.10 extension, SDK, RPC, session, settings, and skill documentation. A hidden or undocumented facility cannot be ruled out.
