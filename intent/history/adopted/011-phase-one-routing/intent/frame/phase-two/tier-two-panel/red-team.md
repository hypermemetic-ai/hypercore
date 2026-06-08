OpenAI Codex v0.137.0
--------
workdir: /home/qqp/projects/hypercore
model: gpt-5.5
provider: openai
approval: never
sandbox: read-only
reasoning effort: xhigh
reasoning summaries: none
session id: 019ea4ba-ad14-7472-b28c-89b34acdc21b
--------
user
You are the 'red-team' lens of the one-way implementation-acceptance panel for hypercore work node
011-phase-one-routing. The operator (qqp-dev) signed the frame; phase two built the delta;
./check.sh is green. Judge the BUILT RESULT against the SIGNED FRAME through your lens only.
Do not debate other lenses.

Read: the signed frame 011-phase-one-routing/intent/frame/frame.md (acceptance condition,
observable acceptance, excluded interpretation, route) and the built changes via
`git --no-pager diff` plus the current state of the changed contract files
(intent/collaboration.md, intent/loop.md, intent/adapter.md and their machine-statements,
hypercore.md, intent/organizing-document.md) and material (adapter/codex.md, adapter/loop.sh,
check.sh). Intent edits are in the worktree (uncommitted), to be folded at archive.

Return EXACTLY:
VERDICT: PASS
RATIONALE: <frame-anchored reason>
EVIDENCE: <concrete paths / command results / findings>
Use VERDICT: FLAG instead when evidence is missing, stale, uncertain, or mismatched with the
signed frame. Treat uncertainty as FLAG.

Lens focus: Try to break it. Find a false-negative hole in the product-absence grammar (a way to leave a real harness-product claim in a contract statement that the check passes). Was excluded-interpretation violated: a second phase-two executor, proof-floor demotion, materialization rename/removal, a new gate, or the collaborator producing phase-two artifacts? Did any loop behavior break?
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
I’ll inspect the signed frame, current diff, and the touched intent/material files, then judge only the red-team acceptance surface against the frame.
exec
/bin/bash -lc "sed -n '1,260p' 011-phase-one-routing/intent/frame/frame.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# frame - 011-phase-one-routing

## work

Addressed node: root (`.`).

Node-local work name: 011-phase-one-routing.

Target segments: `collaboration`, `loop`, `adapter` (intent and machine statements each).

Work in flight: this work node only. The root tree is otherwise clean; the `home` child
node has no active work folders. Three untracked sibling findings exist but are not work
nodes and address nothing here: `DECOMPOSITION-FINDINGS.md`, `WORK-NODE-COLLAPSE-FINDINGS.md`,
`TWO-STEP-BUILD-FINDINGS.md`. Two-step is conceptually adjacent (it splits judgeable intent
from implementation-completeness in phase two); the sweep treats it as parallel, not
colliding.

## problem

The methodology's contract names a single harness product — Codex — throughout the
`collaboration`, `loop`, and `adapter` intent, their machine statements, the adapter prose,
and `check.sh`. Two coupled defects follow.

1. The contract conflates *role* with *product*. A statement like "the Codex review roster"
   cannot separate the durable claim "an independent strong review floor exists" from the
   current setting "today that floor is filled by Codex." The `adapter` segment already holds
   the general truth that "an adapter is per harness; one node may be bound by more than one,"
   yet the surrounding contract contradicts it by hardcoding one product.

