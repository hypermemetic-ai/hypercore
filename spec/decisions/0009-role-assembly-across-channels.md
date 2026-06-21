# ADR 0009 — assembling the two roles across agents files, skills, and prompts

Status: **operator-ratified** (2026-06-21). The full-scan amendment made at first ratification was
**corrected the same day** after the operator re-raised the whole-picture concern: the worker holds
the **whole spec, preloaded, by construction** (the keystone — restored, not moved to just-in-time).
The agents file is a **single minimal shared anchor** (one `AGENTS.md`, symlinked as `CLAUDE.md`),
non-inferable content only. Residual machine-owned specifics — the exact per-harness skill format,
and the harness-seam build — remain [machine] and land with the build.

> **Superseded in part by ADR 0010 (2026-06-21).** The depth disciplines' single source moved out
> of `research/`: the synthesis is now `spec/depth.md` (a standing methodology doc, not work
> product), and the bootstrap `rebuild-spec` this ADR referenced is retired, its content absorbed
> into `intent.md`, the living spec, and the ADRs. The single-sourcing channel decided below is
> unchanged — only the source's location moved (`research/aposd.md` → `spec/depth.md`).

## Context

Item 2 was investigated (`research/context-files.md`), designed (`research/assembly.md`), and
validated a second time against live sources (assembly.md §8). That second pass confirmed the field
grounding and moved two facts; a third turn corrected an over-application of one of them.

