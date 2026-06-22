# Report 1 — Agent-Facing Artifacts

**Project:** hypercore · **Report date:** 2026-06-22 · **Synthesis lead** (integrating four independent researchers: Claude Code harness reality, the AGENTS.md field standard + tooling, LLM writing clarity, and methodology→content).

**Scope:** hypercore's always-on `AGENTS.md` (an operating "role anchor") and its five methodology skills — `skills/{design-it-twice,architecture-review,grilling,coherence,depth}/SKILL.md`.

**The governing fact, true of every recommendation below:** these artifacts are *derived*, not authored. `engine/anchor.py` materializes `AGENTS.md`; `engine/methodology.py` renders the five skills from their spec slices; `engine/channels.py` re-runs both on every fold (`CHANNELS = (*methodology.materializers(), anchor.materialize)`, `channels.py:30`). A hand-edit of any `.md` is overwritten on the next fold. So **every fix lands in a spec slice and/or a generator, never in the artifact.** Each recommendation in Part D names that source.

---

## Executive summary — the verdict in a half-page

hypercore's agent-facing artifacts are, on **content and craft, well above the field median**, and their single most-cited design rationale (keep the anchor minimal) is grounded in a real, correctly-cited paper. The derivation discipline — anchor and skills materialized from one spec source on every fold — is genuinely ahead of the field, which mostly hand-edits these files and lets them rot. The skill *boundaries* are well-cut and the *count* is essentially right.

But there is a **load-bearing structural defect that the operator's skepticism was right to suspect**, and it is bigger than any single researcher framed it: **hypercore targets the wrong harness convention.** It builds to the open `AGENTS.md` + root-level `skills/` standard; a stock Claude Code session (2026-06-22) reads neither. Verified against Anthropic's current docs:

1. **`AGENTS.md` is not auto-loaded by Claude Code.** Anthropic's memory doc states verbatim: *"Claude Code reads `CLAUDE.md`, not `AGENTS.md`."* The generator's claim that "Claude reads it directly when no CLAUDE.md is present" (`anchor.py:3-5`) is **false** as of 2026-06-22. Without a `CLAUDE.md` bridge, a stock Claude Code session on this repo loads the anchor as **nothing**.
2. **The root-level `skills/` directory is not a Claude Code discovery location.** The current docs list `~/.claude/skills/`, `.claude/skills/` (and parents up to repo root), plugins, and enterprise — **not** a bare root `skills/`. hypercore's `skills/<name>/SKILL.md` (`methodology.py:29`) is invisible to stock Claude Code for the same reason the anchor is.

Both defects share one root cause and one class of fix (a derived `.claude/` materialization), and **both turn on one variable: which harness the architect role actually runs.** If the architect runs a custom harness that natively loads `AGENTS.md` and root `skills/`, the defect narrows to the *dogfooding* path (a human or assistant running stock Claude Code on the repo) — still real, because hypercore's runtime root *is* its own source repo (`anchor.py:40-44`), so that path is exercised constantly. The panel must confirm the harness; the report treats stock Claude Code as the conservative default.

**The 5–7 things that actually matter:**

1. **(P0) Materialize a `CLAUDE.md` bridge** (`@AGENTS.md` import or symlink) as one more derived channel, and **mirror the skills into `.claude/skills/`**, so a stock Claude Code session actually loads the anchor and the skills. Correct the false claim in `anchor.py:3-5`.
2. **(P0) De-overclaim `architecture-review`.** Its skill advertises a "model-driven depth verdict" the engine cannot produce — only a length signal plus two AST rules are built. An agent told to "assess structural depth" will over-trust a tool that does not deliver one.
3. **(P0) Fix the prose constructs that measurably cost a machine reader** — over-packed sentences (one statement is 167 words / ~7 obligations), the compound-negation idiom `never a silent veto and never a silent pass`, and mid-clause ADR references that interrupt the subject-verb binding.
4. **(P1) Add an external-conformance + link gate to `python3 -m engine --check`.** The engine guarantees "artifact == my spec" but never checks "artifact == the field standard, and its links resolve."
5. **(P1) Retire the hand-frozen `WORKER` preamble** (`worker.py:52-70`), which restates `spec/worker.md` by hand — the exact drift-by-copy the system retired everywhere else.
6. **Number of skills: keep five in `skills/`** (the boundary "methodologies become skills, mechanisms do not" is correct). The one genuine coverage gap — the worker's discipline — is correctly *not* a sixth skill; it belongs in the worker prompt, single-sourced.
7. **The arXiv citation is sound and can be *strengthened*, not softened** — the paper is harsher than the repo's paraphrase.

Net: the **content and the discipline are strong; the structure has one real, fixable, harness-targeting defect** that the minimal-anchor philosophy accidentally created (it dropped the `CLAUDE.md` bridge on a belief that is now false). Fix the harness targeting, gate it, de-overclaim one skill, and clean three prose constructs, and these artifacts are bulletproof.

---

# Part A — STRUCTURE

## A.1 The AGENTS.md field standard — what is (and is not) prescribed

`AGENTS.md` is an **open, free-form Markdown convention** — "a README for agents" — released by OpenAI (Aug 2025) and now stewarded by the **Agentic AI Foundation under the Linux Foundation**, alongside MCP and goose (agents.md; linuxfoundation.org press release; openai.com, all accessed 2026-06-22).

- **There is no schema and no required fields.** Spec FAQ verbatim: *"No. AGENTS.md is just standard Markdown. Use any headings you like; the agent simply parses the text you provide."* (agents.md, 2026-06-22).
- **Consequence:** a minimal 18-line role-anchor is **spec-compliant by construction.** There is no conformance bar to be "out of spec" against. hypercore cannot be faulted on AGENTS.md conformance — and equally, there is no authoritative validator for a role-anchor (see A.6).
- **Length norm comes from the tools, not the spec:** Anthropic CLAUDE.md "**target under 200 lines**" (code.claude.com/docs/en/memory); Factory "**≤ 150 lines**"; OpenAI Codex default cap 32 KiB. **hypercore's 18-line anchor sits at the lean extreme — an outlier in the good direction.**
- **Precedence:** nearest file wins; hypercore is single-root with one anchor, so the nesting machinery is legitimately unused.

**Content guidance (Anthropic memory doc, 2026-06-22) — and hypercore scores well:** keep IN "facts Claude should hold in every session: build commands, conventions, project layout, 'always do X' rules"; push OUT "a multi-step procedure or [content that] only matters for one part of the codebase → move to a skill." hypercore's anchor is exactly *non-inferable operational lines + a pointer to skills* — textbook adherence. Its check command is the recommended specificity (`python3 -m engine --check`, `anchor.py:31`, cf. Anthropic's "Run `npm test` before committing" not "Test your changes"). Imports do **not** save context ("imported files still load and enter the context window at launch") — but hypercore's skills-on-demand claim does not rely on imports; it relies on the Agent Skills progressive-disclosure mechanism (A.3), which is the correct mechanism.

