# Codex adapter

This is the **adapter** segment of hypercore's intent, materialized for the Codex
harness (`intent/adapter.md`). It states no rule of its own: every rule lives in
the intent, and where this file and the intent disagree, **the intent wins**. It routes
you to the intent and the loop, and makes them enforceable.

This repository is hypercore applied to itself. You are the machine in "operator and
machine," and you begin each session memoryless.

## What the adapter promises

Agreement between this harness and the methodology: that you act in accordance with the
intent and run the loop, not because you chose to, but because the workflow makes the
gates unskippable. Pointing alone is a request; the orchestrator is how agreement is
kept.

## Current Harness Binding

The current root binding is Codex. The root `AGENTS.md` entry point is symlinked to
`adapter/codex.md`; it is the harness-mandated pointer and not where the adapter lives.
Nested work under this root receives that entry point through the project instruction
chain, so nested nodes do not carry their own adapter material.

The current materialization binds Codex to both phase one and phase two. Phase one defaults
to the interactive Codex harness that loaded this adapter. Phase two is driven by
`adapter/loop.sh`, which invokes fresh `codex exec` sessions for builders, reviewers, and
the archive actor; the orchestrator records raw Codex JSON event streams and Codex thread
ids as current binding facts.

The handoff after sign-off is Opus supervising Codex, not Opus doing phase two itself:
Opus launches a fresh Codex orchestrator from the addressed node and has it run
`adapter/loop.sh execute [<work-name>]`; that orchestrator then launches the nested
`codex exec` builder, reviewer, panel, and archive sessions. Opus watches the loop's
recorded progress and intervenes only when the orchestrator blocks on a real gate failure
or operator need.

The current materialization also keeps the `CODEX_*` environment knob names in
`adapter/loop.sh`. Those names are implementation binding, while the intent states the
builder-model, strong-builder, review-model, and review-effort roles. Two-step has shipped;
the default builder is the cheap fast model behind the plan step and plan-match check,
materialized as `gpt-5.3-codex-spark`.

## Orient before you touch anything

First classify the request surface. Ordinary conversation, explanation, and read-only
inspection can proceed directly when they do not need adoption or shelving. Governed work
starts or continues a work node before material changes; perceived simplicity, small file
count, convenience, or low risk never waives the loop for governed work.

Read, in this order. This is where orient begins:

1. `hypercore.md` — the methodology.
2. `intent/organizing-document.md` — how the intent is divided into segments.
3. The segment the work touches (`intent/<segment>.md` and its
   `machine-statements/<segment>.md`), every work node in flight across the node tree,
   and any related work named by a frame.

Don't guess. Search the web for what you don't know. Ask the operator what the artifacts
can't tell you.

## The rigid workflow — `adapter/loop.sh`

Every work node runs the loop's five gates, driven by the orchestrator in two phases split at
the operator's **sign-off**:

- **Phase one — orient, frame — design-phase collaboration.** You and the operator choose
  direction before sign-off by naming the addressed node, node-local work name, target
  segments, work in flight, work classification, and any open direction. Before a route is
  written, you provide a teach-back, at least one alternative framing, information-gain
  questions, and a reversibility classification; route, review, direction, and neutral
  options stay separate artifacts. One-way work requires `./review <work-name> [--add <role>]...`,
  which mechanically seats the base roster `contract-checkability`, `soundness-fit`,
  `simplicity-fastness`, and `red-team`; optional complete-roster reviewers are advisory
  additions only and cannot clear unresolved base or red-team flags. When direction needs
  route selection, `intent/frame/options.md` carries neutral, materially distinct numbered
  options plus reject/abort choices; the machine may draft those options, but it does not
  choose one for the operator. The operator then records substantive direction with
  `./direction [<work-name> [<operator>]]`. The helper opens `/dev/tty`, renders the
  options, accepts a number, `n` for none-of-these, or `q` for abort, and writes
  `direction.md` with `direction-by:`, `direction-given-at:`, `operator-gate: tty`, and
  exactly one selected route, constraint, or delegation copied from the selected option.
  The explicit text form is compatibility/admin surface only and still must cross the
  operator gate to satisfy new-work validation. You never write direction or sign-off for
  the operator, and the route is not framed before direction exists. The written frame is
  lean recoverability: addressed node, node-local
  work name, target segments, work in flight, problem, constraints, decision surface or
  open direction, reversibility, route, acceptance condition, observable acceptance,
  excluded interpretation, proof state, sweep, and adoption or shelving claim. You frame
  the work node directly under the addressed node as
  `<NNN-slug>/`, with artifacts under `intent/frame/`, and run the sweep over the whole
  corpus and work in flight across the node tree, including related work named by a frame.
  Interaction surfaces here. It ends when the operator signs off: from the root,
  `./signoff` signs the single frame-complete, unsigned active work node when the operator
  identity is unambiguous. The sign-off helper renders a concise brief from `frame.md`
  covering route, acceptance condition, observable acceptance, excluded interpretation,
  reversibility, and target segments, then reads the work number from `/dev/tty` and
  writes `signoff.md` with `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty`.
  The explicit `loop.sh [-C <node-path>] signoff <work-name> <operator>` form uses the
  same terminal gate. `operator-gate: tty` means the legitimate helper path crossed the
  current harness's terminal-liveness check, which the default machine command path fails;
  it does not prove cryptographic non-repudiation, tamper-evidence, file integrity, or that
  an operator rather than a deliberately allocated terminal answered. **You never sign off for them.**
