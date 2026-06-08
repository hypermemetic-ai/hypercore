# review - 011-phase-one-routing

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

- contract-checkability (base): The frame is not signed or route-settled: `direction.md` and `signoff.md` are absent, and `frame.md` leaves `route` as TODO.
- soundness-fit (base): `signoff.md` is absent and the frame route is still `TODO`, so this is not a signed, complete frame.
- simplicity-fastness (base): The frame is not route-settled or signed: `route` remains TODO and no direction/signoff artifact is present.
- red-team (base): The frame directory has no `direction.md` or `signoff.md`, and `frame.md` still has `route` as TODO, so the artifact is not a signed, settled frame.

## reviewer notes

### contract-checkability

The frame is not signed or route-settled: `direction.md` and `signoff.md` are absent, and `frame.md` leaves `route` as TODO.

### soundness-fit

`signoff.md` is absent and the frame route is still `TODO`, so this is not a signed, complete frame.

### simplicity-fastness

The frame is not route-settled or signed: `route` remains TODO and no direction/signoff artifact is present.

### red-team

The frame directory has no `direction.md` or `signoff.md`, and `frame.md` still has `route` as TODO, so the artifact is not a signed, settled frame.

## reviewer diagnostics

### contract-checkability

status: 0
selected-output-source: final-output

#### selected output

    VERDICT: FLAG
    NOTE: The frame is not signed or route-settled: `direction.md` and `signoff.md` are absent, and `frame.md` leaves `route` as TODO.

#### final output

    VERDICT: FLAG
    NOTE: The frame is not signed or route-settled: `direction.md` and `signoff.md` are absent, and `frame.md` leaves `route` as TODO.

