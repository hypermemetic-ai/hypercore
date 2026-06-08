# phase-two unit - unit-005

unit: unit-005
status: accepted
updated-at: 2026-06-08T07:25:35Z
proof-obligation: Flip the default builder to spark and flip "held until two-step lands" to "shipped." Change the CODEX_BUILDER_MODEL default in adapter/loop.sh from gpt-5.5 to gpt-5.3-codex-spark, update the header comment and the two-step note, and update intent/loop.md, intent/machine-statements/loop.md, intent/adapter.md, intent/machine-statements/adapter.md, adapter/codex.md, and adapter/claude.md so every "builder held at the strong model until two-step lands" clause becomes "two-step has shipped; the default builder is the cheap fast model behind the plan step and plan-match check." Proof: check.sh asserts the builder default token is gpt-5.3-codex-spark and that no "held until two-step lands" clause remains.
handoff-path: 013-two-step-build/intent/frame/phase-two/handoffs/unit-005.md
diff-path: 013-two-step-build/intent/frame/phase-two/diffs/unit-005.diff
tier-one-verdict-path: 013-two-step-build/intent/frame/phase-two/tier-one/unit-005.md
message: check.sh green; tier-one PASS; fast builder attempt 1; tier-one PASS
