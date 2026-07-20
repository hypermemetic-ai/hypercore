---
id: doc-68
title: Terminal-native plan/review loop — best option (2026-07-19)
type: other
created_date: '2026-07-19 23:29'
updated_date: '2026-07-19 23:30'
tags:
  - research
---
# Terminal-native plan/review loop — best option (2026-07-19)

**Owning task:** T-93. **Research date:** 2026-07-19 (fresh read-only researcher; owning-agent spot-checks same day).
**Context:** operator constraint added after doc-65 — the whole human-in-the-loop plan loop must run **in the terminal** (no browser/IDE/hosted service); polish weighted first because these are the highest-value human-judgment moments; grilling declared in scope for ditching.
**Overall confidence:** HIGH on capability/integration facts (source-verified + spot-checked); MEDIUM on polish ranking; LOW on exact 0.80.10 runtime for uninstalled packages.
**Settles:** Is revdiff the best terminal option (qualified yes — review layer only); no shipped tool or pair completes the loop (composition required); plannotator confirmed browser-only; grilling cannot be retired wholesale. Adoption disposition belongs to the operator; this document is evidence, not authorization.

## Owning-agent verification (2026-07-19)

Spot-checked load-bearing citations:

- revdiff `--compare-old/--compare-new` two-file plan comparison via `git diff --no-index`: VERIFIED in upstream README.
- revdiff Pi launch = **direct terminal handoff** (pi suspends its TUI, revdiff takes over, pi resumes on exit): VERIFIED in plugins/pi/README.md. Herdr-tab launcher exists but is the Claude Code path, NOT the pi path.
- Independent daily-use report (Ylan Segal, revdiff for diffs and non-versioned plans "many times per day"): VERIFIED.
- `pi-hunk` 0.8.0 (2026-07-14) and `pi-openplan` 1.7.0 exist on npm as described: VERIFIED.
- slopchop annotates only added/deleted diff lines (file/whole-change notes otherwise) — unfit for arbitrary plan markup: VERIFIED in installed README.
- pi-plan-mode was **DROPPED by operator ledger in T-107** (2026-07-19, "T-101 stays dead"): VERIFIED in backlog/completed. Re-adoption would reverse a settled disposition and is the operator's call, not a recommendation this report smuggles in.
- Plannotator has no terminal/TUI mode (browser-only): round-1 + round-2 researchers both found none; consistent with its documented local-HTTP-server flow.

## Findings (researcher report, reconciled)

### Verdict: COMPOSITION-REQUIRED

No terminal tool or unmodified pair completes the loop (read-only exploration → exact annotation → structured feedback → plan-version diff → approval → full tools). Phase controllers lack annotation; reviewers lack phase control and a reliable gate.

**Loop-coverage matrix** (✓ native, △ partial/manual, ✗ absent):

| Candidate | 1 read-only phase | 2 annotation | 3 return to pi | 4 version diff | 5 approval gate | code diffs |
|---|---|---|---|---|---|---|
| revdiff (pi pkg) | ✗ | ✓ | ✓ | △ manual snapshots | ✗ (exit-0 ambiguity) | ✓ |
| @narumitw/pi-plan-mode | ✓ fail-closed | ✗ | △ conversational | ✗ | ✓ | ✗ |
| pi-openplan + revdiff | ✓ | ✓ | △ unverified handoff | △ glue | ✓ | ✓ |
| Hunk + pi-hunk | ✗ | ✓ in diffs | △ plan; ✓ code | △ snapshots | △ plan; ✓ code checkpoint | ✓ |
| Crit / tuicr | ✗ | ✓ | △ no pi bridge | ✗ | ✗ | ✓ |
| pi-slopchop (incumbent) | ✗ | △ diff lines only | ✓ staged in editor | ✗ | ✗ | ✓ |
| plannotator | ✓ | browser-only — DISQUALIFIED | | | | |

### revdiff — best terminal REVIEW layer (qualified yes)

First-class plan review: `--only plan.md` context-only mode with markdown TOC navigation, line/range/whole-file annotations, structured markdown output; `--compare-old/--compare-new` gives plan-version diffs as a primitive (qq preserves snapshots); `--stdin` sniffs unified diffs. Pi package: `/revdiff` + `revdiff_review` tool, direct terminal handoff, review-loop skill. Maintenance strong: 403 commits, extensive Go tests, v1.11.1 (2026-07-13), MIT, 693 stars. Peer range ^0.74.0 (covers 0.80.10; no exact smoke). **Strongest case against:** young; blocking handoff; history is a recovery log, not version timeline; approval not fail-closed — exit 0 conflates clean approval and discarded review, so it cannot be the sole implementation gate. [HIGH]

### Phase-control candidates