#### stdout

    VERDICT: FLAG
    NOTE: The frame is not signed or route-settled: `direction.md` and `signoff.md` are absent, and `frame.md` leaves `route` as TODO.

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
    session id: 019ea478-6c6d-71d1-9a6f-51be20393826
    --------
    user
    Review role: contract-checkability
    Work: 011-phase-one-routing
    Frame directory: 011-phase-one-routing/intent/frame
    
    Read only the signed work frame and the intent it references. Do not debate other reviewers.
    Return exactly one structured verdict line:
    VERDICT: PASS
    or
    VERDICT: FLAG
    
    Then optionally add one NOTE: line. Treat uncertainty as FLAG.
    hook: UserPromptSubmit
    hook: UserPromptSubmit Completed
    exec
    /bin/bash -lc "sed -n '1,240p' intent/organizing-document.md" in /home/qqp/projects/hypercore
    exec
    /bin/bash -lc "sed -n '1,240p' hypercore.md" in /home/qqp/projects/hypercore
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
      the root by the methodology prose, the harness adapter (`AGENTS.md` for Codex), and the
      orchestrator under `adapter/`.
    
    The **governed work** -- durable child nodes and mounted work under this root:
    
    - **home** -- the named child node at `home/`, with its own `intent/`, that mounts linked
      project nodes and governs them within itself. home currently mounts `codex-cockpit`.
    
    Each segment has an intent document at `intent/<segment>.md` and a machine-statements file
    at `intent/machine-statements/<segment>.md`. A child node is a directory or settled linked
    entry point carrying its own `intent/`; a mounted project is a child node of home, a
    separate corpus exposed through `home/<name>` as a symbolic link to its own repository.
    
    This is two groups, not a tag: nothing is partitioned twice. A tag is added only the first
    time a real second partition of the whole corpus forces it, not before.
    
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
    /bin/bash -lc 'pwd && rg --files 011-phase-one-routing/intent/frame intent | sort' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    /home/qqp/projects/hypercore
    011-phase-one-routing/intent/frame/frame.md
    011-phase-one-routing/intent/frame/options.md
    011-phase-one-routing/intent/frame/review.md
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
    /bin/bash -lc "sed -n '1,260p' 011-phase-one-routing/intent/frame/frame.md" in /home/qqp/projects/hypercore
    exec
    /bin/bash -lc 'find 011-phase-one-routing/intent/frame -maxdepth 2 -type f -print | sort' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    011-phase-one-routing/intent/frame/frame.md
    011-phase-one-routing/intent/frame/options.md
    011-phase-one-routing/intent/frame/review.md
    
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
    - Materialization stays product-specific: the adapter prose (`adapter/codex.md`), the harness
      entry point (`AGENTS.md`), the orchestrator's actual harness calls in `adapter/loop.sh`,
      and config-knob *values* legitimately name the current binding. De-name the claims, not the
      mechanism.
    - Preserve the proof floor: the review floor and acceptance tiers stay strong; routing never
      demotes them. The phase-one collaborator that frames a one-way work node must not be the
      review floor that scrutinizes it — the framer is not its own witness.
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
    
    Reversibility: one-way
    
    ## route
    
    TODO — written only after `./direction` records the selected option.
    
    ## acceptance condition
    
    After adoption: the `collaboration`/`loop`/`adapter` contract (intent and machine statements),
    the adapter prose, and `check.sh` express the harness binding in role and config terms with no
    harness product named in any *statement*; a phase-one *collaborator* role and a phase-one
    routing/delegation seam exist with held defaults that reproduce current behavior; the strong
    review floor's independence from the framer is stated; and `./check.sh` is green.
    
    ## observable acceptance
    
    - `./check.sh` exits zero after implementation and after the archive fold.
    - A check asserts that no contract *statement* file (`intent/collaboration.md`,
      `intent/loop.md`, `intent/adapter.md`, and their `machine-statements/` counterparts)
      contains a harness-product token — product names and product-bearing knob identifiers alike
      — outside a fenced materialization-pointer context; the exact token set and pointer
      exception are fixed in the route.
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
    
    ## proof state
    
    Required proof: the observable-acceptance checks above, plus `check.sh` self-tests that a
    product-named contract statement fails the product-absence check, and that the held defaults
    reproduce current routing when the knobs are unset. Baseline `./check.sh` is green before
    implementation (to be confirmed at the start of phase two).
    
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
    
    exec
    /bin/bash -lc "sed -n '1,260p' 011-phase-one-routing/intent/frame/options.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # options - 011-phase-one-routing
    
    Direction options are drafted by the machine for operator selection. The operator
    selects one route, rejects all options, or aborts without writing direction.
    
    ## option 1
    
    id: contract-only-denaming
    kind: selected-route
    summary: De-name the whole contract (collaboration/loop/adapter statements and machine statements, the adapter prose, and check.sh) to role and config terms; add the phase-one collaborator role and a phase-one routing/delegation seam with held defaults; keep the materialization product-specific, including the existing CODEX_* environment-knob names, which are materialization config rather than contract.
    reversibility: one-way
    tradeoff: Smallest diff to the running mechanism and to operator muscle memory; the contract is fully product-agnostic, but config-knob identifiers still read CODEX_*, a minor residual product name at the materialization edge.
    
    ## option 2
    
    id: contract-and-knob-denaming
    kind: selected-route
    summary: Everything in option 1, plus neutralize the config-knob identifiers themselves (the CODEX_* environment variables become harness-neutral names), keeping the old names as cheap aliases where practical so existing configuration does not break.
    reversibility: one-way
    tradeoff: Fullest product-agnostic surface, down to the environment-variable names; larger blast radius across the loop.sh env interface, check.sh, and any references to the knob names, with alias upkeep to avoid breaking existing CODEX_* configuration.
    
    ## rejection choices
    
    none: Reject all options and send the work back to frame for a different route surface.
    abort: Abort without recording direction.
    
    exec
    /bin/bash -lc "sed -n '1,260p' 011-phase-one-routing/intent/frame/review.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # review - 011-phase-one-routing
    
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
    
    - contract-checkability (base): The frame is unsigned/incomplete: no signoff or direction artifact exists, and `frame.md` leaves the route as TODO.
    - soundness-fit (base): Option 3 conflicts with the frame's acceptance/adoption condition requiring no harness product token in any contract statement.
    - simplicity-fastness (base): The provided frame is not route-settled: `route` remains TODO, so simplicity-fastness cannot clear it without uncertainty.
    - red-team (base): The frame is not signed and still has `route: TODO`, so the reviewed artifact cannot be treated as a settled signed route.
    
    ## reviewer notes
    
    ### contract-checkability
    
    The frame is unsigned/incomplete: no signoff or direction artifact exists, and `frame.md` leaves the route as TODO.
    
    ### soundness-fit
    
    Option 3 conflicts with the frame's acceptance/adoption condition requiring no harness product token in any contract statement.
    
    ### simplicity-fastness
    
    The provided frame is not route-settled: `route` remains TODO, so simplicity-fastness cannot clear it without uncertainty.
    
    ### red-team
    
    The frame is not signed and still has `route: TODO`, so the reviewed artifact cannot be treated as a settled signed route.
    
    ## reviewer diagnostics
    
    ### contract-checkability
    
    status: 0
    selected-output-source: final-output
    
    #### selected output
    
        VERDICT: FLAG
        NOTE: The frame is unsigned/incomplete: no signoff or direction artifact exists, and `frame.md` leaves the route as TODO.
    
    #### final output
    
        VERDICT: FLAG
        NOTE: The frame is unsigned/incomplete: no signoff or direction artifact exists, and `frame.md` leaves the route as TODO.
    
    #### stdout
    
        VERDICT: FLAG
        NOTE: The frame is unsigned/incomplete: no signoff or direction artifact exists, and `frame.md` leaves the route as TODO.
    
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
        session id: 019ea472-3b2d-7e73-814b-cf5329f75d1a
        --------
        user
        Review role: contract-checkability
        Work: 011-phase-one-routing
        Frame directory: 011-phase-one-routing/intent/frame
        
        Read only the signed work frame and the intent it references. Do not debate other reviewers.
        Return exactly one structured verdict line:
        VERDICT: PASS
        or
        VERDICT: FLAG
        
        Then optionally add one NOTE: line. Treat uncertainty as FLAG.
        hook: UserPromptSubmit
        hook: UserPromptSubmit Completed
        exec
        /bin/bash -lc "sed -n '1,220p' 011-phase-one-routing/intent/frame/frame.md" in /home/qqp/projects/hypercore
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
          or `adapter` names a specific harness product. Role and config-slot vocabulary only.
        - Materialization stays product-specific: the adapter prose (`adapter/codex.md`), the harness
          entry point (`AGENTS.md`), the orchestrator's actual harness calls in `adapter/loop.sh`,
          and config-knob *values* legitimately name the current binding. De-name the claims, not the
          mechanism.
        - Preserve the proof floor: the review floor and acceptance tiers stay strong; routing never
          demotes them. The phase-one collaborator that frames a one-way work node must not be the
          review floor that scrutinizes it — the framer is not its own witness.
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
        a product-agnostic role/config contract that de-names the whole adapter contract. The one
        genuine remaining fork is the de-naming boundary for config-knob *identifiers*, with a
        smaller fallback retained in case review finds the full scope too large to land coherently in
        one node. See `intent/frame/options.md`.
        
        Reversibility: one-way
        
        ## route
        
        TODO — written only after `./direction` records the selected option.
        
        ## acceptance condition
        
        After adoption: the `collaboration`/`loop`/`adapter` contract (intent and machine statements),
        the adapter prose, and `check.sh` express the harness binding in role and config terms with no
        harness product named in any *statement*; a phase-one *collaborator* role and a phase-one
        routing/delegation seam exist with held defaults that reproduce current behavior; the strong
        review floor's independence from the framer is stated; and `./check.sh` is green.
        
        ## observable acceptance
        
        - `./check.sh` exits zero after implementation and after the archive fold.
        - A check asserts that no contract *statement* file (`intent/collaboration.md`,
          `intent/loop.md`, `intent/adapter.md`, and their `machine-statements/` counterparts)
          contains a harness-product token outside a fenced materialization-pointer context; the exact
          token set and pointer exception are fixed in the route.
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
        
        ## proof state
        
        Required proof: the observable-acceptance checks above, plus `check.sh` self-tests that a
        product-named contract statement fails the product-absence check, and that the held defaults
        reproduce current routing when the knobs are unset. Baseline `./check.sh` is green before
        implementation (to be confirmed at the start of phase two).
        
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
        or if the full scope cannot land coherently in one node and the operator does not fall back
        to the smaller option.
        
        exec
        /bin/bash -lc "sed -n '1,120p' 011-phase-one-routing/intent/frame/signoff.md" in /home/qqp/projects/hypercore
         exited 2 in 0ms:
        sed: can't read 011-phase-one-routing/intent/frame/signoff.md: No such file or directory
        
        exec
        /bin/bash -lc 'rg --files 011-phase-one-routing/intent/frame' in /home/qqp/projects/hypercore
         succeeded in 0ms:
        011-phase-one-routing/intent/frame/options.md
        011-phase-one-routing/intent/frame/frame.md
        
        exec
        /bin/bash -lc 'find 011-phase-one-routing -maxdepth 4 -type f | sort' in /home/qqp/projects/hypercore
        exec
        /bin/bash -lc "sed -n '1,220p' 011-phase-one-routing/intent/frame/options.md" in /home/qqp/projects/hypercore
         succeeded in 0ms:
        # options - 011-phase-one-routing
        
        Direction options are drafted by the machine for operator selection. The operator
        selects one route, rejects all options, or aborts without writing direction.
        
        ## option 1
    
    exec
    /bin/bash -lc "sed -n '1,280p' intent/loop.md" in /home/qqp/projects/hypercore
    exec
    /bin/bash -lc "sed -n '1,260p' intent/collaboration.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # collaboration
    
    operator-machine collaboration is a first-class methodology concern, separate from the loop mechanics that enforce it.
    collaboration is the working relation by which operator and machine keep the work scrutable, sound, and fast across memoryless sessions.
    effective collaboration is complementarity, not maximal automation: the operator sets purpose, constraints, acceptance, and open direction; the machine searches, synthesizes, drafts, executes, checks, and settles only what the intent and operator leave open.
    collaboration keeps common ground recoverable without treating field count as proof of collaboration quality.
    phase one is an arc: understanding before route, scrutiny sized by reversibility, operator direction, lean recoverability, and sign-off.
    before a route is written, the machine gives a teach-back, at least one alternative framing, information-gain questions, and a reversibility classification.
    one-way work requires distinct-route scrutiny before route settlement, including a mechanically spawned base review roster.
    the base review roster is `contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`; optional reviewers are additive and advisory only.
    optional reviewers cannot override, outvote, average away, or dilute unresolved base-roster or red-team flags.
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
    the addressed work's current or recent gate, current unit, status, Codex thread id, latest
    message, failure reason, event history, run artifact paths, and phase-two acceptance
    artifact paths are recoverable from loop state files.
    
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
    runs and after recent failure or completion, including the active gate, status, Codex
    thread id, latest message, event history, and run artifact paths.
    before launching the first phase-two Codex gate, `loop.sh execute <work-name>` checks that
    the Codex binary is present and that Codex home/session state is writable; a failed
    preflight records failed run state and stops before `codex exec`.
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
    fresh Codex builder session for each unit, and records lean unit handoff, diff, and
    tier-one verdict artifacts under the work frame.
    `loop.sh execute <work-name>` routes builders through `CODEX_BUILDER_MODEL`, defaulting to
    the strong model until the two-step plan/build work lands, separately from the strong review
    route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
    to `CODEX_STRONG_BUILDER_MODEL`, and stops for the operator when the strong builder fails.
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
    direction and review are phase-one acts or artifacts, not loop gates.
    the Codex review roster for one-way phase-one work has a base roster of
    `contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`.
    the Codex implementation-acceptance reviewer for each phase-two unit is independent and
    read-only.
    the Codex tier-two implementation-acceptance panel for one-way work has required lenses
    `whole-acceptance-conformance`, `proof-integrity`, `independent-coherence`,
    `security-permissions`, and `red-team`.
    the complete optional Codex review roster is `implementation-maintainability`,
    `security-permissions`, `operator-ergonomics`, `migration-compatibility`,
    `domain-evidence`, and `performance-cost`.
    optional reviewers are advisory additions and cannot override, outvote, average away, or
    dilute unresolved base-roster or red-team flags.
    the Codex adapter classifies the request surface before changing material: ordinary
    conversation and read-only inspection may proceed directly, while governed work starts or
    continues a work node.
    the Codex adapter rejects perceived simplicity, file count, convenience, and low risk as
    waivers for governed work.
    on request the adapter renders a statement of the intent intelligible in plain language
    without altering it.
    the adapter carries only what the intent cannot yet reach the harness with -- the order to
    read the intent first, and disciplines not yet written as statements; each is a debt,
    folded into the intent by later work and then dropped.
    an adapter is per harness; one node may be bound by more than one, each loaded by its own
    harness.
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
    the Codex harness loads its adapter through a root `AGENTS.md` symlinked to
    `adapter/codex.md`; the root entry is the harness's mandated pointer, holding nothing, not
    where the adapter lives.
    a machine working in a nested node under the root is bound by Codex including the root
    `AGENTS.md` in the project instruction chain from the project root to the current
    directory, so no node below the root carries its own adapter material.
    a mounted external project may carry a target-local `AGENTS.md` entry point for
    direct-path openings; the entry point links to root-managed adapter material and routes
    back to the root adapter and loop instead of copying root adapter material into the
    mounted node.
    the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
    over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
    builder session from the signed frame, and acceptance reviewers and the archive actor are
    fresh sessions rather than resumes of the builder.
    the Codex loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
    `.hypercore/loop-runs`, with run-local state, event history, raw Codex gate streams, gate
    final outputs, acceptance artifact paths, and current pointers for the addressed work and
    root.
    the Codex loop streams inner `codex exec --json` events into the phase-two run state while
    printing concise progress, without changing the cleared-session contract.
    the Codex loop materializes separate builder and reviewer routing, structured acceptance
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
    the Codex adapter prose describes phase one as design-phase collaboration with direction
    and review artifacts, while preserving phase two as cleared, heads-down execution from the
    signed frame directory and lean phase-two handoff artifacts.
    `check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
    validation, start scaffolding, direction/review helpers, operator-act gating through
    `/dev/tty` with B-ready `operator-gate:` markers and numbered-option direction, review and
    acceptance isolation settings, strict frame parsing, phase-two acceptance gating, structured
    acceptance legibility, acceptance source markers and fake-source rejection, separate
    builder/reviewer routing with bounded retry and strong escalation, resumable execute
    caching, the concurrent tier-two panel, the new operator-act and phase-two performance
    contract in the `collaboration`, `loop`, and `adapter` segments, and current-material
    absence of the retired compatibility route still carry the contract.
    each gate's instructions are held in a file in `adapter/gates/`; the Codex path includes them in
    the `codex exec` gate prompt; the orchestrator owns gate order and preconditions and
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
    /bin/bash -lc "sed -n '1,240p' intent/machine-statements/collaboration.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # collaboration — machine statements
    
    phase-two handoff state is written as common ground for the operator and later tooling:
    the addressed work's current or recent gate, current unit, status, Codex thread id, latest
    message, failure reason, event history, run artifact paths, and phase-two acceptance
    artifact paths are recoverable from loop state files.
    
    exec
    /bin/bash -lc "test -f 011-phase-one-routing/intent/frame/direction.md; printf 'direction:%s\\n' \""'$?"; test -f 011-phase-one-routing/intent/frame/signoff.md; printf '"'signoff:%s\\n' \""'$?"' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    direction:1
    signoff:1
    
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
    runs and after recent failure or completion, including the active gate, status, Codex
    thread id, current unit, latest message, failure reason, event history, run artifact
    paths, and phase-two acceptance artifact paths.
    before launching the first phase-two Codex gate, `loop.sh execute <work-name>` checks that
    the Codex binary is present and that Codex home/session state is writable; a failed
    preflight records failed run state and stops before `codex exec`.
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
    fresh Codex builder session for each unit, and records lean unit handoff, diff, and
    tier-one verdict artifacts under the work frame.
    `loop.sh execute <work-name>` routes builders through `CODEX_BUILDER_MODEL`, defaulting to
    the strong model until the two-step plan/build work lands, separately from the strong review
    route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
    to `CODEX_STRONG_BUILDER_MODEL`, and stops for the operator when the strong builder fails.
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
    the Codex harness loads its adapter through a root `AGENTS.md` symlinked to
    `adapter/codex.md`; the root entry is the harness's mandated pointer, holding nothing, not
    where the adapter lives.
    a machine working in a nested node under the root is bound by Codex including the root
    `AGENTS.md` in the project instruction chain from the project root to the current
    directory, so no node below the root carries its own adapter material.
    a mounted external project may carry a target-local `AGENTS.md` entry point for
    direct-path openings; the entry point links to root-managed adapter material and routes
    back to the root adapter and loop instead of copying root adapter material into the
    mounted node.
    the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
    over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
    builder session from the signed frame, and acceptance reviewers and the archive actor are
    fresh sessions rather than resumes of the builder.
    the Codex loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
    `.hypercore/loop-runs`, with run-local state, event history, raw Codex gate streams, gate
    final outputs, acceptance artifact paths, and current pointers for the addressed work and
    root.
    the Codex loop streams inner `codex exec --json` events into the phase-two run state while
    printing concise progress, without changing the cleared-session contract.
    the Codex loop materializes separate builder and reviewer routing, structured acceptance
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
    the Codex adapter prose describes phase one as design-phase collaboration with direction
    and review artifacts, while preserving phase two as cleared, heads-down execution from the
    signed frame directory and lean phase-two handoff artifacts.
    `check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
    validation, start scaffolding, direction/review helpers, operator-act gating through
    `/dev/tty` with B-ready `operator-gate:` markers and numbered-option direction, review and
    acceptance isolation settings, strict frame parsing, phase-two acceptance gating, structured
    acceptance legibility, acceptance source markers and fake-source rejection, separate
    builder/reviewer routing with bounded retry and strong escalation, resumable execute
    caching, the concurrent tier-two panel, the new operator-act and phase-two performance
    contract in the `collaboration`, `loop`, and `adapter` segments, and current-material
    absence of the retired compatibility route still carry the contract.
    each gate's instructions are held in a file in `adapter/gates/`; the Codex path includes them in
    the `codex exec` gate prompt; the orchestrator owns gate order and preconditions and
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
    NOTE: The frame is not signed or route-settled: `direction.md` and `signoff.md` are absent, and `frame.md` leaves `route` as TODO.
    hook: Stop
    hook: Stop Completed
    tokens used
    25,851