- The ETH Zurich study (`§4.5`'s [arXiv 2602.11988], *Evaluating AGENTS.md*) is real and its numbers
  hold (LLM-generated files −3% success / +20% cost; human-written +4% / +19%, no gain for Claude
  Code). Its recommendation is sharper than "minimal/operational": *omit generated files; limit
  human-written ones to **non-inferable details**.* Files "do not function as effective repository
  overviews." Skills + progressive disclosure are an open cross-vendor standard; the AGENTS.md-vs-skill
  division of labor is field consensus.
- **Fact 1 (held).** Claude now reads `AGENTS.md` (when no `CLAUDE.md` is present), and the clean
  pattern is a single file with a `CLAUDE.md → AGENTS.md` symlink — so the `@AGENTS.md` adapter and
  two role-specialized files are unnecessary.
- **Fact 2, over-applied then corrected.** The field leans just-in-time over preloading — but that
  guidance targets *large/external* context (sprawling codebases, retrieved documents, million-token
  windows). It was first read as "move the worker's spec scan to just-in-time," which the operator's
  re-raised whole-picture concern exposed as a category error: hypercore's living spec is
  deliberately **small and wholly scannable** (a `self-model` requirement, "concise enough to scan
  across all of them at once"), and the field's *actual* recommendation is a hybrid — **preload the
  high-signal core, JIT the long tail.** The spec *is* the high-signal core. So the spec stays
  preloaded; just-in-time applies only to the reference tail (the ADRs).

Today both roles are grounded by one hand-assembled string each. The depth disciplines are
`worker.DEPTH` — a hand-compression of `spec/depth.md` frozen in a Python constant, a second copy
that drifts when aposd.md is sharpened. There is no agents file or skill anywhere.

## Decision

**Each role is assembled from one source across three derived channels, placed by two axes —
durability and reach.**

- **The governing cut is two axes, not one.** *Durability* (does the piece change every fold?) ×
  *reach* (does every episode need it, or only the episodes a task routes to?). Durable +
  every-episode + operational → the **agents file** (minimal); durable + routed → **skills**; live
  (re-derived each fold) + every-episode → the **prompt**. This is why the depth disciplines move to
  a skill (durable) while the live grounding stays prompt-side (it changes every fold).

- **The worker holds the whole spec, preloaded, by construction — the keystone.** Every episode the
  worker's context carries *every* capability's slice in full, with the **touched** slices
  foregrounded for *attention* — "touched" means where to focus, never all it is given. This is the
  non-slice-confinement of the worker (already built in slice 4 and tested by `slice4`):
  the worker's full rescan is the structural defense against the architect's delta mis-naming or
  missing a capability, and against worker **myopia** (building a module locally sensible but
  globally discordant). The first-ratification amendment that moved this to just-in-time is
  **withdrawn**: a conditional pull is gated on the worker *already suspecting* it must look — which a
  myopic worker will not — so it would convert a by-construction guarantee into a discipline, the one
  thing the worker design refuses. The spec is the high-signal core and small by design, so
  preloading it whole is cheap and field-aligned (preload high-signal + JIT the tail). The
  capability-index idea is dropped as premature: redundant when the whole spec is already present.

- **Just-in-time applies to the reference tail, not the spec.** The ADRs/decisions — fastest-growing,
  least relevant per node, no whole-picture stake — are the on-demand target: preloaded for now
  (pre-seam, no fence to pull from), pulled from the fenced checkout once the worker runs there.

- **Single-sourcing is a derived render, regenerated by the fold.** Skills and the agents file are
  generated from the source (the depth skill and the worker's depth grounding from `spec/depth.md`;
  any per-capability skill from `spec/<cap>/spec.md`), never hand-copied — the same "as-built is
  derived, never authored" discipline the operator view obeys. The fold gains a render step that
  regenerates them, so drift is structurally impossible. The one new mechanism: because an *external*
  harness auto-loads the file and skills as static artifacts (unlike the live-rendered operator view),
  they are **materialized** on disk by that step.

- **The filename is the role router; placement is a single shared anchor.** One minimal `AGENTS.md`
  at repo root, **symlinked as `CLAUDE.md`** (`ln -s AGENTS.md CLAUDE.md`) so the architect's harness
  reads the same file and the fenced worker's harness auto-loads it from the checkout. No adapter and
  no two role-specialized files — role specialization lives entirely in **skills** (field consensus),
  so the always-on anchor can be one shared file.

- **The agents file is a minimal shared anchor, non-inferable content only.** [chosen, operator,
  2026-06-21] A handful of non-inferable lines — the check command (`python3 -m hyper --check`), the
  build/hand-back convention, a pointer to the skills — exactly the study's endorsed "non-inferable
  details." No overview/identity prose, no per-capability requirements. Its worth remains measurable,
  but the lean is set: keep it minimal.

## Grounds

The cut falls where the system already cuts: single-sourcing is intent.md's "durable state in
version-controlled files" and the self-model's "as-built is derived, only the vision is authored,"
pointed at new channels, so the fold's derive-on-change guarantee carries it with no new discipline.
The whole-picture grounding is the load-bearing correction: it is a stated operator value (raised
twice), a tested keystone (slice 4), and the defense against both the architect's mis-scoping and worker
myopia — none of which a conditional just-in-time pull preserves, because its trigger *assumes the
absence of the myopia it must guard against*. Preloading the small, high-signal, scannable-by-design
spec honors that value and the field's hybrid at once; just-in-time is reserved for the reference tail
(ADRs), where it pays without a whole-picture cost. Placement is decided by verified facts (the
auto-load rule, the symlink), kept to one shared file because the evidence puts specialization in
skills, not prose; and the agents file is held minimal because even good files are marginal and
costly, so the weight sits on skills + the prompt-rendered whole-spec grounding.

## Consequences

The worker's spec grounding is **unchanged** — whole spec preloaded, touched foregrounded — so item 2
no longer perturbs the slice-4 keystone or its `slice4` checks; the just-in-time spec delta is
withdrawn and there is no capability-index render.

**Buildable now (no harness seam):** a `depth` skill and the worker's depth grounding both rendered
from `spec/depth.md`, retiring the frozen `worker.DEPTH`; the derived-render / materialize-on-fold
mechanism; the architect's methodology skills rendered from their spec slices; and the minimal shared
`AGENTS.md` + `CLAUDE.md` symlink (content the operator set).

**With the parked pi/OMP harness seam:** the transport runs the worker with `cwd` = the fence; the
**reference tail (ADRs/decisions)** is dropped from the prompt and pulled just-in-time from the
checkout (the spec capabilities stay preloaded); the depth + per-capability expertise move from the
prompt to OMP-loaded skills; the OMP flip (worker = GPT-5.5).

**Harness limit:** the acceptance harness asserts the scaffold — the frozen copy is gone and the
grounding renders from `aposd.md`; the channel artifacts exist, are single-sourced, and regenerate on
fold; the whole-spec grounding is unchanged; and (with the seam) the transport runs the worker with
`cwd` = the fence and pulls the reference tail. It cannot assert that a live model loaded a file or
skill — the §4 experiment, recorded not faked. This ADR records an assembly model and supersedes no
prior ADR; a future change that re-routes a channel (e.g. moving the spec scan off by-construction
preload, or dropping single-sourcing) carries an ADR superseding this one.
