---
id: doc-91
title: Plan — qq ecosystem update assessment prompt and first cycle
type: specification
created_date: '2026-07-24 14:29'
updated_date: '2026-07-24 16:35'
---
# Plan — qq ecosystem update assessment prompt and first cycle

**Owning Task:** T-156
**Approved:** 2026-07-24, in the operator-facing accountable session

## Intended outcome

Create a source-controlled project prompt at `.pi/prompts/update.md`, registered as `/update`, that makes a complete, evidence-based assessment of available updates across qq's integrated runtime ecosystem. Run it once for the current state and preserve the resulting decision-grade evidence.

## Ownership boundary

- This Change owns the prompt template, the minimum `.gitignore` exception needed to track it, and one cited current-cycle research report.
- The assessment inventories Pi core, every package reported by `pi list`, Herdr, each source-derived first-class externally versioned integration/runtime owner, and any otherwise commodity dependency implicated by a material compatibility, security, migration, overlap, or simplification edge. Generic prerequisites excluded from the matrix are disclosed with reasons.
- The assessment checks primary release notes or source, maps findings to current qq source and active intent, identifies capabilities, solved problems, simplification opportunities, overlap or territory convergence, compatibility and migration cost, and operational/security risk.
- Each component receives one explicit recommendation: update, hold, test, replace, remove, or no action.

## Non-goals

- Do not install or update any assessed package or runtime. Under decision-13, `/update` may create only the governance-required Task, Change, plan/research evidence, Checks, review, and pull-request handoff; it never merges.
- Do not change qq architecture, retire an extension, or implement an opportunity discovered by the assessment.
- Do not add an update daemon, registry, scheduler, or other persistent workflow machinery.

## Success evidence

1. A fresh Pi process discovers `/update` from the project prompt path and expands it successfully.
2. Prompt assertions demonstrate complete-inventory, primary-evidence, qq-impact, overlap/simplification/risk, explicit-recommendation, and non-mutation requirements.
3. The first run reconciles installed and available versions from live commands, verifies load-bearing claims from primary sources, and produces one confidence-tagged Backlog research report attached to T-156.
4. Repository-specific Checks and fresh-context review are green.

## Decision dispositions

- Project-local, source-controlled prompt: operator-approved recommendation in the 2026-07-24 alignment exchange.
- Source-derived whole-ecosystem inventory rather than notification-derived scope: same exchange.
- Assessment-only behavior; updates require separate approval: same exchange.
- First cycle and prompt share one Change, while adoption/removal work remains follow-up intent: same exchange.
- Standing authorization for each future cycle's durable assessment evidence lifecycle, but never for merge or assessed ecosystem mutation: decision-13.