### soundness-fit

status: 0
selected-output-source: final-output

#### selected output

    VERDICT: FLAG
    NOTE: `signoff.md` is absent and the frame route is still `TODO`, so this is not a signed, complete frame.

#### final output

    VERDICT: FLAG
    NOTE: `signoff.md` is absent and the frame route is still `TODO`, so this is not a signed, complete frame.

#### stdout

    VERDICT: FLAG
    NOTE: `signoff.md` is absent and the frame route is still `TODO`, so this is not a signed, complete frame.

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
    session id: 019ea479-f151-7242-abcd-ab7f19555107
    --------
    user
    Review role: soundness-fit
    Work: 011-phase-one-routing
    Frame directory: 011-phase-one-routing/intent/frame
    
    Read only the signed work frame and the intent it references. Do not debate other reviewers.
    Return exactly one structured verdict line:
    VERDICT: PASS
    or
    VERDICT: FLAG
    
    Then optionally add one NOTE: line. Treat uncertainty as FLAG.
    hook: UserPromptSubmit
    hook: UserPromptSubmit Completed
    codex
    I’ll read the signed frame artifacts first, then only the intent segments explicitly named by that frame before returning the one-line verdict format.
    exec
    /bin/bash -lc "sed -n '1,240p' 011-phase-one-routing/intent/frame/frame.md" in /home/qqp/projects/hypercore
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
    - Materialization stays product-specific: the adapter prose (`adapter/codex.md`), the harness
      entry point (`AGENTS.md`), the orchestrator's actual harness calls in `adapter/loop.sh`,
      and config-knob *values* legitimately name the current binding. De-name the claims, not the
      mechanism.
    - Preserve the proof floor: the review floor and acceptance tiers stay strong; routing never
      demotes them. The phase-one collaborator that frames a one-way work node must not be the
      review floor that scrutinizes it — the framer is not its own witness.
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
    
    Reversibility: one-way
    
    ## route
    
    TODO — written only after `./direction` records the selected option.
    
    ## acceptance condition
    
    After adoption: the `collaboration`/`loop`/`adapter` contract (intent and machine statements),
    the adapter prose, and `check.sh` express the harness binding in role and config terms with no
    harness product named in any *statement*; a phase-one *collaborator* role and a phase-one
    routing/delegation seam exist with held defaults that reproduce current behavior; the strong
    review floor's independence from the framer is stated; and `./check.sh` is green.
    
    ## observable acceptance
    
    - `./check.sh` exits zero after implementation and after the archive fold.
    - A check asserts that no contract *statement* file (`intent/collaboration.md`,
      `intent/loop.md`, `intent/adapter.md`, and their `machine-statements/` counterparts)
      contains a harness-product token — product names and product-bearing knob identifiers alike
      — outside a fenced materialization-pointer context; the exact token set and pointer
      exception are fixed in the route.
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
    
    ## proof state
    
    Required proof: the observable-acceptance checks above, plus `check.sh` self-tests that a
    product-named contract statement fails the product-absence check, and that the held defaults
    reproduce current routing when the knobs are unset. Baseline `./check.sh` is green before
    implementation (to be confirmed at the start of phase two).
    
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
    
    exec
    /bin/bash -lc "sed -n '1,160p' 011-phase-one-routing/intent/frame/signoff.md" in /home/qqp/projects/hypercore
     exited 2 in 0ms:
    sed: can't read 011-phase-one-routing/intent/frame/signoff.md: No such file or directory
    
    exec
    /bin/bash -lc 'find 011-phase-one-routing/intent/frame -maxdepth 2 -type f | sort' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    011-phase-one-routing/intent/frame/frame.md
    011-phase-one-routing/intent/frame/options.md
    011-phase-one-routing/intent/frame/review.md
    
    codex
    VERDICT: FLAG
    NOTE: `signoff.md` is absent and the frame route is still `TODO`, so this is not a signed, complete frame.
    hook: Stop
    hook: Stop Completed
    tokens used
    10,407

