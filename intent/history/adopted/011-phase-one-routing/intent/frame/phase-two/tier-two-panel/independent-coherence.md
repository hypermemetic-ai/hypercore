OpenAI Codex v0.137.0
--------
workdir: /home/qqp/projects/hypercore
model: gpt-5.5
provider: openai
approval: never
sandbox: read-only
reasoning effort: xhigh
reasoning summaries: none
session id: 019ea4ba-ada6-7a31-99d1-d47b7dc550ba
--------
user
You are the 'independent-coherence' lens of the one-way implementation-acceptance panel for hypercore work node
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

Lens focus: Carry the semantic sweep judgement. Does the de-named contract cohere across ALL files -- no half-de-named seam; capability-requirement rephrasings faithful (not overgeneralized to 'any harness'); materialization/contract boundary holds; no statement contradicts another or the methodology? Did moving current-binding facts into adapter/codex.md lose or distort any fact?
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
I’ll read the signed frame, the methodology context, and the changed files/diff, then judge only the independent-coherence question against the frame.
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
/bin/bash -lc "sed -n '1,260p' intent/organizing-document.md" in /home/qqp/projects/hypercore
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
The frame requires more than simple token removal: it hinges on preserving the capability requirements while moving current-binding facts into material. I’m checking the current statements and material side by side for drift rather than relying only on the diff.
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
/bin/bash -lc "sed -n '1,240p' intent/adapter.md" in /home/qqp/projects/hypercore
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
/bin/bash -lc "sed -n '1,220p' intent/machine-statements/collaboration.md" in /home/qqp/projects/hypercore
exec
/bin/bash -lc "sed -n '1,260p' intent/machine-statements/loop.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# collaboration — machine statements

phase-two handoff state is written as common ground for the operator and later tooling:
the addressed work's current or recent gate, current unit, status, harness session id, latest
message, failure reason, event history, run artifact paths, and phase-two acceptance
artifact paths are recoverable from loop state files.

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
/bin/bash -lc "sed -n '1,260p' intent/machine-statements/adapter.md" in /home/qqp/projects/hypercore
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
The core statements now consistently name collaborator, executor, review floor, builder-model, and current materialization. I’m doing a product-token and wording sweep next to catch half-de-named statements or overbroad “any harness” phrasing.
exec
/bin/bash -lc "sed -n '1,190p' adapter/codex.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
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

The current materialization also keeps the `CODEX_*` environment knob names in
`adapter/loop.sh`. Those names are implementation binding, while the intent states the
builder-model, strong-builder, review-model, and review-effort roles.

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
  `loop.sh [-C <node-path>] execute <work-name>` builds the delta in green
  proof-advancing units, records structured phase-two acceptance artifacts under the work
  frame, reuses unchanged accepted units through signed-frame-derived cache state, blocks
  unresolved required `FLAG`s, and runs the required one-way implementation-acceptance panel,
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

exec
/bin/bash -lc "rg -n --case-sensitive 'Codex|codex|CODEX_|Claude|claude|Opus|opus|gpt-[0-9]' intent/collaboration.md intent/loop.md intent/adapter.md intent/machine-statements/collaboration.md intent/machine-statements/loop.md intent/machine-statements/adapter.md hypercore.md intent/organizing-document.md adapter/codex.md adapter/loop.sh check.sh" in /home/qqp/projects/hypercore
exec
/bin/bash -lc "sed -n '15,32p' intent/organizing-document.md" in /home/qqp/projects/hypercore
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
intent/machine-statements/adapter.md:3:the current root harness adapter is materialized as `adapter/codex.md`.
intent/machine-statements/adapter.md:6:the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;

 succeeded in 0ms:
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

exec
/bin/bash -lc "sed -n '250,290p' hypercore.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:

## adapter

The adapter binds a harness to the methodology.

```text
harness loads adapter -> adapter points to intent + loop -> gates become enforceable
```

For the current binding, `AGENTS.md` points at `adapter/codex.md`. The adapter does not
replace the intent; it routes the machine to the intent and makes the loop's gates rigid.

Phase one is interactive design work. Phase two is cleared, heads-down execution from the
signed frame. If a gate precondition fails, the adapter blocks instead of warning.

## collisions

Two kinds of collision matter most:

- **Concurrency**: two work nodes touch the same intent. The first adopted work wins; later
  work builds on the adopted or in-flight material it reads.
- **Orthogonality**: one segment is carrying two separable concerns. Fix the taxonomy,
  preferring clearer documents over more mechanism.

If two names are surely one concept, merge them by taking one name out. If the distinction
is real or uncertain, surface it.

## undecided topics

Absence is not a verdict. The corpus is open-world: only what the work leans on must be
grounded.

When the artifacts cannot settle a choice, the machine records the problem, constraints,
and decision surface for the operator. It does not fill the gap with invented content.

exec
/bin/bash -lc "git status --short && find . -maxdepth 2 -type d -name '[0-9][0-9][0-9]-*' | sort" in /home/qqp/projects/hypercore
 succeeded in 0ms:
A  011-phase-one-routing/intent/frame/direction.md
A  011-phase-one-routing/intent/frame/frame.md
A  011-phase-one-routing/intent/frame/options.md
A  011-phase-one-routing/intent/frame/review-supplementary.md
A  011-phase-one-routing/intent/frame/review.md
A  011-phase-one-routing/intent/frame/signoff.md
A  011-phase-one-routing/intent/organizing-document.md
 M adapter/codex.md
 M adapter/loop.sh
 M check.sh
 M hypercore.md
 M intent/adapter.md
 M intent/collaboration.md
 M intent/loop.md
 M intent/machine-statements/adapter.md
 M intent/machine-statements/collaboration.md
 M intent/machine-statements/loop.md
 M intent/organizing-document.md
?? 011-phase-one-routing/intent/frame/phase-two/
?? 999-check-loop-frame-contract-565249/
?? DECOMPOSITION-FINDINGS.md
?? TWO-STEP-BUILD-FINDINGS.md
?? WORK-NODE-COLLAPSE-FINDINGS.md
./011-phase-one-routing
./999-check-loop-frame-contract-565249

exec
/bin/bash -lc "rg -n '\\bany harness\\b|any capable harness|every harness|all harnesses|configured executor|executor binary|interactive harness|review floor|collaborator|phase-one labor|builder-model|strong-builder|review-model|review-effort' intent/collaboration.md intent/loop.md intent/adapter.md intent/machine-statements/collaboration.md intent/machine-statements/loop.md intent/machine-statements/adapter.md adapter/codex.md adapter/loop.sh check.sh" in /home/qqp/projects/hypercore
 succeeded in 0ms:
intent/collaboration.md:8:the phase-one collaborator is the harness role that drives orient and frame: it carries
intent/collaboration.md:11:may be delegated by the collaborator when written ground preserves accountability and
intent/collaboration.md:17:for one-way work, the strong review floor that scrutinizes a frame is independent of the
intent/collaboration.md:18:collaborator that framed it; the framer is not its own witness.
adapter/codex.md:33:builder-model, strong-builder, review-model, and review-effort roles.
adapter/codex.md:133:- **Pin the strong review floor.** The strong review floor is not yet mechanically pinned
intent/machine-statements/adapter.md:5:phase-one collaborator is the interactive harness that loaded the adapter.
intent/machine-statements/adapter.md:28:then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
intent/machine-statements/loop.md:15:that the configured executor binary is present and that executor home/session state is
intent/machine-statements/loop.md:74:`loop.sh execute <work-name>` routes builders through the builder-model knob, defaulting to
intent/machine-statements/loop.md:77:exhausted unit through the strong-builder model knob, and stops for the operator when the
adapter/loop.sh:40:#   CODEX_STRONG_BUILDER_MODEL (optional strong-builder escalation model)
adapter/loop.sh:3528:        die "strong-builder attempt failed for $unit_id; phase two stops for the operator and $work_name stays in flight: $UNIT_ATTEMPT_REASON"
intent/adapter.md:47:the phase-one collaborator role defaults to the interactive harness that loaded the
intent/adapter.md:61:phase-one collaborator is the interactive harness that loaded the adapter.
intent/adapter.md:84:then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
intent/loop.md:63:phase-one labor may be routed by role: the collaborator drives operator-facing orient and
intent/loop.md:64:frame work, corpus-throughput work may be delegated, and the collaborator may differ from
intent/loop.md:65:the phase-two executor harness while phase-one review stays on the strong review floor.
intent/loop.md:66:the collaborator role defaults to the interactive harness that loaded the adapter.
intent/loop.md:69:strong review floor; the fast-builder default is held at the strong model until the
intent/loop.md:114:that the configured executor binary is present and that executor home/session state is
intent/loop.md:173:`loop.sh execute <work-name>` routes builders through the builder-model knob, defaulting to
intent/loop.md:176:exhausted unit through the strong-builder model knob, and stops for the operator when the
check.sh:155:the Codex review floor is named in a contract statement.
check.sh:198:    "the phase-one collaborator is the harness role that drives orient and frame" \
check.sh:199:    "phase-one routing self-test sees the collaborator role assertion"
check.sh:207:    "phase-one labor may be routed by role" \
check.sh:210:    "the collaborator role defaults to the interactive harness that loaded the adapter" \
check.sh:211:    "phase-one routing self-test sees the collaborator held default"
check.sh:219:    "the phase-one collaborator role defaults to the interactive harness" \
check.sh:220:    "phase-one routing self-test sees the adapter collaborator default"
check.sh:223:    "phase-one routing self-test sees the current binding collaborator default"
check.sh:226:    "phase-one routing self-test sees the review-effort held default"
check.sh:229:    "phase-one routing self-test sees the builder-model held default"
check.sh:1408:    ok "loop execute retries three fast builders then accepts a strong-builder escalation"
check.sh:1410:    bad "loop execute retries three fast builders then accepts a strong-builder escalation"
check.sh:1417:    "strong builder dry-run command uses the strong-builder model knob"
check.sh:1427:    "strong-builder escalation accepts only that unit"
check.sh:1430:    "final handoff records the accepted strong-builder attempt"
check.sh:1459:  require_text "$tmp/strong-stop.err" "strong-builder attempt failed for unit-001" \
check.sh:1460:    "strong-builder failure reports the escalated failure"
check.sh:1462:    "strong-builder failure keeps the work in flight for the operator"
check.sh:1866:  "the phase-one collaborator is the harness role that drives orient and frame" \
check.sh:1867:  "collaboration segment names the phase-one collaborator role"
check.sh:1873:  "collaboration segment keeps the review floor independent of the framer"
check.sh:1875:  "phase-one labor may be routed by role" \
check.sh:1878:  "the collaborator role defaults to the interactive harness that loaded the adapter" \
check.sh:1879:  "loop segment holds the collaborator default"
check.sh:1885:  "loop segment holds the strong review floor"
check.sh:1890:  "the phase-one collaborator role defaults to the interactive harness" \
check.sh:1891:  "adapter segment holds the collaborator materialization default"
check.sh:1894:  "current binding records the collaborator held default"
check.sh:1896:  "builder-model, strong-builder, review-model, and review-effort roles" \
check.sh:2393:  "loop exposes a strong-builder escalation model knob"
check.sh:2459:  "loop routes exhausted units to a strong-builder escalation"
check.sh:2461:  'strong-builder attempt failed for $unit_id' \