- **The session clears at sign-off.** Phase two runs through fresh, memoryless `codex
  exec` sessions. Each implementation unit starts from the signed frame directory, writes
  lean handoff state, and is followed by an independent read-only
  implementation-acceptance reviewer. If the frame directory doesn't tell a cleared
  session something it needs, the frame was incomplete. That is the test.
- **Phase two — implement, check, archive — heads-down.**
  `loop.sh [-C <node-path>] execute [<work-name>]` builds the delta in green
  proof-advancing units, records structured phase-two acceptance artifacts under the work
  frame, resumes by skipping units already carrying a clean plan-match and tier-one PASS for the signed
  frame, blocks unresolved required `FLAG`s, and runs the required one-way implementation-acceptance panel,
  starting the required one-way tier-two lenses concurrently before archive. The required
  one-way panel lenses are
  `whole-acceptance-conformance`, `proof-integrity`, `independent-coherence`,
  `security-permissions`, and `red-team`; two-way work pays tier one but skips this
  panel. Archive adopts or shelves the work according to the signed frame only after every
  required acceptance artifact is clean and real-source. Adoption folds the accepted delta
  into the addressed node's intent, stamps each touched segment's foot with the signer,
  and records adoption history; shelving records history without making proposed parent
  amendments current.

A work name is a node-local `NNN-slug`. The root node is assumed when no node is named.
`loop.sh -C home start 001-example` addresses work in the home child node, and
`loop.sh -C home/<name> start 001-example` addresses work through a
linked mounted node's mount path. Current work is addressed by the node path plus one
node-local work name, with the frame under that work node's `intent/frame/`.
`start` is the phase-one entry point that creates a new work node. `execute` is the
phase-two entry point for a signed work node; when `<work-name>` is omitted, it resolves
only the single signed, unarchived work node in the addressed node and blocks when there
are zero or more than one.

The gates and their order are the loop, already intent (`intent/loop.md`); the
orchestrator only operationalizes them and blocks a gate whose preconditions fail.

## Disciplines the intent does not yet state (debts)

Each line is a **debt**: carried here only until a later change folds it into the intent
as a checked statement, then dropped.

- **Never fabricate content.** An unmaterialized child node is a dormant slot — a real,
  empty node — not a fake app with invented sub-projects.
- **Name in hypercore's own vocabulary** — node, segment, contract, mount, materialize,
  the loop. Reject domain words that collide with the methodology's own concepts.
- **Pin the strong review floor.** The strong review floor is not yet mechanically pinned
  to a checked strong model; it can still ride an ambient harness default. A future loop
  pins it.
- **Re-prompt phase-one one-way review.** The current phase-one one-way review reviewer
  prompt assumes a signed, route-settled frame and therefore cannot PASS a correctly staged
  pre-direction frame. A future loop re-prompts it for a pre-direction decision surface.

---
This adapter is itself governed: the `adapter` segment is its intent, and the sweep reads
this file against that intent, so any rule it drifts into restating, or any debt the intent
has since absorbed, is caught as drift.
