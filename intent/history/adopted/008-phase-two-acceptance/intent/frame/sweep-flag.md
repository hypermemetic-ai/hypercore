# sweep flag - 008-phase-two-acceptance

Phase two implemented the Full Funnel adapter/check material and `./check.sh` exited
zero. The check gate then reported the built corpus as coherent in prose, including that
the remaining parent-intent mismatch was an archive obligation named by the signed frame.

Archive did not run because the outer `loop.sh execute` process was the pre-008
orchestrator. It still required a final `SWEEP_VERDICT: COHERENT` sentinel from the check
gate. The implement unit had already changed `adapter/gates/check.md` to the new
implementation-acceptance contract, whose output no longer carries the old sweep
sentinel. The check gate returned coherent prose but no sentinel, so the pre-008
orchestrator halted with "no readable sweep verdict" and left this work active.

This is a harness-transition stop, not a reported semantic incoherence. Operator
resolution is needed before archive resumes.
