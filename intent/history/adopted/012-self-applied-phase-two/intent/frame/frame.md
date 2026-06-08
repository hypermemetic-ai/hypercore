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

Three review rounds ran (one-way base roster, gpt-5.5, xhigh, read-only). Round one returned four
FLAGs; round two cleared both discriminating flags; the frame was then expanded (cause 5 /
inline-prompt relocation) on operator direction, superseding the prior sign-off, and **round three
on the expanded frame returned only the structural `signoff.md`-absent flag from all four
reviewers — zero substantive objections** to the relocation, reconciliation, `active-work`
clarification, or bootstrap. The only-remaining flag across the roster is the prompt debt below,
which is unfixable before sign-off.

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
