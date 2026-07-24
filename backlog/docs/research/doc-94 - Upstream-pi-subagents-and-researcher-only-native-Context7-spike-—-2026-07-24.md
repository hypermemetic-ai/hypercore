---
id: doc-94
title: Upstream pi-subagents and researcher-only native Context7 spike — 2026-07-24
type: other
created_date: '2026-07-24 18:47'
updated_date: '2026-07-24 18:49'
tags:
  - research
  - pi-subagents
  - context7
  - spike
---
# T-154.3 decision report — upstream pi-subagents and researcher-only Context7

**Owning Task:** T-154.3
**Overall confidence:** HIGH for provenance, recovery-patch necessity, native package-test results, and child-only Context7 tool scoping; MEDIUM-HIGH for the retain/adapt recommendation because real-provider and exact qq production composition remain untested.

## Executive recommendation

**Pause T-154.2 before implementation; do not close or silently reverse it.** The evidence now favors **retaining and adapting/forking pi-subagents as the vendor runtime**, with qq remaining the policy, confinement, observation, and delivery layer. Do not adopt upstream unchanged: qq still needs its terminal `structured_output` recovery patch, trusted canonical-role/model authority, exact immutable pinning, and qq composition checks. Keep production at `b7c531c238469e43866a1fe6697cb44279158c1c` as the rollback baseline. An operator disposition must supersede `decision-12` and reframe T-154/T-154.2 before this recommendation changes production.

**Adopt Context7 only as two pinned native tools for researcher children:** `resolve-library-id` and `query-docs`, loaded through `subagentOnlyExtensions` from an integrity-verified `@upstash/context7-pi@0.1.1` artifact. Do not register the package globally, run MCP, add a key, or expose it to parent/reviewer. `/c7-docs` and the vendor skill are not required for the intended research method: `skills/research/SKILL.md` already makes Context7-first behavior qq policy. This can work on both the current production fork and the candidate; it need not wait for a runtime upgrade.

## Observed findings

### Provenance and recovery semantics — HIGH

The clean clone-time upstream `main` was `https://github.com/nicobailon/pi-subagents.git` at `7bf165240e48cd010263034dcfbeda41bc718fa5`, package version `0.35.1`. Production fork commit `b7c531c...` has sole parent `f1540b09283a1c176a0c721878453c6382ecd399`. Cherry-picking its uncommitted delta onto `7bf165...` applied cleanly to five paths (134 insertions/9 deletions); applied and production stable patch IDs both equal `d184212591f03d2f8cc87b0fe8baacb2a1af2f70` (`.pi/t1543-evidence/checks/provenance-git.log`, `recovery-apply.log`, `recovery-delta-identity.log`).

Upstream still lacks qq's recovery semantic. With only qq's regression tests added, unpatched `7bf165...` passed 265/268 and failed exactly foreground, background, and detector cases where an earlier recovered tool error preceded successful terminal structured output. The patched candidate passed 268/268. Source changes `detectSubagentError` so a non-error `structured_output` tool result is a recovery watermark; focused negatives still reject failed structured output and later errors, while foreground parent validation covers absent/schema-invalid capture (`unpatched-recovery-probe.log`, `patched-recovery-probe.log`, `recovery-case-names.log`, candidate `src/shared/utils.ts` and the four named integration tests). This proves the semantic is still needed; it does not license trusting child prose.

### Candidate health — HIGH

Native verification controls the earlier confined result. The accountable owner copied the exact staged candidate to `/var/tmp/t1543-native.czv6BF/repo`, outside every ancestor `.pi`, with isolated HOME/XDG/TMPDIR and qq/subagent overrides unset (`native-full-suite-environment.log`). Two advertised `npm run test:all` attempts each produced unit **1391 pass, 0 fail, 1 skip**, then integration **643/644** and stopped before E2E at the same case: `preserves completed chain results and marks the timed-out current step`, expected two result entries but observed one (`native-full-suite.log`, `native-full-suite-rerun.log`, candidate `test/integration/chain-execution.test.ts`). The case passed 5/5 alone, and the entire integration suite passed 644/644 with `--test-concurrency=1`; native E2E passed 2/2 (`native-chain-timeout-reruns.log`, `native-integration-serial.log`, `native-e2e.log`).

