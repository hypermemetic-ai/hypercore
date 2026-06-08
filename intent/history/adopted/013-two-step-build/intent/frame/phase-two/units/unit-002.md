# phase-two unit - unit-002

unit: unit-002
status: accepted
updated-at: 2026-06-08T06:57:31Z
proof-obligation: Plan-matches-frame check gating each plan. Add a dedicated independent strong read-only plan-faithfulness reviewer that checks each plan against the signed frame and returns a structured PASS or FLAG; execute requires a clean plan-match result before that unit's build is trusted, and an unresolved plan-match FLAG blocks the unit. Add the loop and adapter statements. Proof: check.sh asserts the plan-match check is required per unit and that a missing or failed plan-match blocks the build.
handoff-path: 013-two-step-build/intent/frame/phase-two/handoffs/unit-002.md
diff-path: 013-two-step-build/intent/frame/phase-two/diffs/unit-002.diff
tier-one-verdict-path: 013-two-step-build/intent/frame/phase-two/tier-one/unit-002.md
message: check.sh green; tier-one PASS; fast builder attempt 2; tier-one PASS
