---
id: doc-60
title: 'pi-sweep G — Cockpit QoL and lean machinery (cockpit, ratchet, tests)'
type: other
created_date: '2026-07-19 16:33'
updated_date: '2026-07-19 16:35'
tags:
  - research
---
# pi-sweep G — Cockpit QoL and lean machinery: reconciled research report

**Owning task:** T-93 — Evaluate pi-ecosystem replacements for qq surfaces.
**Cluster:** G — Cockpit (shell file-navigation, yazi/glow, pi theme/TUI) + internal lean machinery (ratchet, shell tests) + whole-catalog QoL sweep.
**Research date:** 2026-07-19. **Overall confidence:** HIGH on replacement conclusions; MEDIUM on adoption recommendations (nothing installed).
**Settles:** Keep the shell cockpit, yazi/glow config, ratchet, and Bash test harness — no package faithfully replaces any of them, and pi's native themes/keybindings/TUI/settings cover the pi side with zero qq machinery. Top QoL trial: `cc-safety-net` (destructive-command defense-in-depth). Ranked trial list below; trial each in isolation with `pi --no-extensions -e <spec>`.
**Decision this informs:** each QoL trial is its own later Change; this document is evidence, not authorization.

## Owning-agent verification (2026-07-19)

Cluster covered the operator's correction that complexity-related methodology machinery stays in scope: the ratchet and test suite were evaluated as first-class surfaces (verdict: keep — no package implements exact-value only-down CI tripwires, and a generic shell-test framework changes syntax without removing fixture value). Catalog scope note: the sweep covered facets, high-adoption listings, and relevant clusters of the ~5,300-package catalog; it did not open every page.

## Cross-cluster adjudications

