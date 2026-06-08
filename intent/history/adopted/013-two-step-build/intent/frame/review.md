# review - 013-two-step-build

Overall: FLAG
Isolation: reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Disposition: escalated - FLAG verdicts must be answered in the frame; optional reviewers are advisory only and cannot clear base-roster or red-team flags

## base roster verdicts

- contract-checkability: FLAG
- soundness-fit: FLAG
- simplicity-fastness: FLAG
- red-team: FLAG

## unresolved flags

- contract-checkability (base): The frame leaves route as `PENDING` and makes acceptance depend on “the selected option’s specifics,” so the signed contract is not determinate enough to check.
- soundness-fit (base): The frame still has open direction and `route: PENDING`, so soundness-fit cannot verify a signed, route-settled work contract.
- simplicity-fastness (base): The frame is pre-direction with `route` still `PENDING`, so simplicity/fastness cannot validate a concrete route; uncertainty flags.
- red-team (base): The frame is not signed or route-settled: `route` is PENDING/open direction and the frame directory lacks `direction.md` and `signoff.md`.

## reviewer notes

### contract-checkability

The frame leaves route as `PENDING` and makes acceptance depend on “the selected option’s specifics,” so the signed contract is not determinate enough to check.

### soundness-fit

The frame still has open direction and `route: PENDING`, so soundness-fit cannot verify a signed, route-settled work contract.

### simplicity-fastness

The frame is pre-direction with `route` still `PENDING`, so simplicity/fastness cannot validate a concrete route; uncertainty flags.

### red-team

The frame is not signed or route-settled: `route` is PENDING/open direction and the frame directory lacks `direction.md` and `signoff.md`.

## reviewer diagnostics

### contract-checkability

status: 0
selected-output-source: final-output

#### selected output

    VERDICT: FLAG
    NOTE: The frame leaves route as `PENDING` and makes acceptance depend on “the selected option’s specifics,” so the signed contract is not determinate enough to check.

#### final output

    VERDICT: FLAG
    NOTE: The frame leaves route as `PENDING` and makes acceptance depend on “the selected option’s specifics,” so the signed contract is not determinate enough to check.

#### stdout

    VERDICT: FLAG
    NOTE: The frame leaves route as `PENDING` and makes acceptance depend on “the selected option’s specifics,” so the signed contract is not determinate enough to check.

