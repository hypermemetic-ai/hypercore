---
id: doc-59
title: >-
  pi-sweep F — Methodology skills (grilling, diagnosing, operator-input, uat,
  writing)
type: other
created_date: '2026-07-19 16:33'
updated_date: '2026-07-19 16:35'
tags:
  - research
---
# pi-sweep F — Methodology skills: reconciled research report

**Owning task:** T-93 — Evaluate pi-ecosystem replacements for qq surfaces.
**Cluster:** F — Methodology skills (grilling, diagnosing-bugs, operator-input, uat-signoff, writing-for-clients).
**Research date:** 2026-07-19. **Overall confidence:** HIGH on migration/keep decisions; MEDIUM on absolute catalog exhaustiveness (~5,300 rapidly changing packages).
**Settles:** Adopt selected `@tw93/waza` skills (`think`, `hunt`, `write`) via pi package filtering; slim `grilling` and `writing-for-clients` to their qq deltas; retire most of `diagnosing-bugs` keeping the diagnosis-only authorization boundary; keep `operator-input` and `uat-signoff` as-is; adopt `@juicesharp/rpiv-ask-user-question` as question UI. Do not import Superpowers/BigPowers lifecycles wholesale.
**Decision this informs:** the waza adoption + skill slimming is its own later Change with its own alignment; this document is evidence, not authorization.

## Owning-agent verification (2026-07-19)

Spot-checked before reconciliation: `@tw93/waza` on the npm registry at 3.32.0 (report cited 3.31.2 — a newer release landed during the sweep; MIT; modified 2026-07-19, i.e. actively maintained). The `think`/`hunt`/`write` skill inventory was confirmed in the repository tree.

## Cross-cluster adjudications

- **`@dietrichgebert/ponytail` — OVERRIDDEN TO REJECT.** This report below shortlists ponytail as minimalism reinforcement; doc-60 rejects it. Owning-agent adjudication: **reject**. qq already owns the "solve the agreed problem — no more, no less" invariant in AGENTS.md; an always-on methodology pack duplicates the agreement and grows the exact instruction surface `tools/ratchet.sh` budgets. The qq-specific argument wins over the generic content-quality argument.
- **Plan-mode packages (`@narumitw/pi-plan-mode` vs Plannotator):** consistent with doc-54 — adopt one, not both; doc-54's recommendation (`pi-plan-mode` as the terminal-native default, Plannotator when visual annotation matters) stands.
- **`@juicesharp/rpiv-ask-user-question`:** no conflict; complements grilling's question batching without touching decision policy.

---

# Findings report: Pi replacements for qq methodology skills

**Question.** What maintained Pi-native package or combination can replace qq’s operator alignment, bug diagnosis, operator-input handling, UAT sign-off, and client-writing skills, and which unrelated skill-pack QoL additions merit adoption?

**Research date.** July 19, 2026.

**Overall confidence.** **HIGH** on the recommended migration and keep-as-is decisions; **MEDIUM** on absolute catalog exhaustiveness because the Pi catalog has roughly 5,300 rapidly changing packages and several low-adoption sources were not fully fetchable.

**What this settles.** No package faithfully replaces all five skills. The best combination is:

1. **ADOPT selected `@tw93/waza` skills:** `think`, `hunt`, and `write`.
2. **SLIM**, rather than delete, qq’s `grilling` and `writing-for-clients` to their qq-specific deltas.
3. **RETIRE most of `diagnosing-bugs`**, retaining only qq’s diagnosis-only authorization boundary.
4. **KEEP `operator-input` and `uat-signoff` as-is.** No maintained standalone package matches them.
5. **ADOPT `@juicesharp/rpiv-ask-user-question` as a UI complement**, not a methodology replacement.
6. Do **not** import Superpowers, BigPowers, or another full lifecycle wholesale.

No installs or repository changes were made.

## qq baseline and recommended disposition

Percentages below are qualitative content judgments, not mechanical measurements.