Therefore the package's advertised suite is **not green**. The repeated default-concurrency result is a real suite-reliability defect/flaky test under load, not evidence that serial chain-timeout semantics are broken. The watchdog accepted-warning failure seen only in the confined run did not recur in either native default run or native serial integration and is **not an established candidate regression**.

### Capability evidence and proof tiers — HIGH for package behavior, MEDIUM for production behavior

Executed focused integration was 211/211; focused capability unit coverage was 413 pass/0 fail/1 platform skip; native serial integration was 644/644 (`focused-contract-integration.log`, `capability-unit-probes.log`, `native-integration-serial.log`). Exact case names are in `capability-case-names.log` and `contract-case-names.log`.

- **FleetView/status:** package unit tests exercised active/completed/current-session scoping, nested status/transcripts, stale repair, and viewport behavior. Source `src/runs/background/fleet-view.ts` reads bounded/contained artifacts and session tails. No human TUI E2E was performed.
- **Parallel and dynamic fan-out:** integration tests exercised top-level/static parallel execution, concurrency, per-task schemas/outputs, aggregation/failures, and structured `expand` into collected dynamic children.
- **Chains:** integration covered 2-, 3-, and 40-step sequential runs plus sequential→parallel→sequential and dynamic expansion. The sole native default-concurrency flake is the 300 ms timeout assertion described above.
- **Git worktree fan-out:** real-Git unit tests covered creation, setup hooks, synthetic-path refusal, diff capture, and cleanup; integration rejected conflicting child cwd. No real model concurrently wrote those worktrees (`src/runs/shared/worktree.ts`).
- **Async completion/wait/stop:** package process/integration tests covered detached lifecycle, exact-session wait, stop/interrupt/timeout, stale reconciliation, completion batching, and parent notification. They did not cover Herdr notification (`src/runs/background/{control-channel,notify,run-status}.ts`).
- **Steer:** file control-channel tests proved queued delivery, capability/ack records, pause/revive recovery, and budget preservation. This proves transport acknowledgement, not real-model compliance.
- **Resume:** tests and source validate persisted recovery descriptors, source run/agent/session, stopped/cross-session refusal, and restoration of the original agent contract. Exact qq role/schema/deadline composition remains unprobed (`src/runs/background/async-resume.ts`).
- **Append-step:** unit tests covered pending append persistence, reserved output names, graph extension, and terminal/non-chain refusal (`chain-append.ts`).
- **Artifacts/output isolation and progress:** integration/unit tests covered per-task paths, duplicate/path containment rejection, file-only references, transcript selection, live current-tool/activity, and terminal state (`src/shared/artifacts.ts`, status sources).
- **Schedules:** manager tests covered create/list/status/cancel, restart/missed handling, and sanitized async launch. It is config-gated/default-off; no wall-clock real-Pi/provider E2E occurred (`scheduled-runs.ts`).
- **Watchdog:** native package tests cover settings/default-off behavior, stale recovery, budgets, diagnostics, and warning flow. It is vendor-optional machinery and cannot replace fresh-context qq review or operator merge (`src/watchdog/runtime.ts`).

The package E2E is stronger than a pure unit test but still not provider proof: it launches actual Pi parent/child processes and the real extension/stdout path using Pi's **faux provider**, with networking disabled and no real API key (`test/e2e/real-session-subagent.test.ts`, `test/support/real-session-runner.ts`). No capability above has a real-provider candidate proof.

## T-154.2 acceptance and deletion/shrink/retain map

The current T-154.2 surface substantially duplicates proven vendor mechanisms:

