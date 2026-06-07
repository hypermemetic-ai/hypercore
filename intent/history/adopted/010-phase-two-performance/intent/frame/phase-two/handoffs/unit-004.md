# handoff - unit-004

unit: unit-004

proof obligation: Resumable execute cache: add a signed-frame-derived per-unit cache key covering the frame, unit proof obligation, relevant prior-unit state, loop implementation version, diff/check evidence, and tier-one PASS; on rerun, skip unchanged accepted units, rebuild cache misses, and invalidate downstream units when prior state changes; prove skip and invalidation behavior in `./check.sh`.

builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260607T210404Z-root-010-phase-two-performance-pid3746987/gates/implement-unit-004.final.md

## builder final output

Implemented unit-004 and recorded its handoff/diff under the signed frame.

Changed files for this unit:
- [adapter/loop.sh](/home/qqp/projects/hypercore/adapter/loop.sh)
- [check.sh](/home/qqp/projects/hypercore/check.sh)
- [unit-004.md](/home/qqp/projects/hypercore/010-phase-two-performance/intent/frame/phase-two/units/unit-004.md)
- [unit-004 handoff](/home/qqp/projects/hypercore/010-phase-two-performance/intent/frame/phase-two/handoffs/unit-004.md)
- [unit-004 diff](/home/qqp/projects/hypercore/010-phase-two-performance/intent/frame/phase-two/diffs/unit-004.diff)

Checks prepared and run:
- `bash -n adapter/loop.sh`
- `bash -n check.sh`
- `git diff --check -- adapter/loop.sh check.sh`
- `./check.sh` green

Proof gap: none known for this unit.