- **pi-plan-mode** (0.20.0, requires ≥0.80.6): the strongest phase/questions component — fail-closed bash allowlist, edit/write/update_plan blocked, extension tools off by default, `plan_mode_question` (1–3 questions, options + free-form Other — the best terminal question widget found), session-stored plans, `/plan implement`. **But:** plans are session objects (no file artifact → poor revdiff composition), no annotation, no version diff; no independent sustained-use report; and it was DROPPED in T-107 today. [HIGH]
- **pi-openplan** (1.7.0, days old): file-backed plans under `.pi/plans/`, structured questions, prior content preserved on replacement, explicit `/execute_plan` — the cleanest artifact shape for composition. No use record; handoff untested. Prototype pair, not adoption candidate. [MEDIUM]

### Polish challenger: Hunk + pi-hunk

Best raw review UX found: adaptive split/stack, watch mode (`hunk diff plan-v1.md plan-v2.md --watch`), mouse+keyboard, session API, designed to stay open in a second terminal — maps naturally onto a dedicated Herdr pane (better topology than revdiff's blocking handoff). pi-hunk adds explicit review semantics: ready/review/re-review/approved states, submitted-empty-review = approval (solves revdiff's ambiguity), freshness reported as unknown rather than invented. Independent polish reports exist (r/git, r/PiCodingAgent). **Against:** pi-hunk is days old, no exact 0.80.10 evidence, direct-file PLAN mapping through the pi bridge unverified (documented path is git working-tree checkpoints). [HIGH facts / MEDIUM ranking]

### grilling (convergent with owning-agent decomposition)

Tool can subsume ONLY the presentation layer: question widgets replace question rendering; plan approval replaces the one approval question; a phase package upgrades the enactment gate from prose policy to by-construction enforcement. Tool CANNOT: decide which decisions are consequential, cite evidence, keep dispositions scoped, record Backlog decision records, own realignment on scope change. **Do not retire grilling; slim only duplicated mechanics** (choice rendering, question batching) if a phase package is adopted. deliver-change's ledger binding is untouched. [HIGH — researcher and owning agent reached this independently]

## Recommendation shape (disposition belongs to operator)

Adopt nothing new yet. Bounded trial ticket: revdiff vs Hunk on one identical corpus — a markdown plan, a revised plan (version-diff check), and an implementation diff — on pi 0.80.10 under Herdr. Trial must answer: revdiff approve-vs-discard handling, hunk direct-file plan annotation via pi-hunk, handoff/topology feel (blocking takeover vs second pane), annotation ergonomics (the polish criterion), and coexistence with rpiv-todo + guards. Optional second axis, only if the operator wants to revisit T-110: winner vs slopchop on code diffs (one annotation surface total). Phase-control slot: trial pi-openplan as the file-backed candidate, or a thin qq-owned bridge extension; re-opening pi-plan-mode is a T-107 reversal — operator's explicit call only. Plan artifacts stay out of `backlog/` (guard-verified constraint); `.pi/plans/` is the natural home.

## Sources

- [revdiff](https://github.com/umputun/revdiff) + [pi integration source](https://github.com/umputun/revdiff/blob/master/plugins/pi/extensions/revdiff.ts) (spot-checked)
- [Ylan Segal use report](https://ylan.segal-family.com/blog/2026/06/16/how-i-review-my-agents-code/) (spot-checked)
- [Hunk](https://github.com/modem-dev/hunk), [pi-hunk](https://pi.dev/packages/%40roodriigoooo/pi-hunk), [pi-openplan](https://pi.dev/packages/pi-openplan) (spot-checked manifests)
- [@narumitw/pi-plan-mode](https://pi.dev/packages/%40narumitw/pi-plan-mode), [Crit](https://github.com/kevindutra/crit), [tuicr](https://github.com/agavra/tuicr/blob/main/docs/REVIEW_CLI.md), [pi-diff-review](https://pi.dev/packages/pi-diff-review), [tuicr HN report](https://news.ycombinator.com/item?id=48090276), [hunk user discussion](https://www.reddit.com/r/git/comments/1twe88o/a_small_browser_diff_viewer_for_local_gitjj/), [pi-hunk discussion](https://www.reddit.com/r/PiCodingAgent/comments/1ugcakb/extension_for_cleaner_and_customizable_diffs_and/)
- Internal: T-107 (completed; pi-plan-mode DROP), T-110 (slopchop incumbent), doc-65, skills/grilling/SKILL.md, cockpit/pi/qq-backlog-guard.ts

## Gaps

- Nothing was installed or run; exact 0.80.10 behavior verified only for incumbent slopchop.
- No controlled measurement of review speed/quality across candidates (none exists anywhere).
- Hunk plan-review-via-pi bridge unverified; pi-openplan days old with no use record.
- Ecosystem moving daily; several releases were <1 week old at research time.
