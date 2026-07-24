---
id: decision-13
title: qq owns the patched Pi execution-profile seam
date: '2026-07-24 07:07'
status: accepted
---
## Context

T-152 established the strict six-role routing contract and found that Pi 0.81.1's public extension APIs cannot provide exact, request-local, fail-closed profiles across ordinary tool loops and auxiliary model executions. The research recommended an upstream Pi seam followed by a thin qq integration.

The operator rejected upstream contact and selected a qq-owned Pi patch. A normal extension-only workaround remains unacceptable because it would knowingly retain persistence, clamping, fail-open extension errors, incomplete auxiliary coverage, and service-class accounting gaps.

## Decision

qq owns a minimal execution-profile patch against a pinned, checksummed Pi release. The patch and its reproducible build/install/verify machinery live in qq; upstream source archives and built binaries do not.

The patched Pi core owns only generic request-local execution mechanics. qq role names, occupancy, configuration, pi-subagents policy, and display integration remain outside Pi and land in a dependent Change.

The generic Pi seam treats installed provider implementations as the authorities for their declared model capabilities; it does not establish provider-registration provenance against other loaded Pi extensions. The dependent qq policy Change owns that trust boundary for canonical routes: it must accept only verified built-in provider/model source metadata and refuse project, extension, custom-model, or remote-catalog substitution.

Pi owns immutable request enforcement as one central transaction rather than scattered lifecycle checks. After profile resolution, the transaction spans authentication, extension callbacks, provider work, nested auxiliary work, final callbacks, and completion. A compute conflict remains latched until the request fails; nested work checks its parent before resolution or authentication. Guarded provider adapters snapshot payload-hook output once, validate the snapshot, and transport that exact snapshot. Unrelated hook behavior remains available.

qq launch surfaces refuse stock or unverifiable Pi rather than falling back. Each Pi upgrade is an explicit qq Change that updates the source pin, rebases the patch, reruns conformance, and activates only after review.

The work is separated into:

1. a patched Pi seam plus deterministic build/install/verify Change; and
2. a subsequent six-role qq policy/integration Change after the patched binary is active.

## Consequences

- qq accepts ongoing maintenance of the Pi patch across upgrades.
- Pi source, dependencies, archives, and binaries remain derived local artifacts, not Repository content.
- The installed Pi runtime becomes an explicitly pinned qq dependency rather than `@latest`.
- Upgrade or integrity drift fails closed until an approved patch rebase lands.
- No upstream issue or pull request is created.
- The approved routing contract remains unchanged; only ownership of the missing core seam changes.
- Canonical model/provider provenance is enforced by qq policy rather than by turning the generic Pi seam into a provider trust framework.
- The request transaction and exact transported payload snapshot are Pi responsibilities because only Pi owns the complete callback, nested-call, and provider-serialization lifecycle.