codex
One extra untracked root work-looking directory is present (`999-check-loop-frame-contract-565249/`) even though the signed frame says this work node was the only work in flight. I’m reading just enough to determine whether it creates a semantic collision for this lens.
exec
/bin/bash -lc 'find 011-phase-one-routing/intent/frame/phase-two -maxdepth 3 -type f | sort' in /home/qqp/projects/hypercore
 succeeded in 0ms:
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff
011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md
011-phase-one-routing/intent/frame/phase-two/units/unit-001.md

exec
/bin/bash -lc 'find 999-check-loop-frame-contract-565249 -maxdepth 3 -type f | sort' in /home/qqp/projects/hypercore
 succeeded in 0ms:
999-check-loop-frame-contract-565249/intent/frame/direction.md
999-check-loop-frame-contract-565249/intent/frame/frame.md
999-check-loop-frame-contract-565249/intent/frame/options.md
999-check-loop-frame-contract-565249/intent/frame/review.md
999-check-loop-frame-contract-565249/intent/frame/signoff.md
999-check-loop-frame-contract-565249/intent/organizing-document.md

exec
/bin/bash -lc "sed -n '1,220p' 011-phase-one-routing/intent/frame/signoff.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# signoff - 011-phase-one-routing

signed-off-by: qqp-dev
signed-off-at: 2026-06-08T00:22:49Z
operator-gate: tty

