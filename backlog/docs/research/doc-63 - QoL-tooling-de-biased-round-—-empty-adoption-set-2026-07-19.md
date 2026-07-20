---
id: doc-63
title: QoL/tooling de-biased round — empty adoption set (2026-07-19)
type: other
created_date: '2026-07-19 18:21'
updated_date: '2026-07-19 18:21'
tags:
  - research
---
# QoL/tooling research (de-biased round 2) — empty adoption set

**Owning tasks:** T-101, T-102, T-103. **Research date:** 2026-07-19 (fresh researcher, anti-bias brief).
**Overall confidence:** HIGH in the empty adoption list; MEDIUM in catalog exhaustiveness.
**Context:** commissioned after the operator distrusted sweep-era findings (doc-54–60) and round 1 (doc-61). Brief design: no prior candidates or verdicts supplied; adoption grounds restricted to measured outcomes and specific independent user reports; maintainer claims, popularity, and prompt-text quality excluded; strongest-case-against required per candidate; empty list declared a successful outcome.

## Settles

**Adoption-qualified set: `[]`.** No candidate in any of the three need classes met both binding gates: (1) measured outcomes or a specific independent user report demonstrating improvement for a qq-like user, and (2) explicitly verified Pi 0.80.10 compatibility. This is not evidence the packages are ineffective — it means adoption would require relaxing the evidence or compatibility gates.

Closest candidates fail on opposite sides: `pi-agent-goal` has explicit 0.80.10 release smoke validation but no outcome evidence; `@ff-labs/pi-fff` has real performance evidence (500k-file Chromium tree: 3–9s per ripgrep spawn vs sub-10ms warm queries, author-measured) plus a month-in-use independent report, but no exact-0.80.10 validation and no agent-task outcome comparison.

## Per-need verdicts

| Need (ticket) | Verdict |
|---|---|
| Terminal planning surface (T-101) | `pi-plan-mode`: excellent functional fit, but release ~1 day old, no use record, no exact-0.80.10 smoke found → **UNPROVEN, no adoption** |
| Structural code index (T-102) | No candidate ran a comparative architecture/dependency/route/impact corpus against the incumbent graph; `pi-tree-sitter` has benchmarks but not for the required comparison → **no adoption-qualified challenger** |
| Session QoL (T-103) | checklists: `rpiv-todo` UNPROVEN, `pi-tasks` hard-reject (foreign lifecycle); goals: `pi-agent-goal` exact-compatible but UNPROVEN; PR diagnostics: both UNPROVEN; intercom: strong fit, UNPROVEN, `pi-messenger` hard-reject (foreign hierarchy); file browsing: `pi-files-widget` UNPROVEN; search: `pi-fff` strongest evidence-positive lead, gate unmet; statusline: both UNPROVEN |

**Structural note for disposition:** this round evaluated *adoption* against pre-existing evidence. Trial-shaped tickets are evidence-generating — the round's empty set means no trial can be skipped on the strength of published evidence, not that trials would fail. Disposition per ticket belongs to the operator.

**Researcher gap of note:** T-102's sweep-named challenger was not among round 2's discovered candidates (the anti-anchoring brief supplied no names); its pilot remains the only direct evidence path for that specific package.

## Sources

Package pages/manifests and independent reports cited in the raw findings (reconciled here): pi.dev catalog pages for pi-plan-mode, pi-tree-sitter, pi-impact-analyzer, pi-shazam, pi-codeintel, pi-cymbal, rpiv-todo, pi-tasks, pi-agent-goal, pi-goal, pi-pr-status, pi-github-pr, pi-intercom, pi-messenger, pi-files-widget, pi-slopchop, pi-fff, pi-status, pi-statusline; [FFF repository measurements](https://github.com/dmtrKovalenko/fff); independent reports via linux.do and answeroverflow. Owning-agent spot-checks 2026-07-19: pi-agent-goal 0.80.10 smoke-validation references verified on its package page; FFF Chromium benchmark verified in its README.

## Gaps

- Catalog exhaustiveness MEDIUM (~5,300 packages, fast-moving).
- No candidate was installed; compatibility claims are as-published.
- Round 2 did not assess the specific T-102 challenger by name.
