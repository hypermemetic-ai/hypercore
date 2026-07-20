---
id: doc-57
title: 'pi-sweep D — Session and workspace topology (herdr glue, messaging)'
type: other
created_date: '2026-07-19 16:33'
updated_date: '2026-07-19 16:35'
tags:
  - research
---
# pi-sweep D — Session and workspace topology: reconciled research report

**Owning task:** T-93 — Evaluate pi-ecosystem replacements for qq surfaces.
**Cluster:** D — herdr glue (`qq-herdr-home`, `qq-herdr-pull`, `qq-herdr-snap`, agent-messaging skill).
**Research date:** 2026-07-19. **Overall confidence:** HIGH on functional fit and the absence of a drop-in; MEDIUM on third-party runtime quality (nothing installed).
**Settles:** Keep all three topology scripts — they encode qq/herdr policy no package reproduces. Adopt `@ogulcancelik/pi-herdr` (from herdr's author) as pi's generic herdr surface, and shrink `skills/agent-messaging` to a qq-specific routing/protocol overlay on top of its bundled skill. Herdr's native session/layout APIs already cover real snapshot/remote QoL.
**Decision this informs:** the agent-messaging slim and pi-herdr adoption are their own later Changes; this document is evidence, not authorization.

## Owning-agent verification (2026-07-19)

Spot-checked before reconciliation: `@ogulcancelik/pi-herdr` at 0.3.0 on the npm registry, matching the report. The `qq-herdr-snap` terminology correction verified against source: its header comment describes a focus toggle with per-workspace bounce-back state, Pi-first with claude fallback — **not** a workspace snapshot, and **not** Claude-first. **Incidental drift finding:** `openwiki/operations.md` describing Claude-first snap selection is stale against source; record for a future docs refresh (relates to doc-58's openwiki-staleness finding).

## Cross-cluster adjudications

- **`pi-herdr-subagents`:** shortlisted here for visible async children; doc-56 sequences it strictly after the delegation-runner decision. Treat the sequencing note there as binding.
- **`pi-intercom`:** shortlist is gated on `@earendil-works`-scope compatibility shipping or being verified; it stays Pi-only, so it cannot replace cross-runtime qq messaging while Claude/Codex agents remain.
- **Agent-messaging shrink** depends on adopting `@ogulcancelik/pi-herdr`'s bundled skill as the generic-command reference; without that adoption the skill stays as-is.

---

# Session-topology findings

**Question:** What maintained Pi-ecosystem replacement, or combination, best covers qq’s Herdr glue for project-home resolution, pane pull/adoption, `snap`, and agent messaging—and what additional session QoL is available?

**Overall confidence:** **HIGH** on functional fit and the absence of a true drop-in; **MEDIUM** on third-party package runtime quality because packages could not be installed or exercised.

**Settled:** There is no maintained drop-in replacement for qq’s three topology scripts. The best combination is:

1. **Adopt `@ogulcancelik/pi-herdr` as Pi’s generic Herdr control surface.**
2. **Keep `qq-herdr-home`, `qq-herdr-pull`, and `qq-herdr-snap`.**
3. **Shrink `skills/agent-messaging` into a qq-specific routing and protocol overlay**, delegating generic Herdr command instruction to the official package’s bundled skill.
4. Use Herdr’s native session/layout capabilities directly for actual workspace serialization and remote/session QoL.

A terminology correction matters: [`qq-herdr-snap`](/home/qqp/projects/qq/bin/qq-herdr-snap:1) is a focus-navigation toggle with bounce-back state, not a workspace-state snapshot. Herdr’s `session.snapshot` and layout APIs solve the latter problem but do not replace the script.

## Recommended disposition

| Surface | Verdict | Reason |
|---|---|---|
| [`qq-herdr-home`](/home/qqp/projects/qq/bin/qq-herdr-home:35) | **KEEP** | Encodes Git-main uniqueness, common-directory identity, linked-worktree exclusion, exact Herdr workspace selection, and Backlog-board focus policy. No candidate reproduces this. |
| [`qq-herdr-pull`](/home/qqp/projects/qq/bin/qq-herdr-pull:66) | **KEEP** | Encodes sidebar ordering, status-aware `next`, caller-aware adoption, idle-placeholder validation, move-before-close behavior, and distinct operator/agent failure semantics. |
| [`qq-herdr-snap`](/home/qqp/projects/qq/bin/qq-herdr-snap:57) | **KEEP** | Encodes project-home preference, Pi-before-Claude selection, per-workspace origin state, and focus bounce-back. Generic focus APIs are insufficient. |
| [`agent-messaging`](/home/qqp/projects/qq/skills/agent-messaging/SKILL.md:13) | **SHRINK/REWRITE** | Preserve cross-runtime addressing, sender envelope, source verification, reply route, literal-send rules, and operator notifications. Remove duplicated generic Herdr command education. |
| `@ogulcancelik/pi-herdr` | **ADOPT** | Best-maintained Pi-native typed interface to the installed Herdr backend, from Herdr’s author. It is a substrate, not a policy replacement. |
| Herdr session/layout APIs | **ADOPT directly where needed** | Already provide real live-state snapshots, portable layout export/apply, restart restoration, named sessions, and remote attachment. |

## Candidate findings

### `@ogulcancelik/pi-herdr` — ADOPT as substrate

This is the strongest candidate: version 0.3.0 was published July 14, requires current Pi and Herdr versions, is maintained by Herdr’s author, and bundles both an extension and an official Herdr skill. It exposes structured workspace, tab, pane, agent, read/watch/wait/send, split, focus, and run actions. [Pi package catalog](https://pi.dev/packages/%40ogulcancelik/pi-herdr?page=26), [source](https://github.com/ogulcancelik/pi-extensions/tree/main/packages/pi-herdr), [package manifest](https://raw.githubusercontent.com/ogulcancelik/pi-extensions/main/packages/pi-herdr/package.json).

Fidelity:

- **Project home:** None beyond listing workspaces. It lacks Git-main validation, common-dir/repository identity, linked-worktree filtering, and Backlog-board discovery.
- **Pull/adopt:** Herdr itself has `pane.move`, but the package’s structured tool deliberately omits pane movement. It also lacks qq’s target selection and placeholder-shell validation.
- **Snap:** Supplies focus primitives, but no home-selection policy or saved bounce origin.
- **Messaging:** Partial. It supplies the main list/get/read/wait/send/run primitives, but not qq’s envelope, source validation, reply-routing contract, or cross-runtime/operator-notification policy.

**Named residual:** The repository calls the package experimental; a test file exists, but its breadth could not be inspected or executed. The installed Herdr CLI should remain the semantic authority. **Confidence: HIGH** on fit, **MEDIUM** on runtime maturity.

### Herdr 0.7.4 native APIs — ADOPT/KEEP as backend

Herdr is actively maintained, with 0.7.4 and preview releases published during the week of this research. Its official guidance recommends CLI wrappers for shell orchestration and the socket API for custom tools and event subscribers. [Releases](https://github.com/ogulcancelik/herdr/releases), [socket API](https://herdr.dev/docs/socket-api/).

Herdr exposes the primitive operations qq needs: workspace/tab/pane inspection and focus, cross-workspace `pane.move`, agent discovery and messaging, notifications, session snapshots, and layout export/apply.

Fidelity:

- **Project home:** Primitives only; repository policy remains qq-owned.
- **Pull/adopt:** All mutation primitives exist, including moving a live terminal, but no qq selection or safety policy.
- **Snap:** Focus primitives only.
- **Messaging:** Transport primitives exist, but no qq protocol contract.

For actual workspace snapshots, Herdr already offers:

- `session.snapshot` for a point-in-time live-state bootstrap;
- layout export/apply for portable tab-tree structure;
- restart restoration of shape and focus;
- resumable native agent-session references.

These do not preserve arbitrary live processes in a reconstructed layout; detaching from a still-running Herdr server is what keeps processes alive. [Session restoration](https://herdr.dev/docs/session-state/), [persistent and remote sessions](https://herdr.dev/docs/persistence-remote/).

**Named residual:** Herdr is AGPL/commercial licensed and already part of qq’s architecture; this recommendation does not introduce a new licensing dependency. **Confidence: HIGH**.

### `@weshipwork/pi-herdr` — REJECT

This is an older, smaller implementation of essentially the same typed Herdr surface: version 0.1.0, no bundled skill, minimal repository history, and fewer maintenance signals. [Package](https://pi.dev/packages/%40weshipwork/pi-herdr), [repository](https://github.com/WeShipWork/threeonefour).

Fidelity against all four qq behaviors is no better than the official-author package.

**Named residual:** Minimal adoption and maintenance history. **Confidence: HIGH**.

### `@andrewjacop/pi-herdr` — HOLD for delegation QoL; REJECT as glue

This package targets heterogeneous Pi/Claude/Codex/OpenCode delegation and adds composite operations. Its own roadmap still lists layout, notification, worktree, and session/snapshot support as future tiers; Linux verification is also incomplete. [Package](https://pi.dev/packages/%40andrewjacop/pi-herdr?name=web).

Fidelity:

- **Home:** None.
- **Pull/adopt:** No qq-equivalent topology transaction.
- **Snap:** None.
- **Messaging:** Useful heterogeneous delegation, but not qq’s already-live-session protocol.

**Named residual:** Linux and current Herdr 0.7.4 behavior remain unverified. **Confidence: MEDIUM**.

### `pi-intercom` — SHORTLIST after compatibility verification

`pi-intercom` is the strongest messaging QoL candidate. It provides a local broker, peer discovery, direct send, correlated ask/reply, pending requests, attachments, status, an Alt+M overlay, and sensible busy/idle delivery. It has meaningful adoption, releases, and dedicated broker/reply/integration tests. [Package](https://pi.dev/packages/pi-intercom), [repository](https://github.com/nicobailon/pi-intercom).

Fidelity:

- **Home, pull/adopt, snap:** None.
- **Messaging:** Stronger than qq for correlation and UI, but only among Pi sessions running the extension. It cannot route to Claude, Codex, or arbitrary Herdr agents and does not supply qq’s Herdr operator notification path.

It should not replace qq messaging while mixed runtimes remain. Running both transports by default would create two peer directories and ambiguous reply expectations.

**Named residual:** The current unreleased changelog updates package/runtime references to the new `@earendil-works` Pi scope; stable 0.6.0 predates that work, so compatibility with the installed Pi is not established. [Changelog](https://github.com/nicobailon/pi-intercom/blob/main/CHANGELOG.md). **Confidence: HIGH** on semantics, **MEDIUM** on current compatibility.

### `pi-sessions` — SHORTLIST for memory and handoff QoL

`pi-sessions` adds indexed search across past conversations, querying prior sessions, handoff creation, auto-titles, and live Pi-session messaging. It is recent and includes tests and smoke checks. [Package](https://pi.dev/packages/pi-sessions), [repository](https://github.com/thurstonsand/pi-sessions).

Fidelity:

- **Home, pull/adopt, snap:** None.
- **Messaging:** Pi-only live messaging without qq’s cross-runtime routing or explicit request/reply correlation.

Its value is searchable session memory and deliberate handoff, not topology control.

**Named residual:** Requires a resident SQLite index and a narrow Node runtime range; indexing, model cost, and privacy policy need operator acceptance. **Confidence: MEDIUM**.

### `pi-herdr-subagents` — SHORTLIST for visible asynchronous Pi children

This extension runs Pi subagents in visible Herdr panes or tabs and provides lifecycle UI, stall handling, interruption, resumption, and child-to-parent signaling. It has unit/lint checks plus claimed real-Herdr integration coverage. [Package](https://pi.dev/packages/pi-herdr-subagents), [repository](https://github.com/0xRichardH/pi-herdr-subagents).

Fidelity:

- **Home:** None.
- **Pull/adopt:** It creates and manages its own child panes; it does not adopt arbitrary existing terminals.
- **Snap:** None.
- **Messaging:** Purpose-built parent/child signaling, not general peer messaging.

**Named residual:** Catalog/release metadata reports 0.1.5 while the inspected main-branch manifest reported 0.1.3, indicating source/publication drift. **Confidence: MEDIUM**.

### `pi-herdr-squad` — HOLD for bounded read-only investigations

This package creates one to four read-only Pi investigators in a dedicated Herdr tab, with exclusive scopes and a deliberately restricted tool set. [Package](https://pi.dev/packages/pi-herdr-squad).

It has no fidelity to any of the four glue surfaces. Its distinct value is a constrained, auditable investigation squad rather than arbitrary delegation.

**Named residual:** Very new package; initial download figures are likely launch-week artifacts rather than durable adoption evidence. **Confidence: MEDIUM-LOW**.

### `pi-messenger` — HOLD for reservations/feed; REJECT as replacement

`pi-messenger` is a mature Pi-only coordination system with file-based presence and messaging, direct/broadcast messages, wake/steer behavior, file reservations, activity feeds, stuck detection, a human overlay, and crew task graphs. [Package](https://pi.dev/packages/pi-messenger), [repository](https://github.com/nicobailon/pi-messenger).

Fidelity:

- **Home, pull/adopt, snap:** None.
- **Messaging:** Broad Pi-only coordination, but no Herdr topology, mixed-runtime addressing, or qq envelope.

Its file-reservation mechanism is potentially valuable, but adopting it would introduce project state and a second coordination methodology.

**Named residual:** High overlap and split-brain risk with qq’s existing coordination contract. **Confidence: HIGH**.

### Worktree and alternative-multiplexer packages — REJECT for this role

- [`@ogulcancelik/pi-worktree`](https://pi.dev/packages/%40ogulcancelik/pi-worktree) moves a Pi conversation to another Git worktree by switching session files and deleting the old one. That is conversation relocation, not live-pane movement or adoption.
- [`@ogulcancelik/pi-tmux`](https://pi.dev/packages/%40ogulcancelik/pi-tmux) explicitly disables itself under Herdr.
- [`@vanillagreen/pi-agents-tmux`](https://pi.dev/packages/%40vanillagreen/pi-agents-tmux) offers strong persistent-agent QoL, but adopting a second multiplexer would replace the architectural substrate rather than simplify qq’s Herdr glue.
- Pi-native orchestrators such as [`pi-gentic`](https://pi.dev/packages/pi-gentic) and [`pi-subagents`](https://pi.dev/packages/pi-subagents) manage child conversations and worktrees, not arbitrary Herdr topology or mixed-runtime peers.

**Named residual:** These become relevant only if the operator chooses a strategic move away from Herdr or toward homogeneous Pi agents. **Confidence: HIGH**.

## QoL additions qq does not currently expose

The lowest-risk additions are already in Herdr:

1. **Named independent sessions** for separating durable work contexts.
2. **Remote attach over SSH** and direct terminal attach/observe/control.
3. **Session snapshot bootstrap** for custom status/control views.
4. **Layout export/apply** for reproducible terminal arrangements.
5. **Restart restoration plus agent conversation resume.**

These preserve a single topology authority and require no parallel coordination framework. [Herdr persistence and remote sessions](https://herdr.dev/docs/persistence-remote/).

Package-based QoL, in priority order:

1. **`pi-intercom` correlated ask/reply and pending-request UI**—shortlist once current-scope compatibility ships or is verified.
2. **`pi-sessions` searchable historical memory and explicit handoffs**—shortlist if its indexing/privacy/runtime tradeoffs are acceptable.
3. **`pi-herdr-subagents` visible asynchronous children with stall/recovery controls**—shortlist for productized Pi delegation.
4. **`pi-herdr-squad` constrained read-only investigation teams**—hold for situations where restrictive tooling is desirable.
5. **`pi-messenger` file reservations and activity feed**—consider those capabilities independently, but avoid adopting its full messaging/crew model alongside qq by default.

## Implementation boundary implied by the evidence

The appropriate simplified architecture is:

```text
qq policy
├── qq-herdr-home
├── qq-herdr-pull
├── qq-herdr-snap
└── thin agent-messaging protocol overlay
        ↓
official pi-herdr extension/skill + Herdr CLI
        ↓
Herdr socket API and session runtime
```

The thin messaging overlay should retain only qq-specific semantics:

- discovering already-live cross-runtime agents;
- `AGENT from=<terminal-id>` addressing;
- literal-send requirements;
- sender existence verification before replying;
- current-pane caller resolution;
- operator notification behavior;
- explicit unrouteable-message handling.

Everything resembling a generic Herdr command reference can move to the official Herdr skill.

## Sources that shaped the conclusions

Primary local evidence:

- [`qq-herdr-home`](/home/qqp/projects/qq/bin/qq-herdr-home:35)
- [`qq-herdr-pull`](/home/qqp/projects/qq/bin/qq-herdr-pull:66)
- [`qq-herdr-snap`](/home/qqp/projects/qq/bin/qq-herdr-snap:57)
- [`agent-messaging` contract](/home/qqp/projects/qq/skills/agent-messaging/SKILL.md:13)
- [Herdr key configuration](/home/qqp/projects/qq/cockpit/herdr/config.toml:62)

Upstream evidence:

- [Herdr agent integration](https://herdr.dev/docs/agent-skill/)
- [Herdr socket API](https://herdr.dev/docs/socket-api/)
- [Herdr session restoration](https://herdr.dev/docs/session-state/)
- [Pi sessions](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/sessions.md)
- [Pi RPC](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/rpc.md)
- [Official `pi-herdr` implementation](https://github.com/ogulcancelik/pi-extensions/tree/main/packages/pi-herdr)

## Evidence gaps

- Fresh Bash syntax and warning-level ShellCheck checks passed for the local helpers.
- The focused mock tests could not start because the supplied environment made `/tmp` read-only. Existing recorded results were not treated as fresh verification.
- No candidate package was installed or run against Herdr 0.7.4.
- The official `pi-herdr` test file could not be inspected, so its effective coverage is unknown.
- `pi-intercom`’s published stable release was not verified against the current `@earendil-works` Pi runtime.
- `pi-herdr-subagents` has a catalog/source version mismatch.
- Very new relay/threading packages were screened out for insufficient maintenance and trust evidence rather than proven functional defects.
- [`openwiki/operations.md`](/home/qqp/projects/qq/openwiki/operations.md:47) describes Claude-first `snap` selection, while current source and configuration are Pi-first. The source was treated as authoritative.
