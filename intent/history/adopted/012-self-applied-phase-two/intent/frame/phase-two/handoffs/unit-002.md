# handoff - unit-002

unit: unit-002

proof obligation: Relocate the inline gate prompts into the re-read gate files, reconcile them, and make the bounded `active-work` clarification. Move the contract-bearing implement and archive prompt text out of the inline strings in `adapter/loop.sh` (`run_unit_build_attempt`, `cmd_execute`) into `adapter/gates/implement.md` and `adapter/gates/archive.md`, which `run_gate` re-reads per invocation via `cat`, leaving only dynamic per-unit data (unit id, proof obligation, decision line) inline — so a loop-self-change's prompt edits take effect mid-run and the inline bootstrap floor is gone. Reconcile while moving: the implement gate permits a unit to edit intent when the unit's own proof is a check over that intent (removing the blanket "do not edit the intent documents" prohibition that contradicts `intent/loop.md`'s vertical-slice statement); the archive gate adopts — verifies the applied delta against the signed frame, stamps each touched segment foot, and records history — rather than requiring a separate content-fold of intent the units already applied. Clarify in `intent/active-work.md` that intent a signed work node applies in place during phase two is in-flight, not adopted; adoption is the act that stamps the operator's endorsement and records history, making the change adopted-current, and "the parent intent remains current until adoption" governs adopted truth, consistent with the loop's existing in-flight-vs-adopted concurrency reading. Update the `loop` and `adapter` intent and machine statements to match, and add `check.sh` assertions encoding (a) the reconciled contract and (b) that no contract-bearing implement/archive prompt remains frozen inline in `loop.sh` — so neither the self-contradiction nor the inline floor can silently return. `./check.sh` is green at the unit boundary.

builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260608T035103Z-root-012-self-applied-phase-two-pid1848209/gates/implement-unit-002-fast-1.final.md

## builder final output

Implemented `unit-002` and left the unit boundary green.

Changed files:
- [adapter/loop.sh](/home/qqp/projects/hypercore/adapter/loop.sh)
- [adapter/gates/implement.md](/home/qqp/projects/hypercore/adapter/gates/implement.md)
- [adapter/gates/archive.md](/home/qqp/projects/hypercore/adapter/gates/archive.md)
- [check.sh](/home/qqp/projects/hypercore/check.sh)
- [intent/active-work.md](/home/qqp/projects/hypercore/intent/active-work.md)
- [intent/loop.md](/home/qqp/projects/hypercore/intent/loop.md)
- [intent/machine-statements/loop.md](/home/qqp/projects/hypercore/intent/machine-statements/loop.md)
- [intent/adapter.md](/home/qqp/projects/hypercore/intent/adapter.md)
- [intent/machine-statements/adapter.md](/home/qqp/projects/hypercore/intent/machine-statements/adapter.md)
- [unit-002.diff](/home/qqp/projects/hypercore/012-self-applied-phase-two/intent/frame/phase-two/diffs/unit-002.diff)
- [unit-002.md handoff](/home/qqp/projects/hypercore/012-self-applied-phase-two/intent/frame/phase-two/handoffs/unit-002.md)

Prepared checks, all passing:
- `bash -n adapter/loop.sh`
- `bash -n check.sh`
- `./check.sh`

Proof gap: none for this unit.