| qq skill | Generic versus qq-bound | Verdict | Residual qq must retain |
|---|---:|---|---|
| [`grilling`](/home/qqp/projects/qq/skills/grilling/SKILL.md) | About 55% generic / 45% qq-specific | **SLIM around Waza `think`** | Backlog evidence and disposition citations; Task decision ledger; dispositions not transferring automatically; Change/Herdr boundaries; accountable owning Actor versus delegated Actor; compact alignment brief as the default rather than a full interview. **[HIGH]** |
| [`diagnosing-bugs`](/home/qqp/projects/qq/skills/diagnosing-bugs/SKILL.md) | About 90–95% generic | **REPLACE with Waza `hunt`** | One explicit policy: diagnosis does not authorize a fix; stop after establishing cause unless the assignment includes implementation. This could live in a very small skill or repository instruction. **[HIGH]** |
| [`operator-input`](/home/qqp/projects/qq/skills/operator-input/SKILL.md) | About 90% generic, but unusually compact and specific in outcome | **KEEP AS-IS** | The whole useful contract: exhaust self-service first, batch operator-only work, pre-stage the exact page/paste point, keep secrets in their destination rather than chat, validate immediately, and resume autonomously. Question-dialog packages cover none of the browser/credential handoff discipline. **[HIGH]** |
| [`uat-signoff`](/home/qqp/projects/qq/skills/uat-signoff/SKILL.md) | About 90% generic | **KEEP AS-IS** | Hands-on owner acceptance after autonomous Checks; one user-observable outcome at a time; record what the owner actually observed; recheck failures; explicit accepted/skipped/gap result; separate authorization for destructive or outbound actions. **[HIGH]** |
| [`writing-for-clients`](/home/qqp/projects/qq/skills/writing-for-clients/SKILL.md) | About 65–70% generic editorial method / 30–35% operator-earned register | **SLIM around Waza `write`** | Buyer/procurement audience; statement titles that carry the argument; particulars, numbers, names, and dates over adjectives; preserving limitations and failure behavior as trust evidence; saying each claim once; render review; the validated operator probe/example. **[HIGH]** |

All five files are dense rather than filler: 63, 14, 45, 28, and 151 lines respectively. `skills/.system/` is absent. qq mounts one canonical skill root into Pi, Claude Code, and Codex rather than copying it; see [`README.md`](/home/qqp/projects/qq/README.md:49). That makes upstream package filtering preferable to mirroring upstream skill text locally.

## Pi 0.80.10 native affordances

Pi already supplies the mechanics needed for a small upstream-plus-local-delta design:

