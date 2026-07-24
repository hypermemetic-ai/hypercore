---
id: doc-91
title: Plan — qq-owned patched Pi execution-profile seam
type: specification
created_date: '2026-07-24 07:07'
---
# Plan — qq-owned patched Pi execution-profile seam

**Owning Task:** T-153
**Status:** Approved by the operator in the project-home accountable session on 2026-07-24.
**Change boundary:** Generic patched Pi seam plus reproducible build/install/verify path. qq role policy is a dependent Change.

## Intended outcome

Keep the approved six-role routing contract without contacting Pi upstream. qq owns a small source patch against one pinned Pi release, builds a patched standalone Pi binary reproducibly, and later adds the thin qq role resolver as a separate Change.

## Ownership and distribution

- Carry the patch, pinned upstream release identity, checksums, build/verify/install engine, and operating documentation in qq.
- Target Pi `v0.81.1`, tag commit `20be4b18d4c57487f8993d2762bace129f0cf7c6`, using its deterministic release source archive (`sha256:fb9bb7d7e8887e890824a08de588124350045da2cce763c5e6fd98d7141af31c`).
- Build the supported Linux x64 standalone binary from the checksummed source archive after applying the qq patch. Do not commit the upstream source tree, source archive, dependencies, or built binary.
- Install the verified binary in an operator-owned qq runtime location and make qq's Pi launch surfaces resolve only that binary. Refuse launch when patched identity or integrity verification fails; never fall back to stock Pi.
- Treat every Pi upgrade as an explicit qq Change: update the source pin, rebase the patch, rerun conformance, and activate only after review.
- Treat installed Pi provider implementations as the generic seam's capability authorities. The dependent qq policy Change, not this seam, verifies trusted built-in provider/model provenance for canonical routes and rejects project, extension, custom-model, or remote-catalog substitution.

## Implementation

1. Add a minimal patch stack against the pinned Pi source. The patch adds only a generic request-local execution-profile resolver and central request transaction: exact model, effort/default, typed service-class/default, fail-fast capability/auth validation, immutable conflict latching through normal and nested auxiliary work, exact post-hook payload snapshots, provider-option transport, and selected/acknowledged telemetry.
2. Add a qq build/install/verify engine that downloads the exact source archive, verifies its digest, applies the patch with checked preimages, invokes Pi's documented standalone build, verifies the resulting patched identity, and installs atomically. No lifecycle script or unpinned source is trusted.
3. Test source mismatch, patch mismatch, build identity, install refusal, atomic activation, and rollback against temporary fixtures.
4. Add or carry Pi faux-provider conformance tests proving the execution-profile contract. Make no paid provider calls.
5. Run applicable Pi checks from the patched tree and all qq Checks; obtain fresh-context review before commit/publication.
6. After merge, activate the patched binary through the agent-owned installation procedure. Verify root Pi, architect, compaction, branch summary, and delegated child launch paths resolve the patched binary. Walk the operator through a short smoke acceptance before final handoff.

## Required patched seam

The patch must:

- resolve before auth/network work;
- validate the complete profile exactly and propagate failure to the caller;
- freeze one profile in a central request transaction spanning authentication, callbacks, provider calls, nested auxiliary work, final callbacks, and completion;
- keep a compute conflict latched until failure, and refuse nested resolution/authentication when its parent has already conflicted;
- snapshot guarded provider payload-hook output once, validate that snapshot, and transport the exact snapshot while preserving unrelated hook behavior;
- resolve afresh for the next prompt without writing session/global defaults;
- cover ordinary prompts, manual/automatic compaction, branch summaries, and other Pi-owned model calls;
- translate typed service class through provider options and payloads;
- expose requested and provider-acknowledged values for accounting and existing displays;
- reject unsupported effort/service class, missing auth, conflicting mutation, fallback, clamping, omission, probing, and stale continuation.

## Dependent Change

After this Change is landed and the patched binary is active, a separate qq Change adds the single operator profile map, immutable occupancy resolution, trusted manifest-source role assertions, verified built-in provider/model source enforcement for canonical routes, pi-subagents compute/fallback lock, and existing footer/status telemetry. That policy rejects project, extension, custom-model, and remote-catalog substitutions. `qq-codex-fast` retires only after equivalent service-class accounting passes.

## Non-goals

No upstream issue or PR, full Pi fork or vendored source tree, committed source archive/dependencies/binary, qq roles or configuration inside patched Pi, general provider-registration trust framework, profile UI, access/tool/network-policy change, live provider probe, or compatibility fallback to unpatched Pi.

## Success evidence

- Source digest and patch preimage checks fail closed.
- A clean deterministic build produces a patched binary with verifiable identity.
- Faux-provider tests prove zero-call invalid profiles, exact effort/service class, tool-loop pinning, next-request hot changes, compaction, branch summaries, selected/acknowledged telemetry, and no fallback.
- qq launch surfaces refuse stock/unpatched Pi and all resolve the installed patched binary.
- Machine activation is atomic and rollback restores the preceding known-good Pi binary and launch target.
- Full qq Checks, applicable Pi Checks, fresh-context review, and operator-visible smoke acceptance pass before handoff.

## Decision ledger

- Full role-routing semantics and research disposition — T-152, doc-87, and doc-88.
- qq ownership of a pinned local Pi patch, stock-Pi refusal, and two-Change separation — decision-13, approved by the operator on 2026-07-24.
- Provider implementations own generic Pi capability declarations; the dependent qq policy layer owns trusted provider/model provenance for canonical routes — operator continuation after the review convergence breaker on 2026-07-24, recorded in decision-13.
- Pi owns immutable request enforcement through one transaction and exact transported payload snapshot — operator-approved convergence-breaker disposition on 2026-07-24, recorded in decision-13.
