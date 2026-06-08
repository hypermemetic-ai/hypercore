# review - 012-self-applied-phase-two

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

- contract-checkability (base): `signoff.md` is absent from the frame directory, so I cannot verify the signed-frame precondition.
- soundness-fit (base): `intent/frame/signoff.md` is absent, so the signed-frame premise cannot be verified.
- simplicity-fastness (base): `signoff.md` is absent, so the signed-frame premise is not verifiable.
- red-team (base): `signoff.md` is absent, so the signed-frame premise is not verifiable.

## reviewer notes

### contract-checkability

`signoff.md` is absent from the frame directory, so I cannot verify the signed-frame precondition.

### soundness-fit

`intent/frame/signoff.md` is absent, so the signed-frame premise cannot be verified.

### simplicity-fastness

`signoff.md` is absent, so the signed-frame premise is not verifiable.

### red-team

`signoff.md` is absent, so the signed-frame premise is not verifiable.

## reviewer diagnostics

### contract-checkability

status: 0
selected-output-source: final-output

#### selected output

    VERDICT: FLAG
    NOTE: `signoff.md` is absent from the frame directory, so I cannot verify the signed-frame precondition.

#### final output

    VERDICT: FLAG
    NOTE: `signoff.md` is absent from the frame directory, so I cannot verify the signed-frame precondition.

#### stdout

    VERDICT: FLAG
    NOTE: `signoff.md` is absent from the frame directory, so I cannot verify the signed-frame precondition.

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
    session id: 019ea52f-fa3b-7212-941b-773349c9baea
    --------
    user
    Review role: contract-checkability
    Work: 012-self-applied-phase-two
    Frame directory: 012-self-applied-phase-two/intent/frame
    
    Read only the signed work frame and the intent it references. Do not debate other reviewers.
    Return exactly one structured verdict line:
    VERDICT: PASS
    or
    VERDICT: FLAG
    
    Then optionally add one NOTE: line. Treat uncertainty as FLAG.
    hook: UserPromptSubmit
    hook: UserPromptSubmit Completed
    exec
    /bin/bash -lc 'find 012-self-applied-phase-two/intent/frame -maxdepth 2 -type f | sort' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    012-self-applied-phase-two/intent/frame/direction.md
    012-self-applied-phase-two/intent/frame/frame.md
    012-self-applied-phase-two/intent/frame/options.md
    012-self-applied-phase-two/intent/frame/review.md
    
    exec
    /bin/bash -lc "sed -n '1,240p' 012-self-applied-phase-two/intent/frame/frame.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # frame - 012-self-applied-phase-two
    
    ## work
    
    Addressed node: . (the methodology root)
    
    Node-local work name: 012-self-applied-phase-two
    
    Target segments: loop, adapter, active-work
    
    Work in flight: none active. Related ephemeral findings queued but not started:
    `WORK-NODE-COLLAPSE-FINDINGS.md` (work-node taxonomy + the `intent/frame/` folder + the
    intent-vs-material split) — this node defers the deep fold/intent-vs-material question to that
    loop; `TWO-STEP-BUILD-FINDINGS.md` (builder routing — held at gpt-5.5, no conflict);
    `DECOMPOSITION-FINDINGS.md` (seed-units). This node touches the `loop`/`adapter` execute,
    cache, gate-prompt, and handoff statements, plus a bounded `active-work` clarification (the
    in-flight-vs-adopted distinction the gate reconciliation requires), so no live collision (none
    in flight; first to adopt wins).
    
    ## problem
    
    Phase two cannot complete autonomously on hypercore's own methodology self-changes. Every
    self-change to date (008-011) was archived by hand. Four distinct causes:
    
    1. **The resumable cache step is fatal when it should be soft.** After a unit builds and
       passes tier-one, `loop.sh` records a cache entry by calling `phase_two_write_cache_record`
       inside `$(...)` under `set -euo pipefail`; that function `die`s on any missing or unclean
       evidence. Any transient there aborts the whole run before the remaining units and the
       tier-two panel. This is what halted the 011 run (post-hoc every artifact checks clean — the
       signature of a transient). The cache is a resumability optimization; its failure must never
       halt phase two or change a correctness outcome.
    
    2. **The implement gate contradicts the loop's own vertical-slice rule.** `loop.md` says
       "units are vertical slices, so statements, material, and checks land together when the work
       requires all three," but the implement gate prompt says "Do not edit the intent documents."
       For a self-change whose proof is a check over the intent statements themselves (e.g.
       `check.sh` scanning intent), the unit cannot leave `check.sh` green without editing intent
       during implement — which the gate forbids. In 011 the builder had to violate the gate to
       make progress. The contract argues with itself.
    
    3. **A self-modifying unit can edit `loop.sh` while `loop.sh` is the running orchestrator.**
       Editing the bash script a live process is reading is a latent corruption hazard. It has
       never been exercised (every self-change halted earlier or ran by hand), but autonomous
       self-change requires units that edit `loop.sh`, so the goal cannot be reached while the
       orchestrator runs from a file its own units rewrite.
    
    4. **The handoff is not real.** There is no smooth path for Opus to launch a gpt-5.5 codex
       orchestrator after sign-off, and `execute` requires a work name with no way to resolve the
       single signed, unarchived node; "start" (new work) is easy to confuse with "execute"
       (phase two).
    
    5. **Root cause — orchestrator gate prompts are frozen inline at launch (discovered during the
       first execute attempt).** The implement and archive contract prompts live as inline strings
       in `loop.sh` (the implement prompt in `run_unit_build_attempt`, the archive prompt in
       `cmd_execute`), which bash parses into memory when the orchestrator launches; gate-prompt
       *files* under `adapter/gates/*.md` are re-read per invocation via `cat`, but the inline copies
       are not. So a loop-self-change that rewrites these prompts cannot self-apply mid-run — the
       running orchestrator keeps the old prompts regardless of what its units write. This is the
       bootstrap floor under every manual archive (008-011). Moving the contract prompts out of the
       inline strings into the re-read gate files removes the floor so future loop-self-changes need
       no inline bootstrap. (Scope expansion, operator-directed after the first run surfaced it.)
    
    The deeper question of what archive "folds" — which frame parts are intent vs material, and
    whether a work node stages its own proposed intent — is **out of scope**: it is the
    load-bearing open question of `WORK-NODE-COLLAPSE-FINDINGS.md` and is deferred to that loop.
    This node removes the self-contradiction (cause 2) and makes the one `active-work` clarification
    that removal requires, without settling the intent-vs-material split or any staging mechanism.
    
    ## constraints
    
    - Preserve the cleared-session, memoryless re-derivation contract: phase two re-derives each
      unit and acceptance review from the signed frame directory plus lean handoff artifacts.
    - The cache is an optimization: a cache failure degrades to a rebuild, never a halt, and never
      changes a correctness outcome.
    - Keep every correctness gate fatal: `check.sh` red, an unresolved required `FLAG`, a failed
      build, fake/dry-run acceptance for real archive — all still stop phase two. Only the cache
      optimization softens.
    - The `active-work` change is bounded to the in-flight-vs-adopted-current clarification the
      gate reconciliation requires. Do not settle the deep intent-vs-material / fold-staging
      question; that defers to the work-node-collapse loop.
    - Keep the strong review floor and the tier-one + one-way tier-two panel intact and
      independent.
    - The nested codex subprocess is the base function. Cross-session visibility between the
      nested sessions is out of scope.
    - Builder stays held at gpt-5.5 (this is not the two-step plan/build work).
    
    ## decision surface or open direction
    
    Direction selected `include-orchestrator-safety` (tty-gated). After the first execute attempt
    surfaced cause 5 (frozen-inline gate prompts), the operator directed an in-scope expansion:
    relocate the inline implement/archive prompts into the re-read gate files so the orchestrator-
    safety route also removes the bootstrap floor, not just the corruption hazard. Because this
    materially changes what is built, the prior sign-off is superseded and the expanded frame is
    re-signed before phase two. Settled in collaboration: Opus launches and supervises the
    orchestrator (gpt-5.5 orchestrates and builds); the implement-gate self-contradiction is removed
    with the bounded `active-work` clarification; deep fold semantics defer.
    
    Reversibility: one-way
    
    ## route
    
    Ship the operator's selected route, `include-orchestrator-safety`, expanded to fix the root
    cause. Cache soft-fail; the implement-gate/archive reconciliation with the `active-work`
    clarification it requires, **plus relocating the inline implement/archive contract prompts out
    of `loop.sh` into the re-read gate files** so loop-self-changes self-apply with no inline
    bootstrap; the Opus->codex launch + supervise handoff with `execute` auto-detect and
    `start`/`execute` disambiguation; and orchestrator self-edit safety via a snapshot. Each fix
    lands as a vertical slice — `loop.sh`/`check.sh`/gate prompt and the matching `loop`/`adapter`/
    `active-work` intent and machine statements together — leaving `./check.sh` green at every unit
    boundary. The deep fold / intent-vs-material / staging semantics are not touched; they defer to
    the work-node-collapse loop.
    
    **Unit order and the one last bootstrap.** Snapshot self-edit safety lands first so no unit
    edits `loop.sh` before the safety exists in the contract. Because 012 itself rewrites the
    orchestrator's frozen-inline gate prompts, its own run cannot self-apply them (cause 5) — so it
    needs **one last** hand-bootstrap: before launch, Opus pre-applies the implement/archive prompt
    reconciliation to both the inline strings and the gate files, so the launched orchestrator runs
    reconciled (implement permits the unit's required root-intent edits; archive ratifies). The
    codex builders then build all units — editing tracked root intent the diff record can see — and
    unit-002 relocates the inline prompts into the gate files. After 012 adopts, the inline prompts
    are gone, so every future loop-self-change self-applies with no bootstrap at all. 012's own run
    is self-edit-safe regardless because `loop.sh` is fully parsed before `cmd_execute` runs.
    
    Implementation units for phase two:
    
    1. Add orchestrator self-edit safety. Make `adapter/loop.sh` run phase two from an immutable
       snapshot of itself (re-exec from a copy at execute start) so a unit that edits `loop.sh`
       mid-run cannot corrupt the live orchestrator. Record it in the `loop` and `adapter` intent
       and machine statements, and add a self-test proving a mid-run `loop.sh` edit does not corrupt
       the active run. `./check.sh` is green at the unit boundary. (First so no later unit edits
       `loop.sh` before the safety exists; 012's own bootstrap run is launched from a manual
       snapshot by the supervisor.)
    2. Relocate the inline gate prompts into the re-read gate files, reconcile them, and make the
       bounded `active-work` clarification. Move the contract-bearing implement and archive prompt
       text out of the inline strings in `adapter/loop.sh` (`run_unit_build_attempt`, `cmd_execute`)
       into `adapter/gates/implement.md` and `adapter/gates/archive.md`, which `run_gate` re-reads per
       invocation via `cat`, leaving only dynamic per-unit data (unit id, proof obligation, decision
       line) inline — so a loop-self-change's prompt edits take effect mid-run and the inline
       bootstrap floor is gone. Reconcile while moving: the implement gate permits a unit to edit
       intent when the unit's own proof is a check over that intent (removing the blanket "do not edit
       the intent documents" prohibition that contradicts `intent/loop.md`'s vertical-slice
       statement); the archive gate adopts — verifies the applied delta against the signed frame,
       stamps each touched segment foot, and records history — rather than requiring a separate
       content-fold of intent the units already applied. Clarify in `intent/active-work.md` that
       intent a signed work node applies in place during phase two is in-flight, not adopted;
       adoption is the act that stamps the operator's endorsement and records history, making the
       change adopted-current, and "the parent intent remains current until adoption" governs adopted
       truth, consistent with the loop's existing in-flight-vs-adopted concurrency reading. Update the
       `loop` and `adapter` intent and machine statements to match, and add `check.sh` assertions
       encoding (a) the reconciled contract and (b) that no contract-bearing implement/archive prompt
       remains frozen inline in `loop.sh` — so neither the self-contradiction nor the inline floor can
       silently return. `./check.sh` is green at the unit boundary.
    3. Make the resumable cache non-fatal. In `adapter/loop.sh`, a failure at the per-unit
       cache-record step logs and degrades to a soft miss (the unit rebuilds next run); it never
       aborts phase two and never changes a correctness outcome. Record the non-fatality in the
       `loop` and `adapter` intent and machine statements, and add a `check.sh` self-test proving a
       poisoned or failing cache-record step yields a soft miss and the run proceeds (no fatal
       exit), through the existing dry-run / fake-dir self-test surface. `./check.sh` is green at the
       unit boundary.
    4. Make the handoff real. `loop.sh execute` resolves the single signed, unarchived work node in
       the addressed node when `<work-name>` is omitted (and blocks with a clear message when zero or
       more than one exist). Add the Opus->codex launch + supervise path and the `start`-versus-
       `execute` distinction to `adapter/codex.md` and the `adapter` intent and machine statements,
       and add a `check.sh` self-test for the auto-detect resolution. `./check.sh` is green at the
       unit boundary.
    
    ## acceptance condition
    
    After sign-off, Opus launches a fresh gpt-5.5 codex orchestrator session that nests its own
    codex builder/reviewer/archive sub-sessions, and a signed self-modifying work node runs from
    `execute` through adoption with Opus supervising and intervening only on a genuine stuck
    state: every unit builds, `check.sh` is green at each boundary, tier-one and the one-way
    tier-two panel are clean and real-source, archive adopts and records history. A cache-step
    failure produces a rebuild, not a halt. A self-modifying unit cannot corrupt the orchestrator,
    and a unit whose proof is a check over intent may edit that intent without violating the
    contract or the `active-work` "current until adoption" guarantee.
    
    ## observable acceptance
    
    - `./check.sh` is green after the change.
    - A self-test demonstrates that a poisoned/failing cache-record step yields a soft miss and
      the run proceeds (no fatal exit), through the existing dry-run / fake-dir self-test surface.
    - A `check.sh` assertion encodes that the implement gate permits intent edits a unit's own
      proof requires, that archive adopts (verifies the applied delta against the signed frame,
      stamps, records), and that `active-work` distinguishes in-flight from adopted-current — so the
      implement/archive self-contradiction cannot silently return and the gates do not contradict
      `active-work`.
    - A `check.sh` assertion confirms no contract-bearing implement/archive prompt remains frozen
      inline in `adapter/loop.sh` (the contract text lives in the re-read `adapter/gates/*.md`
      files), and a self-test demonstrates that a mid-run change to a gate-prompt file takes effect
      on the next gate invocation in the same run — proving the inline bootstrap floor is removed.
    - A self-test demonstrates a unit editing `loop.sh` mid-run cannot corrupt the active
      orchestrator (the orchestrator runs from a snapshot).
    - `loop.sh execute` resolves the single signed, unarchived work node when `<work-name>` is
      omitted, provable by a self-test; adapter prose names the Opus->codex launch + supervise path
      and distinguishes `start` (new work) from `execute` (phase two).
    
    ## excluded interpretation
    
    - Not settling what archive folds, nor the intent-vs-material split, nor work-node staging —
      those are the work-node-collapse loop's. The `active-work` change here is only the in-flight-
      vs-adopted-current clarification the gate reconciliation requires.
    - Not making the nested codex sessions visible to each other (no shared context or
      cross-session observability) — that is a later loop.
    - Not the two-step strong-plan / cheap-build work; the builder stays gpt-5.5.
    - Not weakening any correctness gate; only the cache optimization becomes non-fatal.
    - Not changing who endorses or the operator-act `/dev/tty` gates.
    
    ## proof state
    
    The five causes are read from current material: cause 1 from `adapter/loop.sh`
    (`phase_two_write_cache_record`, the `$(...)` capture under `set -euo pipefail`); cause 2 from
    `intent/loop.md` ("vertical slices") vs `adapter/gates/implement.md` ("do not edit the intent
    documents"); cause 3 from the orchestrator running `adapter/loop.sh` as a live process while
    units may edit it; cause 4 from `cmd_execute` requiring `<work-name>` and the absence of a
    launch path; cause 5 from `run_gate` (`sys="$(cat "$GATES/$instruction_gate.md")"` re-reads gate
    files per invocation, while the inline implement/archive prompts in `run_unit_build_attempt` and
    `cmd_execute` are frozen at launch) — confirmed empirically when the first execute attempt wedged
    on unit-001. The 011 manual archive
    (`intent/history/adopted/011-phase-one-routing/intent/frame/manual-archive.md`) records the
    empirical halt and the de-naming workaround. Proof of the fix is `./check.sh` green plus the
    new self-tests named in observable acceptance.
    
    ## sweep
    
    Concepts touched and where they appear:
    
    - **resumable cache / execute** — `intent/loop.md`, `intent/machine-statements/loop.md`,
      `intent/machine-statements/adapter.md` ("a resumable per-unit execute cache"),
      `adapter/loop.sh`, `check.sh`. The soft-fail change keeps these statements true (resumable)
      and adds non-fatality; no statement is contradicted.
    - **implement / archive gates / adoption** — `intent/loop.md` (the vertical-slice and archive
      statements), `intent/active-work.md` (amendments not current until adoption; adoption folds
      and records), `intent/endorsement.md` (sign-off stamps each touched segment),
      `adapter/gates/implement.md`, `adapter/gates/archive.md`,
      `intent/machine-statements/adapter.md` (gate-prompt assertions), `check.sh`. Removing the "do
      not edit intent" prohibition aligns the implement gate with the loop's vertical-slice
      statement; archive's adopt-verify-stamp-record keeps `endorsement` true (archive still
      stamps); `active-work` is clarified (not contradicted) so its "current until adoption" reads
      as adopted-current. The deep fold semantics (intent-vs-material split, staging) stay deferred.
    
    exec
    /bin/bash -lc "sed -n '1,120p' 012-self-applied-phase-two/intent/frame/signoff.md" in /home/qqp/projects/hypercore
     exited 2 in 0ms:
    sed: can't read 012-self-applied-phase-two/intent/frame/signoff.md: No such file or directory
    
    codex
    I’m checking the frame artifacts first and keeping this scoped to the frame plus referenced intent. The frame directory does not contain `signoff.md`, so I’m treating that as a contract risk while I verify the referenced segments.
    exec
    /bin/bash -lc "sed -n '241,520p' 012-self-applied-phase-two/intent/frame/frame.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    - **orchestrator / nested sessions / handoff** — `intent/adapter.md` (fresh per-unit builder
      and reviewer sessions), `adapter/codex.md`, `adapter/loop.sh`. The handoff change adds the
      Opus->codex launch + supervise path, `execute` auto-detect, and kickoff prose; the
      nested-subprocess model is already current truth, not new. The snapshot change adds
      orchestrator self-edit safety.
    - **vertical slice** — `intent/loop.md`. The contradiction with the implement gate prompt is
      the bug this node fixes; the resolution makes them consistent.
    
    No contradiction with parent truth is introduced; the work removes an existing internal
    contradiction, clarifies the in-flight-vs-adopted boundary the removal requires, hardens the
    orchestrator, and makes the handoff real.
    
    ## review flags answered
    
    Two review rounds ran on the four-fix frame (one-way base roster, gpt-5.5, xhigh, read-only);
    round one returned four FLAGs, round two cleared both discriminating flags. The frame was then
    expanded (cause 5 / inline-prompt relocation) on operator direction, superseding the prior
    sign-off, so a **third review round runs on the expanded frame** and is answered alongside the
    round-two dispositions below.
    
    - **simplicity-fastness — PASS (round two).** The round-one ordering hazard (a `loop.sh` edit
      before snapshot safety) was answered by making orchestrator self-edit safety unit 1.
    - **soundness-fit — `active-work` conflict resolved; only `signoff.md`-absent remains.** Adding
      `active-work` to target segments with the bounded in-flight-vs-adopted-current clarification in
      unit 2 removed the contradiction the round-one reviewer found. The residual flag is the
      prompt debt below.
    - **`signoff.md` absent (contract-checkability, soundness-fit, red-team):** the known phase-one
      review-prompt debt. The reviewer prompt assumes a signed frame, but review is a phase-one act
      that precedes sign-off, so `signoff.md` cannot exist yet. Non-discriminating and unfixable
      before sign-off; carried as a debt in `adapter/codex.md`. Not a frame defect.
    - **contract-checkability — "frame lacks the adoption-or-shelving claim field":** contradicted
      by the mechanical proof floor. `loop.sh status` reports `frame_complete=yes`, and the frame
      carries both `## adoption claim` and `## shelving claim`. For a mechanical-field fact the
      checker is authoritative; this is a reviewer error anchored on the `signoff.md` confusion.
    - **red-team — autonomy depends on a manual snapshot bootstrap, so the premise is "not
      verifiable":** the autonomous-from-execute property is proven mechanically by the self-tests
      in observable acceptance (cache soft-miss continues; a mid-run `loop.sh` edit cannot corrupt
      the snapshot-run orchestrator; auto-detect resolves the signed node) and by units 2-4 running
      under the installed snapshot and reconciled gate. It does not rest on the bootstrap. 012's own
      unit-001 is the one acknowledged manual bootstrap — the snapshot cannot protect the run that
      installs it — and every self-change after 012 runs hands-off from execute. The premise is
      therefore verifiable on any post-installation run, which is the general case the contract
      governs.
    
    ## adoption claim
    
    Adopt into the root: fold the cache-non-fatality, the implement-gate/archive reconciliation,
    the relocation of inline gate prompts into the re-read gate files, the bounded `active-work`
    in-flight-vs-adopted clarification, the orchestrator self-edit safety, and the handoff
    auto-detect + Opus-launch + kickoff statements into `intent/loop.md`,
    `intent/machine-statements/loop.md`, `intent/adapter.md`, `intent/machine-statements/adapter.md`,
    and `intent/active-work.md`; update `adapter/loop.sh`, `adapter/gates/implement.md`,
    `adapter/gates/archive.md`, `adapter/codex.md`, and `check.sh` to match; stamp each touched
    segment foot with the signed-off operator.
    
    ## shelving claim
    
    Shelve if the selected route proves unsound under review or acceptance (e.g. the implement
    gate reconciliation cannot be encoded as a discriminating check, or the orchestrator-safety
    change destabilizes the run); record the reason and leave parent intent unchanged.
    
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
    /bin/bash -lc "sed -n '1,260p' intent/active-work.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # active-work
    
    active work is a child node with the same reserved tree as any other node: `intent/`, plus
    whatever node-local material its work needs beside that reserved tree.
    active work is bounded by the parent intent statements whose reach includes it.
    a work node may propose parent intent or parent material amendments without making those
    amendments current.
    until adoption accepts an amendment, the parent intent remains current.
    adoption folds accepted child statements and material into the parent and records the work
    node as history.
    shelving records the work node as history without making its proposed amendments parent
    truth.
    a work node may be temporary, durable, adopted, shelved, abandoned, or indefinitely active.
    purpose, rationale, proof state, route, sign-off, and adoption claims are recoverable as
    intent or material within the work node; they are not universal required filenames.
    the loop may require recoverable frame fields before sign-off; that is a frame
    completeness contract, not a universal filename shape.
    root-directed active work lives directly under the root as `<NNN-slug>/`, as a sibling to
    `home`, not under `home`.
    the root active-work contract spans root child work nodes and grants them the general
    ability to parent their own child work nodes unless their own contract narrows that
    freedom.
    
    ## machine
    a sibling set of node-local work nodes is named with `NNN-slug` folders, with the ordinal
    scoped to that sibling set.
    new active work nodes live directly under the addressed node.
    a new work node's frame lives under that work node's `intent/frame/`.
    adopted work-node history is recorded under `intent/history/adopted/`.
    shelved work-node history is recorded under `intent/history/shelved/`.
    empty work-node history collections carry `.gitkeep` so the repository holds the collection
    even when no retained record exists inside it.
    
    ---
    endorsed by qqp-dev
    
    codex
    VERDICT: FLAG
    NOTE: `signoff.md` is absent from the frame directory, so I cannot verify the signed-frame precondition.
    hook: Stop
    hook: Stop Completed
    tokens used
    20,219

