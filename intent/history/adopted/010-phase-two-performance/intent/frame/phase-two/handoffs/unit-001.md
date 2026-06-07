# handoff - unit-001

unit: unit-001

proof obligation: Acceptance legibility and fake-source hardening: update acceptance verdict parsing, tier-one and tier-two prompts, acceptance artifact writing, source markers, and archive validation so required acceptance carries verdict, rationale, evidence, and real-source proof while fake/self-test artifacts are impossible to use for real adoption; add `./check.sh` coverage for structured PASS/FLAG, evidence requirements, malformed output, dry-run behavior, and real-run fake-source rejection.

builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260607T210404Z-root-010-phase-two-performance-pid3746987/gates/implement-unit-001.final.md

## builder final output

Implemented unit-001.

Changed files:
- [adapter/loop.sh](/home/qqp/projects/hypercore/adapter/loop.sh)
- [adapter/gates/check.md](/home/qqp/projects/hypercore/adapter/gates/check.md)
- [adapter/gates/archive.md](/home/qqp/projects/hypercore/adapter/gates/archive.md)
- [check.sh](/home/qqp/projects/hypercore/check.sh)
- [unit-001.md](/home/qqp/projects/hypercore/010-phase-two-performance/intent/frame/phase-two/units/unit-001.md)
- [unit-001 handoff](/home/qqp/projects/hypercore/010-phase-two-performance/intent/frame/phase-two/handoffs/unit-001.md)
- [unit-001 diff](/home/qqp/projects/hypercore/010-phase-two-performance/intent/frame/phase-two/diffs/unit-001.diff)

What changed: acceptance now requires structured `VERDICT`, `RATIONALE`, and `EVIDENCE`; malformed or evidence-free output flags. Acceptance artifacts now carry `source`, `source-proof`, rationale, and evidence. Real execute rejects `HYPERCORE_ACCEPTANCE_FAKE_DIR`, and real archive validation requires `source: real-reviewer`.

Checks prepared and run:
- `bash -n adapter/loop.sh && bash -n check.sh`
- `git diff --check -- adapter/loop.sh adapter/gates/check.md adapter/gates/archive.md check.sh`
- `./check.sh` green

Proof gap: none known for this implementation unit.
