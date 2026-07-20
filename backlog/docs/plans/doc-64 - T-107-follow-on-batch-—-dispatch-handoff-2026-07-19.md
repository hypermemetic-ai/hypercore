---
id: doc-64
title: T-107 follow-on batch — dispatch handoff (2026-07-19)
type: other
created_date: '2026-07-19 20:01'
updated_date: '2026-07-19 20:21'
tags:
  - plans
---
# T-107 follow-on batch — dispatch handoff (2026-07-19)

**Owning task:** T-107 (completed 2026-07-19; final ledger in its notes). **Status:** FINAL at handoff. Dispatch scope: 3 settled tickets. Written by the settler session for the receiving dispatch orchestrator (a fresh pi session in the qq project home).

Per-ticket intent, ACs, and decision ledgers live on the tickets themselves — those are authoritative. This doc carries batch shape, sequencing, constraints, and reconciliation facts the settler verified hands-on.

## Dispatch scope

| Ticket | What it is | Wave |
|---|---|---|
| T-109 | Reshape skills/agent-messaging onto pi-intercom transport (qq overlay + intercom + herdr operator notifications; NO legacy herdr-send path — operator amendment 2026-07-19: "legacy stuff needs to go; this isn't a museum") | 1 |
| T-108 | Pilot opencode-codebase-index vs codebase-memory, structural-first; output = corpus + comparison + proposed verdict | 1 (parallel with T-109) |
| T-110 | Adopt QoL package set: files-widget, slopchop, fff (additive), pi-footer, rpiv-todo | 2 (after T-109 merges — ratchet baselines and skills/ overlap) |

**Held OUT:** T-111 (yazi retirement — needs its own alignment brief first; do not dispatch). T-112 (terminal GitHub merge console — evaluation ending in operator dispositions, same operator-facing-settler shape as T-107; schedule deliberately, not a codex ticket).

## Per-ticket orchestrator notes

### T-109 (messaging reshape)
- pi-intercom verified loading on pi 0.80.10 from BOTH npm 0.6.0 and git main (settler hands-on). npm 0.6.0 peer metadata is stale (@mariozechner scope) but loads and registers the `intercom` tool; install spec: `npm:pi-intercom`. Git main carries extra hardening (trust metadata, rate limits, inboundTrigger policy) — unpinned npm is fine.
- intercom semantics that matter for the skill: broker auto-spawns (local IPC); `intercom` tool actions list/send/ask/reply/status; busy interactive sessions queue inbound until idle; inboundTrigger default `always` auto-triggers a turn on receipt (the desired delegate wake semantics — document the policy); bundled skill ships with the package; operator notifications stay on `herdr notification show` (unchanged).
- AC #2 as amended: pi-to-pi correlated ask/reply smoke; the shipped skill contains NO herdr-send inter-agent path (grep-verified). Codex delegates remaining before T-95 coordinate through delegate-batch's own machinery (work orders, envelopes, detail files, resume-steering) — that machinery never depended on the agent-messaging skill. T-95 has NOT landed (its batch is in flight; T-94's delegate was blocked at handoff) — irrelevant to this ticket now: no codex bridge is built or kept.
- Where the extension install lives: the reshape may need pi-intercom installed in user settings (~/.pi/agent/settings.json) for the smoke — same sandbox constraint as T-110 below; apply locally at delivery, do not sandbox-confine it.

### T-108 (codebase-index pilot, structural-first)
- Challenger facts (settler-verified): opencode-codebase-index 0.14.0; real pi surface (`pi` key → ./dist/pi-extension.js + skills); 15 tools incl. call_graph, call_graph_path, pr_impact, implementation_lookup, index_codebase, index_status. Semantic codebase_search needs an embeddings provider (ollama/openai/gemini) — OUT OF SCOPE for this pilot.
- Incumbent access: `codebase-memory-mcp cli` (AGENTS.md routing block); installed v0.9.0.
- Verdict (replace/keep/additive) is CONSEQUENTIAL — the delegate produces corpus + comparison + a proposed verdict and STOPS; the operator disposes the verdict. No AGENTS.md routing change in this Change.
- Delegates may not edit `backlog/` (doc-48): corpus + raw results land in the Change worktree (suggest `tests/fixtures/` or a scratch path named in the work order); the orchestrator mints the final research doc via backlog CLI at finalization.

### T-110 (QoL adoption set)
- All five packages load-verified TOGETHER on pi 0.80.10 (settler combined-load check; evidence in T-107 notes). Specs: `npm:@tmustier/pi-files-widget`, `npm:pi-slopchop`, `npm:@ff-labs/pi-fff`, `npm:pi-footer`, `npm:@juicesharp/rpiv-todo`.
- fff: additive default (`tools-and-ui`). Do NOT set override mode; monitored drift signal = agent choosing built-in find/grep over fff tools in session logs.
- pi-footer: operator wants text/minimalist icons (narumitw was rejected on emoji aesthetics). Its config lives at ~/.pi/agent/extensions/pi-footer.json; the built-in `pi-footer` preset (iconMode text) is the approved starting point.
- bat + git-delta are already installed system-wide (brew) for files-widget.
- **Sandbox constraint:** codex delegates are confined to their worktree and CANNOT write ~/.pi/agent/settings.json. Split the ticket: delegate makes the repo-side changes (AGENTS.md routing, skills references, ratchet baselines) and emits the exact settings.json packages fragment + pi-footer.json content in its envelope; the orchestrator applies the user-settings changes locally at delivery and runs the combined-session smoke (AC #1) itself.
- Repo-side references to update (settler-identified): AGENTS.md (no structural changes — note fff tools alongside built-ins where relevant), any skills that hard-reference search-tool choice; slopchop = the diff-review surface (GitHub web demoted to checks+merge) belongs in deliver-change/review prose where review is described; rpiv-todo subordinate to Backlog Tasks where task conventions are written. Keep edits minimal.

## Cross-batch facts

- The doc-62 batch is IN FLIGHT under a different orchestrator (T-94 blocked, T-104 working at handoff). Work-session change labels must not collide with existing sessions (`feat-t-94-subagent-pilot`, `fix-t-104-pr-watch-contract`); suggested labels: `t109-intercom`, `t108-index`, `t110-qol`.
- doc-48 hybrid Task-truth rules govern: no `backlog/` edits in worktrees; managed markdown via backlog CLI from the primary checkout only.
- pi 0.80.10, herdr 0.7.4. Trial sandbox /tmp/t107 still exists (settler's ephemeral PI_CODING_AGENT_DIR + scratch repo) — reusable for smokes, disposable.
- Per-ticket commit protocol and completion-envelope verification per delegate-batch, unchanged. Codex-first dispatch, 3-ticket wave limit respected (max 2 concurrent here).

## Evidence base

T-107's completed-task notes carry the full trial evidence (messaging load checks, live TUI trials of files-widget/slopchop/pi-diff-review, fff selection/parity/staleness/cold-start data, statusline renders, rpiv-todo lifecycle + zero-footprint check, plan-mode gating probe, challenger package inspection).