- At startup Pi loads only skill names and descriptions; full `SKILL.md` bodies are loaded on demand. `/skill:name` forces a skill and appends arguments. [`disable-model-invocation: true` hides a skill from automatic routing](https://pi.dev/docs/latest/skills), allowing a local delta to remain manually invocable if desired. **[HIGH]**
- Package settings can select exact skill paths, exclude resources, or set a resource class to `[]`. `pi config` offers the same enable/disable surface interactively. Thus Waza can be limited to `think`, `hunt`, and `write`, and Superpowers could theoretically be limited to `systematic-debugging` while excluding its startup extension. [Pi package filtering documentation](https://pi.dev/docs/latest/packages). **[HIGH]**
- Duplicate skill names warn and keep the first discovered skill. Waza’s names do not directly collide with qq’s, but leaving both generic bodies auto-routable would still create semantic double-routing. **[HIGH]**
- Native prompt templates provide `$1`, `$@`, defaults, and argument slicing, but no model routing or conditional workflow logic. They are sufficient for thin manual entry points but do not replace any methodology. [Pi prompt-template documentation](https://pi.dev/docs/latest/prompt-templates). **[HIGH]**
- Packages and skill helper scripts have full system authority. Selective loading reduces prompt conflict, not execution risk. **[HIGH]**

## Candidate findings

### `@tw93/waza` — ADOPT selectively

**What it is.** A compact MIT skill pack, version 3.31.2 published July 10, 2026, with zero declared dependencies. The catalog reported 1,263 monthly downloads; the repository had roughly 6.5k stars and 437 commits. Pi has a direct npm install path. [Package record](https://pi.dev/packages/%40tw93/waza), [source repository](https://github.com/tw93/Waza). **[HIGH]**

**Inventory.** Eight skills: `think`, `ui`, `check`, `hunt`, `write`, `learn`, `read`, and `health`.

**Head-to-head findings.**

- **Operator alignment — ADOPT `think`, keep a local delta.** `think` inspects current repository rules and prior decisions, distinguishes lightweight/evaluation/triage modes, gives one recommended approach, exposes fragile assumptions, requires approval, and hands off scope, non-scope, verification, manual acceptance, dependencies, and rollback. It is substantially richer than generic grilling while staying outside a replacement project cockpit. It does not understand qq’s Backlog citations, decision ledger, disposition semantics, or owning/delegated Actor distinction. [Actual `think` skill](https://github.com/tw93/Waza/blob/main/skills/think/SKILL.md). **[HIGH]**

- **Bug diagnosis — ADOPT `hunt`.** It requires a specific hypothesis, a discriminating probe, runtime evidence when the hypothesis concerns timing or lifecycle, a lower-layer baseline for tooling symptoms, deterministic reproduction, regression bisecting, and a sibling-pattern blast search. It stops after three failed hypotheses and distinguishes evidence from guesses. This is the strongest debugging text found. Its workflow continues into fix and regression verification, so qq must preserve its diagnosis-only authorization boundary. [Actual `hunt` skill](https://github.com/tw93/Waza/blob/main/skills/hunt/SKILL.md). **[HIGH]**

- **Operator input — REJECT as replacement.** Waza has no skill for reducing browser, login, secret, or other operator-only handoffs. **[HIGH]**

- **UAT sign-off — REJECT as replacement.** `think` can include manual acceptance criteria and `check` verifies work, but neither walks the owner through hands-on acceptance and records the owner’s observations. **[HIGH]**

- **Client writing — ADOPT `write`, keep a local delta.** `write` locks audience and intent, grounds public claims in live artifacts, preserves factual meaning, and has a detailed catalogue of formulaic AI prose patterns. It covers most of qq’s generic anti-slop and editing rules. It lacks qq’s buyer/procurement register, argument-carrying titles, particularity rules, explicit treatment of limits as credibility, and the operator-validated probe. [Actual `write` skill](https://github.com/tw93/Waza/blob/main/skills/write/SKILL.md), [English reference](https://github.com/tw93/Waza/blob/main/skills/write/references/write-en.md). **[HIGH]**

**Fit and caveats.** `pi install npm:@tw93/waza` is the cleanest install story among the substantive packs. The package is Pi-native but declares no explicit minimum Pi version, so compatibility with 0.80.10 remains inferred rather than contractually stated. Each inspected skill asks the agent to run a non-blocking once-per-conversation update script; the script reportedly reads only a public version file once daily, but it is still outbound behavior worth knowing about. **[MEDIUM]**

**Overall verdict.** **ADOPT `think`, `hunt`, and `write`; filter out the rest initially.** Do not also install Superpowers debugging. **[HIGH]**

### Official `obra/superpowers` — SHORTLIST only as the debugging alternative

**What it is.** The canonical upstream methodology, MIT, version 6.1.1 released July 2, 2026. It had about 257k stars and 628 commits and explicitly supports Pi through `pi install git:github.com/obra/superpowers`. Its Pi package includes a startup extension that injects `using-superpowers`. [Repository and Pi install details](https://github.com/obra/superpowers). **[HIGH]**

**Inventory.** Fourteen skills:

`test-driven-development`, `systematic-debugging`, `verification-before-completion`, `brainstorming`, `writing-plans`, `executing-plans`, `dispatching-parallel-agents`, `requesting-code-review`, `receiving-code-review`, `using-git-worktrees`, `finishing-a-development-branch`, `subagent-driven-development`, `writing-skills`, and `using-superpowers`.

**Per-qq verdicts.**

- **Alignment — REJECT.** `brainstorming` is mandatory before broad categories of creative work, asks one question at a time, writes Superpowers design artifacts, and hands off into its planning lifecycle. It is less compatible with qq’s default compact alignment brief and existing Backlog/Task rails. [Actual `brainstorming` skill](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md). **[HIGH]**
- **Diagnosis — SHORTLIST `systematic-debugging`.** Its four phases—root-cause evidence, working-pattern comparison, one falsifiable hypothesis/one variable, then causal fix and verification—are excellent and very close to qq’s current method. Waza `hunt` wins on regression, runtime instrumentation, blast-radius search, npm fit, and covering three qq skills in one pack. [Actual `systematic-debugging` skill](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md). **[HIGH]**
- **Operator input — REJECT.** No equivalent. **[HIGH]**
- **UAT — REJECT.** `verification-before-completion` concerns fresh agent-run evidence before a completion claim, not owner-observed acceptance. **[HIGH]**
- **Client writing — REJECT.** No client-writing skill. **[HIGH]**

If chosen instead of Waza, load only `systematic-debugging` and exclude the startup extension and other skills through Pi’s package filters. Installing the full package would import a competing mandatory lifecycle.

**Forks and ports.**

- [`superpowers-zh`](https://pi.dev/packages/superpowers-zh) ships 20 skills: the 14 upstream skills plus Chinese code review, Git workflow, technical documentation, commit conventions, MCP builder, and workflow runner. It is actively maintained and npm-native, but qq is English-first and gains no methodology fidelity from the translation layer. **REJECT. [HIGH]**
- [`@weiping/pi-superpowers`](https://pi.dev/packages/%40weiping/pi-superpowers) ships the 14 ported skills, Chinese triggers, prompts, and a Pi extension, but was at upstream 5.1-era content while official Superpowers was 6.1.1. **REJECT in favor of upstream. [HIGH]**
- Older `pi-superpowers`, `pi-gauntlet`, and adapter packages offer no advantage over the now-official Pi support. **REJECT. [MEDIUM]**

### `bigpowers` — REJECT the suite; HOLD no standalone component

**What it is.** A large MIT package, version 2.77.2 published July 19, 2026, with 36.8k monthly downloads. It declares both skills and prompts and implements a six-phase methodology using `specs/state.yaml`, `release-plan.yaml`, epics, risk levels, branch gates, quality thresholds, and explicit `next_skill` handoffs. [Package and lifecycle](https://pi.dev/packages/bigpowers), [repository](https://github.com/danielvm-git/bigpowers). **[HIGH]**

**Actual inventory.** The package page advertised 73 skills and the README said 72, while the live GitHub directory exposed 77 names. That metadata drift is unresolved. The observed directory contained:

`align-grid`, `assess-impact`, `audit-code`, `audit-plan`, `build-epic`, `change-request`, `commit-message`, `compose-workflow`, `context7-mcp`, `craft-skill`, `deepen-architecture`, `define-language`, `define-success`, `delegate-task`, `deploy`, `design-interface`, `develop-tdd`, `diagnose-root`, `diagnose-stall`, `dispatch-agents`, `edit-document`, `elaborate-spec`, `enforce-first`, `evolve-skill`, `execute-plan`, `extract-design`, `fix-bug`, `gate-trace`, `grill-me`, `grill-with-docs`, `guard-git`, `hook-commits`, `inspect-quality`, `investigate-bug`, `kickoff-branch`, `maintain-wiki`, `map-codebase`, `migrate-spec`, `model-domain`, `orchestrate-project`, `organize-workspace`, `plan-refactor`, `plan-release`, `plan-tests`, `plan-work`, `publish-package`, `quick-fix`, `release-branch`, `request-review`, `research-first`, `reset-baseline`, `respond-review`, `run-benchmark`, `run-evals`, `run-planning`, `scope-work`, `search-skills`, `security-review`, `seed-conventions`, `session-state`, `setup-environment`, `simulate-agents`, `slice-tasks`, `smoke-test`, `spike-prototype`, `stocktake-skills`, `survey-context`, `terse-mode`, `trace-requirement`, `using-bigpowers`, `validate-contracts`, `validate-fix`, `verify-work`, `visual-dashboard`, `wire-ci`, `wire-observability`, and `write-document`. [Live skill directory](https://github.com/danielvm-git/bigpowers/tree/main/skills). **[HIGH]**

**Per-qq verdicts.**

- **Alignment — REJECT.** `grill-me`, `grill-with-docs`, and planning skills overlap generic grilling but write into BigPowers’ own specification hierarchy and lifecycle.
- **Diagnosis — REJECT.** `diagnose-root`, `investigate-bug`, `fix-bug`, and `validate-fix` are not compelling enough to justify a second cockpit; Waza and Superpowers supply stronger standalone paths.
- **Operator input — REJECT.** No equivalent for operator-only handoffs.
- **UAT — REJECT despite close content.** `verify-work` does step-by-step manual UAT, but it hard-requires a non-main feature branch, active story YAML, `risk:` levels, preflight commands, verification files, security/blind-spot gates, `execution-status.yaml`, and a `state.yaml` handoff to `audit-code`. It is not separable without adopting BigPowers’ rails. [Actual `verify-work` skill](https://raw.githubusercontent.com/danielvm-git/bigpowers/main/skills/verify-work/SKILL.md). **[HIGH]**
- **Client writing — REJECT.** `write-document` and `edit-document` are general documentation methods, not the qq buyer-facing register.

The package declares generated prompt templates, but their exact current file inventory could not be independently enumerated. The documented examples mirror the lifecycle skills as slash commands.

### Human-UAT comparators — useful content, not replacements

- [GSD’s `verify-work` workflow](https://github.com/gsd-build/get-shit-done/blob/main/get-shit-done/workflows/verify-work.md) is the closest conceptual match: it extracts user-testable deliverables, presents one at a time, records pass/fail, and diagnoses failures. It is embedded in GSD’s `.planning/` phase artifacts rather than published as a standalone Pi skill. **HOLD as reference only. [HIGH]**
- [`@firstpick/pi-skill-acceptance-tester`](https://pi.dev/packages/%40firstpick/pi-skill-acceptance-tester?page=35) supplies one `acceptance-tester` skill, but its published contract is an agent-run readiness/go-no-go gate. It does not establish owner-observed hands-on acceptance. **REJECT as `uat-signoff` replacement. [MEDIUM]**
- [`pi-evaluate`](https://pi.dev/packages/pi-evaluate?page=37) compares a contract with outputs and reports satisfied/partial/unsatisfied/unclear without fixing gaps. That is useful agent evaluation, but not UAT dialogue. **REJECT as replacement. [HIGH]**

The honest conclusion is to keep qq’s 28-line UAT skill.

### Operator-question and grilling tools

#### `@juicesharp/rpiv-ask-user-question` — ADOPT as QoL

This is an MIT extension, version 1.20.0, with 22.9k monthly downloads. It adds one `ask_user_question` tool supporting one to four tabbed questions, single- or multi-select choices, option previews, notes, answer review, and free-text fallback. It ships no competing methodology skill. [Package and tool schema](https://pi.dev/packages/%40juicesharp/rpiv-ask-user-question). **[HIGH]**

It is an excellent presentation layer for qq’s batched consequential questions, but it does not decide when to ask, record Backlog dispositions, or handle operator-only browser and secret handoffs.

#### Alternatives

- [`pi-ask-user`](https://pi.dev/packages/pi-ask-user) adds a strong interactive tool plus a 162-line mandatory `ask-user` decision-gate skill. The skill correctly requires evidence first and avoids repeated questions, but enforces one decision per call and duplicates much of `grilling`. Choose RPIV’s extension-only package instead; if `pi-ask-user` is preferred for its TUI, filter out its bundled skill. [Actual bundled skill](https://github.com/edlsh/pi-ask-user/blob/main/skills/ask-user/SKILL.md). **[HIGH]**
- [`@firstpick/pi-extension-grill-me`](https://pi.dev/packages/%40firstpick/pi-extension-grill-me?page=48) records a one-question-at-a-time interview in `.pi/grill-me/state.json` and `GRILL-ME.md`. Its foreign artifacts, one-at-a-time protocol, low adoption, and lack of qq citations make it inferior to Waza `think` plus the qq delta. **REJECT. [MEDIUM]**

### Planning and prompt surfaces

- [`@plannotator/pi-extension`](https://pi.dev/packages/%40plannotator/pi-extension) is a substantial visual plan-review extension: browser annotations, approve/deny-with-notes, plan diffs, code-review annotation, message annotation, progress tracking, and restricted planning writes. Version 0.23.1 declares Pi ≥0.74, so it is compatible with 0.80.10. It replaces no qq skill because it supplies the review surface rather than accountable alignment semantics. **SHORTLIST as QoL. [HIGH]**
- [`@narumitw/pi-plan-mode`](https://pi.dev/packages/%40narumitw/pi-plan-mode) is the lean terminal alternative: read-only exploration, one to three material questions, a stored decision-complete plan, and implement/stay/discard choices. Version 0.20.0 requires Pi ≥0.80.6. It likewise does not replace `grilling`. Choose it instead of, not alongside, Plannotator when a browser review surface is unnecessary. **SHORTLIST. [HIGH]**
- [`pi-prompt-template-model`](https://pi.dev/packages/pi-prompt-template-model) adds model, thinking, skill injection, conditionals, chains, loops, and best-of-N behavior to prompt-template frontmatter. It ships machinery and documentation rather than methodology templates. Native Pi templates already suffice for thin qq entry points. **HOLD unless model-bound slash commands become an explicit need. [HIGH]**

### Other lifecycle suites

The catalog also contains several packages with grilling, planning, or verification inside full replacement workflows:

| Package | Relevant inventory | Verdict |
|---|---|---|
| [`@juicesharp/rpiv-pi`](https://pi.dev/packages/%40juicesharp/rpiv-pi) | Discover, research, design, plan, implement, validate, review; `.rpiv/artifacts` | **REJECT:** imports another lifecycle and decision-artifact hierarchy. **[MEDIUM]** |
| [`nightmanager`](https://pi.dev/packages/nightmanager) | Grilling, specifications, TODOs, delegated execution | **REJECT:** foreign end-to-end workflow. **[MEDIUM]** |
| [`gedpi`](https://pi.dev/packages/gedpi) | `.ged` lifecycle and requirements grilling | **REJECT:** foreign cockpit. **[MEDIUM]** |
| [`skynex-pi`](https://pi.dev/packages/skynex-pi) | Seventeen skills including grilling and verification in a HITL/TDD workflow | **REJECT:** overlaps qq far beyond this cluster. **[MEDIUM]** |
| [`@capyup/pi-specs`](https://pi.dev/packages/%40capyup/pi-specs) | Seven specification/questionnaire skills | **REJECT:** project artifact system, not a compact alignment replacement. **[MEDIUM]** |
| `@cnife/pi-change-based-workflow` | Change workflow suite | **REJECT:** catalog marks it deprecated. **[HIGH]** |
| `@7n/rules` | Rule/skill synchronization and conformance tooling | **REJECT for this question:** distribution machinery rather than a methodology replacement. Source verification remained incomplete. **[LOW]** |

## QoL additions that replace nothing qq owns

### 1. `@juicesharp/rpiv-ask-user-question` — ADOPT

Best immediate QoL addition. It makes alignment questions cheaper to answer while leaving qq’s decision policy in control. No skill-name collision and no foreign artifact hierarchy. **[HIGH]**

### 2. `@dietrichgebert/ponytail` — SHORTLIST for adoption

Ponytail supplies six skills/commands: `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, and `ponytail-help`, plus an extension with adjustable intensity. Its core ladder asks whether work needs to exist, already exists, belongs in the standard library or native platform, or can be implemented minimally before introducing new machinery. That strongly reinforces qq’s “solve the agreed problem, no more” invariant without replacing a current skill.

Version 4.8.4 was published June 29, 2026, MIT, zero dependencies, with 25.5k monthly downloads. Its published small benchmark is favorable but only n=4, and the catalog recommends npm while the README’s Pi section still shows git installation and an outdated uninstall form. A temporary trial should precede permanent adoption. [Package, inventory, and benchmark disclosure](https://pi.dev/packages/%40dietrichgebert/ponytail). **[MEDIUM]**

### 3. Plannotator or Pi Plan Mode — choose one if plan review friction exists

- **Plannotator:** richer visual annotations and plan diffs.
- **Pi Plan Mode:** smaller, terminal-native, stricter read-only exploration.

Neither should be treated as the source of alignment decisions; they are interaction surfaces. **[HIGH]**

### 4. Waza `ui` and `health` — SHORTLIST after the core trial

Because Waza would already be installed, `ui` and `health` are low-friction future candidates: screenshot-driven interface iteration and agent-configuration health checks respectively. Their inventories and descriptions were verified, but their full texts were not assessed to the same depth as `think`, `hunt`, and `write`. **[MEDIUM]**

## Recommended end state

A minimal end state would be:

- Waza supplies the maintained generic bodies for planning/alignment, debugging, and prose editing.
- qq retains small, explicit policy adapters for its accountable-operator rails and buyer register.
- `operator-input` and `uat-signoff` remain unchanged because they are already concise and no package provides equivalent outcomes.
- RPIV’s structured-question extension supplies interaction QoL.
- Full workflow suites remain excluded.

This should retire roughly all but a few lines of `diagnosing-bugs`, about half of `grilling`, and roughly two-thirds of `writing-for-clients`, while preserving the behavior that actually distinguishes qq.

## Sources that shaped the conclusions

- Local truth: [`grilling`](/home/qqp/projects/qq/skills/grilling/SKILL.md), [`diagnosing-bugs`](/home/qqp/projects/qq/skills/diagnosing-bugs/SKILL.md), [`operator-input`](/home/qqp/projects/qq/skills/operator-input/SKILL.md), [`uat-signoff`](/home/qqp/projects/qq/skills/uat-signoff/SKILL.md), [`writing-for-clients`](/home/qqp/projects/qq/skills/writing-for-clients/SKILL.md), and [`README.md`](/home/qqp/projects/qq/README.md:49) settled current behavior, density, qq vocabulary, and mount topology.
- [Pi skills](https://pi.dev/docs/latest/skills), [packages](https://pi.dev/docs/latest/packages), and [prompt templates](https://pi.dev/docs/latest/prompt-templates) settled native discovery, frontmatter, filtering, collision, installation, and substitution behavior; these were cross-checked through Context7’s `/earendil-works/pi` index.
- [Waza package](https://pi.dev/packages/%40tw93/waza), [`think`](https://github.com/tw93/Waza/blob/main/skills/think/SKILL.md), [`hunt`](https://github.com/tw93/Waza/blob/main/skills/hunt/SKILL.md), and [`write`](https://github.com/tw93/Waza/blob/main/skills/write/SKILL.md) settled the primary recommendation.
- [Official Superpowers](https://github.com/obra/superpowers), [`systematic-debugging`](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md), and [`brainstorming`](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md) settled its quality and lifecycle mismatch.
- [BigPowers package](https://pi.dev/packages/bigpowers), [skill directory](https://github.com/danielvm-git/bigpowers/tree/main/skills), and [`verify-work`](https://raw.githubusercontent.com/danielvm-git/bigpowers/main/skills/verify-work/SKILL.md) settled inventory, cockpit dependency, and UAT incompatibility.
- [RPIV structured questions](https://pi.dev/packages/%40juicesharp/rpiv-ask-user-question), [Pi Ask User](https://pi.dev/packages/pi-ask-user), [Plannotator](https://pi.dev/packages/%40plannotator/pi-extension), [Pi Plan Mode](https://pi.dev/packages/%40narumitw/pi-plan-mode), and [Ponytail](https://pi.dev/packages/%40dietrichgebert/ponytail) settled the QoL recommendations.
- [GSD verify-work](https://github.com/gsd-build/get-shit-done/blob/main/get-shit-done/workflows/verify-work.md), [Firstpick acceptance tester](https://pi.dev/packages/%40firstpick/pi-skill-acceptance-tester?page=35), and [pi-evaluate](https://pi.dev/packages/pi-evaluate?page=37) settled the negative UAT finding.

## Gaps

- No package was installed or run against Pi 0.80.10. Compatibility is explicit for Plannotator and Pi Plan Mode; for Waza and several smaller packages it is inferred from current Pi catalog publication.
- BigPowers’ published count disagrees with its live directory, and its generated `.pi/prompts` inventory could not be enumerated.
- `@7n/rules` source and exact package page were not fetchable, so its rejection is based on the catalog description and is low-confidence.
- Some very small Firstpick skill sources were not fetchable; their published package contracts were sufficient to reject them as owner-facing UAT replacements, but not to assess every instruction.
- The Pi catalog changes quickly, so the negative claim is “no maintained match found in the catalog as of July 19, 2026,” not proof that no unpublished or newly added skill exists.
- The appropriate size and placement of each qq delta still needs a migration design and behavioral smoke test; this report establishes what must survive, not the exact edit.