1. **AC1 launch/fresh cwd/schema:** vendor already launches one agent with fresh context, cwd, strict tool selection, and `outputSchema`. **Retain in qq:** trusted canonical manifest-source occupancy and fail-closed role/model authority; candidate discovery still gives project agents precedence over extra user-source agents (`src/agents/agent-selection.ts`, `agents.ts`; T-152/doc-88).
2. **AC2 lifecycle descriptor/status/notification:** delete the planned qq implementation of detached lifecycle, status, wait/stop, completion batching, artifacts, and recovery descriptors. **Retain:** qq's immutable contract definition, exact pin/delta review, owner checks, and Herdr-facing stage/notification boundary. The recovery descriptor is version 1, but no explicit version marker was observed on the general `status.json` shape; pinning and adapter tests remain necessary.
3. **AC3 timeout/confinement/cleanup:** no deletion is supported. Retain `bin/qq-dispatch`, same-Repository/worktree validation, Landstrip policy identity, open-egress threat statement, staged credentials, scratch/session roots, hard timeout, termination forwarding, and descendant cleanup. Vendor worktrees are not confinement.
4. **AC4 completion/recovery:** use vendor schema capture plus qq's small recovery patch. Retain qq ownership of the Completion Envelope schema, `acceptance:none`, role instructions, invalid-output negatives, and owner verification.
5. **AC5 resume:** delete a new qq resume engine; adapt/test vendor resume. Retain qq's requirement that original role, cwd, session, schema, output, deadline, and context cannot drift.
6. **AC6 observation:** retain `bin/qq-observe` and persisted Pi JSONL as the sole content seam under decision-10. Shrink only pi-subagents-specific assembly after a live candidate proves the exact status/session mapping; progress/transcript UI must not become a live observation-content seam.
7. **AC7 migration:** replace “migrate to a qq runtime” with an exact-pin vendor qualification/rollout and shared black-box contract. Current `code-review` and `delegate-batch` remain thin callers.
8. **AC8 generic non-goals:** do not build qq chains, fan-out, schedules, watchdogs, generic discovery, or a TUI. Retaining a vendor that contains these features changes decision-12's narrow product boundary: qq must keep workflow authorization and defaults (especially schedules/watchdogs) distinct, and the operator must accept the larger vendor surface.

Concrete surface disposition:

- **Delete planned work:** custom qq launcher/tool, lifecycle store, status/wait/stop/resume engine, artifact manager, completion notifier, and any `qq-status` TUI (none exists).
- **Shrink T-154.2:** to candidate qualification, a thin policy/contract adapter, trusted role/model lock, observer integration, immutable fork/pin maintenance, canary/rollback, and contract tests.
- **Retain qq-owned:** `bin/qq-dispatch`; role policies/manifests and T-152 routing authority; exact Completion Envelope and workflow deadlines; `bin/qq-observe`; Herdr `$stage`/operator notification; Skills/work orders; GitHub Flow, fresh review, and operator merge.
- **Use vendor, do not duplicate:** FleetView, fan-out/expand/chains/worktree mechanics, lifecycle/status/wait/stop/steer/resume/append, artifacts/progress, schedules, and watchdog implementation.

This is **adapt/fork**, not adopt: upstream recovery is incomplete; canonical role/model authority is conflicting; default-concurrency suite reliability is defective; and exact qq composition is absent.

## Context7 researcher-only result

### Authority/integrity — HIGH; release-commit attribution — MEDIUM-HIGH

Official npm metadata for `@upstash/context7-pi@0.1.1` names Upstash's `https://github.com/upstash/context7.git`, `packages/pi`, and declares Pi extensions, skills, and prompts. The fetched tarball independently reproduced SHA-1 `b9842694a348f659bd0ee7ad7e6559f85f9bb962` and SRI `sha512-RVwu0alq02SoniWzn3oRbtRzQmM3g/UuVwKEGHGKj77B0twq6RHRyXuq1Gs/WF+hgtA2eI2QaSnSVq7lGjElbA==` (`context7-package-metadata.json`, `context7-integrity-verify.log`, packed `package.json`). npm published no `gitHead`; release commit `98baa58d3625e2529e000f1c9f658fff25081bbb` matches every packed file except semantically equivalent package.json ordering/final newline, so it is corroborated, not registry-attested (`context7-source-tree-match.log`, `context7-source-package-diff.log`).

