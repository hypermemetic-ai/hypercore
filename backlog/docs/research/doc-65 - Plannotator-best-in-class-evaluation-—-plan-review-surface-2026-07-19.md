---
id: doc-65
title: Plannotator best-in-class evaluation — plan-review surface (2026-07-19)
type: other
created_date: '2026-07-19 22:54'
updated_date: '2026-07-19 22:55'
tags:
  - research
---
# Plannotator best-in-class evaluation — plan-review surface (2026-07-19)

**Owning task:** T-93 (pi-ecosystem replacement sweep; this is a follow-up evaluation).
**Research date:** 2026-07-19. Fresh read-only researcher (qq-dispatch researcher), anti-duplication brief; owning-agent spot-checks same day.
**Overall confidence:** MEDIUM-HIGH on capability and integration facts (source-verifiable); MEDIUM on comparative ranking (young category, no independent benchmark).
**Settles:** Plannotator is best in class for qq's adoption target — a local-first visual plan-review gate composable with Pi. It replaces nothing qq owns; it fills the open plan-mode need (T-101 class) and collides with two surfaces settled earlier the same day (slopchop, rpiv-todo). Adoption disposition belongs to the operator; this document is evidence, not authorization.

## Owning-agent verification (2026-07-19)

Spot-checked load-bearing citations before reconciliation:

- Plannotator plan mode is **not a read-only boundary**: its own Pi README states Bash is unrestricted during planning and only write/edit are limited to the plan file. VERIFIED against npm readme for `@plannotator/pi-extension` 0.23.1.
- `PLANNOTATOR_SHARE=disabled` and `PLANNOTATOR_JINA=0` kill-switch env vars exist as documented. VERIFIED in repo README.
- Runner-up `umputun/revdiff` exists: MIT, 693 stars, pushed 2026-07-18, terminal-native annotation TUI with a Pi package. VERIFIED via GitHub API + README.
- Independent practitioner evidence: SSW rule "Review AI-generated plans" (July 2026) recommends Plannotator's targeted-comment multi-round loop. VERIFIED page exists and features Plannotator.
- Repo vitality: 7,104 stars, 511 forks, created 2025-12-28, commits and PR merges through 2026-07-19 (same day), v0.23.1 released 2026-07-12, Apache-2.0. VERIFIED via GitHub API.
- Local Pi is 0.80.10 >= the extension's stated >= 0.74.0 requirement. VERIFIED (`pi --version`).

## Findings (researcher report, reconciled)

### Verdict

**Yes — best in class for qq's target, not universally.** Google Antigravity, Claude Code's VS Code/Ultraplan, and GitHub Copilot canvases offer more polished first-party plan review inside their own ecosystems, but adopting any of them means replacing the Pi/qq harness, not adding a surface. Among attachable surfaces, none matches Plannotator's combination: first-class Pi extension + event API, anchored plan comments and direct plan edits returned as structured feedback, multi-round revision with rendered/raw plan diffs, local browser operation without an account, plan+document+diff review in one product, portability across agent harnesses. [HIGH for fit-to-target; MEDIUM for ranking]

### What it is

Plan-review loop closer to PR review than chat: agent submits Markdown plan → local browser review → operator attaches anchored comments/labels, deletes text, edits Markdown directly, or leaves global feedback → structured feedback (selected text + location; direct edits as unified diff) returns to the agent → revise/resubmit with rendered and raw version diffs → approve to execute. Extra surfaces: code review (local git, GitButler, jj, GitHub PRs, GitLab MRs; no Perforce on Pi), general annotation (Markdown/HTML/URLs/folders/last agent message), sharing (URL-fragment encoding for small plans; AES-256-GCM browser-side encryption for larger ones; self-hostable; disable-able). Live multiplayer review is immature. [HIGH — plannotator.ai docs, repo README]

### Pi integration

`pi install npm:@plannotator/pi-extension`; `pi --plan`, `/plannotator`, Ctrl+Alt+P; idle→planning→executing state machine persisted across restarts; `plannotator_submit_plan` agent tool; `/plannotator-review`, `/plannotator-annotate <file>`, `/plannotator-last`; shared event API (`plan-review`, `code-review`, `annotate`, `annotate-last`, `archive`) returning reviewId/approved/feedback/savedPath — composable with qq extensions without terminal scraping. Per-phase config (model/thinking/tools/prompt) layers built-in < `~/.pi/agent/plannotator.json` < `<cwd>/.pi/plannotator.json`. Requires Pi >= 0.74. [HIGH — Pi extension README]

### Material safety issue

Plan mode is workflow phase control, **not a sandbox**: it intercepts Pi write/edit (Markdown only) but leaves Bash and other extension tools available, constrained only by prompt instructions. qq's own guards/sandbox remain authoritative; entering plan mode must never be treated as entering a non-mutating environment. [HIGH — verified in source + readme]

### Competition (checked and not finalists)

