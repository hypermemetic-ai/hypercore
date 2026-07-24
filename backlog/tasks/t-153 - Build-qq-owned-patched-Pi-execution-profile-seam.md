---
id: T-153
title: Build qq-owned patched Pi execution-profile seam
status: Done
assignee: []
created_date: '2026-07-24 07:07'
updated_date: '2026-07-24 23:50'
labels: []
dependencies: []
documentation:
  - doc-87
  - doc-88
  - doc-91
modified_files:
  - bin/qq-pi-runtime
  - tests/qq_pi_runtime_test.py
  - backlog/tasks/t-153 - Build-qq-owned-patched-Pi-execution-profile-seam.md
type: feature
ordinal: 69000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement the first half of the approved role-routing system without contacting Pi upstream: qq owns a minimal patch against a pinned, checksummed Pi release plus a reproducible build/install/verify path for the patched standalone binary. This Change adds only the generic request-local execution seam; the six-role qq policy remains a dependent Change.

Decision ledger:
- Full six-role routing semantics and upstream-gap evidence — T-152, doc-87, and doc-88.
- Reject upstream contribution; qq owns the Pi patch — decision-13, settled by the operator asked-and-answered exchange in the project-home accountable session on 2026-07-24 ("forget about [upstream]"; selected "qq-owned Pi patch").
- Pinned deterministic source-build patch stack, stock-Pi refusal, and separate seam/integration Changes — decision-13 and operator-approved plan doc-91.
- Installed provider implementations own generic Pi capability declarations; trusted built-in provider/model provenance for canonical routes belongs to the dependent qq policy Change — convergence-breaker disposition recorded in decision-13 and doc-91 after the operator directed continuation on 2026-07-24.
- Pi owns immutable enforcement through one central request transaction and an exact post-hook provider payload snapshot — operator-approved convergence-breaker disposition recorded in decision-13 and doc-91 on 2026-07-24.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A pinned Pi v0.81.1 source identity and digest are verified before patching; stale or mismatched source and patch preimages fail closed.
- [x] #2 The minimal Pi patch provides exact request-local model, effort/default, and typed service-class/default resolution; one central transaction keeps conflicts latched across callbacks and nested work; guarded adapters transport the exact validated post-hook snapshot; failures cause zero provider calls; a profile is pinned through a complete tool loop and refreshed only for the next logical request.
- [x] #3 Ordinary prompts, automatic/manual compaction, branch summaries, and other Pi-owned model calls use the same fail-fast profile boundary without persisting session/global defaults or falling back, clamping, omitting, probing, or continuing stale.
- [x] #4 Service class travels through provider options and payloads with requested/acknowledged telemetry and cost-accounting coverage.
- [x] #5 A reproducible qq build/install/verify engine builds the supported standalone binary from the checksummed source plus patch, installs atomically, exposes a verifiable patched identity, refuses stock Pi, and has a tested rollback path.
- [x] #6 No upstream issue/PR, committed Pi source/binary, qq role policy, general Pi provider-provenance framework, profile UI, access-policy change, or paid provider call is introduced.
- [x] #7 Applicable Pi and qq Checks, faux-provider conformance, fresh-context review, and operator-visible smoke acceptance pass before activation and handoff.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Capture the approved plan and durable decision, then implement and verify the pinned qq-owned Pi patch, deterministic builder/installer, and faux-provider conformance coverage before machine activation.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Post-merge activation on 2026-07-24 exposed one composition blocker before T-154.2 promotion could finish: `qq-dispatch` correctly made the installed runtime read-only under Landstrip, but every `qq-pi-runtime exec` identity check attempted to create `.identity-*` beneath that immutable data root and failed before the child Pi session existed. The narrow correction keeps artifact inspection scratch colocated but gives active verify/exec identity probes their ambient private TMPDIR; no binary authority, integrity check, provider behavior, or Landstrip grant changes. Unit/runtime/dispatch Checks pass, and real-provider canonical reviewer async `020dfc57-580e-4e81-87fe-55206c22122f` plus resumed `00bb68ed` completed through the installed pi-subagents pin, corrected worktree wrapper, qq-dispatch, and Landstrip.

Post-merge fresh review of PR #242 found that its ambient identity scratch unintentionally reached mutating install/rollback verification. The final correction makes every generation-verification caller choose scratch explicitly: only public active verify/exec use ambient delegated TMPDIR, while install and rollback retain locked data-root scratch. A regression reproduces the unusable-ambient-TMPDIR install failure before the correction and proves two installs plus rollback after it. Fresh correction review passed; all 34 Repository shell suites passed; the operator accepted the exact patched identity and real reviewer/observer launch behavior on 2026-07-24.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Delivered the qq-owned Pi v0.81.1 execution-profile seam, deterministic pinned runtime engine, immutable verified activation, stock-Pi refusal, exact provider/profile transaction enforcement, and service-class telemetry. Active identity is 0.81.1+qq.execution-profile.1. Real reviewer and observer children launch through qq-dispatch and read-only Landstrip. PR #239 observer analysis is finalized under the operator XDG observer store; the final install/rollback scratch correction preserves atomic mutation when ambient TMPDIR is unavailable.
<!-- SECTION:FINAL_SUMMARY:END -->
