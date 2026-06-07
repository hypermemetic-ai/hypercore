# handoff - unit-003

unit: unit-003

proof obligation: Role routing and builder retry/escalation: add separate builder and reviewer model knobs/defaults, route only builders to `gpt-5.3-codex-spark` by default when available, keep all reviews strong, and implement the per-unit fast-builder three-attempt budget followed by strong-builder escalation and operator stop on strong failure; add focused self-tests using deterministic fake builders/reviewers rather than external model availability.

builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260607T210404Z-root-010-phase-two-performance-pid3746987/gates/implement-unit-003.final.md

## builder final output

Implemented unit-003 and recorded its handoff/diff under the signed frame.

Changed files for this unit:
- [adapter/loop.sh](/home/qqp/projects/hypercore/adapter/loop.sh)
- [check.sh](/home/qqp/projects/hypercore/check.sh)
- [unit-003.md](/home/qqp/projects/hypercore/010-phase-two-performance/intent/frame/phase-two/units/unit-003.md)
- [unit-003 handoff](/home/qqp/projects/hypercore/010-phase-two-performance/intent/frame/phase-two/handoffs/unit-003.md)
- [unit-003 diff](/home/qqp/projects/hypercore/010-phase-two-performance/intent/frame/phase-two/diffs/unit-003.diff)

Checks prepared and run:
- `bash -n adapter/loop.sh`
- `bash -n check.sh`
- `git diff --check -- adapter/loop.sh check.sh 010-phase-two-performance/intent/frame/phase-two/units/unit-003.md 010-phase-two-performance/intent/frame/phase-two/handoffs/unit-003.md 010-phase-two-performance/intent/frame/phase-two/diffs/unit-003.diff`
- `./check.sh` green

Proof gap: none known for this unit.
