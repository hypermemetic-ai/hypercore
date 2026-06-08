# handoff - unit-005

unit: unit-005

proof obligation: Flip the default builder to spark and flip "held until two-step lands" to "shipped." Change the CODEX_BUILDER_MODEL default in adapter/loop.sh from gpt-5.5 to gpt-5.3-codex-spark, update the header comment and the two-step note, and update intent/loop.md, intent/machine-statements/loop.md, intent/adapter.md, intent/machine-statements/adapter.md, adapter/codex.md, and adapter/claude.md so every "builder held at the strong model until two-step lands" clause becomes "two-step has shipped; the default builder is the cheap fast model behind the plan step and plan-match check." Proof: check.sh asserts the builder default token is gpt-5.3-codex-spark and that no "held until two-step lands" clause remains.

builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260608T062609Z-root-013-two-step-build-pid3177438/gates/implement-unit-005-fast-1.final.md

## builder final output

Implemented unit-005.

Changed files: [adapter/loop.sh](/home/qqp/projects/hypercore/adapter/loop.sh), [check.sh](/home/qqp/projects/hypercore/check.sh), [intent/loop.md](/home/qqp/projects/hypercore/intent/loop.md), [intent/machine-statements/loop.md](/home/qqp/projects/hypercore/intent/machine-statements/loop.md), [intent/adapter.md](/home/qqp/projects/hypercore/intent/adapter.md), [intent/machine-statements/adapter.md](/home/qqp/projects/hypercore/intent/machine-statements/adapter.md), [adapter/codex.md](/home/qqp/projects/hypercore/adapter/codex.md), [adapter/claude.md](/home/qqp/projects/hypercore/adapter/claude.md).

Lean handoff state written to [unit-005.md](/home/qqp/projects/hypercore/013-two-step-build/intent/frame/phase-two/handoffs/unit-005.md), and the cumulative unit diff record to [unit-005.diff](/home/qqp/projects/hypercore/013-two-step-build/intent/frame/phase-two/diffs/unit-005.diff).

Prepared check: `./check.sh` exits 0. Proof gap: none for this unit.