### soundness-fit

status: 0
selected-output-source: final-output

#### selected output

    VERDICT: FLAG
    NOTE: `intent/frame/signoff.md` is absent, so the signed-frame premise cannot be verified.

#### final output

    VERDICT: FLAG
    NOTE: `intent/frame/signoff.md` is absent, so the signed-frame premise cannot be verified.

#### stdout

    VERDICT: FLAG
    NOTE: `intent/frame/signoff.md` is absent, so the signed-frame premise cannot be verified.

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
    session id: 019ea530-983b-7a81-a272-f71a19e8e2ca
    --------
    user
    Review role: soundness-fit
    Work: 012-self-applied-phase-two
    Frame directory: 012-self-applied-phase-two/intent/frame
    
    Read only the signed work frame and the intent it references. Do not debate other reviewers.
    Return exactly one structured verdict line:
    VERDICT: PASS
    or
    VERDICT: FLAG
    
    Then optionally add one NOTE: line. Treat uncertainty as FLAG.
    hook: UserPromptSubmit
    hook: UserPromptSubmit Completed
    exec
    /bin/bash -lc 'find 012-self-applied-phase-two/intent/frame -maxdepth 2 -type f -print | sort' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    012-self-applied-phase-two/intent/frame/direction.md
    012-self-applied-phase-two/intent/frame/frame.md
    012-self-applied-phase-two/intent/frame/options.md
    012-self-applied-phase-two/intent/frame/review.md
    
    exec
    /bin/bash -lc 'find 012-self-applied-phase-two -maxdepth 3 -type f -print | sort' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    012-self-applied-phase-two/intent/frame/direction.md
    012-self-applied-phase-two/intent/frame/frame.md
    012-self-applied-phase-two/intent/frame/options.md
    012-self-applied-phase-two/intent/frame/review.md
    012-self-applied-phase-two/intent/organizing-document.md
    
    exec
    /bin/bash -lc "sed -n '1,240p' 012-self-applied-phase-two/intent/frame/frame.md" in /home/qqp/projects/hypercore
    exec
    /bin/bash -lc "sed -n '1,240p' 012-self-applied-phase-two/intent/frame/direction.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # direction - 012-self-applied-phase-two
    
    direction-by: qqp-dev
    direction-given-at: 2026-06-08T01:57:11Z
    operator-gate: tty
    selected-route: Ship all four fixes. Cache soft-fail; implement-gate/archive reconciliation; handoff auto-detect + Opus-launch + kickoff prose; and orchestrator self-edit safety — the orchestrator runs from a snapshot so a unit that edits `loop.sh` mid-run cannot corrupt the live run, with a self-test proving it. Deep fold/intent-vs-material semantics defer to the work-node-collapse loop.
    
     succeeded in 0ms:
    # frame - 012-self-applied-phase-two
    
    ## work
    
    Addressed node: . (the methodology root)
    
    Node-local work name: 012-self-applied-phase-two
    
    Target segments: loop, adapter, active-work
    
    Work in flight: none active. Related ephemeral findings queued but not started:
    `WORK-NODE-COLLAPSE-FINDINGS.md` (work-node taxonomy + the `intent/frame/` folder + the
    intent-vs-material split) — this node defers the deep fold/intent-vs-material question to that
    loop; `TWO-STEP-BUILD-FINDINGS.md` (builder routing — held at gpt-5.5, no conflict);
    `DECOMPOSITION-FINDINGS.md` (seed-units). This node touches the `loop`/`adapter` execute,
    cache, gate-prompt, and handoff statements, plus a bounded `active-work` clarification (the
    in-flight-vs-adopted distinction the gate reconciliation requires), so no live collision (none
    in flight; first to adopt wins).
    
    ## problem
    
    Phase two cannot complete autonomously on hypercore's own methodology self-changes. Every
    self-change to date (008-011) was archived by hand. Four distinct causes:
    
    1. **The resumable cache step is fatal when it should be soft.** After a unit builds and
       passes tier-one, `loop.sh` records a cache entry by calling `phase_two_write_cache_record`
       inside `$(...)` under `set -euo pipefail`; that function `die`s on any missing or unclean
       evidence. Any transient there aborts the whole run before the remaining units and the
       tier-two panel. This is what halted the 011 run (post-hoc every artifact checks clean — the
       signature of a transient). The cache is a resumability optimization; its failure must never
       halt phase two or change a correctness outcome.
    
    2. **The implement gate contradicts the loop's own vertical-slice rule.** `loop.md` says
       "units are vertical slices, so statements, material, and checks land together when the work
       requires all three," but the implement gate prompt says "Do not edit the intent documents."
       For a self-change whose proof is a check over the intent statements themselves (e.g.
       `check.sh` scanning intent), the unit cannot leave `check.sh` green without editing intent
       during implement — which the gate forbids. In 011 the builder had to violate the gate to
       make progress. The contract argues with itself.
    
    3. **A self-modifying unit can edit `loop.sh` while `loop.sh` is the running orchestrator.**
       Editing the bash script a live process is reading is a latent corruption hazard. It has
       never been exercised (every self-change halted earlier or ran by hand), but autonomous
       self-change requires units that edit `loop.sh`, so the goal cannot be reached while the
       orchestrator runs from a file its own units rewrite.
    
    4. **The handoff is not real.** There is no smooth path for Opus to launch a gpt-5.5 codex
       orchestrator after sign-off, and `execute` requires a work name with no way to resolve the
       single signed, unarchived node; "start" (new work) is easy to confuse with "execute"
       (phase two).
    
    5. **Root cause — orchestrator gate prompts are frozen inline at launch (discovered during the
       first execute attempt).** The implement and archive contract prompts live as inline strings
       in `loop.sh` (the implement prompt in `run_unit_build_attempt`, the archive prompt in
       `cmd_execute`), which bash parses into memory when the orchestrator launches; gate-prompt
       *files* under `adapter/gates/*.md` are re-read per invocation via `cat`, but the inline copies
       are not. So a loop-self-change that rewrites these prompts cannot self-apply mid-run — the
       running orchestrator keeps the old prompts regardless of what its units write. This is the
       bootstrap floor under every manual archive (008-011). Moving the contract prompts out of the
       inline strings into the re-read gate files removes the floor so future loop-self-changes need
       no inline bootstrap. (Scope expansion, operator-directed after the first run surfaced it.)
    
    The deeper question of what archive "folds" — which frame parts are intent vs material, and
    whether a work node stages its own proposed intent — is **out of scope**: it is the
    load-bearing open question of `WORK-NODE-COLLAPSE-FINDINGS.md` and is deferred to that loop.
    This node removes the self-contradiction (cause 2) and makes the one `active-work` clarification
    that removal requires, without settling the intent-vs-material split or any staging mechanism.
    
    ## constraints
    
    - Preserve the cleared-session, memoryless re-derivation contract: phase two re-derives each
      unit and acceptance review from the signed frame directory plus lean handoff artifacts.
    - The cache is an optimization: a cache failure degrades to a rebuild, never a halt, and never
      changes a correctness outcome.
    - Keep every correctness gate fatal: `check.sh` red, an unresolved required `FLAG`, a failed
      build, fake/dry-run acceptance for real archive — all still stop phase two. Only the cache
      optimization softens.
    - The `active-work` change is bounded to the in-flight-vs-adopted-current clarification the
      gate reconciliation requires. Do not settle the deep intent-vs-material / fold-staging
      question; that defers to the work-node-collapse loop.
    - Keep the strong review floor and the tier-one + one-way tier-two panel intact and
      independent.
    - The nested codex subprocess is the base function. Cross-session visibility between the
      nested sessions is out of scope.
    - Builder stays held at gpt-5.5 (this is not the two-step plan/build work).
    
    ## decision surface or open direction
    
    Direction selected `include-orchestrator-safety` (tty-gated). After the first execute attempt
    surfaced cause 5 (frozen-inline gate prompts), the operator directed an in-scope expansion:
    relocate the inline implement/archive prompts into the re-read gate files so the orchestrator-
    safety route also removes the bootstrap floor, not just the corruption hazard. Because this
    materially changes what is built, the prior sign-off is superseded and the expanded frame is
    re-signed before phase two. Settled in collaboration: Opus launches and supervises the
    orchestrator (gpt-5.5 orchestrates and builds); the implement-gate self-contradiction is removed
    with the bounded `active-work` clarification; deep fold semantics defer.
    
    Reversibility: one-way
    
    ## route
    
    Ship the operator's selected route, `include-orchestrator-safety`, expanded to fix the root
    cause. Cache soft-fail; the implement-gate/archive reconciliation with the `active-work`
    clarification it requires, **plus relocating the inline implement/archive contract prompts out
    of `loop.sh` into the re-read gate files** so loop-self-changes self-apply with no inline
    bootstrap; the Opus->codex launch + supervise handoff with `execute` auto-detect and
    `start`/`execute` disambiguation; and orchestrator self-edit safety via a snapshot. Each fix
    lands as a vertical slice — `loop.sh`/`check.sh`/gate prompt and the matching `loop`/`adapter`/
    `active-work` intent and machine statements together — leaving `./check.sh` green at every unit
    boundary. The deep fold / intent-vs-material / staging semantics are not touched; they defer to
    the work-node-collapse loop.
    
    **Unit order and the one last bootstrap.** Snapshot self-edit safety lands first so no unit
    edits `loop.sh` before the safety exists in the contract. Because 012 itself rewrites the
    orchestrator's frozen-inline gate prompts, its own run cannot self-apply them (cause 5) — so it
    needs **one last** hand-bootstrap: before launch, Opus pre-applies the implement/archive prompt
    reconciliation to both the inline strings and the gate files, so the launched orchestrator runs
    reconciled (implement permits the unit's required root-intent edits; archive ratifies). The
    codex builders then build all units — editing tracked root intent the diff record can see — and
    unit-002 relocates the inline prompts into the gate files. After 012 adopts, the inline prompts
    are gone, so every future loop-self-change self-applies with no bootstrap at all. 012's own run
    is self-edit-safe regardless because `loop.sh` is fully parsed before `cmd_execute` runs.
    
    Implementation units for phase two:
    
    1. Add orchestrator self-edit safety. Make `adapter/loop.sh` run phase two from an immutable
       snapshot of itself (re-exec from a copy at execute start) so a unit that edits `loop.sh`
       mid-run cannot corrupt the live orchestrator. Record it in the `loop` and `adapter` intent
       and machine statements, and add a self-test proving a mid-run `loop.sh` edit does not corrupt
       the active run. `./check.sh` is green at the unit boundary. (First so no later unit edits
       `loop.sh` before the safety exists; 012's own bootstrap run is launched from a manual
       snapshot by the supervisor.)
    2. Relocate the inline gate prompts into the re-read gate files, reconcile them, and make the
       bounded `active-work` clarification. Move the contract-bearing implement and archive prompt
       text out of the inline strings in `adapter/loop.sh` (`run_unit_build_attempt`, `cmd_execute`)
       into `adapter/gates/implement.md` and `adapter/gates/archive.md`, which `run_gate` re-reads per
       invocation via `cat`, leaving only dynamic per-unit data (unit id, proof obligation, decision
       line) inline — so a loop-self-change's prompt edits take effect mid-run and the inline
       bootstrap floor is gone. Reconcile while moving: the implement gate permits a unit to edit
       intent when the unit's own proof is a check over that intent (removing the blanket "do not edit
       the intent documents" prohibition that contradicts `intent/loop.md`'s vertical-slice
       statement); the archive gate adopts — verifies the applied delta against the signed frame,
       stamps each touched segment foot, and records history — rather than requiring a separate
       content-fold of intent the units already applied. Clarify in `intent/active-work.md` that
       intent a signed work node applies in place during phase two is in-flight, not adopted;
       adoption is the act that stamps the operator's endorsement and records history, making the
       change adopted-current, and "the parent intent remains current until adoption" governs adopted
       truth, consistent with the loop's existing in-flight-vs-adopted concurrency reading. Update the
       `loop` and `adapter` intent and machine statements to match, and add `check.sh` assertions
       encoding (a) the reconciled contract and (b) that no contract-bearing implement/archive prompt
       remains frozen inline in `loop.sh` — so neither the self-contradiction nor the inline floor can
       silently return. `./check.sh` is green at the unit boundary.
    3. Make the resumable cache non-fatal. In `adapter/loop.sh`, a failure at the per-unit
       cache-record step logs and degrades to a soft miss (the unit rebuilds next run); it never
       aborts phase two and never changes a correctness outcome. Record the non-fatality in the
       `loop` and `adapter` intent and machine statements, and add a `check.sh` self-test proving a
       poisoned or failing cache-record step yields a soft miss and the run proceeds (no fatal
       exit), through the existing dry-run / fake-dir self-test surface. `./check.sh` is green at the
       unit boundary.
    4. Make the handoff real. `loop.sh execute` resolves the single signed, unarchived work node in
       the addressed node when `<work-name>` is omitted (and blocks with a clear message when zero or
       more than one exist). Add the Opus->codex launch + supervise path and the `start`-versus-
       `execute` distinction to `adapter/codex.md` and the `adapter` intent and machine statements,
       and add a `check.sh` self-test for the auto-detect resolution. `./check.sh` is green at the
       unit boundary.
    
    ## acceptance condition
    
    After sign-off, Opus launches a fresh gpt-5.5 codex orchestrator session that nests its own
    codex builder/reviewer/archive sub-sessions, and a signed self-modifying work node runs from
    `execute` through adoption with Opus supervising and intervening only on a genuine stuck
    state: every unit builds, `check.sh` is green at each boundary, tier-one and the one-way
    tier-two panel are clean and real-source, archive adopts and records history. A cache-step
    failure produces a rebuild, not a halt. A self-modifying unit cannot corrupt the orchestrator,
    and a unit whose proof is a check over intent may edit that intent without violating the
    contract or the `active-work` "current until adoption" guarantee.
    
    ## observable acceptance
    
    - `./check.sh` is green after the change.
    - A self-test demonstrates that a poisoned/failing cache-record step yields a soft miss and
      the run proceeds (no fatal exit), through the existing dry-run / fake-dir self-test surface.
    - A `check.sh` assertion encodes that the implement gate permits intent edits a unit's own
      proof requires, that archive adopts (verifies the applied delta against the signed frame,
      stamps, records), and that `active-work` distinguishes in-flight from adopted-current — so the
      implement/archive self-contradiction cannot silently return and the gates do not contradict
      `active-work`.
    - A `check.sh` assertion confirms no contract-bearing implement/archive prompt remains frozen
      inline in `adapter/loop.sh` (the contract text lives in the re-read `adapter/gates/*.md`
      files), and a self-test demonstrates that a mid-run change to a gate-prompt file takes effect
      on the next gate invocation in the same run — proving the inline bootstrap floor is removed.
    - A self-test demonstrates a unit editing `loop.sh` mid-run cannot corrupt the active
      orchestrator (the orchestrator runs from a snapshot).
    - `loop.sh execute` resolves the single signed, unarchived work node when `<work-name>` is
      omitted, provable by a self-test; adapter prose names the Opus->codex launch + supervise path
      and distinguishes `start` (new work) from `execute` (phase two).
    
    ## excluded interpretation
    
    - Not settling what archive folds, nor the intent-vs-material split, nor work-node staging —
      those are the work-node-collapse loop's. The `active-work` change here is only the in-flight-
      vs-adopted-current clarification the gate reconciliation requires.
    - Not making the nested codex sessions visible to each other (no shared context or
      cross-session observability) — that is a later loop.
    - Not the two-step strong-plan / cheap-build work; the builder stays gpt-5.5.
    - Not weakening any correctness gate; only the cache optimization becomes non-fatal.
    - Not changing who endorses or the operator-act `/dev/tty` gates.
    
    ## proof state
    
    The five causes are read from current material: cause 1 from `adapter/loop.sh`
    (`phase_two_write_cache_record`, the `$(...)` capture under `set -euo pipefail`); cause 2 from
    `intent/loop.md` ("vertical slices") vs `adapter/gates/implement.md` ("do not edit the intent
    documents"); cause 3 from the orchestrator running `adapter/loop.sh` as a live process while
    units may edit it; cause 4 from `cmd_execute` requiring `<work-name>` and the absence of a
    launch path; cause 5 from `run_gate` (`sys="$(cat "$GATES/$instruction_gate.md")"` re-reads gate
    files per invocation, while the inline implement/archive prompts in `run_unit_build_attempt` and
    `cmd_execute` are frozen at launch) — confirmed empirically when the first execute attempt wedged
    on unit-001. The 011 manual archive
    (`intent/history/adopted/011-phase-one-routing/intent/frame/manual-archive.md`) records the
    empirical halt and the de-naming workaround. Proof of the fix is `./check.sh` green plus the
    new self-tests named in observable acceptance.
    
    ## sweep
    
    Concepts touched and where they appear:
    
    - **resumable cache / execute** — `intent/loop.md`, `intent/machine-statements/loop.md`,
      `intent/machine-statements/adapter.md` ("a resumable per-unit execute cache"),
      `adapter/loop.sh`, `check.sh`. The soft-fail change keeps these statements true (resumable)
      and adds non-fatality; no statement is contradicted.
    - **implement / archive gates / adoption** — `intent/loop.md` (the vertical-slice and archive
      statements), `intent/active-work.md` (amendments not current until adoption; adoption folds
      and records), `intent/endorsement.md` (sign-off stamps each touched segment),
      `adapter/gates/implement.md`, `adapter/gates/archive.md`,
      `intent/machine-statements/adapter.md` (gate-prompt assertions), `check.sh`. Removing the "do
      not edit intent" prohibition aligns the implement gate with the loop's vertical-slice
      statement; archive's adopt-verify-stamp-record keeps `endorsement` true (archive still
      stamps); `active-work` is clarified (not contradicted) so its "current until adoption" reads
      as adopted-current. The deep fold semantics (intent-vs-material split, staging) stay deferred.
    
    exec
    /bin/bash -lc "sed -n '1,240p' 012-self-applied-phase-two/intent/frame/review.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # review - 012-self-applied-phase-two
    
    Overall: FLAG
    Isolation: reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
    Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
    Disposition: escalated - FLAG verdicts must be answered in the frame; optional reviewers are advisory only and cannot clear base-roster or red-team flags
    
    ## base roster verdicts
    
    - contract-checkability: FLAG
    - soundness-fit: FLAG
    - simplicity-fastness: PASS
    - red-team: FLAG
    
    ## unresolved flags
    
    - contract-checkability (base): `intent/frame/signoff.md` is absent and `frame.md` lacks the loop-required adoption-or-shelving claim field, so the purported signed frame is not mechanically checkable.
    - soundness-fit (base): The frame directory has no `signoff.md`, so I cannot verify the signed-frame premise.
    - red-team (base): The frame directory lacks `signoff.md`, and the route also depends on a manual snapshot bootstrap before that mechanism is adopted, so the signed autonomous phase-two premise is not verifiable.
    
    ## reviewer notes
    
    ### contract-checkability
    
    `intent/frame/signoff.md` is absent and `frame.md` lacks the loop-required adoption-or-shelving claim field, so the purported signed frame is not mechanically checkable.
    
    ### soundness-fit
    
    The frame directory has no `signoff.md`, so I cannot verify the signed-frame premise.
    
    ### simplicity-fastness
    
    The route now puts snapshot safety first and bounds 012’s unavoidable bootstrap explicitly, so the prior simplicity-fastness hazard is answered.
    
    ### red-team
    
    The frame directory lacks `signoff.md`, and the route also depends on a manual snapshot bootstrap before that mechanism is adopted, so the signed autonomous phase-two premise is not verifiable.
    
    ## reviewer diagnostics
    
    ### contract-checkability
    
    status: 0
    selected-output-source: final-output
    
    #### selected output
    
        VERDICT: FLAG
        NOTE: `intent/frame/signoff.md` is absent and `frame.md` lacks the loop-required adoption-or-shelving claim field, so the purported signed frame is not mechanically checkable.
    
    #### final output
    
        VERDICT: FLAG
        NOTE: `intent/frame/signoff.md` is absent and `frame.md` lacks the loop-required adoption-or-shelving claim field, so the purported signed frame is not mechanically checkable.
    
    #### stdout
    
        VERDICT: FLAG
        NOTE: `intent/frame/signoff.md` is absent and `frame.md` lacks the loop-required adoption-or-shelving claim field, so the purported signed frame is not mechanically checkable.
    
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
        session id: 019ea501-a753-7260-a565-9b7cc4ff881a
        --------
        user
        Review role: contract-checkability
        Work: 012-self-applied-phase-two
        Frame directory: 012-self-applied-phase-two/intent/frame
        
        Read only the signed work frame and the intent it references. Do not debate other reviewers.
        Return exactly one structured verdict line:
        VERDICT: PASS
        or
        VERDICT: FLAG
        
        Then optionally add one NOTE: line. Treat uncertainty as FLAG.
        hook: UserPromptSubmit
        hook: UserPromptSubmit Completed
        codex
        I’m reading the signed frame artifacts and only the referenced intent segments, then I’ll return the required one-line verdict.
        exec
        /bin/bash -lc 'rg --files 012-self-applied-phase-two/intent/frame' in /home/qqp/projects/hypercore
         succeeded in 0ms:
        012-self-applied-phase-two/intent/frame/review.md
        012-self-applied-phase-two/intent/frame/options.md
        012-self-applied-phase-two/intent/frame/frame.md
        012-self-applied-phase-two/intent/frame/direction.md
        
        exec
        /bin/bash -lc "sed -n '1,220p' 012-self-applied-phase-two/intent/frame/options.md" in /home/qqp/projects/hypercore
         succeeded in 0ms:
        # options - 012-self-applied-phase-two
        
        Direction options are drafted by the machine for operator selection. The operator selects one
        route, rejects all options, or aborts without writing direction. Both routes carry the same
        three fixes — cache soft-fail (a cache-record failure becomes a rebuild, never a halt), the
        implement-gate/archive reconciliation (a unit may edit intent when its own proof is a check
        over that intent; archive adopts = verify-against-signed-frame + stamp + record), and the
        handoff (`execute` auto-detects the single signed unarchived node; adapter prose names the
        Opus->codex launch + supervise path and separates `start` from `execute`). They differ only on
        orchestrator self-edit safety.
        
        ## option 1
        
        id: include-orchestrator-safety
        kind: selected-route
        summary: Ship all four fixes. Cache soft-fail; implement-gate/archive reconciliation; handoff
          auto-detect + Opus-launch + kickoff prose; and orchestrator self-edit safety — the
          orchestrator runs from a snapshot so a unit that edits `loop.sh` mid-run cannot corrupt the
          live run, with a self-test proving it. Deep fold/intent-vs-material semantics defer to the
          work-node-collapse loop.
        reversibility: one-way
        tradeoff: Delivers a fully hands-off autonomous self-applied phase two: units may freely edit
          `loop.sh`/`check.sh`/intent and the run stays safe. Cost: the snapshot/self-edit-safety
          change is the largest and least-exercised piece, so it carries the most build and review risk
          in this node.
        
        ## option 2
        
        id: defer-orchestrator-safety
        kind: selected-route
        summary: Ship three fixes — cache soft-fail; implement-gate/archive reconciliation; handoff
          auto-detect + Opus-launch + kickoff prose — and carry orchestrator self-edit safety as an
          explicit recorded debt for a later loop. Deep fold semantics also defer to work-node-collapse.
        reversibility: one-way
        tradeoff: Leaner, lower-risk node that still fixes the 011 halt and makes the handoff real.
          Cost: a unit that rewrites `loop.sh` mid-run remains a latent hazard, so a self-change that
          edits `loop.sh` heavily may still need Opus to intervene during supervision until the debt is
          paid.
        
        ## rejection choices
        
        none: The operator may reject all options and send the work back to frame.
        abort: The operator may abort without writing direction.
        
        exec
        /bin/bash -lc "sed -n '1,220p' 012-self-applied-phase-two/intent/frame/frame.md" in /home/qqp/projects/hypercore
         succeeded in 0ms:
        # frame - 012-self-applied-phase-two
        
        ## work
        
        Addressed node: . (the methodology root)
        
        Node-local work name: 012-self-applied-phase-two
        
        Target segments: loop, adapter, active-work
        
        Work in flight: none active. Related ephemeral findings queued but not started:
        `WORK-NODE-COLLAPSE-FINDINGS.md` (work-node taxonomy + the `intent/frame/` folder + the
        intent-vs-material split) — this node defers the deep fold/intent-vs-material question to that
        loop; `TWO-STEP-BUILD-FINDINGS.md` (builder routing — held at gpt-5.5, no conflict);
        `DECOMPOSITION-FINDINGS.md` (seed-units). This node touches the `loop`/`adapter` execute,
        cache, gate-prompt, and handoff statements, plus a bounded `active-work` clarification (the
        in-flight-vs-adopted distinction the gate reconciliation requires), so no live collision (none
        in flight; first to adopt wins).
        
        ## problem
        
        Phase two cannot complete autonomously on hypercore's own methodology self-changes. Every
        self-change to date (008-011) was archived by hand. Four distinct causes:
        
        1. **The resumable cache step is fatal when it should be soft.** After a unit builds and
           passes tier-one, `loop.sh` records a cache entry by calling `phase_two_write_cache_record`
           inside `$(...)` under `set -euo pipefail`; that function `die`s on any missing or unclean
           evidence. Any transient there aborts the whole run before the remaining units and the
           tier-two panel. This is what halted the 011 run (post-hoc every artifact checks clean — the
           signature of a transient). The cache is a resumability optimization; its failure must never
           halt phase two or change a correctness outcome.
        
        2. **The implement gate contradicts the loop's own vertical-slice rule.** `loop.md` says
           "units are vertical slices, so statements, material, and checks land together when the work
           requires all three," but the implement gate prompt says "Do not edit the intent documents."
           For a self-change whose proof is a check over the intent statements themselves (e.g.
           `check.sh` scanning intent), the unit cannot leave `check.sh` green without editing intent
           during implement — which the gate forbids. In 011 the builder had to violate the gate to
           make progress. The contract argues with itself.
        
        3. **A self-modifying unit can edit `loop.sh` while `loop.sh` is the running orchestrator.**
           Editing the bash script a live process is reading is a latent corruption hazard. It has
           never been exercised (every self-change halted earlier or ran by hand), but autonomous
           self-change requires units that edit `loop.sh`, so the goal cannot be reached while the
           orchestrator runs from a file its own units rewrite.
        
        4. **The handoff is not real.** There is no smooth path for Opus to launch a gpt-5.5 codex
           orchestrator after sign-off, and `execute` requires a work name with no way to resolve the
           single signed, unarchived node; "start" (new work) is easy to confuse with "execute"
           (phase two).
        
        The deeper question of what archive "folds" — which frame parts are intent vs material, and
        whether a work node stages its own proposed intent — is **out of scope**: it is the
        load-bearing open question of `WORK-NODE-COLLAPSE-FINDINGS.md` and is deferred to that loop.
        This node removes the self-contradiction (cause 2) and makes the one `active-work` clarification
        that removal requires, without settling the intent-vs-material split or any staging mechanism.
        
        ## constraints
        
        - Preserve the cleared-session, memoryless re-derivation contract: phase two re-derives each
          unit and acceptance review from the signed frame directory plus lean handoff artifacts.
        - The cache is an optimization: a cache failure degrades to a rebuild, never a halt, and never
          changes a correctness outcome.
        - Keep every correctness gate fatal: `check.sh` red, an unresolved required `FLAG`, a failed
          build, fake/dry-run acceptance for real archive — all still stop phase two. Only the cache
          optimization softens.
        - The `active-work` change is bounded to the in-flight-vs-adopted-current clarification the
          gate reconciliation requires. Do not settle the deep intent-vs-material / fold-staging
          question; that defers to the work-node-collapse loop.
        - Keep the strong review floor and the tier-one + one-way tier-two panel intact and
          independent.
        - The nested codex subprocess is the base function. Cross-session visibility between the
          nested sessions is out of scope.
        - Builder stays held at gpt-5.5 (this is not the two-step plan/build work).
        
        ## decision surface or open direction
        
        Settled. Direction selected `include-orchestrator-safety` (all four fixes; tty-gated). Settled
        in collaboration: Opus launches and supervises the orchestrator (gpt-5.5 orchestrates and
        builds); the implement-gate self-contradiction is removed in this node with the bounded
        `active-work` clarification it requires; deep fold semantics defer.
        
        Reversibility: one-way
        
        ## route
        
        Ship all four fixes (the operator's selected route, `include-orchestrator-safety`). Cache
        soft-fail; the implement-gate/archive reconciliation with the `active-work` clarification it
        requires; the Opus->codex launch + supervise handoff with `execute` auto-detect and
        `start`/`execute` disambiguation; and orchestrator self-edit safety via a snapshot. Each fix
        lands as a vertical slice — `loop.sh`/`check.sh`/gate prompt and the matching `loop`/`adapter`/
        `active-work` intent and machine statements together — leaving `./check.sh` green at every unit
        boundary. The deep fold / intent-vs-material / staging semantics are not touched; they defer to
    
    exec
    /bin/bash -lc "sed -n '1,240p' 012-self-applied-phase-two/intent/frame/options.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # options - 012-self-applied-phase-two
    
    Direction options are drafted by the machine for operator selection. The operator selects one
    route, rejects all options, or aborts without writing direction. Both routes carry the same
    three fixes — cache soft-fail (a cache-record failure becomes a rebuild, never a halt), the
    implement-gate/archive reconciliation (a unit may edit intent when its own proof is a check
    over that intent; archive adopts = verify-against-signed-frame + stamp + record), and the
    handoff (`execute` auto-detects the single signed unarchived node; adapter prose names the
    Opus->codex launch + supervise path and separates `start` from `execute`). They differ only on
    orchestrator self-edit safety.
    
    ## option 1
    
    id: include-orchestrator-safety
    kind: selected-route
    summary: Ship all four fixes. Cache soft-fail; implement-gate/archive reconciliation; handoff
      auto-detect + Opus-launch + kickoff prose; and orchestrator self-edit safety — the
      orchestrator runs from a snapshot so a unit that edits `loop.sh` mid-run cannot corrupt the
      live run, with a self-test proving it. Deep fold/intent-vs-material semantics defer to the
      work-node-collapse loop.
    reversibility: one-way
    tradeoff: Delivers a fully hands-off autonomous self-applied phase two: units may freely edit
      `loop.sh`/`check.sh`/intent and the run stays safe. Cost: the snapshot/self-edit-safety
      change is the largest and least-exercised piece, so it carries the most build and review risk
      in this node.
    
    ## option 2
    
    id: defer-orchestrator-safety
    kind: selected-route
    summary: Ship three fixes — cache soft-fail; implement-gate/archive reconciliation; handoff
      auto-detect + Opus-launch + kickoff prose — and carry orchestrator self-edit safety as an
      explicit recorded debt for a later loop. Deep fold semantics also defer to work-node-collapse.
    reversibility: one-way
    tradeoff: Leaner, lower-risk node that still fixes the 011 halt and makes the handoff real.
      Cost: a unit that rewrites `loop.sh` mid-run remains a latent hazard, so a self-change that
      edits `loop.sh` heavily may still need Opus to intervene during supervision until the debt is
      paid.
    
    ## rejection choices
    
    none: The operator may reject all options and send the work back to frame.
    abort: The operator may abort without writing direction.
    
    codex
    VERDICT: FLAG
    NOTE: `intent/frame/signoff.md` is absent, so the signed-frame premise cannot be verified.
    hook: Stop
    hook: Stop Completed
    tokens used
    14,769

### simplicity-fastness

status: 0
selected-output-source: final-output

#### selected output

    VERDICT: FLAG
    NOTE: `signoff.md` is absent, so the signed-frame premise is not verifiable.

#### final output

    VERDICT: FLAG
    NOTE: `signoff.md` is absent, so the signed-frame premise is not verifiable.

#### stdout

    VERDICT: FLAG
    NOTE: `signoff.md` is absent, so the signed-frame premise is not verifiable.

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
    session id: 019ea531-1eca-71a3-9e9c-ee283d0f5689
    --------
    user
    Review role: simplicity-fastness
    Work: 012-self-applied-phase-two
    Frame directory: 012-self-applied-phase-two/intent/frame
    
    Read only the signed work frame and the intent it references. Do not debate other reviewers.
    Return exactly one structured verdict line:
    VERDICT: PASS
    or
    VERDICT: FLAG
    
    Then optionally add one NOTE: line. Treat uncertainty as FLAG.
    hook: UserPromptSubmit
    hook: UserPromptSubmit Completed
    exec
    /bin/bash -lc "test -f 012-self-applied-phase-two/intent/frame/frame.md && sed -n '1,240p' 012-self-applied-phase-two/intent/frame/frame.md" in /home/qqp/projects/hypercore
    exec
    /bin/bash -lc "test -f 012-self-applied-phase-two/intent/frame/signoff.md && sed -n '1,200p' 012-self-applied-phase-two/intent/frame/signoff.md" in /home/qqp/projects/hypercore
     exited 1 in 0ms:
     succeeded in 0ms:
    # frame - 012-self-applied-phase-two
    
    ## work
    
    Addressed node: . (the methodology root)
    
    Node-local work name: 012-self-applied-phase-two
    
    Target segments: loop, adapter, active-work
    
    Work in flight: none active. Related ephemeral findings queued but not started:
    `WORK-NODE-COLLAPSE-FINDINGS.md` (work-node taxonomy + the `intent/frame/` folder + the
    intent-vs-material split) — this node defers the deep fold/intent-vs-material question to that
    loop; `TWO-STEP-BUILD-FINDINGS.md` (builder routing — held at gpt-5.5, no conflict);
    `DECOMPOSITION-FINDINGS.md` (seed-units). This node touches the `loop`/`adapter` execute,
    cache, gate-prompt, and handoff statements, plus a bounded `active-work` clarification (the
    in-flight-vs-adopted distinction the gate reconciliation requires), so no live collision (none
    in flight; first to adopt wins).
    
    ## problem
    
    Phase two cannot complete autonomously on hypercore's own methodology self-changes. Every
    self-change to date (008-011) was archived by hand. Four distinct causes:
    
    1. **The resumable cache step is fatal when it should be soft.** After a unit builds and
       passes tier-one, `loop.sh` records a cache entry by calling `phase_two_write_cache_record`
       inside `$(...)` under `set -euo pipefail`; that function `die`s on any missing or unclean
       evidence. Any transient there aborts the whole run before the remaining units and the
       tier-two panel. This is what halted the 011 run (post-hoc every artifact checks clean — the
       signature of a transient). The cache is a resumability optimization; its failure must never
       halt phase two or change a correctness outcome.
    
    2. **The implement gate contradicts the loop's own vertical-slice rule.** `loop.md` says
       "units are vertical slices, so statements, material, and checks land together when the work
       requires all three," but the implement gate prompt says "Do not edit the intent documents."
       For a self-change whose proof is a check over the intent statements themselves (e.g.
       `check.sh` scanning intent), the unit cannot leave `check.sh` green without editing intent
       during implement — which the gate forbids. In 011 the builder had to violate the gate to
       make progress. The contract argues with itself.
    
    3. **A self-modifying unit can edit `loop.sh` while `loop.sh` is the running orchestrator.**
       Editing the bash script a live process is reading is a latent corruption hazard. It has
       never been exercised (every self-change halted earlier or ran by hand), but autonomous
       self-change requires units that edit `loop.sh`, so the goal cannot be reached while the
       orchestrator runs from a file its own units rewrite.
    
    4. **The handoff is not real.** There is no smooth path for Opus to launch a gpt-5.5 codex
       orchestrator after sign-off, and `execute` requires a work name with no way to resolve the
       single signed, unarchived node; "start" (new work) is easy to confuse with "execute"
       (phase two).
    
    5. **Root cause — orchestrator gate prompts are frozen inline at launch (discovered during the
       first execute attempt).** The implement and archive contract prompts live as inline strings
       in `loop.sh` (the implement prompt in `run_unit_build_attempt`, the archive prompt in
       `cmd_execute`), which bash parses into memory when the orchestrator launches; gate-prompt
       *files* under `adapter/gates/*.md` are re-read per invocation via `cat`, but the inline copies
       are not. So a loop-self-change that rewrites these prompts cannot self-apply mid-run — the
       running orchestrator keeps the old prompts regardless of what its units write. This is the
       bootstrap floor under every manual archive (008-011). Moving the contract prompts out of the
       inline strings into the re-read gate files removes the floor so future loop-self-changes need
       no inline bootstrap. (Scope expansion, operator-directed after the first run surfaced it.)
    
    The deeper question of what archive "folds" — which frame parts are intent vs material, and
    whether a work node stages its own proposed intent — is **out of scope**: it is the
    load-bearing open question of `WORK-NODE-COLLAPSE-FINDINGS.md` and is deferred to that loop.
    This node removes the self-contradiction (cause 2) and makes the one `active-work` clarification
    that removal requires, without settling the intent-vs-material split or any staging mechanism.
    
    ## constraints
    
    - Preserve the cleared-session, memoryless re-derivation contract: phase two re-derives each
      unit and acceptance review from the signed frame directory plus lean handoff artifacts.
    - The cache is an optimization: a cache failure degrades to a rebuild, never a halt, and never
      changes a correctness outcome.
    - Keep every correctness gate fatal: `check.sh` red, an unresolved required `FLAG`, a failed
      build, fake/dry-run acceptance for real archive — all still stop phase two. Only the cache
      optimization softens.
    - The `active-work` change is bounded to the in-flight-vs-adopted-current clarification the
      gate reconciliation requires. Do not settle the deep intent-vs-material / fold-staging
      question; that defers to the work-node-collapse loop.
    - Keep the strong review floor and the tier-one + one-way tier-two panel intact and
      independent.
    - The nested codex subprocess is the base function. Cross-session visibility between the
      nested sessions is out of scope.
    - Builder stays held at gpt-5.5 (this is not the two-step plan/build work).
    
    ## decision surface or open direction
    
    Direction selected `include-orchestrator-safety` (tty-gated). After the first execute attempt
    surfaced cause 5 (frozen-inline gate prompts), the operator directed an in-scope expansion:
    relocate the inline implement/archive prompts into the re-read gate files so the orchestrator-
    safety route also removes the bootstrap floor, not just the corruption hazard. Because this
    materially changes what is built, the prior sign-off is superseded and the expanded frame is
    re-signed before phase two. Settled in collaboration: Opus launches and supervises the
    orchestrator (gpt-5.5 orchestrates and builds); the implement-gate self-contradiction is removed
    with the bounded `active-work` clarification; deep fold semantics defer.
    
    Reversibility: one-way
    
    ## route
    
    Ship the operator's selected route, `include-orchestrator-safety`, expanded to fix the root
    cause. Cache soft-fail; the implement-gate/archive reconciliation with the `active-work`
    clarification it requires, **plus relocating the inline implement/archive contract prompts out
    of `loop.sh` into the re-read gate files** so loop-self-changes self-apply with no inline
    bootstrap; the Opus->codex launch + supervise handoff with `execute` auto-detect and
    `start`/`execute` disambiguation; and orchestrator self-edit safety via a snapshot. Each fix
    lands as a vertical slice — `loop.sh`/`check.sh`/gate prompt and the matching `loop`/`adapter`/
    `active-work` intent and machine statements together — leaving `./check.sh` green at every unit
    boundary. The deep fold / intent-vs-material / staging semantics are not touched; they defer to
    the work-node-collapse loop.
    
    **Unit order and the one last bootstrap.** Snapshot self-edit safety lands first so no unit
    edits `loop.sh` before the safety exists in the contract. Because 012 itself rewrites the
    orchestrator's frozen-inline gate prompts, its own run cannot self-apply them (cause 5) — so it
    needs **one last** hand-bootstrap: before launch, Opus pre-applies the implement/archive prompt
    reconciliation to both the inline strings and the gate files, so the launched orchestrator runs
    reconciled (implement permits the unit's required root-intent edits; archive ratifies). The
    codex builders then build all units — editing tracked root intent the diff record can see — and
    unit-002 relocates the inline prompts into the gate files. After 012 adopts, the inline prompts
    are gone, so every future loop-self-change self-applies with no bootstrap at all. 012's own run
    is self-edit-safe regardless because `loop.sh` is fully parsed before `cmd_execute` runs.
    
    Implementation units for phase two:
    
    1. Add orchestrator self-edit safety. Make `adapter/loop.sh` run phase two from an immutable
       snapshot of itself (re-exec from a copy at execute start) so a unit that edits `loop.sh`
       mid-run cannot corrupt the live orchestrator. Record it in the `loop` and `adapter` intent
       and machine statements, and add a self-test proving a mid-run `loop.sh` edit does not corrupt
       the active run. `./check.sh` is green at the unit boundary. (First so no later unit edits
       `loop.sh` before the safety exists; 012's own bootstrap run is launched from a manual
       snapshot by the supervisor.)
    2. Relocate the inline gate prompts into the re-read gate files, reconcile them, and make the
       bounded `active-work` clarification. Move the contract-bearing implement and archive prompt
       text out of the inline strings in `adapter/loop.sh` (`run_unit_build_attempt`, `cmd_execute`)
       into `adapter/gates/implement.md` and `adapter/gates/archive.md`, which `run_gate` re-reads per
       invocation via `cat`, leaving only dynamic per-unit data (unit id, proof obligation, decision
       line) inline — so a loop-self-change's prompt edits take effect mid-run and the inline
       bootstrap floor is gone. Reconcile while moving: the implement gate permits a unit to edit
       intent when the unit's own proof is a check over that intent (removing the blanket "do not edit
       the intent documents" prohibition that contradicts `intent/loop.md`'s vertical-slice
       statement); the archive gate adopts — verifies the applied delta against the signed frame,
       stamps each touched segment foot, and records history — rather than requiring a separate
       content-fold of intent the units already applied. Clarify in `intent/active-work.md` that
       intent a signed work node applies in place during phase two is in-flight, not adopted;
       adoption is the act that stamps the operator's endorsement and records history, making the
       change adopted-current, and "the parent intent remains current until adoption" governs adopted
       truth, consistent with the loop's existing in-flight-vs-adopted concurrency reading. Update the
       `loop` and `adapter` intent and machine statements to match, and add `check.sh` assertions
       encoding (a) the reconciled contract and (b) that no contract-bearing implement/archive prompt
       remains frozen inline in `loop.sh` — so neither the self-contradiction nor the inline floor can
       silently return. `./check.sh` is green at the unit boundary.
    3. Make the resumable cache non-fatal. In `adapter/loop.sh`, a failure at the per-unit
       cache-record step logs and degrades to a soft miss (the unit rebuilds next run); it never
       aborts phase two and never changes a correctness outcome. Record the non-fatality in the
       `loop` and `adapter` intent and machine statements, and add a `check.sh` self-test proving a
       poisoned or failing cache-record step yields a soft miss and the run proceeds (no fatal
       exit), through the existing dry-run / fake-dir self-test surface. `./check.sh` is green at the
       unit boundary.
    4. Make the handoff real. `loop.sh execute` resolves the single signed, unarchived work node in
       the addressed node when `<work-name>` is omitted (and blocks with a clear message when zero or
       more than one exist). Add the Opus->codex launch + supervise path and the `start`-versus-
       `execute` distinction to `adapter/codex.md` and the `adapter` intent and machine statements,
       and add a `check.sh` self-test for the auto-detect resolution. `./check.sh` is green at the
       unit boundary.
    
    ## acceptance condition
    
    After sign-off, Opus launches a fresh gpt-5.5 codex orchestrator session that nests its own
    codex builder/reviewer/archive sub-sessions, and a signed self-modifying work node runs from
    `execute` through adoption with Opus supervising and intervening only on a genuine stuck
    state: every unit builds, `check.sh` is green at each boundary, tier-one and the one-way
    tier-two panel are clean and real-source, archive adopts and records history. A cache-step
    failure produces a rebuild, not a halt. A self-modifying unit cannot corrupt the orchestrator,
    and a unit whose proof is a check over intent may edit that intent without violating the
    contract or the `active-work` "current until adoption" guarantee.
    
    ## observable acceptance
    
    - `./check.sh` is green after the change.
    - A self-test demonstrates that a poisoned/failing cache-record step yields a soft miss and
      the run proceeds (no fatal exit), through the existing dry-run / fake-dir self-test surface.
    - A `check.sh` assertion encodes that the implement gate permits intent edits a unit's own
      proof requires, that archive adopts (verifies the applied delta against the signed frame,
      stamps, records), and that `active-work` distinguishes in-flight from adopted-current — so the
      implement/archive self-contradiction cannot silently return and the gates do not contradict
      `active-work`.
    - A `check.sh` assertion confirms no contract-bearing implement/archive prompt remains frozen
      inline in `adapter/loop.sh` (the contract text lives in the re-read `adapter/gates/*.md`
      files), and a self-test demonstrates that a mid-run change to a gate-prompt file takes effect
      on the next gate invocation in the same run — proving the inline bootstrap floor is removed.
    - A self-test demonstrates a unit editing `loop.sh` mid-run cannot corrupt the active
      orchestrator (the orchestrator runs from a snapshot).
    - `loop.sh execute` resolves the single signed, unarchived work node when `<work-name>` is
      omitted, provable by a self-test; adapter prose names the Opus->codex launch + supervise path
      and distinguishes `start` (new work) from `execute` (phase two).
    
    ## excluded interpretation
    
    - Not settling what archive folds, nor the intent-vs-material split, nor work-node staging —
      those are the work-node-collapse loop's. The `active-work` change here is only the in-flight-
      vs-adopted-current clarification the gate reconciliation requires.
    - Not making the nested codex sessions visible to each other (no shared context or
      cross-session observability) — that is a later loop.
    - Not the two-step strong-plan / cheap-build work; the builder stays gpt-5.5.
    - Not weakening any correctness gate; only the cache optimization becomes non-fatal.
    - Not changing who endorses or the operator-act `/dev/tty` gates.
    
    ## proof state
    
    The five causes are read from current material: cause 1 from `adapter/loop.sh`
    (`phase_two_write_cache_record`, the `$(...)` capture under `set -euo pipefail`); cause 2 from
    `intent/loop.md` ("vertical slices") vs `adapter/gates/implement.md` ("do not edit the intent
    documents"); cause 3 from the orchestrator running `adapter/loop.sh` as a live process while
    units may edit it; cause 4 from `cmd_execute` requiring `<work-name>` and the absence of a
    launch path; cause 5 from `run_gate` (`sys="$(cat "$GATES/$instruction_gate.md")"` re-reads gate
    files per invocation, while the inline implement/archive prompts in `run_unit_build_attempt` and
    `cmd_execute` are frozen at launch) — confirmed empirically when the first execute attempt wedged
    on unit-001. The 011 manual archive
    (`intent/history/adopted/011-phase-one-routing/intent/frame/manual-archive.md`) records the
    empirical halt and the de-naming workaround. Proof of the fix is `./check.sh` green plus the
    new self-tests named in observable acceptance.
    
    ## sweep
    
    Concepts touched and where they appear:
    
    - **resumable cache / execute** — `intent/loop.md`, `intent/machine-statements/loop.md`,
      `intent/machine-statements/adapter.md` ("a resumable per-unit execute cache"),
      `adapter/loop.sh`, `check.sh`. The soft-fail change keeps these statements true (resumable)
      and adds non-fatality; no statement is contradicted.
    - **implement / archive gates / adoption** — `intent/loop.md` (the vertical-slice and archive
      statements), `intent/active-work.md` (amendments not current until adoption; adoption folds
      and records), `intent/endorsement.md` (sign-off stamps each touched segment),
      `adapter/gates/implement.md`, `adapter/gates/archive.md`,
      `intent/machine-statements/adapter.md` (gate-prompt assertions), `check.sh`. Removing the "do
      not edit intent" prohibition aligns the implement gate with the loop's vertical-slice
      statement; archive's adopt-verify-stamp-record keeps `endorsement` true (archive still
      stamps); `active-work` is clarified (not contradicted) so its "current until adoption" reads
      as adopted-current. The deep fold semantics (intent-vs-material split, staging) stay deferred.
    
    exec
    /bin/bash -lc 'rg --files 012-self-applied-phase-two/intent/frame' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    012-self-applied-phase-two/intent/frame/review.md
    012-self-applied-phase-two/intent/frame/options.md
    012-self-applied-phase-two/intent/frame/direction.md
    012-self-applied-phase-two/intent/frame/frame.md
    
    exec
    /bin/bash -lc "sed -n '1,240p' 012-self-applied-phase-two/intent/frame/direction.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # direction - 012-self-applied-phase-two
    
    direction-by: qqp-dev
    direction-given-at: 2026-06-08T01:57:11Z
    operator-gate: tty
    selected-route: Ship all four fixes. Cache soft-fail; implement-gate/archive reconciliation; handoff auto-detect + Opus-launch + kickoff prose; and orchestrator self-edit safety — the orchestrator runs from a snapshot so a unit that edits `loop.sh` mid-run cannot corrupt the live run, with a self-test proving it. Deep fold/intent-vs-material semantics defer to the work-node-collapse loop.
    
    exec
    /bin/bash -lc 'ls -la 012-self-applied-phase-two/intent/frame' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    total 332
    drwxrwxr-x 2 qqp qqp   4096 Jun  7 22:03 .
    drwxrwxr-x 3 qqp qqp   4096 Jun  7 21:55 ..
    -rw-rw-r-- 1 qqp qqp    518 Jun  7 20:57 direction.md
    -rw-rw-r-- 1 qqp qqp  20811 Jun  7 22:03 frame.md
    -rw-rw-r-- 1 qqp qqp   2318 Jun  7 20:55 options.md
    -rw-rw-r-- 1 qqp qqp 296973 Jun  7 21:19 review.md
    
    exec
    /bin/bash -lc "sed -n '1,260p' 012-self-applied-phase-two/intent/frame/options.md" in /home/qqp/projects/hypercore
    exec
    /bin/bash -lc "sed -n '1,260p' 012-self-applied-phase-two/intent/frame/review.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # options - 012-self-applied-phase-two
    
    Direction options are drafted by the machine for operator selection. The operator selects one
    route, rejects all options, or aborts without writing direction. Both routes carry the same
    three fixes — cache soft-fail (a cache-record failure becomes a rebuild, never a halt), the
    implement-gate/archive reconciliation (a unit may edit intent when its own proof is a check
    over that intent; archive adopts = verify-against-signed-frame + stamp + record), and the
    handoff (`execute` auto-detects the single signed unarchived node; adapter prose names the
    Opus->codex launch + supervise path and separates `start` from `execute`). They differ only on
    orchestrator self-edit safety.
    
    ## option 1
    
    id: include-orchestrator-safety
    kind: selected-route
    summary: Ship all four fixes. Cache soft-fail; implement-gate/archive reconciliation; handoff
      auto-detect + Opus-launch + kickoff prose; and orchestrator self-edit safety — the
      orchestrator runs from a snapshot so a unit that edits `loop.sh` mid-run cannot corrupt the
      live run, with a self-test proving it. Deep fold/intent-vs-material semantics defer to the
      work-node-collapse loop.
    reversibility: one-way
    tradeoff: Delivers a fully hands-off autonomous self-applied phase two: units may freely edit
      `loop.sh`/`check.sh`/intent and the run stays safe. Cost: the snapshot/self-edit-safety
      change is the largest and least-exercised piece, so it carries the most build and review risk
      in this node.
    
    ## option 2
    
    id: defer-orchestrator-safety
    kind: selected-route
    summary: Ship three fixes — cache soft-fail; implement-gate/archive reconciliation; handoff
      auto-detect + Opus-launch + kickoff prose — and carry orchestrator self-edit safety as an
      explicit recorded debt for a later loop. Deep fold semantics also defer to work-node-collapse.
    reversibility: one-way
    tradeoff: Leaner, lower-risk node that still fixes the 011 halt and makes the handoff real.
      Cost: a unit that rewrites `loop.sh` mid-run remains a latent hazard, so a self-change that
      edits `loop.sh` heavily may still need Opus to intervene during supervision until the debt is
      paid.
    
    ## rejection choices
    
    none: The operator may reject all options and send the work back to frame.
    abort: The operator may abort without writing direction.
    
     succeeded in 0ms:
    # review - 012-self-applied-phase-two
    
    Overall: FLAG
    Isolation: reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
    Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
    Disposition: escalated - FLAG verdicts must be answered in the frame; optional reviewers are advisory only and cannot clear base-roster or red-team flags
    
    ## base roster verdicts
    
    - contract-checkability: FLAG
    - soundness-fit: FLAG
    - simplicity-fastness: PASS
    - red-team: FLAG
    
    ## unresolved flags
    
    - contract-checkability (base): `intent/frame/signoff.md` is absent and `frame.md` lacks the loop-required adoption-or-shelving claim field, so the purported signed frame is not mechanically checkable.
    - soundness-fit (base): The frame directory has no `signoff.md`, so I cannot verify the signed-frame premise.
    - red-team (base): The frame directory lacks `signoff.md`, and the route also depends on a manual snapshot bootstrap before that mechanism is adopted, so the signed autonomous phase-two premise is not verifiable.
    
    ## reviewer notes
    
    ### contract-checkability
    
    `intent/frame/signoff.md` is absent and `frame.md` lacks the loop-required adoption-or-shelving claim field, so the purported signed frame is not mechanically checkable.
    
    ### soundness-fit
    
    The frame directory has no `signoff.md`, so I cannot verify the signed-frame premise.
    
    ### simplicity-fastness
    
    The route now puts snapshot safety first and bounds 012’s unavoidable bootstrap explicitly, so the prior simplicity-fastness hazard is answered.
    
    ### red-team
    
    The frame directory lacks `signoff.md`, and the route also depends on a manual snapshot bootstrap before that mechanism is adopted, so the signed autonomous phase-two premise is not verifiable.
    
    ## reviewer diagnostics
    
    ### contract-checkability
    
    status: 0
    selected-output-source: final-output
    
    #### selected output
    
        VERDICT: FLAG
        NOTE: `intent/frame/signoff.md` is absent and `frame.md` lacks the loop-required adoption-or-shelving claim field, so the purported signed frame is not mechanically checkable.
    
    #### final output
    
        VERDICT: FLAG
        NOTE: `intent/frame/signoff.md` is absent and `frame.md` lacks the loop-required adoption-or-shelving claim field, so the purported signed frame is not mechanically checkable.
    
    #### stdout
    
        VERDICT: FLAG
        NOTE: `intent/frame/signoff.md` is absent and `frame.md` lacks the loop-required adoption-or-shelving claim field, so the purported signed frame is not mechanically checkable.
    
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
        session id: 019ea501-a753-7260-a565-9b7cc4ff881a
        --------
        user
        Review role: contract-checkability
        Work: 012-self-applied-phase-two
        Frame directory: 012-self-applied-phase-two/intent/frame
        
        Read only the signed work frame and the intent it references. Do not debate other reviewers.
        Return exactly one structured verdict line:
        VERDICT: PASS
        or
        VERDICT: FLAG
        
        Then optionally add one NOTE: line. Treat uncertainty as FLAG.
        hook: UserPromptSubmit
        hook: UserPromptSubmit Completed
        codex
        I’m reading the signed frame artifacts and only the referenced intent segments, then I’ll return the required one-line verdict.
        exec
        /bin/bash -lc 'rg --files 012-self-applied-phase-two/intent/frame' in /home/qqp/projects/hypercore
         succeeded in 0ms:
        012-self-applied-phase-two/intent/frame/review.md
        012-self-applied-phase-two/intent/frame/options.md
        012-self-applied-phase-two/intent/frame/frame.md
        012-self-applied-phase-two/intent/frame/direction.md
        
        exec
        /bin/bash -lc "sed -n '1,220p' 012-self-applied-phase-two/intent/frame/options.md" in /home/qqp/projects/hypercore
         succeeded in 0ms:
        # options - 012-self-applied-phase-two
        
        Direction options are drafted by the machine for operator selection. The operator selects one
        route, rejects all options, or aborts without writing direction. Both routes carry the same
        three fixes — cache soft-fail (a cache-record failure becomes a rebuild, never a halt), the
        implement-gate/archive reconciliation (a unit may edit intent when its own proof is a check
        over that intent; archive adopts = verify-against-signed-frame + stamp + record), and the
        handoff (`execute` auto-detects the single signed unarchived node; adapter prose names the
        Opus->codex launch + supervise path and separates `start` from `execute`). They differ only on
        orchestrator self-edit safety.
        
        ## option 1
        
        id: include-orchestrator-safety
        kind: selected-route
        summary: Ship all four fixes. Cache soft-fail; implement-gate/archive reconciliation; handoff
          auto-detect + Opus-launch + kickoff prose; and orchestrator self-edit safety — the
          orchestrator runs from a snapshot so a unit that edits `loop.sh` mid-run cannot corrupt the
          live run, with a self-test proving it. Deep fold/intent-vs-material semantics defer to the
          work-node-collapse loop.
        reversibility: one-way
        tradeoff: Delivers a fully hands-off autonomous self-applied phase two: units may freely edit
          `loop.sh`/`check.sh`/intent and the run stays safe. Cost: the snapshot/self-edit-safety
          change is the largest and least-exercised piece, so it carries the most build and review risk
          in this node.
        
        ## option 2
        
        id: defer-orchestrator-safety
        kind: selected-route
        summary: Ship three fixes — cache soft-fail; implement-gate/archive reconciliation; handoff
          auto-detect + Opus-launch + kickoff prose — and carry orchestrator self-edit safety as an
          explicit recorded debt for a later loop. Deep fold semantics also defer to work-node-collapse.
        reversibility: one-way
        tradeoff: Leaner, lower-risk node that still fixes the 011 halt and makes the handoff real.
          Cost: a unit that rewrites `loop.sh` mid-run remains a latent hazard, so a self-change that
          edits `loop.sh` heavily may still need Opus to intervene during supervision until the debt is
          paid.
        
        ## rejection choices
        
        none: The operator may reject all options and send the work back to frame.
        abort: The operator may abort without writing direction.
        
        exec
        /bin/bash -lc "sed -n '1,220p' 012-self-applied-phase-two/intent/frame/frame.md" in /home/qqp/projects/hypercore
         succeeded in 0ms:
        # frame - 012-self-applied-phase-two
        
        ## work
        
        Addressed node: . (the methodology root)
        
        Node-local work name: 012-self-applied-phase-two
        
        Target segments: loop, adapter, active-work
        
        Work in flight: none active. Related ephemeral findings queued but not started:
        `WORK-NODE-COLLAPSE-FINDINGS.md` (work-node taxonomy + the `intent/frame/` folder + the
        intent-vs-material split) — this node defers the deep fold/intent-vs-material question to that
        loop; `TWO-STEP-BUILD-FINDINGS.md` (builder routing — held at gpt-5.5, no conflict);
        `DECOMPOSITION-FINDINGS.md` (seed-units). This node touches the `loop`/`adapter` execute,
        cache, gate-prompt, and handoff statements, plus a bounded `active-work` clarification (the
        in-flight-vs-adopted distinction the gate reconciliation requires), so no live collision (none
        in flight; first to adopt wins).
        
        ## problem
        
        Phase two cannot complete autonomously on hypercore's own methodology self-changes. Every
        self-change to date (008-011) was archived by hand. Four distinct causes:
        
        1. **The resumable cache step is fatal when it should be soft.** After a unit builds and
           passes tier-one, `loop.sh` records a cache entry by calling `phase_two_write_cache_record`
           inside `$(...)` under `set -euo pipefail`; that function `die`s on any missing or unclean
           evidence. Any transient there aborts the whole run before the remaining units and the
           tier-two panel. This is what halted the 011 run (post-hoc every artifact checks clean — the
           signature of a transient). The cache is a resumability optimization; its failure must never
           halt phase two or change a correctness outcome.
        
        2. **The implement gate contradicts the loop's own vertical-slice rule.** `loop.md` says
           "units are vertical slices, so statements, material, and checks land together when the work
           requires all three," but the implement gate prompt says "Do not edit the intent documents."
           For a self-change whose proof is a check over the intent statements themselves (e.g.
           `check.sh` scanning intent), the unit cannot leave `check.sh` green without editing intent
           during implement — which the gate forbids. In 011 the builder had to violate the gate to
           make progress. The contract argues with itself.
        
        3. **A self-modifying unit can edit `loop.sh` while `loop.sh` is the running orchestrator.**
           Editing the bash script a live process is reading is a latent corruption hazard. It has
           never been exercised (every self-change halted earlier or ran by hand), but autonomous
           self-change requires units that edit `loop.sh`, so the goal cannot be reached while the
           orchestrator runs from a file its own units rewrite.
        
        4. **The handoff is not real.** There is no smooth path for Opus to launch a gpt-5.5 codex
           orchestrator after sign-off, and `execute` requires a work name with no way to resolve the
           single signed, unarchived node; "start" (new work) is easy to confuse with "execute"
           (phase two).
        
        The deeper question of what archive "folds" — which frame parts are intent vs material, and
        whether a work node stages its own proposed intent — is **out of scope**: it is the
        load-bearing open question of `WORK-NODE-COLLAPSE-FINDINGS.md` and is deferred to that loop.
        This node removes the self-contradiction (cause 2) and makes the one `active-work` clarification
        that removal requires, without settling the intent-vs-material split or any staging mechanism.
        
        ## constraints
        
        - Preserve the cleared-session, memoryless re-derivation contract: phase two re-derives each
          unit and acceptance review from the signed frame directory plus lean handoff artifacts.
        - The cache is an optimization: a cache failure degrades to a rebuild, never a halt, and never
          changes a correctness outcome.
        - Keep every correctness gate fatal: `check.sh` red, an unresolved required `FLAG`, a failed
          build, fake/dry-run acceptance for real archive — all still stop phase two. Only the cache
          optimization softens.
        - The `active-work` change is bounded to the in-flight-vs-adopted-current clarification the
          gate reconciliation requires. Do not settle the deep intent-vs-material / fold-staging
          question; that defers to the work-node-collapse loop.
        - Keep the strong review floor and the tier-one + one-way tier-two panel intact and
          independent.
        - The nested codex subprocess is the base function. Cross-session visibility between the
          nested sessions is out of scope.
        - Builder stays held at gpt-5.5 (this is not the two-step plan/build work).
        
        ## decision surface or open direction
        
        Settled. Direction selected `include-orchestrator-safety` (all four fixes; tty-gated). Settled
        in collaboration: Opus launches and supervises the orchestrator (gpt-5.5 orchestrates and
        builds); the implement-gate self-contradiction is removed in this node with the bounded
        `active-work` clarification it requires; deep fold semantics defer.
        
        Reversibility: one-way
        
        ## route
        
        Ship all four fixes (the operator's selected route, `include-orchestrator-safety`). Cache
        soft-fail; the implement-gate/archive reconciliation with the `active-work` clarification it
        requires; the Opus->codex launch + supervise handoff with `execute` auto-detect and
        `start`/`execute` disambiguation; and orchestrator self-edit safety via a snapshot. Each fix
        lands as a vertical slice — `loop.sh`/`check.sh`/gate prompt and the matching `loop`/`adapter`/
        `active-work` intent and machine statements together — leaving `./check.sh` green at every unit
        boundary. The deep fold / intent-vs-material / staging semantics are not touched; they defer to
        the work-node-collapse loop.
        
        **Unit order and the bootstrap.** Snapshot self-edit safety lands first so no unit edits
        `loop.sh` before the safety exists in the contract. Because 012 is itself a self-modifying
        change, its own first run is the unavoidable bootstrap: the snapshot mechanism cannot protect
        the very run that installs it, and the first units must edit intent before the reconciliation is
        active. Opus handles this as supervisor — launching 012's own phase two from a manual `loop.sh`
        snapshot (re-exec from a copy) so even unit-001's `loop.sh` edit is safe, and carrying the first
        units' intent edits under the pre-reconciliation gate. Every self-change after 012 is protected
        by the in-place snapshot and runs under the reconciled gate with no manual bootstrap.
        
        Implementation units for phase two:
        
        1. Add orchestrator self-edit safety. Make `adapter/loop.sh` run phase two from an immutable
           snapshot of itself (re-exec from a copy at execute start) so a unit that edits `loop.sh`
           mid-run cannot corrupt the live orchestrator. Record it in the `loop` and `adapter` intent
           and machine statements, and add a self-test proving a mid-run `loop.sh` edit does not corrupt
           the active run. `./check.sh` is green at the unit boundary. (First so no later unit edits
           `loop.sh` before the safety exists; 012's own bootstrap run is launched from a manual
           snapshot by the supervisor.)
    
    exec
    /bin/bash -lc "sed -n '1,260p' intent/active-work.md" in /home/qqp/projects/hypercore
    exec
    /bin/bash -lc "sed -n '241,520p' 012-self-applied-phase-two/intent/frame/frame.md" in /home/qqp/projects/hypercore
    exec
    /bin/bash -lc "sed -n '1,260p' intent/loop.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    - **orchestrator / nested sessions / handoff** — `intent/adapter.md` (fresh per-unit builder
      and reviewer sessions), `adapter/codex.md`, `adapter/loop.sh`. The handoff change adds the
      Opus->codex launch + supervise path, `execute` auto-detect, and kickoff prose; the
      nested-subprocess model is already current truth, not new. The snapshot change adds
      orchestrator self-edit safety.
    - **vertical slice** — `intent/loop.md`. The contradiction with the implement gate prompt is
      the bug this node fixes; the resolution makes them consistent.
    
    No contradiction with parent truth is introduced; the work removes an existing internal
    contradiction, clarifies the in-flight-vs-adopted boundary the removal requires, hardens the
    orchestrator, and makes the handoff real.
    
    ## review flags answered
    
    Two review rounds ran on the four-fix frame (one-way base roster, gpt-5.5, xhigh, read-only);
    round one returned four FLAGs, round two cleared both discriminating flags. The frame was then
    expanded (cause 5 / inline-prompt relocation) on operator direction, superseding the prior
    sign-off, so a **third review round runs on the expanded frame** and is answered alongside the
    round-two dispositions below.
    
    - **simplicity-fastness — PASS (round two).** The round-one ordering hazard (a `loop.sh` edit
      before snapshot safety) was answered by making orchestrator self-edit safety unit 1.
    - **soundness-fit — `active-work` conflict resolved; only `signoff.md`-absent remains.** Adding
      `active-work` to target segments with the bounded in-flight-vs-adopted-current clarification in
      unit 2 removed the contradiction the round-one reviewer found. The residual flag is the
      prompt debt below.
    - **`signoff.md` absent (contract-checkability, soundness-fit, red-team):** the known phase-one
      review-prompt debt. The reviewer prompt assumes a signed frame, but review is a phase-one act
      that precedes sign-off, so `signoff.md` cannot exist yet. Non-discriminating and unfixable
      before sign-off; carried as a debt in `adapter/codex.md`. Not a frame defect.
    - **contract-checkability — "frame lacks the adoption-or-shelving claim field":** contradicted
      by the mechanical proof floor. `loop.sh status` reports `frame_complete=yes`, and the frame
      carries both `## adoption claim` and `## shelving claim`. For a mechanical-field fact the
      checker is authoritative; this is a reviewer error anchored on the `signoff.md` confusion.
    - **red-team — autonomy depends on a manual snapshot bootstrap, so the premise is "not
      verifiable":** the autonomous-from-execute property is proven mechanically by the self-tests
      in observable acceptance (cache soft-miss continues; a mid-run `loop.sh` edit cannot corrupt
      the snapshot-run orchestrator; auto-detect resolves the signed node) and by units 2-4 running
      under the installed snapshot and reconciled gate. It does not rest on the bootstrap. 012's own
      unit-001 is the one acknowledged manual bootstrap — the snapshot cannot protect the run that
      installs it — and every self-change after 012 runs hands-off from execute. The premise is
      therefore verifiable on any post-installation run, which is the general case the contract
      governs.
    
    ## adoption claim
    
    Adopt into the root: fold the cache-non-fatality, the implement-gate/archive reconciliation,
    the relocation of inline gate prompts into the re-read gate files, the bounded `active-work`
    in-flight-vs-adopted clarification, the orchestrator self-edit safety, and the handoff
    auto-detect + Opus-launch + kickoff statements into `intent/loop.md`,
    `intent/machine-statements/loop.md`, `intent/adapter.md`, `intent/machine-statements/adapter.md`,
    and `intent/active-work.md`; update `adapter/loop.sh`, `adapter/gates/implement.md`,
    `adapter/gates/archive.md`, `adapter/codex.md`, and `check.sh` to match; stamp each touched
    segment foot with the signed-off operator.
    
    ## shelving claim
    
    Shelve if the selected route proves unsound under review or acceptance (e.g. the implement
    gate reconciliation cannot be encoded as a discriminating check, or the orchestrator-safety
    change destabilizes the run); record the reason and leave parent intent unchanged.
    
     succeeded in 0ms:
    # active-work
    
    active work is a child node with the same reserved tree as any other node: `intent/`, plus
    whatever node-local material its work needs beside that reserved tree.
    active work is bounded by the parent intent statements whose reach includes it.
    a work node may propose parent intent or parent material amendments without making those
    amendments current.
    until adoption accepts an amendment, the parent intent remains current.
    adoption folds accepted child statements and material into the parent and records the work
    node as history.
    shelving records the work node as history without making its proposed amendments parent
    truth.
    a work node may be temporary, durable, adopted, shelved, abandoned, or indefinitely active.
    purpose, rationale, proof state, route, sign-off, and adoption claims are recoverable as
    intent or material within the work node; they are not universal required filenames.
    the loop may require recoverable frame fields before sign-off; that is a frame
    completeness contract, not a universal filename shape.
    root-directed active work lives directly under the root as `<NNN-slug>/`, as a sibling to
    `home`, not under `home`.
    the root active-work contract spans root child work nodes and grants them the general
    ability to parent their own child work nodes unless their own contract narrows that
    freedom.
    
    ## machine
    a sibling set of node-local work nodes is named with `NNN-slug` folders, with the ordinal
    scoped to that sibling set.
    new active work nodes live directly under the addressed node.
    a new work node's frame lives under that work node's `intent/frame/`.
    adopted work-node history is recorded under `intent/history/adopted/`.
    shelved work-node history is recorded under `intent/history/shelved/`.
    empty work-node history collections carry `.gitkeep` so the repository holds the collection
    even when no retained record exists inside it.
    
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
    /bin/bash -lc "sed -n '1,320p' intent/machine-statements/adapter.md" in /home/qqp/projects/hypercore
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
    
    exec
    /bin/bash -lc "sed -n '1,220p' intent/endorsement.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # endorsement
    
    ownership is read off an endorsement: an endorsed statement is the operator's, an
    unendorsed one is the machine's.
    the machine never endorses, so everything unendorsed is the machine's and the machine is
    the floor.
    endorsement does not cross a node boundary: the operator endorses the contract in the
    parent and the child's whole operator set in the child, as two separate acts, and the floor
    is per node.
    endorsement is per segment: one operator stands behind the segment's whole operator set,
    not only the statements they last touched.
    to change a segment is to take its whole operator set on, having read it and able to reason
    about it as a whole.
    a segment's endorsement is a single line at the foot of its intent document.
    there is no partial endorsement and no handover step: you own the operator set or you do
    not.
    the relief for an over-large operator set is to split the segment or demote statements to
    `## machine`, not a finer endorsement.
    a work frame carries sign-off: the operator's vouch for every segment the work adopts.
    on adoption, the sign-off stamps the foot of each touched segment with this operator.
    a segment whose adopted work went unendorsed falls to the machine.
    ownership and truth are separate backings: the endorsement says who stands behind the set,
    a check says each statement holds.
    
    ## machine
    a segment's foot endorsement is a `---` rule followed by a line reading
    `endorsed by <operator>`.
    new work sign-off is recorded in `intent/frame/signoff.md` inside the work node.
    
    ---
    endorsed by qqp-dev
    
    codex
    VERDICT: FLAG
    NOTE: `signoff.md` is absent, so the signed-frame premise is not verifiable.
    hook: Stop
    hook: Stop Completed
    tokens used
    38,460

### red-team

status: 0
selected-output-source: final-output

#### selected output

    VERDICT: FLAG
    NOTE: `signoff.md` is absent, so the signed-frame premise is not verifiable.

#### final output

    VERDICT: FLAG
    NOTE: `signoff.md` is absent, so the signed-frame premise is not verifiable.

#### stdout

    VERDICT: FLAG
    NOTE: `signoff.md` is absent, so the signed-frame premise is not verifiable.

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
    session id: 019ea532-5c60-7c93-b3b0-a4f8f04b0ef1
    --------
    user
    Review role: red-team
    Work: 012-self-applied-phase-two
    Frame directory: 012-self-applied-phase-two/intent/frame
    
    Read only the signed work frame and the intent it references. Do not debate other reviewers.
    Return exactly one structured verdict line:
    VERDICT: PASS
    or
    VERDICT: FLAG
    
    Then optionally add one NOTE: line. Treat uncertainty as FLAG.
    hook: UserPromptSubmit
    hook: UserPromptSubmit Completed
    exec
    /bin/bash -lc "sed -n '1,240p' 012-self-applied-phase-two/intent/frame/frame.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # frame - 012-self-applied-phase-two
    
    ## work
    
    Addressed node: . (the methodology root)
    
    Node-local work name: 012-self-applied-phase-two
    
    Target segments: loop, adapter, active-work
    
    Work in flight: none active. Related ephemeral findings queued but not started:
    `WORK-NODE-COLLAPSE-FINDINGS.md` (work-node taxonomy + the `intent/frame/` folder + the
    intent-vs-material split) — this node defers the deep fold/intent-vs-material question to that
    loop; `TWO-STEP-BUILD-FINDINGS.md` (builder routing — held at gpt-5.5, no conflict);
    `DECOMPOSITION-FINDINGS.md` (seed-units). This node touches the `loop`/`adapter` execute,
    cache, gate-prompt, and handoff statements, plus a bounded `active-work` clarification (the
    in-flight-vs-adopted distinction the gate reconciliation requires), so no live collision (none
    in flight; first to adopt wins).
    
    ## problem
    
    Phase two cannot complete autonomously on hypercore's own methodology self-changes. Every
    self-change to date (008-011) was archived by hand. Four distinct causes:
    
    1. **The resumable cache step is fatal when it should be soft.** After a unit builds and
       passes tier-one, `loop.sh` records a cache entry by calling `phase_two_write_cache_record`
       inside `$(...)` under `set -euo pipefail`; that function `die`s on any missing or unclean
       evidence. Any transient there aborts the whole run before the remaining units and the
       tier-two panel. This is what halted the 011 run (post-hoc every artifact checks clean — the
       signature of a transient). The cache is a resumability optimization; its failure must never
       halt phase two or change a correctness outcome.
    
    2. **The implement gate contradicts the loop's own vertical-slice rule.** `loop.md` says
       "units are vertical slices, so statements, material, and checks land together when the work
       requires all three," but the implement gate prompt says "Do not edit the intent documents."
       For a self-change whose proof is a check over the intent statements themselves (e.g.
       `check.sh` scanning intent), the unit cannot leave `check.sh` green without editing intent
       during implement — which the gate forbids. In 011 the builder had to violate the gate to
       make progress. The contract argues with itself.
    
    3. **A self-modifying unit can edit `loop.sh` while `loop.sh` is the running orchestrator.**
       Editing the bash script a live process is reading is a latent corruption hazard. It has
       never been exercised (every self-change halted earlier or ran by hand), but autonomous
       self-change requires units that edit `loop.sh`, so the goal cannot be reached while the
       orchestrator runs from a file its own units rewrite.
    
    4. **The handoff is not real.** There is no smooth path for Opus to launch a gpt-5.5 codex
       orchestrator after sign-off, and `execute` requires a work name with no way to resolve the
       single signed, unarchived node; "start" (new work) is easy to confuse with "execute"
       (phase two).
    
    5. **Root cause — orchestrator gate prompts are frozen inline at launch (discovered during the
       first execute attempt).** The implement and archive contract prompts live as inline strings
       in `loop.sh` (the implement prompt in `run_unit_build_attempt`, the archive prompt in
       `cmd_execute`), which bash parses into memory when the orchestrator launches; gate-prompt
       *files* under `adapter/gates/*.md` are re-read per invocation via `cat`, but the inline copies
       are not. So a loop-self-change that rewrites these prompts cannot self-apply mid-run — the
       running orchestrator keeps the old prompts regardless of what its units write. This is the
       bootstrap floor under every manual archive (008-011). Moving the contract prompts out of the
       inline strings into the re-read gate files removes the floor so future loop-self-changes need
       no inline bootstrap. (Scope expansion, operator-directed after the first run surfaced it.)
    
    The deeper question of what archive "folds" — which frame parts are intent vs material, and
    whether a work node stages its own proposed intent — is **out of scope**: it is the
    load-bearing open question of `WORK-NODE-COLLAPSE-FINDINGS.md` and is deferred to that loop.
    This node removes the self-contradiction (cause 2) and makes the one `active-work` clarification
    that removal requires, without settling the intent-vs-material split or any staging mechanism.
    
    ## constraints
    
    - Preserve the cleared-session, memoryless re-derivation contract: phase two re-derives each
      unit and acceptance review from the signed frame directory plus lean handoff artifacts.
    - The cache is an optimization: a cache failure degrades to a rebuild, never a halt, and never
      changes a correctness outcome.
    - Keep every correctness gate fatal: `check.sh` red, an unresolved required `FLAG`, a failed
      build, fake/dry-run acceptance for real archive — all still stop phase two. Only the cache
      optimization softens.
    - The `active-work` change is bounded to the in-flight-vs-adopted-current clarification the
      gate reconciliation requires. Do not settle the deep intent-vs-material / fold-staging
      question; that defers to the work-node-collapse loop.
    - Keep the strong review floor and the tier-one + one-way tier-two panel intact and
      independent.
    - The nested codex subprocess is the base function. Cross-session visibility between the
      nested sessions is out of scope.
    - Builder stays held at gpt-5.5 (this is not the two-step plan/build work).
    
    ## decision surface or open direction
    
    Direction selected `include-orchestrator-safety` (tty-gated). After the first execute attempt
    surfaced cause 5 (frozen-inline gate prompts), the operator directed an in-scope expansion:
    relocate the inline implement/archive prompts into the re-read gate files so the orchestrator-
    safety route also removes the bootstrap floor, not just the corruption hazard. Because this
    materially changes what is built, the prior sign-off is superseded and the expanded frame is
    re-signed before phase two. Settled in collaboration: Opus launches and supervises the
    orchestrator (gpt-5.5 orchestrates and builds); the implement-gate self-contradiction is removed
    with the bounded `active-work` clarification; deep fold semantics defer.
    
    Reversibility: one-way
    
    ## route
    
    Ship the operator's selected route, `include-orchestrator-safety`, expanded to fix the root
    cause. Cache soft-fail; the implement-gate/archive reconciliation with the `active-work`
    clarification it requires, **plus relocating the inline implement/archive contract prompts out
    of `loop.sh` into the re-read gate files** so loop-self-changes self-apply with no inline
    bootstrap; the Opus->codex launch + supervise handoff with `execute` auto-detect and
    `start`/`execute` disambiguation; and orchestrator self-edit safety via a snapshot. Each fix
    lands as a vertical slice — `loop.sh`/`check.sh`/gate prompt and the matching `loop`/`adapter`/
    `active-work` intent and machine statements together — leaving `./check.sh` green at every unit
    boundary. The deep fold / intent-vs-material / staging semantics are not touched; they defer to
    the work-node-collapse loop.
    
    **Unit order and the one last bootstrap.** Snapshot self-edit safety lands first so no unit
    edits `loop.sh` before the safety exists in the contract. Because 012 itself rewrites the
    orchestrator's frozen-inline gate prompts, its own run cannot self-apply them (cause 5) — so it
    needs **one last** hand-bootstrap: before launch, Opus pre-applies the implement/archive prompt
    reconciliation to both the inline strings and the gate files, so the launched orchestrator runs
    reconciled (implement permits the unit's required root-intent edits; archive ratifies). The
    codex builders then build all units — editing tracked root intent the diff record can see — and
    unit-002 relocates the inline prompts into the gate files. After 012 adopts, the inline prompts
    are gone, so every future loop-self-change self-applies with no bootstrap at all. 012's own run
    is self-edit-safe regardless because `loop.sh` is fully parsed before `cmd_execute` runs.
    
    Implementation units for phase two:
    
    1. Add orchestrator self-edit safety. Make `adapter/loop.sh` run phase two from an immutable
       snapshot of itself (re-exec from a copy at execute start) so a unit that edits `loop.sh`
       mid-run cannot corrupt the live orchestrator. Record it in the `loop` and `adapter` intent
       and machine statements, and add a self-test proving a mid-run `loop.sh` edit does not corrupt
       the active run. `./check.sh` is green at the unit boundary. (First so no later unit edits
       `loop.sh` before the safety exists; 012's own bootstrap run is launched from a manual
       snapshot by the supervisor.)
    2. Relocate the inline gate prompts into the re-read gate files, reconcile them, and make the
       bounded `active-work` clarification. Move the contract-bearing implement and archive prompt
       text out of the inline strings in `adapter/loop.sh` (`run_unit_build_attempt`, `cmd_execute`)
       into `adapter/gates/implement.md` and `adapter/gates/archive.md`, which `run_gate` re-reads per
       invocation via `cat`, leaving only dynamic per-unit data (unit id, proof obligation, decision
       line) inline — so a loop-self-change's prompt edits take effect mid-run and the inline
       bootstrap floor is gone. Reconcile while moving: the implement gate permits a unit to edit
       intent when the unit's own proof is a check over that intent (removing the blanket "do not edit
       the intent documents" prohibition that contradicts `intent/loop.md`'s vertical-slice
       statement); the archive gate adopts — verifies the applied delta against the signed frame,
       stamps each touched segment foot, and records history — rather than requiring a separate
       content-fold of intent the units already applied. Clarify in `intent/active-work.md` that
       intent a signed work node applies in place during phase two is in-flight, not adopted;
       adoption is the act that stamps the operator's endorsement and records history, making the
       change adopted-current, and "the parent intent remains current until adoption" governs adopted
       truth, consistent with the loop's existing in-flight-vs-adopted concurrency reading. Update the
       `loop` and `adapter` intent and machine statements to match, and add `check.sh` assertions
       encoding (a) the reconciled contract and (b) that no contract-bearing implement/archive prompt
       remains frozen inline in `loop.sh` — so neither the self-contradiction nor the inline floor can
       silently return. `./check.sh` is green at the unit boundary.
    3. Make the resumable cache non-fatal. In `adapter/loop.sh`, a failure at the per-unit
       cache-record step logs and degrades to a soft miss (the unit rebuilds next run); it never
       aborts phase two and never changes a correctness outcome. Record the non-fatality in the
       `loop` and `adapter` intent and machine statements, and add a `check.sh` self-test proving a
       poisoned or failing cache-record step yields a soft miss and the run proceeds (no fatal
       exit), through the existing dry-run / fake-dir self-test surface. `./check.sh` is green at the
       unit boundary.
    4. Make the handoff real. `loop.sh execute` resolves the single signed, unarchived work node in
       the addressed node when `<work-name>` is omitted (and blocks with a clear message when zero or
       more than one exist). Add the Opus->codex launch + supervise path and the `start`-versus-
       `execute` distinction to `adapter/codex.md` and the `adapter` intent and machine statements,
       and add a `check.sh` self-test for the auto-detect resolution. `./check.sh` is green at the
       unit boundary.
    
    ## acceptance condition
    
    After sign-off, Opus launches a fresh gpt-5.5 codex orchestrator session that nests its own
    codex builder/reviewer/archive sub-sessions, and a signed self-modifying work node runs from
    `execute` through adoption with Opus supervising and intervening only on a genuine stuck
    state: every unit builds, `check.sh` is green at each boundary, tier-one and the one-way
    tier-two panel are clean and real-source, archive adopts and records history. A cache-step
    failure produces a rebuild, not a halt. A self-modifying unit cannot corrupt the orchestrator,
    and a unit whose proof is a check over intent may edit that intent without violating the
    contract or the `active-work` "current until adoption" guarantee.
    
    ## observable acceptance
    
    - `./check.sh` is green after the change.
    - A self-test demonstrates that a poisoned/failing cache-record step yields a soft miss and
      the run proceeds (no fatal exit), through the existing dry-run / fake-dir self-test surface.
    - A `check.sh` assertion encodes that the implement gate permits intent edits a unit's own
      proof requires, that archive adopts (verifies the applied delta against the signed frame,
      stamps, records), and that `active-work` distinguishes in-flight from adopted-current — so the
      implement/archive self-contradiction cannot silently return and the gates do not contradict
      `active-work`.
    - A `check.sh` assertion confirms no contract-bearing implement/archive prompt remains frozen
      inline in `adapter/loop.sh` (the contract text lives in the re-read `adapter/gates/*.md`
      files), and a self-test demonstrates that a mid-run change to a gate-prompt file takes effect
      on the next gate invocation in the same run — proving the inline bootstrap floor is removed.
    - A self-test demonstrates a unit editing `loop.sh` mid-run cannot corrupt the active
      orchestrator (the orchestrator runs from a snapshot).
    - `loop.sh execute` resolves the single signed, unarchived work node when `<work-name>` is
      omitted, provable by a self-test; adapter prose names the Opus->codex launch + supervise path
      and distinguishes `start` (new work) from `execute` (phase two).
    
    ## excluded interpretation
    
    - Not settling what archive folds, nor the intent-vs-material split, nor work-node staging —
      those are the work-node-collapse loop's. The `active-work` change here is only the in-flight-
      vs-adopted-current clarification the gate reconciliation requires.
    - Not making the nested codex sessions visible to each other (no shared context or
      cross-session observability) — that is a later loop.
    - Not the two-step strong-plan / cheap-build work; the builder stays gpt-5.5.
    - Not weakening any correctness gate; only the cache optimization becomes non-fatal.
    - Not changing who endorses or the operator-act `/dev/tty` gates.
    
    ## proof state
    
    The five causes are read from current material: cause 1 from `adapter/loop.sh`
    (`phase_two_write_cache_record`, the `$(...)` capture under `set -euo pipefail`); cause 2 from
    `intent/loop.md` ("vertical slices") vs `adapter/gates/implement.md` ("do not edit the intent
    documents"); cause 3 from the orchestrator running `adapter/loop.sh` as a live process while
    units may edit it; cause 4 from `cmd_execute` requiring `<work-name>` and the absence of a
    launch path; cause 5 from `run_gate` (`sys="$(cat "$GATES/$instruction_gate.md")"` re-reads gate
    files per invocation, while the inline implement/archive prompts in `run_unit_build_attempt` and
    `cmd_execute` are frozen at launch) — confirmed empirically when the first execute attempt wedged
    on unit-001. The 011 manual archive
    (`intent/history/adopted/011-phase-one-routing/intent/frame/manual-archive.md`) records the
    empirical halt and the de-naming workaround. Proof of the fix is `./check.sh` green plus the
    new self-tests named in observable acceptance.
    
    ## sweep
    
    Concepts touched and where they appear:
    
    - **resumable cache / execute** — `intent/loop.md`, `intent/machine-statements/loop.md`,
      `intent/machine-statements/adapter.md` ("a resumable per-unit execute cache"),
      `adapter/loop.sh`, `check.sh`. The soft-fail change keeps these statements true (resumable)
      and adds non-fatality; no statement is contradicted.
    - **implement / archive gates / adoption** — `intent/loop.md` (the vertical-slice and archive
      statements), `intent/active-work.md` (amendments not current until adoption; adoption folds
      and records), `intent/endorsement.md` (sign-off stamps each touched segment),
      `adapter/gates/implement.md`, `adapter/gates/archive.md`,
      `intent/machine-statements/adapter.md` (gate-prompt assertions), `check.sh`. Removing the "do
      not edit intent" prohibition aligns the implement gate with the loop's vertical-slice
      statement; archive's adopt-verify-stamp-record keeps `endorsement` true (archive still
      stamps); `active-work` is clarified (not contradicted) so its "current until adoption" reads
      as adopted-current. The deep fold semantics (intent-vs-material split, staging) stay deferred.
    
    exec
    /bin/bash -lc 'rg --files 012-self-applied-phase-two/intent/frame' in /home/qqp/projects/hypercore
     succeeded in 0ms:
    012-self-applied-phase-two/intent/frame/options.md
    012-self-applied-phase-two/intent/frame/frame.md
    012-self-applied-phase-two/intent/frame/review.md
    012-self-applied-phase-two/intent/frame/direction.md
    
    exec
    /bin/bash -lc "sed -n '1,120p' 012-self-applied-phase-two/intent/frame/signoff.md" in /home/qqp/projects/hypercore
     exited 2 in 0ms:
    sed: can't read 012-self-applied-phase-two/intent/frame/signoff.md: No such file or directory
    
    exec
    /bin/bash -lc "sed -n '241,520p' 012-self-applied-phase-two/intent/frame/frame.md" in /home/qqp/projects/hypercore
    exec
    /bin/bash -lc "sed -n '1,220p' 012-self-applied-phase-two/intent/frame/direction.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # direction - 012-self-applied-phase-two
    
    direction-by: qqp-dev
    direction-given-at: 2026-06-08T01:57:11Z
    operator-gate: tty
    selected-route: Ship all four fixes. Cache soft-fail; implement-gate/archive reconciliation; handoff auto-detect + Opus-launch + kickoff prose; and orchestrator self-edit safety — the orchestrator runs from a snapshot so a unit that edits `loop.sh` mid-run cannot corrupt the live run, with a self-test proving it. Deep fold/intent-vs-material semantics defer to the work-node-collapse loop.
    
     succeeded in 0ms:
    - **orchestrator / nested sessions / handoff** — `intent/adapter.md` (fresh per-unit builder
      and reviewer sessions), `adapter/codex.md`, `adapter/loop.sh`. The handoff change adds the
      Opus->codex launch + supervise path, `execute` auto-detect, and kickoff prose; the
      nested-subprocess model is already current truth, not new. The snapshot change adds
      orchestrator self-edit safety.
    - **vertical slice** — `intent/loop.md`. The contradiction with the implement gate prompt is
      the bug this node fixes; the resolution makes them consistent.
    
    No contradiction with parent truth is introduced; the work removes an existing internal
    contradiction, clarifies the in-flight-vs-adopted boundary the removal requires, hardens the
    orchestrator, and makes the handoff real.
    
    ## review flags answered
    
    Two review rounds ran on the four-fix frame (one-way base roster, gpt-5.5, xhigh, read-only);
    round one returned four FLAGs, round two cleared both discriminating flags. The frame was then
    expanded (cause 5 / inline-prompt relocation) on operator direction, superseding the prior
    sign-off, so a **third review round runs on the expanded frame** and is answered alongside the
    round-two dispositions below.
    
    - **simplicity-fastness — PASS (round two).** The round-one ordering hazard (a `loop.sh` edit
      before snapshot safety) was answered by making orchestrator self-edit safety unit 1.
    - **soundness-fit — `active-work` conflict resolved; only `signoff.md`-absent remains.** Adding
      `active-work` to target segments with the bounded in-flight-vs-adopted-current clarification in
      unit 2 removed the contradiction the round-one reviewer found. The residual flag is the
      prompt debt below.
    - **`signoff.md` absent (contract-checkability, soundness-fit, red-team):** the known phase-one
      review-prompt debt. The reviewer prompt assumes a signed frame, but review is a phase-one act
      that precedes sign-off, so `signoff.md` cannot exist yet. Non-discriminating and unfixable
      before sign-off; carried as a debt in `adapter/codex.md`. Not a frame defect.
    - **contract-checkability — "frame lacks the adoption-or-shelving claim field":** contradicted
      by the mechanical proof floor. `loop.sh status` reports `frame_complete=yes`, and the frame
      carries both `## adoption claim` and `## shelving claim`. For a mechanical-field fact the
      checker is authoritative; this is a reviewer error anchored on the `signoff.md` confusion.
    - **red-team — autonomy depends on a manual snapshot bootstrap, so the premise is "not
      verifiable":** the autonomous-from-execute property is proven mechanically by the self-tests
      in observable acceptance (cache soft-miss continues; a mid-run `loop.sh` edit cannot corrupt
      the snapshot-run orchestrator; auto-detect resolves the signed node) and by units 2-4 running
      under the installed snapshot and reconciled gate. It does not rest on the bootstrap. 012's own
      unit-001 is the one acknowledged manual bootstrap — the snapshot cannot protect the run that
      installs it — and every self-change after 012 runs hands-off from execute. The premise is
      therefore verifiable on any post-installation run, which is the general case the contract
      governs.
    
    ## adoption claim
    
    Adopt into the root: fold the cache-non-fatality, the implement-gate/archive reconciliation,
    the relocation of inline gate prompts into the re-read gate files, the bounded `active-work`
    in-flight-vs-adopted clarification, the orchestrator self-edit safety, and the handoff
    auto-detect + Opus-launch + kickoff statements into `intent/loop.md`,
    `intent/machine-statements/loop.md`, `intent/adapter.md`, `intent/machine-statements/adapter.md`,
    and `intent/active-work.md`; update `adapter/loop.sh`, `adapter/gates/implement.md`,
    `adapter/gates/archive.md`, `adapter/codex.md`, and `check.sh` to match; stamp each touched
    segment foot with the signed-off operator.
    
    ## shelving claim
    
    Shelve if the selected route proves unsound under review or acceptance (e.g. the implement
    gate reconciliation cannot be encoded as a discriminating check, or the orchestrator-safety
    change destabilizes the run); record the reason and leave parent intent unchanged.
    
    exec
    /bin/bash -lc "sed -n '1,260p' 012-self-applied-phase-two/intent/frame/options.md" in /home/qqp/projects/hypercore
    exec
    /bin/bash -lc "sed -n '1,260p' 012-self-applied-phase-two/intent/frame/review.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # options - 012-self-applied-phase-two
    
    Direction options are drafted by the machine for operator selection. The operator selects one
    route, rejects all options, or aborts without writing direction. Both routes carry the same
    three fixes — cache soft-fail (a cache-record failure becomes a rebuild, never a halt), the
    implement-gate/archive reconciliation (a unit may edit intent when its own proof is a check
    over that intent; archive adopts = verify-against-signed-frame + stamp + record), and the
    handoff (`execute` auto-detects the single signed unarchived node; adapter prose names the
    Opus->codex launch + supervise path and separates `start` from `execute`). They differ only on
    orchestrator self-edit safety.
    
    ## option 1
    
    id: include-orchestrator-safety
    kind: selected-route
    summary: Ship all four fixes. Cache soft-fail; implement-gate/archive reconciliation; handoff
      auto-detect + Opus-launch + kickoff prose; and orchestrator self-edit safety — the
      orchestrator runs from a snapshot so a unit that edits `loop.sh` mid-run cannot corrupt the
      live run, with a self-test proving it. Deep fold/intent-vs-material semantics defer to the
      work-node-collapse loop.
    reversibility: one-way
    tradeoff: Delivers a fully hands-off autonomous self-applied phase two: units may freely edit
      `loop.sh`/`check.sh`/intent and the run stays safe. Cost: the snapshot/self-edit-safety
      change is the largest and least-exercised piece, so it carries the most build and review risk
      in this node.
    
    ## option 2
    
    id: defer-orchestrator-safety
    kind: selected-route
    summary: Ship three fixes — cache soft-fail; implement-gate/archive reconciliation; handoff
      auto-detect + Opus-launch + kickoff prose — and carry orchestrator self-edit safety as an
      explicit recorded debt for a later loop. Deep fold semantics also defer to work-node-collapse.
    reversibility: one-way
    tradeoff: Leaner, lower-risk node that still fixes the 011 halt and makes the handoff real.
      Cost: a unit that rewrites `loop.sh` mid-run remains a latent hazard, so a self-change that
      edits `loop.sh` heavily may still need Opus to intervene during supervision until the debt is
      paid.
    
    ## rejection choices
    
    none: The operator may reject all options and send the work back to frame.
    abort: The operator may abort without writing direction.
    
     succeeded in 0ms:
    # review - 012-self-applied-phase-two
    
    Overall: FLAG
    Isolation: reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
    Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
    Disposition: escalated - FLAG verdicts must be answered in the frame; optional reviewers are advisory only and cannot clear base-roster or red-team flags
    
    ## base roster verdicts
    
    - contract-checkability: FLAG
    - soundness-fit: FLAG
    - simplicity-fastness: PASS
    - red-team: FLAG
    
    ## unresolved flags
    
    - contract-checkability (base): `intent/frame/signoff.md` is absent and `frame.md` lacks the loop-required adoption-or-shelving claim field, so the purported signed frame is not mechanically checkable.
    - soundness-fit (base): The frame directory has no `signoff.md`, so I cannot verify the signed-frame premise.
    - red-team (base): The frame directory lacks `signoff.md`, and the route also depends on a manual snapshot bootstrap before that mechanism is adopted, so the signed autonomous phase-two premise is not verifiable.
    
    ## reviewer notes
    
    ### contract-checkability
    
    `intent/frame/signoff.md` is absent and `frame.md` lacks the loop-required adoption-or-shelving claim field, so the purported signed frame is not mechanically checkable.
    
    ### soundness-fit
    
    The frame directory has no `signoff.md`, so I cannot verify the signed-frame premise.
    
    ### simplicity-fastness
    
    The route now puts snapshot safety first and bounds 012’s unavoidable bootstrap explicitly, so the prior simplicity-fastness hazard is answered.
    
    ### red-team
    
    The frame directory lacks `signoff.md`, and the route also depends on a manual snapshot bootstrap before that mechanism is adopted, so the signed autonomous phase-two premise is not verifiable.
    
    ## reviewer diagnostics
    
    ### contract-checkability
    
    status: 0
    selected-output-source: final-output
    
    #### selected output
    
        VERDICT: FLAG
        NOTE: `intent/frame/signoff.md` is absent and `frame.md` lacks the loop-required adoption-or-shelving claim field, so the purported signed frame is not mechanically checkable.
    
    #### final output
    
        VERDICT: FLAG
        NOTE: `intent/frame/signoff.md` is absent and `frame.md` lacks the loop-required adoption-or-shelving claim field, so the purported signed frame is not mechanically checkable.
    
    #### stdout
    
        VERDICT: FLAG
        NOTE: `intent/frame/signoff.md` is absent and `frame.md` lacks the loop-required adoption-or-shelving claim field, so the purported signed frame is not mechanically checkable.
    
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
        session id: 019ea501-a753-7260-a565-9b7cc4ff881a
        --------
        user
        Review role: contract-checkability
        Work: 012-self-applied-phase-two
        Frame directory: 012-self-applied-phase-two/intent/frame
        
        Read only the signed work frame and the intent it references. Do not debate other reviewers.
        Return exactly one structured verdict line:
        VERDICT: PASS
        or
        VERDICT: FLAG
        
        Then optionally add one NOTE: line. Treat uncertainty as FLAG.
        hook: UserPromptSubmit
        hook: UserPromptSubmit Completed
        codex
        I’m reading the signed frame artifacts and only the referenced intent segments, then I’ll return the required one-line verdict.
        exec
        /bin/bash -lc 'rg --files 012-self-applied-phase-two/intent/frame' in /home/qqp/projects/hypercore
         succeeded in 0ms:
        012-self-applied-phase-two/intent/frame/review.md
        012-self-applied-phase-two/intent/frame/options.md
        012-self-applied-phase-two/intent/frame/frame.md
        012-self-applied-phase-two/intent/frame/direction.md
        
        exec
        /bin/bash -lc "sed -n '1,220p' 012-self-applied-phase-two/intent/frame/options.md" in /home/qqp/projects/hypercore
         succeeded in 0ms:
        # options - 012-self-applied-phase-two
        
        Direction options are drafted by the machine for operator selection. The operator selects one
        route, rejects all options, or aborts without writing direction. Both routes carry the same
        three fixes — cache soft-fail (a cache-record failure becomes a rebuild, never a halt), the
        implement-gate/archive reconciliation (a unit may edit intent when its own proof is a check
        over that intent; archive adopts = verify-against-signed-frame + stamp + record), and the
        handoff (`execute` auto-detects the single signed unarchived node; adapter prose names the
        Opus->codex launch + supervise path and separates `start` from `execute`). They differ only on
        orchestrator self-edit safety.
        
        ## option 1
        
        id: include-orchestrator-safety
        kind: selected-route
        summary: Ship all four fixes. Cache soft-fail; implement-gate/archive reconciliation; handoff
          auto-detect + Opus-launch + kickoff prose; and orchestrator self-edit safety — the
          orchestrator runs from a snapshot so a unit that edits `loop.sh` mid-run cannot corrupt the
          live run, with a self-test proving it. Deep fold/intent-vs-material semantics defer to the
          work-node-collapse loop.
        reversibility: one-way
        tradeoff: Delivers a fully hands-off autonomous self-applied phase two: units may freely edit
          `loop.sh`/`check.sh`/intent and the run stays safe. Cost: the snapshot/self-edit-safety
          change is the largest and least-exercised piece, so it carries the most build and review risk
          in this node.
        
        ## option 2
        
        id: defer-orchestrator-safety
        kind: selected-route
        summary: Ship three fixes — cache soft-fail; implement-gate/archive reconciliation; handoff
          auto-detect + Opus-launch + kickoff prose — and carry orchestrator self-edit safety as an
          explicit recorded debt for a later loop. Deep fold semantics also defer to work-node-collapse.
        reversibility: one-way
        tradeoff: Leaner, lower-risk node that still fixes the 011 halt and makes the handoff real.
          Cost: a unit that rewrites `loop.sh` mid-run remains a latent hazard, so a self-change that
          edits `loop.sh` heavily may still need Opus to intervene during supervision until the debt is
          paid.
        
        ## rejection choices
        
        none: The operator may reject all options and send the work back to frame.
        abort: The operator may abort without writing direction.
        
        exec
        /bin/bash -lc "sed -n '1,220p' 012-self-applied-phase-two/intent/frame/frame.md" in /home/qqp/projects/hypercore
         succeeded in 0ms:
        # frame - 012-self-applied-phase-two
        
        ## work
        
        Addressed node: . (the methodology root)
        
        Node-local work name: 012-self-applied-phase-two
        
        Target segments: loop, adapter, active-work
        
        Work in flight: none active. Related ephemeral findings queued but not started:
        `WORK-NODE-COLLAPSE-FINDINGS.md` (work-node taxonomy + the `intent/frame/` folder + the
        intent-vs-material split) — this node defers the deep fold/intent-vs-material question to that
        loop; `TWO-STEP-BUILD-FINDINGS.md` (builder routing — held at gpt-5.5, no conflict);
        `DECOMPOSITION-FINDINGS.md` (seed-units). This node touches the `loop`/`adapter` execute,
        cache, gate-prompt, and handoff statements, plus a bounded `active-work` clarification (the
        in-flight-vs-adopted distinction the gate reconciliation requires), so no live collision (none
        in flight; first to adopt wins).
        
        ## problem
        
        Phase two cannot complete autonomously on hypercore's own methodology self-changes. Every
        self-change to date (008-011) was archived by hand. Four distinct causes:
        
        1. **The resumable cache step is fatal when it should be soft.** After a unit builds and
           passes tier-one, `loop.sh` records a cache entry by calling `phase_two_write_cache_record`
           inside `$(...)` under `set -euo pipefail`; that function `die`s on any missing or unclean
           evidence. Any transient there aborts the whole run before the remaining units and the
           tier-two panel. This is what halted the 011 run (post-hoc every artifact checks clean — the
           signature of a transient). The cache is a resumability optimization; its failure must never
           halt phase two or change a correctness outcome.
        
        2. **The implement gate contradicts the loop's own vertical-slice rule.** `loop.md` says
           "units are vertical slices, so statements, material, and checks land together when the work
           requires all three," but the implement gate prompt says "Do not edit the intent documents."
           For a self-change whose proof is a check over the intent statements themselves (e.g.
           `check.sh` scanning intent), the unit cannot leave `check.sh` green without editing intent
           during implement — which the gate forbids. In 011 the builder had to violate the gate to
           make progress. The contract argues with itself.
        
        3. **A self-modifying unit can edit `loop.sh` while `loop.sh` is the running orchestrator.**
           Editing the bash script a live process is reading is a latent corruption hazard. It has
           never been exercised (every self-change halted earlier or ran by hand), but autonomous
           self-change requires units that edit `loop.sh`, so the goal cannot be reached while the
           orchestrator runs from a file its own units rewrite.
        
        4. **The handoff is not real.** There is no smooth path for Opus to launch a gpt-5.5 codex
           orchestrator after sign-off, and `execute` requires a work name with no way to resolve the
           single signed, unarchived node; "start" (new work) is easy to confuse with "execute"
           (phase two).
        
        The deeper question of what archive "folds" — which frame parts are intent vs material, and
        whether a work node stages its own proposed intent — is **out of scope**: it is the
        load-bearing open question of `WORK-NODE-COLLAPSE-FINDINGS.md` and is deferred to that loop.
        This node removes the self-contradiction (cause 2) and makes the one `active-work` clarification
        that removal requires, without settling the intent-vs-material split or any staging mechanism.
        
        ## constraints
        
        - Preserve the cleared-session, memoryless re-derivation contract: phase two re-derives each
          unit and acceptance review from the signed frame directory plus lean handoff artifacts.
        - The cache is an optimization: a cache failure degrades to a rebuild, never a halt, and never
          changes a correctness outcome.
        - Keep every correctness gate fatal: `check.sh` red, an unresolved required `FLAG`, a failed
          build, fake/dry-run acceptance for real archive — all still stop phase two. Only the cache
          optimization softens.
        - The `active-work` change is bounded to the in-flight-vs-adopted-current clarification the
          gate reconciliation requires. Do not settle the deep intent-vs-material / fold-staging
          question; that defers to the work-node-collapse loop.
        - Keep the strong review floor and the tier-one + one-way tier-two panel intact and
          independent.
        - The nested codex subprocess is the base function. Cross-session visibility between the
          nested sessions is out of scope.
        - Builder stays held at gpt-5.5 (this is not the two-step plan/build work).
        
        ## decision surface or open direction
        
        Settled. Direction selected `include-orchestrator-safety` (all four fixes; tty-gated). Settled
        in collaboration: Opus launches and supervises the orchestrator (gpt-5.5 orchestrates and
        builds); the implement-gate self-contradiction is removed in this node with the bounded
        `active-work` clarification it requires; deep fold semantics defer.
        
        Reversibility: one-way
        
        ## route
        
        Ship all four fixes (the operator's selected route, `include-orchestrator-safety`). Cache
        soft-fail; the implement-gate/archive reconciliation with the `active-work` clarification it
        requires; the Opus->codex launch + supervise handoff with `execute` auto-detect and
        `start`/`execute` disambiguation; and orchestrator self-edit safety via a snapshot. Each fix
        lands as a vertical slice — `loop.sh`/`check.sh`/gate prompt and the matching `loop`/`adapter`/
        `active-work` intent and machine statements together — leaving `./check.sh` green at every unit
        boundary. The deep fold / intent-vs-material / staging semantics are not touched; they defer to
        the work-node-collapse loop.
        
        **Unit order and the bootstrap.** Snapshot self-edit safety lands first so no unit edits
        `loop.sh` before the safety exists in the contract. Because 012 is itself a self-modifying
        change, its own first run is the unavoidable bootstrap: the snapshot mechanism cannot protect
        the very run that installs it, and the first units must edit intent before the reconciliation is
        active. Opus handles this as supervisor — launching 012's own phase two from a manual `loop.sh`
        snapshot (re-exec from a copy) so even unit-001's `loop.sh` edit is safe, and carrying the first
        units' intent edits under the pre-reconciliation gate. Every self-change after 012 is protected
        by the in-place snapshot and runs under the reconciled gate with no manual bootstrap.
        
        Implementation units for phase two:
        
        1. Add orchestrator self-edit safety. Make `adapter/loop.sh` run phase two from an immutable
           snapshot of itself (re-exec from a copy at execute start) so a unit that edits `loop.sh`
           mid-run cannot corrupt the live orchestrator. Record it in the `loop` and `adapter` intent
           and machine statements, and add a self-test proving a mid-run `loop.sh` edit does not corrupt
           the active run. `./check.sh` is green at the unit boundary. (First so no later unit edits
           `loop.sh` before the safety exists; 012's own bootstrap run is launched from a manual
           snapshot by the supervisor.)
    
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
    
    exec
    /bin/bash -lc "sed -n '1,260p' intent/loop.md" in /home/qqp/projects/hypercore
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
    /bin/bash -lc "sed -n '1,240p' intent/active-work.md" in /home/qqp/projects/hypercore
     succeeded in 0ms:
    # active-work
    
    active work is a child node with the same reserved tree as any other node: `intent/`, plus
    whatever node-local material its work needs beside that reserved tree.
    active work is bounded by the parent intent statements whose reach includes it.
    a work node may propose parent intent or parent material amendments without making those
    amendments current.
    until adoption accepts an amendment, the parent intent remains current.
    adoption folds accepted child statements and material into the parent and records the work
    node as history.
    shelving records the work node as history without making its proposed amendments parent
    truth.
    a work node may be temporary, durable, adopted, shelved, abandoned, or indefinitely active.
    purpose, rationale, proof state, route, sign-off, and adoption claims are recoverable as
    intent or material within the work node; they are not universal required filenames.
    the loop may require recoverable frame fields before sign-off; that is a frame
    completeness contract, not a universal filename shape.
    root-directed active work lives directly under the root as `<NNN-slug>/`, as a sibling to
    `home`, not under `home`.
    the root active-work contract spans root child work nodes and grants them the general
    ability to parent their own child work nodes unless their own contract narrows that
    freedom.
    
    ## machine
    a sibling set of node-local work nodes is named with `NNN-slug` folders, with the ordinal
    scoped to that sibling set.
    new active work nodes live directly under the addressed node.
    a new work node's frame lives under that work node's `intent/frame/`.
    adopted work-node history is recorded under `intent/history/adopted/`.
    shelved work-node history is recorded under `intent/history/shelved/`.
    empty work-node history collections carry `.gitkeep` so the repository holds the collection
    even when no retained record exists inside it.
    
    ---
    endorsed by qqp-dev
    
    codex
    VERDICT: FLAG
    NOTE: `signoff.md` is absent, so the signed-frame premise is not verifiable.
    hook: Stop
    hook: Stop Completed
    tokens used
    27,024

