---
id: doc-84
title: Plan — qq-footer approved 2026-07-23
type: specification
created_date: '2026-07-23 17:02'
updated_date: '2026-07-23 17:03'
tags:
  - plan
---
# Plan — qq-footer (T-149), approved 2026-07-23

## Intended outcome

New `extensions/qq-footer.ts` replacing pi's built-in footer with exactly the operator-chosen content:

- **Line 1:** `~/projects/qq (branch) • session-name` — unchanged from built-in.
- **Line 2:** `14.2%/200k • $0.012 • K ▓▓░░░░░░ 5h · ▓▓▓▓▓▓▓░ wk        (kimi) kimi-k2 • high` — context %, $ cost, quota bars; model • thinking right-aligned. Token/cache stat segments dropped.
- **Quota bars (active provider only):** one 8-block bar per window, fill = fraction of the window used.
  - Kimi (`kimi-coding`): 5-hour + weekly windows from `GET https://api.kimi.com/coding/v1/usages`, Bearer = key from `~/.pi/agent/auth.json`; live-verified against operator credentials 2026-07-23.
  - Codex (`openai-codex`): windows from `GET https://chatgpt.com/backend-api/wham/usage`, Bearer access token + `ChatGPT-Account-Id` header from auth.json; live-verified 2026-07-23.
  - Anthropic (`anthropic`): wired via `GET https://api.anthropic.com/api/oauth/usage`, hidden until auth is configured.
  - Unsupported or unconfigured provider → no quota segment.
- **Extension statuses:** rendered minus blocklist `{pi-lens-lsp, hunk, merge-ready}`.
- **Fetching:** on session start + every 5 minutes, cached; rendering never blocks on the network; `/qq-footer-refresh` forces a refetch.
- **Also:** delete `extensions/pi-footer.json` (dead config from the T-133/T-138 era; the pi-footer package was removed 2026-07-23); register the extension in `~/.pi/agent/settings.json`; add `tests/test-qq-footer-extension.sh` in the established node-import style.

## Ownership boundary

This Change owns: the new extension, its test, the `pi-footer.json` removal, the settings.json registration, and any README touch-up where the extensions list mentions footers. It does not touch pi-lens, pi core, or other qq extensions.

## Non-goals

No third-party quota packages; no configurable layout system; no Anthropic auth setup (auto-detect only); no Moonshot pay-as-you-go balance; no per-model breakdown; no powerline.

## Success evidence

1. `tests/test-qq-footer-extension.sh` green: quota parsing for both live response shapes, blocklist filtering, render output.
2. Full native suite + repo Checks green.
3. Live verification in a fresh pi session: footer matches spec, no LSP status, Kimi bar fill matches a manual curl of `/usages`.

## Decision dispositions

The decision ledger lives in T-149's Description: approach (qq-owned all-in-one), active-provider-only display, and bar rendering are asked-and-answered this session; the status blocklist cites T-133/T-138; pi-config-as-qq-scope is asked-and-answered 2026-07-23; poll cadence, endpoint shapes, and command naming are owner calls stated in the approved brief.