2. Phase one has no routing contract. Phase two already routes a *builder* role separately
   from the *review floor* (`loop.md`: "phase-two builders may be routed separately from
   reviewers... the fast-builder default is held at the strong model"). Phase one — the
   interactive design phase — names no roles and no config seam, so it cannot say that
   operator-facing judgment and corpus-facing throughput are different work that different
   harnesses may fill, nor that the strong review floor must stay independent of whoever
   framed the work.

The result: the contract cannot state "any capable harness may be the phase-one collaborator"
without contradicting the Codex-named statements around it, and cannot route phase-one labor
the way phase two already routes its builder.

## constraints

- Product-agnostic contract: no operator or machine *statement* in `collaboration`, `loop`,
  or `adapter` names a specific harness product — including config-knob identifiers that embed
  a product name. Statements describe config seams by role (a builder-model knob, a
  review-model knob, a collaborator-routing knob); a literal product-bearing identifier such
  as `CODEX_BUILDER_MODEL` is materialization, named only in `adapter/loop.sh` and `check.sh`,
  never in a contract statement.
- Three layers, not two. The de-naming sorts every product-named statement into: (a) a
  **methodology claim** (e.g. "an independent strong review floor exists") → role/config
  language; (b) a **capability requirement** — a statement that names a product today only
  because it encodes a behavioral assumption (entry-point loading, instruction-chain
  inheritance, structured exec-event streaming, cleared session-state preflight) → rephrased as
  "the harness must support X", product-agnostic but not overgeneralized to "any harness can";
  or (c) a **current-binding fact** → materialization, which stays product-named.
- Materialization stays product-specific: the adapter prose (`adapter/codex.md`), the harness
  entry point (`AGENTS.md`), the orchestrator's actual harness calls in `adapter/loop.sh`,
  config-knob *values*, and a designated current-binding section legitimately name the current
  binding. De-name the claims, not the mechanism.
- Preserve the proof floor: routing never demotes the review floor or acceptance tiers below
  current behavior, and the phase-one collaborator that frames a one-way work node must not be
  the review floor that scrutinizes it — the framer is not its own witness. (Today the review
  floor rides an ambient harness default rather than a checked, pinned strong model; whether
  011 pins a checked strong-review default or records the unpinned floor as debt is a route
  decision named below.)
- Preserve the five gates and the sign-off split: phase one interactive, phase two
  re-derives from the signed frame alone. No new gates.
- Preserve fastness: two-way work keeps skipping review and the panel.
- Hold defaults, strand nothing: every newly named role or config slot carries a held default
  that reproduces current behavior, mirroring how builder routing landed.
- Do not rewrite adopted history. Change only current corpus.
- Keep `./check.sh` green throughout, and make it prove both the product-name absence in the
  contract and the presence of the new role/config seams and held defaults.

## decision surface or open direction

Framing and scope are settled through operator deliberation, to be anchored by `./direction`:
a product-agnostic role/config contract that de-names the whole adapter contract. Statements
always describe config seams by role; the one genuine remaining fork is whether the *material*
config-knob identifiers (`CODEX_*` in `adapter/loop.sh`) are also neutralized. See
`intent/frame/options.md`. If the full scope cannot land coherently in one node, the work
shelves and re-frames smaller rather than weakening this acceptance condition.

Two route deliverables are load-bearing and must be made exact when the route is written: the
materialization-pointer grammar (so the product-absence check has no false positives on
legitimate pointers and no loophole), and the review-floor decision (pin a checked
strong-review default, or preserve current behavior and record the unpinned floor as debt).

Reversibility: one-way

## route

Adopt Option 1 (`contract-only-denaming`; `direction-by: qqp-dev`, `operator-gate: tty`):
de-name the whole harness-binding contract to role and capability terms, keep the
materialization product-specific including the `CODEX_*` knob identifiers, and add the
product-agnostic phase-one collaborator and review-floor roles.

### the three-layer sort

Every product-named line in a contract statement file is sorted into one of:

- **methodology claim** → rewritten in role/config language ("the Codex review roster" → "the
  review roster");
- **capability requirement** → rewritten as "the harness must support X", product-agnostic but
  not overgeneralized to "any harness" ("the Codex harness loads its adapter through a root
  `AGENTS.md`" → "the harness loads its adapter from a root entry point it reads at session
  start", with the concrete entry point named only in materialization);
- **current-binding fact** → moved into the materialization (`adapter/codex.md` prose,
  `adapter/loop.sh`, `check.sh`) and out of the statement files, leaving statements that point
  at the materialization by path only.

### the materialization-pointer grammar (this defines the check)

In a contract statement file, a harness-product token may appear ONLY inside a backtick-fenced
span whose content is a whitelisted materialization pointer: the binding paths `adapter/codex.md`,
`AGENTS.md`, `adapter/codex-mounted.md`, and the orchestrator path `adapter/loop.sh`. The scanned
product-token set (case-insensitive) is `codex`, `claude`, `opus`, `gpt-<n>`, and the knob
prefix `CODEX_`. A token outside a whitelisted fenced pointer fails. Knob identifiers
(`CODEX_BUILDER_MODEL`, `CODEX_STRONG_BUILDER_MODEL`, `CODEX_REVIEW_MODEL`, `CODEX_REVIEW_EFFORT`)
live only in `adapter/loop.sh` and `check.sh`; statements name them by role (the builder-model
knob, the strong-builder knob, the review-model knob, the review-effort knob). Out of scope, not
scanned: adopted/shelved history, scratch findings, child-node names (`codex-cockpit`), and the
mounted entry point itself; for `hypercore.md` and `intent/organizing-document.md` only the
adapter description is scanned, so the `home`/governed-work text naming `codex-cockpit` is
untouched.

### phase-one roles and routing seam (product-agnostic statements)

- `collaboration`: phase one decomposes into operator-facing judgment, owned by the
  **collaborator**, and corpus-facing throughput (research, the orient corpus read, the sweep
  map), which the collaborator may delegate; the collaborator is the harness that drives orient
  and frame.
- `collaboration`/`loop`: the **strong review floor** that scrutinizes a one-way frame is
  independent of the collaborator that framed it — the framer is not its own witness —
  generalizing the existing "the builder is not the witness of its own archive".
- `loop` (sibling to the existing phase-two builder-routing statement): phase-one labor is
  routable — the collaborator harness may differ from the phase-two executor harness, and
  breadth work may be delegated — while the review floor and acceptance tiers stay on the strong
  route.
- `adapter`: an adapter binds a harness to a phase; phase one and phase two may bind different
  harnesses (the standing "an adapter is per harness" already permits this); the current
  materialization binds one harness to both phases.
- Held defaults: the existing review-model and builder-model knobs are described by role with
  their current held defaults preserved (review/acceptance on the strong route; builder held at
  the strong model until two-step lands). The collaborator role defaults to the interactive
  harness that loads the adapter. No new orchestrator env knob is required: phase one is the
  interactive design phase and the orchestrator does not drive it.

### review-floor settlement (machine settlement of a delegated open choice)

The operator delegated the review-floor decision. Settled as **debt, not pin**: 011 preserves
current behavior and records as debt that the strong review floor is not yet mechanically pinned
to a checked strong model (it can ride an ambient harness default). The de-named statements
preserve the existing strong-floor intent without adding a proof 011 does not deliver; a future
loop pins a checked strong-review default.

### parent intent amendments

- `collaboration` (+ machine statements): de-name the review-roster and acceptance statements;
  add the collaborator/throughput partition and the review-floor-independent-of-collaborator
  statement.
- `loop` (+ machine statements): de-name builder-session, exec, and knob-identifier wording to
  role/capability terms; add the phase-one routing statement as a sibling to the phase-two
  builder-routing line.
- `adapter` (+ machine statements): the largest delta — sort every product-named statement
  through the three layers, move current-binding behavioral facts into `adapter/codex.md`, keep
  only whitelisted path pointers in statements, and add the per-phase binding statement.

### material amendments

- `hypercore.md`: de-name the adapter section to role/pointer language.
- `intent/organizing-document.md`: de-name the adapter bullet, leaving the `home`/`codex-cockpit`
  text untouched.
- `adapter/codex.md`: receives the current-binding behavioral facts moved out of the statements;
  stays the product-named materialization. Records two debts: the unpinned strong review floor,
  and the phase-one review reviewer prompt that assumes a signed route-settled frame and so
  cannot PASS a correctly-staged pre-direction frame.
- `adapter/loop.sh`: no behavior change; de-name only comments that restate contract; `CODEX_*`
  knob identifiers unchanged (Option 1).
- `check.sh`: add the product-absence check (the grammar above) over the enumerated statement
  files; assert the collaborator, throughput-delegation, review-floor-independence, and
  phase-one-routing statements are present; assert held defaults reproduce current routing when
  the knobs are unset. Self-tests: an unwhitelisted product token in a statement file FAILS; a
  whitelisted fenced pointer PASSES; a `codex-cockpit` mention in the home text PASSES; the new
  role statements are present.

Implementation units for phase two:

1. De-name the contract statements and add the phase-one roles, updating `check.sh` in lockstep
   so it stays green. Across `intent/collaboration.md`, `intent/loop.md`, `intent/adapter.md`
   and their `machine-statements/` counterparts, plus the adapter sections of `hypercore.md` and
   `intent/organizing-document.md`, apply the three-layer sort (methodology claim → role;
   capability → "the harness must support X"; current-binding fact → moved into
   `adapter/codex.md`); add the collaborator, throughput-delegation,
   review-floor-independent-of-framer, and phase-one-routing statements; and update `check.sh`
   to drop assertions that require the old product-named wording and add the scoped
   product-absence check with the pointer grammar, the role-statement-presence assertions, and
   the held-default assertions. `./check.sh` is green at the unit boundary.
2. Add the `check.sh` self-tests for the grammar (an unwhitelisted product token in a statement
   file fails; a whitelisted fenced pointer passes; a `codex-cockpit` home-text mention passes;
   the role statements are present) and a held-defaults-reproduce-current-routing test; record
   the two debts in `adapter/codex.md` (the unpinned strong review floor; the phase-one review
   reviewer-prompt mismatch); and de-name any contract-restating comments in `adapter/loop.sh`.
   `./check.sh` is green at the unit boundary.

## acceptance condition

After adoption: the `collaboration`/`loop`/`adapter` contract (intent and machine statements),
the adapter prose, and `check.sh` express the harness binding in role and config terms with no
harness product named in any *statement*; a phase-one *collaborator* role and a phase-one
routing/delegation seam exist with held defaults that reproduce current behavior; the strong
review floor's independence from the framer is stated; and `./check.sh` is green.

## observable acceptance

- `./check.sh` exits zero after implementation and after the archive fold.
- A check asserts that no contract *statement* file — the enumerated set
  `intent/collaboration.md`, `intent/loop.md`, `intent/adapter.md`, their `machine-statements/`
  counterparts, and the adapter sections of `hypercore.md` and `intent/organizing-document.md`
  — contains a harness-product token (product names and product-bearing knob identifiers alike)
  except inside an exactly specified materialization-pointer grammar (a whitelisted fenced path
  reference such as `adapter/codex.md` or `AGENTS.md`, or a designated current-binding section).
  The check is scoped to those files only: adopted history, scratch findings, child-node names
  (e.g. `codex-cockpit`), and mounted-entrypoint material are out of scope. Capability-requirement
  statements pass because they name a required capability, not a product. The exact grammar and
  token set are fixed in the route.
- The contract names a phase-one collaborator role and a phase-one routing/delegation seam,
  each with a held default.
- A check asserts the "review floor independent of the framer" statement is present.
- The materialization still binds the current harness and still executes phase two:
  `adapter/codex.md` and `AGENTS.md` remain, and `adapter/loop.sh` still runs the executor.

## excluded interpretation

- Not a second phase-two executor. This introduces no new execution or build path; unlike the
  retired `001-remove-claude-adapter` Claude binding, phase two stays on the existing executor.
- Not a demotion of the proof floor. Routing never makes review or acceptance cheaper, and
  never lets the framer review its own work.
- Not a rename or removal of materialization. `adapter/loop.sh` still calls the executor;
  `adapter/codex.md` remains the current binding.
- Not a new gate and not field-count collaboration. It adds roles and config, not paperwork.
- Not a planner or executor. The phase-one collaborator's output ends at orient and frame
  artifacts (teach-back, options, frame, decision brief); it does not create implementation
  units, plan tasks, acceptance artifacts, or review evidence. This keeps the collaborator seam
  distinct from the queued two-step planner.

## proof state

Required proof: the observable-acceptance checks above, plus `check.sh` self-tests that a
product-named contract statement fails the product-absence check, and that the held defaults
reproduce current routing when the knobs are unset. Baseline `./check.sh` is green before
implementation (to be confirmed at the start of phase two).

Phase-one evidence: the governed one-way review roster ran (`intent/frame/review.md`); its base
flags reduced to a pre-direction staging artifact (route is TODO before direction, by gate
design) rather than a substantive defect, so a corrected independent decision review was run and
recorded at `intent/frame/review-supplementary.md`. Its substantive findings — the
capability-requirement layer, the exact pointer grammar, the scoped check, the collaborator
output boundary, and the unpinned review floor — are folded into the constraints, observable

exec
/bin/bash -lc "sed -n '1,240p' intent/organizing-document.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# organizing document

hypercore's intent is held in two groups of segments, one document each.

The **methodology** -- the nine segments describing the rules themselves,
leaf-materialized by `hypercore.md` and `check.sh`, divided along one axis:

- **foundations** -- the premise, the three properties, and what the intent is.
- **collaboration** -- how operator and machine work together: role partition, common
  ground, reliance calibration, control, feedback, handoff, and graceful failure.
- **structure** -- the reserved intent tree, how the corpus is laid out, and how a node
  nests inside another.
- **statements** -- what a statement is, and ownership.
- **endorsement** -- who stands behind a set, per segment and per work, and where the node
  boundary stops it.
- **active-work** -- the work-node lifecycle and the root contract for active child work.
- **loop** -- the five gates a work node goes through.
- **sweep** -- how coherence is checked across the corpus, work in flight, proposed parent
  amendments, and node boundaries.
- **adapter** -- the binding between a harness and the loop: what the harness loads at the
  start of work, promising agreement and enforcing it as a rigid workflow. Materialized at
  the root by the methodology prose, the harness entry point (`AGENTS.md`), the current
  binding (`adapter/codex.md`), and the orchestrator under `adapter/`.

The **governed work** -- durable child nodes and mounted work under this root:

- **home** -- the named child node at `home/`, with its own `intent/`, that mounts linked
  project nodes and governs them within itself. home currently mounts `codex-cockpit`.

Each segment has an intent document at `intent/<segment>.md` and a machine-statements file
at `intent/machine-statements/<segment>.md`. A child node is a directory or settled linked
entry point carrying its own `intent/`; a mounted project is a child node of home, a
separate corpus exposed through `home/<name>` as a symbolic link to its own repository.

This is two groups, not a tag: nothing is partitioned twice. A tag is added only the first
time a real second partition of the whole corpus forces it, not before.

exec
/bin/bash -lc "sed -n '1,240p' hypercore.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# hypercore

hypercore is a way to keep a growing codebase coherent when the machine starts each
session with no memory.

The method has three tests:

- **scrutable**: a reader can recover what the system means.
- **sound**: nothing important rests on unproven ground.
- **fast**: work moves in small steps with little ceremony.

When those tests pull against each other, name the tension instead of hiding the tradeoff.

```text
operator purpose + written intent + checked material
        \              |              /
         \             |             /
          ---------- hypercore -------
```

## intent

Intent is the current written model of the system: what each part is meant to be, how it
behaves, and what it depends on.

It does not carry memory or rationale. The reason a statement exists lives in the work
that made it. The proof lives in checks on the material.

```text
intent says:     what is meant to be true
work records:    why this became true
checks prove:    whether the material still holds it
```

Work starts by reading the intent and the material. If something needed is not written,
it is not assumed.

## collaboration

The operator and the machine keep common ground written, but phase one is not proved by
field count. It is an arc: understanding before route, reversibility-sized scrutiny,
operator direction, lean recoverability, then sign-off.

- The operator sets purpose, constraints, acceptance, and open direction.
- The machine searches, synthesizes, drafts, executes, checks, and settles what is left
  open.
- Before a route is written, the machine gives a teach-back, at least one alternative
  framing, information-gain questions, and a reversibility classification.
- One-way work gets a small mechanical base review roster before route settlement:
  `contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`.
  Optional reviewers are additive and advisory only; they cannot clear unresolved base or
  red-team flags.
- Direction and sign-off are the two anchored operator acts. On the legitimate helper
  path, each act crosses an operator gate that reads the decisive token from `/dev/tty`
  and records `operator-gate: tty`; this is terminal liveness for the helper path, which
  the default machine command path lacks. It is not cryptographic non-repudiation,
  tamper-evidence, file integrity, or proof an operator rather than a deliberately
  allocated terminal answered.
- Direction records a selected route, constraint, or explicit delegation with
  `direction-by:` and `direction-given-at:`. When direction needs a route choice, the
  machine drafts neutral, materially distinct options in `intent/frame/options.md`, and
  the operator picks one; the machine never writes direction for itself.
- The machine makes uncertainty, evidence, limits, and failure modes visible enough for
  the operator to rely on it, challenge it, redirect it, or stop it.
- Sign-off attests informed expectation and understanding, and still requires a complete
  lean frame plus the required phase-one acts; it is not earned by bloated field scanning.
  The helper renders a frame-derived brief and requires the work number before writing
  `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty`.
- Phase-two acceptance is part of reliance calibration: before one-way adoption stamps the
  operator's endorsement, the built result is checked independently against what the
  operator signed, with structured verdicts that include rationale and evidence.
- Unresolved implementation-acceptance flags block archive and surface to the operator
  rather than being self-cleared, averaged away, or treated as warnings.
- When written ground is insufficient, the machine records the blocker and stops instead
  of fabricating content.

Feedback becomes durable: corrections, discovered facts, failed checks, and sweep flags
become intent, proof, machine statements, or debt.

## nodes

A node is a governed corpus. The root is a node; any node-local corpus entry with
`intent/` can be a child node too.

```text
node/
  intent/
    organizing-document.md
    <segment>.md
    machine-statements/<segment>.md
    history/
  leaf material
  child nodes
  active work nodes
```

The node boundary matters. A child is free except where a parent statement explicitly
reaches into it.

```text
parent node
  statement reach:
    node-local        -> parent only
    named child       -> one child
    direct children   -> every immediate child
    descendants       -> the tree below
```

An unmaterialized child slot is dormant. Do not invent its content.

## segments

Each node chooses its own segments in `intent/organizing-document.md`.

At the methodology root, the methodology has nine segments:

- foundations
- collaboration
- structure
- statements
- endorsement
- active-work
- loop
- sweep
- adapter

The governed work group names durable child nodes and mounted work governed by this root.

Each segment has:

- `intent/<segment>.md` for current statements.
- `intent/machine-statements/<segment>.md` for machine statements.

The methodology prose is this file. The mechanical check over nodes is `check.sh`.

## statements

A statement is plain, declarative, and strong enough to be wrong.

```text
good statement:  check.sh checks every node in the tree.
weak statement:  checks should probably cover most important things.
```

One name means one concept. Behavior and dependency are both written as statements.

Every statement must be ownable and checkable. If it is neither, the work turns it away.

## ownership

Ownership is the right to change a statement, not permission to break it.

```text
endorsed statement   -> operator owned
unendorsed statement -> machine owned
```

The machine never endorses, so unendorsed statements fall to the machine by default. Both
operator and machine are still bound by coherence.

Machine freedom is taken, not declared: when the operator leaves a choice open and the
machine settles it, the machine statement records that settlement.

## endorsement

Endorsement is per segment and per node.

```text
intent/<segment>.md

... statements ...

## machine
... machine statements ...

---
endorsed by <operator>
```

Changing a segment means taking on the segment's whole operator set. There is no partial
endorsement. If a segment becomes too large to own, split it or move suitable statements
under `## machine`.

A work frame carries sign-off. On adoption, that sign-off stamps each touched segment.

## active work

Active work is a child node directly under the addressed node.

```text
002-simplify-methodology-doc/
  intent/
    frame/
```

A work node can propose parent intent or parent material amendments without making them
current. Until adoption accepts the amendment, the parent intent remains current.

Adoption folds accepted child statements and material into the parent and records history.
Shelving records history without changing parent truth.

## loop

Every work node that needs adoption or shelving goes through five gates.

```text
orient -> frame -> implement -> check -> archive
\___ phase one ___/  \______ phase two _____/
          |
       sign-off
```

- **orient**: read the intent, work in flight, and material conventions.
- **frame**: after substantive direction exists, write the problem, constraints, route,
  reversibility, acceptance condition, observable acceptance, excluded interpretation,
  proof state, target segments, work in flight, sweep, and adoption or shelving claim.
- **implement**: after sign-off, build from the written frame in green proof-advancing
  units.
- **check**: run mechanical checks and independent structured implementation acceptance;
  one-way work gets a required implementation-acceptance panel before archive, with the
  panel lenses started concurrently after tier-one evidence is clean.
- **archive**: adopt or shelve according to the signed frame.

Direction and review are phase-one acts and artifacts, not extra gates. New work that
needs route selection carries `intent/frame/options.md`; `./direction` selects one
numbered option through `/dev/tty`, writes `operator-gate: tty`, or lets the operator
reject all options or abort without writing direction. Two-way work skips review unless
requested. One-way work requires the base review artifact before the route is signable.
Sign-off is the operator act between phases: `./signoff` renders a concise frame-derived
attestation brief through `/dev/tty`, requires the work number as confirmation, and writes
`signed-off-at:` plus `operator-gate: tty`. The session clears at sign-off, and phase two
must be able to re-derive each unit and acceptance review from the signed frame directory
plus lean handoff artifacts alone.

## sweep

The sweep checks semantic coherence. It does not replace proof.

```text
map:  where does this concept appear?

exec
/bin/bash -lc 'git --no-pager diff -- intent/collaboration.md intent/loop.md intent/adapter.md intent/machine-statements/collaboration.md intent/machine-statements/loop.md intent/machine-statements/adapter.md hypercore.md intent/organizing-document.md adapter/codex.md adapter/loop.sh check.sh' in /home/qqp/projects/hypercore
 succeeded in 0ms:
diff --git a/adapter/codex.md b/adapter/codex.md
index f71f4cd..e0a8a53 100644
--- a/adapter/codex.md
+++ b/adapter/codex.md
@@ -15,6 +15,23 @@ intent and run the loop, not because you chose to, but because the workflow make
 gates unskippable. Pointing alone is a request; the orchestrator is how agreement is
 kept.
 
+## Current Harness Binding
+
+The current root binding is Codex. The root `AGENTS.md` entry point is symlinked to
+`adapter/codex.md`; it is the harness-mandated pointer and not where the adapter lives.
+Nested work under this root receives that entry point through the project instruction
+chain, so nested nodes do not carry their own adapter material.
+
+The current materialization binds Codex to both phase one and phase two. Phase one defaults
+to the interactive Codex harness that loaded this adapter. Phase two is driven by
+`adapter/loop.sh`, which invokes fresh `codex exec` sessions for builders, reviewers, and
+the archive actor; the orchestrator records raw Codex JSON event streams and Codex thread
+ids as current binding facts.
+
+The current materialization also keeps the `CODEX_*` environment knob names in
+`adapter/loop.sh`. Those names are implementation binding, while the intent states the
+builder-model, strong-builder, review-model, and review-effort roles.
+
 ## Orient before you touch anything
 
 First classify the request surface. Ordinary conversation, explanation, and read-only
@@ -113,6 +130,12 @@ as a checked statement, then dropped.
   empty node — not a fake app with invented sub-projects.
 - **Name in hypercore's own vocabulary** — node, segment, contract, mount, materialize,
   the loop. Reject domain words that collide with the methodology's own concepts.
+- **Pin the strong review floor.** The strong review floor is not yet mechanically pinned
+  to a checked strong model; it can still ride an ambient harness default. A future loop
+  pins it.
+- **Re-prompt phase-one one-way review.** The current phase-one one-way review reviewer
+  prompt assumes a signed, route-settled frame and therefore cannot PASS a correctly staged
+  pre-direction frame. A future loop re-prompts it for a pre-direction decision surface.
 
 ---
 This adapter is itself governed: the `adapter` segment is its intent, and the sweep reads
diff --git a/adapter/loop.sh b/adapter/loop.sh
index c20c43f..085604b 100755
--- a/adapter/loop.sh
+++ b/adapter/loop.sh
@@ -2792,7 +2792,7 @@ run_codex_gate() {
   printf '%s\n' "$GATE_OUTPUT"
 }
 
-# a single fresh phase-two Codex session.
+# a single fresh phase-two executor session.
 # args: <gate-name> <allowed-tools> <mode> <session-id> <prompt> [instruction-gate]
 # mode is start; every phase-two builder, acceptance reviewer, and archive actor is fresh.
 run_gate() {
diff --git a/check.sh b/check.sh
index 1f39843..51bffa5 100755
--- a/check.sh
+++ b/check.sh
@@ -68,6 +68,172 @@ reject_regular_file() {
   fi
 }
 
+contract_statement_product_absence_errors() {
+  local file=$1 scope=$2
+  HYPERCORE_CONTRACT_SCOPE="$scope" perl -0ne '
+    my $scope = $ENV{HYPERCORE_CONTRACT_SCOPE} || "all";
+    my $text = $_;
+
+    if ($scope eq "hypercore-adapter") {
+      if ($text =~ /^## adapter\n(.*?)(?=^## |\z)/ms) {
+        $text = $1;
+      } else {
+        print "$ARGV: missing ## adapter section\n";
+        exit 1;
+      }
+    } elsif ($scope eq "organizing-adapter") {
+      my @kept;
+      my $taking = 0;
+      for my $line (split /\n/, $text) {
+        if ($line =~ /^- \*\*adapter\*\*/) {
+          $taking = 1;
+        } elsif ($taking && $line =~ /^\s*$/) {
+          last;
+        }
+        push @kept, $line if $taking;
+      }
+      if (!@kept) {
+        print "$ARGV: missing adapter bullet\n";
+        exit 1;
+      }
+      $text = join("\n", @kept) . "\n";
+    }
+
+    my %allowed = map { $_ => 1 } (
+      "adapter/codex.md",
+      "AGENTS.md",
+      "adapter/codex-mounted.md",
+      "adapter/loop.sh",
+    );
+    my @spans;
+    while ($text =~ /`([^`\n]+)`/g) {
+      push @spans, [$-[1], $+[1], $1];
+    }
+
+    my $product = qr/(?<![A-Za-z0-9_])(?:codex|claude|opus|gpt-[0-9][A-Za-z0-9._-]*|CODEX_[A-Za-z0-9_]*)(?![A-Za-z0-9_])/i;
+    while ($text =~ /$product/g) {
+      my ($start, $end, $token) = ($-[0], $+[0], $&);
+      my $ok = 0;
+      for my $span (@spans) {
+        if ($start >= $span->[0] && $end <= $span->[1] && $allowed{$span->[2]}) {
+          $ok = 1;
+          last;
+        }
+      }
+      next if $ok;
+      my $prefix = substr($text, 0, $start);
+      my $line = 1 + ($prefix =~ tr/\n//);
+      print "$ARGV:$line: product token \"$token\" is outside a whitelisted materialization pointer\n";
+      exit 1;
+    }
+  ' "$file"
+}
+
+contract_statement_product_absence() {
+  local file=$1 scope=$2 label=$3 output status
+  output="$(contract_statement_product_absence_errors "$file" "$scope" 2>&1)"
+  status=$?
+  if [ $status -eq 0 ]; then
+    ok "$label"
+  else
+    bad "$label ($output)"
+  fi
+  return $status
+}
+
+check_contract_statement_product_absence_self_tests() {
+  local tmp forbidden pointer organizing
+
+  echo "root - contract statement product grammar self-test"
+  tmp="$(mktemp -d "${TMPDIR:-/tmp}/hypercore-contract-product-check.XXXXXX")" \
+    || { bad "contract product grammar self-test can create temporary space"; return; }
+
+  forbidden="$tmp/forbidden.md"
+  cat > "$forbidden" <<'EOF'
+# fixture
+
+the Codex review floor is named in a contract statement.
+EOF
+  if ( fail=0; contract_statement_product_absence "$forbidden" all \
+    "forbidden product token fixture" >"$tmp/forbidden.out" 2>&1 ); then
+    bad "contract product grammar rejects an unwhitelisted harness-product token"
+  else
+    ok "contract product grammar rejects an unwhitelisted harness-product token"
+  fi
+  require_text "$tmp/forbidden.out" \
+    'product token "Codex" is outside a whitelisted materialization pointer' \
+    "contract product grammar failure names the forbidden token"
+
+  pointer="$tmp/pointer.md"
+  cat > "$pointer" <<'EOF'
+# fixture
+
+the current root harness adapter is materialized as `adapter/codex.md`.
+EOF
+  if ( fail=0; contract_statement_product_absence "$pointer" all \
+    "whitelisted materialization pointer fixture" >"$tmp/pointer.out" 2>&1 ); then
+    ok "contract product grammar accepts a whitelisted materialization pointer"
+  else
+    bad "contract product grammar accepts a whitelisted materialization pointer"
+  fi
+
+  organizing="$tmp/organizing-document.md"
+  cat > "$organizing" <<'EOF'
+# organizing document
+
+- **adapter** -- the binding between a harness and the loop, materialized through `adapter/codex.md`.
+
+The **governed work** -- durable child nodes and mounted work under this root:
+
+- **home** -- home currently mounts codex-cockpit.
+EOF
+  if ( fail=0; contract_statement_product_absence "$organizing" organizing-adapter \
+    "out-of-scope governed-work product mention fixture" >"$tmp/organizing.out" 2>&1 ); then
+    ok "contract product grammar ignores out-of-scope governed-work child-node names"
+  else
+    bad "contract product grammar ignores out-of-scope governed-work child-node names"
+  fi
+
+  require_text "$root/intent/collaboration.md" \
+    "the phase-one collaborator is the harness role that drives orient and frame" \
+    "phase-one routing self-test sees the collaborator role assertion"
+  require_text "$root/intent/collaboration.md" \
+    "phase-one corpus-throughput work" \
+    "phase-one routing self-test sees the throughput-delegation assertion"
+  require_text "$root/intent/collaboration.md" \
+    "the framer is not its own witness" \
+    "phase-one routing self-test sees the independent-review-floor assertion"
+  require_text "$root/intent/loop.md" \
+    "phase-one labor may be routed by role" \
+    "phase-one routing self-test sees the phase-one routing assertion"
+  require_text "$root/intent/loop.md" \
+    "the collaborator role defaults to the interactive harness that loaded the adapter" \
+    "phase-one routing self-test sees the collaborator held default"
+  require_text "$root/intent/loop.md" \
+    "the fast-builder default is held at the strong model" \
+    "phase-one routing self-test sees the builder held default"
+  require_text "$root/intent/loop.md" \
+    "phase-one review stay on the" \
+    "phase-one routing self-test sees the review-floor held default"
+  require_text "$root/intent/adapter.md" \
+    "the phase-one collaborator role defaults to the interactive harness" \
+    "phase-one routing self-test sees the adapter collaborator default"
+  require_text "$root/adapter/codex.md" \
+    "to the interactive Codex harness that loaded this adapter" \
+    "phase-one routing self-test sees the current binding collaborator default"
+  require_text "$root/adapter/loop.sh" \
+    'CODEX_REVIEW_EFFORT:-xhigh' \
+    "phase-one routing self-test sees the review-effort held default"
+  require_text "$root/adapter/loop.sh" \
+    'CODEX_BUILDER_MODEL:-gpt-5.5' \
+    "phase-one routing self-test sees the builder-model held default"
+  require_text "$root/adapter/loop.sh" \
+    'CODEX_BUILDER_EFFORT:-xhigh' \
+    "phase-one routing self-test sees the builder-effort held default"
+
+  rm -rf "$tmp"
+}
+
 shopt -s nullglob
 HOME_GREENFIELD_CHECK_TMP=
 HOME_GREENFIELD_CHECK_MOUNT=
@@ -1696,6 +1862,56 @@ require_text "$root/intent/loop.md" \
 require_text "$root/intent/adapter.md" \
   "resumable per-unit execute cache" \
   "adapter segment folds resumable execute materialization"
+require_text "$root/intent/collaboration.md" \
+  "the phase-one collaborator is the harness role that drives orient and frame" \
+  "collaboration segment names the phase-one collaborator role"
+require_text "$root/intent/collaboration.md" \
+  "phase-one corpus-throughput work" \
+  "collaboration segment allows delegated phase-one throughput"
+require_text "$root/intent/collaboration.md" \
+  "the framer is not its own witness" \
+  "collaboration segment keeps the review floor independent of the framer"
+require_text "$root/intent/loop.md" \
+  "phase-one labor may be routed by role" \
+  "loop segment carries phase-one routing"
+require_text "$root/intent/loop.md" \
+  "the collaborator role defaults to the interactive harness that loaded the adapter" \
+  "loop segment holds the collaborator default"
+require_text "$root/intent/loop.md" \
+  "the fast-builder default is held at the strong model" \
+  "loop segment holds the builder default"
+require_text "$root/intent/loop.md" \
+  "phase-one review stay on the" \
+  "loop segment holds the strong review floor"
+require_text "$root/intent/adapter.md" \
+  "an adapter binds a harness to a phase" \
+  "adapter segment permits per-phase harness binding"
+require_text "$root/intent/adapter.md" \
+  "the phase-one collaborator role defaults to the interactive harness" \
+  "adapter segment holds the collaborator materialization default"
+require_text "$root/adapter/codex.md" \
+  "to the interactive Codex harness that loaded this adapter" \
+  "current binding records the collaborator held default"
+require_text "$root/adapter/codex.md" \
+  "builder-model, strong-builder, review-model, and review-effort roles" \
+  "current binding separates material knob names from role statements"
+contract_statement_product_absence "$root/intent/collaboration.md" all \
+  "collaboration intent has no unscoped harness product token"
+contract_statement_product_absence "$root/intent/loop.md" all \
+  "loop intent has no unscoped harness product token"
+contract_statement_product_absence "$root/intent/adapter.md" all \
+  "adapter intent has no unscoped harness product token"
+contract_statement_product_absence "$root/intent/machine-statements/collaboration.md" all \
+  "collaboration machine statements have no unscoped harness product token"
+contract_statement_product_absence "$root/intent/machine-statements/loop.md" all \
+  "loop machine statements have no unscoped harness product token"
+contract_statement_product_absence "$root/intent/machine-statements/adapter.md" all \
+  "adapter machine statements have no unscoped harness product token"
+contract_statement_product_absence "$root/hypercore.md" hypercore-adapter \
+  "hypercore adapter section has no unscoped harness product token"
+contract_statement_product_absence "$root/intent/organizing-document.md" organizing-adapter \
+  "organizing adapter bullet has no unscoped harness product token"
+check_contract_statement_product_absence_self_tests
 [ -x "$root/check.sh" ] \
   && ok "check.sh exists and is executable" \
   || bad "check.sh is missing or not executable"
diff --git a/hypercore.md b/hypercore.md
index 9db8bab..530d5a5 100644
--- a/hypercore.md
+++ b/hypercore.md
@@ -256,8 +256,8 @@ The adapter binds a harness to the methodology.
 harness loads adapter -> adapter points to intent + loop -> gates become enforceable
 ```
 
-For Codex, the root `AGENTS.md` points at the adapter. The adapter does not replace the
-intent; it routes the machine to the intent and makes the loop's gates rigid.
+For the current binding, `AGENTS.md` points at `adapter/codex.md`. The adapter does not
+replace the intent; it routes the machine to the intent and makes the loop's gates rigid.
 
 Phase one is interactive design work. Phase two is cleared, heads-down execution from the
 signed frame. If a gate precondition fails, the adapter blocks instead of warning.
diff --git a/intent/adapter.md b/intent/adapter.md
index d7bda9c..97528c2 100644
--- a/intent/adapter.md
+++ b/intent/adapter.md
@@ -19,23 +19,22 @@ a decision surface for substantive operator direction; after sign-off, implement
 and archive run through cleared sessions that re-derive each unit and acceptance review
 from the signed frame directory and lean phase-two handoff artifacts alone.
 direction and review are phase-one acts or artifacts, not loop gates.
-the Codex review roster for one-way phase-one work has a base roster of
+the review roster for one-way phase-one work has a base roster of
 `contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`.
-the Codex implementation-acceptance reviewer for each phase-two unit is independent and
-read-only.
-the Codex tier-two implementation-acceptance panel for one-way work has required lenses
+the implementation-acceptance reviewer for each phase-two unit is independent and read-only.
+the tier-two implementation-acceptance panel for one-way work has required lenses
 `whole-acceptance-conformance`, `proof-integrity`, `independent-coherence`,
 `security-permissions`, and `red-team`.
-the complete optional Codex review roster is `implementation-maintainability`,
+the complete optional review roster is `implementation-maintainability`,
 `security-permissions`, `operator-ergonomics`, `migration-compatibility`,
 `domain-evidence`, and `performance-cost`.
 optional reviewers are advisory additions and cannot override, outvote, average away, or
 dilute unresolved base-roster or red-team flags.
-the Codex adapter classifies the request surface before changing material: ordinary
+the adapter classifies the request surface before changing material: ordinary
 conversation and read-only inspection may proceed directly, while governed work starts or
 continues a work node.
-the Codex adapter rejects perceived simplicity, file count, convenience, and low risk as
-waivers for governed work.
+the adapter rejects perceived simplicity, file count, convenience, and low risk as waivers
+for governed work.
 on request the adapter renders a statement of the intent intelligible in plain language
 without altering it.
 the adapter carries only what the intent cannot yet reach the harness with -- the order to
@@ -43,6 +42,10 @@ read the intent first, and disciplines not yet written as statements; each is a
 folded into the intent by later work and then dropped.
 an adapter is per harness; one node may be bound by more than one, each loaded by its own
 harness.
+an adapter binds a harness to a phase; phase one and phase two may bind different harnesses,
+and the current materialization binds one harness to both phases.
+the phase-one collaborator role defaults to the interactive harness that loaded the
+adapter; no orchestrator routing knob is required until a materialization routes that role.
 the adapter material is materialized only at the methodology root, with the prose it routes
 to, and not in any nested node; a mounted external project may carry a target-local entry
 point that links to root-managed adapter material and routes direct-path work back to the
@@ -54,27 +57,29 @@ the intent has since absorbed, is caught as drift.
 
 ## machine
 the current root harness adapter is materialized as `adapter/codex.md`.
-the Codex harness loads its adapter through a root `AGENTS.md` symlinked to
-`adapter/codex.md`; the root entry is the harness's mandated pointer, holding nothing, not
-where the adapter lives.
-a machine working in a nested node under the root is bound by Codex including the root
-`AGENTS.md` in the project instruction chain from the project root to the current
-directory, so no node below the root carries its own adapter material.
+the current materialization binds the same harness to phase one and phase two; the
+phase-one collaborator is the interactive harness that loaded the adapter.
+the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;
+the root entry is the harness's mandated pointer, holding nothing, not where the adapter
+lives.
+a machine working in a nested node under the root is bound by the root `AGENTS.md` in the
+project instruction chain from the project root to the current directory, so no node below
+the root carries its own adapter material.
 a mounted external project may carry a target-local `AGENTS.md` entry point for
 direct-path openings; the entry point links to root-managed adapter material and routes
 back to the root adapter and loop instead of copying root adapter material into the
 mounted node.
 the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
-over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
-builder session from the signed frame, and acceptance reviewers and the archive actor are
-fresh sessions rather than resumes of the builder.
-the Codex loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
-`.hypercore/loop-runs`, with run-local state, event history, raw Codex gate streams, gate
+over the phase-two executor harness: each implementation unit opens a fresh builder
+session from the signed frame, and acceptance reviewers and the archive actor are fresh
+sessions rather than resumes of the builder.
+the loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
+`.hypercore/loop-runs`, with run-local state, event history, raw harness gate streams, gate
 final outputs, acceptance artifact paths, and current pointers for the addressed work and
 root.
-the Codex loop streams inner `codex exec --json` events into the phase-two run state while
+the loop streams inner executor JSON events into the phase-two run state while
 printing concise progress, without changing the cleared-session contract.
-the Codex loop materializes separate builder and reviewer routing, structured acceptance
+the loop materializes separate builder and reviewer routing, structured acceptance
 artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
 then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
 one-way tier-two panel, and phase-one review subprocess crash diagnostics.
@@ -105,10 +110,10 @@ framing and requires `intent/frame/review.md` for one-way work.
 the frame gate prompt tells the machine not to write operator direction, not to collect
 direction retrospectively, and not to let optional reviewer verdicts clear base-roster or
 red-team flags.
-the Codex adapter prose describes phase one as design-phase collaboration with direction
+the adapter prose describes phase one as design-phase collaboration with direction
 and review artifacts, while preserving phase two as cleared, heads-down execution from the
 signed frame directory and lean phase-two handoff artifacts.
-`check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
+`check.sh` mechanically checks that the gate prompts, adapter prose, loop frame
 validation, start scaffolding, direction/review helpers, operator-act gating through
 `/dev/tty` with B-ready `operator-gate:` markers and numbered-option direction, review and
 acceptance isolation settings, strict frame parsing, phase-two acceptance gating, structured
@@ -117,8 +122,8 @@ builder/reviewer routing with bounded retry and strong escalation, resumable exe
 caching, the concurrent tier-two panel, the new operator-act and phase-two performance
 contract in the `collaboration`, `loop`, and `adapter` segments, and current-material
 absence of the retired compatibility route still carry the contract.
-each gate's instructions are held in a file in `adapter/gates/`; the Codex path includes them in
-the `codex exec` gate prompt; the orchestrator owns gate order and preconditions and
+each gate's instructions are held in a file in `adapter/gates/`; the harness path includes
+them in the executor gate prompt; the orchestrator owns gate order and preconditions and
 blocks a gate whose preconditions fail.
 sign-off for new work records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty`
 in the work-node frame's `intent/frame/signoff.md`; the orchestrator seals phase two until
diff --git a/intent/collaboration.md b/intent/collaboration.md
index 83ab76a..49db957 100644
--- a/intent/collaboration.md
+++ b/intent/collaboration.md
@@ -5,10 +5,17 @@ collaboration is the working relation by which operator and machine keep the wor
 effective collaboration is complementarity, not maximal automation: the operator sets purpose, constraints, acceptance, and open direction; the machine searches, synthesizes, drafts, executes, checks, and settles only what the intent and operator leave open.
 collaboration keeps common ground recoverable without treating field count as proof of collaboration quality.
 phase one is an arc: understanding before route, scrutiny sized by reversibility, operator direction, lean recoverability, and sign-off.
+the phase-one collaborator is the harness role that drives orient and frame: it carries
+operator-facing judgment, surfaces understanding and options, and frames the signed route.
+phase-one corpus-throughput work -- research, the orient corpus read, and the sweep map --
+may be delegated by the collaborator when written ground preserves accountability and
+operator direction.
 before a route is written, the machine gives a teach-back, at least one alternative framing, information-gain questions, and a reversibility classification.
 one-way work requires distinct-route scrutiny before route settlement, including a mechanically spawned base review roster.
 the base review roster is `contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`; optional reviewers are additive and advisory only.
 optional reviewers cannot override, outvote, average away, or dilute unresolved base-roster or red-team flags.
+for one-way work, the strong review floor that scrutinizes a frame is independent of the
+collaborator that framed it; the framer is not its own witness.
 review quality is not proved by artifact scanning; review artifacts record structured signal, unresolved flags, and disposition.
 direction and sign-off are the two anchored operator acts in phase one, and the machine performs neither for itself.
 operator direction is substantive: it records a selected route, constraint, or explicit delegation with `direction-by:`.
@@ -29,7 +36,7 @@ collaboration degrades gracefully: when written ground is insufficient, the mach
 
 ## machine
 phase-two handoff state is written as common ground for the operator and later tooling:
-the addressed work's current or recent gate, current unit, status, Codex thread id, latest
+the addressed work's current or recent gate, current unit, status, harness session id, latest
 message, failure reason, event history, run artifact paths, and phase-two acceptance
 artifact paths are recoverable from loop state files.
 
diff --git a/intent/loop.md b/intent/loop.md
index 08d4577..8bd5109 100644
--- a/intent/loop.md
+++ b/intent/loop.md
@@ -60,6 +60,10 @@ acceptance reviewer output counts as `FLAG`.
 acceptance artifacts record their source as real reviewer, dry-run/self-test, or
 fake/self-test; real execute refuses fake acceptance, and real archive refuses dry-run or
 fake-source required acceptance.
+phase-one labor may be routed by role: the collaborator drives operator-facing orient and
+frame work, corpus-throughput work may be delegated, and the collaborator may differ from
+the phase-two executor harness while phase-one review stays on the strong review floor.
+the collaborator role defaults to the interactive harness that loaded the adapter.
 phase-two builders may be routed separately from reviewers through a fast-builder model
 knob, while tier-one acceptance, tier-two acceptance, and phase-one review stay on the
 strong review floor; the fast-builder default is held at the strong model until the
@@ -104,11 +108,12 @@ corpus.
 `loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work and
 act only on that addressed work.
 `loop.sh execute <work-name>` exposes phase-two run state for the addressed work while it
-runs and after recent failure or completion, including the active gate, status, Codex
-thread id, latest message, event history, and run artifact paths.
-before launching the first phase-two Codex gate, `loop.sh execute <work-name>` checks that
-the Codex binary is present and that Codex home/session state is writable; a failed
-preflight records failed run state and stops before `codex exec`.
+runs and after recent failure or completion, including the active gate, status, harness
+session id, latest message, event history, and run artifact paths.
+before launching the first phase-two executor gate, `loop.sh execute <work-name>` checks
+that the configured executor binary is present and that executor home/session state is
+writable; a failed preflight records failed run state and stops before the executor
+session starts.
 `loop.sh status <work-name>` reports the addressed work's current phase and, for
 non-historical work with phase-two state, the current or recent run's gate, status, state
 path, event path, and latest message; `loop.sh status --json <work-name>` renders the same
@@ -163,12 +168,13 @@ optional reviewer verdicts cannot clear unresolved base-roster or red-team flags
 new work sign-off records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty` in
 the work node's `intent/frame/signoff.md`.
 `loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
-fresh Codex builder session for each unit, and records lean unit handoff, diff, and
-tier-one verdict artifacts under the work frame.
-`loop.sh execute <work-name>` routes builders through `CODEX_BUILDER_MODEL`, defaulting to
-the strong model until the two-step plan/build work lands, separately from the strong review
-route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
-to `CODEX_STRONG_BUILDER_MODEL`, and stops for the operator when the strong builder fails.
+fresh builder session for each unit, and records lean unit handoff, diff, and tier-one
+verdict artifacts under the work frame.
+`loop.sh execute <work-name>` routes builders through the builder-model knob, defaulting to
+the strong model until the two-step plan/build work lands, separately from the strong
+review route; it gives each unit a three-attempt fast-builder budget, escalates an
+exhausted unit through the strong-builder model knob, and stops for the operator when the
+strong builder fails.
 `loop.sh execute <work-name>` runs implementation-acceptance reviewers with literal
 approval `never` and literal sandbox `read-only`.
 `loop.sh execute <work-name>` writes structured acceptance artifacts with a verdict,
diff --git a/intent/machine-statements/adapter.md b/intent/machine-statements/adapter.md
index 7a704b0..fddc96b 100644
--- a/intent/machine-statements/adapter.md
+++ b/intent/machine-statements/adapter.md
@@ -1,27 +1,29 @@
 # adapter -- machine statements
 
 the current root harness adapter is materialized as `adapter/codex.md`.
-the Codex harness loads its adapter through a root `AGENTS.md` symlinked to
-`adapter/codex.md`; the root entry is the harness's mandated pointer, holding nothing, not
-where the adapter lives.
-a machine working in a nested node under the root is bound by Codex including the root
-`AGENTS.md` in the project instruction chain from the project root to the current
-directory, so no node below the root carries its own adapter material.
+the current materialization binds the same harness to phase one and phase two; the
+phase-one collaborator is the interactive harness that loaded the adapter.
+the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;
+the root entry is the harness's mandated pointer, holding nothing, not where the adapter
+lives.
+a machine working in a nested node under the root is bound by the root `AGENTS.md` in the
+project instruction chain from the project root to the current directory, so no node below
+the root carries its own adapter material.
 a mounted external project may carry a target-local `AGENTS.md` entry point for
 direct-path openings; the entry point links to root-managed adapter material and routes
 back to the root adapter and loop instead of copying root adapter material into the
 mounted node.
 the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
-over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
-builder session from the signed frame, and acceptance reviewers and the archive actor are
-fresh sessions rather than resumes of the builder.
-the Codex loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
-`.hypercore/loop-runs`, with run-local state, event history, raw Codex gate streams, gate
+over the phase-two executor harness: each implementation unit opens a fresh builder
+session from the signed frame, and acceptance reviewers and the archive actor are fresh
+sessions rather than resumes of the builder.
+the loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
+`.hypercore/loop-runs`, with run-local state, event history, raw harness gate streams, gate
 final outputs, acceptance artifact paths, and current pointers for the addressed work and
 root.
-the Codex loop streams inner `codex exec --json` events into the phase-two run state while
+the loop streams inner executor JSON events into the phase-two run state while
 printing concise progress, without changing the cleared-session contract.
-the Codex loop materializes separate builder and reviewer routing, structured acceptance
+the loop materializes separate builder and reviewer routing, structured acceptance
 artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
 then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
 one-way tier-two panel, and phase-one review subprocess crash diagnostics.
@@ -52,10 +54,10 @@ framing and requires `intent/frame/review.md` for one-way work.
 the frame gate prompt tells the machine not to write operator direction, not to collect
 direction retrospectively, and not to let optional reviewer verdicts clear base-roster or
 red-team flags.
-the Codex adapter prose describes phase one as design-phase collaboration with direction
+the adapter prose describes phase one as design-phase collaboration with direction
 and review artifacts, while preserving phase two as cleared, heads-down execution from the
 signed frame directory and lean phase-two handoff artifacts.
-`check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
+`check.sh` mechanically checks that the gate prompts, adapter prose, loop frame
 validation, start scaffolding, direction/review helpers, operator-act gating through
 `/dev/tty` with B-ready `operator-gate:` markers and numbered-option direction, review and
 acceptance isolation settings, strict frame parsing, phase-two acceptance gating, structured
@@ -64,8 +66,8 @@ builder/reviewer routing with bounded retry and strong escalation, resumable exe
 caching, the concurrent tier-two panel, the new operator-act and phase-two performance
 contract in the `collaboration`, `loop`, and `adapter` segments, and current-material
 absence of the retired compatibility route still carry the contract.
-each gate's instructions are held in a file in `adapter/gates/`; the Codex path includes them in
-the `codex exec` gate prompt; the orchestrator owns gate order and preconditions and
+each gate's instructions are held in a file in `adapter/gates/`; the harness path includes
+them in the executor gate prompt; the orchestrator owns gate order and preconditions and
 blocks a gate whose preconditions fail.
 sign-off for new work records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty`
 in the work-node frame's `intent/frame/signoff.md`; the orchestrator seals phase two until
diff --git a/intent/machine-statements/collaboration.md b/intent/machine-statements/collaboration.md
index 81e8f88..5058567 100644
--- a/intent/machine-statements/collaboration.md
+++ b/intent/machine-statements/collaboration.md
@@ -1,6 +1,6 @@
 # collaboration — machine statements
 
 phase-two handoff state is written as common ground for the operator and later tooling:
-the addressed work's current or recent gate, current unit, status, Codex thread id, latest
+the addressed work's current or recent gate, current unit, status, harness session id, latest
 message, failure reason, event history, run artifact paths, and phase-two acceptance
 artifact paths are recoverable from loop state files.
diff --git a/intent/machine-statements/loop.md b/intent/machine-statements/loop.md
index 8fbea36..ec719e2 100644
--- a/intent/machine-statements/loop.md
+++ b/intent/machine-statements/loop.md
@@ -8,12 +8,13 @@ corpus.
 `loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work and
 act only on that addressed work.
 `loop.sh execute <work-name>` exposes phase-two run state for the addressed work while it
-runs and after recent failure or completion, including the active gate, status, Codex
-thread id, current unit, latest message, failure reason, event history, run artifact
+runs and after recent failure or completion, including the active gate, status, harness
+session id, current unit, latest message, failure reason, event history, run artifact
 paths, and phase-two acceptance artifact paths.
-before launching the first phase-two Codex gate, `loop.sh execute <work-name>` checks that
-the Codex binary is present and that Codex home/session state is writable; a failed
-preflight records failed run state and stops before `codex exec`.
+before launching the first phase-two executor gate, `loop.sh execute <work-name>` checks
+that the configured executor binary is present and that executor home/session state is
+writable; a failed preflight records failed run state and stops before the executor
+session starts.
 `loop.sh status <work-name>` reports the addressed work's current phase and, for
 non-historical work with phase-two state, the current or recent run's gate, status, state
 path, event path, and latest message; `loop.sh status --json <work-name>` renders the same
@@ -68,12 +69,13 @@ optional reviewer verdicts cannot clear unresolved base-roster or red-team flags
 new work sign-off records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty` in
 the work node's `intent/frame/signoff.md`.
 `loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
-fresh Codex builder session for each unit, and records lean unit handoff, diff, and
-tier-one verdict artifacts under the work frame.
-`loop.sh execute <work-name>` routes builders through `CODEX_BUILDER_MODEL`, defaulting to
-the strong model until the two-step plan/build work lands, separately from the strong review
-route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
-to `CODEX_STRONG_BUILDER_MODEL`, and stops for the operator when the strong builder fails.
+fresh builder session for each unit, and records lean unit handoff, diff, and tier-one
+verdict artifacts under the work frame.
+`loop.sh execute <work-name>` routes builders through the builder-model knob, defaulting to
+the strong model until the two-step plan/build work lands, separately from the strong
+review route; it gives each unit a three-attempt fast-builder budget, escalates an
+exhausted unit through the strong-builder model knob, and stops for the operator when the
+strong builder fails.
 `loop.sh execute <work-name>` runs implementation-acceptance reviewers with literal
 approval `never` and literal sandbox `read-only`.
 `loop.sh execute <work-name>` writes structured acceptance artifacts with a verdict,
diff --git a/intent/organizing-document.md b/intent/organizing-document.md
index 2b37be7..43f21c1 100644
--- a/intent/organizing-document.md
+++ b/intent/organizing-document.md
@@ -19,8 +19,8 @@ leaf-materialized by `hypercore.md` and `check.sh`, divided along one axis:
   amendments, and node boundaries.
 - **adapter** -- the binding between a harness and the loop: what the harness loads at the
   start of work, promising agreement and enforcing it as a rigid workflow. Materialized at
-  the root by the methodology prose, the harness adapter (`AGENTS.md` for Codex), and the
-  orchestrator under `adapter/`.
+  the root by the methodology prose, the harness entry point (`AGENTS.md`), the current
+  binding (`adapter/codex.md`), and the orchestrator under `adapter/`.
 
 The **governed work** -- durable child nodes and mounted work under this root:
 

codex
The frame’s route is very specific: the check must reject any harness-product token in statement scope except exact fenced materialization pointers, while leaving current-binding material and the `codex-cockpit` child-name text alone. I’m going straight at that grammar and the excluded interpretations.
exec
/bin/bash -lc "rg -n -i 'codex|claude|opus|gpt-[0-9]|CODEX_' intent/collaboration.md intent/loop.md intent/adapter.md intent/machine-statements/collaboration.md intent/machine-statements/loop.md intent/machine-statements/adapter.md hypercore.md intent/organizing-document.md adapter/codex.md adapter/loop.sh check.sh" in /home/qqp/projects/hypercore
 succeeded in 0ms:
intent/adapter.md:59:the current root harness adapter is materialized as `adapter/codex.md`.
intent/adapter.md:62:the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;
adapter/codex.md:1:# Codex adapter
adapter/codex.md:3:This is the **adapter** segment of hypercore's intent, materialized for the Codex
adapter/codex.md:20:The current root binding is Codex. The root `AGENTS.md` entry point is symlinked to
adapter/codex.md:21:`adapter/codex.md`; it is the harness-mandated pointer and not where the adapter lives.
adapter/codex.md:25:The current materialization binds Codex to both phase one and phase two. Phase one defaults
adapter/codex.md:26:to the interactive Codex harness that loaded this adapter. Phase two is driven by
adapter/codex.md:27:`adapter/loop.sh`, which invokes fresh `codex exec` sessions for builders, reviewers, and
adapter/codex.md:28:the archive actor; the orchestrator records raw Codex JSON event streams and Codex thread
adapter/codex.md:31:The current materialization also keeps the `CODEX_*` environment knob names in
adapter/codex.md:95:- **The session clears at sign-off.** Phase two runs through fresh, memoryless `codex
intent/organizing-document.md:23:  binding (`adapter/codex.md`), and the orchestrator under `adapter/`.
intent/organizing-document.md:28:  project nodes and governs them within itself. home currently mounts `codex-cockpit`.
intent/machine-statements/adapter.md:3:the current root harness adapter is materialized as `adapter/codex.md`.
intent/machine-statements/adapter.md:6:the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;
hypercore.md:259:For the current binding, `AGENTS.md` points at `adapter/codex.md`. The adapter does not
adapter/loop.sh:34:#   LOOP_HARNESS=codex (default and only supported phase-two harness)
adapter/loop.sh:37:#   CODEX_BIN (default: codex), CODEX_APPROVAL (default: never)
adapter/loop.sh:38:#   CODEX_WRITE_SANDBOX (default: workspace-write), CODEX_READ_SANDBOX (default: read-only)
adapter/loop.sh:39:#   CODEX_BUILDER_MODEL (default: gpt-5.5 until the two-step plan/build lands), CODEX_BUILDER_EFFORT (default: xhigh)
adapter/loop.sh:40:#   CODEX_STRONG_BUILDER_MODEL (optional strong-builder escalation model)
adapter/loop.sh:41:#   CODEX_STRONG_BUILDER_EFFORT (default: CODEX_REVIEW_EFFORT or xhigh)
adapter/loop.sh:42:#   CODEX_REVIEW_MODEL (optional strong review/acceptance model), CODEX_REVIEW_EFFORT (default: xhigh)
adapter/loop.sh:54:LOOP_HARNESS="${LOOP_HARNESS:-codex}"
adapter/loop.sh:56:CODEX_BIN="${CODEX_BIN:-codex}"
adapter/loop.sh:57:CODEX_APPROVAL="${CODEX_APPROVAL:-never}"
adapter/loop.sh:58:CODEX_WRITE_SANDBOX="${CODEX_WRITE_SANDBOX:-workspace-write}"
adapter/loop.sh:59:CODEX_READ_SANDBOX="${CODEX_READ_SANDBOX:-read-only}"
adapter/loop.sh:204:    printf '  "codex_thread_id": %s,\n' "$(json_string "$PHASE_TWO_SESSION_ID")"
adapter/loop.sh:308:  msg="preflight failed before codex exec: $reason; rerun the outer loop with that permission, using: $(loop_execute_command "$work_name")"
adapter/loop.sh:317:  local work_name=$1 codex_home codex_parent reason msg
adapter/loop.sh:319:  msg="checking Codex binary and writable Codex home/session state"
adapter/loop.sh:324:    msg="dry-run: would check Codex binary and Codex home/session write permission before launching codex exec"
adapter/loop.sh:330:  command -v "$CODEX_BIN" >/dev/null 2>&1 \
adapter/loop.sh:331:    || phase_two_preflight_fail "Codex binary '$CODEX_BIN' is not on PATH" "$work_name" \
adapter/loop.sh:334:  if [ -n "${CODEX_HOME:-}" ]; then
adapter/loop.sh:335:    codex_home=$CODEX_HOME
adapter/loop.sh:338:      || phase_two_preflight_fail "HOME is unset and CODEX_HOME is not set, so Codex home cannot be resolved" "$work_name" \
adapter/loop.sh:340:    codex_home=$HOME/.codex
adapter/loop.sh:343:  if [ -d "$codex_home/sessions" ]; then
adapter/loop.sh:344:    can_write_dir "$codex_home/sessions" \
adapter/loop.sh:345:      || reason="missing write permission for Codex sessions directory $codex_home/sessions"
adapter/loop.sh:346:  elif [ -d "$codex_home" ]; then
adapter/loop.sh:347:    can_write_dir "$codex_home" \
adapter/loop.sh:348:      || reason="missing write permission to create Codex sessions under $codex_home"
adapter/loop.sh:350:    codex_parent="$(dirname "$codex_home")"
adapter/loop.sh:351:    can_write_dir "$codex_parent" \
adapter/loop.sh:352:      || reason="missing write permission to create Codex home $codex_home under $codex_parent"
adapter/loop.sh:359:  msg="preflight passed: Codex binary is present and $codex_home can hold session state"
adapter/loop.sh:2119:      printf 'real reviewer subprocess completed through codex exec with literal approval never and literal sandbox read-only'
adapter/loop.sh:2183:  command -v "$CODEX_BIN" >/dev/null 2>&1 \
adapter/loop.sh:2184:    || die "acceptance review cannot spawn Codex reviewers: Codex binary '$CODEX_BIN' is not on PATH"
adapter/loop.sh:2195:  CODEX_CMD=("$CODEX_BIN" -a never -s read-only -C "$ROOT")
adapter/loop.sh:2196:  codex_add_review_route_args
adapter/loop.sh:2197:  ACCEPTANCE_CMD=("${CODEX_CMD[@]}")
adapter/loop.sh:2251:    printf 'Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.\n'
adapter/loop.sh:2549:codex_sandbox_for_tools() {
adapter/loop.sh:2551:    *Edit*|*Write*) printf '%s' "$CODEX_WRITE_SANDBOX" ;;
adapter/loop.sh:2552:    *)              printf '%s' "$CODEX_READ_SANDBOX" ;;
adapter/loop.sh:2556:codex_thread_id() {
adapter/loop.sh:2564:codex_json_string_value() {
adapter/loop.sh:2573:codex_progress_detail() {
adapter/loop.sh:2585:record_codex_progress_line() {
adapter/loop.sh:2587:  type="$(codex_json_string_value "$line" type)"
adapter/loop.sh:2589:    msg="codex output: $(short_message "$line")"
adapter/loop.sh:2591:    loop_event codex-output "$gate" running "$msg"
adapter/loop.sh:2601:    thread_id="$(codex_json_string_value "$line" thread_id)"
adapter/loop.sh:2602:    msg="codex thread discovered"
adapter/loop.sh:2605:    loop_event codex-thread "$gate" running "$msg"
adapter/loop.sh:2610:  detail="$(codex_progress_detail "$line")"
adapter/loop.sh:2614:  loop_event codex-event "$gate" running "$msg"
adapter/loop.sh:2618:codex_model_token_ok() {
adapter/loop.sh:2623:codex_effort_token_ok() {
adapter/loop.sh:2628:validate_codex_model_var() {
adapter/loop.sh:2631:  codex_model_token_ok "$value" || die "$var must be a single model token"
adapter/loop.sh:2634:validate_codex_effort_var() {
adapter/loop.sh:2637:  codex_effort_token_ok "$value" || die "$var must be a single effort token"
adapter/loop.sh:2640:codex_add_model_and_effort_args() {
adapter/loop.sh:2642:  validate_codex_model_var "$model_var" "$model"
adapter/loop.sh:2643:  validate_codex_effort_var "$effort_var" "$effort"
adapter/loop.sh:2644:  [ -n "$model" ] && CODEX_CMD+=(-m "$model")
adapter/loop.sh:2645:  [ -n "$effort" ] && CODEX_CMD+=(-c "model_reasoning_effort=\"$effort\"")
adapter/loop.sh:2649:codex_route_model_and_effort() {
adapter/loop.sh:2653:      model="${CODEX_BUILDER_MODEL:-gpt-5.5}"
adapter/loop.sh:2654:      effort="${CODEX_BUILDER_EFFORT:-xhigh}"
adapter/loop.sh:2655:      codex_add_model_and_effort_args "$model" "$effort" CODEX_BUILDER_MODEL CODEX_BUILDER_EFFORT
adapter/loop.sh:2658:      model="${CODEX_STRONG_BUILDER_MODEL:-${CODEX_REVIEW_MODEL:-${CODEX_MODEL:-}}}"
adapter/loop.sh:2659:      effort="${CODEX_STRONG_BUILDER_EFFORT:-${CODEX_REVIEW_EFFORT:-xhigh}}"
adapter/loop.sh:2660:      codex_add_model_and_effort_args "$model" "$effort" CODEX_STRONG_BUILDER_MODEL CODEX_STRONG_BUILDER_EFFORT
adapter/loop.sh:2663:      model="${CODEX_MODEL:-}"
adapter/loop.sh:2664:      effort="${CODEX_EFFORT:-}"
adapter/loop.sh:2665:      codex_add_model_and_effort_args "$model" "$effort" CODEX_MODEL CODEX_EFFORT
adapter/loop.sh:2668:      die "unknown Codex route: $route"
adapter/loop.sh:2673:codex_cmd_prefix() {
adapter/loop.sh:2675:  CODEX_CMD=("$CODEX_BIN" -a "$CODEX_APPROVAL" -s "$sandbox" -C "$ROOT")
adapter/loop.sh:2676:  codex_route_model_and_effort "$route"
adapter/loop.sh:2677:  [ -n "${CODEX_PROFILE:-}" ] && CODEX_CMD+=(-p "$CODEX_PROFILE")
adapter/loop.sh:2681:run_codex_gate() {
adapter/loop.sh:2683:  local sandbox final combined codex_events gate_output cmd_status pipeline_status msg
adapter/loop.sh:2685:  sandbox="$(codex_sandbox_for_tools "$tools")"
adapter/loop.sh:2686:  final="$(mktemp "${TMPDIR:-/tmp}/hypercore-loop-codex-$gate-final.XXXXXX")"
adapter/loop.sh:2688:  codex_events="$LOOP_RUN_DIR/events-codex-$gate.jsonl"
adapter/loop.sh:2690:  codex_cmd_prefix "$sandbox" "$route"
adapter/loop.sh:2693:    start)  CODEX_CMD+=(exec --json -o "$final" -) ;;
adapter/loop.sh:2697:  msg="starting $gate gate with Codex sandbox $sandbox"
adapter/loop.sh:2720:      "$(json_string "$gate")" "$(json_string "$route")" "$cmd_status" > "$codex_events"
adapter/loop.sh:2721:    printf '%q ' "${CODEX_CMD[@]}"; printf '<<< stdin: %q\n' "$combined"
adapter/loop.sh:2724:    loop_event codex-thread "$gate" running "fake builder session: $PHASE_TWO_SESSION_ID"
adapter/loop.sh:2741:    printf '{"type":"dry-run","gate":%s,"mode":%s}\n' "$(json_string "$gate")" "$(json_string "$mode")" > "$codex_events"
adapter/loop.sh:2742:    printf '%q ' "${CODEX_CMD[@]}"; printf '<<< stdin: %q\n' "$combined"
adapter/loop.sh:2744:      PHASE_TWO_SESSION_ID=dry-run-codex-session
adapter/loop.sh:2745:      loop_event codex-thread "$gate" running "dry-run Codex thread: $PHASE_TWO_SESSION_ID"
adapter/loop.sh:2747:    GATE_OUTPUT="(dry-run) $gate gate final output would be written by Codex."
adapter/loop.sh:2755:  : > "$codex_events"
adapter/loop.sh:2757:  printf '%s' "$combined" | "${CODEX_CMD[@]}" | while IFS= read -r line || [ -n "$line" ]; do
adapter/loop.sh:2758:    printf '%s\n' "$line" >> "$codex_events"
adapter/loop.sh:2759:    record_codex_progress_line "$gate" "$line"
adapter/loop.sh:2769:      GATE_OUTPUT="codex exec exited $cmd_status"
adapter/loop.sh:2772:    msg="gate $gate failed: codex exec exited $cmd_status"
adapter/loop.sh:2781:    PHASE_TWO_SESSION_ID="$(codex_thread_id < "$codex_events")"
adapter/loop.sh:2783:      || { rm -f "$final"; die "could not read codex thread id from gate $gate"; }
adapter/loop.sh:2784:    loop_state_write "$gate" running "codex thread discovered: $PHASE_TWO_SESSION_ID"
adapter/loop.sh:2803:    codex) run_codex_gate "$gate" "$tools" "$mode" "$sid" "$prompt" "$sys" "$route" "$allow_failure" ;;
adapter/loop.sh:2804:    *) die "unsupported LOOP_HARNESS: $LOOP_HARNESS (only codex is supported)" ;;
adapter/loop.sh:3001:  local model=${CODEX_REVIEW_MODEL:-}
adapter/loop.sh:3002:  local effort=${CODEX_REVIEW_EFFORT:-xhigh}
adapter/loop.sh:3003:  validate_codex_model_var CODEX_REVIEW_MODEL "$model"
adapter/loop.sh:3004:  validate_codex_effort_var CODEX_REVIEW_EFFORT "$effort"
adapter/loop.sh:3007:codex_add_review_route_args() {
adapter/loop.sh:3008:  local model=${CODEX_REVIEW_MODEL:-}
adapter/loop.sh:3009:  local effort=${CODEX_REVIEW_EFFORT:-xhigh}
adapter/loop.sh:3011:  [ -n "$model" ] && CODEX_CMD+=(-m "$model")
adapter/loop.sh:3012:  [ -n "$effort" ] && CODEX_CMD+=(-c "model_reasoning_effort=\"$effort\"")
adapter/loop.sh:3092:  command -v "$CODEX_BIN" >/dev/null 2>&1 \
adapter/loop.sh:3093:    || die "review cannot spawn Codex reviewers: Codex binary '$CODEX_BIN' is not on PATH"
adapter/loop.sh:3108:  CODEX_CMD=("$CODEX_BIN" -a never -s read-only -C "$ROOT")
adapter/loop.sh:3109:  codex_add_review_route_args
adapter/loop.sh:3110:  REVIEW_CMD=("${CODEX_CMD[@]}")
adapter/loop.sh:3209:    printf 'Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.\n'
adapter/loop.sh:3463:  [ "$LOOP_HARNESS" = codex ] \
adapter/loop.sh:3464:    || die "unsupported LOOP_HARNESS: $LOOP_HARNESS (only codex is supported)"
check.sh:103:      "adapter/codex.md",
check.sh:105:      "adapter/codex-mounted.md",
check.sh:113:    my $product = qr/(?<![A-Za-z0-9_])(?:codex|claude|opus|gpt-[0-9][A-Za-z0-9._-]*|CODEX_[A-Za-z0-9_]*)(?![A-Za-z0-9_])/i;
check.sh:155:the Codex review floor is named in a contract statement.
check.sh:164:    'product token "Codex" is outside a whitelisted materialization pointer' \
check.sh:171:the current root harness adapter is materialized as `adapter/codex.md`.
check.sh:184:- **adapter** -- the binding between a harness and the loop, materialized through `adapter/codex.md`.
check.sh:188:- **home** -- home currently mounts codex-cockpit.
check.sh:221:  require_text "$root/adapter/codex.md" \
check.sh:222:    "to the interactive Codex harness that loaded this adapter" \
check.sh:225:    'CODEX_REVIEW_EFFORT:-xhigh' \
check.sh:228:    'CODEX_BUILDER_MODEL:-gpt-5.5' \
check.sh:231:    'CODEX_BUILDER_EFFORT:-xhigh' \
check.sh:300:      -o -path "$root/.codex" \
check.sh:301:      -o -path "$root/.claude" \
check.sh:314:          -o -path "*/.codex" \
check.sh:315:          -o -path "*/.claude" \
check.sh:1069:  printf 'fixture crash stderr from codex exec\npartial stdout before failure\n' > "$fake_review/red-team"
check.sh:1086:  require_text "$review" "fixture crash stderr from codex exec" \
check.sh:1406:    CODEX_STRONG_BUILDER_MODEL="gpt-5.3-codex" \
check.sh:1412:  require_text "$tmp/retry-escalation.out" "-m gpt-5.5" \
check.sh:1413:    "fast builder dry-run command uses the gpt-5.5 builder default"
check.sh:1416:  require_text "$tmp/retry-escalation.out" "-m gpt-5.3-codex" \
check.sh:1588:    "AGENTS.md points to the mounted-node Codex entrypoint" \
check.sh:1589:    "home CLI explains the mounted Codex entrypoint link"
check.sh:1648:    "$root/adapter/codex-mounted.md" \
check.sh:1649:    "greenfield AGENTS.md points at the root-managed mounted Codex entrypoint"
check.sh:1730:        "$root/adapter/codex-mounted.md" \
check.sh:1731:        "$label AGENTS.md points at the root-managed mounted Codex entrypoint"
check.sh:1892:require_text "$root/adapter/codex.md" \
check.sh:1893:  "to the interactive Codex harness that loaded this adapter" \
check.sh:1895:require_text "$root/adapter/codex.md" \
check.sh:1936:[ -f "$root/adapter/codex.md" ] && ok "adapter/codex.md exists" \
check.sh:1937:  || bad "adapter/codex.md missing"
check.sh:1938:[ -f "$root/adapter/codex-mounted.md" ] && ok "adapter/codex-mounted.md exists" \
check.sh:1939:  || bad "adapter/codex-mounted.md missing"
check.sh:1965:  "AGENTS.md routes Codex into the methodology prose"
check.sh:1968:  "AGENTS.md routes Codex into the loop"
check.sh:2115:require_text "$root/adapter/codex.md" \
check.sh:2117:  "Codex adapter describes phase one as design-phase collaboration"
check.sh:2118:require_text "$root/adapter/codex.md" \
check.sh:2120:  "Codex adapter classifies the request surface"
check.sh:2121:require_text "$root/adapter/codex.md" \
check.sh:2123:  "Codex adapter rejects simplicity-based loop bypass"
check.sh:2124:require_text "$root/adapter/codex.md" \
check.sh:2126:  "Codex adapter carries teach-back before route"
check.sh:2127:require_text "$root/adapter/codex.md" \
check.sh:2129:  "Codex adapter carries alternative framing before route"
check.sh:2130:require_text "$root/adapter/codex.md" \
check.sh:2132:  "Codex adapter carries reversibility classification"
check.sh:2133:require_text "$root/adapter/codex.md" \
check.sh:2135:  "Codex adapter names the root review helper"
check.sh:2136:require_text "$root/adapter/codex.md" \
check.sh:2138:  "Codex adapter names the base review roster"
check.sh:2139:require_text "$root/adapter/codex.md" \
check.sh:2141:  "Codex adapter makes optional reviewers advisory"
check.sh:2142:require_text "$root/adapter/codex.md" \
check.sh:2144:  "Codex adapter names the root direction helper"
check.sh:2145:require_text "$root/adapter/codex.md" \
check.sh:2147:  "Codex adapter blocks machine-authored direction"
check.sh:2148:require_text "$root/adapter/codex.md" \
check.sh:2150:  "Codex adapter names neutral direction options"
check.sh:2151:require_text "$root/adapter/codex.md" \
check.sh:2153:  "Codex adapter carries the operator-gate marker"
check.sh:2154:require_text "$root/adapter/codex.md" \
check.sh:2156:  "Codex adapter names the terminal liveness channel"
check.sh:2157:require_text "$root/adapter/codex.md" \
check.sh:2159:  "Codex adapter ties direction to selected option text"
check.sh:2160:require_text "$root/adapter/codex.md" \
check.sh:2162:  "Codex adapter carries work-number sign-off confirmation"
check.sh:2163:require_text "$root/adapter/codex.md" \
check.sh:2165:  "Codex adapter does not overclaim the operator gate"
check.sh:2166:reject_text "$root/adapter/codex.md" \
check.sh:2168:  "Codex adapter no longer presents argument-transcribed direction as primary"
check.sh:2169:require_text "$root/adapter/codex.md" \
check.sh:2171:  "Codex adapter carries acceptance condition"
check.sh:2172:require_text "$root/adapter/codex.md" \
check.sh:2174:  "Codex adapter carries observable acceptance"
check.sh:2175:require_text "$root/adapter/codex.md" \
check.sh:2177:  "Codex adapter carries excluded interpretation"
check.sh:2178:require_text "$root/adapter/codex.md" \
check.sh:2180:  "Codex adapter keeps phase two tied to the signed frame directory"
check.sh:2181:require_text "$root/adapter/codex.md" \
check.sh:2183:  "Codex adapter carries one-way implementation acceptance"
check.sh:2184:require_text "$root/adapter/codex.md" \
check.sh:2186:  "Codex adapter carries structured phase-two acceptance artifacts"
check.sh:2187:require_text "$root/adapter/codex.md" \
check.sh:2189:  "Codex adapter carries concurrent tier-two panel execution"
check.sh:2190:reject_text "$root/adapter/codex.md" \
check.sh:2192:  "Codex adapter no longer describes one resumed phase-two thread"
check.sh:2193:require_text "$root/adapter/codex.md" \
check.sh:2195:  "Codex adapter carries the decision surface"
check.sh:2196:require_text "$root/adapter/codex.md" \
check.sh:2198:  "Codex adapter carries node-local work wording"
check.sh:2199:require_text "$root/adapter/codex.md" \
check.sh:2201:  "Codex adapter describes adoption or shelving"
check.sh:2202:require_text "$root/adapter/codex.md" \
check.sh:2204:  "Codex adapter names the root sign-off helper"
check.sh:2205:require_text "$root/adapter/codex-mounted.md" \
check.sh:2207:  "mounted Codex entrypoint identifies root-managed adapter material"
check.sh:2208:require_text "$root/adapter/codex-mounted.md" \
check.sh:2210:  "mounted Codex entrypoint names the governing root"
check.sh:2211:require_text "$root/adapter/codex-mounted.md" \
check.sh:2213:  "mounted Codex entrypoint tells Codex to read local intent first"
check.sh:2214:require_text "$root/adapter/codex-mounted.md" \
check.sh:2216:  "mounted Codex entrypoint routes through home resolve"
check.sh:2217:require_text "$root/adapter/codex-mounted.md" \
check.sh:2219:  "mounted Codex entrypoint routes work through the resolved mount path"
check.sh:2220:require_text "$root/adapter/codex-mounted.md" \
check.sh:2221:  "$root/adapter/codex.md" \
check.sh:2222:  "mounted Codex entrypoint points to the root adapter"
check.sh:2223:require_text "$root/adapter/codex-mounted.md" \
check.sh:2225:  "mounted Codex entrypoint keeps local checks as proof only"
check.sh:2226:require_text "$root/adapter/codex-mounted.md" \
check.sh:2228:  "mounted Codex entrypoint rejects fabrication"
check.sh:2236:  'LOOP_HARNESS="${LOOP_HARNESS:-codex}"' \
check.sh:2237:  "loop defaults phase two to Codex"
check.sh:2261:  "loop has a phase-two Codex preflight"
check.sh:2365:  'CODEX_CMD=("$CODEX_BIN" -a never -s read-only -C "$ROOT")' \
check.sh:2368:  'codex_add_review_route_args' \
check.sh:2371:  'ACCEPTANCE_CMD=("${CODEX_CMD[@]}")' \
check.sh:2381:  "loop validates CODEX_REVIEW_MODEL"
check.sh:2383:  'CODEX_REVIEW_EFFORT:-xhigh' \
check.sh:2386:  'CODEX_BUILDER_MODEL:-gpt-5.5' \
check.sh:2387:  "loop defaults fast builders to gpt-5.5 until the two-step plan/build lands"
check.sh:2389:  'CODEX_BUILDER_EFFORT:-xhigh' \
check.sh:2392:  'CODEX_STRONG_BUILDER_MODEL' \
check.sh:2575:  'command -v "$CODEX_BIN"' \
check.sh:2576:  "loop preflight checks the Codex binary"
check.sh:2578:  'CODEX_HOME' \
check.sh:2579:  "loop preflight resolves Codex home"
check.sh:2581:  'can_write_dir "$codex_home/sessions"' \
check.sh:2582:  "loop preflight checks Codex session write permission"
check.sh:2590:  'events-codex-$gate.jsonl' \
check.sh:2591:  "loop stores the raw Codex JSON event stream per gate"
check.sh:2594:  "loop streams Codex JSON events while the gate runs"
check.sh:2596:  'record_codex_progress_line "$gate" "$line"' \
check.sh:2597:  "loop prints progress from streamed Codex events"
check.sh:2600:  "loop no longer buffers the Codex JSON stream before progress"
check.sh:2704:for file in "$root/README.md" "$root/hypercore.md" "$root/adapter/codex.md" \
check.sh:2705:  "$root/adapter/codex-mounted.md" \

exec
/bin/bash -lc "sed -n '1,220p' intent/collaboration.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# collaboration

operator-machine collaboration is a first-class methodology concern, separate from the loop mechanics that enforce it.
collaboration is the working relation by which operator and machine keep the work scrutable, sound, and fast across memoryless sessions.
effective collaboration is complementarity, not maximal automation: the operator sets purpose, constraints, acceptance, and open direction; the machine searches, synthesizes, drafts, executes, checks, and settles only what the intent and operator leave open.
collaboration keeps common ground recoverable without treating field count as proof of collaboration quality.
phase one is an arc: understanding before route, scrutiny sized by reversibility, operator direction, lean recoverability, and sign-off.
the phase-one collaborator is the harness role that drives orient and frame: it carries
operator-facing judgment, surfaces understanding and options, and frames the signed route.
phase-one corpus-throughput work -- research, the orient corpus read, and the sweep map --
may be delegated by the collaborator when written ground preserves accountability and
operator direction.
before a route is written, the machine gives a teach-back, at least one alternative framing, information-gain questions, and a reversibility classification.
one-way work requires distinct-route scrutiny before route settlement, including a mechanically spawned base review roster.
the base review roster is `contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`; optional reviewers are additive and advisory only.
optional reviewers cannot override, outvote, average away, or dilute unresolved base-roster or red-team flags.
for one-way work, the strong review floor that scrutinizes a frame is independent of the
collaborator that framed it; the framer is not its own witness.
review quality is not proved by artifact scanning; review artifacts record structured signal, unresolved flags, and disposition.
direction and sign-off are the two anchored operator acts in phase one, and the machine performs neither for itself.
operator direction is substantive: it records a selected route, constraint, or explicit delegation with `direction-by:`.
sign-off attests informed expectation and understanding, but it still requires the complete lean frame and required phase-one acts; it is not earned by bloated field scanning.
a legitimate helper-written operator act crosses an operator gate that reads its decisive token from `/dev/tty` and records `operator-gate: tty`, staying simple enough that the operator confirms rather than transcribes.
direction is a real operator choice: when the frame offers neutral, materially distinct numbered options, the helper copies the operator's selected option verbatim into `direction.md`; the machine may draft options but never chooses one for the operator.
sign-off is informed at the moment of attestation: the helper renders the signed frame's route, acceptance condition, observable acceptance, excluded interpretation, reversibility, and target segments before it reads the confirming token.
`operator-gate: tty` is a terminal-liveness marker for the helper path that the default machine command path lacks; it is not cryptographic non-repudiation, tamper-evidence, file integrity, or proof an operator rather than a deliberately allocated terminal answered.
collaboration calibrates reliance: the machine makes its capabilities, limits, uncertainty, evidence, and failure modes visible enough for the operator to judge when to rely on it, challenge it, redirect it, or stop it.
collaboration preserves operator agency without wasting motion: the machine asks before settling open direction or choices the artifacts cannot ground, and proceeds without interruption when the signed frame, intent, and checks give it enough written ground.
phase-two acceptance is an operator-reliance concern, not only loop mechanics: before one-way adoption stamps the operator's endorsement, the machine makes the built result independently checkable against what the operator signed.
implementation-acceptance scrutiny is independent of the builder's attestation; the builder does not become the witness that proves its own one-way archive.
unresolved implementation-acceptance `FLAG`s are feedback material: they block archive and surface to the operator rather than being self-cleared, averaged away, outvoted, or treated as warnings.
implementation-acceptance signal is legible: a required acceptance verdict carries a parseable `PASS` or `FLAG` plus rationale and concrete evidence enough for the operator or a later machine to act on a `FLAG`; uncertainty still flags, and legibility makes the door actionable without weakening it.
build retry is bounded proof-floor recovery, not a structural re-decision: a builder may re-attempt a failed unit within the signed route, but structural mismatches, tier-two `FLAG`s, and an exhausted escalation budget still surface to the operator rather than being retried away.
collaboration treats feedback as material: operator corrections, machine-discovered facts, failed checks, and sweep flags become intent, proof, machine statements, or debt rather than remaining transient chat.
collaboration degrades gracefully: when written ground is insufficient, the machine records the blocker and decision surface and stops rather than fabricating content.

## machine
phase-two handoff state is written as common ground for the operator and later tooling:
the addressed work's current or recent gate, current unit, status, harness session id, latest
message, failure reason, event history, run artifact paths, and phase-two acceptance
artifact paths are recoverable from loop state files.

---
endorsed by qqp-dev

exec
/bin/bash -lc "sed -n '1,260p' intent/loop.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# loop

every work node that needs adoption or shelving goes through five gates: orient, frame,
implement, check, archive.
governed work is not optional by perceived simplicity, file count, risk, or convenience
when it changes governed material or needs adoption or shelving.
orient and frame are the design phase: understanding, scrutiny, operator direction, route
framing, and sign-off happen there before phase two begins.
direction and review are phase-one acts or artifacts inside orient and frame, not new loop
gates.
when a work node's direction is still open, the machine states the problem, constraints,
decision surface, reversibility, and information needed from the operator before settling
the route.
before a route is written, governed work has substantive operator direction recorded in
`intent/frame/direction.md`.
new work that needs route selection carries `intent/frame/options.md` with neutral,
materially distinct numbered options, and the operator's direction is one option selected
through `/dev/tty` and recorded with `operator-gate: tty`.
direction and sign-off for new work are terminal-gated operator acts; the `operator-gate:`
token is `tty` today and the field stays open to a later keyed scheme such as `hmac:<...>`.
one-way work has `intent/frame/review.md` before route framing and sign-off; two-way work
skips review unless the operator requests it.
before sign-off, a new work frame carries lean recoverability fields: addressed node,
node-local work name, target segments, work in flight, problem, constraints, decision
surface or open direction, reversibility, route, acceptance condition, observable
acceptance, excluded interpretation, proof state, sweep, and adoption or shelving claim.
`observable acceptance` names the concrete command, state, check, or externally inspectable
condition that phase-two acceptance can test.
`excluded interpretation` names what the work must not mean.
implementation autonomy begins after sign-off: phase two builds from the signed frame in
green proof-advancing units, and stops when the frame is incomplete, a check fails, or
required implementation acceptance returns `FLAG`.
orient: read the intent documents, the work in flight across the node tree, and the
material's conventions; search the web for what you do not know; ask the operator what the
artifacts cannot tell you; do not guess.
frame: write enough of the addressed work node's intent and material to make the proposed
work scrutable, including proposed parent amendments where the work needs them, and run the
sweep over the whole corpus and work in flight across the node tree.
implement: build in proof-advancing units from the signed frame.
an implementation unit is the smallest proof-advancing delta that leaves `./check.sh`
green; units are vertical slices, so statements, material, and checks land together when
the work requires all three.
check: prove each statement with checks on the material, and run the phase-two acceptance
scrutiny required by the signed frame and reversibility.
`./check.sh` is green at every phase-two unit boundary and before any acceptance verdict
or archive fold is trusted.
after each implementation unit, a fresh independent read-only implementation-acceptance
reviewer reads the signed frame, unit proof obligation, unit diff, and lean unit handoff,
then returns a structured verdict: exactly one `PASS` or `FLAG` with required rationale and
concrete evidence.
for one-way work, a required tier-two implementation-acceptance panel runs before archive,
its lenses started concurrently after every required tier-one artifact is clean; two-way
work does not run that panel unless later intent explicitly requires it.
the one-way tier-two panel lenses are `whole-acceptance-conformance`, `proof-integrity`,
`independent-coherence`, `security-permissions`, and `red-team`.
the `independent-coherence` lens carries the semantic sweep judgement for one-way archive;
this does not solve the deeper semantic-indexing problem.
missing, malformed, nonzero, unsupported-source, evidence-free, or non-`PASS`/`FLAG`
acceptance reviewer output counts as `FLAG`.
acceptance artifacts record their source as real reviewer, dry-run/self-test, or
fake/self-test; real execute refuses fake acceptance, and real archive refuses dry-run or
fake-source required acceptance.
phase-one labor may be routed by role: the collaborator drives operator-facing orient and
frame work, corpus-throughput work may be delegated, and the collaborator may differ from
the phase-two executor harness while phase-one review stays on the strong review floor.
the collaborator role defaults to the interactive harness that loaded the adapter.
phase-two builders may be routed separately from reviewers through a fast-builder model
knob, while tier-one acceptance, tier-two acceptance, and phase-one review stay on the
strong review floor; the fast-builder default is held at the strong model until the
two-step plan/build work lands.
a unit build attempts the fast builder first, retries a failed unit up to three fast
attempts when `./check.sh` or tier-one acceptance fails, escalates that unit to the strong
builder after the fast budget, and returns to the operator if the strong attempt still
fails.
execute is resumable from the signed frame and on-disk artifacts: a passed unit's build and
tier-one evidence is reused only when its cache key still matches the signed frame, unit
proof obligation, relevant prior-unit state, loop implementation version, recorded diff, and
green mechanical-check evidence, and a cache miss rebuilds the unit and invalidates
downstream unit evidence.
unresolved required tier-one or tier-two `FLAG`s halt phase two before archive; the active
work node remains in flight for the operator.
the checks re-run for every statement, not only the ones a work node touched.
drift is a check that falls without work meaning to break it, and it surfaces wherever it
happens.
archive: adopt or shelve the work according to the signed frame.
one-way archive cannot fold or stamp until required implementation-acceptance artifacts
are present and clean.
adoption folds accepted child statements and material into the parent, stamps each touched
segment's foot with this operator, and records the work node as adopted history.
shelving records the work node as shelved history without changing parent truth.
large work breaks into related work at frame, and related work is an ordinary work node in
the node it alters.
a coordinating work node remains responsible for its plan: before it adopts or shelves,
related unfinished work is either resolved in its own node or carried as explicit debt.
two work nodes touching the same intent document is a smell, caused by concurrency or
orthogonality.
concurrent work is sequenced by the loop's gates: first to adopt wins, and later work builds
on the in-flight or adopted material it reads across the node tree.
an orthogonal collision is fixed in the taxonomy, preferring more documents over more
mechanism.

## machine
a work address names the addressed node and one node-local work name in that node.
when no node is named, the root node is assumed.
`loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node.
`loop.sh start <work-name>` creates a work node directly under the addressed node's
corpus.
`loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work and
act only on that addressed work.
`loop.sh execute <work-name>` exposes phase-two run state for the addressed work while it
runs and after recent failure or completion, including the active gate, status, harness
session id, latest message, event history, and run artifact paths.
before launching the first phase-two executor gate, `loop.sh execute <work-name>` checks
that the configured executor binary is present and that executor home/session state is
writable; a failed preflight records failed run state and stops before the executor
session starts.
`loop.sh status <work-name>` reports the addressed work's current phase and, for
non-historical work with phase-two state, the current or recent run's gate, status, state
path, event path, and latest message; `loop.sh status --json <work-name>` renders the same
run state for tooling.
from the root, `./signoff` invokes the root loop sign-off gate and preserves any explicit
arguments it receives.
`loop.sh signoff <work-name> <operator>` remains the explicit sign-off form, and for new
work it renders a concise frame-derived attestation brief through `/dev/tty`, requires the
work number as the confirming token, and writes `signed-off-by:`, `signed-off-at:`, and
`operator-gate: tty`.
`loop.sh signoff` infers the work name only when exactly one frame-complete unsigned work
node exists in the addressed node; otherwise it blocks and asks for `<work-name>`.
`loop.sh signoff` infers the operator from `HYPERCORE_OPERATOR` when set, otherwise from
the addressed node's current intent foot endorsements when exactly one operator is present;
otherwise it blocks and asks for `<operator>`.
from the root, `./direction` invokes `loop.sh direct` and preserves explicit arguments.
`loop.sh direct [<work-name> [<operator>]]` with no direction form renders the neutral
numbered options from `intent/frame/options.md` through `/dev/tty` and copies the operator's
selected option verbatim into `intent/frame/direction.md`, accepting a bare number, `n` for
none-of-these, or `q` for abort.
the explicit `loop.sh direct ... --route|--constraint|--delegate <text-or->` form is an
admin form that cannot record gated operator direction for new work; only the narrow
gate-introducing bootstrap work may record direction without the numbered selection.
`loop.sh direct` rejects empty or placeholder direction, multiple direction forms, an
existing valid direction artifact, a malformed existing direction artifact, and direction
after route content is already present.
`intent/frame/options.md` records numbered options with `kind`, `summary`, `reversibility`,
and `tradeoff`, plus `none` and `abort` rejection choices, and carries no recommendation
marker.
`direction.md` contains `direction-by:`, `direction-given-at:`, `operator-gate: tty`, and
exactly one non-placeholder `selected-route:`, `constraint:`, or `delegation:` copied from a
numbered option.
`operator-gate:` is a B-ready gate token, either `tty` or a reserved `<scheme>:<value>` such
as a later `hmac:<...>`, and only the `tty` liveness scheme is implemented.
from the root, `./review` invokes `loop.sh review` and preserves explicit arguments.
`loop.sh review <work-name> [--add <role>]...` seats the base review roster and any valid
optional complete-roster roles, then writes `intent/frame/review.md`.
new work frame completeness is checked from the canonical `intent/frame/frame.md` only;
`direction.md`, `review.md`, and `signoff.md` do not satisfy ordinary frame fields.
new work frame completeness requires these recoverable fields: addressed node,
node-local work name, target segments, work in flight, problem, constraints, decision
surface or open direction, reversibility, route, acceptance condition, observable
acceptance, excluded interpretation, proof state, sweep, and adoption or shelving claim.
`reversibility:` is parsed as exactly `one-way` or `two-way`.
`loop.sh start <work-name>` scaffolds `intent/frame/frame.md` with the lean fields.
`loop.sh frame` and `loop.sh signoff` block new work whose frame is incomplete, whose
direction is absent or malformed, whose direction appears retrospective, whose new-work
direction or sign-off lacks the `operator-gate: tty` marker, or whose one-way frame lacks a
review artifact.
one-way review artifacts record base-role verdicts, unresolved flags, and disposition;
optional reviewer verdicts cannot clear unresolved base-roster or red-team flags.
new work sign-off records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty` in
the work node's `intent/frame/signoff.md`.
`loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
fresh builder session for each unit, and records lean unit handoff, diff, and tier-one
verdict artifacts under the work frame.
`loop.sh execute <work-name>` routes builders through the builder-model knob, defaulting to
the strong model until the two-step plan/build work lands, separately from the strong
review route; it gives each unit a three-attempt fast-builder budget, escalates an
exhausted unit through the strong-builder model knob, and stops for the operator when the
strong builder fails.
`loop.sh execute <work-name>` runs implementation-acceptance reviewers with literal
approval `never` and literal sandbox `read-only`.
`loop.sh execute <work-name>` writes structured acceptance artifacts with a verdict,
rationale, evidence, and a `source:` marker, refuses `HYPERCORE_ACCEPTANCE_FAKE_DIR` outside
dry-run, and lets real archive accept only `source: real-reviewer` required acceptance.
`loop.sh execute <work-name>` caches per-unit build and tier-one evidence under a
signed-frame-derived key, skips unchanged accepted units on rerun, and rebuilds cache misses
while invalidating downstream evidence.
`loop.sh execute <work-name>` treats malformed, evidence-free, or unsupported-source
implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
concurrent one-way tier-two panel before archive.
`loop.sh execute <work-name>` records the addressed work in node-local history after archive.

---
endorsed by qqp-dev

exec
/bin/bash -lc "sed -n '1,220p' intent/adapter.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# adapter

the adapter is the binding between a harness and the methodology: it promises the harness
acts in agreement with the intent and the loop.
a harness begins each session memoryless, reaching the work only through what it loads;
absent the adapter, agreement is left to chance.
the adapter points the harness at the intent and the loop -- the single source of truth --
and drives it through them; pointing alone is a request, agreement is enforced.
the adapter's specifics are a rigid workflow over the loop's gates: each gate's
preconditions must hold before the next is allowed, and a gate whose preconditions fail
blocks rather than warns.
the rigid workflow restates no rule: the gates and their order are the loop, already
intent; the workflow operationalizes them, and where workflow and intent disagree, the
intent wins.
the rigid workflow is interactive through orient and frame as the design phase, and through
sign-off as the human gate: before a route is written, the machine surfaces understanding,
alternative framing, information-gain questions, reversibility, review where required, and
a decision surface for substantive operator direction; after sign-off, implement, check,
and archive run through cleared sessions that re-derive each unit and acceptance review
from the signed frame directory and lean phase-two handoff artifacts alone.
direction and review are phase-one acts or artifacts, not loop gates.
the review roster for one-way phase-one work has a base roster of
`contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`.
the implementation-acceptance reviewer for each phase-two unit is independent and read-only.
the tier-two implementation-acceptance panel for one-way work has required lenses
`whole-acceptance-conformance`, `proof-integrity`, `independent-coherence`,
`security-permissions`, and `red-team`.
the complete optional review roster is `implementation-maintainability`,
`security-permissions`, `operator-ergonomics`, `migration-compatibility`,
`domain-evidence`, and `performance-cost`.
optional reviewers are advisory additions and cannot override, outvote, average away, or
dilute unresolved base-roster or red-team flags.
the adapter classifies the request surface before changing material: ordinary
conversation and read-only inspection may proceed directly, while governed work starts or
continues a work node.
the adapter rejects perceived simplicity, file count, convenience, and low risk as waivers
for governed work.
on request the adapter renders a statement of the intent intelligible in plain language
without altering it.
the adapter carries only what the intent cannot yet reach the harness with -- the order to
read the intent first, and disciplines not yet written as statements; each is a debt,
folded into the intent by later work and then dropped.
an adapter is per harness; one node may be bound by more than one, each loaded by its own
harness.
an adapter binds a harness to a phase; phase one and phase two may bind different harnesses,
and the current materialization binds one harness to both phases.
the phase-one collaborator role defaults to the interactive harness that loaded the
adapter; no orchestrator routing knob is required until a materialization routes that role.
the adapter material is materialized only at the methodology root, with the prose it routes
to, and not in any nested node; a mounted external project may carry a target-local entry
point that links to root-managed adapter material and routes direct-path work back to the
root adapter and loop.
the adapter is not in the orient path; loading it is how orient begins, not part of the
intent it routes to.
the sweep reads the adapter against the intent, so a rule it has come to restate, or a debt
the intent has since absorbed, is caught as drift.

## machine
the current root harness adapter is materialized as `adapter/codex.md`.
the current materialization binds the same harness to phase one and phase two; the
phase-one collaborator is the interactive harness that loaded the adapter.
the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;
the root entry is the harness's mandated pointer, holding nothing, not where the adapter
lives.
a machine working in a nested node under the root is bound by the root `AGENTS.md` in the
project instruction chain from the project root to the current directory, so no node below
the root carries its own adapter material.
a mounted external project may carry a target-local `AGENTS.md` entry point for
direct-path openings; the entry point links to root-managed adapter material and routes
back to the root adapter and loop instead of copying root adapter material into the
mounted node.
the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
over the phase-two executor harness: each implementation unit opens a fresh builder
session from the signed frame, and acceptance reviewers and the archive actor are fresh
sessions rather than resumes of the builder.
the loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
`.hypercore/loop-runs`, with run-local state, event history, raw harness gate streams, gate
final outputs, acceptance artifact paths, and current pointers for the addressed work and
root.
the loop streams inner executor JSON events into the phase-two run state while
printing concise progress, without changing the cleared-session contract.
the loop materializes separate builder and reviewer routing, structured acceptance
artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
one-way tier-two panel, and phase-one review subprocess crash diagnostics.
`adapter/loop.sh` accepts one node-local work name in the addressed node for new work.
the root node is the default addressed node.
`loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node, including a
linked mounted child when `<node-path>` is its mount path.
`loop.sh start <work-name>` creates a work node directly under the addressed node.
`loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work
and act only on that addressed work.
`loop.sh execute <work-name>` records only the addressed node-local work in that node's
history.
the orchestrator creates, signs, executes, and records only addressed node-local work
nodes.
the gate prompts use addressed-node and node-local work wording and point cleared sessions
at the addressed work frame.
the orient gate prompt requires the machine to classify the request surface, name the
addressed node, node-local work name, target segments, work in flight, teach-back,
alternative framing, information-gain questions, reversibility classification, and any
open direction that needs an operator decision before the frame settles a route.
the orient gate prompt tells the machine not to write a route or operator direction.
the frame gate prompt requires addressed node, node-local work name, target segments, work
in flight, problem, constraints, decision surface or open direction, reversibility, route,
acceptance condition, observable acceptance, excluded interpretation, proof state, sweep,
and adoption or shelving claim in `intent/frame/frame.md`.
the frame gate prompt requires substantive `intent/frame/direction.md` before route
framing and requires `intent/frame/review.md` for one-way work.
the frame gate prompt tells the machine not to write operator direction, not to collect
direction retrospectively, and not to let optional reviewer verdicts clear base-roster or
red-team flags.
the adapter prose describes phase one as design-phase collaboration with direction
and review artifacts, while preserving phase two as cleared, heads-down execution from the
signed frame directory and lean phase-two handoff artifacts.
`check.sh` mechanically checks that the gate prompts, adapter prose, loop frame
validation, start scaffolding, direction/review helpers, operator-act gating through
`/dev/tty` with B-ready `operator-gate:` markers and numbered-option direction, review and
acceptance isolation settings, strict frame parsing, phase-two acceptance gating, structured
acceptance legibility, acceptance source markers and fake-source rejection, separate
builder/reviewer routing with bounded retry and strong escalation, resumable execute
caching, the concurrent tier-two panel, the new operator-act and phase-two performance
contract in the `collaboration`, `loop`, and `adapter` segments, and current-material
absence of the retired compatibility route still carry the contract.
each gate's instructions are held in a file in `adapter/gates/`; the harness path includes
them in the executor gate prompt; the orchestrator owns gate order and preconditions and
blocks a gate whose preconditions fail.
sign-off for new work records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty`
in the work-node frame's `intent/frame/signoff.md`; the orchestrator seals phase two until
sign-off is present, and the machine never writes it for itself.
the root `./direction` and `./signoff` helpers are terminal-gated operator-act helpers for
new work: direction selects a numbered option from `intent/frame/options.md` through
`/dev/tty`, and sign-off renders a frame-derived brief and reads the work number through
`/dev/tty`, each writing `operator-gate: tty`; the explicit argument forms are admin forms
that cannot record gated operator acts for new work.
`operator-gate: tty` records that the legitimate helper path crossed the current harness's
terminal-liveness check, which the default machine command path lacks; it does not prove
network isolation, cryptographic non-repudiation, tamper-evidence, file integrity, or that
an operator rather than a deliberately allocated terminal answered.
at the check gate the orchestrator records tier-one implementation acceptance for each
unit, records the concurrent one-way tier-two panel when required, and halts phase two
before archive when required acceptance flags remain unresolved.

---
endorsed by qqp-dev

exec
/bin/bash -lc "sed -n '1,220p' intent/machine-statements/loop.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# loop -- machine statements

a work address names the addressed node and one node-local work name in that node.
when no node is named, the root node is assumed.
`loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node.
`loop.sh start <work-name>` creates a work node directly under the addressed node's
corpus.
`loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work and
act only on that addressed work.
`loop.sh execute <work-name>` exposes phase-two run state for the addressed work while it
runs and after recent failure or completion, including the active gate, status, harness
session id, current unit, latest message, failure reason, event history, run artifact
paths, and phase-two acceptance artifact paths.
before launching the first phase-two executor gate, `loop.sh execute <work-name>` checks
that the configured executor binary is present and that executor home/session state is
writable; a failed preflight records failed run state and stops before the executor
session starts.
`loop.sh status <work-name>` reports the addressed work's current phase and, for
non-historical work with phase-two state, the current or recent run's gate, status, state
path, event path, and latest message; `loop.sh status --json <work-name>` renders the same
run state for tooling.
from the root, `./signoff` invokes the root loop sign-off gate and preserves any explicit
arguments it receives.
`loop.sh signoff <work-name> <operator>` remains the explicit sign-off form, and for new
work it renders a concise frame-derived attestation brief through `/dev/tty`, requires the
work number as the confirming token, and writes `signed-off-by:`, `signed-off-at:`, and
`operator-gate: tty`.
`loop.sh signoff` infers the work name only when exactly one frame-complete unsigned work
node exists in the addressed node; otherwise it blocks and asks for `<work-name>`.
`loop.sh signoff` infers the operator from `HYPERCORE_OPERATOR` when set, otherwise from
the addressed node's current intent foot endorsements when exactly one operator is present;
otherwise it blocks and asks for `<operator>`.
from the root, `./direction` invokes `loop.sh direct` and preserves explicit arguments.
`loop.sh direct [<work-name> [<operator>]]` with no direction form renders the neutral
numbered options from `intent/frame/options.md` through `/dev/tty` and copies the operator's
selected option verbatim into `intent/frame/direction.md`, accepting a bare number, `n` for
none-of-these, or `q` for abort.
the explicit `loop.sh direct ... --route|--constraint|--delegate <text-or->` form is an
admin form that cannot record gated operator direction for new work; only the narrow
gate-introducing bootstrap work may record direction without the numbered selection.
`loop.sh direct` rejects empty or placeholder direction, multiple direction forms, an
existing valid direction artifact, a malformed existing direction artifact, and direction
after route content is already present.
`intent/frame/options.md` records numbered options with `kind`, `summary`, `reversibility`,
and `tradeoff`, plus `none` and `abort` rejection choices, and carries no recommendation
marker.
`direction.md` contains `direction-by:`, `direction-given-at:`, `operator-gate: tty`, and
exactly one non-placeholder `selected-route:`, `constraint:`, or `delegation:` copied from a
numbered option.
`operator-gate:` is a B-ready gate token, either `tty` or a reserved `<scheme>:<value>` such
as a later `hmac:<...>`, and only the `tty` liveness scheme is implemented.
from the root, `./review` invokes `loop.sh review` and preserves explicit arguments.
`loop.sh review <work-name> [--add <role>]...` seats the base review roster and any valid
optional complete-roster roles, then writes `intent/frame/review.md`.
new work frame completeness is checked from the canonical `intent/frame/frame.md` only;
`direction.md`, `review.md`, and `signoff.md` do not satisfy ordinary frame fields.
new work frame completeness requires these recoverable fields: addressed node,
node-local work name, target segments, work in flight, problem, constraints, decision
surface or open direction, reversibility, route, acceptance condition, observable
acceptance, excluded interpretation, proof state, sweep, and adoption or shelving claim.
`reversibility:` is parsed as exactly `one-way` or `two-way`.
`loop.sh start <work-name>` scaffolds `intent/frame/frame.md` with the lean fields.
`loop.sh frame` and `loop.sh signoff` block new work whose frame is incomplete, whose
direction is absent or malformed, whose direction appears retrospective, whose new-work
direction or sign-off lacks the `operator-gate: tty` marker, or whose one-way frame lacks a
review artifact.
one-way review artifacts record base-role verdicts, unresolved flags, and disposition;
optional reviewer verdicts cannot clear unresolved base-roster or red-team flags.
new work sign-off records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty` in
the work node's `intent/frame/signoff.md`.
`loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
fresh builder session for each unit, and records lean unit handoff, diff, and tier-one
verdict artifacts under the work frame.
`loop.sh execute <work-name>` routes builders through the builder-model knob, defaulting to
the strong model until the two-step plan/build work lands, separately from the strong
review route; it gives each unit a three-attempt fast-builder budget, escalates an
exhausted unit through the strong-builder model knob, and stops for the operator when the
strong builder fails.
`loop.sh execute <work-name>` runs implementation-acceptance reviewers with literal
approval `never` and literal sandbox `read-only`.
`loop.sh execute <work-name>` writes structured acceptance artifacts with a verdict,
rationale, evidence, and a `source:` marker, refuses `HYPERCORE_ACCEPTANCE_FAKE_DIR` outside
dry-run, and lets real archive accept only `source: real-reviewer` required acceptance.
`loop.sh execute <work-name>` caches per-unit build and tier-one evidence under a
signed-frame-derived key, skips unchanged accepted units on rerun, and rebuilds cache misses
while invalidating downstream evidence.
`loop.sh execute <work-name>` treats malformed, evidence-free, or unsupported-source
implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
concurrent one-way tier-two panel before archive.
`loop.sh execute <work-name>` records the addressed work in node-local history after archive.

exec
/bin/bash -lc "sed -n '1,180p' intent/machine-statements/adapter.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# adapter -- machine statements

the current root harness adapter is materialized as `adapter/codex.md`.
the current materialization binds the same harness to phase one and phase two; the
phase-one collaborator is the interactive harness that loaded the adapter.
the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;
the root entry is the harness's mandated pointer, holding nothing, not where the adapter
lives.
a machine working in a nested node under the root is bound by the root `AGENTS.md` in the
project instruction chain from the project root to the current directory, so no node below
the root carries its own adapter material.
a mounted external project may carry a target-local `AGENTS.md` entry point for
direct-path openings; the entry point links to root-managed adapter material and routes
back to the root adapter and loop instead of copying root adapter material into the
mounted node.
the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
over the phase-two executor harness: each implementation unit opens a fresh builder
session from the signed frame, and acceptance reviewers and the archive actor are fresh
sessions rather than resumes of the builder.
the loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
`.hypercore/loop-runs`, with run-local state, event history, raw harness gate streams, gate
final outputs, acceptance artifact paths, and current pointers for the addressed work and
root.
the loop streams inner executor JSON events into the phase-two run state while
printing concise progress, without changing the cleared-session contract.
the loop materializes separate builder and reviewer routing, structured acceptance
artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
one-way tier-two panel, and phase-one review subprocess crash diagnostics.
`adapter/loop.sh` accepts one node-local work name in the addressed node for new work.
the root node is the default addressed node.
`loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node, including a
linked mounted child when `<node-path>` is its mount path.
`loop.sh start <work-name>` creates a work node directly under the addressed node.
`loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work
and act only on that addressed work.
`loop.sh execute <work-name>` records only the addressed node-local work in that node's
history.
the orchestrator creates, signs, executes, and records only addressed node-local work
nodes.
the gate prompts use addressed-node and node-local work wording and point cleared sessions
at the addressed work frame.
the orient gate prompt requires the machine to classify the request surface, name the
addressed node, node-local work name, target segments, work in flight, teach-back,
alternative framing, information-gain questions, reversibility classification, and any
open direction that needs an operator decision before the frame settles a route.
the orient gate prompt tells the machine not to write a route or operator direction.
the frame gate prompt requires addressed node, node-local work name, target segments, work
in flight, problem, constraints, decision surface or open direction, reversibility, route,
acceptance condition, observable acceptance, excluded interpretation, proof state, sweep,
and adoption or shelving claim in `intent/frame/frame.md`.
the frame gate prompt requires substantive `intent/frame/direction.md` before route
framing and requires `intent/frame/review.md` for one-way work.
the frame gate prompt tells the machine not to write operator direction, not to collect
direction retrospectively, and not to let optional reviewer verdicts clear base-roster or
red-team flags.
the adapter prose describes phase one as design-phase collaboration with direction
and review artifacts, while preserving phase two as cleared, heads-down execution from the
signed frame directory and lean phase-two handoff artifacts.
`check.sh` mechanically checks that the gate prompts, adapter prose, loop frame
validation, start scaffolding, direction/review helpers, operator-act gating through
`/dev/tty` with B-ready `operator-gate:` markers and numbered-option direction, review and
acceptance isolation settings, strict frame parsing, phase-two acceptance gating, structured
acceptance legibility, acceptance source markers and fake-source rejection, separate
builder/reviewer routing with bounded retry and strong escalation, resumable execute
caching, the concurrent tier-two panel, the new operator-act and phase-two performance
contract in the `collaboration`, `loop`, and `adapter` segments, and current-material
absence of the retired compatibility route still carry the contract.
each gate's instructions are held in a file in `adapter/gates/`; the harness path includes
them in the executor gate prompt; the orchestrator owns gate order and preconditions and
blocks a gate whose preconditions fail.
sign-off for new work records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty`
in the work-node frame's `intent/frame/signoff.md`; the orchestrator seals phase two until
sign-off is present, and the machine never writes it for itself.
the root `./direction` and `./signoff` helpers are terminal-gated operator-act helpers for
new work: direction selects a numbered option from `intent/frame/options.md` through
`/dev/tty`, and sign-off renders a frame-derived brief and reads the work number through
`/dev/tty`, each writing `operator-gate: tty`; the explicit argument forms are admin forms
that cannot record gated operator acts for new work.
`operator-gate: tty` records that the legitimate helper path crossed the current harness's
terminal-liveness check, which the default machine command path lacks; it does not prove
network isolation, cryptographic non-repudiation, tamper-evidence, file integrity, or that
an operator rather than a deliberately allocated terminal answered.
at the check gate the orchestrator records tier-one implementation acceptance for each
unit, records the concurrent one-way tier-two panel when required, and halts phase two
before archive when required acceptance flags remain unresolved.

codex
The current files no longer contain unscoped literal product tokens in the enumerated statement scope; the remaining product text is either material (`adapter/codex.md`, `adapter/loop.sh`, `check.sh`) or whitelisted fenced pointers. I’m testing whether the scanner can be bypassed by a still-readable product-bearing contract claim rather than only checking today’s exact text.
exec
/bin/bash -lc "perl -0ne 'my "'$text=$_; my %allowed=map { $_=>1 } ("adapter/codex.md","AGENTS.md","adapter/codex-mounted.md","adapter/loop.sh"); my @spans; while ($text =~ /`([''^`'"\\n]+)"'`/g) { push @spans, [$-[1], $+[1], $1]; } my $product = qr/(?<![A-Za-z0-9_])(?:codex|claude|opus|gpt-[0-9][A-Za-z0-9._-]*|CODEX_[A-Za-z0-9_]*)(?![A-Za-z0-9_])/i; while ($text =~ /$product/g) { my ($start,$end,$token)=($-[0],$+[0],$&); my $ok=0; for my $span (@spans) { if ($start >= $span->[0] && $end <= $span->[1] && $allowed{$span->[2]}) { $ok=1; last; } } next if $ok; my $prefix=substr($text,0,$start); my $line=1+($prefix =~ tr/'"\\n//); print \""'$ARGV:$line: product token '"\\\""'$token'"\\\" is outside a whitelisted materialization pointer\\n\"; exit 1; }' - <<'EOF'
the strong review floor is Review_GPT-5 and the phase-one route is CodexHarness.
EOF
printf 'status=%s\\n' \""'$?"' in /home/qqp/projects/hypercore
 succeeded in 0ms:
status=0

exec
/bin/bash -lc "perl -0ne 'my "'$text=$_; my %allowed=map { $_=>1 } ("adapter/codex.md","AGENTS.md","adapter/codex-mounted.md","adapter/loop.sh"); my @spans; while ($text =~ /`([''^`'"\\n]+)"'`/g) { push @spans, [$-[1], $+[1], $1]; } my $product = qr/(?<![A-Za-z0-9_])(?:codex|claude|opus|gpt-[0-9][A-Za-z0-9._-]*|CODEX_[A-Za-z0-9_]*)(?![A-Za-z0-9_])/i; while ($text =~ /$product/g) { my ($start,$end,$token)=($-[0],$+[0],$&); my $ok=0; for my $span (@spans) { if ($start >= $span->[0] && $end <= $span->[1] && $allowed{$span->[2]}) { $ok=1; last; } } next if $ok; my $prefix=substr($text,0,$start); my $line=1+($prefix =~ tr/'"\\n//); print \""'$ARGV:$line: product token '"\\\""'$token'"\\\" is outside a whitelisted materialization pointer\\n\"; exit 1; }' - <<'EOF'
the strong review floor is GPT-5 and the phase-one route is Codex.
EOF
printf 'status=%s\\n' \""'$?"' in /home/qqp/projects/hypercore
 succeeded in 0ms:
-:1: product token "GPT-5" is outside a whitelisted materialization pointer
status=1

exec
/bin/bash -lc "perl -0ne 'my "'$text=$_; my %allowed=map { $_=>1 } ("adapter/codex.md","AGENTS.md","adapter/codex-mounted.md","adapter/loop.sh"); my @spans; while ($text =~ /`([''^`'"\\n]+)"'`/g) { push @spans, [$-[1], $+[1], $1]; } my $product = qr/(?<![A-Za-z0-9_])(?:codex|claude|opus|gpt-[0-9][A-Za-z0-9._-]*|CODEX_[A-Za-z0-9_]*)(?![A-Za-z0-9_])/i; while ($text =~ /$product/g) { my ($start,$end,$token)=($-[0],$+[0],$&); my $ok=0; for my $span (@spans) { if ($start >= $span->[0] && $end <= $span->[1] && $allowed{$span->[2]}) { $ok=1; last; } } next if $ok; my $prefix=substr($text,0,$start); my $line=1+($prefix =~ tr/'"\\n//); print \""'$ARGV:$line: product token '"\\\""'$token'"\\\" is outside a whitelisted materialization pointer\\n\"; exit 1; }' - <<'EOF'
the current root harness adapter is materialized as "'`adapter/codex.md`.
EOF
printf '"'status=%s\\n' \""'$?"' in /home/qqp/projects/hypercore
 succeeded in 0ms:
status=0

exec
/bin/bash -lc "sed -n '1,90p' adapter/loop.sh && sed -n '2538,2810p' adapter/loop.sh && sed -n '2988,3120p' adapter/loop.sh && sed -n '3450,3470p' adapter/loop.sh" in /home/qqp/projects/hypercore
 succeeded in 0ms:
#!/usr/bin/env bash
# hypercore loop orchestrator — the adapter's rigid workflow.
#
# Drives one work node through the loop's five gates (intent/loop.md), in two phases
# split at the operator's sign-off:
#
#   phase one — orient, frame — is interactive: the operator and the agent frame the
#     work together, and the operator SIGNS OFF. The machine never signs off itself.
#   phase two — implement, check, archive — runs through cleared, memoryless phase-two
#     sessions that re-derive the work from the written work-node frame alone. Builders
#     work in signed-frame implementation units; independent acceptance sessions check
#     those units before archive can fold one-way work.
#
# The gates and their order are the loop, already intent; this script only operationalizes
# them and blocks a gate whose preconditions fail. It states no rule of its own. Where this
# script and the intent disagree, the intent wins.
#
# Usage:
#   loop.sh [-C <node-path>] start    <work-name>              scaffold the work node; print the orient gate
#   loop.sh [-C <node-path>] direct   [<work-name> [<operator>]]
#                                                               select a neutral direction option
#   loop.sh [-C <node-path>] direct   [<work-name> [<operator>]]
#                                      --route|--constraint|--delegate <text-or->
#                                                               legacy/admin direction text form
#   loop.sh [-C <node-path>] review   <work-name> [--add <role>]...
#                                                               spawn/read the one-way review roster
#   loop.sh [-C <node-path>] frame    <work-name>              check the frame is written and ready for sign-off
#   loop.sh [-C <node-path>] signoff  [<work-name> [<operator>]]
#                                                               record the operator's sign-off (the human gate)
#   loop.sh [-C <node-path>] execute  <work-name> [--dry-run]  run phase two on a cleared session
#   loop.sh [-C <node-path>] status   [--json] <work-name>     print the work node's current phase
#
# Env:
#   LOOP_HARNESS=codex (default and only supported phase-two harness)
#   HYPERCORE_LOOP_STATE_DIR (default: .hypercore/loop-runs under the root)
#   HYPERCORE_OPERATOR (optional sign-off identity when <operator> is omitted)
#   CODEX_BIN (default: codex), CODEX_APPROVAL (default: never)
#   CODEX_WRITE_SANDBOX (default: workspace-write), CODEX_READ_SANDBOX (default: read-only)
#   CODEX_BUILDER_MODEL (default: gpt-5.5 until the two-step plan/build lands), CODEX_BUILDER_EFFORT (default: xhigh)
#   CODEX_STRONG_BUILDER_MODEL (optional strong-builder escalation model)
#   CODEX_STRONG_BUILDER_EFFORT (default: CODEX_REVIEW_EFFORT or xhigh)
#   CODEX_REVIEW_MODEL (optional strong review/acceptance model), CODEX_REVIEW_EFFORT (default: xhigh)
#   HYPERCORE_PHASE_TWO_DRY_RUN_ACCEPTANCE_DIR (optional stable dry-run acceptance/cache dir for self-tests)

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
GATES="$HERE/gates"
NODE="$ROOT"
NODE_REL="."
INTENT_TREE=intent
WORKS="$NODE"
LOOP_HARNESS="${LOOP_HARNESS:-codex}"
HYPERCORE_LOOP_STATE_DIR="${HYPERCORE_LOOP_STATE_DIR:-$ROOT/.hypercore/loop-runs}"
CODEX_BIN="${CODEX_BIN:-codex}"
CODEX_APPROVAL="${CODEX_APPROVAL:-never}"
CODEX_WRITE_SANDBOX="${CODEX_WRITE_SANDBOX:-workspace-write}"
CODEX_READ_SANDBOX="${CODEX_READ_SANDBOX:-read-only}"
DRY_RUN="${DRY_RUN:-0}"
FRAME_REQUIRED_FIELDS=(
  "addressed node"
  "node-local work name"
  "target segments"
  "work in flight"
  "problem"
  "constraints"
  "decision surface or open direction"
  "reversibility"
  "route"
  "acceptance condition"
  "observable acceptance"
  "excluded interpretation"
  "proof state"
  "sweep"
  "adoption or shelving claim"
)
BASE_REVIEW_ROLES=(
  "contract-checkability"
  "soundness-fit"
  "simplicity-fastness"
  "red-team"
)
OPTIONAL_REVIEW_ROLES=(
  "implementation-maintainability"
  "security-permissions"
  "operator-ergonomics"
  "migration-compatibility"
  "domain-evidence"
  "performance-cost"
  printf '"frame_complete":%s,' "$frame_ok"
  printf '"signed_off":%s,' "$signed_ok"
  printf '"phase_two_run":'
  if [ "$ph" != done ] && [ -s "$state" ]; then
    cat "$state"
  else
    printf 'null'
  fi
  printf '}\n'
}

codex_sandbox_for_tools() {
  case "$1" in
    *Edit*|*Write*) printf '%s' "$CODEX_WRITE_SANDBOX" ;;
    *)              printf '%s' "$CODEX_READ_SANDBOX" ;;
  esac
}

codex_thread_id() {
  if command -v jq >/dev/null 2>&1; then
    jq -r 'select(.type=="thread.started") | .thread_id' 2>/dev/null | sed -n '1p'
  else
    sed -nE 's/.*"type":"thread\.started".*"thread_id":"([^"]+)".*/\1/p' | sed -n '1p'
  fi
}

codex_json_string_value() {
  local line=$1 key=$2
  if command -v jq >/dev/null 2>&1; then
    printf '%s\n' "$line" | jq -r --arg key "$key" '.[$key] // empty | if type == "string" then . else empty end' 2>/dev/null
  else
    printf '%s\n' "$line" | sed -nE 's/.*"'"$key"'"[[:space:]]*:[[:space:]]*"([^"]*)".*/\1/p' | sed -n '1p'
  fi
}

codex_progress_detail() {
  local line=$1
  if command -v jq >/dev/null 2>&1; then
    printf '%s\n' "$line" | jq -r '
      (.message? // .msg? // .text? // .command? // .name? // empty)
      | if type == "string" then . else empty end
    ' 2>/dev/null | sed -n '1p'
  else
    printf '%s\n' "$line" | sed -nE 's/.*"(message|msg|text|command|name)"[[:space:]]*:[[:space:]]*"([^"]*)".*/\2/p' | sed -n '1p'
  fi
}

record_codex_progress_line() {
  local gate=$1 line=$2 type detail thread_id msg
  type="$(codex_json_string_value "$line" type)"
  if [ -z "$type" ]; then
    msg="codex output: $(short_message "$line")"
    printf '[phase-two:%s] %s\n' "$gate" "$msg"
    loop_event codex-output "$gate" running "$msg"
    loop_state_write "$gate" running "$msg"
    return
  fi

  case "$type" in
    *delta*|*.delta|token.count) return ;;
  esac

  if [ "$type" = "thread.started" ]; then
    thread_id="$(codex_json_string_value "$line" thread_id)"
    msg="codex thread discovered"
    [ -n "$thread_id" ] && msg="$msg: $thread_id"
    printf '[phase-two:%s] %s\n' "$gate" "$msg"
    loop_event codex-thread "$gate" running "$msg"
    loop_state_write "$gate" running "$msg"
    return
  fi

  detail="$(codex_progress_detail "$line")"
  msg="$type"
  [ -n "$detail" ] && msg="$msg: $detail"
  printf '[phase-two:%s] %s\n' "$gate" "$(short_message "$msg")"
  loop_event codex-event "$gate" running "$msg"
  loop_state_write "$gate" running "$msg"
}

codex_model_token_ok() {
  local value=$1
  [[ "$value" =~ ^[A-Za-z0-9][A-Za-z0-9._:/+-]*$ ]]
}

codex_effort_token_ok() {
  local value=$1
  [[ "$value" =~ ^[A-Za-z0-9][A-Za-z0-9._+-]*$ ]]
}

validate_codex_model_var() {
  local var=$1 value=$2
  [ -z "$value" ] && return 0
  codex_model_token_ok "$value" || die "$var must be a single model token"
}

validate_codex_effort_var() {
  local var=$1 value=$2
  [ -z "$value" ] && return 0
  codex_effort_token_ok "$value" || die "$var must be a single effort token"
}

codex_add_model_and_effort_args() {
  local model=$1 effort=$2 model_var=$3 effort_var=$4
  validate_codex_model_var "$model_var" "$model"
  validate_codex_effort_var "$effort_var" "$effort"
  [ -n "$model" ] && CODEX_CMD+=(-m "$model")
  [ -n "$effort" ] && CODEX_CMD+=(-c "model_reasoning_effort=\"$effort\"")
  return 0
}

codex_route_model_and_effort() {
  local route=$1 model="" effort=""
  case "$route" in
    builder-fast)
      model="${CODEX_BUILDER_MODEL:-gpt-5.5}"
      effort="${CODEX_BUILDER_EFFORT:-xhigh}"
      codex_add_model_and_effort_args "$model" "$effort" CODEX_BUILDER_MODEL CODEX_BUILDER_EFFORT
      ;;
    builder-strong)
      model="${CODEX_STRONG_BUILDER_MODEL:-${CODEX_REVIEW_MODEL:-${CODEX_MODEL:-}}}"
      effort="${CODEX_STRONG_BUILDER_EFFORT:-${CODEX_REVIEW_EFFORT:-xhigh}}"
      codex_add_model_and_effort_args "$model" "$effort" CODEX_STRONG_BUILDER_MODEL CODEX_STRONG_BUILDER_EFFORT
      ;;
    default)
      model="${CODEX_MODEL:-}"
      effort="${CODEX_EFFORT:-}"
      codex_add_model_and_effort_args "$model" "$effort" CODEX_MODEL CODEX_EFFORT
      ;;
    *)
      die "unknown Codex route: $route"
      ;;
  esac
}

codex_cmd_prefix() {
  local sandbox="$1" route="${2:-default}"
  CODEX_CMD=("$CODEX_BIN" -a "$CODEX_APPROVAL" -s "$sandbox" -C "$ROOT")
  codex_route_model_and_effort "$route"
  [ -n "${CODEX_PROFILE:-}" ] && CODEX_CMD+=(-p "$CODEX_PROFILE")
  return 0
}

run_codex_gate() {
  local gate="$1" tools="$2" mode="$3" sid="$4" prompt="$5" sys="$6" route="${7:-default}" allow_failure="${8:-0}"
  local sandbox final combined codex_events gate_output cmd_status pipeline_status msg
  local fake_file fake_status_file fake_status_line
  sandbox="$(codex_sandbox_for_tools "$tools")"
  final="$(mktemp "${TMPDIR:-/tmp}/hypercore-loop-codex-$gate-final.XXXXXX")"
  combined="$(printf '%s\n\n---\n\n%s' "$sys" "$prompt")"
  codex_events="$LOOP_RUN_DIR/events-codex-$gate.jsonl"
  gate_output="$LOOP_RUN_GATE_DIR/$gate.final.md"
  codex_cmd_prefix "$sandbox" "$route"

  case "$mode" in
    start)  CODEX_CMD+=(exec --json -o "$final" -) ;;
    *) die "unknown gate mode: $mode" ;;
  esac

  msg="starting $gate gate with Codex sandbox $sandbox"
  loop_event gate-start "$gate" running "$msg"
  loop_state_write "$gate" running "$msg"

  if [ -n "${HYPERCORE_BUILDER_FAKE_DIR:-}" ] && [[ "$route" == builder-* ]]; then
    [ "$DRY_RUN" = 1 ] \
      || die "real execute refuses HYPERCORE_BUILDER_FAKE_DIR; fake builders are dry-run/self-test only"
    fake_file="$HYPERCORE_BUILDER_FAKE_DIR/$gate"
    fake_status_file="$fake_file.status"
    if [ -f "$fake_file" ]; then
      GATE_OUTPUT="$(cat "$fake_file")"
    else
      GATE_OUTPUT="fake builder output for $gate"
    fi
    cmd_status=0
    if [ -f "$fake_status_file" ]; then
      fake_status_line="$(sed -n '1p' "$fake_status_file")"
      case "$fake_status_line" in
        ""|*[!0-9]*) die "fake builder status for $gate must be a non-negative integer" ;;
        *) cmd_status=$fake_status_line ;;
      esac
    fi
    printf '{"type":"fake-builder","gate":%s,"route":%s,"status":%s}\n' \
      "$(json_string "$gate")" "$(json_string "$route")" "$cmd_status" > "$codex_events"
    printf '%q ' "${CODEX_CMD[@]}"; printf '<<< stdin: %q\n' "$combined"
    printf '%s\n' "$GATE_OUTPUT" > "$gate_output"
    PHASE_TWO_SESSION_ID="fake-builder-$gate"
    loop_event codex-thread "$gate" running "fake builder session: $PHASE_TWO_SESSION_ID"
    if [ "$cmd_status" -ne 0 ]; then
      msg="gate $gate failed: fake builder exited $cmd_status"
      loop_event gate-failure "$gate" failed "$msg"
      loop_state_write "$gate" failed "$msg"
      rm -f "$final"
      [ "$allow_failure" = 1 ] && return "$cmd_status"
      die "$msg"
    fi
    loop_event gate-finish "$gate" passed "fake builder stored $gate final message at $gate_output"
    loop_state_write "$gate" passed "fake builder stored $gate final message at $gate_output"
    rm -f "$final"
    printf '%s\n' "$GATE_OUTPUT"
    return 0
  fi

  if [ "$DRY_RUN" = 1 ]; then
    printf '{"type":"dry-run","gate":%s,"mode":%s}\n' "$(json_string "$gate")" "$(json_string "$mode")" > "$codex_events"
    printf '%q ' "${CODEX_CMD[@]}"; printf '<<< stdin: %q\n' "$combined"
    if [ "$mode" = start ]; then
      PHASE_TWO_SESSION_ID=dry-run-codex-session
      loop_event codex-thread "$gate" running "dry-run Codex thread: $PHASE_TWO_SESSION_ID"
    fi
    GATE_OUTPUT="(dry-run) $gate gate final output would be written by Codex."
    printf '%s\n' "$GATE_OUTPUT" > "$gate_output"
    loop_event gate-finish "$gate" skipped "dry-run stored $gate final message at $gate_output"
    loop_state_write "$gate" skipped "dry-run stored $gate final message at $gate_output"
    rm -f "$final"
    return 0
  fi

  : > "$codex_events"
  set +e
  printf '%s' "$combined" | "${CODEX_CMD[@]}" | while IFS= read -r line || [ -n "$line" ]; do
    printf '%s\n' "$line" >> "$codex_events"
    record_codex_progress_line "$gate" "$line"
  done
  pipeline_status=("${PIPESTATUS[@]}")
  set -e
  cmd_status=${pipeline_status[1]}
  if [ "$cmd_status" -ne 0 ]; then
    [ -s "$final" ] && cp "$final" "$gate_output"
    if [ -s "$final" ]; then
      GATE_OUTPUT="$(cat "$final")"
    else
      GATE_OUTPUT="codex exec exited $cmd_status"
      printf '%s\n' "$GATE_OUTPUT" > "$gate_output"
    fi
    msg="gate $gate failed: codex exec exited $cmd_status"
    loop_event gate-failure "$gate" failed "$msg"
    loop_state_write "$gate" failed "$msg"
    rm -f "$final"
    [ "$allow_failure" = 1 ] && return "$cmd_status"
    die "$msg"
  fi

  if [ "$mode" = start ]; then
    PHASE_TWO_SESSION_ID="$(codex_thread_id < "$codex_events")"
    [ -n "$PHASE_TWO_SESSION_ID" ] \
      || { rm -f "$final"; die "could not read codex thread id from gate $gate"; }
    loop_state_write "$gate" running "codex thread discovered: $PHASE_TWO_SESSION_ID"
  fi

  GATE_OUTPUT="$(cat "$final")"
  printf '%s\n' "$GATE_OUTPUT" > "$gate_output"
  rm -f "$final"
  loop_event gate-finish "$gate" passed "stored $gate final message at $gate_output"
  loop_state_write "$gate" passed "stored $gate final message at $gate_output"
  printf '%s\n' "$GATE_OUTPUT"
}

# a single fresh phase-two executor session.
# args: <gate-name> <allowed-tools> <mode> <session-id> <prompt> [instruction-gate]
# mode is start; every phase-two builder, acceptance reviewer, and archive actor is fresh.
run_gate() {
  local gate="$1" tools="$2" mode="$3" sid="$4" prompt="$5" instruction_gate="${6:-$1}" route="${7:-default}" allow_failure="${8:-0}" sys
  sys="$(cat "$GATES/$instruction_gate.md")"

  case "$LOOP_HARNESS" in
    codex) run_codex_gate "$gate" "$tools" "$mode" "$sid" "$prompt" "$sys" "$route" "$allow_failure" ;;
    *) die "unsupported LOOP_HARNESS: $LOOP_HARNESS (only codex is supported)" ;;
  esac
}

cmd_start() {
  local work_name="${1:-}" collection d frame address template options_template
  [ -n "$work_name" ] || die "usage: loop.sh [-C <node-path>] start <work-name>"
  mv "$tmp" "$file"
  printf 'recorded operator direction at %s\n' "$(relpath "$file")"
}

valid_optional_review_role() {
  local role=$1 r
  for r in "${OPTIONAL_REVIEW_ROLES[@]}"; do
    [ "$role" = "$r" ] && return 0
  done
  return 1
}

validate_review_model() {
  local model=${CODEX_REVIEW_MODEL:-}
  local effort=${CODEX_REVIEW_EFFORT:-xhigh}
  validate_codex_model_var CODEX_REVIEW_MODEL "$model"
  validate_codex_effort_var CODEX_REVIEW_EFFORT "$effort"
}

codex_add_review_route_args() {
  local model=${CODEX_REVIEW_MODEL:-}
  local effort=${CODEX_REVIEW_EFFORT:-xhigh}
  validate_review_model
  [ -n "$model" ] && CODEX_CMD+=(-m "$model")
  [ -n "$effort" ] && CODEX_CMD+=(-c "model_reasoning_effort=\"$effort\"")
  return 0
}

reviewer_verdict_from_output() {
  local output=$1 status=$2
  [ "$status" -eq 0 ] || { printf 'FLAG'; return; }
  if printf '%s\n' "$output" | grep -Eq '^VERDICT:[[:space:]]*PASS[[:space:]]*$'; then
    printf 'PASS'
  elif printf '%s\n' "$output" | grep -Eq '^VERDICT:[[:space:]]*FLAG[[:space:]]*$'; then
    printf 'FLAG'
  else
    printf 'FLAG'
  fi
}

reviewer_note_from_output() {
  local output=$1 status=$2 note diag
  if [ "$status" -ne 0 ]; then
    note="reviewer subprocess exited $status; counted as FLAG"
    diag="$(printf '%s\n' "$output" | sed -n '/[^[:space:]]/{s/^[[:space:]]*//;p;q;}')"
    [ -n "$diag" ] && note="$note; diagnostic: $diag"
  elif printf '%s\n' "$output" | grep -Eq '^VERDICT:[[:space:]]*(PASS|FLAG)[[:space:]]*$'; then
    note="$(printf '%s\n' "$output" | sed -nE 's/^NOTE:[[:space:]]*(.*)$/\1/p' | sed -n '1p')"
    [ -n "$note" ] || note="structured verdict returned"
  else
    note="missing or malformed PASS/FLAG verdict; counted as FLAG"
  fi
  short_message "$note"
}

write_indented_diagnostic_block() {
  local title=$1 content=$2
  printf '#### %s\n\n' "$title"
  if [ -n "$content" ]; then
    printf '%s\n' "$content" | sed 's/^/    /'
  else
    printf '    (none)\n'
  fi
  printf '\n'
}

run_reviewer_role() {
  local role=$1 work_name=$2 frame_rel=$3 output status final tmpout tmperr prompt fake_file fake_status_file status_line
  local stdout_output stderr_output final_output output_source
  REVIEWER_VERDICT=FLAG
  REVIEWER_NOTES="missing reviewer output; counted as FLAG"
  REVIEWER_STATUS=1
  REVIEWER_OUTPUT=""
  REVIEWER_STDOUT=""
  REVIEWER_STDERR=""
  REVIEWER_FINAL_OUTPUT=""
  REVIEWER_OUTPUT_SOURCE=none

  if [ -n "${HYPERCORE_REVIEW_FAKE_DIR:-}" ]; then
    fake_file="$HYPERCORE_REVIEW_FAKE_DIR/$role"
    fake_status_file="$fake_file.status"
    if [ -f "$fake_file" ]; then
      output="$(cat "$fake_file")"
      status=0
    else
      output="missing fake reviewer output for $role"
      status=1
    fi
    if [ -f "$fake_status_file" ]; then
      status_line="$(sed -n '1p' "$fake_status_file")"
      case "$status_line" in
        ""|*[!0-9]*) die "fake reviewer status for $role must be a non-negative integer" ;;
        *) status=$status_line ;;
      esac
    fi
    REVIEWER_STATUS="$status"
    REVIEWER_OUTPUT="$output"
    REVIEWER_FINAL_OUTPUT="$output"
    REVIEWER_OUTPUT_SOURCE=fake-output
    REVIEWER_VERDICT="$(reviewer_verdict_from_output "$output" "$status")"
    REVIEWER_NOTES="$(reviewer_note_from_output "$output" "$status")"
    return 0
  fi

  command -v "$CODEX_BIN" >/dev/null 2>&1 \
    || die "review cannot spawn Codex reviewers: Codex binary '$CODEX_BIN' is not on PATH"
  final="$(mktemp "${TMPDIR:-/tmp}/hypercore-review-$role-final.XXXXXX")"
  tmpout="$(mktemp "${TMPDIR:-/tmp}/hypercore-review-$role-out.XXXXXX")"
  tmperr="$(mktemp "${TMPDIR:-/tmp}/hypercore-review-$role-err.XXXXXX")"
  prompt="Review role: $role