- **revdiff** — practical runner-up [HIGH]: native Pi package, terminal UI, structured stdout annotations, persistent history, explicit Herdr support, git/hg/jj. Prefer it if SSH/terminal-only operation outweighs visual plan-version review. Its plan loop is manual file review, not an automatic plan-mode gate. Note: it also overlaps slopchop's diff-review surface, so adopting it would re-open a settled disposition.
- **Agent-Native Visual Plans** — specialist [MEDIUM-HIGH]: rich diagrams/wireframes/walkthroughs, threads/mentions; hosted connector is the normal path; Pi support generic; adds a generated presentation layer that can diverge from the plan.
- **PlanBridge** — minimal local browser comments for Claude/Codex hooks; no Pi extension, no code review, no version diffs; much smaller.
- **OpenCode / Windsurf / Zed** — plan modes exist but feedback is conversational; no anchored visual annotation gate. **Plandex** — separate agent, not attachable. **Spec Kit / OpenSpec / Kiro** — spec-governance methodologies with human gates, complementary not competing; qq already hard-rejects foreign lifecycles (doc-61, doc-63).
- Dead/deprecated: **Vibe Kanban** (company shut down 2026-04, community-maintained), **Crystal** (deprecated 2026-02 → Nimbalyst), **HumanLayer** (repo mostly deprecated).

### Maturity

~7.1k stars, 511 forks, ~845 commits, 125 releases, v0.23.1 (2026-07-12), commits through research date; dual MIT/Apache-2.0; SHA-256 sidecars + SLSA provenance on recent releases; ~93 open issues. 0.x churn is high — pin versions. Maintainer concentration appears near one [MEDIUM inference]. Independent comparative evidence is one practitioner comparison (SSW) plus sparse creator-adjacent community threads [LOW-MEDIUM].

## qq-side collision analysis (owning agent)

Plannotator features vs surfaces settled in T-110 (2026-07-19, operator ledger):

| Plannotator feature | qq incumbent | Disposition needed |
|---|---|---|
| Plan mode (plan file → browser approve/annotate → execute) + plan diffs | none — pi-plan-mode evaluated but UNPROVEN (doc-63), never adopted | Fills the open T-101-class need; doc-54's "adopt one plan mode, not both" stands → adopting Plannotator rejects pi-plan-mode |
| `/plannotator-review` (browser diff review) | **pi-slopchop** — T-110 settled "one review surface", slopchop owns diff review | Convention: slopchop keeps diff review; `/plannotator-review` unused (or re-open T-110 — not recommended same-day) |
| `[DONE:n]` execution checklist widget | **rpiv-todo** — T-110 settled "one todo" | Coexistence smoke required; Plannotator's widget is plan-scoped, rpiv-todo session-scoped |
| Archive browser (saved plans/decisions) | Backlog decision records | Informational only; never a source of alignment decisions (doc-54 warning); grilling keeps decision authority |
| `/plannotator-annotate`, `/plannotator-last` | none | Additive |

Integration constraints: plan files must live outside `backlog/` (cockpit `qq-backlog-guard.ts` blocks write/edit into `backlog/`; T-101 convention "plans live in the pi session, never under backlog/" applies); start with `PLANNOTATOR_SHARE=disabled` + `PLANNOTATOR_JINA=0`; pin the extension version.

## Recommendation shape (disposition belongs to operator)

Evidence-generating trial ticket, per doc-63's structural note (published evidence cannot skip a trial): install `@plannotator/pi-extension` pinned into user settings; smoke on one real planning task; verify browser launch under Herdr, repeated reject/revise cycles, recovery after browser closure, coexistence with slopchop + rpiv-todo + qq-backlog-guard, plan file location outside `backlog/`. Exit criteria: keep revdiff as the terminal-native fallback if browser review proves operationally awkward.

## Sources

- [Plannotator repo](https://github.com/backnotprop/plannotator) and [Pi extension README](https://github.com/backnotprop/plannotator/tree/main/apps/pi-extension); npm `@plannotator/pi-extension` 0.23.1 readme (verified)
- [Plan-review docs](https://plannotator.ai/docs/commands/plan-review/), [code-review docs](https://plannotator.ai/docs/commands/code-review/)
- [revdiff](https://github.com/umputun/revdiff) (verified)
- [SSW: Review AI-generated plans](https://www.ssw.com.au/rules/review-ai-plans) (verified)
- [Antigravity artifact review](https://antigravity.google/docs/artifact-review), [Claude permission modes](https://code.claude.com/docs/en/permission-modes) / [Ultraplan](https://code.claude.com/docs/en/ultraplan), [OpenCode agents](https://opencode.ai/docs/agents/), [Zed Agent Panel](https://zed.dev/docs/ai/agent-panel), [Plandex review](https://docs.plandex.ai/core-concepts/reviewing-changes), [Vibe Kanban shutdown](https://www.vibekanban.com/blog/shutdown), [Crystal](https://github.com/stravu/crystal), [HumanLayer](https://github.com/humanlayer/humanlayer), [Spec Kit workflows](https://github.github.com/spec-kit/reference/workflows.html), [OpenSpec](https://github.com/Fission-AI/OpenSpec), [Kiro specs](https://kiro.dev/docs/specs/), [Visual Plans](https://www.agent-native.com/docs/plan-plugin)
- Internal: doc-54, doc-59, doc-61, doc-63; T-101 (archived), T-110

## Gaps

- No hands-on install or end-to-end usability test performed (read-only research).
- No published benchmark of review quality/speed across these products; comparative ranking rests on feature evidence + one practitioner comparison.
- Sharing-crypto and self-host claims inspected in docs/source, not audited.
- Browser-under-Herdr, SSH port-forwarding, and coexistence with qq's exact extension stack untested.
- Category is moving fast; conclusions may age within months.
