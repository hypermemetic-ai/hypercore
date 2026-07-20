---
id: doc-62
title: pi-sweep batch — alignment dispositions and dispatch handoff (2026-07-19)
type: other
created_date: '2026-07-19 18:11'
updated_date: '2026-07-19 18:42'
tags:
  - plans
---
# pi-sweep batch — alignment dispositions and dispatch handoff (2026-07-19)

**Owning task:** T-93 (follow-up) · **Status:** FINAL at wrap-up 2026-07-19. Dispatch scope: 7 settled tickets. Everything unsettled lives in T-107, owned by a separate operator-facing session. Written by the alignment session for the receiving dispatch orchestrator.

Per-ticket intent, amendments, and decision ledgers live on the tickets themselves — those are authoritative. This doc carries batch shape, sequencing, and open items.

## Dispatch scope (aligned)

| Ticket | What it is now | Unblocks |
|---|---|---|
| T-94 [HIGH] | Pilot pi-subagents + Landstrip, **bridge-less** (no qq-status stage bridge; AC #2 = 9 checks); decision record for the herdr kill minted in its Change (AC #4) | T-95 |
| T-104 [MED bug] | deliver-change/qq-pr-watch divergence; direction: **converge on the owned command**, prose 5s loop dies, skill names the contract | T-99 |
| T-105 [MED docs] | openwiki refresh vs current source; routes to the **openwiki-maintainer Actor**, docs-only, operator merge | — |
| T-97 [MED] | Disposable-repo trial of upstream OpenWiki CI docs-PRs; **Kimi key via OpenAI-compatible endpoint**; trial *accepts* upstream's marked-section AGENTS.md/CLAUDE.md management and proves section-scoping (byte-identical outside markers); telemetry inspected once via `--telemetry-file` | — |

**Aligned, blocked:** T-95 [HIGH] (after T-94 adopt — migration incl. **removal** of qq-status herdr paths and delegate-batch's status-surface protocol; detail files stay) · T-99 [LOW] (after T-104) · T-106 [MED chore] (after T-95 — retire Claude Code support surfaces; seed inventory on ticket).

**Held OUT of this batch:** T-98 — held pending T-107's messaging evaluation (a broker/file transport would moot or reshape the pi-herdr slim).

**Dropped (archived with disposition notes):** T-96 (methodology adoptions — no adoption without outcome evidence; doc-61) · T-100 (cc-safety-net — no demonstrated need) · T-101, T-102, T-103 (superseded by T-107 after the operator reviewed the raw round-2 findings, doc-63).

## Cross-cutting dispositions (operator, 2026-07-19 alignment session)

1. **Herdr delegation-status machinery killed outright** — stage tokens, pane presence, delegate notifications. T-94 flies bridge-less; T-95 deletes qq-status's herdr paths and delegate-batch's reporting protocol; detail-file protocol stays. Cockpit, topology scripts, and agent messaging survive. Accepted loss: out-of-transcript blocked-delegate ping. T-94 mints the decision record.
2. **Upstream OpenWiki owns its marked AGENTS.md/CLAUDE.md sections** (verified surgical in 0.2.0 source). qq's shadow/restore machinery and hand-authored section content drop via T-97's verdict.
3. **qq does not support Claude Code** — CLAUDE.md is upstream's file only; Claude surfaces retire in T-106.
4. **No methodology adoptions without behavioral outcome evidence.**
5. **Dispatch runs the delegate-batch status surface as written** — the herdr glass dies properly via T-95, not ad hoc.

## Dispatch plan (delegate-batch, current codex-first substrate)

- **Wave 1:** T-94, T-104, T-105, T-97 — files disjoint; T-105 goes to the maintainer Actor, T-97's trial runs in a disposable external repo (operator-input moment for the Kimi key).
- **Wave 2:** T-95 (on T-94 adopt verdict), T-99 (after T-104 lands).
- **Wave 3:** T-106 (after T-95).
- **Work-order facts:** doc-48 hybrid Task-truth rules still govern (no `backlog/` edits in worktrees — T-88's convention-retirement half hasn't landed; see ticket comment); per-ticket commit protocol and completion-envelope verification per delegate-batch.

## Open items

1. **T-107 — owned by the separate settler session**, not this batch: messaging candidates walkthrough (resolves T-98), file-tree/diff deep round with hands-on trials, fff best-in-class check, statusline comparison, rpiv-todo, T-101/T-102 dispositions.
2. **T-88:** no drift — PR #145 was its board half only; convention-retirement half is a later Change needing its own alignment brief. Not this batch's blocker.