Work: $work_name
Frame directory: $frame_rel

Read only the signed work frame and the intent it references. Do not debate other reviewers.
Return exactly one structured verdict line:
VERDICT: PASS
or
VERDICT: FLAG

Then optionally add one NOTE: line. Treat uncertainty as FLAG."
  CODEX_CMD=("$CODEX_BIN" -a never -s read-only -C "$ROOT")
  codex_add_review_route_args
  REVIEW_CMD=("${CODEX_CMD[@]}")
  REVIEW_CMD+=(exec -o "$final" -)
  set +e
  printf '%s' "$prompt" | "${REVIEW_CMD[@]}" >"$tmpout" 2>"$tmperr"
  status=$?
  set -e
  stdout_output="$(cat "$tmpout")"
  stderr_output="$(cat "$tmperr")"
  final_output=""
  if [ -s "$final" ]; then
    final_output="$(cat "$final")"
    || die "signed frame does not name implementation units for phase two; cannot re-derive unit boundaries without inventing"
  mapfile -t units <<< "$units_text"
  source_desc="$frame_rel/ (the signed work-node frame)"
  if [ "$DRY_RUN" != 1 ] && [ -n "${HYPERCORE_ACCEPTANCE_FAKE_DIR:-}" ]; then
    die "real execute refuses HYPERCORE_ACCEPTANCE_FAKE_DIR; fake acceptance is dry-run/self-test only"
  fi
  if [ "$DRY_RUN" != 1 ] && [ -n "${HYPERCORE_BUILDER_FAKE_DIR:-}" ]; then
    die "real execute refuses HYPERCORE_BUILDER_FAKE_DIR; fake builders are dry-run/self-test only"
  fi
  if [ "$DRY_RUN" != 1 ] && [ -n "${HYPERCORE_CHECK_FAKE_DIR:-}" ]; then
    die "real execute refuses HYPERCORE_CHECK_FAKE_DIR; fake checks are dry-run/self-test only"
  fi

  [ "$LOOP_HARNESS" = codex ] \
    || die "unsupported LOOP_HARNESS: $LOOP_HARNESS (only codex is supported)"
  printf '=== phase two: %s cleared per-unit sessions, re-deriving %s in node %s from its frame ===\n' \
    "$LOOP_HARNESS" "$work_name" "$NODE_REL"
  phase_two_run_init "$work_name"
  if ! phase_two_preflight "$work_name"; then
    PHASE_TWO_RUN_ACTIVE=0
    exit 1