## A.2 The Claude Code harness reality (2026-06-22) — and the CLAUDE.md/AGENTS.md adjudication

This is the report's central structural adjudication. Researcher 1 concluded AGENTS.md discovery is "correctly implemented"; Researcher 2 found a P0 defect. **I verified the contested fact directly. Researcher 2 is correct.**

**Finding 1 — Claude Code does not read AGENTS.md.** Anthropic's current memory doc, verbatim (https://code.claude.com/docs/en/memory, accessed 2026-06-22):

> *"Claude Code reads `CLAUDE.md`, not `AGENTS.md`. If your repository already uses `AGENTS.md` for other coding agents, create a `CLAUDE.md` that imports it … `@AGENTS.md` … A symlink also works … `ln -s AGENTS.md CLAUDE.md`."*

This **directly contradicts a load-bearing assertion in the generator.** `anchor.py:3-5` (docstring) states: *"The architect's harness (Claude) reads it [AGENTS.md] directly when no `CLAUDE.md` is present … so one file serves both roles and the `CLAUDE.md` symlink … was pure redundancy, dropped."* Per the primary source, present-or-absent `CLAUDE.md` is irrelevant — Claude Code does not auto-load `AGENTS.md` at all. With no `CLAUDE.md` (or symlink/import), a stock Claude Code session loads the anchor as **nothing.** The orientation paragraph that is supposed to catch a misdirected session (`anchor.py:40-44`) never loads — and that dogfooding path is exactly the case the orientation exists for, since hypercore's runtime root is its own source repo.

**Why R1 reached the opposite conclusion:** R1's audit asserts "Claude Code auto-discovers `AGENTS.md` at the repository root" and cites `skills.md`, but that page does not say so, and the *memory* page (the authoritative source for what loads every session) says the opposite. R1's conclusion is unsupported by the current primary sources. **The defect is real.**

