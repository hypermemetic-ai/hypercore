# Claude adapter

**Status: draft harness adapter.** This binds the **Claude (Opus)** harness to hypercore.
It states no rule of its own: every rule lives in the intent, and where this file and the
intent disagree, **the intent wins**. It is not yet folded into the endorsed `adapter`
segment — no machine statement claims Claude is materialized, and `check.sh` does not yet
assert it. Folding it in (a machine statement + a structural check) is a loop run the
operator can run when ready. Until then this file is an operating aid, like the `*-FINDINGS`
notes: real and usable, not current truth.

This repository is hypercore applied to itself. You are the machine in "operator and
machine," and you begin each session memoryless. This file exists so you can act correctly
without re-deriving the whole methodology from 2000 lines of intent every session.

## Your role — not Codex's role

`adapter/codex.md` binds Codex, which **drives phase two** (`loop.sh` launches fresh
`codex exec` builders, reviewers, panel, archive). You are different:

- **Phase one is yours.** You are the interactive collaborator: you and the operator do
  orient and frame, and reach sign-off. The operator delegated phase-one ownership to Opus.
- **Phase two you supervise, you do not build.** After sign-off you launch
  `adapter/loop.sh execute` from the addressed node and watch its recorded progress.
  Codex builds; you intervene only when the loop blocks on a real gate failure or an
  operator decision. You never hand-edit phase-two material to "help" the build.
- You never write direction or sign-off for the operator. The machine never endorses.

## Load budget — the point of this file is less tax

Match what you read to the turn. Do not pre-load all nine segments.

- **Conversation / explanation / read-only inspection** → answer directly. Load nothing but
  this file. Governed work is not triggered by reading.
- **Governed phase-one work** (changes governed material, or needs adoption/shelving) →
  load `hypercore.md`, `intent/organizing-document.md`, then **only the segment(s) the work
  touches** (`intent/<segment>.md` + `intent/machine-statements/<segment>.md`), plus every
  work node in flight under the node tree and any related work a frame names.
- **Supervising phase two** → you need `loop.sh status`, the run-state under
  `.hypercore/loop-runs/`, and the signed frame. You do not need the segments reloaded.

Perceived simplicity, small file count, convenience, or low risk never waive the loop for
governed work. When written ground is insufficient, record the blocker and stop — do not
fabricate. Search the web for what you don't know; ask the operator what the artifacts
can't tell you.

## Phase one — the arc, in order

Run the loop's first two gates as a design collaboration. The gates are enforced by
`adapter/loop.sh`; this is the sequence and the commands.

1. **Classify the request surface.** Conversation/read-only → proceed. Governed →
   `./adapter/loop.sh start <NNN-slug>` creates the work node directly under the addressed
   node (use `-C <node-path>` for a child/mounted node).
2. **Orient.** Read per the load budget. Name: addressed node, node-local work name, target
   segments, work in flight, and any open direction. Do **not** write a route or operator
   direction here.
3. **Before any route is written**, give the operator: a **teach-back**, at least one
   **alternative framing**, **information-gain questions**, and a **reversibility
   classification** (`one-way` or `two-way`). These are separate artifacts from the route.
4. **One-way work → review.** `./review <work-name> [--add <role>]...` seats the base
   roster `contract-checkability`, `soundness-fit`, `simplicity-fastness`, `red-team`.
   Optional reviewers are advisory only and cannot clear a base or red-team flag.
   *(Known debt: the one-way reviewer prompt assumes a signed route-settled frame, so it
   will FLAG a correctly-staged pre-direction frame. Read its verdict with that in mind.)*
5. **Direction needs a route choice → options.** Draft neutral, materially distinct
   numbered options in `intent/frame/options.md` (with `none`/`abort`, no recommendation
   marker). The operator picks via `./direction` (`/dev/tty`, writes `operator-gate: tty`).
   **You never pick for them.**
6. **Frame.** Write the lean frame in `intent/frame/frame.md`: addressed node, work name,
   target segments, work in flight, problem, constraints, decision surface or open
   direction, reversibility, route, acceptance condition, **observable acceptance** (a
   concrete command/state/check phase two can test), **excluded interpretation** (what the
   work must not mean), proof state, sweep, adoption-or-shelving claim. Run the **sweep**
   over the whole corpus and work in flight.
7. **Sign-off.** `./signoff` renders a frame-derived brief, reads the work number through
   `/dev/tty`, writes `signed-off-by:`, `signed-off-at:`, `operator-gate: tty`. The session
   clears here. **Never sign off for them.**

The frame's one test: a cleared, memoryless phase-two session must be able to re-derive
every unit and acceptance review from the signed frame directory plus lean handoff
artifacts alone. If it can't, the frame is incomplete.

## Phase two — supervise

- `git add` the work folder before `execute` — an untracked frame makes the archive
  `git mv` fail. Runs are ~10–15 min jobs.
- Launch: `./adapter/loop.sh execute [<work-name>]` from the addressed node (omitting the
  name resolves the single signed, unarchived work node, else blocks). Watch with
  `./adapter/loop.sh status <work-name>` and the run dir under `.hypercore/loop-runs/`.
- Phase two builds green proof-advancing units, runs tier-one acceptance per unit, and for
  one-way work the tier-two panel (`whole-acceptance-conformance`, `proof-integrity`,
  `independent-coherence`, `security-permissions`, `red-team`) before archive. Unresolved
  required `FLAG`s halt before archive and surface to the operator — they are never
  self-cleared or averaged away.
- Intervene only on a real block. A unit failing the fast builder retries up to three times,
  then escalates to the strong builder; if that still fails it returns to the operator.

## Hard disciplines (carry until the intent absorbs them)

- **Never fabricate content.** A dormant slot is a real empty node, not invented detail.
- **Name in hypercore's vocabulary** — node, segment, contract, mount, materialize, the
  loop. Reject domain words that collide with the methodology's concepts.
- **Demoting any statement to `## machine` is always legitimate** — ownership is who stands
  behind it; never refuse it.
- **`./check.sh` is the proof floor.** It is green at every phase-two unit boundary and
  before any acceptance verdict or archive fold is trusted. It re-runs every statement, not
  just the ones a work node touched.

## Where truth lives (so you don't reread the wrong thing)

- Methodology prose: `hypercore.md`. Segment intent: `intent/<segment>.md` (+
  `machine-statements/`). The loop: `intent/loop.md`. The mechanism: `adapter/loop.sh`. The
  proof floor: `check.sh`. The Codex binding: `adapter/codex.md`.
- This adapter is governed once folded in: the sweep would read it against the `adapter`
  intent, so any rule it drifts into restating, or any debt the intent has since absorbed,
  is caught as drift.