exec
/bin/bash -lc "rg -n 'VERDICT:|FLAG|PASS|source:|unit|check.sh|implementation acceptance|independent-coherence' 011-phase-one-routing/intent/frame/phase-two 011-phase-one-routing/intent/frame/*.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
011-phase-one-routing/intent/frame/options.md:10:summary: De-name the whole contract (collaboration/loop/adapter statements and machine statements, the adapter prose, and check.sh) to role and config terms; add the phase-one collaborator role and a phase-one routing/delegation seam with held defaults; keep the materialization product-specific, including the existing CODEX_* environment-knob names, which are materialization config rather than contract.
011-phase-one-routing/intent/frame/options.md:20:tradeoff: Fullest product-agnostic surface, down to the environment-variable names; larger blast radius across the loop.sh env interface, check.sh, and any references to the knob names, with alias upkeep to avoid breaking existing CODEX_* configuration. Also collides with the queued two-step builder-routing work unless alias and default precedence are nailed down now, since two-step later flips the builder default and must stay intelligible across both the old and the neutral knob names.
011-phase-one-routing/intent/frame/frame.md:22:and `check.sh`. Two coupled defects follow.
011-phase-one-routing/intent/frame/frame.md:48:  as `CODEX_BUILDER_MODEL` is materialization, named only in `adapter/loop.sh` and `check.sh`,
011-phase-one-routing/intent/frame/frame.md:73:- Keep `./check.sh` green throughout, and make it prove both the product-name absence in the
011-phase-one-routing/intent/frame/frame.md:110:  `adapter/loop.sh`, `check.sh`) and out of the statement files, leaving statements that point
011-phase-one-routing/intent/frame/frame.md:121:live only in `adapter/loop.sh` and `check.sh`; statements name them by role (the builder-model
011-phase-one-routing/intent/frame/frame.md:178:  cannot PASS a correctly-staged pre-direction frame.
011-phase-one-routing/intent/frame/frame.md:181:- `check.sh`: add the product-absence check (the grammar above) over the enumerated statement
011-phase-one-routing/intent/frame/frame.md:185:  whitelisted fenced pointer PASSES; a `codex-cockpit` mention in the home text PASSES; the new
011-phase-one-routing/intent/frame/frame.md:188:Implementation units for phase two:
011-phase-one-routing/intent/frame/frame.md:190:1. De-name the contract statements and add the phase-one roles, updating `check.sh` in lockstep
011-phase-one-routing/intent/frame/frame.md:196:   review-floor-independent-of-framer, and phase-one-routing statements; and update `check.sh`
011-phase-one-routing/intent/frame/frame.md:199:   the held-default assertions. `./check.sh` is green at the unit boundary.
011-phase-one-routing/intent/frame/frame.md:200:2. Add the `check.sh` self-tests for the grammar (an unwhitelisted product token in a statement
011-phase-one-routing/intent/frame/frame.md:205:   `./check.sh` is green at the unit boundary.
011-phase-one-routing/intent/frame/frame.md:210:the adapter prose, and `check.sh` express the harness binding in role and config terms with no
011-phase-one-routing/intent/frame/frame.md:213:review floor's independence from the framer is stated; and `./check.sh` is green.
011-phase-one-routing/intent/frame/frame.md:217:- `./check.sh` exits zero after implementation and after the archive fold.
011-phase-one-routing/intent/frame/frame.md:245:  units, plan tasks, acceptance artifacts, or review evidence. This keeps the collaborator seam
011-phase-one-routing/intent/frame/frame.md:250:Required proof: the observable-acceptance checks above, plus `check.sh` self-tests that a
011-phase-one-routing/intent/frame/frame.md:252:reproduce current routing when the knobs are unset. Baseline `./check.sh` is green before
011-phase-one-routing/intent/frame/frame.md:268:`check.sh` proves it; `hypercore.md` summarizes it; `adapter/codex.md` is the current
011-phase-one-routing/intent/frame/frame.md:273:prose, and `check.sh` together — a half-de-named contract is a worse smell than the current
011-phase-one-routing/intent/frame/frame.md:287:the current harness, `./check.sh` proves all of this and is green, and the sweep is coherent.
011-phase-one-routing/intent/frame/review.md:3:Overall: FLAG
011-phase-one-routing/intent/frame/review.md:6:Disposition: escalated - FLAG verdicts must be answered in the frame; optional reviewers are advisory only and cannot clear base-roster or red-team flags
011-phase-one-routing/intent/frame/review.md:10:- contract-checkability: FLAG
011-phase-one-routing/intent/frame/review.md:11:- soundness-fit: FLAG
011-phase-one-routing/intent/frame/review.md:12:- simplicity-fastness: FLAG
011-phase-one-routing/intent/frame/review.md:13:- red-team: FLAG
011-phase-one-routing/intent/frame/review.md:45:selected-output-source: final-output
011-phase-one-routing/intent/frame/review.md:49:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:54:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:59:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:82:    VERDICT: PASS
011-phase-one-routing/intent/frame/review.md:84:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:86:    Then optionally add one NOTE: line. Treat uncertainty as FLAG.
011-phase-one-routing/intent/frame/review.md:99:    leaf-materialized by `hypercore.md` and `check.sh`, divided along one axis:
011-phase-one-routing/intent/frame/review.md:265:    The methodology prose is this file. The mechanical check over nodes is `check.sh`.
011-phase-one-routing/intent/frame/review.md:272:    good statement:  check.sh checks every node in the tree.
011-phase-one-routing/intent/frame/review.md:349:      units.
011-phase-one-routing/intent/frame/review.md:350:    - **check**: run mechanical checks and independent structured implementation acceptance;
011-phase-one-routing/intent/frame/review.md:363:    must be able to re-derive each unit and acceptance review from the signed frame directory
011-phase-one-routing/intent/frame/review.md:421:    intent/history/adopted/008-phase-two-acceptance/intent/frame/phase-two/diffs/unit-001.diff
011-phase-one-routing/intent/frame/review.md:422:    intent/history/adopted/008-phase-two-acceptance/intent/frame/phase-two/handoffs/unit-001.md
011-phase-one-routing/intent/frame/review.md:423:    intent/history/adopted/008-phase-two-acceptance/intent/frame/phase-two/tier-one/unit-001.md
011-phase-one-routing/intent/frame/review.md:424:    intent/history/adopted/008-phase-two-acceptance/intent/frame/phase-two/units/unit-001.md
011-phase-one-routing/intent/frame/review.md:434:    intent/history/adopted/009-operator-acts/intent/frame/phase-two/diffs/unit-001.diff
011-phase-one-routing/intent/frame/review.md:435:    intent/history/adopted/009-operator-acts/intent/frame/phase-two/diffs/unit-002.diff
011-phase-one-routing/intent/frame/review.md:436:    intent/history/adopted/009-operator-acts/intent/frame/phase-two/diffs/unit-003.diff
011-phase-one-routing/intent/frame/review.md:437:    intent/history/adopted/009-operator-acts/intent/frame/phase-two/diffs/unit-004.diff
011-phase-one-routing/intent/frame/review.md:438:    intent/history/adopted/009-operator-acts/intent/frame/phase-two/handoffs/unit-001.md
011-phase-one-routing/intent/frame/review.md:439:    intent/history/adopted/009-operator-acts/intent/frame/phase-two/handoffs/unit-002.md
011-phase-one-routing/intent/frame/review.md:440:    intent/history/adopted/009-operator-acts/intent/frame/phase-two/handoffs/unit-003.md
011-phase-one-routing/intent/frame/review.md:441:    intent/history/adopted/009-operator-acts/intent/frame/phase-two/handoffs/unit-004.md
011-phase-one-routing/intent/frame/review.md:442:    intent/history/adopted/009-operator-acts/intent/frame/phase-two/tier-one/unit-001.md
011-phase-one-routing/intent/frame/review.md:443:    intent/history/adopted/009-operator-acts/intent/frame/phase-two/tier-one/unit-002.md
011-phase-one-routing/intent/frame/review.md:444:    intent/history/adopted/009-operator-acts/intent/frame/phase-two/tier-one/unit-003.md
011-phase-one-routing/intent/frame/review.md:445:    intent/history/adopted/009-operator-acts/intent/frame/phase-two/tier-one/unit-004.md
011-phase-one-routing/intent/frame/review.md:446:    intent/history/adopted/009-operator-acts/intent/frame/phase-two/tier-two-panel/independent-coherence.md
011-phase-one-routing/intent/frame/review.md:451:    intent/history/adopted/009-operator-acts/intent/frame/phase-two/units/unit-001.md
011-phase-one-routing/intent/frame/review.md:452:    intent/history/adopted/009-operator-acts/intent/frame/phase-two/units/unit-002.md
011-phase-one-routing/intent/frame/review.md:453:    intent/history/adopted/009-operator-acts/intent/frame/phase-two/units/unit-003.md
011-phase-one-routing/intent/frame/review.md:454:    intent/history/adopted/009-operator-acts/intent/frame/phase-two/units/unit-004.md
011-phase-one-routing/intent/frame/review.md:463:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/diffs/unit-001.diff
011-phase-one-routing/intent/frame/review.md:464:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/diffs/unit-002.diff
011-phase-one-routing/intent/frame/review.md:465:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/diffs/unit-003.diff
011-phase-one-routing/intent/frame/review.md:466:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/diffs/unit-004.diff
011-phase-one-routing/intent/frame/review.md:467:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/diffs/unit-005.diff
011-phase-one-routing/intent/frame/review.md:468:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/handoffs/unit-001.md
011-phase-one-routing/intent/frame/review.md:469:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/handoffs/unit-002.md
011-phase-one-routing/intent/frame/review.md:470:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/handoffs/unit-003.md
011-phase-one-routing/intent/frame/review.md:471:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/handoffs/unit-004.md
011-phase-one-routing/intent/frame/review.md:472:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/handoffs/unit-005.md
011-phase-one-routing/intent/frame/review.md:473:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/tier-one/unit-001.md
011-phase-one-routing/intent/frame/review.md:474:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/tier-one/unit-002.md
011-phase-one-routing/intent/frame/review.md:475:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/tier-one/unit-003.md
011-phase-one-routing/intent/frame/review.md:476:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/tier-one/unit-004.md
011-phase-one-routing/intent/frame/review.md:477:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/tier-one/unit-005.md
011-phase-one-routing/intent/frame/review.md:478:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/tier-two-panel/independent-coherence.md
011-phase-one-routing/intent/frame/review.md:483:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/units/unit-001.md
011-phase-one-routing/intent/frame/review.md:484:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/units/unit-002.md
011-phase-one-routing/intent/frame/review.md:485:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/units/unit-003.md
011-phase-one-routing/intent/frame/review.md:486:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/units/unit-004.md
011-phase-one-routing/intent/frame/review.md:487:    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/units/unit-005.md
011-phase-one-routing/intent/frame/review.md:539:    and `check.sh`. Two coupled defects follow.
011-phase-one-routing/intent/frame/review.md:565:      as `CODEX_BUILDER_MODEL` is materialization, named only in `adapter/loop.sh` and `check.sh`,
011-phase-one-routing/intent/frame/review.md:580:    - Keep `./check.sh` green throughout, and make it prove both the product-name absence in the
011-phase-one-routing/intent/frame/review.md:601:    the adapter prose, and `check.sh` express the harness binding in role and config terms with no
011-phase-one-routing/intent/frame/review.md:604:    review floor's independence from the framer is stated; and `./check.sh` is green.
011-phase-one-routing/intent/frame/review.md:608:    - `./check.sh` exits zero after implementation and after the archive fold.
011-phase-one-routing/intent/frame/review.md:632:    Required proof: the observable-acceptance checks above, plus `check.sh` self-tests that a
011-phase-one-routing/intent/frame/review.md:634:    reproduce current routing when the knobs are unset. Baseline `./check.sh` is green before
011-phase-one-routing/intent/frame/review.md:642:    `check.sh` proves it; `hypercore.md` summarizes it; `adapter/codex.md` is the current
011-phase-one-routing/intent/frame/review.md:647:    prose, and `check.sh` together — a half-de-named contract is a worse smell than the current
011-phase-one-routing/intent/frame/review.md:661:    the current harness, `./check.sh` proves all of this and is green, and the sweep is coherent.
011-phase-one-routing/intent/frame/review.md:683:    summary: De-name the whole contract (collaboration/loop/adapter statements and machine statements, the adapter prose, and check.sh) to role and config terms; add the phase-one collaborator role and a phase-one routing/delegation seam with held defaults; keep the materialization product-specific, including the existing CODEX_* environment-knob names, which are materialization config rather than contract.
011-phase-one-routing/intent/frame/review.md:693:    tradeoff: Fullest product-agnostic surface, down to the environment-variable names; larger blast radius across the loop.sh env interface, check.sh, and any references to the knob names, with alias upkeep to avoid breaking existing CODEX_* configuration.
011-phase-one-routing/intent/frame/review.md:705:    Overall: FLAG
011-phase-one-routing/intent/frame/review.md:708:    Disposition: escalated - FLAG verdicts must be answered in the frame; optional reviewers are advisory only and cannot clear base-roster or red-team flags
011-phase-one-routing/intent/frame/review.md:712:    - contract-checkability: FLAG
011-phase-one-routing/intent/frame/review.md:713:    - soundness-fit: FLAG
011-phase-one-routing/intent/frame/review.md:714:    - simplicity-fastness: FLAG
011-phase-one-routing/intent/frame/review.md:715:    - red-team: FLAG
011-phase-one-routing/intent/frame/review.md:747:    selected-output-source: final-output
011-phase-one-routing/intent/frame/review.md:751:        VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:756:        VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:761:        VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:784:        VERDICT: PASS
011-phase-one-routing/intent/frame/review.md:786:        VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:788:        Then optionally add one NOTE: line. Treat uncertainty as FLAG.
011-phase-one-routing/intent/frame/review.md:815:        and `check.sh`. Two coupled defects follow.
011-phase-one-routing/intent/frame/review.md:852:        - Keep `./check.sh` green throughout, and make it prove both the product-name absence in the
011-phase-one-routing/intent/frame/review.md:872:        the adapter prose, and `check.sh` express the harness binding in role and config terms with no
011-phase-one-routing/intent/frame/review.md:875:        review floor's independence from the framer is stated; and `./check.sh` is green.
011-phase-one-routing/intent/frame/review.md:879:        - `./check.sh` exits zero after implementation and after the archive fold.
011-phase-one-routing/intent/frame/review.md:902:        Required proof: the observable-acceptance checks above, plus `check.sh` self-tests that a
011-phase-one-routing/intent/frame/review.md:904:        reproduce current routing when the knobs are unset. Baseline `./check.sh` is green before
011-phase-one-routing/intent/frame/review.md:912:        `check.sh` proves it; `hypercore.md` summarizes it; `adapter/codex.md` is the current
011-phase-one-routing/intent/frame/review.md:917:        prose, and `check.sh` together — a half-de-named contract is a worse smell than the current
011-phase-one-routing/intent/frame/review.md:931:        the current harness, `./check.sh` proves all of this and is green, and the sweep is coherent.
011-phase-one-routing/intent/frame/review.md:992:    unresolved implementation-acceptance `FLAG`s are feedback material: they block archive and surface to the operator rather than being self-cleared, averaged away, outvoted, or treated as warnings.
011-phase-one-routing/intent/frame/review.md:993:    implementation-acceptance signal is legible: a required acceptance verdict carries a parseable `PASS` or `FLAG` plus rationale and concrete evidence enough for the operator or a later machine to act on a `FLAG`; uncertainty still flags, and legibility makes the door actionable without weakening it.
011-phase-one-routing/intent/frame/review.md:994:    build retry is bounded proof-floor recovery, not a structural re-decision: a builder may re-attempt a failed unit within the signed route, but structural mismatches, tier-two `FLAG`s, and an exhausted escalation budget still surface to the operator rather than being retried away.
011-phase-one-routing/intent/frame/review.md:1000:    the addressed work's current or recent gate, current unit, status, Codex thread id, latest
011-phase-one-routing/intent/frame/review.md:1038:    green proof-advancing units, and stops when the frame is incomplete, a check fails, or
011-phase-one-routing/intent/frame/review.md:1039:    required implementation acceptance returns `FLAG`.
011-phase-one-routing/intent/frame/review.md:1046:    implement: build in proof-advancing units from the signed frame.
011-phase-one-routing/intent/frame/review.md:1047:    an implementation unit is the smallest proof-advancing delta that leaves `./check.sh`
011-phase-one-routing/intent/frame/review.md:1048:    green; units are vertical slices, so statements, material, and checks land together when
011-phase-one-routing/intent/frame/review.md:1052:    `./check.sh` is green at every phase-two unit boundary and before any acceptance verdict
011-phase-one-routing/intent/frame/review.md:1054:    after each implementation unit, a fresh independent read-only implementation-acceptance
011-phase-one-routing/intent/frame/review.md:1055:    reviewer reads the signed frame, unit proof obligation, unit diff, and lean unit handoff,
011-phase-one-routing/intent/frame/review.md:1056:    then returns a structured verdict: exactly one `PASS` or `FLAG` with required rationale and
011-phase-one-routing/intent/frame/review.md:1062:    `independent-coherence`, `security-permissions`, and `red-team`.
011-phase-one-routing/intent/frame/review.md:1063:    the `independent-coherence` lens carries the semantic sweep judgement for one-way archive;
011-phase-one-routing/intent/frame/review.md:1065:    missing, malformed, nonzero, unsupported-source, evidence-free, or non-`PASS`/`FLAG`
011-phase-one-routing/intent/frame/review.md:1066:    acceptance reviewer output counts as `FLAG`.
011-phase-one-routing/intent/frame/review.md:1074:    a unit build attempts the fast builder first, retries a failed unit up to three fast
011-phase-one-routing/intent/frame/review.md:1075:    attempts when `./check.sh` or tier-one acceptance fails, escalates that unit to the strong
011-phase-one-routing/intent/frame/review.md:1078:    execute is resumable from the signed frame and on-disk artifacts: a passed unit's build and
011-phase-one-routing/intent/frame/review.md:1079:    tier-one evidence is reused only when its cache key still matches the signed frame, unit
011-phase-one-routing/intent/frame/review.md:1080:    proof obligation, relevant prior-unit state, loop implementation version, recorded diff, and
011-phase-one-routing/intent/frame/review.md:1081:    green mechanical-check evidence, and a cache miss rebuilds the unit and invalidates
011-phase-one-routing/intent/frame/review.md:1082:    downstream unit evidence.
011-phase-one-routing/intent/frame/review.md:1083:    unresolved required tier-one or tier-two `FLAG`s halt phase two before archive; the active
011-phase-one-routing/intent/frame/review.md:1172:    `loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
011-phase-one-routing/intent/frame/review.md:1173:    fresh Codex builder session for each unit, and records lean unit handoff, diff, and
011-phase-one-routing/intent/frame/review.md:1177:    route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
011-phase-one-routing/intent/frame/review.md:1182:    rationale, evidence, and a `source:` marker, refuses `HYPERCORE_ACCEPTANCE_FAKE_DIR` outside
011-phase-one-routing/intent/frame/review.md:1183:    dry-run, and lets real archive accept only `source: real-reviewer` required acceptance.
011-phase-one-routing/intent/frame/review.md:1184:    `loop.sh execute <work-name>` caches per-unit build and tier-one evidence under a
011-phase-one-routing/intent/frame/review.md:1185:    signed-frame-derived key, skips unchanged accepted units on rerun, and rebuilds cache misses
011-phase-one-routing/intent/frame/review.md:1188:    implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
011-phase-one-routing/intent/frame/review.md:1216:    and archive run through cleared sessions that re-derive each unit and acceptance review
011-phase-one-routing/intent/frame/review.md:1221:    the Codex implementation-acceptance reviewer for each phase-two unit is independent and
011-phase-one-routing/intent/frame/review.md:1224:    `whole-acceptance-conformance`, `proof-integrity`, `independent-coherence`,
011-phase-one-routing/intent/frame/review.md:1265:    over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
011-phase-one-routing/intent/frame/review.md:1275:    artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
011-phase-one-routing/intent/frame/review.md:1276:    then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
011-phase-one-routing/intent/frame/review.md:1308:    `check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
011-phase-one-routing/intent/frame/review.md:1332:    at the check gate the orchestrator records tier-one implementation acceptance for each
011-phase-one-routing/intent/frame/review.md:1333:    unit, records the concurrent one-way tier-two panel when required, and halts phase two
011-phase-one-routing/intent/frame/review.md:1345:    the addressed work's current or recent gate, current unit, status, Codex thread id, latest
011-phase-one-routing/intent/frame/review.md:1369:    thread id, current unit, latest message, failure reason, event history, run artifact
011-phase-one-routing/intent/frame/review.md:1427:    `loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
011-phase-one-routing/intent/frame/review.md:1428:    fresh Codex builder session for each unit, and records lean unit handoff, diff, and
011-phase-one-routing/intent/frame/review.md:1432:    route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
011-phase-one-routing/intent/frame/review.md:1437:    rationale, evidence, and a `source:` marker, refuses `HYPERCORE_ACCEPTANCE_FAKE_DIR` outside
011-phase-one-routing/intent/frame/review.md:1438:    dry-run, and lets real archive accept only `source: real-reviewer` required acceptance.
011-phase-one-routing/intent/frame/review.md:1439:    `loop.sh execute <work-name>` caches per-unit build and tier-one evidence under a
011-phase-one-routing/intent/frame/review.md:1440:    signed-frame-derived key, skips unchanged accepted units on rerun, and rebuilds cache misses
011-phase-one-routing/intent/frame/review.md:1443:    implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
011-phase-one-routing/intent/frame/review.md:1464:    over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
011-phase-one-routing/intent/frame/review.md:1474:    artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
011-phase-one-routing/intent/frame/review.md:1475:    then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
011-phase-one-routing/intent/frame/review.md:1507:    `check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
011-phase-one-routing/intent/frame/review.md:1531:    at the check gate the orchestrator records tier-one implementation acceptance for each
011-phase-one-routing/intent/frame/review.md:1532:    unit, records the concurrent one-way tier-two panel when required, and halts phase two
011-phase-one-routing/intent/frame/review.md:1536:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:1546:selected-output-source: final-output
011-phase-one-routing/intent/frame/review.md:1550:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:1555:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:1560:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:1583:    VERDICT: PASS
011-phase-one-routing/intent/frame/review.md:1585:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:1587:    Then optionally add one NOTE: line. Treat uncertainty as FLAG.
011-phase-one-routing/intent/frame/review.md:1616:    and `check.sh`. Two coupled defects follow.
011-phase-one-routing/intent/frame/review.md:1642:      as `CODEX_BUILDER_MODEL` is materialization, named only in `adapter/loop.sh` and `check.sh`,
011-phase-one-routing/intent/frame/review.md:1657:    - Keep `./check.sh` green throughout, and make it prove both the product-name absence in the
011-phase-one-routing/intent/frame/review.md:1678:    the adapter prose, and `check.sh` express the harness binding in role and config terms with no
011-phase-one-routing/intent/frame/review.md:1681:    review floor's independence from the framer is stated; and `./check.sh` is green.
011-phase-one-routing/intent/frame/review.md:1685:    - `./check.sh` exits zero after implementation and after the archive fold.
011-phase-one-routing/intent/frame/review.md:1709:    Required proof: the observable-acceptance checks above, plus `check.sh` self-tests that a
011-phase-one-routing/intent/frame/review.md:1711:    reproduce current routing when the knobs are unset. Baseline `./check.sh` is green before
011-phase-one-routing/intent/frame/review.md:1719:    `check.sh` proves it; `hypercore.md` summarizes it; `adapter/codex.md` is the current
011-phase-one-routing/intent/frame/review.md:1724:    prose, and `check.sh` together — a half-de-named contract is a worse smell than the current
011-phase-one-routing/intent/frame/review.md:1738:    the current harness, `./check.sh` proves all of this and is green, and the sweep is coherent.
011-phase-one-routing/intent/frame/review.md:1761:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:1771:selected-output-source: final-output
011-phase-one-routing/intent/frame/review.md:1775:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:1780:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:1785:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:1808:    VERDICT: PASS
011-phase-one-routing/intent/frame/review.md:1810:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:1812:    Then optionally add one NOTE: line. Treat uncertainty as FLAG.
011-phase-one-routing/intent/frame/review.md:1846:    and `check.sh`. Two coupled defects follow.
011-phase-one-routing/intent/frame/review.md:1872:      as `CODEX_BUILDER_MODEL` is materialization, named only in `adapter/loop.sh` and `check.sh`,
011-phase-one-routing/intent/frame/review.md:1887:    - Keep `./check.sh` green throughout, and make it prove both the product-name absence in the
011-phase-one-routing/intent/frame/review.md:1908:    the adapter prose, and `check.sh` express the harness binding in role and config terms with no
011-phase-one-routing/intent/frame/review.md:1911:    review floor's independence from the framer is stated; and `./check.sh` is green.
011-phase-one-routing/intent/frame/review.md:1915:    - `./check.sh` exits zero after implementation and after the archive fold.
011-phase-one-routing/intent/frame/review.md:1939:    Required proof: the observable-acceptance checks above, plus `check.sh` self-tests that a
011-phase-one-routing/intent/frame/review.md:1941:    reproduce current routing when the knobs are unset. Baseline `./check.sh` is green before
011-phase-one-routing/intent/frame/review.md:1949:    `check.sh` proves it; `hypercore.md` summarizes it; `adapter/codex.md` is the current
011-phase-one-routing/intent/frame/review.md:1954:    prose, and `check.sh` together — a half-de-named contract is a worse smell than the current
011-phase-one-routing/intent/frame/review.md:1968:    the current harness, `./check.sh` proves all of this and is green, and the sweep is coherent.
011-phase-one-routing/intent/frame/review.md:1983:    Overall: FLAG
011-phase-one-routing/intent/frame/review.md:1986:    Disposition: escalated - FLAG verdicts must be answered in the frame; optional reviewers are advisory only and cannot clear base-roster or red-team flags
011-phase-one-routing/intent/frame/review.md:1990:    - contract-checkability: FLAG
011-phase-one-routing/intent/frame/review.md:1991:    - soundness-fit: FLAG
011-phase-one-routing/intent/frame/review.md:1992:    - simplicity-fastness: FLAG
011-phase-one-routing/intent/frame/review.md:1993:    - red-team: FLAG
011-phase-one-routing/intent/frame/review.md:2025:    selected-output-source: final-output
011-phase-one-routing/intent/frame/review.md:2029:        VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:2034:        VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:2039:        VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:2062:        VERDICT: PASS
011-phase-one-routing/intent/frame/review.md:2064:        VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:2066:        Then optionally add one NOTE: line. Treat uncertainty as FLAG.
011-phase-one-routing/intent/frame/review.md:2093:        and `check.sh`. Two coupled defects follow.
011-phase-one-routing/intent/frame/review.md:2130:        - Keep `./check.sh` green throughout, and make it prove both the product-name absence in the
011-phase-one-routing/intent/frame/review.md:2150:        the adapter prose, and `check.sh` express the harness binding in role and config terms with no
011-phase-one-routing/intent/frame/review.md:2153:        review floor's independence from the framer is stated; and `./check.sh` is green.
011-phase-one-routing/intent/frame/review.md:2157:        - `./check.sh` exits zero after implementation and after the archive fold.
011-phase-one-routing/intent/frame/review.md:2180:        Required proof: the observable-acceptance checks above, plus `check.sh` self-tests that a
011-phase-one-routing/intent/frame/review.md:2182:        reproduce current routing when the knobs are unset. Baseline `./check.sh` is green before
011-phase-one-routing/intent/frame/review.md:2190:        `check.sh` proves it; `hypercore.md` summarizes it; `adapter/codex.md` is the current
011-phase-one-routing/intent/frame/review.md:2195:        prose, and `check.sh` together — a half-de-named contract is a worse smell than the current
011-phase-one-routing/intent/frame/review.md:2209:        the current harness, `./check.sh` proves all of this and is green, and the sweep is coherent.
011-phase-one-routing/intent/frame/review.md:2234:    summary: De-name the whole contract (collaboration/loop/adapter statements and machine statements, the adapter prose, and check.sh) to role and config terms; add the phase-one collaborator role and a phase-one routing/delegation seam with held defaults; keep the materialization product-specific, including the existing CODEX_* environment-knob names, which are materialization config rather than contract.
011-phase-one-routing/intent/frame/review.md:2244:    tradeoff: Fullest product-agnostic surface, down to the environment-variable names; larger blast radius across the loop.sh env interface, check.sh, and any references to the knob names, with alias upkeep to avoid breaking existing CODEX_* configuration.
011-phase-one-routing/intent/frame/review.md:2284:    green proof-advancing units, and stops when the frame is incomplete, a check fails, or
011-phase-one-routing/intent/frame/review.md:2285:    required implementation acceptance returns `FLAG`.
011-phase-one-routing/intent/frame/review.md:2292:    implement: build in proof-advancing units from the signed frame.
011-phase-one-routing/intent/frame/review.md:2293:    an implementation unit is the smallest proof-advancing delta that leaves `./check.sh`
011-phase-one-routing/intent/frame/review.md:2294:    green; units are vertical slices, so statements, material, and checks land together when
011-phase-one-routing/intent/frame/review.md:2298:    `./check.sh` is green at every phase-two unit boundary and before any acceptance verdict
011-phase-one-routing/intent/frame/review.md:2300:    after each implementation unit, a fresh independent read-only implementation-acceptance
011-phase-one-routing/intent/frame/review.md:2301:    reviewer reads the signed frame, unit proof obligation, unit diff, and lean unit handoff,
011-phase-one-routing/intent/frame/review.md:2302:    then returns a structured verdict: exactly one `PASS` or `FLAG` with required rationale and
011-phase-one-routing/intent/frame/review.md:2308:    `independent-coherence`, `security-permissions`, and `red-team`.
011-phase-one-routing/intent/frame/review.md:2309:    the `independent-coherence` lens carries the semantic sweep judgement for one-way archive;
011-phase-one-routing/intent/frame/review.md:2311:    missing, malformed, nonzero, unsupported-source, evidence-free, or non-`PASS`/`FLAG`
011-phase-one-routing/intent/frame/review.md:2312:    acceptance reviewer output counts as `FLAG`.
011-phase-one-routing/intent/frame/review.md:2320:    a unit build attempts the fast builder first, retries a failed unit up to three fast
011-phase-one-routing/intent/frame/review.md:2321:    attempts when `./check.sh` or tier-one acceptance fails, escalates that unit to the strong
011-phase-one-routing/intent/frame/review.md:2324:    execute is resumable from the signed frame and on-disk artifacts: a passed unit's build and
011-phase-one-routing/intent/frame/review.md:2325:    tier-one evidence is reused only when its cache key still matches the signed frame, unit
011-phase-one-routing/intent/frame/review.md:2326:    proof obligation, relevant prior-unit state, loop implementation version, recorded diff, and
011-phase-one-routing/intent/frame/review.md:2327:    green mechanical-check evidence, and a cache miss rebuilds the unit and invalidates
011-phase-one-routing/intent/frame/review.md:2328:    downstream unit evidence.
011-phase-one-routing/intent/frame/review.md:2329:    unresolved required tier-one or tier-two `FLAG`s halt phase two before archive; the active
011-phase-one-routing/intent/frame/review.md:2418:    `loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
011-phase-one-routing/intent/frame/review.md:2419:    fresh Codex builder session for each unit, and records lean unit handoff, diff, and
011-phase-one-routing/intent/frame/review.md:2423:    route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
011-phase-one-routing/intent/frame/review.md:2428:    rationale, evidence, and a `source:` marker, refuses `HYPERCORE_ACCEPTANCE_FAKE_DIR` outside
011-phase-one-routing/intent/frame/review.md:2429:    dry-run, and lets real archive accept only `source: real-reviewer` required acceptance.
011-phase-one-routing/intent/frame/review.md:2430:    `loop.sh execute <work-name>` caches per-unit build and tier-one evidence under a
011-phase-one-routing/intent/frame/review.md:2431:    signed-frame-derived key, skips unchanged accepted units on rerun, and rebuilds cache misses
011-phase-one-routing/intent/frame/review.md:2434:    implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
011-phase-one-routing/intent/frame/review.md:2455:    thread id, current unit, latest message, failure reason, event history, run artifact
011-phase-one-routing/intent/frame/review.md:2513:    `loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
011-phase-one-routing/intent/frame/review.md:2514:    fresh Codex builder session for each unit, and records lean unit handoff, diff, and
011-phase-one-routing/intent/frame/review.md:2518:    route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
011-phase-one-routing/intent/frame/review.md:2523:    rationale, evidence, and a `source:` marker, refuses `HYPERCORE_ACCEPTANCE_FAKE_DIR` outside
011-phase-one-routing/intent/frame/review.md:2524:    dry-run, and lets real archive accept only `source: real-reviewer` required acceptance.
011-phase-one-routing/intent/frame/review.md:2525:    `loop.sh execute <work-name>` caches per-unit build and tier-one evidence under a
011-phase-one-routing/intent/frame/review.md:2526:    signed-frame-derived key, skips unchanged accepted units on rerun, and rebuilds cache misses
011-phase-one-routing/intent/frame/review.md:2529:    implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
011-phase-one-routing/intent/frame/review.md:2550:    over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
011-phase-one-routing/intent/frame/review.md:2560:    artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
011-phase-one-routing/intent/frame/review.md:2561:    then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
011-phase-one-routing/intent/frame/review.md:2593:    `check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
011-phase-one-routing/intent/frame/review.md:2617:    at the check gate the orchestrator records tier-one implementation acceptance for each
011-phase-one-routing/intent/frame/review.md:2618:    unit, records the concurrent one-way tier-two panel when required, and halts phase two
011-phase-one-routing/intent/frame/review.md:2627:    the addressed work's current or recent gate, current unit, status, Codex thread id, latest
011-phase-one-routing/intent/frame/review.md:2657:    unresolved implementation-acceptance `FLAG`s are feedback material: they block archive and surface to the operator rather than being self-cleared, averaged away, outvoted, or treated as warnings.
011-phase-one-routing/intent/frame/review.md:2658:    implementation-acceptance signal is legible: a required acceptance verdict carries a parseable `PASS` or `FLAG` plus rationale and concrete evidence enough for the operator or a later machine to act on a `FLAG`; uncertainty still flags, and legibility makes the door actionable without weakening it.
011-phase-one-routing/intent/frame/review.md:2659:    build retry is bounded proof-floor recovery, not a structural re-decision: a builder may re-attempt a failed unit within the signed route, but structural mismatches, tier-two `FLAG`s, and an exhausted escalation budget still surface to the operator rather than being retried away.
011-phase-one-routing/intent/frame/review.md:2665:    the addressed work's current or recent gate, current unit, status, Codex thread id, latest
011-phase-one-routing/intent/frame/review.md:2693:    and archive run through cleared sessions that re-derive each unit and acceptance review
011-phase-one-routing/intent/frame/review.md:2698:    the Codex implementation-acceptance reviewer for each phase-two unit is independent and
011-phase-one-routing/intent/frame/review.md:2701:    `whole-acceptance-conformance`, `proof-integrity`, `independent-coherence`,
011-phase-one-routing/intent/frame/review.md:2742:    over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
011-phase-one-routing/intent/frame/review.md:2752:    artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
011-phase-one-routing/intent/frame/review.md:2753:    then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
011-phase-one-routing/intent/frame/review.md:2785:    `check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
011-phase-one-routing/intent/frame/review.md:2809:    at the check gate the orchestrator records tier-one implementation acceptance for each
011-phase-one-routing/intent/frame/review.md:2810:    unit, records the concurrent one-way tier-two panel when required, and halts phase two
011-phase-one-routing/intent/frame/review.md:2817:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:2827:selected-output-source: final-output
011-phase-one-routing/intent/frame/review.md:2831:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:2836:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:2841:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:2864:    VERDICT: PASS
011-phase-one-routing/intent/frame/review.md:2866:    VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:2868:    Then optionally add one NOTE: line. Treat uncertainty as FLAG.
011-phase-one-routing/intent/frame/review.md:2910:    and `check.sh`. Two coupled defects follow.
011-phase-one-routing/intent/frame/review.md:2936:      as `CODEX_BUILDER_MODEL` is materialization, named only in `adapter/loop.sh` and `check.sh`,
011-phase-one-routing/intent/frame/review.md:2951:    - Keep `./check.sh` green throughout, and make it prove both the product-name absence in the
011-phase-one-routing/intent/frame/review.md:2972:    the adapter prose, and `check.sh` express the harness binding in role and config terms with no
011-phase-one-routing/intent/frame/review.md:2975:    review floor's independence from the framer is stated; and `./check.sh` is green.
011-phase-one-routing/intent/frame/review.md:2979:    - `./check.sh` exits zero after implementation and after the archive fold.
011-phase-one-routing/intent/frame/review.md:3003:    Required proof: the observable-acceptance checks above, plus `check.sh` self-tests that a
011-phase-one-routing/intent/frame/review.md:3005:    reproduce current routing when the knobs are unset. Baseline `./check.sh` is green before
011-phase-one-routing/intent/frame/review.md:3013:    `check.sh` proves it; `hypercore.md` summarizes it; `adapter/codex.md` is the current
011-phase-one-routing/intent/frame/review.md:3018:    prose, and `check.sh` together — a half-de-named contract is a worse smell than the current
011-phase-one-routing/intent/frame/review.md:3032:    the current harness, `./check.sh` proves all of this and is green, and the sweep is coherent.
011-phase-one-routing/intent/frame/review.md:3054:    summary: De-name the whole contract (collaboration/loop/adapter statements and machine statements, the adapter prose, and check.sh) to role and config terms; add the phase-one collaborator role and a phase-one routing/delegation seam with held defaults; keep the materialization product-specific, including the existing CODEX_* environment-knob names, which are materialization config rather than contract.
011-phase-one-routing/intent/frame/review.md:3064:    tradeoff: Fullest product-agnostic surface, down to the environment-variable names; larger blast radius across the loop.sh env interface, check.sh, and any references to the knob names, with alias upkeep to avoid breaking existing CODEX_* configuration.
011-phase-one-routing/intent/frame/review.md:3076:    Overall: FLAG
011-phase-one-routing/intent/frame/review.md:3079:    Disposition: escalated - FLAG verdicts must be answered in the frame; optional reviewers are advisory only and cannot clear base-roster or red-team flags
011-phase-one-routing/intent/frame/review.md:3083:    - contract-checkability: FLAG
011-phase-one-routing/intent/frame/review.md:3084:    - soundness-fit: FLAG
011-phase-one-routing/intent/frame/review.md:3085:    - simplicity-fastness: FLAG
011-phase-one-routing/intent/frame/review.md:3086:    - red-team: FLAG
011-phase-one-routing/intent/frame/review.md:3118:    selected-output-source: final-output
011-phase-one-routing/intent/frame/review.md:3122:        VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:3127:        VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:3132:        VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:3155:        VERDICT: PASS
011-phase-one-routing/intent/frame/review.md:3157:        VERDICT: FLAG
011-phase-one-routing/intent/frame/review.md:3159:        Then optionally add one NOTE: line. Treat uncertainty as FLAG.
011-phase-one-routing/intent/frame/review.md:3186:        and `check.sh`. Two coupled defects follow.
011-phase-one-routing/intent/frame/review.md:3223:        - Keep `./check.sh` green throughout, and make it prove both the product-name absence in the
011-phase-one-routing/intent/frame/review.md:3243:        the adapter prose, and `check.sh` express the harness binding in role and config terms with no
011-phase-one-routing/intent/frame/review.md:3246:        review floor's independence from the framer is stated; and `./check.sh` is green.
011-phase-one-routing/intent/frame/review.md:3250:        - `./check.sh` exits zero after implementation and after the archive fold.
011-phase-one-routing/intent/frame/review.md:3273:        Required proof: the observable-acceptance checks above, plus `check.sh` self-tests that a
011-phase-one-routing/intent/frame/review.md:3275:        reproduce current routing when the knobs are unset. Baseline `./check.sh` is green before
011-phase-one-routing/intent/frame/review.md:3283:        `check.sh` proves it; `hypercore.md` summarizes it; `adapter/codex.md` is the current
011-phase-one-routing/intent/frame/review.md:3288:        prose, and `check.sh` together — a half-de-named contract is a worse smell than the current
011-phase-one-routing/intent/frame/review.md:3302:        the current harness, `./check.sh` proves all of this and is green, and the sweep is coherent.
011-phase-one-routing/intent/frame/review.md:3348:    green proof-advancing units, and stops when the frame is incomplete, a check fails, or
011-phase-one-routing/intent/frame/review.md:3349:    required implementation acceptance returns `FLAG`.
011-phase-one-routing/intent/frame/review.md:3356:    implement: build in proof-advancing units from the signed frame.
011-phase-one-routing/intent/frame/review.md:3357:    an implementation unit is the smallest proof-advancing delta that leaves `./check.sh`
011-phase-one-routing/intent/frame/review.md:3358:    green; units are vertical slices, so statements, material, and checks land together when
011-phase-one-routing/intent/frame/review.md:3362:    `./check.sh` is green at every phase-two unit boundary and before any acceptance verdict
011-phase-one-routing/intent/frame/review.md:3364:    after each implementation unit, a fresh independent read-only implementation-acceptance
011-phase-one-routing/intent/frame/review.md:3365:    reviewer reads the signed frame, unit proof obligation, unit diff, and lean unit handoff,
011-phase-one-routing/intent/frame/review.md:3366:    then returns a structured verdict: exactly one `PASS` or `FLAG` with required rationale and
011-phase-one-routing/intent/frame/review.md:3372:    `independent-coherence`, `security-permissions`, and `red-team`.
011-phase-one-routing/intent/frame/review.md:3373:    the `independent-coherence` lens carries the semantic sweep judgement for one-way archive;
011-phase-one-routing/intent/frame/review.md:3375:    missing, malformed, nonzero, unsupported-source, evidence-free, or non-`PASS`/`FLAG`
011-phase-one-routing/intent/frame/review.md:3376:    acceptance reviewer output counts as `FLAG`.
011-phase-one-routing/intent/frame/review.md:3384:    a unit build attempts the fast builder first, retries a failed unit up to three fast
011-phase-one-routing/intent/frame/review.md:3385:    attempts when `./check.sh` or tier-one acceptance fails, escalates that unit to the strong
011-phase-one-routing/intent/frame/review.md:3388:    execute is resumable from the signed frame and on-disk artifacts: a passed unit's build and
011-phase-one-routing/intent/frame/review.md:3389:    tier-one evidence is reused only when its cache key still matches the signed frame, unit
011-phase-one-routing/intent/frame/review.md:3390:    proof obligation, relevant prior-unit state, loop implementation version, recorded diff, and
011-phase-one-routing/intent/frame/review.md:3391:    green mechanical-check evidence, and a cache miss rebuilds the unit and invalidates
011-phase-one-routing/intent/frame/review.md:3392:    downstream unit evidence.
011-phase-one-routing/intent/frame/review.md:3393:    unresolved required tier-one or tier-two `FLAG`s halt phase two before archive; the active
011-phase-one-routing/intent/frame/review.md:3482:    `loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
011-phase-one-routing/intent/frame/review.md:3483:    fresh Codex builder session for each unit, and records lean unit handoff, diff, and
011-phase-one-routing/intent/frame/review.md:3487:    route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
011-phase-one-routing/intent/frame/review.md:3492:    rationale, evidence, and a `source:` marker, refuses `HYPERCORE_ACCEPTANCE_FAKE_DIR` outside
011-phase-one-routing/intent/frame/review.md:3493:    dry-run, and lets real archive accept only `source: real-reviewer` required acceptance.
011-phase-one-routing/intent/frame/review.md:3494:    `loop.sh execute <work-name>` caches per-unit build and tier-one evidence under a
011-phase-one-routing/intent/frame/review.md:3495:    signed-frame-derived key, skips unchanged accepted units on rerun, and rebuilds cache misses
011-phase-one-routing/intent/frame/review.md:3498:    implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
011-phase-one-routing/intent/frame/review.md:3523:    thread id, current unit, latest message, failure reason, event history, run artifact
011-phase-one-routing/intent/frame/review.md:3581:    `loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
011-phase-one-routing/intent/frame/review.md:3582:    fresh Codex builder session for each unit, and records lean unit handoff, diff, and
011-phase-one-routing/intent/frame/review.md:3586:    route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
011-phase-one-routing/intent/frame/review.md:3591:    rationale, evidence, and a `source:` marker, refuses `HYPERCORE_ACCEPTANCE_FAKE_DIR` outside
011-phase-one-routing/intent/frame/review.md:3592:    dry-run, and lets real archive accept only `source: real-reviewer` required acceptance.
011-phase-one-routing/intent/frame/review.md:3593:    `loop.sh execute <work-name>` caches per-unit build and tier-one evidence under a
011-phase-one-routing/intent/frame/review.md:3594:    signed-frame-derived key, skips unchanged accepted units on rerun, and rebuilds cache misses
011-phase-one-routing/intent/frame/review.md:3597:    implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
011-phase-one-routing/intent/frame/review.md:3625:    unresolved implementation-acceptance `FLAG`s are feedback material: they block archive and surface to the operator rather than being self-cleared, averaged away, outvoted, or treated as warnings.
011-phase-one-routing/intent/frame/review.md:3626:    implementation-acceptance signal is legible: a required acceptance verdict carries a parseable `PASS` or `FLAG` plus rationale and concrete evidence enough for the operator or a later machine to act on a `FLAG`; uncertainty still flags, and legibility makes the door actionable without weakening it.
011-phase-one-routing/intent/frame/review.md:3627:    build retry is bounded proof-floor recovery, not a structural re-decision: a builder may re-attempt a failed unit within the signed route, but structural mismatches, tier-two `FLAG`s, and an exhausted escalation budget still surface to the operator rather than being retried away.
011-phase-one-routing/intent/frame/review.md:3633:    the addressed work's current or recent gate, current unit, status, Codex thread id, latest
011-phase-one-routing/intent/frame/review.md:3644:    the addressed work's current or recent gate, current unit, status, Codex thread id, latest
011-phase-one-routing/intent/frame/review.md:3669:    and archive run through cleared sessions that re-derive each unit and acceptance review
011-phase-one-routing/intent/frame/review.md:3674:    the Codex implementation-acceptance reviewer for each phase-two unit is independent and
011-phase-one-routing/intent/frame/review.md:3677:    `whole-acceptance-conformance`, `proof-integrity`, `independent-coherence`,
011-phase-one-routing/intent/frame/review.md:3718:    over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
011-phase-one-routing/intent/frame/review.md:3728:    artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
011-phase-one-routing/intent/frame/review.md:3729:    then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
011-phase-one-routing/intent/frame/review.md:3761:    `check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
011-phase-one-routing/intent/frame/review.md:3785:    at the check gate the orchestrator records tier-one implementation acceptance for each
011-phase-one-routing/intent/frame/review.md:3786:    unit, records the concurrent one-way tier-two panel when required, and halts phase two
011-phase-one-routing/intent/frame/review.md:3809:    over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
011-phase-one-routing/intent/frame/review.md:3819:    artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
011-phase-one-routing/intent/frame/review.md:3820:    then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
011-phase-one-routing/intent/frame/review.md:3852:    `check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
011-phase-one-routing/intent/frame/review.md:3876:    at the check gate the orchestrator records tier-one implementation acceptance for each
011-phase-one-routing/intent/frame/review.md:3877:    unit, records the concurrent one-way tier-two panel when required, and halts phase two
011-phase-one-routing/intent/frame/review.md:3881:    VERDICT: FLAG
011-phase-one-routing/intent/frame/direction.md:6:selected-route: De-name the whole contract (collaboration/loop/adapter statements and machine statements, the adapter prose, and check.sh) to role and config terms; add the phase-one collaborator role and a phase-one routing/delegation seam with held defaults; keep the materialization product-specific, including the existing CODEX_* environment-knob names, which are materialization config rather than contract.
011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md:1:# handoff - unit-001
011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md:3:unit: unit-001
011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md:5:proof obligation: De-name the contract statements and add the phase-one roles, updating `check.sh` in lockstep so it stays green. Across `intent/collaboration.md`, `intent/loop.md`, `intent/adapter.md` and their `machine-statements/` counterparts, plus the adapter sections of `hypercore.md` and `intent/organizing-document.md`, apply the three-layer sort (methodology claim → role; capability → "the harness must support X"; current-binding fact → moved into `adapter/codex.md`); add the collaborator, throughput-delegation, review-floor-independent-of-framer, and phase-one-routing statements; and update `check.sh` to drop assertions that require the old product-named wording and add the scoped product-absence check with the pointer grammar, the role-statement-presence assertions, and the held-default assertions. `./check.sh` is green at the unit boundary.
011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md:7:builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260608T002351Z-root-011-phase-one-routing-pid310606/gates/implement-unit-001-fast-1.final.md
011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md:11:Built `unit-001`.
011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md:14:`adapter/codex.md`, `check.sh`, `hypercore.md`, `intent/adapter.md`, `intent/collaboration.md`, `intent/loop.md`, `intent/machine-statements/adapter.md`, `intent/machine-statements/collaboration.md`, `intent/machine-statements/loop.md`, `intent/organizing-document.md`.
011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md:17:`011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md`
011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md:18:`011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff`
011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md:21:`bash -n check.sh`
011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md:22:`./check.sh` - green after handoff/diff were written.
011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md:24:Proof gap: none for this unit.
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:1:# tier-one implementation acceptance - unit-001
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:3:reviewer: tier-one-unit-001-fast-1
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:4:Verdict: PASS
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:5:source: real-reviewer
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:7:Rationale: The unit satisfies the signed unit-001 obligation as a proof-advancing delta: it de-names the scoped contract statements, adds the phase-one collaborator/delegation/review-floor/routing statements in the owning intent files, moves current binding facts into `adapter/codex.md`, and wires `check.sh` to enforce the scoped product-absence grammar and role/default assertions.
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:8:Evidence: `011-phase-one-routing/intent/frame/frame.md` and `signoff.md` anchor the route and sign-off; `phase-two/handoffs/unit-001.md` reports `bash -n check.sh` and `./check.sh` green; `phase-two/diffs/unit-001.diff` shows the relevant edits. Current scoped files contain only whitelisted product pointers by targeted `rg`: contract hits are `adapter/codex.md`/`AGENTS.md` pointers, while `codex-cockpit` is outside the scanned organizing adapter scope. `check.sh` now contains `contract_statement_product_absence`, role-presence assertions, and held-default assertions.
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:12:Notes: structured acceptance verdict PASS with rationale and evidence
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:19:Unit: unit-001
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:20:Proof obligation: De-name the contract statements and add the phase-one roles, updating `check.sh` in lockstep so it stays green. Across `intent/collaboration.md`, `intent/loop.md`, `intent/adapter.md` and their `machine-statements/` counterparts, plus the adapter sections of `hypercore.md` and `intent/organizing-document.md`, apply the three-layer sort (methodology claim → role; capability → "the harness must support X"; current-binding fact → moved into `adapter/codex.md`); add the collaborator, throughput-delegation, review-floor-independent-of-framer, and phase-one-routing statements; and update `check.sh` to drop assertions that require the old product-named wording and add the scoped product-absence check with the pointer grammar, the role-statement-presence assertions, and the held-default assertions. `./check.sh` is green at the unit boundary.
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:22:Unit handoff: 011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:23:Unit diff record: 011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:24:Mechanical check immediately before this reviewer: check.sh green
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:26:Read only the signed frame, the intent it references, the unit handoff, and the unit diff record.
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:27:The unit diff record is a cumulative worktree snapshot after this unit, so it may include other already-built or planned unit changes. Check whether the handoff and proof-obligation-relevant diff content make this unit a proof-advancing delta toward the operator-signed acceptance; do not flag solely because unrelated cumulative diff hunks are present.
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:29:VERDICT: PASS
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:33:Use VERDICT: FLAG instead of VERDICT: PASS when the evidence is missing, stale, uncertain, or mismatched.
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:35:Treat uncertainty, missing evidence, or mismatch with the signed frame as FLAG.
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:39:VERDICT: PASS
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:40:RATIONALE: The unit satisfies the signed unit-001 obligation as a proof-advancing delta: it de-names the scoped contract statements, adds the phase-one collaborator/delegation/review-floor/routing statements in the owning intent files, moves current binding facts into `adapter/codex.md`, and wires `check.sh` to enforce the scoped product-absence grammar and role/default assertions.
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md:41:EVIDENCE: `011-phase-one-routing/intent/frame/frame.md` and `signoff.md` anchor the route and sign-off; `phase-two/handoffs/unit-001.md` reports `bash -n check.sh` and `./check.sh` green; `phase-two/diffs/unit-001.diff` shows the relevant edits. Current scoped files contain only whitelisted product pointers by targeted `rg`: contract hits are `adapter/codex.md`/`AGENTS.md` pointers, while `codex-cockpit` is outside the scanned organizing adapter scope. `check.sh` now contains `contract_statement_product_absence`, role-presence assertions, and held-default assertions.
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:7:Tracked changes only; untracked files are excluded from this unit diff record.
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:17: M check.sh
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:57:diff --git a/check.sh b/check.sh
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:59:--- a/check.sh
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:60:+++ b/check.sh
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:137:   "resumable per-unit execute cache" \
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:188: [ -x "$root/check.sh" ] \
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:189:   && ok "check.sh exists and is executable" \
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:190:   || bad "check.sh is missing or not executable"
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:211: and archive run through cleared sessions that re-derive each unit and acceptance review
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:217:-the Codex implementation-acceptance reviewer for each phase-two unit is independent and
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:220:+the implementation-acceptance reviewer for each phase-two unit is independent and read-only.
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:222: `whole-acceptance-conformance`, `proof-integrity`, `independent-coherence`,
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:275:-over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:280:+over the phase-two executor harness: each implementation unit opens a fresh builder
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:292: artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:293: then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:303:-`check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:304:+`check.sh` mechanically checks that the gate prompts, adapter prose, loop frame
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:345:-the addressed work's current or recent gate, current unit, status, Codex thread id, latest
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:346:+the addressed work's current or recent gate, current unit, status, harness session id, latest
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:354:@@ -60,6 +60,10 @@ acceptance reviewer output counts as `FLAG`.
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:386: `loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:387:-fresh Codex builder session for each unit, and records lean unit handoff, diff, and
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:391:-route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:393:+fresh builder session for each unit, and records lean unit handoff, diff, and tier-one
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:397:+review route; it gives each unit a three-attempt fast-builder budget, escalates an
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:398:+exhausted unit through the strong-builder model knob, and stops for the operator when the
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:430:-over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:435:+over the phase-two executor harness: each implementation unit opens a fresh builder
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:447: artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:448: then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:458:-`check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:459:+`check.sh` mechanically checks that the gate prompts, adapter prose, loop frame
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:482:-the addressed work's current or recent gate, current unit, status, Codex thread id, latest
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:483:+the addressed work's current or recent gate, current unit, status, harness session id, latest
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:495:-thread id, current unit, latest message, failure reason, event history, run artifact
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:497:+session id, current unit, latest message, failure reason, event history, run artifact
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:512: `loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:513:-fresh Codex builder session for each unit, and records lean unit handoff, diff, and
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:517:-route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:519:+fresh builder session for each unit, and records lean unit handoff, diff, and tier-one
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:523:+review route; it gives each unit a three-attempt fast-builder budget, escalates an
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:524:+exhausted unit through the strong-builder model knob, and stops for the operator when the
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff:533:@@ -19,8 +19,8 @@ leaf-materialized by `hypercore.md` and `check.sh`, divided along one axis:
011-phase-one-routing/intent/frame/phase-two/units/unit-001.md:1:# phase-two unit - unit-001
011-phase-one-routing/intent/frame/phase-two/units/unit-001.md:3:unit: unit-001
011-phase-one-routing/intent/frame/phase-two/units/unit-001.md:6:proof-obligation: De-name the contract statements and add the phase-one roles, updating `check.sh` in lockstep so it stays green. Across `intent/collaboration.md`, `intent/loop.md`, `intent/adapter.md` and their `machine-statements/` counterparts, plus the adapter sections of `hypercore.md` and `intent/organizing-document.md`, apply the three-layer sort (methodology claim → role; capability → "the harness must support X"; current-binding fact → moved into `adapter/codex.md`); add the collaborator, throughput-delegation, review-floor-independent-of-framer, and phase-one-routing statements; and update `check.sh` to drop assertions that require the old product-named wording and add the scoped product-absence check with the pointer grammar, the role-statement-presence assertions, and the held-default assertions. `./check.sh` is green at the unit boundary.
011-phase-one-routing/intent/frame/phase-two/units/unit-001.md:7:handoff-path: 011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md
011-phase-one-routing/intent/frame/phase-two/units/unit-001.md:8:diff-path: 011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff
011-phase-one-routing/intent/frame/phase-two/units/unit-001.md:9:tier-one-verdict-path: 011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md
011-phase-one-routing/intent/frame/phase-two/units/unit-001.md:10:cache-key-path: 011-phase-one-routing/intent/frame/phase-two/cache/unit-001.key

codex
The extra `999-...` directory has a signed frame, so it is a real active work node in the root tree unless intentionally created as a disposable fixture. I’m checking whether its target overlaps this work’s routing contract.
exec
/bin/bash -lc "sed -n '1,260p' 999-check-loop-frame-contract-565249/intent/frame/frame.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# frame - self-test

## work

Addressed node: root

Node-local work name: 999-check-loop-frame-contract-565249

Target segments: loop

Work in flight: none

## problem

Lean contract completeness self-test.

## constraints

Keep this frame intentionally narrow.

## decision surface or open direction

The operator direction surface is named.

Reversibility: two-way

## route

Exercise phase-two acceptance in dry-run.

Implementation units for phase two:

1. First acceptance dry-run unit: prove tier-one behavior.
2. Second acceptance dry-run unit: prove full-panel ordering.

## acceptance condition

The loop reports frame_complete=yes for complete test cases.

## observable acceptance

Run loop status for this self-test work.

## excluded interpretation

This self-test does not adopt parent intent.

## proof state

The proof state is recorded.

## sweep

The sweep is recorded.

## adoption claim

The adoption claim is recorded.

exec
/bin/bash -lc "sed -n '1,120p' 999-check-loop-frame-contract-565249/intent/frame/signoff.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# signoff - 999-check-loop-frame-contract-565249

signed-off-by: qqp-dev
signed-off-at: 2026-06-07T00:00:00Z
operator-gate: tty

exec
/bin/bash -lc "sed -n '1,160p' 999-check-loop-frame-contract-565249/intent/frame/direction.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# direction - 999-check-loop-frame-contract-565249

direction-by: qqp-dev
direction-given-at: 2026-06-07T00:00:00Z
operator-gate: tty
selected-route: operator chose route

exec
/bin/bash -lc "sed -n '1,120p' 999-check-loop-frame-contract-565249/intent/organizing-document.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# organizing document - 999-check-loop-frame-contract-565249

This work node keeps its design frame under intent/frame/.

codex
That `999-...` node is a check fixture for loop frame completeness, not a parent intent amendment for the routing contract. I’ll now verify the scoped product grammar and route-required statements directly from the current worktree.
exec
/bin/bash -lc "rg -n 'codex exec|Codex thread|raw Codex JSON|CODEX_\\*|interactive Codex harness|symlinked to|Nested work|phase one and phase two' adapter/codex.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
20:The current root binding is Codex. The root `AGENTS.md` entry point is symlinked to
22:Nested work under this root receives that entry point through the project instruction
25:The current materialization binds Codex to both phase one and phase two. Phase one defaults
26:to the interactive Codex harness that loaded this adapter. Phase two is driven by
27:`adapter/loop.sh`, which invokes fresh `codex exec` sessions for builders, reviewers, and
28:the archive actor; the orchestrator records raw Codex JSON event streams and Codex thread
31:The current materialization also keeps the `CODEX_*` environment knob names in

exec
/bin/bash -lc "rg -n 'the phase-one collaborator is the harness role that drives orient and frame|phase-one corpus-throughput work|the framer is not its own witness|phase-one labor may be routed by role|the collaborator role defaults to the interactive harness that loaded the adapter|an adapter binds a harness to a phase|current materialization binds the same harness to phase one and phase two|builder-model, strong-builder, review-model, and review-effort roles|Pin the strong review floor|Re-prompt phase-one one-way review' intent/collaboration.md intent/loop.md intent/adapter.md intent/machine-statements/adapter.md adapter/codex.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
adapter/codex.md:33:builder-model, strong-builder, review-model, and review-effort roles.
adapter/codex.md:133:- **Pin the strong review floor.** The strong review floor is not yet mechanically pinned
adapter/codex.md:136:- **Re-prompt phase-one one-way review.** The current phase-one one-way review reviewer
intent/machine-statements/adapter.md:4:the current materialization binds the same harness to phase one and phase two; the
intent/adapter.md:45:an adapter binds a harness to a phase; phase one and phase two may bind different harnesses,
intent/adapter.md:60:the current materialization binds the same harness to phase one and phase two; the
intent/collaboration.md:8:the phase-one collaborator is the harness role that drives orient and frame: it carries
intent/collaboration.md:10:phase-one corpus-throughput work -- research, the orient corpus read, and the sweep map --
intent/collaboration.md:18:collaborator that framed it; the framer is not its own witness.
intent/loop.md:63:phase-one labor may be routed by role: the collaborator drives operator-facing orient and
intent/loop.md:66:the collaborator role defaults to the interactive harness that loaded the adapter.

exec
/bin/bash -lc "perl -0ne '
my "'$text=$_; if ($ARGV =~ /hypercore'"\\.md"'$/) { $text = ($text =~ /''^## adapter'"\\n(.*?)(?="'^## |'"\\z)/ms) ? "'$1 : ""; } elsif ($ARGV =~ /organizing-document'"\\.md"'$/) { my @kept; my $taking=0; for my $line (split /'"\\n/, "'$text) { if ($line =~ /''^- '"\\*\\*adapter\\*\\*/) { "'$taking=1; } elsif ($taking && $line =~ /''^'"\\s*"'$/) { last; } push @kept, $line if $taking; } $text=join("'"\\n\", @kept).\"\\n\"; }
my %allowed=map { "'$_=>1 } qw(adapter/codex.md AGENTS.md adapter/codex-mounted.md adapter/loop.sh);
my @spans; while ($text =~ /`([''^`'"\\n]+)"'`/g) { push @spans, [$-[1], $+[1], $1]; }
my $product=qr/(?<![A-Za-z0-9_])(?:codex|claude|opus|gpt-[0-9][A-Za-z0-9._-]*|CODEX_[A-Za-z0-9_]*)(?![A-Za-z0-9_])/i;
while ($text =~ /$product/g) { my ($s,$e,$tok)=($-[0],$+[0],$&); my $ok=0; for my $span (@spans) { if ($s >= $span->[0] && $e <= $span->[1] && $allowed{$span->[2]}) { $ok=1; last; } } next if $ok; my $prefix=substr($text,0,$s); my $line=1+($prefix=~tr/'"\\n//); print \""'$ARGV:$line:$tok'"\\n\"; }
' intent/collaboration.md intent/loop.md intent/adapter.md intent/machine-statements/collaboration.md intent/machine-statements/loop.md intent/machine-statements/adapter.md hypercore.md intent/organizing-document.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
exec
/bin/bash -lc 'git --no-pager diff --stat -- intent/collaboration.md intent/loop.md intent/adapter.md intent/machine-statements/collaboration.md intent/machine-statements/loop.md intent/machine-statements/adapter.md hypercore.md intent/organizing-document.md adapter/codex.md adapter/loop.sh check.sh' in /home/qqp/projects/hypercore
 succeeded in 0ms:
 adapter/codex.md                           |  23 +++
 adapter/loop.sh                            |   2 +-
 check.sh                                   | 216 +++++++++++++++++++++++++++++
 hypercore.md                               |   4 +-
 intent/adapter.md                          |  55 ++++----
 intent/collaboration.md                    |   9 +-
 intent/loop.md                             |  28 ++--
 intent/machine-statements/adapter.md       |  36 ++---
 intent/machine-statements/collaboration.md |   2 +-
 intent/machine-statements/loop.md          |  24 ++--
 intent/organizing-document.md              |   4 +-
 11 files changed, 332 insertions(+), 71 deletions(-)

codex
The scoped product-token check produced no violations, and the required role/default statements are present in the expected files. I’m doing one final syntax/basic consistency pass over the material scripts before I return the panel verdict.
exec
/bin/bash -lc 'bash -n check.sh' in /home/qqp/projects/hypercore
 succeeded in 0ms:
exec
/bin/bash -lc 'bash -n adapter/loop.sh' in /home/qqp/projects/hypercore
 succeeded in 0ms:
exec
/bin/bash -lc "sed -n '1,80p' adapter/loop.sh" in /home/qqp/projects/hypercore
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

exec
/bin/bash -lc "sed -n '300,365p' adapter/loop.sh && sed -n '2540,2810p' adapter/loop.sh && sed -n '3000,3020p' adapter/loop.sh" in /home/qqp/projects/hypercore
 succeeded in 0ms:
    return 0
  fi
  rm -f "$probe" 2>/dev/null || true
  return 1
}

phase_two_preflight_fail() {
  local reason=$1 work_name=$2 msg
  msg="preflight failed before codex exec: $reason; rerun the outer loop with that permission, using: $(loop_execute_command "$work_name")"
  loop_event preflight preflight failed "$msg"
  loop_state_write preflight failed "$msg"
  printf 'phase-two preflight failed: %s\n' "$reason" >&2
  printf 'rerun with outer escalation: %s\n' "$(loop_execute_command "$work_name")" >&2
  return 1
}

phase_two_preflight() {
  local work_name=$1 codex_home codex_parent reason msg
  LOOP_CURRENT_GATE=preflight
  msg="checking Codex binary and writable Codex home/session state"
  loop_event preflight preflight running "$msg"
  loop_state_write preflight running "$msg"

  if [ "$DRY_RUN" = 1 ]; then
    msg="dry-run: would check Codex binary and Codex home/session write permission before launching codex exec"
    loop_event preflight preflight skipped "$msg"
    loop_state_write preflight skipped "$msg"
    return 0
  fi

  command -v "$CODEX_BIN" >/dev/null 2>&1 \
    || phase_two_preflight_fail "Codex binary '$CODEX_BIN' is not on PATH" "$work_name" \
    || return 1

  if [ -n "${CODEX_HOME:-}" ]; then
    codex_home=$CODEX_HOME
  else
    [ -n "${HOME:-}" ] \
      || phase_two_preflight_fail "HOME is unset and CODEX_HOME is not set, so Codex home cannot be resolved" "$work_name" \
      || return 1
    codex_home=$HOME/.codex
  fi

  if [ -d "$codex_home/sessions" ]; then
    can_write_dir "$codex_home/sessions" \
      || reason="missing write permission for Codex sessions directory $codex_home/sessions"
  elif [ -d "$codex_home" ]; then
    can_write_dir "$codex_home" \
      || reason="missing write permission to create Codex sessions under $codex_home"
  else
    codex_parent="$(dirname "$codex_home")"
    can_write_dir "$codex_parent" \
      || reason="missing write permission to create Codex home $codex_home under $codex_parent"
  fi

  [ -z "${reason:-}" ] \
    || phase_two_preflight_fail "$reason" "$work_name" \
    || return 1

  msg="preflight passed: Codex binary is present and $codex_home can hold session state"
  loop_event preflight preflight passed "$msg"
  loop_state_write preflight passed "$msg"
}

ensure_work_history() {
  local d
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

codex
I have enough evidence for the coherence lens now: the token sweep is clean under the signed grammar, the role/config statements are present, the current-binding facts are present in `adapter/codex.md`, and the material scripts parse.
exec
/bin/bash -lc 'ls -l AGENTS.md adapter/codex.md adapter/loop.sh check.sh' in /home/qqp/projects/hypercore
 succeeded in 0ms:
lrwxrwxrwx 1 qqp qqp     16 Jun  6 18:06 AGENTS.md -> adapter/codex.md
-rw-rw-r-- 1 qqp qqp   9181 Jun  7 19:52 adapter/codex.md
-rwxrwxr-x 1 qqp qqp 134321 Jun  7 19:52 adapter/loop.sh
-rwxrwxr-x 1 qqp qqp 118773 Jun  7 19:52 check.sh

exec
/bin/bash -lc "sed -n '1,60p' 011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# handoff - unit-001

unit: unit-001

proof obligation: De-name the contract statements and add the phase-one roles, updating `check.sh` in lockstep so it stays green. Across `intent/collaboration.md`, `intent/loop.md`, `intent/adapter.md` and their `machine-statements/` counterparts, plus the adapter sections of `hypercore.md` and `intent/organizing-document.md`, apply the three-layer sort (methodology claim → role; capability → "the harness must support X"; current-binding fact → moved into `adapter/codex.md`); add the collaborator, throughput-delegation, review-floor-independent-of-framer, and phase-one-routing statements; and update `check.sh` to drop assertions that require the old product-named wording and add the scoped product-absence check with the pointer grammar, the role-statement-presence assertions, and the held-default assertions. `./check.sh` is green at the unit boundary.

builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260608T002351Z-root-011-phase-one-routing-pid310606/gates/implement-unit-001-fast-1.final.md

## builder final output

Built `unit-001`.

Changed files:
`adapter/codex.md`, `check.sh`, `hypercore.md`, `intent/adapter.md`, `intent/collaboration.md`, `intent/loop.md`, `intent/machine-statements/adapter.md`, `intent/machine-statements/collaboration.md`, `intent/machine-statements/loop.md`, `intent/organizing-document.md`.

Unit artifacts written:
`011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md`
`011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff`

Prepared checks:
`bash -n check.sh`
`./check.sh` - green after handoff/diff were written.

Proof gap: none for this unit.

exec
/bin/bash -lc "sed -n '1,45p' 011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# tier-one implementation acceptance - unit-001

reviewer: tier-one-unit-001-fast-1
Verdict: PASS
source: real-reviewer
source-proof: real reviewer subprocess completed through codex exec with literal approval never and literal sandbox read-only
Rationale: The unit satisfies the signed unit-001 obligation as a proof-advancing delta: it de-names the scoped contract statements, adds the phase-one collaborator/delegation/review-floor/routing statements in the owning intent files, moves current binding facts into `adapter/codex.md`, and wires `check.sh` to enforce the scoped product-absence grammar and role/default assertions.
Evidence: `011-phase-one-routing/intent/frame/frame.md` and `signoff.md` anchor the route and sign-off; `phase-two/handoffs/unit-001.md` reports `bash -n check.sh` and `./check.sh` green; `phase-two/diffs/unit-001.diff` shows the relevant edits. Current scoped files contain only whitelisted product pointers by targeted `rg`: contract hits are `adapter/codex.md`/`AGENTS.md` pointers, while `codex-cockpit` is outside the scanned organizing adapter scope. `check.sh` now contains `contract_statement_product_absence`, role-presence assertions, and held-default assertions.
dry-run: no
Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Notes: structured acceptance verdict PASS with rationale and evidence

## prompt

Implementation-acceptance reviewer: tier one
Work: 011-phase-one-routing
Node: .
Unit: unit-001
Proof obligation: De-name the contract statements and add the phase-one roles, updating `check.sh` in lockstep so it stays green. Across `intent/collaboration.md`, `intent/loop.md`, `intent/adapter.md` and their `machine-statements/` counterparts, plus the adapter sections of `hypercore.md` and `intent/organizing-document.md`, apply the three-layer sort (methodology claim → role; capability → "the harness must support X"; current-binding fact → moved into `adapter/codex.md`); add the collaborator, throughput-delegation, review-floor-independent-of-framer, and phase-one-routing statements; and update `check.sh` to drop assertions that require the old product-named wording and add the scoped product-absence check with the pointer grammar, the role-statement-presence assertions, and the held-default assertions. `./check.sh` is green at the unit boundary.
Signed frame directory: 011-phase-one-routing/intent/frame
Unit handoff: 011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md
Unit diff record: 011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff
Mechanical check immediately before this reviewer: check.sh green

Read only the signed frame, the intent it references, the unit handoff, and the unit diff record.
The unit diff record is a cumulative worktree snapshot after this unit, so it may include other already-built or planned unit changes. Check whether the handoff and proof-obligation-relevant diff content make this unit a proof-advancing delta toward the operator-signed acceptance; do not flag solely because unrelated cumulative diff hunks are present.
Return exactly these required fields, with exactly one VERDICT line:
VERDICT: PASS
RATIONALE: the frame-anchored reason for the verdict
EVIDENCE: concrete artifact paths, command results, or missing evidence that supports the verdict

Use VERDICT: FLAG instead of VERDICT: PASS when the evidence is missing, stale, uncertain, or mismatched.

Treat uncertainty, missing evidence, or mismatch with the signed frame as FLAG.

## raw output

VERDICT: PASS
RATIONALE: The unit satisfies the signed unit-001 obligation as a proof-advancing delta: it de-names the scoped contract statements, adds the phase-one collaborator/delegation/review-floor/routing statements in the owning intent files, moves current binding facts into `adapter/codex.md`, and wires `check.sh` to enforce the scoped product-absence grammar and role/default assertions.
EVIDENCE: `011-phase-one-routing/intent/frame/frame.md` and `signoff.md` anchor the route and sign-off; `phase-two/handoffs/unit-001.md` reports `bash -n check.sh` and `./check.sh` green; `phase-two/diffs/unit-001.diff` shows the relevant edits. Current scoped files contain only whitelisted product pointers by targeted `rg`: contract hits are `adapter/codex.md`/`AGENTS.md` pointers, while `codex-cockpit` is outside the scanned organizing adapter scope. `check.sh` now contains `contract_statement_product_absence`, role-presence assertions, and held-default assertions.

codex
VERDICT: PASS
RATIONALE: The built result coheres with the signed Option 1 route: the contract is de-named into role/capability language, the phase-one collaborator/routing/delegation seam and framer-independent review floor are stated consistently, and current Codex binding facts remain preserved in materialization without contradicting the methodology.
EVIDENCE: Scoped product-token scan over the enumerated statement files returned no violations; `rg` finds the required collaborator/delegation/framer-independence/routing/default/debt statements in `intent/collaboration.md`, `intent/loop.md`, `intent/adapter.md`, and `adapter/codex.md`; `adapter/codex.md:20-33` preserves the current binding facts; `AGENTS.md -> adapter/codex.md`; phase-two handoff/tier-one artifacts report `./check.sh` green; `bash -n check.sh` and `bash -n adapter/loop.sh` exited 0.
hook: Stop
hook: Stop Completed
tokens used
84,427
VERDICT: PASS
RATIONALE: The built result coheres with the signed Option 1 route: the contract is de-named into role/capability language, the phase-one collaborator/routing/delegation seam and framer-independent review floor are stated consistently, and current Codex binding facts remain preserved in materialization without contradicting the methodology.
EVIDENCE: Scoped product-token scan over the enumerated statement files returned no violations; `rg` finds the required collaborator/delegation/framer-independence/routing/default/debt statements in `intent/collaboration.md`, `intent/loop.md`, `intent/adapter.md`, and `adapter/codex.md`; `adapter/codex.md:20-33` preserves the current binding facts; `AGENTS.md -> adapter/codex.md`; phase-two handoff/tier-one artifacts report `./check.sh` green; `bash -n check.sh` and `bash -n adapter/loop.sh` exited 0.
