---
id: doc-92
title: Current qq ecosystem update assessment — 2026-07-24
type: other
created_date: '2026-07-24 14:53'
updated_date: '2026-07-24 16:43'
tags:
  - research
  - updates
  - pi
  - herdr
---
# Current qq ecosystem update assessment — 2026-07-24

**Owning Task:** T-156
**Overall confidence:** MEDIUM-HIGH
**Settles:** the complete decision-relevant point-in-time update inventory, notification gaps, qq implications, overlap/simplification opportunities, risks, and a recommendation for every in-scope component. This is assessment evidence only; no assessed runtime was changed.

## Executive verdict

**HIGH — the two visible extension updates were not the complete qq-relevant update set.** Pi 0.81.1 omits pinned package sources from its startup update check, and bulk package update skips exact npm pins while reconciling a git package only to its configured ref (installed Pi `dist/core/package-manager.js:838-970`). The live settings contain exact pins for `rpiv-ask-user-question@2.0.0`, `rpiv-btw@2.0.0`, and the custom `pi-subagents` commit. Pi also does not own Herdr, OpenWiki, Backlog, Landstrip, the underlying browser binary/Node compatibility, or Context7's unpinned MCP launch.

Recommended order:

1. **Update Pi 0.81.1 → 0.82.0 after one focused compatibility smoke.** The release fixes the installed `protobufjs` 7.6.4 advisory and adds useful provider/tool/observability improvements; it does not replace qq's Completion Envelope, trace context, or the execution-profile seam sought by T-152 ([Pi 0.82.0](https://github.com/earendil-works/pi/releases/tag/v0.82.0); [GHSA-j3f2-48v5-ccww](https://github.com/advisories/GHSA-j3f2-48v5-ccww)).
2. **Repair the browser stack through an isolated coordinated trial.** The wrapper's own doctor rejects the live combination: wrapper 0.2.71 expects `agent-browser` 0.32.2 but PATH has 0.27.0. Wrapper 0.2.72 targets browser 0.33.0, which requires Node 24 while the host is Node 22. Treat consequential browser results as unsupported until the stack is coherent ([wrapper 0.2.72](https://github.com/fitchmultz/pi-agent-browser-native/releases/tag/v0.2.72)).
3. **Test Landstrip 0.17.34, then replace the accidental `pi-landstrip` carrier with the documented direct platform binary.** qq source pins 0.17.31 and explicitly requires the platform package; the live npm root instead gets that binary transitively from an unregistered `pi-landstrip` package. No accountable-session sandbox is registered, but the install shape is drift ([Landstrip 0.17.34](https://github.com/landstrip/landstrip/releases/tag/0.17.34); `README.md:68-83`; `delegation/policies/roles.json:1-4`).
4. **Test OpenWiki 0.2.3 before promotion.** It fixes a reachable docs-only `..` traversal, credential/workflow handling, and adds Mermaid/OKF output, but also adds default outbound PostHog telemetry for init/update. Keep qq's root-state restoration until a live trial proves what can shrink ([OpenWiki 0.2.3](https://github.com/langchain-ai/openwiki/releases/tag/0.2.3); [PR #406](https://github.com/langchain-ai/openwiki/pull/406); [PR #285](https://github.com/langchain-ai/openwiki/pull/285)).
5. **Update only `rpiv-ask-user-question` 2.0.0 → 2.1.0 among the two visible pinned rpiv updates.** It contains real notes/collapse/lifecycle fixes. `rpiv-btw` 2.1.0 changes documentation/packaging only, so leave its exact 2.0.0 pin unchanged ([rpiv 2.0→2.1 compare](https://github.com/juicesharp/rpiv-mono/compare/v2.0.0...v2.1.0); [ask changelog](https://raw.githubusercontent.com/juicesharp/rpiv-mono/v2.1.0/packages/rpiv-ask-user-question/CHANGELOG.md)).
6. **Remove dormant `pi-prompt-template-model` after a final machine-wide consumer scan.** Pi itself owns the native prompt format used by qq's new `/update`; pi-subagents owns bounded workflows and model-role execution is moving toward T-152's single install-wide authority. No consumer of the extension-specific frontmatter/config was found under `~/.pi/agent` or `~/projects`. This is a MEDIUM-HIGH inference, not an automatic removal.
7. **Hold the exact custom pi-subagents commit.** Stable 0.35.1 predates the required structured-output recovery patch; upstream `main` has valuable but untagged changes and omits the custom commit. Integrate only over a future stable and preserve the patch ([custom commit](https://github.com/hypermemetic-ai/pi-subagents/commit/b7c531c238469e43866a1fe6697cb44279158c1c); [upstream comparison](https://github.com/nicobailon/pi-subagents/compare/f1540b09283a1c176a0c721878453c6382ecd399...main)).
8. **Test an explicit Context7 MCP pin.** `.mcp.json` executes `@upstash/context7-mcp@latest`, so research inputs can change and execute fetched code without a Repository diff. Trial exact 3.2.4, then replace `@latest` only if current research/review use stays green ([registry metadata](https://registry.npmjs.org/%40upstash%2Fcontext7-mcp)).

## Scope boundary and excluded prerequisites

The inventory covers Pi core, all 12 `pi list` packages, Herdr, first-class externally versioned owners derived from qq source, and otherwise commodity dependencies when a current candidate exposes a material edge. Node is included because the browser candidate requires Node 24; Context7 is included because `.mcp.json` makes it a first-class research integration. Python is live at 3.14.6 and is required by `qq-observe`, `qq-handoff`, and `qq-dispatch`, but no observed release, security, compatibility, migration, overlap, or simplification edge makes it decision-relevant this cycle. Git, GitHub CLI, npm/npx, Homebrew, jq, curl, fzf, renderers, and standard shell/GNU utilities (including Bash, grep, sed, find, xargs, flock, sha256sum, and coreutils) are likewise disclosed generic prerequisites with no material edge controlling a current recommendation. A future observed edge brings any of them into the matrix.

## Complete inventory

| Component | Installed | Latest stable | Pin/channel and material delta | Recommendation | Confidence |
|---|---:|---:|---|---|---|
| Node.js | 22.22.3 (`node@22`, Jod LTS) | 24.18.0 (Krypton LTS) | current Pi and wrapper support Node 22; browser 0.33.0 requires >=24 and is trialed separately | **hold** | HIGH |
| Context7 MCP | no fixed install; `npx -y …@latest` | 3.2.4 at assessment time | source-integrated, unpinned fetched execution; no prior ref for a release delta | **test** exact pin | HIGH |
| Pi core | 0.81.1 | 0.82.0 | global npm; security dependency, constrained sampling, OAuth/session metadata, provider/retry fixes | **update** (smoke-gated) | HIGH |
| `pi-intercom` | 0.6.0 | 0.6.0 | no release delta; obsolete Pi/TUI peers leave a Pi 0.82 smoke requirement | **no action** | MEDIUM |
| `@tmustier/pi-files-widget` | 0.2.0 | 0.2.0 | no stable delta | **no action** | HIGH |
| `@ff-labs/pi-fff` | 0.10.1 | 0.10.1 | no stable delta; nightlies excluded | **no action** | HIGH |
| `@juicesharp/rpiv-todo` | 2.1.0 | 2.1.0 | no delta | **no action** | HIGH |
| `rpiv-ask-user-question` | 2.0.0 | 2.1.0 | exact pin omitted from Pi checks; notes, collapse, blocked event, long-session robustness | **update** | HIGH |
| `@narumitw/pi-github-pr` | 0.23.0 | 0.28.0 | current semver range holds 0.23; package-specific runtime is unchanged across exact source diff | **no action** | HIGH |
| `rpiv-btw` | 2.0.0 | 2.1.0 | exact pin omitted from Pi checks; docs/tarball-only delta | **no action** | HIGH |
| `rpiv-web-tools` | 2.1.0 | 2.1.0 | no delta | **no action** | HIGH |
| `pi-lens` | 3.8.71 | 3.8.71 | no stable delta; formatter canon remains T-147 | **no action** | HIGH |
| `pi-agent-browser-native` | 0.2.71 | 0.2.72 | wrapper rebaseline 0.32.2→0.33.0; current doctor fails | **test** | HIGH |
| underlying `agent-browser` | 0.27.0 | 0.33.0 | outside Pi updater; latest requires Node >=24 | **test** with wrapper/Node | HIGH |
| `pi-prompt-template-model` | 0.10.0 | 0.10.0 | current but no verified extension-specific consumer; overlaps native prompts/pi-subagents/T-152 | **remove** after preflight | MEDIUM-HIGH |
| `pi-subagents` | custom `b7c531c` / package 0.35.1 | upstream stable 0.35.1 | exact git pin; stable lacks custom recovery; main is divergent preview | **hold** | HIGH |
| Herdr | 0.7.5 stable | 0.7.5 stable | no forward stable delta | **no action** | HIGH |
| Landstrip | 0.17.31 via `pi-landstrip` carrier | 0.17.34 | qq boundary pin plus install-shape drift | **replace** after full test | HIGH |
| OpenWiki | 0.1.2 | 0.2.3 | safety/workflow/output improvements plus default telemetry | **test** | HIGH |
| Backlog.md | 1.48.0 | 1.48.0 | no delta | **no action** | HIGH |

## Findings and qq implications

### Node and Context7 — HOLD global Node; TEST isolated Node 24 and an exact Context7 pin

**Observed, HIGH:** the host runs Homebrew `node@22` 22.22.3, an LTS line that satisfies current Pi and wrapper requirements. Official Node data lists 24.18.0 as the newer LTS; browser 0.33.0 specifically requires Node >=24. `.mcp.json` launches `npx -y @upstash/context7-mcp@latest`; registry `latest` was 3.2.4 on the assessment date, so there is no durable installed/ref baseline and each cold launch may fetch different code.

**Inference, HIGH:** a machine-wide Node move is not justified solely to repair one browser integration; isolate Node 24 in the browser trial first. Context7's moving alias weakens reproducibility and adds supply-chain/change-without-diff exposure on a first-source research path. This is not a known 3.2.4 defect; the issue is unpinned execution.

**Smallest Check/rollback:** trial Node 24 only in the isolated browser prefix. For Context7, replace `@latest` with exact 3.2.4 in a temporary Change, run representative research/review lookups, then keep the pin if green; rollback restores the prior config. Do not execute the fetched MCP merely to inspect its version.

### Pi 0.82.0 — UPDATE

**Observed, HIGH:** official notes add constrained JSON-schema/grammar tool sampling, Kimi Code/OpenRouter OAuth, Bash session/model metadata, RPC Bash streaming, and provider/retry fixes. They also update `protobufjs` from the installed affected 7.6.4 to patched 7.6.5. The advisory requires attacker-influenced `.proto` parsing, so this is a moderate hardening benefit rather than evidence of an active qq exploit.

**Inference, HIGH:** constrained sampling may improve schema-bound tool calls only when a tool opts in. It does not replace Completion Envelopes, owner verification, fresh review, or T-152's missing fail-closed request-local role profile. Bash metadata may complement observation but does not replace qq's trace IDs and parent-span propagation.

**Smallest Check/rollback:** isolated 0.82 install; load all 12 package resources and mounted qq extensions; verify footer, guard, handoff, watch, ask UI, pi-intercom, and one real confined structured-output child. Roll back to exact 0.81.1 and restart if any contract fails.

### Browser wrapper/runtime — TEST

**Observed, HIGH:** wrapper doctor exits 1 with `expected 0.32.2, found 0.27.0` and says no backward-compatibility shims. Upstream's own 0.27 doctor can still launch a disposable browser, but that does not validate the native wrapper's target contract. Candidate wrapper 0.2.72 targets browser 0.33.0; registry metadata requires Node >=24, host is 22.22.3.

**Inference, HIGH:** an extension-only update would remain incoherent. Browser and `rpiv-web-tools` are complementary: browser owns rendered/stateful interaction, accessibility, HAR, and authenticated sessions; web-tools owns text search/fetch.

**Smallest Check/rollback:** isolated Node 24 prefix with browser 0.33.0 and wrapper 0.2.72; require both doctors green and a disposable navigate/snapshot/click/a11y/HAR/domain-policy/teardown probe. Promote or roll back all three together.

### Landstrip — TEST, then REPLACE install carrier

**Observed, HIGH:** current source requires `@landstrip/landstrip-linux-x64@0.17.31` directly and warns not to `pi install` the extension; live npm root instead has direct `pi-landstrip@0.17.31`, which carries the binary transitively. It is absent from Pi settings, so it is not currently wrapping accountable Bash. qq independently pins the boundary version. Compared 0.17.32–0.17.34 changes include correct existing-path `mkdir` behavior and clearer partial-Landlock rights diagnostics; no change closes decision-8's open network-egress boundary.

**Inference, HIGH:** direct platform installation is the smaller, less activation-prone state. Because the engine is a security boundary, release notes cannot authorize promotion.

**Smallest Check/rollback:** select 0.17.34 through `QQ_LANDSTRIP_BIN`; run the complete native role/confinement suite, existing-path mkdir, partial-rights, nested teardown, structured-output capture, and expected open egress. If green, update Repository pins/CI/docs and replace the carrier in one Change. Roll back all pins and binary to 0.17.31.

### OpenWiki 0.2.3 — TEST

**Observed, HIGH:** 0.2.3 normalizes the sole docs-only write guard before prefix checking, preserves customized update workflows, atomically writes credentials, isolates MCP credential inheritance, and adds Mermaid/OKF. Its published package also sends one default PostHog `openwiki_run` event for init/update unless `OPENWIKI_TELEMETRY_DISABLED=1` or `DO_NOT_TRACK=1`. The live 0.1.2 already includes ChatGPT OAuth, making `README.md:311-316`'s source-build debt stale.

**Inference, HIGH:** upstream now owns more safety, but still refreshes root agent files and init can create a workflow; qq's baseline restoration remains useful. Likely shrinkage is stale README compatibility prose, not wholesale removal of `qq-openwiki` guards.

**Smallest Check/rollback:** isolated 0.2.3 executable in the dedicated update worktree; explicitly decide/inspect/disable telemetry before live promotion; run `tests/test-qq-openwiki.sh`, prove byte restoration, OAuth continuity, and review one complete generated diff for Mermaid/OKF churn. Roll back executable to 0.1.2 without rewriting credentials.

### pi-subagents — HOLD exact custom ref

**Observed, HIGH:** installed `b7c531c` adds recovery when successful terminal structured output follows an earlier tool error. Stable 0.35.1 is older. Upstream main has 15 post-parent commits for Pi 0.81 compatibility, TypeBox bundling, artifact/output isolation, async completion/waits, progress, and FleetView, but is untagged and lacks the custom commit.

**Inference, HIGH:** FleetView may later subsume part of `qq-status`/cockpit detail glass, but only after a stable release proves qq's role/run/failure fields. Bridge-off configuration also reduces the value of upstream intercom wake fixes.

**Smallest Check/rollback:** rebase/cherry-pick the custom fix over a future stable in a temporary integration branch; test strict envelopes, prior-error recovery, async reload/completion, output isolation, session-root confinement, trusted role identity, and Pi 0.82. Rollback is the exact `b7c531c` pin.

### Extension territory

- **Prompt workflows, MEDIUM-HIGH:** native Pi prompt templates are sufficient for qq's new `/update`. `pi-prompt-template-model` adds model fallback, Skill injection, loops/chains/best-of-N, deterministic commands, worktrees, and a pi-subagents bridge, but none is presently consumed. pi-subagents owns bounded execution, and T-152 seeks one install-wide model-role authority. Prefer native prompts + pi-subagents and remove the dormant overlapping extension after a final scan outside `~/projects`.
- **rpiv family, HIGH:** no consolidation. Todo is ephemeral session checklist state, Ask is structured agent→operator clarification, Btw is an operator→same-session side thread, and web-tools is search/fetch. They own distinct states. Ask's new blocked event is available but qq has no listener; it does not replace Herdr lifecycle.
- **PR status, HIGH:** `pi-github-pr` remains passive current-branch status while `qq_pr_watch` watches one exact PR for terminal disposition. Retain both; reassess only if upstream adds exact-PR wake semantics.
- **Messaging/lifecycle, HIGH:** pi-intercom owns root Pi-to-Pi messaging; pi-subagents owns bounded children with its intercom bridge deliberately off; Herdr owns terminal placement/operator-visible lifecycle. No current surface subsumes another.

## Gaps and residual risks

- **MEDIUM:** the configured Context7 MCP was unavailable to the confined researcher, so no live lookup or installed baseline was claimed; official repositories/releases, registry metadata/tarballs, installed source, and safe live commands were used instead.
- **MEDIUM:** a fresh `pi list` inside the confined researcher was inconclusive because its config was redirected and the real settings lock was read-only. The accountable session independently ran `pi list` and reconciled all 12 entries against safe settings fields and installed package trees.
- **HIGH:** no candidate was installed or promoted. Compatibility recommendations remain proposed follow-up Checks.
- **MEDIUM:** pi-intercom has no newer stable and carries old Pi/TUI peers; Pi 0.82 behavior remains unproven.
- **MEDIUM:** prompt-template-model consumer search covered `~/.pi/agent` and `~/projects`; another project root may depend on it.
- **HIGH:** OpenWiki telemetry is an operator-owned privacy decision; no upgrade may silently choose it.
- **HIGH:** browser wrapper/runtime mismatch is a verified live defect.

## Sources

Primary sources that shaped the conclusion:

- [Node release lines](https://nodejs.org/en/about/previous-releases) and [official distribution index](https://nodejs.org/dist/index.json)
- [Context7 MCP registry metadata](https://registry.npmjs.org/%40upstash%2Fcontext7-mcp) and [repository](https://github.com/upstash/context7)
- [Pi 0.82.0 release](https://github.com/earendil-works/pi/releases/tag/v0.82.0) and [compare](https://github.com/earendil-works/pi/compare/v0.81.1...v0.82.0)
- [`protobufjs` advisory](https://github.com/advisories/GHSA-j3f2-48v5-ccww)
- [rpiv 2.0.0→2.1.0](https://github.com/juicesharp/rpiv-mono/compare/v2.0.0...v2.1.0) and [Ask changelog](https://raw.githubusercontent.com/juicesharp/rpiv-mono/v2.1.0/packages/rpiv-ask-user-question/CHANGELOG.md)
- [Browser wrapper 0.2.72](https://github.com/fitchmultz/pi-agent-browser-native/releases/tag/v0.2.72) and [agent-browser 0.33.0](https://github.com/vercel-labs/agent-browser/releases/tag/v0.33.0)
- [Landstrip 0.17.34](https://github.com/landstrip/landstrip/releases/tag/0.17.34) and [0.17.31→0.17.34 compare](https://github.com/landstrip/landstrip/compare/0.17.31...0.17.34)
- [Custom pi-subagents recovery commit](https://github.com/hypermemetic-ai/pi-subagents/commit/b7c531c238469e43866a1fe6697cb44279158c1c), [stable 0.35.1](https://github.com/nicobailon/pi-subagents/releases/tag/v0.35.1), and [post-parent main comparison](https://github.com/nicobailon/pi-subagents/compare/f1540b09283a1c176a0c721878453c6382ecd399...main)
- [OpenWiki 0.2.3](https://github.com/langchain-ai/openwiki/releases/tag/0.2.3), [docs-only traversal fix](https://github.com/langchain-ai/openwiki/pull/406), and [workflow preservation](https://github.com/langchain-ai/openwiki/pull/285)
- [Herdr 0.7.5](https://github.com/ogulcancelik/herdr/releases/tag/v0.7.5)
- [Backlog.md 1.48.0](https://github.com/MrLesk/Backlog.md/releases/tag/v1.48.0)
- npm registry metadata for every npm component, including [`openwiki`](https://registry.npmjs.org/openwiki), [`agent-browser`](https://registry.npmjs.org/agent-browser), and [Pi](https://registry.npmjs.org/%40earendil-works%2Fpi-coding-agent)
- Local source and checks: `.mcp.json:1-8`; `README.md:58-146,169-202,291-352`; `bin/qq-openwiki:15-136`; `bin/qq-handoff:1-20`; `bin/qq-observe:70-82`; `bin/qq-dispatch:235-247`; `delegation/policies/roles.json:1-22`; T-147; T-152; installed Pi `dist/core/package-manager.js:838-970`; live Python/package versions; live wrapper doctor.