codex
I found a bypass in the scanner rather than a current literal leftover: product names embedded in an identifier-style statement can survive because the regex requires non-identifier boundaries. I’m grabbing exact line references so the verdict can be concrete.
exec
/bin/bash -lc "nl -ba check.sh | sed -n '80,132p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
    80	      } else {
    81	        print "$ARGV: missing ## adapter section\n";
    82	        exit 1;
    83	      }
    84	    } elsif ($scope eq "organizing-adapter") {
    85	      my @kept;
    86	      my $taking = 0;
    87	      for my $line (split /\n/, $text) {
    88	        if ($line =~ /^- \*\*adapter\*\*/) {
    89	          $taking = 1;
    90	        } elsif ($taking && $line =~ /^\s*$/) {
    91	          last;
    92	        }
    93	        push @kept, $line if $taking;
    94	      }
    95	      if (!@kept) {
    96	        print "$ARGV: missing adapter bullet\n";
    97	        exit 1;
    98	      }
    99	      $text = join("\n", @kept) . "\n";
   100	    }
   101	
   102	    my %allowed = map { $_ => 1 } (
   103	      "adapter/codex.md",
   104	      "AGENTS.md",
   105	      "adapter/codex-mounted.md",
   106	      "adapter/loop.sh",
   107	    );
   108	    my @spans;
   109	    while ($text =~ /`([^`\n]+)`/g) {
   110	      push @spans, [$-[1], $+[1], $1];
   111	    }
   112	
   113	    my $product = qr/(?<![A-Za-z0-9_])(?:codex|claude|opus|gpt-[0-9][A-Za-z0-9._-]*|CODEX_[A-Za-z0-9_]*)(?![A-Za-z0-9_])/i;
   114	    while ($text =~ /$product/g) {
   115	      my ($start, $end, $token) = ($-[0], $+[0], $&);
   116	      my $ok = 0;
   117	      for my $span (@spans) {
   118	        if ($start >= $span->[0] && $end <= $span->[1] && $allowed{$span->[2]}) {
   119	          $ok = 1;
   120	          last;
   121	        }
   122	      }
   123	      next if $ok;
   124	      my $prefix = substr($text, 0, $start);
   125	      my $line = 1 + ($prefix =~ tr/\n//);
   126	      print "$ARGV:$line: product token \"$token\" is outside a whitelisted materialization pointer\n";
   127	      exit 1;
   128	    }
   129	  ' "$file"
   130	}
   131	
   132	contract_statement_product_absence() {

exec
/bin/bash -lc "nl -ba check.sh | sed -n '146,190p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
   146	
   147	  echo "root - contract statement product grammar self-test"
   148	  tmp="$(mktemp -d "${TMPDIR:-/tmp}/hypercore-contract-product-check.XXXXXX")" \
   149	    || { bad "contract product grammar self-test can create temporary space"; return; }
   150	
   151	  forbidden="$tmp/forbidden.md"
   152	  cat > "$forbidden" <<'EOF'
   153	# fixture
   154	
   155	the Codex review floor is named in a contract statement.
   156	EOF
   157	  if ( fail=0; contract_statement_product_absence "$forbidden" all \
   158	    "forbidden product token fixture" >"$tmp/forbidden.out" 2>&1 ); then
   159	    bad "contract product grammar rejects an unwhitelisted harness-product token"
   160	  else
   161	    ok "contract product grammar rejects an unwhitelisted harness-product token"
   162	  fi
   163	  require_text "$tmp/forbidden.out" \
   164	    'product token "Codex" is outside a whitelisted materialization pointer' \
   165	    "contract product grammar failure names the forbidden token"
   166	
   167	  pointer="$tmp/pointer.md"
   168	  cat > "$pointer" <<'EOF'
   169	# fixture
   170	
   171	the current root harness adapter is materialized as `adapter/codex.md`.
   172	EOF
   173	  if ( fail=0; contract_statement_product_absence "$pointer" all \
   174	    "whitelisted materialization pointer fixture" >"$tmp/pointer.out" 2>&1 ); then
   175	    ok "contract product grammar accepts a whitelisted materialization pointer"
   176	  else
   177	    bad "contract product grammar accepts a whitelisted materialization pointer"
   178	  fi
   179	
   180	  organizing="$tmp/organizing-document.md"
   181	  cat > "$organizing" <<'EOF'
   182	# organizing document
   183	
   184	- **adapter** -- the binding between a harness and the loop, materialized through `adapter/codex.md`.
   185	
   186	The **governed work** -- durable child nodes and mounted work under this root:
   187	
   188	- **home** -- home currently mounts codex-cockpit.
   189	EOF
   190	  if ( fail=0; contract_statement_product_absence "$organizing" organizing-adapter \

exec
/bin/bash -lc "nl -ba intent/collaboration.md | sed -n '1,24p' && nl -ba intent/loop.md | sed -n '55,74p' && nl -ba intent/adapter.md | sed -n '42,66p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
     1	# collaboration
     2	
     3	operator-machine collaboration is a first-class methodology concern, separate from the loop mechanics that enforce it.
     4	collaboration is the working relation by which operator and machine keep the work scrutable, sound, and fast across memoryless sessions.
     5	effective collaboration is complementarity, not maximal automation: the operator sets purpose, constraints, acceptance, and open direction; the machine searches, synthesizes, drafts, executes, checks, and settles only what the intent and operator leave open.
     6	collaboration keeps common ground recoverable without treating field count as proof of collaboration quality.
     7	phase one is an arc: understanding before route, scrutiny sized by reversibility, operator direction, lean recoverability, and sign-off.
     8	the phase-one collaborator is the harness role that drives orient and frame: it carries
     9	operator-facing judgment, surfaces understanding and options, and frames the signed route.
    10	phase-one corpus-throughput work -- research, the orient corpus read, and the sweep map --
    11	may be delegated by the collaborator when written ground preserves accountability and
    12	operator direction.
    13	before a route is written, the machine gives a teach-back, at least one alternative framing, information-gain questions, and a reversibility classification.
    14	one-way work requires distinct-route scrutiny before route settlement, including a mechanically spawned base review roster.
    15	the base review roster is `contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`; optional reviewers are additive and advisory only.
    16	optional reviewers cannot override, outvote, average away, or dilute unresolved base-roster or red-team flags.
    17	for one-way work, the strong review floor that scrutinizes a frame is independent of the
    18	collaborator that framed it; the framer is not its own witness.
    19	review quality is not proved by artifact scanning; review artifacts record structured signal, unresolved flags, and disposition.
    20	direction and sign-off are the two anchored operator acts in phase one, and the machine performs neither for itself.
    21	operator direction is substantive: it records a selected route, constraint, or explicit delegation with `direction-by:`.
    22	sign-off attests informed expectation and understanding, but it still requires the complete lean frame and required phase-one acts; it is not earned by bloated field scanning.
    23	a legitimate helper-written operator act crosses an operator gate that reads its decisive token from `/dev/tty` and records `operator-gate: tty`, staying simple enough that the operator confirms rather than transcribes.
    24	direction is a real operator choice: when the frame offers neutral, materially distinct numbered options, the helper copies the operator's selected option verbatim into `direction.md`; the machine may draft options but never chooses one for the operator.
    55	`independent-coherence`, `security-permissions`, and `red-team`.
    56	the `independent-coherence` lens carries the semantic sweep judgement for one-way archive;
    57	this does not solve the deeper semantic-indexing problem.
    58	missing, malformed, nonzero, unsupported-source, evidence-free, or non-`PASS`/`FLAG`
    59	acceptance reviewer output counts as `FLAG`.
    60	acceptance artifacts record their source as real reviewer, dry-run/self-test, or
    61	fake/self-test; real execute refuses fake acceptance, and real archive refuses dry-run or
    62	fake-source required acceptance.
    63	phase-one labor may be routed by role: the collaborator drives operator-facing orient and
    64	frame work, corpus-throughput work may be delegated, and the collaborator may differ from
    65	the phase-two executor harness while phase-one review stays on the strong review floor.
    66	the collaborator role defaults to the interactive harness that loaded the adapter.
    67	phase-two builders may be routed separately from reviewers through a fast-builder model
    68	knob, while tier-one acceptance, tier-two acceptance, and phase-one review stay on the
    69	strong review floor; the fast-builder default is held at the strong model until the
    70	two-step plan/build work lands.
    71	a unit build attempts the fast builder first, retries a failed unit up to three fast
    72	attempts when `./check.sh` or tier-one acceptance fails, escalates that unit to the strong
    73	builder after the fast budget, and returns to the operator if the strong attempt still
    74	fails.
    42	folded into the intent by later work and then dropped.
    43	an adapter is per harness; one node may be bound by more than one, each loaded by its own
    44	harness.
    45	an adapter binds a harness to a phase; phase one and phase two may bind different harnesses,
    46	and the current materialization binds one harness to both phases.
    47	the phase-one collaborator role defaults to the interactive harness that loaded the
    48	adapter; no orchestrator routing knob is required until a materialization routes that role.
    49	the adapter material is materialized only at the methodology root, with the prose it routes
    50	to, and not in any nested node; a mounted external project may carry a target-local entry
    51	point that links to root-managed adapter material and routes direct-path work back to the
    52	root adapter and loop.
    53	the adapter is not in the orient path; loading it is how orient begins, not part of the
    54	intent it routes to.
    55	the sweep reads the adapter against the intent, so a rule it has come to restate, or a debt
    56	the intent has since absorbed, is caught as drift.
    57	
    58	## machine
    59	the current root harness adapter is materialized as `adapter/codex.md`.
    60	the current materialization binds the same harness to phase one and phase two; the
    61	phase-one collaborator is the interactive harness that loaded the adapter.
    62	the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;
    63	the root entry is the harness's mandated pointer, holding nothing, not where the adapter
    64	lives.
    65	a machine working in a nested node under the root is bound by the root `AGENTS.md` in the
    66	project instruction chain from the project root to the current directory, so no node below

exec
/bin/bash -lc "nl -ba adapter/codex.md | sed -n '18,34p' && nl -ba adapter/codex.md | sed -n '128,138p' && nl -ba adapter/loop.sh | sed -n '2796,2806p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
    18	## Current Harness Binding
    19	
    20	The current root binding is Codex. The root `AGENTS.md` entry point is symlinked to
    21	`adapter/codex.md`; it is the harness-mandated pointer and not where the adapter lives.
    22	Nested work under this root receives that entry point through the project instruction
    23	chain, so nested nodes do not carry their own adapter material.
    24	
    25	The current materialization binds Codex to both phase one and phase two. Phase one defaults
    26	to the interactive Codex harness that loaded this adapter. Phase two is driven by
    27	`adapter/loop.sh`, which invokes fresh `codex exec` sessions for builders, reviewers, and
    28	the archive actor; the orchestrator records raw Codex JSON event streams and Codex thread
    29	ids as current binding facts.
    30	
    31	The current materialization also keeps the `CODEX_*` environment knob names in
    32	`adapter/loop.sh`. Those names are implementation binding, while the intent states the
    33	builder-model, strong-builder, review-model, and review-effort roles.
    34	
   128	
   129	- **Never fabricate content.** An unmaterialized child node is a dormant slot — a real,
   130	  empty node — not a fake app with invented sub-projects.
   131	- **Name in hypercore's own vocabulary** — node, segment, contract, mount, materialize,
   132	  the loop. Reject domain words that collide with the methodology's own concepts.
   133	- **Pin the strong review floor.** The strong review floor is not yet mechanically pinned
   134	  to a checked strong model; it can still ride an ambient harness default. A future loop
   135	  pins it.
   136	- **Re-prompt phase-one one-way review.** The current phase-one one-way review reviewer
   137	  prompt assumes a signed, route-settled frame and therefore cannot PASS a correctly staged
   138	  pre-direction frame. A future loop re-prompts it for a pre-direction decision surface.
  2796	# args: <gate-name> <allowed-tools> <mode> <session-id> <prompt> [instruction-gate]
  2797	# mode is start; every phase-two builder, acceptance reviewer, and archive actor is fresh.
  2798	run_gate() {
  2799	  local gate="$1" tools="$2" mode="$3" sid="$4" prompt="$5" instruction_gate="${6:-$1}" route="${7:-default}" allow_failure="${8:-0}" sys
  2800	  sys="$(cat "$GATES/$instruction_gate.md")"
  2801	
  2802	  case "$LOOP_HARNESS" in
  2803	    codex) run_codex_gate "$gate" "$tools" "$mode" "$sid" "$prompt" "$sys" "$route" "$allow_failure" ;;
  2804	    *) die "unsupported LOOP_HARNESS: $LOOP_HARNESS (only codex is supported)" ;;
  2805	  esac
  2806	}

exec
/bin/bash -lc "perl -0ne 'my "'$text=$_; my %allowed=map { $_=>1 } ("adapter/codex.md","AGENTS.md","adapter/codex-mounted.md","adapter/loop.sh"); my @spans; while ($text =~ /`([''^`'"\\n]+)"'`/g) { push @spans, [$-[1], $+[1], $1]; } my $product = qr/(?<![A-Za-z0-9_])(?:codex|claude|opus|gpt-[0-9][A-Za-z0-9._-]*|CODEX_[A-Za-z0-9_]*)(?![A-Za-z0-9_])/i; while ($text =~ /$product/g) { my ($start,$end,$token)=($-[0],$+[0],$&); my $ok=0; for my $span (@spans) { if ($start >= $span->[0] && $end <= $span->[1] && $allowed{$span->[2]}) { $ok=1; last; } } next if $ok; my $prefix=substr($text,0,$start); my $line=1+($prefix =~ tr/'"\\n//); print \""'$ARGV:$line: product token '"\\\""'$token'"\\\" is outside a whitelisted materialization pointer\\n\"; exit 1; }' - <<'EOF'
the builder knob is HYPERCORE_CODEX_BUILDER_MODEL for phase two.
EOF
printf 'status=%s\\n' \""'$?"' in /home/qqp/projects/hypercore
 succeeded in 0ms:
status=0

codex
VERDICT: FLAG
RATIONALE: The signed route required the product-absence grammar to have no loophole, but the built check can pass real product-bearing contract claims when the product token is embedded inside an identifier-style word.
EVIDENCE: `check.sh:113` uses `(?<![A-Za-z0-9_])...` / `(?![A-Za-z0-9_])`, so `HYPERCORE_CODEX_BUILDER_MODEL`, `Review_GPT-5`, and `CodexHarness` are missed; reproducer using the same regex returned `status=0` for `the builder knob is HYPERCORE_CODEX_BUILDER_MODEL for phase two.` while literal `GPT-5 ... Codex` returned `status=1`.
hook: Stop
hook: Stop Completed
tokens used
81,205
VERDICT: FLAG
RATIONALE: The signed route required the product-absence grammar to have no loophole, but the built check can pass real product-bearing contract claims when the product token is embedded inside an identifier-style word.
EVIDENCE: `check.sh:113` uses `(?<![A-Za-z0-9_])...` / `(?![A-Za-z0-9_])`, so `HYPERCORE_CODEX_BUILDER_MODEL`, `Review_GPT-5`, and `CodexHarness` are missed; reproducer using the same regex returned `status=0` for `the builder knob is HYPERCORE_CODEX_BUILDER_MODEL for phase two.` while literal `GPT-5 ... Codex` returned `status=1`.