Package source registers only `resolve-library-id` and `query-docs`; `lib/api.ts` calls `https://context7.com/api` directly with native `fetch`. `CONTEXT7_API_KEY` is optional and only adds Bearer auth. This is native Pi, not MCP (`extensions/context7.ts`, `lib/api.ts`, official clone `docs/clients/pi.mdx`). One no-key public Express query succeeded; only response metadata/digest/source URLs were retained (`context7-public-query-metadata.json`). Fetched Context7 content remains untrusted evidence.

### Child scoping — HIGH for the isolated real-Pi/faux-provider probe

Both patched upstream and the production fork produced the same matrix: researcher child tools included `resolve-library-id`, `query-docs`, and `read`; reviewer had no Context7 tools; accountable parent had no Context7 tools; API key was absent. No Pi package setting registered Context7: the harness passed the unpacked extension file only through researcher `subagentOnlyExtensions` (`context7-child-scope-probe.json`, `context7-production-fork-scope-probe.json`, `context7-probe-harness-excerpt.log`). The later executable-filtered process/credential scan found no running node/npm Context7 MCP process and no credential-like `ctx7sk_` value; the earlier process listing merely self-matched its scan shell (`owner-context7-process-credential-scan.log`, `owner-final-leak-process-scan.log`).

Package-level Pi resource discovery found `c7-docs` and `context7-docs`, but child-local extension loading found neither prompt nor skill. That is expected from the exercised mechanism: direct extension paths register tools; they do not register package prompt/skill assets. The two tools are sufficient for qq's delegated research method because `skills/research/SKILL.md` already instructs Context7-first use and the work-order brief carries that method. `/c7-docs` is a manual convenience, and duplicating vendor skill prose is unnecessary. qq should still own a minimal privacy rule: never send credentials, personal/private data, or proprietary code in Context7 queries.

A deployment recipe is not yet proven: the lab supplied peer dependencies through lab-only symlinks (`context7-peer-link.log`). A production canary must prove a stable, integrity-pinned artifact location and peer resolution without Pi package registration.

### Reviewers and stale MCP policy — HIGH for current Pi-subagents surfaces

Reviewers do not need Context7 by default. Their recurring authority is fresh-context examination of Change intent, source, tests, and failure paths; external library research can be explicitly delegated when material. Default Context7 would add latency, egress/query disclosure, and another tool without strengthening review independence. This also matches the T-154.3 operator disposition and the current reviewer manifest.

`decision-2` is stale **for the current Pi-subagents dispatch surfaces**: it settled older Codex MCP startup behavior, while current researcher/reviewer manifests contain no `mcp:`/`mcpDirectTools` selection and `qq-dispatch` uses isolated child configuration. Candidate source reads `.mcp.json` only when resolving explicitly selected direct MCP tools; the file alone does not grant current children Context7. Root `.mcp.json` still names `npx -y @upstash/context7-mcp@latest`, contradicting the intended pinned/native/no-MCP direction. Recommend superseding decision-2 for these surfaces and removing `.mcp.json` after auditing any non-Pi consumer; do not delete it silently.

## Smallest next experiment and promotion gates

