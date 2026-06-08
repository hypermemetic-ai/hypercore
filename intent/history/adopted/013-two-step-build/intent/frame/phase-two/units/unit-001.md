# phase-two unit - unit-001

unit: unit-001
status: accepted
updated-at: 2026-06-08T06:42:24Z
proof-obligation: Strong-model plan step plus a readable per-unit plan artifact. Add a planner model knob to adapter/loop.sh (defaulting to the strong model) and make execute run a strong-model plan sub-step at the head of each unit that writes a human-readable plan under the unit's phase-two tree before the build runs. Add the loop and adapter intent statements for the per-unit plan step and the readable plan artifact. Proof: check.sh asserts the planner knob exists and defaults to the strong model, the new statements are present, and a dry-run execute records a plan artifact before that unit's build artifact.
handoff-path: 013-two-step-build/intent/frame/phase-two/handoffs/unit-001.md
diff-path: 013-two-step-build/intent/frame/phase-two/diffs/unit-001.diff
tier-one-verdict-path: 013-two-step-build/intent/frame/phase-two/tier-one/unit-001.md
message: check.sh green; tier-one PASS; fast builder attempt 2; tier-one PASS
