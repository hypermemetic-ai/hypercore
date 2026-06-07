# handoff - unit-002

unit: unit-002

proof obligation: Phase-one review crash and lens-specific proof: fix or harden the phase-one review subprocess path that produced exit-1 base-roster flags, preserve diagnostic output in `review.md`, keep optional reviewers advisory, and prove each tier-two panel lens uses its own live instruction rather than stale copied text.

builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260607T210404Z-root-010-phase-two-performance-pid3746987/gates/implement-unit-002.final.md

## builder final output

Implemented unit-002.

Changed files:
- [adapter/loop.sh](/home/qqp/projects/hypercore/adapter/loop.sh)
- [check.sh](/home/qqp/projects/hypercore/check.sh)
- [unit-002.md](/home/qqp/projects/hypercore/010-phase-two-performance/intent/frame/phase-two/units/unit-002.md)
- [unit-002 handoff](/home/qqp/projects/hypercore/010-phase-two-performance/intent/frame/phase-two/handoffs/unit-002.md)
- [unit-002 diff](/home/qqp/projects/hypercore/010-phase-two-performance/intent/frame/phase-two/diffs/unit-002.diff)

What changed: phase-one review now preserves subprocess status and captured diagnostic output in `review.md`; optional reviewer flags stay advisory. Tier-two panel proof now checks all five lenses for their own live instruction and rejects stale copied lens text.

Checks prepared and run:
- `bash -n adapter/loop.sh`
- `bash -n check.sh`
- `git diff --check -- adapter/loop.sh check.sh`
- `./check.sh` green

Proof gap: none known for this unit.