**Finding 2 — the root-level `skills/` directory is also not a discovery location.** This goes *beyond* both researchers. The current Claude Code skills doc lists where skills live (https://code.claude.com/docs/en/skills, accessed 2026-06-22):

| Location | Path | Applies to |
|---|---|---|
| Enterprise | managed settings | All org users |
| Personal | `~/.claude/skills/<name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<name>/SKILL.md` | This project |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where enabled |

Discovery walks `.claude/skills/` from the working directory up to the repo root, plus nested `.claude/skills/`. **A bare root-level `skills/<name>/SKILL.md` is not in any of these paths.** hypercore renders to `SKILL_DIR = "skills"` (`methodology.py:29`), i.e. `skills/<cap>/SKILL.md`. So in a stock Claude Code session the five skills are **not discovered at all** — the same failure mode as the anchor, same root cause. R1's claim that this location "works in practice (confirmed by field testing with Claude Code v2.1.x)" is **not supported by the 2026-06-22 docs**; it should not be relied on.

**The deciding variable — name the harness.** Both findings turn on one question the panel must answer: **does the architect role run stock Claude Code, or a custom harness ("OMP" in the generator's words) that natively loads `AGENTS.md` and root `skills/`?**

- If **stock Claude Code:** both findings are live P0 defects in the running system.
- If **a custom harness that loads them natively:** the defects narrow to the **dogfooding path** — any human or coding assistant running stock Claude Code *on* this repo (which the orientation paragraph explicitly targets). Still a real gap, because that path is exercised every time someone develops hypercore with Claude Code, and the orientation/skills silently fail to load.

Either way the fix is the same shape and cheap (A.2 → Part D, P0). The generator's docstring claim must be corrected regardless, because it is false against the current primary source.

**Caveat preserved:** `anchor.py:19-22` already honestly records that *whether the file helps a live model is "a measurement, not a check."* That honesty is right and should be kept; it is orthogonal to this finding, which is about whether the file **loads at all**, not whether it helps once loaded.

## A.3 Skills: frontmatter, hard limits, and progressive disclosure

**Hard, documented constraints (Anthropic platform overview, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview, accessed 2026-06-22):**

- `name`: **≤ 64 chars**, lowercase/numbers/hyphens only, no XML tags, no reserved words ("anthropic"/"claude"). Required.
- `description`: **non-empty, ≤ 1024 chars**, no XML tags; *"should include both what the Skill does and when Claude should use it."* Required.
- Body budget: metadata ~100 tokens (always loaded); **SKILL.md body < 5k tokens** (loaded on trigger); resources unlimited.
- Claude Code adds a listing nuance: combined `description` + optional `when_to_use` is **truncated at 1,536 chars** in the skill listing; the budget scales at ~1% of the context window and can drop least-used skills' descriptions (skills.md, 2026-06-22).

**hypercore passes every hard limit with wide margins** (measured 2026-06-22):

| Skill | `name`==dir | description chars | commas | body lines |
|---|---|---|---|---|
| depth | OK | 218 | 2 | 30 |
| design-it-twice | OK | 239 | 3 | 27 |
| architecture-review | OK | 252 | 1 | 27 |
| coherence | OK | 297 | 1 | 28 |
| grilling | OK | 330 | 2 | 29 |

All five `description`s are well under 1024 (and 1,536); bodies are 27–30 lines, far under <5k tokens / <500 lines. **Reconciling the researchers:** R1 worried descriptions might exceed "256 chars" — that limit does not exist; the real cap is 1024/1,536, so this concern is void. R2's measured pass is correct.

**Progressive disclosure is implemented exactly as Anthropic prescribes.** Level 1 (frontmatter `name`+`description`, always loaded) → Level 2 (SKILL.md body, on trigger) → Level 3 (`spec/<cap>.md`, via the "Going deeper" pointer). `methodology.skill()` (`methodology.py:64-79`) renders precisely this shape: metadata names *when* to load, the body is the slice preamble + each requirement's statement, scenarios stay in the slice. This matches the one architecture the arXiv paper and context-rot literature endorse (minimal always-on, detail on demand).

**Description-as-when-to-load is correct, not a defect.** R1 flagged the descriptions as "overloaded" because they encode both *what* and *when* in one field, and floated a separate `when-to-use` field. The Claude Code spec **requires** the description to do both jobs, and a `when_to_use` field exists but is *appended to* the description for the same listing budget — it is not a cleaner separation. So the current single-field form is the intended form. R1's "low severity, not machine-parseable" framing is correct but the recommendation to split is unnecessary; leave it.

## A.4 The arXiv:2602.11988 citation — verified, and harsher than the repo claims

`anchor.py:6-9` rests the whole minimal-anchor decision on: *"even a good one is marginal and adds ~20% cost, and it hurts as a repository overview (arXiv 2602.11988)."* I verified the paper directly (https://arxiv.org/abs/2602.11988, accessed 2026-06-22):

- **Real, correctly cited.** Title: *"Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?"* Authors: Thibaud Gloaguen, Niels Mündler, Mark Müller, Veselin Raychev, Martin Vechev (ETH Zurich / SRI Lab). Submitted **12 Feb 2026** (the "2602" prefix is a valid past month). Independently indexed by InfoQ (2026-03-06) and DAIR.AI (2026-02-25).

| Sub-claim | Verdict | Evidence (abstract, verbatim where quoted) |
|---|---|---|
| "even a good one is marginal" | **VERIFIED — under-stated** | Human-written files improve only ≈+4%; the abstract says context files *"tend to reduce task success rates compared to providing no repository context."* |
| "adds ~20% cost" | **VERIFIED (conservative)** | Abstract: *"increasing inference cost by over 20%."* Body: 20–23% avg (USD inference cost), from 2.45–3.92 extra agent steps. |
| "hurts as a repository overview" | **VERIFIED** | *"Context files do not provide effective overviews"*; harm attributed to *"unnecessary requirements from context files make tasks harder"*; *"human-written context files should describe only minimal requirements."* |

**This is one of the better-grounded design rationales in the repo.** Corroboration is mainstream, not an outlier: Chroma's *Context Rot* (18 frontier models degrade as input grows; trychroma.com, 2025-07-14) and Anthropic's *Effective context engineering* (curate/minimize context as a finite resource) both back the mechanism. **Recommendation: strengthen the citation, don't soften it** — the repo currently *under*-claims; the abstract's "reduce task success rates" is the stronger, defensible phrasing (Part D, P3).

## A.5 Vetted tools inventory

Anchors everything: AGENTS.md has **no official validator and no schema by design**; SKILL.md is the better-served format (hard limits + a reference validator + a quality linter). Frontmatter *values* are a blind spot for every generic Markdown tool.

| # | Tool | URL | What it checks | Maturity (2026-06-22) | Would it catch a hypercore issue? |
|---|---|---|---|---|---|
| 1 | agents.md project | github.com/agentsmd/agents.md | Nothing — freeform, no schema | ~22.4k★, MIT, Linux Foundation | No — and that's the finding: nothing authoritative to lint a role-anchor against |
| 2 | **skills-ref** (agentskills, Anthropic-lineage) | github.com/agentskills/agentskills | `name` regex/len, **name==dir**, `description` ≤1024 present | In ~20.9k★ repo; closest to official SKILL.md validator | **Yes — run it.** hypercore passes; makes the pass *checked* |
| 3 | **skill-validator** (agent-ecosystem) | github.com/agent-ecosystem/skill-validator | Spec + quality heuristics; flags 5+ quoted strings / 8+ comma segments as keyword-stuffing | 173★, Go, MIT, v1.5.6 (2026-04-29); most mature dedicated linter | Would **not** trip the hard rule (commas 1–3); may warn on density/word count |
| 4 | skill-creator (Anthropic, official) | github.com/anthropics/skills | Scaffold + **eval-iterate** (baseline-vs-skill A/B) | Anthropic-maintained, active | No (authoring/eval aid) — but it *is* the right tool for the live A/B in Open Questions |
| 5 | cclint | github.com/carlrannaberg/cclint | Claude Code project linter; frontmatter, settings, CLAUDE.md/AGENTS.md sections | 20★, npm v0.2.10 | Partial — targets `.claude/agents`+`commands`, not `skills/<name>` |
| 6 | AgentLinter | agentlinter.com | CLAUDE.md/AGENTS.md/skill: structure, secrets, **cross-file contradictions** | v2.3.0, MIT; **stars unverified** | Plausibly — verify repo maturity before trusting |
| 7 | agents-lint | github.com/giacomo/agents-lint | Referenced-paths-exist, freshness score | 8★ (immature) | Mostly no on an 18-line anchor |
| 8 | **remark-lint-frontmatter-schema** | github.com/JulianCataldo/remark-lint-frontmatter-schema | YAML frontmatter vs **JSON Schema** (regex, `maxLength`, required) | 77★, **stale (2023-10)** | **Yes if you author a schema** — the one generic frontmatter gate |
| 9 | markdownlint-cli2 | github.com/DavidAnson/markdownlint-cli2 | ~50 structural Markdown rules; autofix. Blind to frontmatter values | ~842★, active | Yes, low-severity body hygiene |
| 10 | **Vale** | github.com/vale-cli/vale · vale.sh | Markup-aware **prose** linter; custom YAML rules; **can scope into frontmatter** | ~5.5k★, v3.15.1 (2026-06-12) | **Strongest prose fit** — encode hypercore's own rules (sentence length, compound negation, mid-clause ADR) over `spec/*.md` |
| 11 | **lychee** | github.com/lycheeverse/lychee | Fast link checker (URLs, **relative paths**); GH Action | ~3.7k★, active | **Conditional — run it.** A moved `spec/<cap>.md` silently breaks the rendered pointer even though the engine's own check passed |
| 12 | proselint / write-good / textlint | github.com/amperser/proselint · btford/write-good · textlint/textlint | Curated prose rules (hedging, passives, weasel words) | proselint ~4.5k★ | Marginal/noisy on terse instructional prose; best consumed via a Vale style |

**Readability metrics (Flesch-Kincaid, Gunning Fog, SMOG) are NOT a gate.** They measure only syllables/word and words/sentence — weakly tied to cognitive load and *doubly* invalid for a model (which is not syllable-bound), and they *reward* short words while being blind to the things that actually hurt the model: negation, ambiguous referents, mid-clause interruptions, instructions-per-sentence (myersfreelance.com; langsolinc.com, 2026-06-22). Use raw *sentence length* as a Vale signal; ignore the grade-level number.

**Honest gap (all three researchers agree):** there is **no validated prompt-quality linter.** Every tool above was built for human readers; their scores are signals, not machine-legibility verdicts. The only true validity test is an **A/B behavioral eval** (a "plain" rewrite vs. the original on fixed tasks) — exactly the measurement `anchor.py:19-22` already names. skill-creator (tool #4) automates that loop.

## A.6 What a linter / gate should check (the meta-gap)

The engine's `python3 -m engine --check` enforces "**artifact == my spec**" (re-render on fold; `channels.py`, `anchor.py:19-22`). It does **not** enforce "**artifact == the field standard, and its pointers resolve.**" Those are different invariants; only the first is gated. The fix is to add an external-conformance + link gate (Part D, P1) that runs over the *rendered* artifacts:

- **skills-ref `validate`** per skill (name regex, name==dir, description present + ≤1024).
- **A small JSON-Schema frontmatter check** (or remark-lint-frontmatter-schema) enforcing `name` regex + `description` length + required fields.
- **lychee** over `AGENTS.md` and `skills/*/SKILL.md` so a moved `spec/<cap>.md` or README pointer fails loudly.
- **Vale with a custom `hypercore` style** over `spec/*.md` requirement statements (sentence-length, compound-negation, mid-clause-ADR) — wired as a *signal*, not an auto-refusal, consistent with the project's own `length signal` philosophy and the not-yet-built red-flag scan (ADR 0020).
- **A discovery-location assertion**: that the materialized skills and the `CLAUDE.md` bridge land where the *target harness* actually reads them (this is what would have caught A.2 by construction).

---

# Part B — CONTENT

## B.1 The methodology → content map (derivation, line by line)

ADR 0009's two-axis cut governs *what goes where*: **durability** (does it change every fold?) × **reach** (every episode, or only routed episodes?).

| Channel | Durability × reach | Materialized? | Generator |
|---|---|---|---|
| **prompt** | live, every episode | no (live) | `worker.prompt` / `conversation` |
| **skills** | durable, routed | yes (on fold) | `engine/methodology.py` |
| **agents file** | durable, every-episode | yes (on fold) | `engine/anchor.py` |

- **`AGENTS.md`** = authored residue (`anchor.py:45-63`: orientation paragraph + the two `## Operating` lines + the `## Skills` lead-in) **welded to** a derived skills index (`_skills_index`, `anchor.py:76-88`, one bullet per `METHODOLOGIES` entry, trimmed to the description's first sentence). Adding a skill lists it automatically.
- **Each `SKILL.md`** = a lossless reformat of `spec/<cap>.md` (`_overview` = the slice preamble with HTML comments stripped, `methodology.py:111-124`; `_disciplines` = `**name** — statement` per requirement, scenarios left in the slice, `methodology.py:127-140`) **plus one authored line**: the `description` from `METHODOLOGIES` (`methodology.py:34-57`) — the *only* hand-written content in the whole skill.
- **The fold** re-renders all of them (`channels.py:30-37`). A committed `.md` cannot drift from its source.

**What decides "is this capability a skill?"** There is **no rule in code** — the set is the literal contents of `METHODOLOGIES`. The tacit, real, and defensible policy: **a capability is a skill iff a *role* (architect or worker) runs it as a discipline, not iff the *engine* runs it as a mechanism.** This lives nowhere in the spec; it is tacit in the curation of one dict.

## B.2 The skill roster and the number-of-skills answer

**The direct answer: keep five skills in `skills/`. Not more, not fewer.** This is R4's spine, and it survives pressure-testing.

Classifying all 13 capability slices on disk by the tacit policy reproduces *exactly* the five the system shipped:

| Capability | Kind | Skill today? | Should be? |
|---|---|---|---|
| graph, queue, interface, conversation, self-model, folding-conditions, schedule | engine/operator **mechanisms** | no | **no** |
| worker | role mechanism (fence, grounding, hand-back) | no | **borderline → no, see below** |
| design-it-twice, grilling, coherence, architecture-review | architect **disciplines** | yes | **yes** |
| depth | worker **discipline** | yes | **yes** |

The boundary the operator drew — *methodologies become skills; mechanisms do not* — is the right one. ADR 0022 independently confirms it: the scheduler got a capability slice but **no skill question was even raised**, because it is engine machinery, the same family as transport/record.

**Pressure-testing the count:**

- **Merge into fewer (one "methodology" skill)?** No. The descriptions drive auto-routing; a 5-in-1 description cannot route reliably, and the listing budget would shorten it. The separation is load-bearing.
- **Split any?** No. Each is already minimal (27–30 lines) and maps to one clean phase. Splitting is artificial.
- **Add the worker as a sixth skill?** This is the strongest "missing skill" candidate, and the answer is a *principled no.* The worker runs a real, teachable discipline (rescan the whole spec; build behind a red→green loop; refine the delta; write for the machine — `worker.py:56-59`, `spec/worker.md`). But that discipline is **always-on, not routed** — it is the worker's standing identity, hard-coded into `worker.prompt`. ADR 0009's two-axis cut puts always-on grounding in the *prompt*, not in a routed skill. So the spec is internally consistent in not skilling it. **The roster move is +1 capability of *coverage*, +0 skill files** — the sixth discipline materializes into the prompt, not into `skills/`. (The defect this exposes is the worker preamble drift, B.4 / P1.)
- **Trim coherence (the thinnest, 2 requirements, overlaps depth at the gate)?** No — it owns the *operator's-altitude coherence check, not a code review* framing (`coherence/SKILL.md:23`, `spec/coherence.md:17-21`) that nothing else owns, and ADR 0013 deliberately carved it a slice to avoid a requirement-subset render that would reintroduce drift. **Keep, but watch** if the roster is ever trimmed.

**Final roster:** five `skills/` (design-it-twice, grilling, coherence, architecture-review, depth) + the worker discipline single-sourced into the prompt. **No skill added or removed.**

## B.3 Per-artifact content gaps and overclaims

**Lead finding — the `architecture-review` overclaim (the most dangerous content error).** An agent acts on what a skill *claims*.

- **Vision (what the skill advertises):** "the standing scan that keeps the system **deep**," a "red-flag depth scan," "the deletion test, the shallow-module and information-leakage judgments, testable-through-the-interface" (`spec/architecture-review.md:24-38`).
- **Implementation (what the engine does):** only a **length** signal (a context-cost proxy) plus **two mechanical AST rules** — dead module-level symbols and circular imports (ADR 0020, `spec/architecture-review.md:55-63`). The model-driven *verdict* is explicitly **"not yet built"** (`spec/architecture-review.md:36-38`).
- **The skill does say "not yet built" — but it leads with the aspiration and buries the limit** at the end of a ~167-word statement. An agent loading this skill to "assess structural depth" (its stated trigger) will over-trust a tool that does not deliver a depth verdict. **Fix (P0): invert the emphasis** so the statement *opens* with the three concrete built things (length-vs-record; dead symbols; cycles) and marks the model-driven verdict as roadmap. Because the skill is a faithful render, the fix lands in `spec/architecture-review.md` requirement 2 and auto-propagates.

**The worker preamble drift (R4's second lead).** The `WORKER` constant (`worker.py:52-70`) hand-restates `spec/worker.md` — "rescan the WHOLE spec," "build deep up front… no shallow modules, no red flags," "reply with ONLY a JSON object." That discipline prose lives almost verbatim in `spec/worker.md` requirements. **It is the exact `worker.DEPTH`-constant drift-by-copy that ADR 0019/0009 retired for depth — left unretired for the worker's own discipline.** It can drift the moment `spec/worker.md` sharpens. (Fix P1.)

**Other per-artifact findings:**

- **`AGENTS.md`** — the healthiest artifact. Present and correct: the check command, the build/hand-back convention, the derived skills index. The orientation paragraph is a *defended* exception to "non-inferable only" (the dogfooding tax, `anchor.py:40-44`) and earns its place — it *routes* a misdirected session rather than *describing* the repo, the one kind of overview the arXiv study would still bless. **One non-inferable omission:** the fence / decisions-floor invariant (a worker is read-only outside its worktree; send/publish/install/spend must route through the decisions floor, `intent.md:58,62`). This is load-bearing and currently in neither anchor nor prompt. It belongs in the **worker prompt** (worker-specific), not the role-neutral anchor (P2).
- **`design-it-twice`** — faithful render. Missing the *when-to-stop / how-many-candidates* and *"is this interface load-bearing enough to spend a contest?"* judgment; the trigger is asserted, not taught. A spec-slice gap, not a render gap.
- **`grilling`** — cleanest architect skill, no content errors. Minor: never says operationally *how* to form a defensible lean (the worked behavior is in the scenarios via the pointer).
- **`coherence`** — faithful; the load-bearing "**not a code review**" instruction is present. Thinness noted (B.2).
- **`depth`** — **the model skill.** Five crisp Ousterhout disciplines; the preamble cites the synthesis as *provenance*, not inlined (`depth/SKILL.md:11-13`). Single-sourced into both the skill and the worker prompt with no drift (ADR 0019). Exemplary.

## B.4 Vision-vs-implementation gaps the artifacts must respect

Where the vision runs ahead of the engine, an artifact must not *claim* the capability:

1. **`architecture-review` depth verdict** — covered above; the one that touches a skill directly. Fix it.
2. **Atomic-fold overclaim** — ADR 0022 records that integration serializes but the fold is *not* transactional; the glossary's "same act" language (glossary:63-65) and `coherence/SKILL.md:14-16` are vision-ahead under concurrency. For a single worker this is fine; the caveat belongs in `self-model`/`schedule`, **not a skill** — skills should not encode concurrency edge-cases.
3. **`design.py` is architect-invoked, not scheduler-driven** (ADR 0022, parked). The `design-it-twice` skill describes a discipline the architect runs by hand today — which is true. **Flag only, no edit.**
4. **OMP / multi-model flip is parked** — the worker is still single-harness (`claude -p`). No artifact *claims* multi-model, so no content error; a roadmap note. **(This is the same harness-assumption thread as A.2 — worth confirming alongside it.)**
5. **interface / conversation / queue are largely vision** — but none is skill-facing (operator-facing mechanisms, correctly not rendered into any skill). That the biggest vision-ahead gaps *don't* touch the agent-facing artifacts is itself evidence the skill boundary (B.2) is drawn in the right place.

**Cross-artifact coherence defect (R4):** four slices carry **no `<!-- vision: … -->` binding** — `architecture-review`, `depth`, `design-it-twice`, `folding-conditions` — while the other nine do. `folding-conditions` is plausibly pure-machinery (arguably correct to omit). But `depth`, `design-it-twice`, `architecture-review` are the *opposite* of machinery — they most embody the intent's depth/strategic-programming arc, yet the **operator view shows no vision for exactly the capabilities that most embody the vision.** The render strips the comment anyway (`methodology.py:115`), so the *skill* is unaffected — but the operator-view derivation is incomplete where it matters. This is precisely the kind of finding ADR 0020's own dogfood was meant to catch. (Fix P0-2-bind.)

---

# Part C — WRITING FOR THE MACHINE

This gets its own prominent part because hypercore treats obsessively clear, concise writing for an LLM reader as a fundamental ability — and its artifacts are explicitly "written for the machine, never for the operator" (`AGENTS.md:8`). The discipline is real, the evidence is specific, and the house style is **right but pushed ~15% past its useful limit for a machine reader.**

## C.1 The discipline and the evidence — why writing for a model differs from writing for a human

A human resolves an ambiguous referent by re-reading or asking; an agent consuming an auto-loaded skill **has no back-channel and binds the most probable antecedent in one pass.** Ambiguity a human absorbs silently becomes a coin-flip for the model. The evidence base (all fetched 2026-06-22):

- **Be clear and direct; the golden rule.** Anthropic prompting best practices: *"Show your prompt to a colleague with minimal context… If they'd be confused, Claude will be too."* Recommends *"sequential steps using numbered lists or bullet points when the order or completeness of steps matters."*
- **Right altitude, smallest high-signal token set.** Anthropic context-engineering: the goal is *"the smallest possible set of high-signal tokens,"* but *"minimal does not necessarily mean short."* **Concision is not the goal; signal density is.** Ornament fails not because it is long but because it spends attention without adding a decision-relevant token.
- **Context rot — every token spends an attention budget.** *"As the number of tokens… increases, the model's ability to accurately recall… decreases."* For an always-on file (`AGENTS.md`, read every episode) ornament is the **most expensive ornament in the system.**
- **Instruction density has a measurable cliff.** "How Many Instructions Can LLMs Follow at Once?" (arXiv:2507.11538): even frontier models reach only **~68% accuracy at 500 simultaneous instructions**, with a **primacy effect** — *"selective attention mechanisms favor earlier instructions."* **When one sentence packs five obligations, the later ones are systematically dropped.** "One sentence = one instruction" is not a style preference; it keeps an instruction off the discard pile.
- **Negation is the single most failure-prone construction.** Jang et al. (KAIST): models perform *worse* on negated prompts as they scale. "When Prohibitions Become Permissions" (arXiv:2601.21433): open-source models endorse prohibited actions **77% under simple negation, 100% under compound negation.** Anthropic operationalizes it: *"Tell Claude what to do instead of what not to do."*

## C.2 The house-style verdict — productive density vs. genuine obscurity

**The density is deliberate and often productive.** Where every clause is a distinct, reused ubiquitous-language term, compression *is* signal — the textual equivalent of the deep-module discipline the project preaches (much meaning behind a small surface). **That is left alone.** The audit separates it from genuine obscurity, which is the target. hypercore does **not** have an ornament problem; it has a *packing* problem (too much true signal per sentence) and a *negation* problem.

Quantified profile of the SKILL.md discipline bullets (each rendered as one line, `methodology.py:133-140`): the **median** statement (~70 words, 2 em-dashes, 0 ADR refs, opens imperative) is dense but acceptable. The **imperative `MUST` spine is healthy** — 8 of 13 statements open with a clean `MUST`; preserve it. The **outliers are the problem**, led by:

> `architecture-review` god-file statement (`spec/architecture-review.md:25-38`): **167 words, 6 em-dashes, 3 mid-statement ADR refs, ~7 distinct obligations in one rendered line.** Per the primacy finding, obligations after the first ~two are at risk of being dropped. This is the single highest-value prose fix in the corpus — and it is the same statement as the `architecture-review` overclaim (B.3), so one edit fixes both.

The three offender classes:
- **(A) Sentences doing too much** — split them (one instruction per sentence).
- **(B) Mid-instruction parenthetical ADR refs** — e.g. `"…the scan now reads (ADR 0020) are a subset…"` (`architecture-review.md:34-35`) drops the ref *between the verb and its predicate*, split across a line break; `"(a stale acceptance, ADR 0008) MUST return"` (`:29`) drops it *between subject and verb*. These are the highest-cost interruptions because they land exactly where the model binds subject to verb. Provenance is *context*, not instruction — move it to line-end.
- **(C) Negation-as-definition** — `never a silent veto and never a silent pass` (`coherence.md` ×2 + the SKILL body) is a *compound negation* that also defines the desired behavior only by what it is not. The positive form is shorter and in-distribution.

## C.3 Top before → after rewrites (carried verbatim from the applied audit)

Each preserves meaning and voice and fixes a specific, evidenced failure mode. **All are edits to the spec source**, which the fold re-renders.

**#1 — Split the 167-word god-file statement** (`spec/architecture-review.md:25-38`; fixes both the packing offender and the overclaim):

> **BEFORE:** "**Depth is the criterion, not length**: the *mechanical* structural red flags a tool can read — dead module-level symbols and circular dependencies — the scan now reads (ADR 0020) are a subset; the deeper, model-driven **red-flag depth verdict** — the deletion test, the shallow-module and information-leakage judgments, testable-through-the-interface — is the assessment this review is still meant to grow, and is **not yet built** (ADR 0006)."
>
> **AFTER (three statements, built-thing first):** (a) "A module past the length signal with no accepting depth-decision MUST surface as a strong deepening opportunity; one nearing the signal surfaces as a lighter one." (b) "A module within an accepting depth-decision's length is not debt. A module grown materially past the length it was accepted at MUST return to the backlog, marked as having outgrown its bar. *(Stale acceptance: ADR 0008.)*" (c) "The measure shipped is length — one signal of depth — plus two mechanical rules a tool reads: dead module-level symbols and circular dependencies. The model-driven depth verdict (the deletion test, shallow-module and information-leakage judgments) is **not yet built**. *(Mechanical subset: ADR 0020. Verdict not-yet-built: ADR 0006.)*"

**#2 — Positivize the compound negation** (`spec/coherence.md`, ×2 + SKILL body):

> **BEFORE:** "…on the operator's queue rather than folding — never a silent veto and never a silent pass (ADR 0006)."
>
> **AFTER:** "…surface every result as exactly one of two outcomes: a fold, or a decision card on the operator's queue. *(ADR 0006.)*"

**#3 — ADR ref out of the verb-predicate gap** (`architecture-review.md:34-35`):

> **BEFORE:** "…the scan now reads (ADR 0020) are a subset…"
> **AFTER:** "…the scan now reads these red flags; they are a subset. *(ADR 0020.)*"

**#4 — Bare "this/so" → named subject** (`design-it-twice.md:8-9`):

> **BEFORE:** "…so this applies hypercore's existing isolation where first-draft commitment hurts most: the shape of a deep module."
> **AFTER:** "The first shape committed is rarely the deepest. Design-it-twice applies hypercore's existing isolation where first-draft commitment hurts most: the shape of a deep module."

**#5 — Pronoun "It" → named subject; ADR to trailing note** (`architecture-review.md:3-4`):

> **BEFORE:** "The standing scan that keeps the system deep (ADR 0005). It reads the source tree live for deepening opportunities…"
> **AFTER:** "The standing scan keeps the system deep. The review reads the source tree live for deepening opportunities… *(ADR 0005.)*"

**#6 — Assign the action to the actor, not the object** (`coherence.md:9-10`):

> **BEFORE:** "A result that honors the contract folds its refined delta into the spec — the work leaving the work view in the same act;"
> **AFTER:** "When a result honors the contract, the architect folds its refined delta into the spec; the work leaves the work view in the same act."

**#10 — Reduce stacked negation, make the single positive rule explicit** (`depth.md` bullet, `:26`):

> **BEFORE:** "…each a symptom a judge weighs, none a threshold a tool checks. The system keeps at most a **length** tripwire (a context-cost signal that raises a depth decision, never an auto-refusal);"
> **AFTER:** "…each a symptom a judge weighs, not a threshold a tool checks. The system keeps one mechanical signal: a **length** tripwire. It raises a depth decision and stops there — it never auto-refuses."

(Further vetted rewrites #8, #9, #11, #12 — grilling preamble, the cross-skill `standing-guard floor` reference, the `coherence.md:8-9` double-negative, and the `architecture-review.md:62-63` antecedent — are in the working audit and follow the same rules.)

## C.4 A short style guide, encodable in the generators

Seven rules, tuned to *preserve* the dense aphoristic register while removing the constructs that cost a machine reader. Each maps to evidence above and to a Vale rule:

1. **One instruction per sentence.** Split any statement with more than one `MUST`-worthy obligation. Density lives in the *vocabulary*, not the *clause count*. (Target: requirement statements ≤ ~40 words; hard-flag > 60.)
2. **Say what to do, not only what not to do.** Replace `never X` / `never X, never Y` with the positive form. Keep a negation only when the prohibition is the whole point and no positive form exists.
3. **Provenance refs go at line-end, never mid-clause.** Every `(ADR NNNN)` moves out of the subject-verb-object spine to a trailing `*(ADR NNNN.)*` note.
4. **Every pronoun has a named antecedent in the same sentence.** Ban sentence-initial bare `It`/`This`/`That` for the unnamed practice; prefer `the review`, `that difference`, `the architect`.
5. **Assign each action to its actor.** If the architect does it, the architect is the subject — don't let the object ("a result") wear the active verb.
6. **A skill is read alone — gloss or link cross-skill terms.** Name a sibling-skill term's home on first use (`standing-guard floor` lives in `grilling`); the glossary is not guaranteed to be in context.
7. **Reserve bold for term-marking, and budget it.** Bold signals "ubiquitous-language vocabulary"; cap at ~2–3 per sentence, or it discriminates nothing.

**Preserve on purpose** (do *not* flatten): the em-dash as a *single* aside; coined-and-glossed vocabulary; the `MUST` spine; the aphoristic preamble *as a why*. **The voice is an asset; only its excess is the cost.**

**Encode it where it can't rot:** because `_statement()` already parses requirement prose deterministically, a Vale step (or a small harness lint) can run over `spec/*.md` requirement statements and *signal* on: sentence > 60 words, `\bnever\b.*\bnever\b`, `(ADR \d+)` not at line-end. This makes rules 1–3 *checkable by construction* — the same "advice made into a discipline" move the project already applies to depth — recorded honestly as a **signal, not a verdict** (the A/B behavioral eval is the only true validity test, per `anchor.py:19-22`).

---

# Part D — Prioritized recommendations

Every item is a change to a **source** (spec slice or generator), because the `.md` are derived. Each carries the evidence and the weakness it removes.

## P0 — Defects the artifacts must not ship with

**P0-1 · Target the harness Claude Code actually reads.** *(generators: `engine/channels.py`, `engine/methodology.py`, `engine/anchor.py` docstring)*
First **confirm the architect harness** (see Open Questions). Treating stock Claude Code as the default:
- Materialize a **`CLAUDE.md` bridge** containing `@AGENTS.md` (Anthropic-sanctioned import) — or a `CLAUDE.md → AGENTS.md` symlink — as one more derived channel appended to `channels.CHANNELS`, so it can't drift.
- **Mirror the five skills into `.claude/skills/<cap>/SKILL.md`** (change `methodology.SKILL_DIR` to `.claude/skills`, or render to both locations during the transition), which is where Claude Code discovers project skills.
- **Correct the false docstring** at `anchor.py:3-5` ("Claude reads it directly when no CLAUDE.md is present") — it contradicts the primary source.
*Evidence:* https://code.claude.com/docs/en/memory and https://code.claude.com/docs/en/skills (accessed 2026-06-22). *Removes:* the anchor and skills loading as **nothing** in a stock Claude Code session (at minimum the dogfooding path). *If the harness is custom and loads AGENTS.md + root `skills/` natively:* scope to the dogfooding path and document the assumption explicitly in the docstring.

**P0-2 · De-overclaim `architecture-review` and split its 167-word statement.** *(slice: `spec/architecture-review.md`, requirement 2, `:24-38`)*
Rewrite the statement so it *opens* with the three built capabilities (length-vs-record; dead module-level symbols; circular dependencies) and relegates the model-driven verdict to a clearly-marked roadmap clause; split the 15-line paragraph into ≤3 sentences (Part C #1). The faithful render (`methodology.py:130`) auto-fixes `architecture-review/SKILL.md`. *Evidence:* `spec/architecture-review.md:36-38` ("not yet built"), ADR 0020/0006; instruction-density primacy (arXiv:2507.11538). *Removes:* an agent over-trusting a depth verdict the engine cannot produce, and the densest, most-droppable statement in the corpus. *No generator change.*

**P0-3 · Clean the three machine-costly prose constructs at the source.** *(slices: `spec/coherence.md`, `spec/architecture-review.md`, `spec/depth.md`; generator string `anchor.py:47-53` for the 70-word orientation sentence)*
Positivize `never a silent veto and never a silent pass` (Part C #2); pull every mid-clause ADR ref to line-end, priority the verb-splitters `architecture-review.md:34-35` and `:29` (Part C #3); reduce the stacked negation in `depth.md` (Part C #10). *Evidence:* negation endorsement 77%/100% (arXiv:2601.21433); Anthropic "say what to do." *Removes:* the highest-failure-rate construction and the highest-cost interruptions.

**P0-2-bind · Add the three missing vision bindings.** *(slices: `spec/depth.md`, `spec/design-it-twice.md`, `spec/architecture-review.md`)*
Add `<!-- vision: … -->` to the three discipline slices that most embody the intent's depth/strategic arc; decide explicitly whether `folding-conditions` is pure-machinery (leave bare, *say so* in a one-line comment) or realizes intent (bind it). *Evidence:* ADR 0020; render strips the comment so the skill is unaffected (`methodology.py:115`). *Removes:* the operator view showing no vision for exactly the capabilities that most embody it. *No generator change.*

## P1 — High-value structural and content hardening

**P1-1 · Add an external-conformance + link gate to `python3 -m engine --check`.** *(harness/CI; tools A.5 #2, #8, #10, #11)*
Run over the *rendered* artifacts: skills-ref `validate` per skill; a tiny JSON-Schema frontmatter check (`name` regex + `description` ≤1024 + required); lychee over the `.md` pointers; a Vale `hypercore` style over `spec/*.md` requirement statements (signal, not refusal); and a **discovery-location assertion** that the materialized skills + `CLAUDE.md` bridge land where the target harness reads them. *Removes:* the meta-gap — the engine checks "artifact == my spec" but never "artifact == the field standard, and its links resolve" (A.6); and would have caught P0-1 by construction.

**P1-2 · Single-source the worker discipline prose; retire the hand-frozen `WORKER` preamble.** *(generator: `engine/worker.py`, `:52-70`, `:118-142`)*
Render the worker's discipline lines from `spec/worker.md`'s requirement statements (reuse `methodology._disciplines`/`_statement`), leaving only the genuinely non-spec residue authored — the JSON envelope (`worker.py:62-70`) and the role salutation. *Evidence:* the `worker.DEPTH`-constant drift ADR 0019 retired everywhere else, left unretired here. *Removes:* a hand copy of `spec/worker.md` that drifts the moment the spec sharpens. This is the "worker skill" the roster lacks — materialized into the prompt by design, not into `skills/`.

## P2 — Quality and one missing operational fact

**P2-1 · State the fence + decisions-floor invariant in the worker prompt.** *(generator: `engine/worker.py`)*
A worker is read-only outside its worktree and must route send/publish/install/spend through the decisions floor (`intent.md:58,62`) — non-inferable and load-bearing. Put it in the *worker prompt* (worker-specific), **not** the role-neutral `AGENTS.md` (which stays minimal per ADR 0009).

**P2-2 · One-time quality pass + description tightening toward the house exemplar.** *(slice/registry: `methodology.METHODOLOGIES`; tools #3, #10)*
Run skill-validator + Vale (frontmatter-scoped). Descriptions are *legal* but 2–4× denser than Anthropic's own ~150-char exemplar; optionally trim the longest (grilling 330 / coherence 297) toward two short clauses (what + when). Low severity — they pass all hard limits.

## P3 — Provenance hygiene (no agent impact)

**P3-1 · Strengthen the arXiv citation.** *(generator: `anchor.py:6-9`)* Cite the abstract's stronger "reduce task success rates" finding and add the corroboration (context-rot; Anthropic context-engineering). *Removes:* an *under*-claim — the repo is currently weaker than its own evidence.
**P3-2 · Refresh ADR 0009's stale anchor sketch** (`python3 -m hyper` → `python3 -m engine`) so the ADR describes what `anchor.py:31` emits.
**P3-3 · Reconcile / derive the capability count** across README, ADR 0013/0018, and reality (13 on disk); don't hard-type a count anywhere — derive or omit, the discipline README already applies to the check count.

---

# Open questions / verify in a live end-to-end

1. **Which harness does the architect role run?** This is the single deciding variable for P0-1. If stock Claude Code → P0-1 is a live defect; if a custom harness that natively loads `AGENTS.md` + root `skills/` → P0-1 narrows to the (still-real) dogfooding path. **Verify by opening a stock Claude Code session on the repo and checking what loads.**
2. **Live discovery test.** In a stock Claude Code session on hypercore, run `/memory` (does `AGENTS.md`/the bridge appear?) and `What skills are available?` / `/doctor` (are the five skills listed, and are any descriptions shortened/dropped under the listing budget?). This directly confirms or refutes A.2.
3. **Auto-invocation behavioral test.** Auto-routing is probabilistic. Run prompts matching each skill's trigger ("design a load-bearing interface" → design-it-twice; "I'm filing a feature request" → grilling; "check my architecture" → architecture-review) and record whether each auto-loads. Refine descriptions only if a skill mis-routes.
4. **The only true clarity validity test is an A/B eval**, not any linter score — a "plain" rewrite of a skill vs. the original on fixed tasks, measuring adherence (skill-creator automates this). The linter rules (P1-1) are signals; record the caveat the way `anchor.py:19-22` already does.
5. **Does the engine's spec-existence check survive a `spec/<cap>.md` rename?** lychee over the rendered pointers (P1-1) would catch a moved target that the internal check passes.

---

# Sources (consolidated; all accessed 2026-06-22 unless noted)

**Harness reality — the load-bearing adjudication**
- Claude Code memory (verbatim "reads CLAUDE.md, not AGENTS.md"; `@AGENTS.md` import; symlink; `/init`; <200 lines): https://code.claude.com/docs/en/memory
- Claude Code skills (discovery locations `.claude/skills/`, `~/.claude/skills/`, plugin, enterprise; 1,536-char listing cap; skill-creator A/B eval): https://code.claude.com/docs/en/skills
- Agent Skills overview (hard limits: `name` ≤64, `description` ≤1024 non-empty, body <5k tokens; description must state what+when; three-level progressive disclosure): https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

**The AGENTS.md field standard + norms**
- https://agents.md/ · https://github.com/agentsmd/agents.md · https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation · https://openai.com/index/agentic-ai-foundation/
- https://developers.openai.com/codex/guides/agents-md · https://docs.factory.ai/cli/configuration/agents-md · https://www.humanlayer.dev/blog/writing-a-good-claude-md
- Cautionary hand-edited exemplars: https://github.com/openai/codex/blob/main/AGENTS.md (~309 lines) · https://raw.githubusercontent.com/apache/airflow/main/AGENTS.md (~650 lines)

**The research claim (verified)**
- https://arxiv.org/abs/2602.11988 · https://arxiv.org/html/2602.11988v1 — "Evaluating AGENTS.md…", Gloaguen/Mündler/Müller/Raychev/Vechev (ETH/SRI), submitted 2026-02-12; abstract: context files "tend to reduce task success rates," "increasing inference cost by over 20%," "do not provide effective overviews."
- https://www.infoq.com/news/2026/03/agents-context-file-value-review/ (2026-03-06) · https://academy.dair.ai/blog/agents-md-evaluation (2026-02-25)
- https://www.trychroma.com/research/context-rot (2025-07-14) · https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

**Writing for the machine**
- Anthropic prompting best practices (be clear/direct; golden rule; "tell Claude what to do not what not to do"): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Anthropic effective context engineering (right altitude; smallest high-signal token set; context rot; attention budget): https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Instruction density: arXiv:2507.11538 (~68% at 500 instructions; primacy effect): https://arxiv.org/html/2507.11538v1 · https://arxiv.org/pdf/2507.11538
- Negation: Jang et al. (KAIST) arXiv:2209.12711 · "When Prohibitions Become Permissions" arXiv:2601.21433 (77%/100% endorsement)
- Readability-metric limits: https://www.myersfreelance.com/the-flesch-kincaid-test-is-flawed-and-we-should-stop-using-it/ · https://langsolinc.com/understanding-flesch-kincaid-readability-scores/

**Tooling (vetted)**
- skills-ref: https://github.com/agentskills/agentskills · skill-validator: https://github.com/agent-ecosystem/skill-validator · skill-creator: https://github.com/anthropics/skills · cclint: https://github.com/carlrannaberg/cclint · AgentLinter: https://agentlinter.com/ · agents-lint: https://github.com/giacomo/agents-lint
- remark-lint-frontmatter-schema: https://github.com/JulianCataldo/remark-lint-frontmatter-schema · markdownlint-cli2: https://github.com/DavidAnson/markdownlint-cli2 · Vale: https://github.com/vale-cli/vale · https://vale.sh/ · lychee: https://github.com/lycheeverse/lychee · proselint: https://github.com/amperser/proselint
- Agent Skills standard: https://agentskills.io/specification

**Repo evidence (file:line)**
- `engine/anchor.py:3-5` (false "Claude reads it directly" claim), `:6-9` (arXiv claim), `:19-22` (honest limit), `:31` (CHECK command), `:40-44` (dogfooding orientation), `:45-63` (authored residue), `:76-88` (derived skills index)
- `engine/methodology.py:29` (SKILL_DIR="skills"), `:34-57` (METHODOLOGIES descriptions), `:64-79` (skill render), `:111-124` (overview, comment-strip `:115`), `:127-140` (disciplines/statement)
- `engine/channels.py:30` (CHANNELS registry), `:33-37` (materialize)
- `engine/worker.py:52-70` (hand-frozen WORKER preamble), `:118-142` (prompt assembly)
- `AGENTS.md` (18 lines, measured); `skills/{depth,design-it-twice,architecture-review,coherence,grilling}/SKILL.md` (27–30 lines; descriptions 218–330 chars; name==dir all five — measured 2026-06-22)
- `spec/architecture-review.md:24-38` (the 167-word overclaim statement), `:55-63` (the two built mechanical rules)
- `spec/coherence.md` (compound-negation idiom ×2), `spec/worker.md` (restated by the WORKER constant), `intent.md:58,62` (fence/decisions-floor)