### simplicity-fastness

status: 0
selected-output-source: final-output

#### selected output

    VERDICT: FLAG
    NOTE: The frame is not route-settled or signed: `route` remains TODO and no direction/signoff artifact is present.

#### final output

    VERDICT: FLAG
    NOTE: The frame is not route-settled or signed: `route` remains TODO and no direction/signoff artifact is present.

#### stdout

    VERDICT: FLAG
    NOTE: The frame is not route-settled or signed: `route` remains TODO and no direction/signoff artifact is present.

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
    session id: 019ea47a-4864-7480-a13c-d0785e23ce26
    --------
    user
    Review role: simplicity-fastness
    Work: 011-phase-one-routing
    Frame directory: 011-phase-one-routing/intent/frame
    
    Read only the signed work frame and the intent it references. Do not debate other reviewers.
    Return exactly one structured verdict line:
    VERDICT: PASS
    or
    VERDICT: FLAG
    
    Then optionally add one NOTE: line. Treat uncertainty as FLAG.
    hook: UserPromptSubmit
    hook: UserPromptSubmit Completed
    exec
    /bin/bash -lc 'rg --files 011-phase-one-routing/intent/frame' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    011-phase-one-routing/intent/frame/options.md
    011-phase-one-routing/intent/frame/frame.md
    011-phase-one-routing/intent/frame/review.md
    
    exec
    /bin/bash -lc "sed -n '1,240p' 011-phase-one-routing/intent/frame/frame.md" in /home/qqp/projects/hypercore
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
    - Materialization stays product-specific: the adapter prose (`adapter/codex.md`), the harness
      entry point (`AGENTS.md`), the orchestrator's actual harness calls in `adapter/loop.sh`,
      and config-knob *values* legitimately name the current binding. De-name the claims, not the
      mechanism.
    - Preserve the proof floor: the review floor and acceptance tiers stay strong; routing never
      demotes them. The phase-one collaborator that frames a one-way work node must not be the
      review floor that scrutinizes it — the framer is not its own witness.
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
    
    Reversibility: one-way
    
    ## route
    
    TODO — written only after `./direction` records the selected option.
    
    ## acceptance condition
    
    After adoption: the `collaboration`/`loop`/`adapter` contract (intent and machine statements),
    the adapter prose, and `check.sh` express the harness binding in role and config terms with no
    harness product named in any *statement*; a phase-one *collaborator* role and a phase-one
    routing/delegation seam exist with held defaults that reproduce current behavior; the strong
    review floor's independence from the framer is stated; and `./check.sh` is green.
    
    ## observable acceptance
    
    - `./check.sh` exits zero after implementation and after the archive fold.
    - A check asserts that no contract *statement* file (`intent/collaboration.md`,
      `intent/loop.md`, `intent/adapter.md`, and their `machine-statements/` counterparts)
      contains a harness-product token — product names and product-bearing knob identifiers alike
      — outside a fenced materialization-pointer context; the exact token set and pointer
      exception are fixed in the route.
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
    
    ## proof state
    
    Required proof: the observable-acceptance checks above, plus `check.sh` self-tests that a
    product-named contract statement fails the product-absence check, and that the held defaults
    reproduce current routing when the knobs are unset. Baseline `./check.sh` is green before
    implementation (to be confirmed at the start of phase two).
    
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
    
    exec
    /bin/bash -lc "sed -n '1,240p' 011-phase-one-routing/intent/frame/review.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # review - 011-phase-one-routing
    
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
    
    - contract-checkability (base): The frame is unsigned/incomplete: no signoff or direction artifact exists, and `frame.md` leaves the route as TODO.
    - soundness-fit (base): Option 3 conflicts with the frame's acceptance/adoption condition requiring no harness product token in any contract statement.
    - simplicity-fastness (base): The provided frame is not route-settled: `route` remains TODO, so simplicity-fastness cannot clear it without uncertainty.
    - red-team (base): The frame is not signed and still has `route: TODO`, so the reviewed artifact cannot be treated as a settled signed route.
    
    ## reviewer notes
    
    ### contract-checkability
    
    The frame is unsigned/incomplete: no signoff or direction artifact exists, and `frame.md` leaves the route as TODO.
    
    ### soundness-fit
    
    Option 3 conflicts with the frame's acceptance/adoption condition requiring no harness product token in any contract statement.
    
    ### simplicity-fastness
    
    The provided frame is not route-settled: `route` remains TODO, so simplicity-fastness cannot clear it without uncertainty.
    
    ### red-team
    
    The frame is not signed and still has `route: TODO`, so the reviewed artifact cannot be treated as a settled signed route.
    
    ## reviewer diagnostics
    
    ### contract-checkability
    
    status: 0
    selected-output-source: final-output
    
    #### selected output
    
        VERDICT: FLAG
        NOTE: The frame is unsigned/incomplete: no signoff or direction artifact exists, and `frame.md` leaves the route as TODO.
    
    #### final output
    
        VERDICT: FLAG
        NOTE: The frame is unsigned/incomplete: no signoff or direction artifact exists, and `frame.md` leaves the route as TODO.
    
    #### stdout
    
        VERDICT: FLAG
        NOTE: The frame is unsigned/incomplete: no signoff or direction artifact exists, and `frame.md` leaves the route as TODO.
    
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
        session id: 019ea472-3b2d-7e73-814b-cf5329f75d1a
        --------
        user
        Review role: contract-checkability
        Work: 011-phase-one-routing
        Frame directory: 011-phase-one-routing/intent/frame
        
        Read only the signed work frame and the intent it references. Do not debate other reviewers.
        Return exactly one structured verdict line:
        VERDICT: PASS
        or
        VERDICT: FLAG
        
        Then optionally add one NOTE: line. Treat uncertainty as FLAG.
        hook: UserPromptSubmit
        hook: UserPromptSubmit Completed
        exec
        /bin/bash -lc "sed -n '1,220p' 011-phase-one-routing/intent/frame/frame.md" in /home/qqp/projects/hypercore
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
          or `adapter` names a specific harness product. Role and config-slot vocabulary only.
        - Materialization stays product-specific: the adapter prose (`adapter/codex.md`), the harness
          entry point (`AGENTS.md`), the orchestrator's actual harness calls in `adapter/loop.sh`,
          and config-knob *values* legitimately name the current binding. De-name the claims, not the
          mechanism.
        - Preserve the proof floor: the review floor and acceptance tiers stay strong; routing never
          demotes them. The phase-one collaborator that frames a one-way work node must not be the
          review floor that scrutinizes it — the framer is not its own witness.
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
        a product-agnostic role/config contract that de-names the whole adapter contract. The one
        genuine remaining fork is the de-naming boundary for config-knob *identifiers*, with a
        smaller fallback retained in case review finds the full scope too large to land coherently in
        one node. See `intent/frame/options.md`.
        
        Reversibility: one-way
        
        ## route
        
        TODO — written only after `./direction` records the selected option.
        
        ## acceptance condition
        
        After adoption: the `collaboration`/`loop`/`adapter` contract (intent and machine statements),
        the adapter prose, and `check.sh` express the harness binding in role and config terms with no
        harness product named in any *statement*; a phase-one *collaborator* role and a phase-one
        routing/delegation seam exist with held defaults that reproduce current behavior; the strong
        review floor's independence from the framer is stated; and `./check.sh` is green.
        
        ## observable acceptance
        
        - `./check.sh` exits zero after implementation and after the archive fold.
        - A check asserts that no contract *statement* file (`intent/collaboration.md`,
          `intent/loop.md`, `intent/adapter.md`, and their `machine-statements/` counterparts)
          contains a harness-product token outside a fenced materialization-pointer context; the exact
          token set and pointer exception are fixed in the route.
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
        
        ## proof state
        
        Required proof: the observable-acceptance checks above, plus `check.sh` self-tests that a
        product-named contract statement fails the product-absence check, and that the held defaults
        reproduce current routing when the knobs are unset. Baseline `./check.sh` is green before
        implementation (to be confirmed at the start of phase two).
        
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
        or if the full scope cannot land coherently in one node and the operator does not fall back
        to the smaller option.
        
        exec
        /bin/bash -lc "sed -n '1,120p' 011-phase-one-routing/intent/frame/signoff.md" in /home/qqp/projects/hypercore
    
    exec
    /bin/bash -lc "sed -n '1,240p' 011-phase-one-routing/intent/frame/options.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # options - 011-phase-one-routing
    
    Direction options are drafted by the machine for operator selection. The operator
    selects one route, rejects all options, or aborts without writing direction.
    
    ## option 1
    
    id: contract-only-denaming
    kind: selected-route
    summary: De-name the whole contract (collaboration/loop/adapter statements and machine statements, the adapter prose, and check.sh) to role and config terms; add the phase-one collaborator role and a phase-one routing/delegation seam with held defaults; keep the materialization product-specific, including the existing CODEX_* environment-knob names, which are materialization config rather than contract.
    reversibility: one-way
    tradeoff: Smallest diff to the running mechanism and to operator muscle memory; the contract is fully product-agnostic, but config-knob identifiers still read CODEX_*, a minor residual product name at the materialization edge.
    
    ## option 2
    
    id: contract-and-knob-denaming
    kind: selected-route
    summary: Everything in option 1, plus neutralize the config-knob identifiers themselves (the CODEX_* environment variables become harness-neutral names), keeping the old names as cheap aliases where practical so existing configuration does not break.
    reversibility: one-way
    tradeoff: Fullest product-agnostic surface, down to the environment-variable names; larger blast radius across the loop.sh env interface, check.sh, and any references to the knob names, with alias upkeep to avoid breaking existing CODEX_* configuration.
    
    ## rejection choices
    
    none: Reject all options and send the work back to frame for a different route surface.
    abort: Abort without recording direction.
    
    exec
    /bin/bash -lc "sed -n '1,280p' intent/loop.md" in /home/qqp/projects/hypercore
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
    runs and after recent failure or completion, including the active gate, status, Codex
    thread id, latest message, event history, and run artifact paths.
    before launching the first phase-two Codex gate, `loop.sh execute <work-name>` checks that
    the Codex binary is present and that Codex home/session state is writable; a failed
    preflight records failed run state and stops before `codex exec`.
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
    fresh Codex builder session for each unit, and records lean unit handoff, diff, and
    tier-one verdict artifacts under the work frame.
    `loop.sh execute <work-name>` routes builders through `CODEX_BUILDER_MODEL`, defaulting to
    the strong model until the two-step plan/build work lands, separately from the strong review
    route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
    to `CODEX_STRONG_BUILDER_MODEL`, and stops for the operator when the strong builder fails.
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
    /bin/bash -lc "sed -n '1,300p' intent/machine-statements/loop.md" in /home/qqp/projects/hypercore
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
    runs and after recent failure or completion, including the active gate, status, Codex
    thread id, current unit, latest message, failure reason, event history, run artifact
    paths, and phase-two acceptance artifact paths.
    before launching the first phase-two Codex gate, `loop.sh execute <work-name>` checks that
    the Codex binary is present and that Codex home/session state is writable; a failed
    preflight records failed run state and stops before `codex exec`.
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
    fresh Codex builder session for each unit, and records lean unit handoff, diff, and
    tier-one verdict artifacts under the work frame.
    `loop.sh execute <work-name>` routes builders through `CODEX_BUILDER_MODEL`, defaulting to
    the strong model until the two-step plan/build work lands, separately from the strong review
    route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
    to `CODEX_STRONG_BUILDER_MODEL`, and stops for the operator when the strong builder fails.
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
    the Codex harness loads its adapter through a root `AGENTS.md` symlinked to
    `adapter/codex.md`; the root entry is the harness's mandated pointer, holding nothing, not
    where the adapter lives.
    a machine working in a nested node under the root is bound by Codex including the root
    `AGENTS.md` in the project instruction chain from the project root to the current
    directory, so no node below the root carries its own adapter material.
    a mounted external project may carry a target-local `AGENTS.md` entry point for
    direct-path openings; the entry point links to root-managed adapter material and routes
    back to the root adapter and loop instead of copying root adapter material into the
    mounted node.
    the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
    over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
    builder session from the signed frame, and acceptance reviewers and the archive actor are
    fresh sessions rather than resumes of the builder.
    the Codex loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
    `.hypercore/loop-runs`, with run-local state, event history, raw Codex gate streams, gate
    final outputs, acceptance artifact paths, and current pointers for the addressed work and
    root.
    the Codex loop streams inner `codex exec --json` events into the phase-two run state while
    printing concise progress, without changing the cleared-session contract.
    the Codex loop materializes separate builder and reviewer routing, structured acceptance
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
    the Codex adapter prose describes phase one as design-phase collaboration with direction
    and review artifacts, while preserving phase two as cleared, heads-down execution from the
    signed frame directory and lean phase-two handoff artifacts.
    `check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
    validation, start scaffolding, direction/review helpers, operator-act gating through
    `/dev/tty` with B-ready `operator-gate:` markers and numbered-option direction, review and
    acceptance isolation settings, strict frame parsing, phase-two acceptance gating, structured
    acceptance legibility, acceptance source markers and fake-source rejection, separate
    builder/reviewer routing with bounded retry and strong escalation, resumable execute
    caching, the concurrent tier-two panel, the new operator-act and phase-two performance
    contract in the `collaboration`, `loop`, and `adapter` segments, and current-material
    absence of the retired compatibility route still carry the contract.
    each gate's instructions are held in a file in `adapter/gates/`; the Codex path includes them in
    the `codex exec` gate prompt; the orchestrator owns gate order and preconditions and
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
    /bin/bash -lc "sed -n '1,260p' intent/machine-statements/collaboration.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # collaboration — machine statements
    
    phase-two handoff state is written as common ground for the operator and later tooling:
    the addressed work's current or recent gate, current unit, status, Codex thread id, latest
    message, failure reason, event history, run artifact paths, and phase-two acceptance
    artifact paths are recoverable from loop state files.
    
    exec
    /bin/bash -lc "sed -n '1,260p' intent/collaboration.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # collaboration
    
    operator-machine collaboration is a first-class methodology concern, separate from the loop mechanics that enforce it.
    collaboration is the working relation by which operator and machine keep the work scrutable, sound, and fast across memoryless sessions.
    effective collaboration is complementarity, not maximal automation: the operator sets purpose, constraints, acceptance, and open direction; the machine searches, synthesizes, drafts, executes, checks, and settles only what the intent and operator leave open.
    collaboration keeps common ground recoverable without treating field count as proof of collaboration quality.
    phase one is an arc: understanding before route, scrutiny sized by reversibility, operator direction, lean recoverability, and sign-off.
    before a route is written, the machine gives a teach-back, at least one alternative framing, information-gain questions, and a reversibility classification.
    one-way work requires distinct-route scrutiny before route settlement, including a mechanically spawned base review roster.
    the base review roster is `contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`; optional reviewers are additive and advisory only.
    optional reviewers cannot override, outvote, average away, or dilute unresolved base-roster or red-team flags.
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
    the addressed work's current or recent gate, current unit, status, Codex thread id, latest
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
    direction and review are phase-one acts or artifacts, not loop gates.
    the Codex review roster for one-way phase-one work has a base roster of
    `contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`.
    the Codex implementation-acceptance reviewer for each phase-two unit is independent and
    read-only.
    the Codex tier-two implementation-acceptance panel for one-way work has required lenses
    `whole-acceptance-conformance`, `proof-integrity`, `independent-coherence`,
    `security-permissions`, and `red-team`.
    the complete optional Codex review roster is `implementation-maintainability`,
    `security-permissions`, `operator-ergonomics`, `migration-compatibility`,
    `domain-evidence`, and `performance-cost`.
    optional reviewers are advisory additions and cannot override, outvote, average away, or
    dilute unresolved base-roster or red-team flags.
    the Codex adapter classifies the request surface before changing material: ordinary
    conversation and read-only inspection may proceed directly, while governed work starts or
    continues a work node.
    the Codex adapter rejects perceived simplicity, file count, convenience, and low risk as
    waivers for governed work.
    on request the adapter renders a statement of the intent intelligible in plain language
    without altering it.
    the adapter carries only what the intent cannot yet reach the harness with -- the order to
    read the intent first, and disciplines not yet written as statements; each is a debt,
    folded into the intent by later work and then dropped.
    an adapter is per harness; one node may be bound by more than one, each loaded by its own
    harness.
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
    the Codex harness loads its adapter through a root `AGENTS.md` symlinked to
    `adapter/codex.md`; the root entry is the harness's mandated pointer, holding nothing, not
    where the adapter lives.
    a machine working in a nested node under the root is bound by Codex including the root
    `AGENTS.md` in the project instruction chain from the project root to the current
    directory, so no node below the root carries its own adapter material.
    a mounted external project may carry a target-local `AGENTS.md` entry point for
    direct-path openings; the entry point links to root-managed adapter material and routes
    back to the root adapter and loop instead of copying root adapter material into the
    mounted node.
    the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
    over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
    builder session from the signed frame, and acceptance reviewers and the archive actor are
    fresh sessions rather than resumes of the builder.
    the Codex loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
    `.hypercore/loop-runs`, with run-local state, event history, raw Codex gate streams, gate
    final outputs, acceptance artifact paths, and current pointers for the addressed work and
    root.
    the Codex loop streams inner `codex exec --json` events into the phase-two run state while
    printing concise progress, without changing the cleared-session contract.
    the Codex loop materializes separate builder and reviewer routing, structured acceptance
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
    the Codex adapter prose describes phase one as design-phase collaboration with direction
    and review artifacts, while preserving phase two as cleared, heads-down execution from the
    signed frame directory and lean phase-two handoff artifacts.
    `check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
    validation, start scaffolding, direction/review helpers, operator-act gating through
    `/dev/tty` with B-ready `operator-gate:` markers and numbered-option direction, review and
    acceptance isolation settings, strict frame parsing, phase-two acceptance gating, structured
    acceptance legibility, acceptance source markers and fake-source rejection, separate
    builder/reviewer routing with bounded retry and strong escalation, resumable execute
    caching, the concurrent tier-two panel, the new operator-act and phase-two performance
    contract in the `collaboration`, `loop`, and `adapter` segments, and current-material
    absence of the retired compatibility route still carry the contract.
    each gate's instructions are held in a file in `adapter/gates/`; the Codex path includes them in
    the `codex exec` gate prompt; the orchestrator owns gate order and preconditions and
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
    NOTE: The frame is not route-settled or signed: `route` remains TODO and no direction/signoff artifact is present.
    hook: Stop
    hook: Stop Completed
    tokens used
    18,069

