# manual-archive - 013-two-step-build

Operator-authorized manual adoption past a tier-two panel FLAG, on the established
012 precedent. Recorded 2026-06-08.

## what ran

Phase two built all five signed units. Tier-one: every unit PASS with `source: real-reviewer`,
`dry-run: no`; only units 001 and 002 needed a fast-builder retry (001 a flaky
untracked-file evidence FLAG, 002 a real resume-coherence FLAG that fast-2 reconciled); zero
strong-builder escalations. `./check.sh` green (966 checks) at every unit boundary and at
adoption.

## why the tier-two panel FLAGged (all 5 lenses)

One structural cause plus one fixable defect — neither is a code-correctness failure:

1. **Bootstrap gap (structural).** The signed frame requires each unit to produce a `plan`
   and a `plan-match` artifact before its build is trusted. This run produced none: `execute`
   re-execs from an immutable snapshot of `loop.sh` taken at launch — the *pre*-two-step loop,
   which has no plan step. The plan step is exactly what 013 builds, so the run that builds it
   cannot run it. You cannot exercise the two-step pipeline on the run that creates it. The
   machinery is nonetheless proven: `check.sh` self-tests the ordering via
   `loop.sh execute --dry-run` ("missing plan-match blocks before the builder", "plan-match
   FLAG blocks before the builder") — the dry-run demonstration the frame's *observable
   acceptance* actually names.
2. **Adapter resume coherence defect — FIXED.** The build updated the `loop` segment's resume
   rule to "plan-match **and** tier-one PASS" but left the `adapter` segment's mirrors
   ("tier-one PASS" only) at `intent/adapter.md`, `intent/machine-statements/adapter.md` (×2),
   `adapter/codex.md`, `adapter/gates/implement.md`. The panel correctly caught this. Fixed
   post-build (all five now read "plan-match and tier-one"); `check.sh` green after the fix.

The operator was shown this full diagnosis and chose informed one-way adoption.

## debts carried (not blockers — recorded for follow-up)

- **D1 — two-step is unproven in a real run.** Node 014 (the next real work node) is the first
  to actually run plan -> plan-match -> (spark) build end-to-end. Watch its first run closely;
  spark-as-builder remains untested in production. Until 014 runs clean, two-step is proven
  only by `check.sh` dry-run self-tests, not by a real build.
- **D2 — check gap.** No `check.sh` assertion enforces that the adapter-segment resume wording
  mentions plan-match (the coherence the panel caught by reading, not by a check). Add one so
  it cannot regress.
- **D3 — proof record excludes untracked/new files.** `write_current_diff_record` is
  tracked-only (`git diff` + `--untracked-files=no`), so a unit that *adds* a file is invisible
  in its own diff record, making tier-one flaky on file-adding units (the unit-001 FLAG->PASS).
  Fix: capture untracked/new files in the diff record, or stage builder-created files before
  recording.
- **D4 — acceptance-artifact bloat.** Phase-one `review.md` (~269KB) and tier-two lens files
  embed full reviewer transcripts. Consider trimming embedded diagnostics.

## adoption

Adopted delta is already applied in place across the `loop` and `adapter` segments,
`adapter/loop.sh`, `adapter/gates/{plan,implement}.md`, `adapter/codex.md`, and `check.sh`:
the per-unit strong-model plan step + readable plan artifact, the dedicated plan-match check
gating each build, confirmed-non-decomposable units routing to the strong builder, the
short-but-judgeable frame altitude rule, and the builder default flipped to
`gpt-5.3-codex-spark`. `loop` and `adapter` segment feet remain `endorsed by qqp-dev`.
