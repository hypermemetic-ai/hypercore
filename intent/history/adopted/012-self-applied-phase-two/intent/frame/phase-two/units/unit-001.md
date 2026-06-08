# phase-two unit - unit-001

unit: unit-001
status: accepted
updated-at: 2026-06-08T04:00:39Z
proof-obligation: Add orchestrator self-edit safety. Make `adapter/loop.sh` run phase two from an immutable snapshot of itself (re-exec from a copy at execute start) so a unit that edits `loop.sh` mid-run cannot corrupt the live orchestrator. Record it in the `loop` and `adapter` intent and machine statements, and add a self-test proving a mid-run `loop.sh` edit does not corrupt the active run. `./check.sh` is green at the unit boundary. (First so no later unit edits `loop.sh` before the safety exists; 012's own bootstrap run is launched from a manual snapshot by the supervisor.)
handoff-path: 012-self-applied-phase-two/intent/frame/phase-two/handoffs/unit-001.md
diff-path: 012-self-applied-phase-two/intent/frame/phase-two/diffs/unit-001.diff
tier-one-verdict-path: 012-self-applied-phase-two/intent/frame/phase-two/tier-one/unit-001.md
cache-key-path: 012-self-applied-phase-two/intent/frame/phase-two/cache/unit-001.key
message: check.sh green; tier-one PASS; fast builder attempt 1; tier-one PASS; cache-key 
