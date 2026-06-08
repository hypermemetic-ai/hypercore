# phase-two unit - unit-003

unit: unit-003
status: accepted
updated-at: 2026-06-08T04:18:21Z
proof-obligation: Make the resumable cache non-fatal. In `adapter/loop.sh`, a failure at the per-unit cache-record step logs and degrades to a soft miss (the unit rebuilds next run); it never aborts phase two and never changes a correctness outcome. Record the non-fatality in the `loop` and `adapter` intent and machine statements, and add a `check.sh` self-test proving a poisoned or failing cache-record step yields a soft miss and the run proceeds (no fatal exit), through the existing dry-run / fake-dir self-test surface. `./check.sh` is green at the unit boundary.
handoff-path: 012-self-applied-phase-two/intent/frame/phase-two/handoffs/unit-003.md
diff-path: 012-self-applied-phase-two/intent/frame/phase-two/diffs/unit-003.diff
tier-one-verdict-path: 012-self-applied-phase-two/intent/frame/phase-two/tier-one/unit-003.md
cache-key-path: 012-self-applied-phase-two/intent/frame/phase-two/cache/unit-003.key
message: check.sh green; tier-one PASS; fast builder attempt 1; tier-one PASS; cache-key 