#### stderr

    OpenAI Codex v0.137.0
    --------
    workdir: /home/qqp/projects/hypercore
    model: gpt-5.5
    provider: openai
    approval: never
    sandbox: read-only
    reasoning effort: xhigh
    reasoning summaries: none
    session id: 019ea5d0-a018-7760-90c2-bde3b99418b0
    --------
    user
    Review role: contract-checkability
    Work: 013-two-step-build
    Frame directory: 013-two-step-build/intent/frame
    
    Read only the signed work frame and the intent it references. Do not debate other reviewers.
    Return exactly one structured verdict line:
    VERDICT: PASS
    or
    VERDICT: FLAG
    
    Then optionally add one NOTE: line. Treat uncertainty as FLAG.
    hook: UserPromptSubmit
    hook: UserPromptSubmit Completed
    codex
    I’ll inspect only the signed frame artifacts and the intent segments named by that frame, then return the requested one-line verdict.
    exec
    /bin/bash -lc 'rg --files 013-two-step-build/intent/frame' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    013-two-step-build/intent/frame/options.md
    013-two-step-build/intent/frame/frame.md
    
    exec
    /bin/bash -lc "sed -n '1,240p' 013-two-step-build/intent/frame/frame.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # frame - 013-two-step-build
    
    ## work
    
    Addressed node: root (hypercore)
    
    Node-local work name: 013-two-step-build
    
    Target segments: loop, adapter
    
    Work in flight: none other in flight (tree clean after the cache-removal commit `91f12aa`
    and the Claude-adapter-draft commit `60fb127`). Related but unadopted scratch:
    `DECOMPOSITION-FINDINGS.md` (seed-unit decomposition) and `WORK-NODE-COLLAPSE-FINDINGS.md`
    — ephemeral, not intent, read for coherence only. This frame derives from
    `TWO-STEP-BUILD-FINDINGS.md` (ephemeral seed, 2026-06-07), which is not itself intent.
    
    ## problem
    
    The signed frame today serves three consumers at one altitude and is compromised for all
    three: the operator signs it, the builder implements from it, and the acceptance panel
    judges against it. The result is dense feature-altitude units. Concrete evidence: work
    unit-003 (in 010) bundled builder/reviewer routing, the retry budget, strong escalation,
    operator-stop, and self-tests into one paragraph, and the gpt-5.5 build trace shows the
    builder *diagnosing architecture* and exercising feature-level judgement — not applying
    mechanical edits. Because units demand that judgement, the builder default is held at the
    strong model (`gpt-5.5`), and 010's cheap-builder (`gpt-5.3-codex-spark`) routing is an
    untested, unsafe bet: no work node has ever been built by spark. There is no artifact at an
    altitude a cheap builder can execute safely.
    
    ## constraints
    
    - C1 (settled, not re-opened): lean hard into two-step — frame -> (strong) plan -> (cheap)
      build is the path, not a maybe.
    - C2: the frame optimizes for operator + panel legibility — clear, separate, falsifiable
      statements; count bounded to *ownable claims*, not edits.
    - C3 (the guardrail): floor of judgeability. The frame stops being load-bearing in
      *execution* but stays load-bearing in *acceptance* — the panel must still be able to FLAG
      a wrong result against a frame statement *without reading code*. Legibility must never
      drift into "soft." Altitude test: judgeable-without-the-diff -> frame statement;
      only-means-something-next-to-the-diff -> task.
    - C4: spark executes *tasks*, never features; no node is ever built by spark at feature
      altitude. The strong model builds non-decomposable units directly (the proactive form of
      010's reactive three-fail escalation ladder).
    - C5: planner faithfulness is a new load-bearing seam. A strong model *planning* is not the
      same as the plan being *faithful to the frame*; a faithful-looking-but-wrong plan is a new
      way to ship a defect and must be caught by a check before the build trusts it.
    - C6 (operator info-gain lean, 2026-06-08): plan placement is a per-unit sub-step at the
      head of each build, not a whole-phase pass. Both route options honor this.
    - C7: `./check.sh` stays the proof floor, green at every phase-two unit boundary. 010's
      routing / retry / strong-escalation machinery and 008's tier-one + tier-two acceptance are
      extended, not replaced.
    - C8: on adoption, flip the builder default `gpt-5.5 -> gpt-5.3-codex-spark` (the held knob),
      because spark now executes tasks behind a legible review — the configuration that makes it
      safe. The strong-builder escalation knob stays intact.
    
    ## decision surface or open direction
    
    Open direction — needs operator selection via `./direction` from `options.md`. Per-unit
    placement (C6) is set by the operator's info-gain lean; the options differ on how much new
    governance and visibility surface the plan step carries:
    
    1. Plan visibility — sub-signature only (never surfaced) vs surfaced read-only to the operator.
    2. Non-decomposable declaration — planner self-report vs an explicit signal a check ratifies.
    3. Plan-faithfulness check — reuse the seed-unit "faithful carve" tier-one variant vs a
       purpose-built sibling `plan-faithfulness` lens.
    4. Altitude line — ratify the judgeability test as-is vs ratify-and-sharpen with baked-in
       frame-vs-task examples.
    
    These bundle into the two numbered options. Route is left open until `./direction`.
    
    Reversibility: one-way
    
    ## route
    
    PENDING — open direction. To be copied verbatim from the operator-selected numbered option
    in `options.md` at `./direction`. (Methodology-level loop/adapter contract change plus the
    spark builder flip, which accrues hard-to-revert build state; defaults one-way.)
    
    ## acceptance condition
    
    The loop gains a per-unit strong-model **plan** sub-step between the signed frame and the
    cheap build; the frame's altitude is governed by the floor of judgeability (C3); a
    plan-faithfulness check gates each plan before its build is trusted; non-decomposable units
    route to the strong builder; the builder default flips to `gpt-5.3-codex-spark`; `./check.sh`
    proves the new contract structurally; and for this one-way work the tier-two panel passes
    before archive. The selected option's specifics (visibility, faithfulness check shape,
    non-decomposable declaration, altitude wording) are honored by the build.
    
    ## observable acceptance
    
    - `./check.sh` exits 0 with new structural assertions that: (a) `loop` and `adapter` intent
      carry the plan-step, floor-of-judgeability, and plan-faithfulness statements; (b)
      `adapter/loop.sh` routes a per-unit plan sub-step through a strong-planner model knob
      *ahead of* the spark build, and exposes that knob; (c) the builder default token is
      `gpt-5.3-codex-spark`; (d) a plan-faithfulness verdict artifact is required per unit before
      that unit's build is trusted.
    - A dry-run / self-test of `loop.sh execute` records, per unit and in order, a strong-model
      plan artifact, then a plan-faithfulness verdict, then the (spark) build artifact, then the
      tier-one verdict — visible under the run's frame artifacts.
    
    ## excluded interpretation
    
    This work must NOT mean any of:
    
    - that the frame becomes "soft" or non-falsifiable — legibility is *to the floor of
      judgeability*, never below it; the panel must still FLAG a wrong result without reading code.
    - that any node is built by spark at feature altitude — spark executes tasks only;
      non-decomposable units go to the strong builder.
    - that the plan is signed by the operator or becomes operator-owned intent — the plan is
      sub-signature build material, not a frame and not a statement.
    - that 010's routing/retry/escalate or 008's acceptance tiers are replaced — they are extended.
    - that a strong model *planning* discharges faithfulness — the plan-faithfulness check is
      required, not optional or self-cleared.
    
    ## proof state
    
    Unproven until built: the plan-step contract (strong-planner knob present and ordered before
    the build; builder default = spark; per-unit plan-faithfulness artifact required) asserted by
    `./check.sh` and demonstrated by a dry-run execute trace. Existing 010 (routing/retry/escalate,
    resumable execute) and 008 (tier-one + tier-two acceptance) proofs are preserved and must stay
    green.
    
    ## sweep
    
    Concept map and likely clashes:
    
    - "fast builder / builder default held at strong until two-step lands" appears in
      `intent/loop.md`, `intent/machine-statements/loop.md`, `intent/adapter.md`,
      `intent/machine-statements/adapter.md`, `adapter/loop.sh` (header + `CODEX_BUILDER_MODEL`
      default + the two-step note), `adapter/codex.md`, `adapter/claude.md`, and `check.sh`
      assertions. Every "held until two-step lands" clause must flip to "two-step has landed;
      default is spark." This is the central coherence obligation.
    - Resumable execute was just rewritten by `91f12aa` (skip a unit whose tier-one PASS is on
      disk). The new per-unit plan + plan-faithfulness artifacts add to what a resume must
      account for; the resume statement must stay coherent with the added artifacts.
    - Tier-one acceptance (008) — plan-faithfulness is a new per-unit check that sits beside or
      reuses the tier-one reviewer; the route choice (reuse carve-variant vs purpose-built lens)
      decides which.
    - Seed-unit "faithful, non-pre-deciding carve" (`DECOMPOSITION-FINDINGS.md`, NOT adopted) —
      option 1 reuses its variant on the plan; that finding is unadopted scratch, so reuse means
      materializing the variant here, not depending on an unadopted node.
    - 010 routing/retry/escalate — C4's proactive "strong builds non-decomposable units" is the
      proactive form of the reactive three-fail ladder; they must compose, not contradict.
    - `collaboration` segment frame-legibility statements ("lean frame", "not proved by field
      count") must stay coherent with C2/C3 — two-step adds no frame field, it sets the frame's
      altitude doctrine; flag if any collaboration statement implies the frame is
      implementation-complete.
    - Known debt (carried, not fixed here): the one-way review prompt assumes a signed
      route-settled frame, so it will FLAG this correctly-staged pre-direction frame; its verdict
      is read with that caveat (recorded by 011, see memory).
    
    ## adoption claim
    
    Adopt: fold the plan-step, floor-of-judgeability, plan-faithfulness, and
    non-decomposable-routing statements into the `loop` and `adapter` segments; flip the
    `CODEX_BUILDER_MODEL` default to `gpt-5.3-codex-spark`; materialize the mechanism in
    `adapter/loop.sh` and the gate contracts; assert it all in `./check.sh`; pass the one-way
    tier-two panel; and stamp the operator's endorsement on the `loop` and `adapter` segments.
    
    ## shelving claim
    
    Shelve: if the operator rejects both options or the build cannot prove the contract, record
    013 as shelved history under `intent/history/shelved/` without flipping the builder default
    or adding the plan step; the builder stays held at `gpt-5.5` and the findings remain
    ephemeral scratch for a later attempt.
    
    exec
    /bin/bash -lc "sed -n '1,240p' 013-two-step-build/intent/frame/options.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # options - 013-two-step-build
    
    Direction options are drafted by the machine for operator selection. The operator
    selects one route, rejects all options, or aborts without writing direction.
    
    Both options share the settled spine: a per-unit strong-model plan sub-step between the
    signed frame and the cheap build (C6); the frame held to the floor of judgeability (C3);
    spark executes tasks while the strong model builds non-decomposable units (C4); a required
    plan-faithfulness check (C5); and the builder default flipped to `gpt-5.3-codex-spark` (C8).
    They differ on how much new governance and visibility surface the plan step carries.
    
    ## option 1
    
    id: minimal-two-step
    kind: selected-route
    summary: Minimal-surface two-step. The per-unit plan is sub-signature and never surfaced to
      the operator. The planner self-reports a unit as non-decomposable ("cannot separate into
      mechanical tasks"), which routes that unit straight to the strong builder. Plan
      faithfulness reuses the seed-unit "faithful, non-pre-deciding carve" tier-one variant,
      materialized here and applied to the plan — no new check type. The altitude line ratifies
      the findings' judgeability test as-is.
    reversibility: one-way
    tradeoff: Smallest new surface, fastest to ship, fewest new seams to prove. Cost: the
      operator never inspects the plan, so trust rests entirely on the planner plus the reused
      faithfulness check; and a carve-check built for node->child carving may fit the
      frame->task plan imperfectly.
    
    ## option 2
    
    id: audited-two-step
    kind: selected-route
    summary: Audited two-step. The per-unit plan is surfaced read-only to the operator
      (available, unsigned, not required reading). Non-decomposability is an explicit signal the
      planner emits that a check ratifies before routing to the strong builder, not bare
      self-report. Plan faithfulness is a purpose-built `plan-faithfulness` tier-one lens
      distinct from the carve check, with the floor-of-judgeability test baked into its prompt.
      The altitude line is ratified and sharpened with explicit frame-vs-task examples baked into
      the plan and faithfulness gate prompts.
    reversibility: one-way
    tradeoff: Most legible and auditable, strongest faithfulness seam, sharpest altitude
      guidance. Cost: the largest new surface to build and prove, and surfacing the plan
      read-only risks partially re-drowning the operator the frame split was meant to prevent.
    
    ## rejection choices
    
    none: The operator may reject all options and send the work back to frame.
    abort: The operator may abort without writing direction.
    
    codex
    The frame itself leaves route selection pending, so I’m checking the referenced `loop` and `adapter` intent only to verify whether that uncertainty affects the acceptance contract.
    exec
    /bin/bash -lc "sed -n '1,260p' intent/adapter.md" in /home/qqp/projects/hypercore
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
    the phase-two orchestrator protects self-editing work by running execute from a snapshot
    made at execute start; later edits to the live orchestrator material do not change the
    already-running process.
    phase two has a real supervisor-to-executor handoff: after sign-off, an outer supervisor
    launches a fresh phase-two executor from the addressed node and supervises its recorded
    progress, intervening only when the loop blocks on a real gate failure or operator need.
    `start` creates a new work node for phase one; `execute` enters phase two for signed work,
    and omitting the execute work name is only an inference convenience that succeeds when
    exactly one signed, unarchived work node exists in the addressed node and blocks otherwise.
    the implement and archive gate contracts live in re-read gate files, not in frozen inline
    orchestrator strings; `adapter/loop.sh` supplies only dynamic unit or work context and the
    archive decision line.
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
    `adapter/loop.sh` snapshots and re-execs itself at the start of `execute`, using the
    original root adapter paths for gate files and the snapshot path for the running loop
    version digest.
    the loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
    `.hypercore/loop-runs`, with run-local state, event history, raw harness gate streams, gate
    final outputs, acceptance artifact paths, and current pointers for the addressed work and
    root.
    the loop streams inner executor JSON events into the phase-two run state while
    printing concise progress, without changing the cleared-session contract.
    the loop materializes separate builder and reviewer routing, structured acceptance
    artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
    then strong-builder escalation ladder, on-disk resumable execute that skips a unit already
    carrying a clean tier-one PASS for the signed frame, the concurrent one-way tier-two panel,
    and phase-one review subprocess crash diagnostics.
    `adapter/loop.sh` accepts one node-local work name in the addressed node for new work.
    the root node is the default addressed node.
    `loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node, including a
    linked mounted child when `<node-path>` is its mount path.
    `loop.sh start <work-name>` creates a work node directly under the addressed node.
    `loop.sh execute` without `<work-name>` resolves the single signed, unarchived work node in
    the addressed node and blocks when there are zero or more than one.
    `loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work
    and act only on that addressed work.
    `loop.sh execute <work-name>` records only the addressed node-local work in that node's
    history.
    the orchestrator creates, signs, executes, and records only addressed node-local work
    nodes.
    the gate prompts use addressed-node and node-local work wording and point cleared sessions
    at the addressed work frame.
    the implement and archive gate prompts carry their contract in `adapter/gates/implement.md`
    and `adapter/gates/archive.md`; `run_gate` reads those files for each invocation, so a
    self-change to a gate prompt can affect the next gate invocation in the same execute run.
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
    builder/reviewer routing with bounded retry and strong escalation, on-disk resumable execute
    that skips units already carrying a clean tier-one PASS, the concurrent tier-two panel, the
    re-read implement/archive prompt contract and
    absence of frozen inline implement/archive contract text, the new operator-act and
    phase-two performance contract in the `collaboration`, `loop`, and `adapter` segments, and
    current-material absence of the retired compatibility route still carry the contract.
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
    /bin/bash -lc "sed -n '1,220p' intent/machine-statements/adapter.md" in /home/qqp/projects/hypercore
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
    `adapter/loop.sh` snapshots and re-execs itself at the start of `execute`, using the
    original root adapter paths for gate files and the snapshot path for the running loop
    version digest.
    the loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
    `.hypercore/loop-runs`, with run-local state, event history, raw harness gate streams, gate
    final outputs, acceptance artifact paths, and current pointers for the addressed work and
    root.
    the loop streams inner executor JSON events into the phase-two run state while
    printing concise progress, without changing the cleared-session contract.
    the current handoff path is that an outer supervisor launches a fresh phase-two executor
    from the addressed node and supervises the loop's recorded progress, intervening only when
    the loop blocks on a real gate failure or operator need.
    the loop materializes separate builder and reviewer routing, structured acceptance
    artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
    then strong-builder escalation ladder, on-disk resumable execute that skips a unit already
    carrying a clean tier-one PASS for the signed frame, the concurrent
    one-way tier-two panel, and phase-one review subprocess crash diagnostics.
    the loop keeps the contract-bearing implement and archive prompt text in
    `adapter/gates/implement.md` and `adapter/gates/archive.md`, while inline execute prompts
    carry only dynamic unit or work context and the archive decision line.
    `adapter/loop.sh` accepts one node-local work name in the addressed node for new work.
    the root node is the default addressed node.
    `loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node, including a
    linked mounted child when `<node-path>` is its mount path.
    `loop.sh start <work-name>` creates a work node directly under the addressed node.
    `loop.sh execute` without `<work-name>` resolves the single signed, unarchived work node in
    the addressed node and blocks when there are zero or more than one.
    `start` is the new-work phase-one entry point, while `execute` is the signed-work phase-two
    entry point.
    `loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work
    and act only on that addressed work.
    `loop.sh execute <work-name>` records only the addressed node-local work in that node's
    history.
    the orchestrator creates, signs, executes, and records only addressed node-local work
    nodes.
    the gate prompts use addressed-node and node-local work wording and point cleared sessions
    at the addressed work frame.
    the implement and archive gate prompts carry their contract in `adapter/gates/implement.md`
    and `adapter/gates/archive.md`; `run_gate` reads those files for each invocation, so a
    self-change to a gate prompt can affect the next gate invocation in the same execute run.
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
    builder/reviewer routing with bounded retry and strong escalation, on-disk resumable execute
    that skips units already carrying a clean tier-one PASS, the concurrent tier-two panel, the
    re-read implement/archive prompt contract and
    absence of frozen inline implement/archive contract text, the new operator-act and
    phase-two performance contract in the `collaboration`, `loop`, and `adapter` segments, and
    current-material absence of the retired compatibility route still carry the contract.
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
    `loop.sh execute <work-name>` re-execs from a read-only snapshot of `adapter/loop.sh` at
    execute start before phase-two builders, reviewers, or archive actors can edit the live
    orchestrator material.
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
    `loop.sh execute <work-name>` passes only dynamic unit identifiers, proof obligation, and
    signed-frame location to the implement actor; the implement contract lives in
    `adapter/gates/implement.md`, which `run_gate` reads for each invocation.
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
    `loop.sh execute <work-name>` resumes from on-disk artifacts: it skips a unit whose tier-one
    acceptance artifact is already a clean PASS for the current signed frame, and rebuilds any
    unit without that artifact.
    `loop.sh execute <work-name>` treats malformed, evidence-free, or unsupported-source
    implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
    concurrent one-way tier-two panel before archive.
    `loop.sh execute <work-name>` passes only dynamic work location, acceptance artifact
    location, and the archive decision line to the archive actor; the archive contract lives in
    `adapter/gates/archive.md`, which `run_gate` reads for each invocation.
    `loop.sh execute <work-name>` records the addressed work in node-local history after archive.
    
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
    execute runs phase two from an orchestrator snapshot made at execute start, so a unit that
    edits the live orchestrator material cannot corrupt the already-running phase-two process.
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
    when a unit's own proof is a check over addressed-node intent, implement may edit that
    intent in the unit; those edits remain in-flight proof material until archive adoption.
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
    execute is resumable from the signed frame and on-disk artifacts: a unit is reused on a
    rerun only when its tier-one acceptance artifact is already present as a clean PASS for the
    current signed frame, and any unit without that artifact is rebuilt.
    unresolved required tier-one or tier-two `FLAG`s halt phase two before archive; the active
    work node remains in flight for the operator.
    the checks re-run for every statement, not only the ones a work node touched.
    drift is a check that falls without work meaning to break it, and it surfaces wherever it
    happens.
    archive: adopt or shelve the work according to the signed frame.
    one-way archive cannot fold or stamp until required implementation-acceptance artifacts
    are present and clean.
    adoption verifies the accepted applied delta against the signed frame, stamps each touched
    segment's foot with this operator, and records the work node as adopted history.
    adoption does not re-fold intent statements that phase-two units already applied in place.
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
    `loop.sh execute <work-name>` re-execs from a read-only snapshot of `adapter/loop.sh` at
    execute start before phase-two builders, reviewers, or archive actors can edit the live
    orchestrator material.
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
    `loop.sh execute <work-name>` passes only dynamic unit identifiers, proof obligation, and
    signed-frame location to the implement actor; the implement contract lives in
    `adapter/gates/implement.md`, which `run_gate` reads for each invocation.
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
    `loop.sh execute <work-name>` resumes from on-disk artifacts: it skips a unit whose tier-one
    acceptance artifact is already a clean PASS for the current signed frame, and rebuilds any
    unit without that artifact.
    `loop.sh execute <work-name>` treats malformed, evidence-free, or unsupported-source
    implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
    concurrent one-way tier-two panel before archive.
    `loop.sh execute <work-name>` passes only dynamic work location, acceptance artifact
    location, and the archive decision line to the archive actor; the archive contract lives in
    `adapter/gates/archive.md`, which `run_gate` reads for each invocation.
    `loop.sh execute <work-name>` records the addressed work in node-local history after archive.
    
    ---
    endorsed by qqp-dev
    
    codex
    VERDICT: FLAG
    NOTE: The frame leaves route as `PENDING` and makes acceptance depend on “the selected option’s specifics,” so the signed contract is not determinate enough to check.
    hook: Stop
    hook: Stop Completed
    tokens used
    24,143

### soundness-fit

status: 0
selected-output-source: final-output

#### selected output

    VERDICT: FLAG
    NOTE: The frame still has open direction and `route: PENDING`, so soundness-fit cannot verify a signed, route-settled work contract.

#### final output

    VERDICT: FLAG
    NOTE: The frame still has open direction and `route: PENDING`, so soundness-fit cannot verify a signed, route-settled work contract.

#### stdout

    VERDICT: FLAG
    NOTE: The frame still has open direction and `route: PENDING`, so soundness-fit cannot verify a signed, route-settled work contract.

#### stderr

    OpenAI Codex v0.137.0
    --------
    workdir: /home/qqp/projects/hypercore
    model: gpt-5.5
    provider: openai
    approval: never
    sandbox: read-only
    reasoning effort: xhigh
    reasoning summaries: none
    session id: 019ea5d1-340c-7591-9d4b-de0a7487b9a1
    --------
    user
    Review role: soundness-fit
    Work: 013-two-step-build
    Frame directory: 013-two-step-build/intent/frame
    
    Read only the signed work frame and the intent it references. Do not debate other reviewers.
    Return exactly one structured verdict line:
    VERDICT: PASS
    or
    VERDICT: FLAG
    
    Then optionally add one NOTE: line. Treat uncertainty as FLAG.
    hook: UserPromptSubmit
    hook: UserPromptSubmit Completed
    codex
    I’ll inspect only the signed frame directory and the intent files it names, then return the requested verdict format.
    exec
    /bin/bash -lc 'rg --files 013-two-step-build/intent/frame' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    013-two-step-build/intent/frame/options.md
    013-two-step-build/intent/frame/frame.md
    
    exec
    /bin/bash -lc 'ls -la 013-two-step-build/intent/frame' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    total 24
    drwxrwxr-x 2 qqp qqp 4096 Jun  8 00:59 .
    drwxrwxr-x 3 qqp qqp 4096 Jun  8 00:54 ..
    -rw-rw-r-- 1 qqp qqp 9643 Jun  8 00:58 frame.md
    -rw-rw-r-- 1 qqp qqp 2567 Jun  8 00:59 options.md
    
    codex
    The frame directory contains `frame.md` and `options.md`; I’m reading those first to identify the referenced intent segments.
    exec
    /bin/bash -lc "sed -n '1,240p' 013-two-step-build/intent/frame/frame.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # frame - 013-two-step-build
    
    ## work
    
    Addressed node: root (hypercore)
    
    Node-local work name: 013-two-step-build
    
    Target segments: loop, adapter
    
    Work in flight: none other in flight (tree clean after the cache-removal commit `91f12aa`
    and the Claude-adapter-draft commit `60fb127`). Related but unadopted scratch:
    `DECOMPOSITION-FINDINGS.md` (seed-unit decomposition) and `WORK-NODE-COLLAPSE-FINDINGS.md`
    — ephemeral, not intent, read for coherence only. This frame derives from
    `TWO-STEP-BUILD-FINDINGS.md` (ephemeral seed, 2026-06-07), which is not itself intent.
    
    ## problem
    
    The signed frame today serves three consumers at one altitude and is compromised for all
    three: the operator signs it, the builder implements from it, and the acceptance panel
    judges against it. The result is dense feature-altitude units. Concrete evidence: work
    unit-003 (in 010) bundled builder/reviewer routing, the retry budget, strong escalation,
    operator-stop, and self-tests into one paragraph, and the gpt-5.5 build trace shows the
    builder *diagnosing architecture* and exercising feature-level judgement — not applying
    mechanical edits. Because units demand that judgement, the builder default is held at the
    strong model (`gpt-5.5`), and 010's cheap-builder (`gpt-5.3-codex-spark`) routing is an
    untested, unsafe bet: no work node has ever been built by spark. There is no artifact at an
    altitude a cheap builder can execute safely.
    
    ## constraints
    
    - C1 (settled, not re-opened): lean hard into two-step — frame -> (strong) plan -> (cheap)
      build is the path, not a maybe.
    - C2: the frame optimizes for operator + panel legibility — clear, separate, falsifiable
      statements; count bounded to *ownable claims*, not edits.
    - C3 (the guardrail): floor of judgeability. The frame stops being load-bearing in
      *execution* but stays load-bearing in *acceptance* — the panel must still be able to FLAG
      a wrong result against a frame statement *without reading code*. Legibility must never
      drift into "soft." Altitude test: judgeable-without-the-diff -> frame statement;
      only-means-something-next-to-the-diff -> task.
    - C4: spark executes *tasks*, never features; no node is ever built by spark at feature
      altitude. The strong model builds non-decomposable units directly (the proactive form of
      010's reactive three-fail escalation ladder).
    - C5: planner faithfulness is a new load-bearing seam. A strong model *planning* is not the
      same as the plan being *faithful to the frame*; a faithful-looking-but-wrong plan is a new
      way to ship a defect and must be caught by a check before the build trusts it.
    - C6 (operator info-gain lean, 2026-06-08): plan placement is a per-unit sub-step at the
      head of each build, not a whole-phase pass. Both route options honor this.
    - C7: `./check.sh` stays the proof floor, green at every phase-two unit boundary. 010's
      routing / retry / strong-escalation machinery and 008's tier-one + tier-two acceptance are
      extended, not replaced.
    - C8: on adoption, flip the builder default `gpt-5.5 -> gpt-5.3-codex-spark` (the held knob),
      because spark now executes tasks behind a legible review — the configuration that makes it
      safe. The strong-builder escalation knob stays intact.
    
    ## decision surface or open direction
    
    Open direction — needs operator selection via `./direction` from `options.md`. Per-unit
    placement (C6) is set by the operator's info-gain lean; the options differ on how much new
    governance and visibility surface the plan step carries:
    
    1. Plan visibility — sub-signature only (never surfaced) vs surfaced read-only to the operator.
    2. Non-decomposable declaration — planner self-report vs an explicit signal a check ratifies.
    3. Plan-faithfulness check — reuse the seed-unit "faithful carve" tier-one variant vs a
       purpose-built sibling `plan-faithfulness` lens.
    4. Altitude line — ratify the judgeability test as-is vs ratify-and-sharpen with baked-in
       frame-vs-task examples.
    
    These bundle into the two numbered options. Route is left open until `./direction`.
    
    Reversibility: one-way
    
    ## route
    
    PENDING — open direction. To be copied verbatim from the operator-selected numbered option
    in `options.md` at `./direction`. (Methodology-level loop/adapter contract change plus the
    spark builder flip, which accrues hard-to-revert build state; defaults one-way.)
    
    ## acceptance condition
    
    The loop gains a per-unit strong-model **plan** sub-step between the signed frame and the
    cheap build; the frame's altitude is governed by the floor of judgeability (C3); a
    plan-faithfulness check gates each plan before its build is trusted; non-decomposable units
    route to the strong builder; the builder default flips to `gpt-5.3-codex-spark`; `./check.sh`
    proves the new contract structurally; and for this one-way work the tier-two panel passes
    before archive. The selected option's specifics (visibility, faithfulness check shape,
    non-decomposable declaration, altitude wording) are honored by the build.
    
    ## observable acceptance
    
    - `./check.sh` exits 0 with new structural assertions that: (a) `loop` and `adapter` intent
      carry the plan-step, floor-of-judgeability, and plan-faithfulness statements; (b)
      `adapter/loop.sh` routes a per-unit plan sub-step through a strong-planner model knob
      *ahead of* the spark build, and exposes that knob; (c) the builder default token is
      `gpt-5.3-codex-spark`; (d) a plan-faithfulness verdict artifact is required per unit before
      that unit's build is trusted.
    - A dry-run / self-test of `loop.sh execute` records, per unit and in order, a strong-model
      plan artifact, then a plan-faithfulness verdict, then the (spark) build artifact, then the
      tier-one verdict — visible under the run's frame artifacts.
    
    ## excluded interpretation
    
    This work must NOT mean any of:
    
    - that the frame becomes "soft" or non-falsifiable — legibility is *to the floor of
      judgeability*, never below it; the panel must still FLAG a wrong result without reading code.
    - that any node is built by spark at feature altitude — spark executes tasks only;
      non-decomposable units go to the strong builder.
    - that the plan is signed by the operator or becomes operator-owned intent — the plan is
      sub-signature build material, not a frame and not a statement.
    - that 010's routing/retry/escalate or 008's acceptance tiers are replaced — they are extended.
    - that a strong model *planning* discharges faithfulness — the plan-faithfulness check is
      required, not optional or self-cleared.
    
    ## proof state
    
    Unproven until built: the plan-step contract (strong-planner knob present and ordered before
    the build; builder default = spark; per-unit plan-faithfulness artifact required) asserted by
    `./check.sh` and demonstrated by a dry-run execute trace. Existing 010 (routing/retry/escalate,
    resumable execute) and 008 (tier-one + tier-two acceptance) proofs are preserved and must stay
    green.
    
    ## sweep
    
    Concept map and likely clashes:
    
    - "fast builder / builder default held at strong until two-step lands" appears in
      `intent/loop.md`, `intent/machine-statements/loop.md`, `intent/adapter.md`,
      `intent/machine-statements/adapter.md`, `adapter/loop.sh` (header + `CODEX_BUILDER_MODEL`
      default + the two-step note), `adapter/codex.md`, `adapter/claude.md`, and `check.sh`
      assertions. Every "held until two-step lands" clause must flip to "two-step has landed;
      default is spark." This is the central coherence obligation.
    - Resumable execute was just rewritten by `91f12aa` (skip a unit whose tier-one PASS is on
      disk). The new per-unit plan + plan-faithfulness artifacts add to what a resume must
      account for; the resume statement must stay coherent with the added artifacts.
    - Tier-one acceptance (008) — plan-faithfulness is a new per-unit check that sits beside or
      reuses the tier-one reviewer; the route choice (reuse carve-variant vs purpose-built lens)
      decides which.
    - Seed-unit "faithful, non-pre-deciding carve" (`DECOMPOSITION-FINDINGS.md`, NOT adopted) —
      option 1 reuses its variant on the plan; that finding is unadopted scratch, so reuse means
      materializing the variant here, not depending on an unadopted node.
    - 010 routing/retry/escalate — C4's proactive "strong builds non-decomposable units" is the
      proactive form of the reactive three-fail ladder; they must compose, not contradict.
    - `collaboration` segment frame-legibility statements ("lean frame", "not proved by field
      count") must stay coherent with C2/C3 — two-step adds no frame field, it sets the frame's
      altitude doctrine; flag if any collaboration statement implies the frame is
      implementation-complete.
    - Known debt (carried, not fixed here): the one-way review prompt assumes a signed
      route-settled frame, so it will FLAG this correctly-staged pre-direction frame; its verdict
      is read with that caveat (recorded by 011, see memory).
    
    ## adoption claim
    
    Adopt: fold the plan-step, floor-of-judgeability, plan-faithfulness, and
    non-decomposable-routing statements into the `loop` and `adapter` segments; flip the
    `CODEX_BUILDER_MODEL` default to `gpt-5.3-codex-spark`; materialize the mechanism in
    `adapter/loop.sh` and the gate contracts; assert it all in `./check.sh`; pass the one-way
    tier-two panel; and stamp the operator's endorsement on the `loop` and `adapter` segments.
    
    ## shelving claim
    
    Shelve: if the operator rejects both options or the build cannot prove the contract, record
    013 as shelved history under `intent/history/shelved/` without flipping the builder default
    or adding the plan step; the builder stays held at `gpt-5.5` and the findings remain
    ephemeral scratch for a later attempt.
    
    exec
    /bin/bash -lc "sed -n '1,220p' 013-two-step-build/intent/frame/options.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # options - 013-two-step-build
    
    Direction options are drafted by the machine for operator selection. The operator
    selects one route, rejects all options, or aborts without writing direction.
    
    Both options share the settled spine: a per-unit strong-model plan sub-step between the
    signed frame and the cheap build (C6); the frame held to the floor of judgeability (C3);
    spark executes tasks while the strong model builds non-decomposable units (C4); a required
    plan-faithfulness check (C5); and the builder default flipped to `gpt-5.3-codex-spark` (C8).
    They differ on how much new governance and visibility surface the plan step carries.
    
    ## option 1
    
    id: minimal-two-step
    kind: selected-route
    summary: Minimal-surface two-step. The per-unit plan is sub-signature and never surfaced to
      the operator. The planner self-reports a unit as non-decomposable ("cannot separate into
      mechanical tasks"), which routes that unit straight to the strong builder. Plan
      faithfulness reuses the seed-unit "faithful, non-pre-deciding carve" tier-one variant,
      materialized here and applied to the plan — no new check type. The altitude line ratifies
      the findings' judgeability test as-is.
    reversibility: one-way
    tradeoff: Smallest new surface, fastest to ship, fewest new seams to prove. Cost: the
      operator never inspects the plan, so trust rests entirely on the planner plus the reused
      faithfulness check; and a carve-check built for node->child carving may fit the
      frame->task plan imperfectly.
    
    ## option 2
    
    id: audited-two-step
    kind: selected-route
    summary: Audited two-step. The per-unit plan is surfaced read-only to the operator
      (available, unsigned, not required reading). Non-decomposability is an explicit signal the
      planner emits that a check ratifies before routing to the strong builder, not bare
      self-report. Plan faithfulness is a purpose-built `plan-faithfulness` tier-one lens
      distinct from the carve check, with the floor-of-judgeability test baked into its prompt.
      The altitude line is ratified and sharpened with explicit frame-vs-task examples baked into
      the plan and faithfulness gate prompts.
    reversibility: one-way
    tradeoff: Most legible and auditable, strongest faithfulness seam, sharpest altitude
      guidance. Cost: the largest new surface to build and prove, and surfacing the plan
      read-only risks partially re-drowning the operator the frame split was meant to prevent.
    
    ## rejection choices
    
    none: The operator may reject all options and send the work back to frame.
    abort: The operator may abort without writing direction.
    
    codex
    The frame targets `loop` and `adapter` and explicitly calls out their machine statements; it also names `collaboration` only for coherence against frame-legibility statements. I’m limiting the next read to those intent files.
    exec
    /bin/bash -lc "sed -n '1,220p' intent/machine-statements/adapter.md" in /home/qqp/projects/hypercore
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
    `adapter/loop.sh` snapshots and re-execs itself at the start of `execute`, using the
    original root adapter paths for gate files and the snapshot path for the running loop
    version digest.
    the loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
    `.hypercore/loop-runs`, with run-local state, event history, raw harness gate streams, gate
    final outputs, acceptance artifact paths, and current pointers for the addressed work and
    root.
    the loop streams inner executor JSON events into the phase-two run state while
    printing concise progress, without changing the cleared-session contract.
    the current handoff path is that an outer supervisor launches a fresh phase-two executor
    from the addressed node and supervises the loop's recorded progress, intervening only when
    the loop blocks on a real gate failure or operator need.
    the loop materializes separate builder and reviewer routing, structured acceptance
    artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
    then strong-builder escalation ladder, on-disk resumable execute that skips a unit already
    carrying a clean tier-one PASS for the signed frame, the concurrent
    one-way tier-two panel, and phase-one review subprocess crash diagnostics.
    the loop keeps the contract-bearing implement and archive prompt text in
    `adapter/gates/implement.md` and `adapter/gates/archive.md`, while inline execute prompts
    carry only dynamic unit or work context and the archive decision line.
    `adapter/loop.sh` accepts one node-local work name in the addressed node for new work.
    the root node is the default addressed node.
    `loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node, including a
    linked mounted child when `<node-path>` is its mount path.
    `loop.sh start <work-name>` creates a work node directly under the addressed node.
    `loop.sh execute` without `<work-name>` resolves the single signed, unarchived work node in
    the addressed node and blocks when there are zero or more than one.
    `start` is the new-work phase-one entry point, while `execute` is the signed-work phase-two
    entry point.
    `loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work
    and act only on that addressed work.
    `loop.sh execute <work-name>` records only the addressed node-local work in that node's
    history.
    the orchestrator creates, signs, executes, and records only addressed node-local work
    nodes.
    the gate prompts use addressed-node and node-local work wording and point cleared sessions
    at the addressed work frame.
    the implement and archive gate prompts carry their contract in `adapter/gates/implement.md`
    and `adapter/gates/archive.md`; `run_gate` reads those files for each invocation, so a
    self-change to a gate prompt can affect the next gate invocation in the same execute run.
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
    builder/reviewer routing with bounded retry and strong escalation, on-disk resumable execute
    that skips units already carrying a clean tier-one PASS, the concurrent tier-two panel, the
    re-read implement/archive prompt contract and
    absence of frozen inline implement/archive contract text, the new operator-act and
    phase-two performance contract in the `collaboration`, `loop`, and `adapter` segments, and
    current-material absence of the retired compatibility route still carry the contract.
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
    
    exec
    /bin/bash -lc "sed -n '1,260p' intent/adapter.md" in /home/qqp/projects/hypercore
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
    the phase-two orchestrator protects self-editing work by running execute from a snapshot
    made at execute start; later edits to the live orchestrator material do not change the
    already-running process.
    phase two has a real supervisor-to-executor handoff: after sign-off, an outer supervisor
    launches a fresh phase-two executor from the addressed node and supervises its recorded
    progress, intervening only when the loop blocks on a real gate failure or operator need.
    `start` creates a new work node for phase one; `execute` enters phase two for signed work,
    and omitting the execute work name is only an inference convenience that succeeds when
    exactly one signed, unarchived work node exists in the addressed node and blocks otherwise.
    the implement and archive gate contracts live in re-read gate files, not in frozen inline
    orchestrator strings; `adapter/loop.sh` supplies only dynamic unit or work context and the
    archive decision line.
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
    `adapter/loop.sh` snapshots and re-execs itself at the start of `execute`, using the
    original root adapter paths for gate files and the snapshot path for the running loop
    version digest.
    the loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
    `.hypercore/loop-runs`, with run-local state, event history, raw harness gate streams, gate
    final outputs, acceptance artifact paths, and current pointers for the addressed work and
    root.
    the loop streams inner executor JSON events into the phase-two run state while
    printing concise progress, without changing the cleared-session contract.
    the loop materializes separate builder and reviewer routing, structured acceptance
    artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
    then strong-builder escalation ladder, on-disk resumable execute that skips a unit already
    carrying a clean tier-one PASS for the signed frame, the concurrent one-way tier-two panel,
    and phase-one review subprocess crash diagnostics.
    `adapter/loop.sh` accepts one node-local work name in the addressed node for new work.
    the root node is the default addressed node.
    `loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node, including a
    linked mounted child when `<node-path>` is its mount path.
    `loop.sh start <work-name>` creates a work node directly under the addressed node.
    `loop.sh execute` without `<work-name>` resolves the single signed, unarchived work node in
    the addressed node and blocks when there are zero or more than one.
    `loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work
    and act only on that addressed work.
    `loop.sh execute <work-name>` records only the addressed node-local work in that node's
    history.
    the orchestrator creates, signs, executes, and records only addressed node-local work
    nodes.
    the gate prompts use addressed-node and node-local work wording and point cleared sessions
    at the addressed work frame.
    the implement and archive gate prompts carry their contract in `adapter/gates/implement.md`
    and `adapter/gates/archive.md`; `run_gate` reads those files for each invocation, so a
    self-change to a gate prompt can affect the next gate invocation in the same execute run.
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
    builder/reviewer routing with bounded retry and strong escalation, on-disk resumable execute
    that skips units already carrying a clean tier-one PASS, the concurrent tier-two panel, the
    re-read implement/archive prompt contract and
    absence of frozen inline implement/archive contract text, the new operator-act and
    phase-two performance contract in the `collaboration`, `loop`, and `adapter` segments, and
    current-material absence of the retired compatibility route still carry the contract.
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
    `loop.sh execute <work-name>` re-execs from a read-only snapshot of `adapter/loop.sh` at
    execute start before phase-two builders, reviewers, or archive actors can edit the live
    orchestrator material.
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
    `loop.sh execute <work-name>` passes only dynamic unit identifiers, proof obligation, and
    signed-frame location to the implement actor; the implement contract lives in
    `adapter/gates/implement.md`, which `run_gate` reads for each invocation.
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
    `loop.sh execute <work-name>` resumes from on-disk artifacts: it skips a unit whose tier-one
    acceptance artifact is already a clean PASS for the current signed frame, and rebuilds any
    unit without that artifact.
    `loop.sh execute <work-name>` treats malformed, evidence-free, or unsupported-source
    implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
    concurrent one-way tier-two panel before archive.
    `loop.sh execute <work-name>` passes only dynamic work location, acceptance artifact
    location, and the archive decision line to the archive actor; the archive contract lives in
    `adapter/gates/archive.md`, which `run_gate` reads for each invocation.
    `loop.sh execute <work-name>` records the addressed work in node-local history after archive.
    
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
    execute runs phase two from an orchestrator snapshot made at execute start, so a unit that
    edits the live orchestrator material cannot corrupt the already-running phase-two process.
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
    when a unit's own proof is a check over addressed-node intent, implement may edit that
    intent in the unit; those edits remain in-flight proof material until archive adoption.
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
    execute is resumable from the signed frame and on-disk artifacts: a unit is reused on a
    rerun only when its tier-one acceptance artifact is already present as a clean PASS for the
    current signed frame, and any unit without that artifact is rebuilt.
    unresolved required tier-one or tier-two `FLAG`s halt phase two before archive; the active
    work node remains in flight for the operator.
    the checks re-run for every statement, not only the ones a work node touched.
    drift is a check that falls without work meaning to break it, and it surfaces wherever it
    happens.
    archive: adopt or shelve the work according to the signed frame.
    one-way archive cannot fold or stamp until required implementation-acceptance artifacts
    are present and clean.
    adoption verifies the accepted applied delta against the signed frame, stamps each touched
    segment's foot with this operator, and records the work node as adopted history.
    adoption does not re-fold intent statements that phase-two units already applied in place.
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
    `loop.sh execute <work-name>` re-execs from a read-only snapshot of `adapter/loop.sh` at
    execute start before phase-two builders, reviewers, or archive actors can edit the live
    orchestrator material.
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
    `loop.sh execute <work-name>` passes only dynamic unit identifiers, proof obligation, and
    signed-frame location to the implement actor; the implement contract lives in
    `adapter/gates/implement.md`, which `run_gate` reads for each invocation.
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
    `loop.sh execute <work-name>` resumes from on-disk artifacts: it skips a unit whose tier-one
    acceptance artifact is already a clean PASS for the current signed frame, and rebuilds any
    unit without that artifact.
    `loop.sh execute <work-name>` treats malformed, evidence-free, or unsupported-source
    implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
    concurrent one-way tier-two panel before archive.
    `loop.sh execute <work-name>` passes only dynamic work location, acceptance artifact
    location, and the archive decision line to the archive actor; the archive contract lives in
    `adapter/gates/archive.md`, which `run_gate` reads for each invocation.
    `loop.sh execute <work-name>` records the addressed work in node-local history after archive.
    
    ---
    endorsed by qqp-dev
    
    codex
    One more referenced intent segment is `collaboration`; I’m checking only that segment’s statements for the frame-altitude fit the sweep names.
    exec
    /bin/bash -lc "sed -n '1,240p' intent/collaboration.md" in /home/qqp/projects/hypercore
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
    /bin/bash -lc "sed -n '1,220p' intent/machine-statements/collaboration.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # collaboration — machine statements
    
    phase-two handoff state is written as common ground for the operator and later tooling:
    the addressed work's current or recent gate, current unit, status, harness session id, latest
    message, failure reason, event history, run artifact paths, and phase-two acceptance
    artifact paths are recoverable from loop state files.
    
    codex
    VERDICT: FLAG
    NOTE: The frame still has open direction and `route: PENDING`, so soundness-fit cannot verify a signed, route-settled work contract.
    hook: Stop
    hook: Stop Completed
    tokens used
    23,559

### simplicity-fastness

status: 0
selected-output-source: final-output

#### selected output

    VERDICT: FLAG
    NOTE: The frame is pre-direction with `route` still `PENDING`, so simplicity/fastness cannot validate a concrete route; uncertainty flags.

#### final output

    VERDICT: FLAG
    NOTE: The frame is pre-direction with `route` still `PENDING`, so simplicity/fastness cannot validate a concrete route; uncertainty flags.

#### stdout

    VERDICT: FLAG
    NOTE: The frame is pre-direction with `route` still `PENDING`, so simplicity/fastness cannot validate a concrete route; uncertainty flags.

#### stderr

    OpenAI Codex v0.137.0
    --------
    workdir: /home/qqp/projects/hypercore
    model: gpt-5.5
    provider: openai
    approval: never
    sandbox: read-only
    reasoning effort: xhigh
    reasoning summaries: none
    session id: 019ea5d2-c31e-7c82-81f5-5f00610a06c6
    --------
    user
    Review role: simplicity-fastness
    Work: 013-two-step-build
    Frame directory: 013-two-step-build/intent/frame
    
    Read only the signed work frame and the intent it references. Do not debate other reviewers.
    Return exactly one structured verdict line:
    VERDICT: PASS
    or
    VERDICT: FLAG
    
    Then optionally add one NOTE: line. Treat uncertainty as FLAG.
    hook: UserPromptSubmit
    hook: UserPromptSubmit Completed
    exec
    /bin/bash -lc 'rg --files 013-two-step-build/intent/frame' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    013-two-step-build/intent/frame/options.md
    013-two-step-build/intent/frame/frame.md
    
    exec
    /bin/bash -lc "sed -n '1,240p' 013-two-step-build/intent/frame/frame.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # frame - 013-two-step-build
    
    ## work
    
    Addressed node: root (hypercore)
    
    Node-local work name: 013-two-step-build
    
    Target segments: loop, adapter
    
    Work in flight: none other in flight (tree clean after the cache-removal commit `91f12aa`
    and the Claude-adapter-draft commit `60fb127`). Related but unadopted scratch:
    `DECOMPOSITION-FINDINGS.md` (seed-unit decomposition) and `WORK-NODE-COLLAPSE-FINDINGS.md`
    — ephemeral, not intent, read for coherence only. This frame derives from
    `TWO-STEP-BUILD-FINDINGS.md` (ephemeral seed, 2026-06-07), which is not itself intent.
    
    ## problem
    
    The signed frame today serves three consumers at one altitude and is compromised for all
    three: the operator signs it, the builder implements from it, and the acceptance panel
    judges against it. The result is dense feature-altitude units. Concrete evidence: work
    unit-003 (in 010) bundled builder/reviewer routing, the retry budget, strong escalation,
    operator-stop, and self-tests into one paragraph, and the gpt-5.5 build trace shows the
    builder *diagnosing architecture* and exercising feature-level judgement — not applying
    mechanical edits. Because units demand that judgement, the builder default is held at the
    strong model (`gpt-5.5`), and 010's cheap-builder (`gpt-5.3-codex-spark`) routing is an
    untested, unsafe bet: no work node has ever been built by spark. There is no artifact at an
    altitude a cheap builder can execute safely.
    
    ## constraints
    
    - C1 (settled, not re-opened): lean hard into two-step — frame -> (strong) plan -> (cheap)
      build is the path, not a maybe.
    - C2: the frame optimizes for operator + panel legibility — clear, separate, falsifiable
      statements; count bounded to *ownable claims*, not edits.
    - C3 (the guardrail): floor of judgeability. The frame stops being load-bearing in
      *execution* but stays load-bearing in *acceptance* — the panel must still be able to FLAG
      a wrong result against a frame statement *without reading code*. Legibility must never
      drift into "soft." Altitude test: judgeable-without-the-diff -> frame statement;
      only-means-something-next-to-the-diff -> task.
    - C4: spark executes *tasks*, never features; no node is ever built by spark at feature
      altitude. The strong model builds non-decomposable units directly (the proactive form of
      010's reactive three-fail escalation ladder).
    - C5: planner faithfulness is a new load-bearing seam. A strong model *planning* is not the
      same as the plan being *faithful to the frame*; a faithful-looking-but-wrong plan is a new
      way to ship a defect and must be caught by a check before the build trusts it.
    - C6 (operator info-gain lean, 2026-06-08): plan placement is a per-unit sub-step at the
      head of each build, not a whole-phase pass. Both route options honor this.
    - C7: `./check.sh` stays the proof floor, green at every phase-two unit boundary. 010's
      routing / retry / strong-escalation machinery and 008's tier-one + tier-two acceptance are
      extended, not replaced.
    - C8: on adoption, flip the builder default `gpt-5.5 -> gpt-5.3-codex-spark` (the held knob),
      because spark now executes tasks behind a legible review — the configuration that makes it
      safe. The strong-builder escalation knob stays intact.
    
    ## decision surface or open direction
    
    Open direction — needs operator selection via `./direction` from `options.md`. Per-unit
    placement (C6) is set by the operator's info-gain lean; the options differ on how much new
    governance and visibility surface the plan step carries:
    
    1. Plan visibility — sub-signature only (never surfaced) vs surfaced read-only to the operator.
    2. Non-decomposable declaration — planner self-report vs an explicit signal a check ratifies.
    3. Plan-faithfulness check — reuse the seed-unit "faithful carve" tier-one variant vs a
       purpose-built sibling `plan-faithfulness` lens.
    4. Altitude line — ratify the judgeability test as-is vs ratify-and-sharpen with baked-in
       frame-vs-task examples.
    
    These bundle into the two numbered options. Route is left open until `./direction`.
    
    Reversibility: one-way
    
    ## route
    
    PENDING — open direction. To be copied verbatim from the operator-selected numbered option
    in `options.md` at `./direction`. (Methodology-level loop/adapter contract change plus the
    spark builder flip, which accrues hard-to-revert build state; defaults one-way.)
    
    ## acceptance condition
    
    The loop gains a per-unit strong-model **plan** sub-step between the signed frame and the
    cheap build; the frame's altitude is governed by the floor of judgeability (C3); a
    plan-faithfulness check gates each plan before its build is trusted; non-decomposable units
    route to the strong builder; the builder default flips to `gpt-5.3-codex-spark`; `./check.sh`
    proves the new contract structurally; and for this one-way work the tier-two panel passes
    before archive. The selected option's specifics (visibility, faithfulness check shape,
    non-decomposable declaration, altitude wording) are honored by the build.
    
    ## observable acceptance
    
    - `./check.sh` exits 0 with new structural assertions that: (a) `loop` and `adapter` intent
      carry the plan-step, floor-of-judgeability, and plan-faithfulness statements; (b)
      `adapter/loop.sh` routes a per-unit plan sub-step through a strong-planner model knob
      *ahead of* the spark build, and exposes that knob; (c) the builder default token is
      `gpt-5.3-codex-spark`; (d) a plan-faithfulness verdict artifact is required per unit before
      that unit's build is trusted.
    - A dry-run / self-test of `loop.sh execute` records, per unit and in order, a strong-model
      plan artifact, then a plan-faithfulness verdict, then the (spark) build artifact, then the
      tier-one verdict — visible under the run's frame artifacts.
    
    ## excluded interpretation
    
    This work must NOT mean any of:
    
    - that the frame becomes "soft" or non-falsifiable — legibility is *to the floor of
      judgeability*, never below it; the panel must still FLAG a wrong result without reading code.
    - that any node is built by spark at feature altitude — spark executes tasks only;
      non-decomposable units go to the strong builder.
    - that the plan is signed by the operator or becomes operator-owned intent — the plan is
      sub-signature build material, not a frame and not a statement.
    - that 010's routing/retry/escalate or 008's acceptance tiers are replaced — they are extended.
    - that a strong model *planning* discharges faithfulness — the plan-faithfulness check is
      required, not optional or self-cleared.
    
    ## proof state
    
    Unproven until built: the plan-step contract (strong-planner knob present and ordered before
    the build; builder default = spark; per-unit plan-faithfulness artifact required) asserted by
    `./check.sh` and demonstrated by a dry-run execute trace. Existing 010 (routing/retry/escalate,
    resumable execute) and 008 (tier-one + tier-two acceptance) proofs are preserved and must stay
    green.
    
    ## sweep
    
    Concept map and likely clashes:
    
    - "fast builder / builder default held at strong until two-step lands" appears in
      `intent/loop.md`, `intent/machine-statements/loop.md`, `intent/adapter.md`,
      `intent/machine-statements/adapter.md`, `adapter/loop.sh` (header + `CODEX_BUILDER_MODEL`
      default + the two-step note), `adapter/codex.md`, `adapter/claude.md`, and `check.sh`
      assertions. Every "held until two-step lands" clause must flip to "two-step has landed;
      default is spark." This is the central coherence obligation.
    - Resumable execute was just rewritten by `91f12aa` (skip a unit whose tier-one PASS is on
      disk). The new per-unit plan + plan-faithfulness artifacts add to what a resume must
      account for; the resume statement must stay coherent with the added artifacts.
    - Tier-one acceptance (008) — plan-faithfulness is a new per-unit check that sits beside or
      reuses the tier-one reviewer; the route choice (reuse carve-variant vs purpose-built lens)
      decides which.
    - Seed-unit "faithful, non-pre-deciding carve" (`DECOMPOSITION-FINDINGS.md`, NOT adopted) —
      option 1 reuses its variant on the plan; that finding is unadopted scratch, so reuse means
      materializing the variant here, not depending on an unadopted node.
    - 010 routing/retry/escalate — C4's proactive "strong builds non-decomposable units" is the
      proactive form of the reactive three-fail ladder; they must compose, not contradict.
    - `collaboration` segment frame-legibility statements ("lean frame", "not proved by field
      count") must stay coherent with C2/C3 — two-step adds no frame field, it sets the frame's
      altitude doctrine; flag if any collaboration statement implies the frame is
      implementation-complete.
    - Known debt (carried, not fixed here): the one-way review prompt assumes a signed
      route-settled frame, so it will FLAG this correctly-staged pre-direction frame; its verdict
      is read with that caveat (recorded by 011, see memory).
    
    ## adoption claim
    
    Adopt: fold the plan-step, floor-of-judgeability, plan-faithfulness, and
    non-decomposable-routing statements into the `loop` and `adapter` segments; flip the
    `CODEX_BUILDER_MODEL` default to `gpt-5.3-codex-spark`; materialize the mechanism in
    `adapter/loop.sh` and the gate contracts; assert it all in `./check.sh`; pass the one-way
    tier-two panel; and stamp the operator's endorsement on the `loop` and `adapter` segments.
    
    ## shelving claim
    
    Shelve: if the operator rejects both options or the build cannot prove the contract, record
    013 as shelved history under `intent/history/shelved/` without flipping the builder default
    or adding the plan step; the builder stays held at `gpt-5.5` and the findings remain
    ephemeral scratch for a later attempt.
    
    exec
    /bin/bash -lc "sed -n '1,240p' 013-two-step-build/intent/frame/options.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # options - 013-two-step-build
    
    Direction options are drafted by the machine for operator selection. The operator
    selects one route, rejects all options, or aborts without writing direction.
    
    Both options share the settled spine: a per-unit strong-model plan sub-step between the
    signed frame and the cheap build (C6); the frame held to the floor of judgeability (C3);
    spark executes tasks while the strong model builds non-decomposable units (C4); a required
    plan-faithfulness check (C5); and the builder default flipped to `gpt-5.3-codex-spark` (C8).
    They differ on how much new governance and visibility surface the plan step carries.
    
    ## option 1
    
    id: minimal-two-step
    kind: selected-route
    summary: Minimal-surface two-step. The per-unit plan is sub-signature and never surfaced to
      the operator. The planner self-reports a unit as non-decomposable ("cannot separate into
      mechanical tasks"), which routes that unit straight to the strong builder. Plan
      faithfulness reuses the seed-unit "faithful, non-pre-deciding carve" tier-one variant,
      materialized here and applied to the plan — no new check type. The altitude line ratifies
      the findings' judgeability test as-is.
    reversibility: one-way
    tradeoff: Smallest new surface, fastest to ship, fewest new seams to prove. Cost: the
      operator never inspects the plan, so trust rests entirely on the planner plus the reused
      faithfulness check; and a carve-check built for node->child carving may fit the
      frame->task plan imperfectly.
    
    ## option 2
    
    id: audited-two-step
    kind: selected-route
    summary: Audited two-step. The per-unit plan is surfaced read-only to the operator
      (available, unsigned, not required reading). Non-decomposability is an explicit signal the
      planner emits that a check ratifies before routing to the strong builder, not bare
      self-report. Plan faithfulness is a purpose-built `plan-faithfulness` tier-one lens
      distinct from the carve check, with the floor-of-judgeability test baked into its prompt.
      The altitude line is ratified and sharpened with explicit frame-vs-task examples baked into
      the plan and faithfulness gate prompts.
    reversibility: one-way
    tradeoff: Most legible and auditable, strongest faithfulness seam, sharpest altitude
      guidance. Cost: the largest new surface to build and prove, and surfacing the plan
      read-only risks partially re-drowning the operator the frame split was meant to prevent.
    
    ## rejection choices
    
    none: The operator may reject all options and send the work back to frame.
    abort: The operator may abort without writing direction.
    
    exec
    /bin/bash -lc "sed -n '1,260p' intent/machine-statements/loop.md" in /home/qqp/projects/hypercore
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
    `loop.sh execute <work-name>` re-execs from a read-only snapshot of `adapter/loop.sh` at
    execute start before phase-two builders, reviewers, or archive actors can edit the live
    orchestrator material.
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
    `loop.sh execute <work-name>` passes only dynamic unit identifiers, proof obligation, and
    signed-frame location to the implement actor; the implement contract lives in
    `adapter/gates/implement.md`, which `run_gate` reads for each invocation.
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
    `loop.sh execute <work-name>` resumes from on-disk artifacts: it skips a unit whose tier-one
    acceptance artifact is already a clean PASS for the current signed frame, and rebuilds any
    unit without that artifact.
    `loop.sh execute <work-name>` treats malformed, evidence-free, or unsupported-source
    implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
    concurrent one-way tier-two panel before archive.
    `loop.sh execute <work-name>` passes only dynamic work location, acceptance artifact
    location, and the archive decision line to the archive actor; the archive contract lives in
    `adapter/gates/archive.md`, which `run_gate` reads for each invocation.
    `loop.sh execute <work-name>` records the addressed work in node-local history after archive.
    
    exec
    /bin/bash -lc "sed -n '1,260p' intent/machine-statements/collaboration.md" in /home/qqp/projects/hypercore
    exec
    /bin/bash -lc "sed -n '1,260p' intent/machine-statements/adapter.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # collaboration — machine statements
    
    phase-two handoff state is written as common ground for the operator and later tooling:
    the addressed work's current or recent gate, current unit, status, harness session id, latest
    message, failure reason, event history, run artifact paths, and phase-two acceptance
    artifact paths are recoverable from loop state files.
    
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
    `adapter/loop.sh` snapshots and re-execs itself at the start of `execute`, using the
    original root adapter paths for gate files and the snapshot path for the running loop
    version digest.
    the loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
    `.hypercore/loop-runs`, with run-local state, event history, raw harness gate streams, gate
    final outputs, acceptance artifact paths, and current pointers for the addressed work and
    root.
    the loop streams inner executor JSON events into the phase-two run state while
    printing concise progress, without changing the cleared-session contract.
    the current handoff path is that an outer supervisor launches a fresh phase-two executor
    from the addressed node and supervises the loop's recorded progress, intervening only when
    the loop blocks on a real gate failure or operator need.
    the loop materializes separate builder and reviewer routing, structured acceptance
    artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
    then strong-builder escalation ladder, on-disk resumable execute that skips a unit already
    carrying a clean tier-one PASS for the signed frame, the concurrent
    one-way tier-two panel, and phase-one review subprocess crash diagnostics.
    the loop keeps the contract-bearing implement and archive prompt text in
    `adapter/gates/implement.md` and `adapter/gates/archive.md`, while inline execute prompts
    carry only dynamic unit or work context and the archive decision line.
    `adapter/loop.sh` accepts one node-local work name in the addressed node for new work.
    the root node is the default addressed node.
    `loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node, including a
    linked mounted child when `<node-path>` is its mount path.
    `loop.sh start <work-name>` creates a work node directly under the addressed node.
    `loop.sh execute` without `<work-name>` resolves the single signed, unarchived work node in
    the addressed node and blocks when there are zero or more than one.
    `start` is the new-work phase-one entry point, while `execute` is the signed-work phase-two
    entry point.
    `loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work
    and act only on that addressed work.
    `loop.sh execute <work-name>` records only the addressed node-local work in that node's
    history.
    the orchestrator creates, signs, executes, and records only addressed node-local work
    nodes.
    the gate prompts use addressed-node and node-local work wording and point cleared sessions
    at the addressed work frame.
    the implement and archive gate prompts carry their contract in `adapter/gates/implement.md`
    and `adapter/gates/archive.md`; `run_gate` reads those files for each invocation, so a
    self-change to a gate prompt can affect the next gate invocation in the same execute run.
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
    builder/reviewer routing with bounded retry and strong escalation, on-disk resumable execute
    that skips units already carrying a clean tier-one PASS, the concurrent tier-two panel, the
    re-read implement/archive prompt contract and
    absence of frozen inline implement/archive contract text, the new operator-act and
    phase-two performance contract in the `collaboration`, `loop`, and `adapter` segments, and
    current-material absence of the retired compatibility route still carry the contract.
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
    execute runs phase two from an orchestrator snapshot made at execute start, so a unit that
    edits the live orchestrator material cannot corrupt the already-running phase-two process.
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
    when a unit's own proof is a check over addressed-node intent, implement may edit that
    intent in the unit; those edits remain in-flight proof material until archive adoption.
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
    execute is resumable from the signed frame and on-disk artifacts: a unit is reused on a
    rerun only when its tier-one acceptance artifact is already present as a clean PASS for the
    current signed frame, and any unit without that artifact is rebuilt.
    unresolved required tier-one or tier-two `FLAG`s halt phase two before archive; the active
    work node remains in flight for the operator.
    the checks re-run for every statement, not only the ones a work node touched.
    drift is a check that falls without work meaning to break it, and it surfaces wherever it
    happens.
    archive: adopt or shelve the work according to the signed frame.
    one-way archive cannot fold or stamp until required implementation-acceptance artifacts
    are present and clean.
    adoption verifies the accepted applied delta against the signed frame, stamps each touched
    segment's foot with this operator, and records the work node as adopted history.
    adoption does not re-fold intent statements that phase-two units already applied in place.
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
    `loop.sh execute <work-name>` re-execs from a read-only snapshot of `adapter/loop.sh` at
    execute start before phase-two builders, reviewers, or archive actors can edit the live
    orchestrator material.
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
    `loop.sh execute <work-name>` passes only dynamic unit identifiers, proof obligation, and
    signed-frame location to the implement actor; the implement contract lives in
    `adapter/gates/implement.md`, which `run_gate` reads for each invocation.
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
    `loop.sh execute <work-name>` resumes from on-disk artifacts: it skips a unit whose tier-one
    acceptance artifact is already a clean PASS for the current signed frame, and rebuilds any
    unit without that artifact.
    `loop.sh execute <work-name>` treats malformed, evidence-free, or unsupported-source
    implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
    concurrent one-way tier-two panel before archive.
    `loop.sh execute <work-name>` passes only dynamic work location, acceptance artifact
    location, and the archive decision line to the archive actor; the archive contract lives in
    `adapter/gates/archive.md`, which `run_gate` reads for each invocation.
    `loop.sh execute <work-name>` records the addressed work in node-local history after archive.
    
    ---
    endorsed by qqp-dev
    
    exec
    /bin/bash -lc "sed -n '1,260p' intent/collaboration.md" in /home/qqp/projects/hypercore
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
    /bin/bash -lc "sed -n '1,260p' intent/adapter.md" in /home/qqp/projects/hypercore
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
    the phase-two orchestrator protects self-editing work by running execute from a snapshot
    made at execute start; later edits to the live orchestrator material do not change the
    already-running process.
    phase two has a real supervisor-to-executor handoff: after sign-off, an outer supervisor
    launches a fresh phase-two executor from the addressed node and supervises its recorded
    progress, intervening only when the loop blocks on a real gate failure or operator need.
    `start` creates a new work node for phase one; `execute` enters phase two for signed work,
    and omitting the execute work name is only an inference convenience that succeeds when
    exactly one signed, unarchived work node exists in the addressed node and blocks otherwise.
    the implement and archive gate contracts live in re-read gate files, not in frozen inline
    orchestrator strings; `adapter/loop.sh` supplies only dynamic unit or work context and the
    archive decision line.
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
    `adapter/loop.sh` snapshots and re-execs itself at the start of `execute`, using the
    original root adapter paths for gate files and the snapshot path for the running loop
    version digest.
    the loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
    `.hypercore/loop-runs`, with run-local state, event history, raw harness gate streams, gate
    final outputs, acceptance artifact paths, and current pointers for the addressed work and
    root.
    the loop streams inner executor JSON events into the phase-two run state while
    printing concise progress, without changing the cleared-session contract.
    the loop materializes separate builder and reviewer routing, structured acceptance
    artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
    then strong-builder escalation ladder, on-disk resumable execute that skips a unit already
    carrying a clean tier-one PASS for the signed frame, the concurrent one-way tier-two panel,
    and phase-one review subprocess crash diagnostics.
    `adapter/loop.sh` accepts one node-local work name in the addressed node for new work.
    the root node is the default addressed node.
    `loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node, including a
    linked mounted child when `<node-path>` is its mount path.
    `loop.sh start <work-name>` creates a work node directly under the addressed node.
    `loop.sh execute` without `<work-name>` resolves the single signed, unarchived work node in
    the addressed node and blocks when there are zero or more than one.
    `loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work
    and act only on that addressed work.
    `loop.sh execute <work-name>` records only the addressed node-local work in that node's
    history.
    the orchestrator creates, signs, executes, and records only addressed node-local work
    nodes.
    the gate prompts use addressed-node and node-local work wording and point cleared sessions
    at the addressed work frame.
    the implement and archive gate prompts carry their contract in `adapter/gates/implement.md`
    and `adapter/gates/archive.md`; `run_gate` reads those files for each invocation, so a
    self-change to a gate prompt can affect the next gate invocation in the same execute run.
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
    builder/reviewer routing with bounded retry and strong escalation, on-disk resumable execute
    that skips units already carrying a clean tier-one PASS, the concurrent tier-two panel, the
    re-read implement/archive prompt contract and
    absence of frozen inline implement/archive contract text, the new operator-act and
    phase-two performance contract in the `collaboration`, `loop`, and `adapter` segments, and
    current-material absence of the retired compatibility route still carry the contract.
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
    
    codex
    VERDICT: FLAG
    NOTE: The frame is pre-direction with `route` still `PENDING`, so simplicity/fastness cannot validate a concrete route; uncertainty flags.
    hook: Stop
    hook: Stop Completed
    tokens used
    21,240

### red-team

status: 0
selected-output-source: final-output

#### selected output

    VERDICT: FLAG
    NOTE: The frame is not signed or route-settled: `route` is PENDING/open direction and the frame directory lacks `direction.md` and `signoff.md`.

#### final output

    VERDICT: FLAG
    NOTE: The frame is not signed or route-settled: `route` is PENDING/open direction and the frame directory lacks `direction.md` and `signoff.md`.

#### stdout

    VERDICT: FLAG
    NOTE: The frame is not signed or route-settled: `route` is PENDING/open direction and the frame directory lacks `direction.md` and `signoff.md`.

#### stderr

    OpenAI Codex v0.137.0
    --------
    workdir: /home/qqp/projects/hypercore
    model: gpt-5.5
    provider: openai
    approval: never
    sandbox: read-only
    reasoning effort: xhigh
    reasoning summaries: none
    session id: 019ea5d3-9359-7aa0-bdc6-1d971074accf
    --------
    user
    Review role: red-team
    Work: 013-two-step-build
    Frame directory: 013-two-step-build/intent/frame
    
    Read only the signed work frame and the intent it references. Do not debate other reviewers.
    Return exactly one structured verdict line:
    VERDICT: PASS
    or
    VERDICT: FLAG
    
    Then optionally add one NOTE: line. Treat uncertainty as FLAG.
    hook: UserPromptSubmit
    hook: UserPromptSubmit Completed
    codex
    I’ll inspect only the signed frame artifacts and the referenced intent segments, then return the requested verdict format.
    exec
    /bin/bash -lc 'rg --files 013-two-step-build/intent/frame intent | sort' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    013-two-step-build/intent/frame/frame.md
    013-two-step-build/intent/frame/options.md
    intent/active-work.md
    intent/adapter.md
    intent/collaboration.md
    intent/endorsement.md
    intent/foundations.md
    intent/history/adopted/001-flatten-material-tree/intent/frame/frame.md
    intent/history/adopted/001-flatten-material-tree/intent/frame/signoff.md
    intent/history/adopted/001-flatten-material-tree/intent/organizing-document.md
    intent/history/adopted/001-home-greenfield-setup/intent/frame/frame.md
    intent/history/adopted/001-home-greenfield-setup/intent/frame/signoff.md
    intent/history/adopted/001-home-greenfield-setup/intent/organizing-document.md
    intent/history/adopted/001-remove-claude-adapter/intent/frame/frame.md
    intent/history/adopted/001-remove-claude-adapter/intent/frame/signoff.md
    intent/history/adopted/001-remove-claude-adapter/intent/organizing-document.md
    intent/history/adopted/002-direct-path-greenfield-adapter/intent/frame/frame.md
    intent/history/adopted/002-direct-path-greenfield-adapter/intent/frame/signoff.md
    intent/history/adopted/002-direct-path-greenfield-adapter/intent/frame/sweep-flag.md
    intent/history/adopted/002-direct-path-greenfield-adapter/intent/frame/sweep-resolution.md
    intent/history/adopted/002-direct-path-greenfield-adapter/intent/organizing-document.md
    intent/history/adopted/002-simplify-methodology-doc/intent/frame/frame.md
    intent/history/adopted/002-simplify-methodology-doc/intent/frame/signoff.md
    intent/history/adopted/002-simplify-methodology-doc/intent/organizing-document.md
    intent/history/adopted/003-phase-two-observability/intent/frame/frame.md
    intent/history/adopted/003-phase-two-observability/intent/frame/signoff.md
    intent/history/adopted/003-phase-two-observability/intent/organizing-document.md
    intent/history/adopted/004-root-managed-greenfield-entrypoints/intent/frame/frame.md
    intent/history/adopted/004-root-managed-greenfield-entrypoints/intent/frame/signoff.md
    intent/history/adopted/004-root-managed-greenfield-entrypoints/intent/organizing-document.md
    intent/history/adopted/005-harden-loop-collaboration/intent/frame/frame.md
    intent/history/adopted/005-harden-loop-collaboration/intent/frame/signoff.md
    intent/history/adopted/005-harden-loop-collaboration/intent/organizing-document.md
    intent/history/adopted/006-collaboration-deliberation/intent/frame/frame.md
    intent/history/adopted/006-collaboration-deliberation/intent/frame/signoff.md
    intent/history/adopted/006-collaboration-deliberation/intent/organizing-document.md
    intent/history/adopted/007-phase-one-collaboration/intent/frame/frame.md
    intent/history/adopted/007-phase-one-collaboration/intent/frame/review.md
    intent/history/adopted/007-phase-one-collaboration/intent/frame/signoff.md
    intent/history/adopted/007-phase-one-collaboration/intent/organizing-document.md
    intent/history/adopted/008-phase-two-acceptance/intent/frame/direction.md
    intent/history/adopted/008-phase-two-acceptance/intent/frame/frame.md
    intent/history/adopted/008-phase-two-acceptance/intent/frame/manual-archive.md
    intent/history/adopted/008-phase-two-acceptance/intent/frame/phase-two/diffs/unit-001.diff
    intent/history/adopted/008-phase-two-acceptance/intent/frame/phase-two/handoffs/unit-001.md
    intent/history/adopted/008-phase-two-acceptance/intent/frame/phase-two/tier-one/unit-001.md
    intent/history/adopted/008-phase-two-acceptance/intent/frame/phase-two/units/unit-001.md
    intent/history/adopted/008-phase-two-acceptance/intent/frame/review.md
    intent/history/adopted/008-phase-two-acceptance/intent/frame/signoff.md
    intent/history/adopted/008-phase-two-acceptance/intent/frame/sweep-flag.md
    intent/history/adopted/008-phase-two-acceptance/intent/frame/sweep-resolution.md
    intent/history/adopted/008-phase-two-acceptance/intent/organizing-document.md
    intent/history/adopted/009-operator-acts/intent/frame/direction.md
    intent/history/adopted/009-operator-acts/intent/frame/frame.md
    intent/history/adopted/009-operator-acts/intent/frame/manual-archive.md
    intent/history/adopted/009-operator-acts/intent/frame/options.md
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/diffs/unit-001.diff
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/diffs/unit-002.diff
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/diffs/unit-003.diff
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/diffs/unit-004.diff
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/handoffs/unit-001.md
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/handoffs/unit-002.md
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/handoffs/unit-003.md
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/handoffs/unit-004.md
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/tier-one/unit-001.md
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/tier-one/unit-002.md
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/tier-one/unit-003.md
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/tier-one/unit-004.md
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/tier-two-panel/independent-coherence.md
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/tier-two-panel/proof-integrity.md
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/tier-two-panel/red-team.md
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/tier-two-panel/security-permissions.md
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/tier-two-panel/whole-acceptance-conformance.md
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/units/unit-001.md
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/units/unit-002.md
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/units/unit-003.md
    intent/history/adopted/009-operator-acts/intent/frame/phase-two/units/unit-004.md
    intent/history/adopted/009-operator-acts/intent/frame/review.md
    intent/history/adopted/009-operator-acts/intent/frame/session-handoff.md
    intent/history/adopted/009-operator-acts/intent/frame/signoff.md
    intent/history/adopted/009-operator-acts/intent/organizing-document.md
    intent/history/adopted/010-phase-two-performance/intent/frame/direction.md
    intent/history/adopted/010-phase-two-performance/intent/frame/frame.md
    intent/history/adopted/010-phase-two-performance/intent/frame/manual-archive.md
    intent/history/adopted/010-phase-two-performance/intent/frame/options.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/diffs/unit-001.diff
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/diffs/unit-002.diff
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/diffs/unit-003.diff
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/diffs/unit-004.diff
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/diffs/unit-005.diff
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/handoffs/unit-001.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/handoffs/unit-002.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/handoffs/unit-003.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/handoffs/unit-004.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/handoffs/unit-005.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/tier-one/unit-001.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/tier-one/unit-002.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/tier-one/unit-003.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/tier-one/unit-004.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/tier-one/unit-005.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/tier-two-panel/independent-coherence.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/tier-two-panel/proof-integrity.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/tier-two-panel/red-team.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/tier-two-panel/security-permissions.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/tier-two-panel/whole-acceptance-conformance.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/units/unit-001.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/units/unit-002.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/units/unit-003.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/units/unit-004.md
    intent/history/adopted/010-phase-two-performance/intent/frame/phase-two/units/unit-005.md
    intent/history/adopted/010-phase-two-performance/intent/frame/review.md
    intent/history/adopted/010-phase-two-performance/intent/frame/signoff.md
    intent/history/adopted/010-phase-two-performance/intent/organizing-document.md
    intent/history/adopted/011-phase-one-routing/intent/frame/direction.md
    intent/history/adopted/011-phase-one-routing/intent/frame/frame.md
    intent/history/adopted/011-phase-one-routing/intent/frame/manual-archive.md
    intent/history/adopted/011-phase-one-routing/intent/frame/options.md
    intent/history/adopted/011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff
    intent/history/adopted/011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md
    intent/history/adopted/011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md
    intent/history/adopted/011-phase-one-routing/intent/frame/phase-two/tier-two-panel/independent-coherence.md
    intent/history/adopted/011-phase-one-routing/intent/frame/phase-two/tier-two-panel/proof-integrity.md
    intent/history/adopted/011-phase-one-routing/intent/frame/phase-two/tier-two-panel/red-team-rejudge.md
    intent/history/adopted/011-phase-one-routing/intent/frame/phase-two/tier-two-panel/red-team.md
    intent/history/adopted/011-phase-one-routing/intent/frame/phase-two/tier-two-panel/security-permissions.md
    intent/history/adopted/011-phase-one-routing/intent/frame/phase-two/tier-two-panel/whole-acceptance-conformance.md
    intent/history/adopted/011-phase-one-routing/intent/frame/phase-two/units/unit-001.md
    intent/history/adopted/011-phase-one-routing/intent/frame/review-supplementary.md
    intent/history/adopted/011-phase-one-routing/intent/frame/review.md
    intent/history/adopted/011-phase-one-routing/intent/frame/signoff.md
    intent/history/adopted/011-phase-one-routing/intent/organizing-document.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/direction.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/frame.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/manual-archive.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/options.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/diffs/unit-001.diff
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/diffs/unit-002.diff
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/diffs/unit-003.diff
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/diffs/unit-004.diff
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/handoffs/unit-001.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/handoffs/unit-002.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/handoffs/unit-003.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/handoffs/unit-004.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/tier-one/unit-001.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/tier-one/unit-002.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/tier-one/unit-003.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/tier-one/unit-004.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/tier-two-panel/independent-coherence.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/tier-two-panel/proof-integrity.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/tier-two-panel/red-team.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/tier-two-panel/security-permissions.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/tier-two-panel/whole-acceptance-conformance.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/units/unit-001.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/units/unit-002.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/units/unit-003.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/phase-two/units/unit-004.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/review.md
    intent/history/adopted/012-self-applied-phase-two/intent/frame/signoff.md
    intent/history/adopted/012-self-applied-phase-two/intent/organizing-document.md
    intent/home.md
    intent/loop.md
    intent/machine-statements/active-work.md
    intent/machine-statements/adapter.md
    intent/machine-statements/collaboration.md
    intent/machine-statements/endorsement.md
    intent/machine-statements/foundations.md
    intent/machine-statements/home.md
    intent/machine-statements/loop.md
    intent/machine-statements/statements.md
    intent/machine-statements/structure.md
    intent/machine-statements/sweep.md
    intent/organizing-document.md
    intent/statements.md
    intent/structure.md
    intent/sweep.md
    
    exec
    /bin/bash -lc "sed -n '1,240p' 013-two-step-build/intent/frame/frame.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # frame - 013-two-step-build
    
    ## work
    
    Addressed node: root (hypercore)
    
    Node-local work name: 013-two-step-build
    
    Target segments: loop, adapter
    
    Work in flight: none other in flight (tree clean after the cache-removal commit `91f12aa`
    and the Claude-adapter-draft commit `60fb127`). Related but unadopted scratch:
    `DECOMPOSITION-FINDINGS.md` (seed-unit decomposition) and `WORK-NODE-COLLAPSE-FINDINGS.md`
    — ephemeral, not intent, read for coherence only. This frame derives from
    `TWO-STEP-BUILD-FINDINGS.md` (ephemeral seed, 2026-06-07), which is not itself intent.
    
    ## problem
    
    The signed frame today serves three consumers at one altitude and is compromised for all
    three: the operator signs it, the builder implements from it, and the acceptance panel
    judges against it. The result is dense feature-altitude units. Concrete evidence: work
    unit-003 (in 010) bundled builder/reviewer routing, the retry budget, strong escalation,
    operator-stop, and self-tests into one paragraph, and the gpt-5.5 build trace shows the
    builder *diagnosing architecture* and exercising feature-level judgement — not applying
    mechanical edits. Because units demand that judgement, the builder default is held at the
    strong model (`gpt-5.5`), and 010's cheap-builder (`gpt-5.3-codex-spark`) routing is an
    untested, unsafe bet: no work node has ever been built by spark. There is no artifact at an
    altitude a cheap builder can execute safely.
    
    ## constraints
    
    - C1 (settled, not re-opened): lean hard into two-step — frame -> (strong) plan -> (cheap)
      build is the path, not a maybe.
    - C2: the frame optimizes for operator + panel legibility — clear, separate, falsifiable
      statements; count bounded to *ownable claims*, not edits.
    - C3 (the guardrail): floor of judgeability. The frame stops being load-bearing in
      *execution* but stays load-bearing in *acceptance* — the panel must still be able to FLAG
      a wrong result against a frame statement *without reading code*. Legibility must never
      drift into "soft." Altitude test: judgeable-without-the-diff -> frame statement;
      only-means-something-next-to-the-diff -> task.
    - C4: spark executes *tasks*, never features; no node is ever built by spark at feature
      altitude. The strong model builds non-decomposable units directly (the proactive form of
      010's reactive three-fail escalation ladder).
    - C5: planner faithfulness is a new load-bearing seam. A strong model *planning* is not the
      same as the plan being *faithful to the frame*; a faithful-looking-but-wrong plan is a new
      way to ship a defect and must be caught by a check before the build trusts it.
    - C6 (operator info-gain lean, 2026-06-08): plan placement is a per-unit sub-step at the
      head of each build, not a whole-phase pass. Both route options honor this.
    - C7: `./check.sh` stays the proof floor, green at every phase-two unit boundary. 010's
      routing / retry / strong-escalation machinery and 008's tier-one + tier-two acceptance are
      extended, not replaced.
    - C8: on adoption, flip the builder default `gpt-5.5 -> gpt-5.3-codex-spark` (the held knob),
      because spark now executes tasks behind a legible review — the configuration that makes it
      safe. The strong-builder escalation knob stays intact.
    
    ## decision surface or open direction
    
    Open direction — needs operator selection via `./direction` from `options.md`. Per-unit
    placement (C6) is set by the operator's info-gain lean; the options differ on how much new
    governance and visibility surface the plan step carries:
    
    1. Plan visibility — sub-signature only (never surfaced) vs surfaced read-only to the operator.
    2. Non-decomposable declaration — planner self-report vs an explicit signal a check ratifies.
    3. Plan-faithfulness check — reuse the seed-unit "faithful carve" tier-one variant vs a
       purpose-built sibling `plan-faithfulness` lens.
    4. Altitude line — ratify the judgeability test as-is vs ratify-and-sharpen with baked-in
       frame-vs-task examples.
    
    These bundle into the two numbered options. Route is left open until `./direction`.
    
    Reversibility: one-way
    
    ## route
    
    PENDING — open direction. To be copied verbatim from the operator-selected numbered option
    in `options.md` at `./direction`. (Methodology-level loop/adapter contract change plus the
    spark builder flip, which accrues hard-to-revert build state; defaults one-way.)
    
    ## acceptance condition
    
    The loop gains a per-unit strong-model **plan** sub-step between the signed frame and the
    cheap build; the frame's altitude is governed by the floor of judgeability (C3); a
    plan-faithfulness check gates each plan before its build is trusted; non-decomposable units
    route to the strong builder; the builder default flips to `gpt-5.3-codex-spark`; `./check.sh`
    proves the new contract structurally; and for this one-way work the tier-two panel passes
    before archive. The selected option's specifics (visibility, faithfulness check shape,
    non-decomposable declaration, altitude wording) are honored by the build.
    
    ## observable acceptance
    
    - `./check.sh` exits 0 with new structural assertions that: (a) `loop` and `adapter` intent
      carry the plan-step, floor-of-judgeability, and plan-faithfulness statements; (b)
      `adapter/loop.sh` routes a per-unit plan sub-step through a strong-planner model knob
      *ahead of* the spark build, and exposes that knob; (c) the builder default token is
      `gpt-5.3-codex-spark`; (d) a plan-faithfulness verdict artifact is required per unit before
      that unit's build is trusted.
    - A dry-run / self-test of `loop.sh execute` records, per unit and in order, a strong-model
      plan artifact, then a plan-faithfulness verdict, then the (spark) build artifact, then the
      tier-one verdict — visible under the run's frame artifacts.
    
    ## excluded interpretation
    
    This work must NOT mean any of:
    
    - that the frame becomes "soft" or non-falsifiable — legibility is *to the floor of
      judgeability*, never below it; the panel must still FLAG a wrong result without reading code.
    - that any node is built by spark at feature altitude — spark executes tasks only;
      non-decomposable units go to the strong builder.
    - that the plan is signed by the operator or becomes operator-owned intent — the plan is
      sub-signature build material, not a frame and not a statement.
    - that 010's routing/retry/escalate or 008's acceptance tiers are replaced — they are extended.
    - that a strong model *planning* discharges faithfulness — the plan-faithfulness check is
      required, not optional or self-cleared.
    
    ## proof state
    
    Unproven until built: the plan-step contract (strong-planner knob present and ordered before
    the build; builder default = spark; per-unit plan-faithfulness artifact required) asserted by
    `./check.sh` and demonstrated by a dry-run execute trace. Existing 010 (routing/retry/escalate,
    resumable execute) and 008 (tier-one + tier-two acceptance) proofs are preserved and must stay
    green.
    
    ## sweep
    
    Concept map and likely clashes:
    
    - "fast builder / builder default held at strong until two-step lands" appears in
      `intent/loop.md`, `intent/machine-statements/loop.md`, `intent/adapter.md`,
      `intent/machine-statements/adapter.md`, `adapter/loop.sh` (header + `CODEX_BUILDER_MODEL`
      default + the two-step note), `adapter/codex.md`, `adapter/claude.md`, and `check.sh`
      assertions. Every "held until two-step lands" clause must flip to "two-step has landed;
      default is spark." This is the central coherence obligation.
    - Resumable execute was just rewritten by `91f12aa` (skip a unit whose tier-one PASS is on
      disk). The new per-unit plan + plan-faithfulness artifacts add to what a resume must
      account for; the resume statement must stay coherent with the added artifacts.
    - Tier-one acceptance (008) — plan-faithfulness is a new per-unit check that sits beside or
      reuses the tier-one reviewer; the route choice (reuse carve-variant vs purpose-built lens)
      decides which.
    - Seed-unit "faithful, non-pre-deciding carve" (`DECOMPOSITION-FINDINGS.md`, NOT adopted) —
      option 1 reuses its variant on the plan; that finding is unadopted scratch, so reuse means
      materializing the variant here, not depending on an unadopted node.
    - 010 routing/retry/escalate — C4's proactive "strong builds non-decomposable units" is the
      proactive form of the reactive three-fail ladder; they must compose, not contradict.
    - `collaboration` segment frame-legibility statements ("lean frame", "not proved by field
      count") must stay coherent with C2/C3 — two-step adds no frame field, it sets the frame's
      altitude doctrine; flag if any collaboration statement implies the frame is
      implementation-complete.
    - Known debt (carried, not fixed here): the one-way review prompt assumes a signed
      route-settled frame, so it will FLAG this correctly-staged pre-direction frame; its verdict
      is read with that caveat (recorded by 011, see memory).
    
    ## adoption claim
    
    Adopt: fold the plan-step, floor-of-judgeability, plan-faithfulness, and
    non-decomposable-routing statements into the `loop` and `adapter` segments; flip the
    `CODEX_BUILDER_MODEL` default to `gpt-5.3-codex-spark`; materialize the mechanism in
    `adapter/loop.sh` and the gate contracts; assert it all in `./check.sh`; pass the one-way
    tier-two panel; and stamp the operator's endorsement on the `loop` and `adapter` segments.
    
    ## shelving claim
    
    Shelve: if the operator rejects both options or the build cannot prove the contract, record
    013 as shelved history under `intent/history/shelved/` without flipping the builder default
    or adding the plan step; the builder stays held at `gpt-5.5` and the findings remain
    ephemeral scratch for a later attempt.
    
    exec
    /bin/bash -lc 'find 013-two-step-build/intent/frame -maxdepth 2 -type f -print | sort' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    013-two-step-build/intent/frame/frame.md
    013-two-step-build/intent/frame/options.md
    
    exec
    /bin/bash -lc "sed -n '1,220p' 013-two-step-build/intent/frame/options.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # options - 013-two-step-build
    
    Direction options are drafted by the machine for operator selection. The operator
    selects one route, rejects all options, or aborts without writing direction.
    
    Both options share the settled spine: a per-unit strong-model plan sub-step between the
    signed frame and the cheap build (C6); the frame held to the floor of judgeability (C3);
    spark executes tasks while the strong model builds non-decomposable units (C4); a required
    plan-faithfulness check (C5); and the builder default flipped to `gpt-5.3-codex-spark` (C8).
    They differ on how much new governance and visibility surface the plan step carries.
    
    ## option 1
    
    id: minimal-two-step
    kind: selected-route
    summary: Minimal-surface two-step. The per-unit plan is sub-signature and never surfaced to
      the operator. The planner self-reports a unit as non-decomposable ("cannot separate into
      mechanical tasks"), which routes that unit straight to the strong builder. Plan
      faithfulness reuses the seed-unit "faithful, non-pre-deciding carve" tier-one variant,
      materialized here and applied to the plan — no new check type. The altitude line ratifies
      the findings' judgeability test as-is.
    reversibility: one-way
    tradeoff: Smallest new surface, fastest to ship, fewest new seams to prove. Cost: the
      operator never inspects the plan, so trust rests entirely on the planner plus the reused
      faithfulness check; and a carve-check built for node->child carving may fit the
      frame->task plan imperfectly.
    
    ## option 2
    
    id: audited-two-step
    kind: selected-route
    summary: Audited two-step. The per-unit plan is surfaced read-only to the operator
      (available, unsigned, not required reading). Non-decomposability is an explicit signal the
      planner emits that a check ratifies before routing to the strong builder, not bare
      self-report. Plan faithfulness is a purpose-built `plan-faithfulness` tier-one lens
      distinct from the carve check, with the floor-of-judgeability test baked into its prompt.
      The altitude line is ratified and sharpened with explicit frame-vs-task examples baked into
      the plan and faithfulness gate prompts.
    reversibility: one-way
    tradeoff: Most legible and auditable, strongest faithfulness seam, sharpest altitude
      guidance. Cost: the largest new surface to build and prove, and surfacing the plan
      read-only risks partially re-drowning the operator the frame split was meant to prevent.
    
    ## rejection choices
    
    none: The operator may reject all options and send the work back to frame.
    abort: The operator may abort without writing direction.
    
    codex
    The frame directory contains only `frame.md` and `options.md`; there is no `direction.md` or `signoff.md`, and the frame itself leaves route as `PENDING`. I’m checking the referenced `loop` and `adapter` intent now to avoid overreaching beyond the requested surface.
    exec
    /bin/bash -lc "sed -n '1,260p' intent/machine-statements/loop.md" in /home/qqp/projects/hypercore
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
    `loop.sh execute <work-name>` re-execs from a read-only snapshot of `adapter/loop.sh` at
    execute start before phase-two builders, reviewers, or archive actors can edit the live
    orchestrator material.
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
    `loop.sh execute <work-name>` passes only dynamic unit identifiers, proof obligation, and
    signed-frame location to the implement actor; the implement contract lives in
    `adapter/gates/implement.md`, which `run_gate` reads for each invocation.
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
    `loop.sh execute <work-name>` resumes from on-disk artifacts: it skips a unit whose tier-one
    acceptance artifact is already a clean PASS for the current signed frame, and rebuilds any
    unit without that artifact.
    `loop.sh execute <work-name>` treats malformed, evidence-free, or unsupported-source
    implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
    concurrent one-way tier-two panel before archive.
    `loop.sh execute <work-name>` passes only dynamic work location, acceptance artifact
    location, and the archive decision line to the archive actor; the archive contract lives in
    `adapter/gates/archive.md`, which `run_gate` reads for each invocation.
    `loop.sh execute <work-name>` records the addressed work in node-local history after archive.
    
    exec
    /bin/bash -lc "sed -n '1,260p' intent/adapter.md" in /home/qqp/projects/hypercore
    exec
    /bin/bash -lc "sed -n '1,260p' intent/loop.md" in /home/qqp/projects/hypercore
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
    the phase-two orchestrator protects self-editing work by running execute from a snapshot
    made at execute start; later edits to the live orchestrator material do not change the
    already-running process.
    phase two has a real supervisor-to-executor handoff: after sign-off, an outer supervisor
    launches a fresh phase-two executor from the addressed node and supervises its recorded
    progress, intervening only when the loop blocks on a real gate failure or operator need.
    `start` creates a new work node for phase one; `execute` enters phase two for signed work,
    and omitting the execute work name is only an inference convenience that succeeds when
    exactly one signed, unarchived work node exists in the addressed node and blocks otherwise.
    the implement and archive gate contracts live in re-read gate files, not in frozen inline
    orchestrator strings; `adapter/loop.sh` supplies only dynamic unit or work context and the
    archive decision line.
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
    `adapter/loop.sh` snapshots and re-execs itself at the start of `execute`, using the
    original root adapter paths for gate files and the snapshot path for the running loop
    version digest.
    the loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
    `.hypercore/loop-runs`, with run-local state, event history, raw harness gate streams, gate
    final outputs, acceptance artifact paths, and current pointers for the addressed work and
    root.
    the loop streams inner executor JSON events into the phase-two run state while
    printing concise progress, without changing the cleared-session contract.
    the loop materializes separate builder and reviewer routing, structured acceptance
    artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
    then strong-builder escalation ladder, on-disk resumable execute that skips a unit already
    carrying a clean tier-one PASS for the signed frame, the concurrent one-way tier-two panel,
    and phase-one review subprocess crash diagnostics.
    `adapter/loop.sh` accepts one node-local work name in the addressed node for new work.
    the root node is the default addressed node.
    `loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node, including a
    linked mounted child when `<node-path>` is its mount path.
    `loop.sh start <work-name>` creates a work node directly under the addressed node.
    `loop.sh execute` without `<work-name>` resolves the single signed, unarchived work node in
    the addressed node and blocks when there are zero or more than one.
    `loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work
    and act only on that addressed work.
    `loop.sh execute <work-name>` records only the addressed node-local work in that node's
    history.
    the orchestrator creates, signs, executes, and records only addressed node-local work
    nodes.
    the gate prompts use addressed-node and node-local work wording and point cleared sessions
    at the addressed work frame.
    the implement and archive gate prompts carry their contract in `adapter/gates/implement.md`
    and `adapter/gates/archive.md`; `run_gate` reads those files for each invocation, so a
    self-change to a gate prompt can affect the next gate invocation in the same execute run.
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
    builder/reviewer routing with bounded retry and strong escalation, on-disk resumable execute
    that skips units already carrying a clean tier-one PASS, the concurrent tier-two panel, the
    re-read implement/archive prompt contract and
    absence of frozen inline implement/archive contract text, the new operator-act and
    phase-two performance contract in the `collaboration`, `loop`, and `adapter` segments, and
    current-material absence of the retired compatibility route still carry the contract.
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
    execute runs phase two from an orchestrator snapshot made at execute start, so a unit that
    edits the live orchestrator material cannot corrupt the already-running phase-two process.
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
    when a unit's own proof is a check over addressed-node intent, implement may edit that
    intent in the unit; those edits remain in-flight proof material until archive adoption.
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
    execute is resumable from the signed frame and on-disk artifacts: a unit is reused on a
    rerun only when its tier-one acceptance artifact is already present as a clean PASS for the
    current signed frame, and any unit without that artifact is rebuilt.
    unresolved required tier-one or tier-two `FLAG`s halt phase two before archive; the active
    work node remains in flight for the operator.
    the checks re-run for every statement, not only the ones a work node touched.
    drift is a check that falls without work meaning to break it, and it surfaces wherever it
    happens.
    archive: adopt or shelve the work according to the signed frame.
    one-way archive cannot fold or stamp until required implementation-acceptance artifacts
    are present and clean.
    adoption verifies the accepted applied delta against the signed frame, stamps each touched
    segment's foot with this operator, and records the work node as adopted history.
    adoption does not re-fold intent statements that phase-two units already applied in place.
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
    `loop.sh execute <work-name>` re-execs from a read-only snapshot of `adapter/loop.sh` at
    execute start before phase-two builders, reviewers, or archive actors can edit the live
    orchestrator material.
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
    `loop.sh execute <work-name>` passes only dynamic unit identifiers, proof obligation, and
    signed-frame location to the implement actor; the implement contract lives in
    `adapter/gates/implement.md`, which `run_gate` reads for each invocation.
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
    `loop.sh execute <work-name>` resumes from on-disk artifacts: it skips a unit whose tier-one
    acceptance artifact is already a clean PASS for the current signed frame, and rebuilds any
    unit without that artifact.
    `loop.sh execute <work-name>` treats malformed, evidence-free, or unsupported-source
    implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
    concurrent one-way tier-two panel before archive.
    `loop.sh execute <work-name>` passes only dynamic work location, acceptance artifact
    location, and the archive decision line to the archive actor; the archive contract lives in
    `adapter/gates/archive.md`, which `run_gate` reads for each invocation.
    `loop.sh execute <work-name>` records the addressed work in node-local history after archive.
    
    ---
    endorsed by qqp-dev
    
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
    `adapter/loop.sh` snapshots and re-execs itself at the start of `execute`, using the
    original root adapter paths for gate files and the snapshot path for the running loop
    version digest.
    the loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
    `.hypercore/loop-runs`, with run-local state, event history, raw harness gate streams, gate
    final outputs, acceptance artifact paths, and current pointers for the addressed work and
    root.
    the loop streams inner executor JSON events into the phase-two run state while
    printing concise progress, without changing the cleared-session contract.
    the current handoff path is that an outer supervisor launches a fresh phase-two executor
    from the addressed node and supervises the loop's recorded progress, intervening only when
    the loop blocks on a real gate failure or operator need.
    the loop materializes separate builder and reviewer routing, structured acceptance
    artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
    then strong-builder escalation ladder, on-disk resumable execute that skips a unit already
    carrying a clean tier-one PASS for the signed frame, the concurrent
    one-way tier-two panel, and phase-one review subprocess crash diagnostics.
    the loop keeps the contract-bearing implement and archive prompt text in
    `adapter/gates/implement.md` and `adapter/gates/archive.md`, while inline execute prompts
    carry only dynamic unit or work context and the archive decision line.
    `adapter/loop.sh` accepts one node-local work name in the addressed node for new work.
    the root node is the default addressed node.
    `loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node, including a
    linked mounted child when `<node-path>` is its mount path.
    `loop.sh start <work-name>` creates a work node directly under the addressed node.
    `loop.sh execute` without `<work-name>` resolves the single signed, unarchived work node in
    the addressed node and blocks when there are zero or more than one.
    `start` is the new-work phase-one entry point, while `execute` is the signed-work phase-two
    entry point.
    `loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work
    and act only on that addressed work.
    `loop.sh execute <work-name>` records only the addressed node-local work in that node's
    history.
    the orchestrator creates, signs, executes, and records only addressed node-local work
    nodes.
    the gate prompts use addressed-node and node-local work wording and point cleared sessions
    at the addressed work frame.
    the implement and archive gate prompts carry their contract in `adapter/gates/implement.md`
    and `adapter/gates/archive.md`; `run_gate` reads those files for each invocation, so a
    self-change to a gate prompt can affect the next gate invocation in the same execute run.
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
    builder/reviewer routing with bounded retry and strong escalation, on-disk resumable execute
    that skips units already carrying a clean tier-one PASS, the concurrent tier-two panel, the
    re-read implement/archive prompt contract and
    absence of frozen inline implement/archive contract text, the new operator-act and
    phase-two performance contract in the `collaboration`, `loop`, and `adapter` segments, and
    current-material absence of the retired compatibility route still carry the contract.
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
    VERDICT: FLAG
    NOTE: The frame is not signed or route-settled: `route` is PENDING/open direction and the frame directory lacks `direction.md` and `signoff.md`.
    hook: Stop
    hook: Stop Completed
    tokens used
    34,061

