# manual archive - 012-self-applied-phase-two

Adopted manually on 2026-06-08, operator-authorized for this work node, following the precedent
of 008/009/010/011: a self-change that rewrites the loop's own orchestrator cannot fully
self-apply (the running `loop.sh` is frozen at launch), so the loop's automated archive does not
cleanly carry it. The build is sound and `./check.sh` is green; it was adopted by hand under
scrutiny equivalent to the loop's required acceptance, with the one residual gap recorded below.

## what happened

- **Phase two ran end-to-end autonomously** after a one-time hand-bootstrap. Because the
  orchestrator is parsed into memory at launch, 012's own run had to start with its own
  orchestrator-behaviour fixes pre-applied: the operator/Opus pre-applied (a) the implement/
  archive gate reconciliation (implement permits a unit to edit intent when its proof is a check
  over that intent; archive ratifies) in both the inline `loop.sh` prompts and the gate files,
  and (b) the cache-record non-fatality (cause 1). With those in place, `loop.sh execute` built
  all four units on the first fast-builder attempt each, tier-one PASS (real-source) for every
  unit, `check.sh` green at every boundary, and the resumable-cache transient (the 008-011 halt)
  was correctly soft-missed and the run continued — reaching the tier-two panel unattended. This
  is the autonomous self-applied phase two the node set out to deliver.
- **The four units, as adopted:**
  1. orchestrator self-edit safety — `loop.sh execute` re-execs phase two from an immutable
     snapshot of itself, so a unit editing `loop.sh` mid-run cannot corrupt the live run.
  2. relocate the inline implement/archive contract prompts into the re-read `adapter/gates/*.md`
     files + reconcile them (implement permits required intent edits; archive ratifies) + the
     bounded `active-work` in-flight-vs-adopted-current clarification. This removes the inline
     bootstrap floor so future loop-self-changes self-apply with no bootstrap.
  3. cache-record non-fatality — a failing/transient cache record becomes a soft miss and the
     run continues; the cache never halts phase two or changes a correctness outcome.
  4. handoff — `loop.sh execute` auto-detects the single signed unarchived node; adapter prose
     names the Opus->codex launch + supervise path and separates `start` from `execute`.
- **Tier-two panel (real-source, read-only, gpt-5.5):** `whole-acceptance-conformance` PASS,
  `proof-integrity` PASS, `security-permissions` PASS; `independent-coherence` and `red-team`
  FLAG. Raw lens outputs are preserved under `phase-two/tier-two-panel/`.

## the one residual gap (why the two FLAGs, and why adoption is still safe)

The signed observable acceptance required a dynamic self-test proving a mid-run gate-prompt-file
change is observed on the next gate invocation. The phase-two builder built only the static
"`run_gate` re-reads the gate file" assertions; the dynamic self-test was added afterward by a
targeted cleared builder directly into `check.sh` (an execute-driven fixture that appends a marker
to `adapter/gates/archive.md` after the implement gate and asserts the next gate sees it, then
restores the file). `whole-acceptance-conformance` re-judged PASS once the self-test existed.
`independent-coherence` and `red-team` still FLAG — **not on code correctness**, but on evidence
*provenance*: that self-test hunk has no matching per-unit diff / tier-one record, because it was
added outside the unit build. The code itself is sound (`check.sh` green; the three substantive
lenses PASS). The operator authorized manual adoption rather than spend a further clean re-run
purely to regenerate the tier-one trail for one already-passing test. The gap is provenance, not
defect.

## adoption

`./check.sh` green. The accepted delta is folded into the root intent in place: `intent/loop.md`,
`intent/machine-statements/loop.md`, `intent/adapter.md`, `intent/machine-statements/adapter.md`,
and `intent/active-work.md`; materialized in `adapter/loop.sh`, `adapter/gates/implement.md`,
`adapter/gates/archive.md`, `adapter/codex.md`, and `check.sh`. Touched segment feet
(`loop`, `adapter`, `active-work`) remain endorsed by qqp-dev (the signer).

## carried debts / loop-hardening for a future loop

- **The phase-two builder under-built a signed observable-acceptance item** (built static
  assertions, skipped the dynamic self-test the unit text did not explicitly enumerate). The
  unit proof text should enumerate every observable-acceptance artifact, or tier-one should check
  unit output against observable acceptance, so the panel is not the first place the gap appears.
- **A loop-self-change still needs a one-time hand-bootstrap** of its orchestrator-behaviour
  fixes (gate prompts + cache) because the running `loop.sh` is frozen at launch. 012 removes the
  *inline-prompt* floor (prompts now live in re-read gate files), so future prompt changes
  self-apply; a deeper fix would let the orchestrator re-exec from the updated snapshot to pick up
  its own non-prompt changes mid-run.
- **No clean granular re-run.** The loop has no panel-only / archive-only resume, and a
  soft-missed cache leaves no record to skip rebuilt units, so a targeted post-build fix cannot be
  re-accepted without either a full rebuild or hand-driving the panel. A resumable
  re-acceptance path would avoid the manual finish.
- The deep fold / intent-vs-material split remains deferred to the work-node-collapse loop.