- **`cc-safety-net` (#1 QoL here):** doc-54 rejected it *as a backlog-guard replacement* — a different question. As destructive-Git/filesystem defense-in-depth it stands as the top trial candidate. Both verdicts hold.
- **`@dietrichgebert/ponytail` (rejected here, short-listed in doc-59):** owning-agent adjudication is **reject** — see doc-59's cross-cluster note for the ruling. This report's reasoning (duplicates qq's owned minimalism invariant; grows ratchet-budgeted prose) is the binding rationale.
- **`pi-simplify`:** complementary note only; it is an agent-driven review pass, not a deterministic gate — the ratchet's role is unchanged.
- **Files-widget / fff / statusline / pi-lsp:** additive trials, no conflicts with other clusters.

---

# Findings report: Pi cockpit and QoL sweep

**Research question:** Can maintained Pi packages or native Pi 0.80.10 capabilities replace qq’s cockpit, ratchet, or shell-test machinery, and which broader Pi QoL additions fit qq?

**Overall confidence:** High on the replacement conclusions; medium on adoption recommendations because no packages were installed or runtime-tested.

**Settled by this research:**

- Keep qq’s shell cockpit, Yazi/Glow configuration, ratchet, and Bash test harness.
- Use native Pi capabilities for Pi-side themes, keybindings, editor integration, sessions, and conversation branching.
- No catalog package is a faithful replacement for the qq cockpit or ratchet.
- A small set of packages merits isolated trials, led by `cc-safety-net`.
- No repository files or package installations were changed.

## 1. Findings for qq-owned surfaces

### Shell file-navigation cockpit — KEEP

qq’s cockpit is more than a file viewer. It:

- Changes the parent shell’s working directory after Yazi exits.
- Evaluates Broot’s generated shell command.
- Resolves the currently focused Herdr worktree.
- Provides `qqroot`, `qqy`, `qqbr`, and their aliases.
- Operates outside Pi as ordinary shell infrastructure.

Those behaviors are visible in [file-navigation.bash](/home/qqp/projects/qq/cockpit/shell/file-navigation.bash) and summarized in [cockpit/README.md](/home/qqp/projects/qq/cockpit/README.md).

Pi extensions cannot replace the parent-shell or Herdr-focus responsibilities. Pi’s shell facility is noninteractive, while its TUI extension API is intended for overlays, widgets, status displays, custom editors, and other in-process UI—not as a general shell file manager. [Pi TUI documentation](https://pi.dev/docs/latest/tui)

Candidate findings:

- **`@tmustier/pi-files-widget@0.2.0` — SHORTLIST as an additive Pi viewer.** It provides an in-terminal tree, changed-file filtering, Git diffs, Markdown rendering, line selection, and inline comments sent back to the agent. Maintenance is current and its parent repository is active. It requires `bat`, `delta`, and `glow`. Fidelity is high for browsing and reviewing files *inside Pi*, but low for cwd changes, Yazi MIME/open behavior, Broot, `qqroot`, or focused-worktree selection. Residual responsibility remains entirely with the shell cockpit. Confidence: high. [Package](https://pi.dev/packages/%40tmustier/pi-files-widget) · [Repository](https://github.com/tmustier/pi-extensions)

- **`@ff-labs/pi-fff@0.10.0` — SHORTLIST for agent-side search.** It adds fast file finding, grep, multi-grep, and `@` completion. Its default additive mode avoids overriding Pi’s core tools. The underlying FFF project is mature, although the Pi package itself is recent. It improves agent discovery; it is not a human file navigator and cannot change shell cwd. Confidence: high. [Package](https://pi.dev/packages/%40ff-labs/pi-fff) · [FFF repository](https://github.com/dmtrKovalenko/fff)

- **`@pandi-coding-agent/mdview@0.1.1` — HOLD.** Small and focused, but effectively unadopted and superseded by the richer files widget. [Package](https://pi.dev/packages/%40pandi-coding-agent/mdview)

- **`pi-markdown-preview@0.10.0` — CONDITIONAL.** Useful for math, Mermaid, browser/PDF export, and complex documents, but its Pandoc and Chromium requirements make it much heavier than qq’s fast Glow path. It should not replace [glow.yml](/home/qqp/projects/qq/cockpit/glow/glow.yml). [Package](https://pi.dev/packages/pi-markdown-preview)

**Conclusion:** Retain the existing cockpit. Trial the files widget only if an in-Pi review surface is valuable enough to justify its extra binaries.

### Yazi and Glow configuration — KEEP

The Yazi configuration is deliberately pane-first, suppresses the preview pane, handles Markdown through `mdcat` or tuned Glow, and supplies project-specific key bindings. See [yazi.toml](/home/qqp/projects/qq/cockpit/yazi/yazi.toml).

Neither Pi’s native Markdown renderer nor the candidate preview extensions reproduce Yazi’s general file operations, opener routing, shell access, or external use. The Pi packages are complementary viewers, not configuration replacements.

### Pi theme and TUI configuration — USE NATIVE PI

There is no qq-owned Pi theme machinery to retire; `cockpit/pi` contains only the sibling-owned backlog guard.

Pi 0.80.10 already supplies the appropriate primitives:

- Built-in and JSON themes, project/global lookup, package-provided themes, `/settings`, 51 semantic color tokens, schema validation, variables, and hot reload. [Themes](https://pi.dev/docs/latest/themes)
- Configurable keybindings with reload support. [Keybindings](https://pi.dev/docs/latest/keybindings)
- External editor support through `$VISUAL` or `$EDITOR`, plus kill-ring editing, undo, image insertion, tool expansion, follow-up queuing, model selection, and tree navigation.
- Widgets, overlays, custom footer/editor components, Markdown, and images through the TUI API. [TUI](https://pi.dev/docs/latest/tui)
- Native model selection, session resume, fork, conversation tree, retry, and compaction. [Settings](https://pi.dev/docs/latest/settings) · [Sessions](https://pi.dev/docs/latest/sessions)

Candidate findings:

- **Native JSON theme — ADOPT if customization is wanted.** This is sufficient and remains inspectable.
- **`pi-terminal-theme@0.2.0` — HOLD.** A reasonable terminal-palette theme, but it adds little over native JSON configuration. [Package](https://pi.dev/packages/pi-terminal-theme)
- **`@narumitw/pi-statusline@0.21.0` — OPTIONAL SHORTLIST.** Current, zero-dependency, and displays model, provider, Git state, path, context, tokens, cost, time, and tool activity. It adds observability without replacing cockpit behavior. [Package](https://pi.dev/packages/%40narumitw/pi-statusline)
- **`pi-powerline-footer@0.7.0` — REJECT.** It replaces more of the editor/viewport, captures mouse and shell behavior, and has documented tmux interaction concerns. That is unnecessarily invasive for qq. [Package](https://pi.dev/packages/pi-powerline-footer)

### Ratchet — KEEP

qq’s [ratchet.sh](/home/qqp/projects/qq/tools/ratchet.sh) implements repository-specific, exact-value, only-down constraints:

- Mandatory-read word count.
- `codex exec` occurrences in skills.
- Vendor flags in skills.
- `shlex` and `bashlex` occurrences in `bin`.
- Controlled baseline updates that may lower but never raise a metric.

Its baselines live in [ratchet-baselines.conf](/home/qqp/projects/qq/tools/ratchet-baselines.conf), and [test-ratchet.sh](/home/qqp/projects/qq/tests/test-ratchet.sh) exercises increased metrics, stale lower values, updates, and malformed/NUL input.

No Pi package found implements this policy. Nearby packages solve different problems:

- **`pi-simplify@0.2.3` — COMPLEMENTARY, not a replacement.** It reviews changed lines and may edit or test them; it is not a deterministic CI gate. [Package](https://pi.dev/packages/pi-simplify)
- **`@dietrichgebert/ponytail@4.8.4` — REJECT.** It injects another always-on minimalism methodology, duplicating qq’s own agreement and increasing the very instruction surface the ratchet measures. [Package](https://pi.dev/packages/%40dietrichgebert/ponytail)
- **`tdd-enforcer@0.3.8` — REJECT.** Its phase locks and private Git-reset rollback do not match qq’s contract-testing model and introduce consequential repository behavior. [Package](https://pi.dev/packages/tdd-enforcer)

### Shell-test approach — KEEP

qq’s tests use a small black-box Bash harness, temporary fixtures, fake executables, captured environment/log output, and occasional real temporary Git repositories. See [tests/helpers.sh](/home/qqp/projects/qq/tests/helpers.sh).

A generic shell framework could change assertion syntax, but it would not remove the important fixtures or contract setup. Adding Bats, ShellSpec, or a Pi-specific TDD layer would add dependencies without replacing the behavior under test.

## 2. Ranked QoL additions

These are exact research specs, not executed installations. Because Pi packages run with the user’s full privileges, each should first be reviewed and trialed alone with `pi --no-extensions -e <spec>`. [Pi package documentation](https://pi.dev/docs/latest/packages)

| Rank | Package specification | Verdict and value | Confidence |
|---|---|---|---|
| 1 | `npm:cc-safety-net@1.0.6` | **TRIAL → likely adopt.** Semantic pre-tool blocking for destructive Git and filesystem commands, including wrapper/interpreter forms. Keep worktree relaxation disabled so uncommitted work remains protected. This is defense-in-depth, not a sandbox or network boundary. MIT; maintained repository with tests and security policy. [Package](https://pi.dev/packages/cc-safety-net) · [Repository](https://github.com/kenryu42/cc-safety-net) | High |
| 2 | `npm:@tmustier/pi-files-widget@0.2.0` | **TRIAL if in-Pi review is wanted.** Best cockpit-adjacent package, but additive only. Requires `bat`, `delta`, and `glow`. | High |
| 3 | `npm:@ff-labs/pi-fff@0.10.0` | **TRIAL in default additive mode.** Fast local agent search with a mature underlying engine. Avoid override mode initially. | High |
| 4 | `npm:@narumitw/pi-lsp@0.20.0` | **SHORTLIST conditionally.** Adds language-agnostic diagnostics and preview-first source fixes without automatically downloading servers. Useful if Bash or other language servers are already on `PATH`; fresh project tests remain authoritative. [Package](https://pi.dev/packages/%40narumitw/pi-lsp) | Medium-high |
| 5 | `npm:pi-lean-ctx@3.9.12` | **BENCHMARK trial only.** Mature, transparent, locally recoverable context reduction with additive defaults and cached rereads. It also requires the external `lean-ctx` binary, adding operational machinery. Do not start in replacement mode. [Package](https://pi.dev/packages/pi-lean-ctx) · [Repository](https://github.com/yvgude/lean-ctx) | Medium |
| 6 | `npm:@ayulab/pi-rewind@0.4.6` | **DISPOSABLE-REPOSITORY trial only.** Current Git-backed file and conversation rewind. Keep native-tree restore at `ask`, and resume/fork/clone restoration disabled. Explicit rewind can overwrite tracked state and remove checkpoint-managed untracked files; nested repositories are excluded. GPL-3.0. [Package](https://pi.dev/packages/%40ayulab/pi-rewind) · [Repository](https://github.com/ayu-exorcist/oh-my-pi) | Medium |
| 7 | `npm:@narumitw/pi-statusline@0.21.0` | **OPTIONAL.** Low-risk visibility improvement, not a functional gap. | High |

Do not trial multiple core-tool modifiers simultaneously. In particular, context reducers, edit replacements, background Bash overrides, and safety hooks need isolated compatibility checks.

## 3. Conditional additions and holds

- **Rewind alternatives:** `pi-rewind@0.5.0` has attractive diff preview, redo, branch safety, and pruning, but maintenance trails current Pi and its repository has unresolved correctness/platform reports. `pi-undo-redo` is too immature. [Package](https://pi.dev/packages/pi-rewind) · [Repository](https://github.com/arpagon/pi-rewind)

- **Context alternatives:** `@hypabolic/pi-hypa` is easier to install than Lean Context, but remains early-stage, uses a source-available license that only later converts to Apache-2.0, and fails open on several reducer errors. `context-mode` is widely adopted but requires Node 22.5, a separate global package, an MCP configuration, numerous tools, and an auto-loaded skill—contrary to qq’s current preference not to add a Pi MCP server. [Hypa](https://pi.dev/packages/%40hypabolic/pi-hypa) · [context-mode](https://pi.dev/packages/context-mode)

- **Compaction:** Native Pi compaction is the default. Trial `pi-safe-compact@0.1.1` only after observing an actual summarization-overflow failure; it is a targeted fallback, not general optimization. [Package](https://pi.dev/packages/pi-safe-compact)

- **Editing:** Hold both hashline packages unless stale-string edit failures are measured. `pi-hashline-edit-pro` can silently remove duplicated boundary lines, which conflicts with qq’s requirement to make uncertainty visible. The older `pi-hashline-edit` is more conservative but still overrides core read/edit behavior. [Pro package](https://pi.dev/packages/pi-hashline-edit-pro) · [Conservative package](https://pi.dev/packages/pi-hashline-edit)

- **Web:** Avoid installing a universal web layer by default. `pi-web-access` is capable and popular, but brings multiple remote-provider fallbacks, browser-cookie support, file downloads/clones, and an auto-loaded librarian skill. Prefer a narrow provider-specific extension when the provider is already in use. [Package](https://pi.dev/packages/pi-web-access) · [Repository](https://github.com/nicobailon/pi-web-access)

- **Browser automation:** For an explicit browser-QA assignment, use an isolated one-off trial of `npm:pi-agent-browser-native@0.2.71`. It is current and has good snapshot, redaction, stale-reference, and domain-containment features, but should not be part of routine file-oriented work. [Package](https://pi.dev/packages/pi-agent-browser-native) · [Repository](https://github.com/fitchmultz/pi-agent-browser-native)

- **Retry:** Pi’s native retry is normally sufficient. `npm:@narumitw/pi-retry@0.22.0` is justified only if provider-specific websocket/backend errors or hung requests are actually recurring. [Package](https://pi.dev/packages/%40narumitw/pi-retry)

- **Background tasks:** Hold `pi-patty-bg-tasks`; it overrides Bash, adds detached jobs and monitoring, and uses Ctrl+B, creating likely interaction risks with tmux and safety hooks. [Package](https://pi.dev/packages/pi-patty-bg-tasks)

- **Model and session packages:** Native `/model`, model cycling, `/resume`, `/fork`, and `/tree` cover the ordinary need. Provider quota dashboards may be useful, but no general model/session replacement is warranted.

## 4. Suggested adoption checks

Before retaining any candidate:

1. Test it in isolation with all normal extensions disabled.
2. Inspect the pinned package source and transitive dependencies.
3. Exercise it in a disposable repository containing dirty tracked files, untracked files, symlinks, and a nested repository.
4. Verify behavior under qq’s tmux/Herdr environment.
5. Compare observable benefit—latency, tokens, blocked hazards, or review time—against the new commands, binaries, prompt/tool surface, and maintenance burden.

For `cc-safety-net`, the critical check is that destructive reset/checkout/removal variants are blocked while normal temporary-file and branch operations remain usable. For rewind, recovery correctness must be demonstrated before use on valuable work.

## 5. Sources that materially shaped the conclusions

The principal local evidence was the cockpit implementation, Yazi/Glow configurations, ratchet implementation and baselines, and test harness linked above. Native-capability conclusions came from Pi’s current [themes](https://pi.dev/docs/latest/themes), [TUI](https://pi.dev/docs/latest/tui), [keybindings](https://pi.dev/docs/latest/keybindings), [settings](https://pi.dev/docs/latest/settings), [sessions](https://pi.dev/docs/latest/sessions), and [package-security model](https://pi.dev/docs/latest/packages). Package conclusions used Pi’s catalog metadata/readmes and the linked upstream repositories; Context7 corroborated the native Pi documentation but did not alter a conclusion.

## 6. Evidence gaps

- Direct npm package pages returned access errors, so versions, manifests, and readmes were checked through Pi’s catalog mirror and upstream repositories rather than npm’s web UI.
- The catalog changed from roughly 5,305 to 5,310 entries during the sweep and deeper pagination became rate-limited. The sweep covered catalog facets, high-adoption listings, supplied candidates, and relevant package clusters, but did not manually open every package page.
- No package was installed or smoke-tested, so multi-extension hook ordering and override compatibility remain unproven.
- There are no qq workload measurements yet for context reduction, LSP diagnostics, or in-Pi file review; those benefits remain hypotheses until benchmarked.
