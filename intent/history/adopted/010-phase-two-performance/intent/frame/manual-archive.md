# manual archive - 010-phase-two-performance

The operator requested a one-time manual archive outside the loop, for the same structural
reason as 008 and 009: the loop's own one-way acceptance door is exactly what this thread
set out to repair, and the loop that executed the run could not pass 010 through itself.

## why ordinary archive was impossible

- The run was orchestrated by the pre-010 `loop.sh`, whose tier-two panel emits a single
  `PASS`/`FLAG` bit under an uncertainty-defaults-to-`FLAG` rule. All five lenses returned a
  bare `FLAG` with no rationale and no evidence — the blind-`FLAG` pathology recorded in the
  (now removed) `PERFORMANCE-FINDINGS.md`. That pathology is the precise thing 010 replaces;
  it fired on its own replacement.
- The recorded panel prompts are the old one-line form ("Return exactly one line: PASS or
  FLAG"), and `state.json` shows `failure_reason: tier-two implementation-acceptance panel
  FLAG`. The five tier-one unit reviewers, run under the same old contract, all returned
  `PASS`.
- Because the old orchestrator does not memoize, re-running would have rebuilt and
  re-reviewed every unit and produced the same content-free `FLAG`s — the ~10-run / ~3h loop
  010 exists to end. The operator declined that rerun and delegated the acceptance judgment.

## legible re-judgment, by lens

The five bare `FLAG`s were made legible by reading the built worktree against the signed
frame with rationale and evidence — the door-cure "legibility probe" prototyped on 009. The
build's own new proof floor (`./check.sh`, 745 `ok`, green) was treated as primary evidence,
together with a direct read of the door-integrity code in `adapter/loop.sh`.

- **whole-acceptance-conformance — PASS.** Every clause of the signed acceptance and
  observable-acceptance conditions is met: structured acceptance with verdict + rationale +
  evidence (`adapter/loop.sh` tier-one/tier-two prompts), real archive rejects fake and
  dry-run sources, reviewers stay on the strong floor, builders route separately with a
  three-attempt fast budget then strong escalation, unchanged accepted units are reusable on
  rerun, tier-two lenses start concurrently, the phase-one review crash path preserves
  diagnostics, stale lens reuse is guarded, and the contract is carried in `hypercore.md` and
  the gate prompts. The excluded interpretation holds: uncertainty still flags and any
  required `FLAG` still blocks archive.
- **proof-integrity — PASS.** Each unit obligation is backed by named self-tests that
  *exercise* the loop, not greps: three-attempt retry then strong escalation, cache skip and
  downstream invalidation, real-run fake-source rejection. No dry-run or stale evidence
  underpins a proof claim; `PERFORMANCE-FINDINGS.md` is absent and `check.sh` now asserts its
  absence.
- **independent-coherence — PASS.** The folded statements extend rather than contradict
  current intent: legibility strengthens the existing "unresolved `FLAG`s block and surface"
  statement; routing keeps reviewers strong, consistent with "do not cheapen reviewers";
  `hypercore.md` already carries the concurrent-panel and rationale+evidence prose.
- **security-permissions — PASS.** Acceptance reviewers run `-a never -s read-only` under a
  bounded `timeout`; operator-gate claims are unchanged. The 009-deferred
  `HYPERCORE_ACCEPTANCE_FAKE_DIR` fabrication hole is now *closed* in real runs — execute
  `die`s on a fake dir outside dry-run, and archive accepts only `source: real-reviewer`.
- **red-team — PASS, with one surfaced note.** Bypass routes were checked and are blocked:
  fake/dry-run acceptance (rejected at execute and archive), stale lens text (5×4 guard
  matrix), cache reuse across a changed unit (key folds frame + proof obligation + prior-unit
  state + impl version + diff + green check, with downstream invalidation), and retry used to
  self-clear a required `FLAG` (retry is build-attempt-only; an exhausted budget still stops
  for the operator).

## surfaced settlement, not a defect

The signed route's prose named `gpt-5.3-codex-spark` as the *default* builder. The build
instead holds the fast-builder default at the strong model (`gpt-5.5`), keeping only the
routing knobs (`CODEX_BUILDER_MODEL` / `CODEX_STRONG_BUILDER_MODEL`) live. This is a
deliberate, more-conservative settlement: it is permitted by the route's own "may use … when
available" hedge and the direction's delegation of routing detail to the machine, it violates
no proof-floor constraint (reviewers stay strong; "fast routing only for builders" only caps
how cheap things may get), and it aligns with the separate two-step-build decision to never
let a node be built by the spark model until a strong plan step lands. The folded `loop`
statement therefore describes the true held-at-strong default, and `check.sh` asserts it.

## honest limits of this record

- The on-disk `phase-two/tier-two-panel/*.md` artifacts still carry their original bare
  `FLAG` verdicts from the old orchestrator. They are *superseded* by this legible
  re-judgment, not cleared by a fresh clean panel run.
- The recorded unit diffs, handoffs, and tier-one verdicts describe the signed build, which
  is current in the worktree. No remediation edits were needed on top of the build (unlike
  009); `./check.sh` is green on the adopted tree.
- This is not a clean phase-two acceptance record and is not precedent for later work. The
  durable fix is this very loop: future one-way work run through the *new* `loop.sh` gets a
  legible, memoized, concurrent panel and should pass or fail itself on the record.

## manual archive action

Fold the signed 010 route into current intent — the `collaboration`, `loop`, and `adapter`
segments and their machine statements — for structured/legible acceptance, acceptance source
markers with fake-source rejection, separate builder/reviewer routing with bounded retry and
strong escalation, resumable execute, and the concurrent tier-two panel; keep the segment
feet stamped `qqp-dev` (the 010 signer); add `check.sh` coverage that the three segments
carry the new contract; then record this work under adopted history. The 010 material
(`adapter/loop.sh`, `check.sh`, `hypercore.md`, `adapter/codex.md`, `adapter/gates/*`) and the
removal of `PERFORMANCE-FINDINGS.md` were built in place during phase two and are already
current.
