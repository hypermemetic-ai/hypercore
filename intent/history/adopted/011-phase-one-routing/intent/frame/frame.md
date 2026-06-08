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
acceptance, excluded interpretation, and route deliverables above.

## sweep

Map: `collaboration` owns role partition, reliance, and the new phase-one routing principle;
`loop` owns gate order and the routing statements (sibling to the existing phase-two
builder-routing line); `adapter` owns harness binding, materialization, and config seams;
`check.sh` proves it; `hypercore.md` summarizes it; `adapter/codex.md` is the current
materialization. The general rule "an adapter is per harness" already supports multi-harness
binding and does not conflict — this work makes the rest of the contract consistent with it.

Read: the change is coherent only if the de-naming lands across intent, machine statements,
prose, and `check.sh` together — a half-de-named contract is a worse smell than the current
uniform product naming (the same lesson `007` recorded: replace everywhere or nowhere). The
adjacency to `TWO-STEP-BUILD` is parallel, not colliding: that work routes the phase-two
builder; this routes phase-one labor; different phase, different knobs. No active work node
collides.

Verdict: coherent provided the contract is de-named atomically and the
materialization/config boundary holds.

## adoption claim

Adopt if the contract is product-agnostic (no harness product token in any contract
statement), the phase-one collaborator role and routing seam exist with held defaults, the
review-floor-independent-of-the-framer statement is present, the materialization still binds
the current harness, `./check.sh` proves all of this and is green, and the sweep is coherent.

## shelving claim

Shelve if the contract cannot be de-named without breaking the materialization boundary or
the proof floor; if the product-absence check proves too brittle (false positives on
legitimate materialization pointers); if the held defaults cannot reproduce current behavior;
or if the full scope cannot land coherently in one node, in which case the work shelves and
re-frames at a smaller scope rather than weakening this frame's acceptance condition.