### red-team

status: 0
selected-output-source: final-output

#### selected output

    VERDICT: FLAG
    NOTE: The frame directory has no `direction.md` or `signoff.md`, and `frame.md` still has `route` as TODO, so the artifact is not a signed, settled frame.

#### final output

    VERDICT: FLAG
    NOTE: The frame directory has no `direction.md` or `signoff.md`, and `frame.md` still has `route` as TODO, so the artifact is not a signed, settled frame.

#### stdout

    VERDICT: FLAG
    NOTE: The frame directory has no `direction.md` or `signoff.md`, and `frame.md` still has `route` as TODO, so the artifact is not a signed, settled frame.

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
    session id: 019ea47a-c32b-7962-be4a-c7946dc82410
    --------
    user
    Review role: red-team
    Work: 011-phase-one-routing
    Frame directory: 011-phase-one-routing/intent/frame
    
    Read only the signed work frame and the intent it references. Do not debate other reviewers.
    Return exactly one structured verdict line:
    VERDICT: PASS
    or
    VERDICT: FLAG
    
    Then optionally add one NOTE: line. Treat uncertainty as FLAG.
    hook: UserPromptSubmit
    hook: UserPromptSubmit Completed
    exec
    /bin/bash -lc 'rg --files 011-phase-one-routing/intent/frame' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    011-phase-one-routing/intent/frame/options.md
    011-phase-one-routing/intent/frame/frame.md
    011-phase-one-routing/intent/frame/review.md
    
    exec
    /bin/bash -lc 'rg --files 011-phase-one-routing' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    011-phase-one-routing/intent/frame/options.md
    011-phase-one-routing/intent/frame/frame.md
    011-phase-one-routing/intent/frame/review.md
    011-phase-one-routing/intent/organizing-document.md
    
    exec
    /bin/bash -lc "sed -n '1,240p' 011-phase-one-routing/intent/frame/frame.md" in /home/qqp/projects/hypercore
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
    - Materialization stays product-specific: the adapter prose (`adapter/codex.md`), the harness
      entry point (`AGENTS.md`), the orchestrator's actual harness calls in `adapter/loop.sh`,
      and config-knob *values* legitimately name the current binding. De-name the claims, not the
      mechanism.
    - Preserve the proof floor: the review floor and acceptance tiers stay strong; routing never
      demotes them. The phase-one collaborator that frames a one-way work node must not be the
      review floor that scrutinizes it — the framer is not its own witness.
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
    
    Reversibility: one-way
    
    ## route
    
    TODO — written only after `./direction` records the selected option.
    
    ## acceptance condition
    
    After adoption: the `collaboration`/`loop`/`adapter` contract (intent and machine statements),
    the adapter prose, and `check.sh` express the harness binding in role and config terms with no
    harness product named in any *statement*; a phase-one *collaborator* role and a phase-one
    routing/delegation seam exist with held defaults that reproduce current behavior; the strong
    review floor's independence from the framer is stated; and `./check.sh` is green.
    
    ## observable acceptance
    
    - `./check.sh` exits zero after implementation and after the archive fold.
    - A check asserts that no contract *statement* file (`intent/collaboration.md`,
      `intent/loop.md`, `intent/adapter.md`, and their `machine-statements/` counterparts)
      contains a harness-product token — product names and product-bearing knob identifiers alike
      — outside a fenced materialization-pointer context; the exact token set and pointer
      exception are fixed in the route.
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
    
    ## proof state
    
    Required proof: the observable-acceptance checks above, plus `check.sh` self-tests that a
    product-named contract statement fails the product-absence check, and that the held defaults
    reproduce current routing when the knobs are unset. Baseline `./check.sh` is green before
    implementation (to be confirmed at the start of phase two).
    
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
    
    exec
    /bin/bash -lc "sed -n '1,240p' 011-phase-one-routing/intent/frame/options.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # options - 011-phase-one-routing
    
    Direction options are drafted by the machine for operator selection. The operator
    selects one route, rejects all options, or aborts without writing direction.
    
    ## option 1
    
    id: contract-only-denaming
    kind: selected-route
    summary: De-name the whole contract (collaboration/loop/adapter statements and machine statements, the adapter prose, and check.sh) to role and config terms; add the phase-one collaborator role and a phase-one routing/delegation seam with held defaults; keep the materialization product-specific, including the existing CODEX_* environment-knob names, which are materialization config rather than contract.
    reversibility: one-way
    tradeoff: Smallest diff to the running mechanism and to operator muscle memory; the contract is fully product-agnostic, but config-knob identifiers still read CODEX_*, a minor residual product name at the materialization edge.
    
    ## option 2
    
    id: contract-and-knob-denaming
    kind: selected-route
    summary: Everything in option 1, plus neutralize the config-knob identifiers themselves (the CODEX_* environment variables become harness-neutral names), keeping the old names as cheap aliases where practical so existing configuration does not break.
    reversibility: one-way
    tradeoff: Fullest product-agnostic surface, down to the environment-variable names; larger blast radius across the loop.sh env interface, check.sh, and any references to the knob names, with alias upkeep to avoid breaking existing CODEX_* configuration.
    
    ## rejection choices
    
    none: Reject all options and send the work back to frame for a different route surface.
    abort: Abort without recording direction.
    
    exec
    /bin/bash -lc "sed -n '1,240p' 011-phase-one-routing/intent/frame/review.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # review - 011-phase-one-routing
    
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
    
    - contract-checkability (base): The frame is unsigned/incomplete: no signoff or direction artifact exists, and `frame.md` leaves the route as TODO.
    - soundness-fit (base): Option 3 conflicts with the frame's acceptance/adoption condition requiring no harness product token in any contract statement.
    - simplicity-fastness (base): The provided frame is not route-settled: `route` remains TODO, so simplicity-fastness cannot clear it without uncertainty.
    - red-team (base): The frame is not signed and still has `route: TODO`, so the reviewed artifact cannot be treated as a settled signed route.
    
    ## reviewer notes
    
    ### contract-checkability
    
    The frame is unsigned/incomplete: no signoff or direction artifact exists, and `frame.md` leaves the route as TODO.
    
    ### soundness-fit
    
    Option 3 conflicts with the frame's acceptance/adoption condition requiring no harness product token in any contract statement.
    
    ### simplicity-fastness
    
    The provided frame is not route-settled: `route` remains TODO, so simplicity-fastness cannot clear it without uncertainty.
    
    ### red-team
    
    The frame is not signed and still has `route: TODO`, so the reviewed artifact cannot be treated as a settled signed route.
    
    ## reviewer diagnostics
    
    ### contract-checkability
    
    status: 0
    selected-output-source: final-output
    
    #### selected output
    
        VERDICT: FLAG
        NOTE: The frame is unsigned/incomplete: no signoff or direction artifact exists, and `frame.md` leaves the route as TODO.
    
    #### final output
    
        VERDICT: FLAG
        NOTE: The frame is unsigned/incomplete: no signoff or direction artifact exists, and `frame.md` leaves the route as TODO.
    
    #### stdout
    
        VERDICT: FLAG
        NOTE: The frame is unsigned/incomplete: no signoff or direction artifact exists, and `frame.md` leaves the route as TODO.
    
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
        session id: 019ea472-3b2d-7e73-814b-cf5329f75d1a
        --------
        user
        Review role: contract-checkability
        Work: 011-phase-one-routing
        Frame directory: 011-phase-one-routing/intent/frame
        
        Read only the signed work frame and the intent it references. Do not debate other reviewers.
        Return exactly one structured verdict line:
        VERDICT: PASS
        or
        VERDICT: FLAG
        
        Then optionally add one NOTE: line. Treat uncertainty as FLAG.
        hook: UserPromptSubmit
        hook: UserPromptSubmit Completed
        exec
        /bin/bash -lc "sed -n '1,220p' 011-phase-one-routing/intent/frame/frame.md" in /home/qqp/projects/hypercore
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
          or `adapter` names a specific harness product. Role and config-slot vocabulary only.
        - Materialization stays product-specific: the adapter prose (`adapter/codex.md`), the harness
          entry point (`AGENTS.md`), the orchestrator's actual harness calls in `adapter/loop.sh`,
          and config-knob *values* legitimately name the current binding. De-name the claims, not the
          mechanism.
        - Preserve the proof floor: the review floor and acceptance tiers stay strong; routing never
          demotes them. The phase-one collaborator that frames a one-way work node must not be the
          review floor that scrutinizes it — the framer is not its own witness.
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
        a product-agnostic role/config contract that de-names the whole adapter contract. The one
        genuine remaining fork is the de-naming boundary for config-knob *identifiers*, with a
        smaller fallback retained in case review finds the full scope too large to land coherently in
        one node. See `intent/frame/options.md`.
        
        Reversibility: one-way
        
        ## route
        
        TODO — written only after `./direction` records the selected option.
        
        ## acceptance condition
        
        After adoption: the `collaboration`/`loop`/`adapter` contract (intent and machine statements),
        the adapter prose, and `check.sh` express the harness binding in role and config terms with no
        harness product named in any *statement*; a phase-one *collaborator* role and a phase-one
        routing/delegation seam exist with held defaults that reproduce current behavior; the strong
        review floor's independence from the framer is stated; and `./check.sh` is green.
        
        ## observable acceptance
        
        - `./check.sh` exits zero after implementation and after the archive fold.
        - A check asserts that no contract *statement* file (`intent/collaboration.md`,
          `intent/loop.md`, `intent/adapter.md`, and their `machine-statements/` counterparts)
          contains a harness-product token outside a fenced materialization-pointer context; the exact
          token set and pointer exception are fixed in the route.
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
        
        ## proof state
        
        Required proof: the observable-acceptance checks above, plus `check.sh` self-tests that a
        product-named contract statement fails the product-absence check, and that the held defaults
        reproduce current routing when the knobs are unset. Baseline `./check.sh` is green before
        implementation (to be confirmed at the start of phase two).
        
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
        or if the full scope cannot land coherently in one node and the operator does not fall back
        to the smaller option.
        
        exec
        /bin/bash -lc "sed -n '1,120p' 011-phase-one-routing/intent/frame/signoff.md" in /home/qqp/projects/hypercore
    
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
    runs and after recent failure or completion, including the active gate, status, Codex
    thread id, latest message, event history, and run artifact paths.
    before launching the first phase-two Codex gate, `loop.sh execute <work-name>` checks that
    the Codex binary is present and that Codex home/session state is writable; a failed
    preflight records failed run state and stops before `codex exec`.
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
    fresh Codex builder session for each unit, and records lean unit handoff, diff, and
    tier-one verdict artifacts under the work frame.
    `loop.sh execute <work-name>` routes builders through `CODEX_BUILDER_MODEL`, defaulting to
    the strong model until the two-step plan/build work lands, separately from the strong review
    route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
    to `CODEX_STRONG_BUILDER_MODEL`, and stops for the operator when the strong builder fails.
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
    /bin/bash -lc "sed -n '1,260p' intent/machine-statements/loop.md" in /home/qqp/projects/hypercore
    exec
    /bin/bash -lc "sed -n '1,240p' intent/collaboration.md" in /home/qqp/projects/hypercore
    exec
    /bin/bash -lc "sed -n '1,240p' intent/machine-statements/collaboration.md" in /home/qqp/projects/hypercore
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
    runs and after recent failure or completion, including the active gate, status, Codex
    thread id, current unit, latest message, failure reason, event history, run artifact
    paths, and phase-two acceptance artifact paths.
    before launching the first phase-two Codex gate, `loop.sh execute <work-name>` checks that
    the Codex binary is present and that Codex home/session state is writable; a failed
    preflight records failed run state and stops before `codex exec`.
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
    fresh Codex builder session for each unit, and records lean unit handoff, diff, and
    tier-one verdict artifacts under the work frame.
    `loop.sh execute <work-name>` routes builders through `CODEX_BUILDER_MODEL`, defaulting to
    the strong model until the two-step plan/build work lands, separately from the strong review
    route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
    to `CODEX_STRONG_BUILDER_MODEL`, and stops for the operator when the strong builder fails.
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
    
     succeeded in 0ms:
    # collaboration
    
    operator-machine collaboration is a first-class methodology concern, separate from the loop mechanics that enforce it.
    collaboration is the working relation by which operator and machine keep the work scrutable, sound, and fast across memoryless sessions.
    effective collaboration is complementarity, not maximal automation: the operator sets purpose, constraints, acceptance, and open direction; the machine searches, synthesizes, drafts, executes, checks, and settles only what the intent and operator leave open.
    collaboration keeps common ground recoverable without treating field count as proof of collaboration quality.
    phase one is an arc: understanding before route, scrutiny sized by reversibility, operator direction, lean recoverability, and sign-off.
    before a route is written, the machine gives a teach-back, at least one alternative framing, information-gain questions, and a reversibility classification.
    one-way work requires distinct-route scrutiny before route settlement, including a mechanically spawned base review roster.
    the base review roster is `contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`; optional reviewers are additive and advisory only.
    optional reviewers cannot override, outvote, average away, or dilute unresolved base-roster or red-team flags.
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
    the addressed work's current or recent gate, current unit, status, Codex thread id, latest
    message, failure reason, event history, run artifact paths, and phase-two acceptance
    artifact paths are recoverable from loop state files.
    
    ---
    endorsed by qqp-dev
    
     succeeded in 0ms:
    # collaboration — machine statements
    
    phase-two handoff state is written as common ground for the operator and later tooling:
    the addressed work's current or recent gate, current unit, status, Codex thread id, latest
    message, failure reason, event history, run artifact paths, and phase-two acceptance
    artifact paths are recoverable from loop state files.
    
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
    direction and review are phase-one acts or artifacts, not loop gates.
    the Codex review roster for one-way phase-one work has a base roster of
    `contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`.
    the Codex implementation-acceptance reviewer for each phase-two unit is independent and
    read-only.
    the Codex tier-two implementation-acceptance panel for one-way work has required lenses
    `whole-acceptance-conformance`, `proof-integrity`, `independent-coherence`,
    `security-permissions`, and `red-team`.
    the complete optional Codex review roster is `implementation-maintainability`,
    `security-permissions`, `operator-ergonomics`, `migration-compatibility`,
    `domain-evidence`, and `performance-cost`.
    optional reviewers are advisory additions and cannot override, outvote, average away, or
    dilute unresolved base-roster or red-team flags.
    the Codex adapter classifies the request surface before changing material: ordinary
    conversation and read-only inspection may proceed directly, while governed work starts or
    continues a work node.
    the Codex adapter rejects perceived simplicity, file count, convenience, and low risk as
    waivers for governed work.
    on request the adapter renders a statement of the intent intelligible in plain language
    without altering it.
    the adapter carries only what the intent cannot yet reach the harness with -- the order to
    read the intent first, and disciplines not yet written as statements; each is a debt,
    folded into the intent by later work and then dropped.
    an adapter is per harness; one node may be bound by more than one, each loaded by its own
    harness.
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
    the Codex harness loads its adapter through a root `AGENTS.md` symlinked to
    `adapter/codex.md`; the root entry is the harness's mandated pointer, holding nothing, not
    where the adapter lives.
    a machine working in a nested node under the root is bound by Codex including the root
    `AGENTS.md` in the project instruction chain from the project root to the current
    directory, so no node below the root carries its own adapter material.
    a mounted external project may carry a target-local `AGENTS.md` entry point for
    direct-path openings; the entry point links to root-managed adapter material and routes
    back to the root adapter and loop instead of copying root adapter material into the
    mounted node.
    the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
    over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
    builder session from the signed frame, and acceptance reviewers and the archive actor are
    fresh sessions rather than resumes of the builder.
    the Codex loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
    `.hypercore/loop-runs`, with run-local state, event history, raw Codex gate streams, gate
    final outputs, acceptance artifact paths, and current pointers for the addressed work and
    root.
    the Codex loop streams inner `codex exec --json` events into the phase-two run state while
    printing concise progress, without changing the cleared-session contract.
    the Codex loop materializes separate builder and reviewer routing, structured acceptance
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
    the Codex adapter prose describes phase one as design-phase collaboration with direction
    and review artifacts, while preserving phase two as cleared, heads-down execution from the
    signed frame directory and lean phase-two handoff artifacts.
    `check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
    validation, start scaffolding, direction/review helpers, operator-act gating through
    `/dev/tty` with B-ready `operator-gate:` markers and numbered-option direction, review and
    acceptance isolation settings, strict frame parsing, phase-two acceptance gating, structured
    acceptance legibility, acceptance source markers and fake-source rejection, separate
    builder/reviewer routing with bounded retry and strong escalation, resumable execute
    caching, the concurrent tier-two panel, the new operator-act and phase-two performance
    contract in the `collaboration`, `loop`, and `adapter` segments, and current-material
    absence of the retired compatibility route still carry the contract.
    each gate's instructions are held in a file in `adapter/gates/`; the Codex path includes them in
    the `codex exec` gate prompt; the orchestrator owns gate order and preconditions and
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
    /bin/bash -lc "sed -n '1,260p' intent/machine-statements/adapter.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # adapter -- machine statements
    
    the current root harness adapter is materialized as `adapter/codex.md`.
    the Codex harness loads its adapter through a root `AGENTS.md` symlinked to
    `adapter/codex.md`; the root entry is the harness's mandated pointer, holding nothing, not
    where the adapter lives.
    a machine working in a nested node under the root is bound by Codex including the root
    `AGENTS.md` in the project instruction chain from the project root to the current
    directory, so no node below the root carries its own adapter material.
    a mounted external project may carry a target-local `AGENTS.md` entry point for
    direct-path openings; the entry point links to root-managed adapter material and routes
    back to the root adapter and loop instead of copying root adapter material into the
    mounted node.
    the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
    over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
    builder session from the signed frame, and acceptance reviewers and the archive actor are
    fresh sessions rather than resumes of the builder.
    the Codex loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
    `.hypercore/loop-runs`, with run-local state, event history, raw Codex gate streams, gate
    final outputs, acceptance artifact paths, and current pointers for the addressed work and
    root.
    the Codex loop streams inner `codex exec --json` events into the phase-two run state while
    printing concise progress, without changing the cleared-session contract.
    the Codex loop materializes separate builder and reviewer routing, structured acceptance
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
    the Codex adapter prose describes phase one as design-phase collaboration with direction
    and review artifacts, while preserving phase two as cleared, heads-down execution from the
    signed frame directory and lean phase-two handoff artifacts.
    `check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
    validation, start scaffolding, direction/review helpers, operator-act gating through
    `/dev/tty` with B-ready `operator-gate:` markers and numbered-option direction, review and
    acceptance isolation settings, strict frame parsing, phase-two acceptance gating, structured
    acceptance legibility, acceptance source markers and fake-source rejection, separate
    builder/reviewer routing with bounded retry and strong escalation, resumable execute
    caching, the concurrent tier-two panel, the new operator-act and phase-two performance
    contract in the `collaboration`, `loop`, and `adapter` segments, and current-material
    absence of the retired compatibility route still carry the contract.
    each gate's instructions are held in a file in `adapter/gates/`; the Codex path includes them in
    the `codex exec` gate prompt; the orchestrator owns gate order and preconditions and
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
    NOTE: The frame directory has no `direction.md` or `signoff.md`, and `frame.md` still has `route` as TODO, so the artifact is not a signed, settled frame.
    hook: Stop
    hook: Stop Completed
    tokens used
    21,797