**Next experiment (separately aligned; no automatic install):** after resolving the package-suite flake, run one production-shaped, nonregistered, read-only canary from an isolated Pi root. Explicitly load an immutable patched candidate path, route one canonical researcher through the real `bin/qq-dispatch`/Landstrip policy in a disposable same-Repository worktree, require the exact Completion Envelope and `acceptance:none`, load the integrity-pinned Context7 extension only through that researcher, perform one public resolve/query, then exercise contract-preserving resume. Inspect lifecycle/status/events/session artifacts and `qq-observe` assembly; prove parent tool absence, descendant cleanup, no MCP/key/process, unchanged production settings, and rollback to `b7c531c...`. This tests the missing production composition without first registering a package globally.

**Gates before any production pin promotion:** (1) fix or upstream the default-concurrency chain-timeout reliability defect and obtain repeated green advertised `test:all` runs; do not relabel serial green as full-suite green; (2) review the complete candidate/fork delta and publish one immutable hash only; (3) pass qq's exact foreground/background/invalid-output/recovery/resume contract against reviewer and implementer call shapes; (4) prove `qq-dispatch` policy identity, same-Repository refusal, forbidden-write boundaries, hard deadlines, signals, and descendant cleanup; (5) solve or explicitly sequence T-152's trusted canonical manifest-source occupancy and locked model/fallback authority; (6) prove live candidate session/status mapping and post-hoc observer harvest; (7) prove the nonregistered Context7 artifact/peer-resolution recipe and researcher-only scope in the actual qq composition; (8) fresh review, operator-approved rollback, and current production pin retained until all gates pass.

## Operator decisions required

1. Whether to supersede `decision-12`, pause the replacement destination, and rewrite T-154/T-154.2 as vendor qualification plus a thin qq adapter.
2. Whether qq accepts the larger vendor feature surface while keeping chains/fan-out/schedules/watchdog unauthorized by default; recommendation: yes, with exact pinning and policy ownership.
3. Whether to authorize a new immutable candidate fork/canary after the concurrency defect is fixed; recommendation: yes, no global install as the first experiment.
4. Whether to adopt pinned Context7 tools-only for researcher children and a qq-owned privacy/query rule; recommendation: yes, no key/MCP/global registration.
5. Whether to supersede decision-2 for Pi-subagents and remove `.mcp.json` after checking other clients; recommendation: yes. None of these dispositions is enacted by this report.

## Gaps and residual risks

- No real-provider candidate probe for any vendor capability, and no exact candidate run through canonical qq manifests, `qq-dispatch`, Completion Envelope deadlines, Herdr, or observer assembly.
- The advertised default-concurrency package suite remains red despite serial/isolated green.
- Trusted canonical role source/model fallback authority remains unresolved in candidate source.
- No human FleetView interaction, wall-clock schedule, real concurrent model writer, or real-model steer-compliance test.
- General vendor status format lacks an observed explicit version marker; upgrades require pin-bound contract tests.
- Context7 was unavailable as an active tool in this research. Findings use the official fetched package/repository/docs and recorded API probe, not a pretend Context7 lookup.
- Context7's stable nonregistered artifact/peer layout, public-rate reliability, and actual qq-dispatch composition remain unproven; npm did not attest a gitHead.

## Sources opened

qq: `CONCEPTS.md`, `openwiki/quickstart.md`, `README.md` bridge section, T-154/T-154.1/T-154.2/T-154.3, doc-93, decisions 2/8/10/12, T-152/doc-88, `.mcp.json`, `skills/{research,code-review,delegate-batch}/SKILL.md`, canonical manifests/policies, `bin/qq-dispatch`, `bin/qq-observe`, and `tests/test-delegate-runtime-bridge.sh`.

pi-subagents exact clone: `package.json`, agent discovery/selection, `pi-args.ts`, worktree/FleetView/control/resume/append/schedule/notify/status/artifact/watchdog sources, real-session E2E runner/tests, recovery sources/tests, and the executed logs under `.pi/t1543-evidence/checks/` cited above.

Context7 official fetched evidence: packed `@upstash/context7-pi@0.1.1` package source/assets, official repository `packages/pi`, `docs/clients/pi.mdx`, registry metadata/integrity/history logs, child-scope probes, and no-key query metadata.
