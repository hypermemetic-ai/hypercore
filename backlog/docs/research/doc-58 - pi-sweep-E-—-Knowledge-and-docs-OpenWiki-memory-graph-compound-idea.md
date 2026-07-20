---
id: doc-58
title: 'pi-sweep E — Knowledge and docs (OpenWiki, memory graph, compound, idea)'
type: other
created_date: '2026-07-19 16:33'
updated_date: '2026-07-19 16:35'
tags:
  - research
---
# pi-sweep E — Knowledge and docs: reconciled research report

**Owning task:** T-93 — Evaluate pi-ecosystem replacements for qq surfaces.
**Cluster:** E — Knowledge and documentation (OpenWiki, codebase-memory-mcp, CONCEPTS.md, compound, idea).
**Research date:** 2026-07-19. **Overall confidence:** HIGH on keep/retire decisions; MEDIUM on optional package rankings (static inspection only).
**Settles:** No faithful all-in-one replacement. Keep all five qq surfaces. codebase-memory-mcp confirmed third-party (not operator-owned) — qq owns only routing guidance; keep it, and pilot `opencode-codebase-index` as the strongest pi-native challenger with a real query corpus before any switch. The plausible OpenWiki shrink is upstream's CI-generated docs PR, gated on a disposable-repo trial of qq's safeguards.
**Decision this informs:** the codebase-index pilot and the OpenWiki CI trial are their own later Changes; this document is evidence, not authorization.

## Owning-agent verification (2026-07-19)

Spot-checked before reconciliation: the openwiki drift finding is real — `openwiki/.last-update.json` records generation at commit `c5fa552` on 2026-07-16, while `bin/qq-openwiki` changed 2026-07-18; the wiki describes stale-snapshot recovery the current 137-line wrapper no longer implements. **Incidental drift finding** — schedule a wiki refresh (relates to T-89's stale-doc scans). Also verified locally: `.mcp.json` declares only Context7, consistent with the report's claim that pi reaches codebase-memory through the AGENTS.md CLI route.

## Cross-cluster adjudications

- **Memory packages (hermes-memory / pi-memory / engram):** pick at most one, as QoL only; none touches `compound`'s settled-lesson gate. No overlap with other clusters' verdicts.
- **`opencode-codebase-index` pilot** is the highest-value QoL item in this cluster; define the representative qq query corpus (architecture, dependency, route, impact questions) as part of the pilot Change's acceptance.
- Doc-57's incidental drift finding (Claude-first snap prose in `openwiki/operations.md`) lands in the same wiki-refresh bucket as the drift above.

---

# Findings report — Pi replacements for qq knowledge surfaces

**Question:** What maintained Pi-native package or combination can replace qq’s recurring documentation, structural code graph, glossary, lesson capture, and idea capture?

**Overall confidence:** **HIGH** on the keep/retire decisions; **MEDIUM** on optional package rankings because candidates were inspected statically, not installed or benchmarked in qq.

**What this settles:** There is no faithful all-in-one replacement. Retiring any of the five qq surfaces now would lose material behavior. The best maintained combination remains the one qq already uses: upstream OpenWiki plus upstream codebase-memory-mcp, with qq retaining its small operator-governance layer. The strongest Pi-native challenger is `opencode-codebase-index`, but it needs a real query-corpus pilot before replacing codebase-memory.

## Decision

| qq surface | Verdict | Finding |
|---|---|---|
| `bin/qq-openwiki` | **Keep; shortlist shrink** | Upstream OpenWiki now supports code mode and CI-generated documentation PRs, but does not reproduce qq’s branch, symlink, provider, cleanup, and review safeguards. |
| `skills/openwiki-maintainer` | **Keep; possibly reduce later** | Upstream automation can open PRs, but does not encode assignment, fresh review, docs-only acceptance, operator merge, and no-self-merge boundaries. |
| codebase-memory-mcp coupling | **Keep now; pilot challenger** | codebase-memory-mcp remains the strongest structural graph. `opencode-codebase-index` is the best Pi-native alternative but lacks arbitrary graph queries and comparable architecture breadth. |
| `CONCEPTS.md` | **Keep** | No package provides canonical, operator-owned vocabulary that agents are required to read. |
| `skills/compound` | **Keep** | Memory packages capture observations or habits, not only settled, verified, reusable causal lessons. |
| `skills/idea` | **Keep** | No package matches its exact trigger, verbatim capture, timestamp, singleton, duplicate refusal, and resume-current-task transaction. |

The local OpenWiki is demonstrably behind current source: [.last-update.json](/home/qqp/projects/qq/openwiki/.last-update.json) records commit `c5fa552` on July 16, while `bin/qq-openwiki` changed July 17. Consequently, [architecture.md](/home/qqp/projects/qq/openwiki/architecture.md:57) and [operations.md](/home/qqp/projects/qq/openwiki/operations.md:57) still describe durable stale-snapshot recovery that the current 137-line [wrapper](/home/qqp/projects/qq/bin/qq-openwiki:60) no longer implements. This is expected post-update drift, not evidence that the July 16 generation missed its source; it does show why scheduled refresh automation is worth pursuing.

## Replacement fidelity

“Partial” means related functionality, not drop-in compatibility.

| Candidate | Recurring docs | Structural graph | Canonical glossary | Settled lessons | Exact idea capture |
|---|---:|---:|---:|---:|---:|
| OpenWiki | Full | — | — | — | — |
| codebase-memory-mcp | — | Full | — | — | — |
| `opencode-codebase-index` | — | Partial–strong | — | — | — |
| RepoRecall | Partial | Partial | — | Weak partial | — |
| `pi-llm-wiki` | Different wiki | — | — | Partial research synthesis | — |
| `pi-hermes-memory` | — | — | — | Partial | — |
| Gentle Engram | — | — | — | Partial | — |
| ProjectMem | — | — | — | Partial | Partial |
| `pi-knowledge` | — | — | — | Retrieval only | — |
| Notes packages | — | — | — | — | Partial |
| Pi core | — | — | — | — | — |

## Findings

### Pi core — reject as a durable-knowledge replacement

**Mechanism:** Pi stores JSONL session trees and supports resume, fork, clone, labels, export, and compaction. Extensions can persist custom session entries and react to lifecycle hooks. Prompt templates and Skills supply reusable instructions. [Sessions](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/sessions.md), [compaction](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/compaction.md), and [extensions](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/extensions.md) confirm these are conversation/runtime primitives, not curated repository knowledge.

**Verdict:** **REJECT as replacement; KEEP as substrate [HIGH].**

**Residual qq:** All five surfaces. Pi can host a package implementing them, but building another qq-owned extension would not achieve the requested maintenance transfer. Prompt templates also require slash-style invocation and cannot implement the `idea:` prefix transaction by themselves.

### OpenWiki upstream — adopt/keep

**Mechanism:** Maintained Node CLI that generates `openwiki/` Markdown from code, honors operator-owned `INSTRUCTIONS.md`, and supplies GitHub/GitLab/Bitbucket PR workflows. Current upstream is MIT, v0.2.0, Node ≥22, with Vitest, coverage, typecheck, lint, and focused tests for checkpoints, docs-only behavior, prompts, redaction, and telemetry. [Repository](https://github.com/langchain-ai/openwiki), [package metadata](https://github.com/langchain-ai/openwiki/blob/main/package.json), [tests](https://github.com/langchain-ai/openwiki/tree/main/test).

**Fidelity:** Full for source-derived recurring documentation. Its user-owned instruction contract aligns closely with qq’s [OpenWiki instructions](/home/qqp/projects/qq/openwiki/INSTRUCTIONS.md).

**Verdict:** **ADOPT/KEEP [HIGH].** This is already the best maintained product for the job; switching generators would be regression.

**Inference:** The plausible shrink path is upstream’s scheduled CI workflow opening a docs PR. Before retiring qq’s wrapper, a disposable-repository trial must prove:

- fresh `main` is the generation base;
- linked `AGENTS.md`/`CLAUDE.md` cannot be overwritten;
- output is confined to `openwiki/`;
- provider and telemetry policy are acceptable;
- operator review and merge remain mandatory.

**Residual qq:** Keep the current [wrapper](/home/qqp/projects/qq/bin/qq-openwiki) and [maintainer contract](/home/qqp/projects/qq/skills/openwiki-maintainer/SKILL.md) until those checks pass. Afterward, the wrapper might retire and the maintainer contract shrink to a short review/merge policy.

### `@zosmaai/pi-llm-wiki` — reject as OpenWiki replacement

**Mechanism:** Pi extension, Skill, and prompt package that converts URLs, PDFs, Markdown, XML, JSON, and pasted text into `.llm-wiki` source packets, concept pages, backlinks, and synthesis pages. It is actively maintained—v0.10.4, MIT, tests and CI—but its durable project/company Git-tracked workflow is still described as future work. [Pi package](https://pi.dev/packages/%40zosmaai/pi-llm-wiki), [repository](https://github.com/zosmaai/pi-llm-wiki).

**Verdict:** **REJECT as replacement; HOLD as optional research library [HIGH].**

**Fidelity:** It synthesizes supplied information; it does not derive operational documentation from merged code or produce reviewed docs-only PRs.

**Residual qq:** OpenWiki, its maintainer workflow, glossary, graph, compound, and idea all remain.

### RepoRecall — hold as an integrated future challenger

**Mechanism:** Local CLI/daemon plus MCP server combining AST indexing, call graphs, semantic search, generated wiki/business pages, persistent memory, freshness banners, and an architecture dashboard. It has tests and stress harnesses, MIT licensing, roughly 90 commits, and a recent npm v0.8.1. [npm](https://www.npmjs.com/package/%40proofofwork-agency/reporecall), [repository](https://github.com/proofofwork-agency/reporecall).

**Observed limitation:** Its README calls adoption “nascent,” and its advertised token-reduction section explicitly says the 40–70% numbers are placeholders awaiting real runs. Its automatic hook experience targets Claude Code; Pi would require CLI use or an adapter.

**Verdict:** **HOLD [MEDIUM].**

**Fidelity:** Promising partial coverage of docs, graph, and memory, with unusually good staleness disclosure. It has no documented equivalent to merged-main operational prose, user-authored wiki instructions, docs-only PR review, arbitrary graph queries, canonical glossary governance, or compound/idea eligibility rules.

**Residual qq:** All governance surfaces remain. It could eventually challenge OpenWiki plus codebase-memory together, but is not mature enough to justify a migration.

### codebase-memory-mcp — adopt/keep

**Mechanism:** Third-party MIT static binary using tree-sitter and SQLite to build a persistent graph. It supports well over 150 languages, symbol and route relationships, callers/callees, impact analysis, architecture/clusters, snippets, semantic search, and arbitrary Cypher-like `query_graph`. v0.9.0 was released July 8 with signed release metadata. [Repository](https://github.com/DeusData/codebase-memory-mcp), [v0.9.0 release](https://github.com/DeusData/codebase-memory-mcp/releases/tag/v0.9.0), [research preprint](https://arxiv.org/abs/2603.27277).

The locally installed binary is v0.9.0. It is not operator-owned; qq only owns routing guidance. [.mcp.json](/home/qqp/projects/qq/.mcp.json) declares Context7, not codebase-memory, so Pi already reaches it through the CLI route in [AGENTS.md](/home/qqp/projects/qq/AGENTS.md).

**Verdict:** **ADOPT/KEEP [HIGH].**

**Fidelity:** Full against qq’s structural requirements: graph search, path tracing, snippets, arbitrary graph queries, and architecture summaries.

**Residual qq:** Only small Pi routing instructions remain. That coupling is cheaper and more reliable than replacing the graph with a weaker package merely for native tool registration.

### `opencode-codebase-index` — shortlist as the best Pi-native challenger

**Mechanism:** First-class Pi extension and packaged Skill backed by Rust/tree-sitter, SQLite, BM25, vector embeddings, branch-aware indexes, file watching, call graphs, shortest paths, PR impact, and knowledge-base directories. v0.14.0 was released July 8; the repository has substantial tests, retrieval evaluation harnesses, signed releases, 474 commits, and Pi 0.80.2 development compatibility with an unrestricted Pi peer range. [npm/README](https://www.npmjs.com/package/opencode-codebase-index), [repository](https://github.com/Helweg/opencode-codebase-index), [v0.14.0 release](https://github.com/Helweg/opencode-codebase-index/releases/tag/v0.14.0).

**Verdict:** **SHORTLIST [HIGH].** This is the best maintained Pi-native option and the most valuable pilot.

**Fidelity:** Strong semantic discovery, snippets, callers/callees, call paths, branch freshness, and PR blast-radius analysis. Its graph currently covers a much narrower language set and does not expose codebase-memory’s arbitrary graph query, rich route/resource schema, cross-repository graph, ADR/runtime-trace ingestion, or equivalent `get_architecture`.

**Residual qq:** If adopted only for QoL, all current surfaces remain. If piloted as a replacement, retain codebase-memory and its routing until a representative corpus of qq’s architecture, dependency, route, and impact questions passes. Avoid running two permanent code indexes unless measured benefit warrants it.

### Other code-index candidates

- **`pi-cbm` — HOLD [LOW/MEDIUM].** v1.1.0 claims native codebase-memory tools, auto-indexing, and token optimization, with the highest catalog use among the dedicated bridges. Its full source/test surface could not be fetched during this investigation, and registry metadata exposes typecheck/build checks but no test script. [Catalog entry](https://pi.dev/packages/pi-cbm).

- **`pi-codebase-memory-mcp` — HOLD [MEDIUM].** Its published extension maintains a long-lived MCP subprocess, dynamically registers `cbm_*` tools, reconnects, and retries once. It is only v0.1.2, has no visible tests, and its packaged guidance advertises `/cbm` commands while source registers a `cbm_connect` tool. [Package](https://pi.dev/packages/pi-codebase-memory-mcp), [repository](https://github.com/porameht/pi-codebase-memory-mcp).

- **`pi-codebase-memory-bridge` — REJECT [MEDIUM].** It performs a one-time MCP schema handshake and shells out to the CLI per call; it requires initial indexing and has negligible adoption. This adds another failure layer without removing the backend. [Package](https://pi.dev/packages/pi-codebase-memory-bridge).

- **`@fodx/codelens` — HOLD [MEDIUM].** Active Pi-native branch-aware FTS5/tree-sitter graph with calls/imports/tests/definitions, tests, benchmarks, and a July 18 v2.4.1 release. It is the second-best native graph challenger, but its relation schema and language evidence remain narrower than codebase-memory’s. [Package](https://pi.dev/packages/%40fodx/codelens).

- **`@arvoretech/pi-codebase-index` — HOLD for centralized search, REJECT for graph replacement [HIGH].** It supplies Pi-native semantic snippets but needs an HTTP backend, authentication, embeddings, and usually Qdrant; it has no structural graph. [Package](https://pi.dev/packages/%40arvoretech/pi-codebase-index).

- **Supi Code Intelligence, `pi-shazam`, and `pi-readseek` — REJECT as graph replacements [HIGH].** They provide strong LSP/tree-sitter diagnostics, navigation, rename, anchored editing, or local impact tools, but not a persistent general relationship graph. [Supi](https://pi.dev/packages/%40mrclrchtr/supi-code-intelligence), [Shazam](https://pi.dev/packages/pi-shazam), [Readseek](https://pi.dev/packages/pi-readseek).

### Shared glossary — keep `CONCEPTS.md`

The glossary’s essential behavior is authority, not retrieval: stable definitions are operator-owned, versioned, and must be read before work. That contract is explicit in [CONCEPTS.md](/home/qqp/projects/qq/CONCEPTS.md) and [AGENTS.md](/home/qqp/projects/qq/AGENTS.md:28).

**Verdict:** **KEEP [HIGH].**

No reviewed package provides an equivalent. Memory/RAG packages may retrieve a relevant definition, omit one, or surface obsolete text; they cannot become canonical without changing qq’s governance. Pi’s context-file mechanism can mandate reading the glossary, but does not itself maintain or validate it.

**Residual qq:** Keep `CONCEPTS.md` and the read-before-work instruction. Indexing it in a search package is safe only as an additive retrieval aid.

### `compound` and lesson/decision capture

The current [compound contract](/home/qqp/projects/qq/skills/compound/SKILL.md) is unusually narrow: capture only after an operator-settled no-change decision, accepted verified diagnosis, or landed dependency; deduplicate against existing solutions; preserve Symptom, Root cause, Resolution, and Verification; update the glossary only for genuinely stable vocabulary.

No candidate matches that gate.

- **`pi-hermes-memory` — SHORTLIST for QoL, REJECT as compound replacement [HIGH].** It is the strongest Pi-specific memory package: Markdown plus SQLite FTS5, project/global memories, session search, secret scanning, policy-only injection, background review, correction capture, compaction/shutdown flushes, consolidation, and managed procedural Skills. It has active releases and a large source test suite. [Package](https://pi.dev/packages/pi-hermes-memory), [repository](https://github.com/chandra447/pi-hermes-memory). Its automatic capture occurs before qq’s settlement and landing gates. A conservative pilot should initially disable automatic review, correction detection, and flush-triggered writes.

- **Gentle Engram — SHORTLIST only for cross-agent sharing [MEDIUM].** Mature local Go/SQLite memory with CLI, HTTP, MCP, TUI, Git synchronization, conflict handling, and structured What/Why/Where/Learned records. It is more operationally expensive and still lacks compound’s eligibility and causal-document contract. [Pi package](https://pi.dev/packages/gentle-engram), [core repository](https://github.com/Gentleman-Programming/engram).

- **`pi-memory` — HOLD as the simpler transparent option [HIGH].** Plain Markdown long-term memory, daily logs, scratchpad, optional qmd semantic search, and tests. Easier to audit than Hermes but offers less governance and can inject ambient memory. Choose it instead of Hermes, not alongside it. [Package](https://www.npmjs.com/package/pi-memory), [repository](https://github.com/jayzeng/pi-memory).

- **ProjectMem — HOLD [MEDIUM].** Append-only typed issues, attempts, fixes, decisions, and notes; deterministic summaries; stale-memory detection; pre-commit gate; MCP/CLI; and tests. Its model captures activity continuously and installs hooks/watchers, whereas compound records only settled reusable conclusions. [Repository](https://github.com/riponcm/projectmem), [PyPI](https://pypi.org/project/projectmem/), [paper](https://arxiv.org/abs/2606.12329).

- **`pi-prior` and `pi-experiences` — REJECT as replacements [HIGH].** Prior turns scored traces into human-approved short heuristics; Experiences creates approved When/Do behavioral habits and explicitly distinguishes those from facts and decisions. Neither creates evidence-backed causal solution records. [Prior](https://pi.dev/packages/pi-prior), [Experiences](https://pi.dev/packages/pi-experiences).

- **`pi-total-recall` — REJECT [HIGH].** It activates multiple overlapping memory/search systems and requires Node 24+, adding redundancy without compound fidelity. [Package](https://pi.dev/packages/pi-total-recall).

**Residual qq:** Keep `compound` even if a general memory package is adopted.

### `idea` capture

The [idea contract](/home/qqp/projects/qq/skills/idea/SKILL.md) is a precise transaction: only `idea:` or explicit `$idea`, exact text, timestamp, one Backlog Ideas document, duplicate refusal, no interpretation or research, one-line acknowledgment, then resume the active task.

**Verdict:** **KEEP [HIGH].**

- **`@firstpick/pi-extension-notes` — REJECT as replacement [HIGH].** Provides ordinary Markdown note CRUD, editor integration, fuzzy lookup, and `/note`; it does not implement the trigger, singleton, verbatim, duplicate, or resume semantics. [Package](https://pi.dev/packages/%40firstpick/pi-extension-notes).

- ProjectMem’s `plan.md`, `pi-memory` scratchpad, and stash packages are likewise general stores, not exact capture transactions.

A custom Pi extension could intercept message prefixes, but that would replace a tiny declarative Skill with new qq-owned executable machinery—the opposite of the requested simplification.

## QoL additions that replace nothing

Prioritized recommendations:

1. **Pilot `opencode-codebase-index` [HIGH].** It adds semantic “find by meaning,” branch-aware results, definition ranking, similar-code discovery, and PR impact. First test it as a temporary challenger to codebase-memory, not a permanent second index.

2. **Shortlist `pi-knowledge` [MEDIUM].** Local Pi-native hybrid retrieval across code, Markdown, PDFs, DOCX, URLs, and notes using SQLite FTS5 and local embeddings, with update/watch/doctor/export/import tools and a serious test/release structure. It could make OpenWiki, `CONCEPTS.md`, and research material easier to retrieve without changing their authority. v0.5.2 was published July 19 and repository adoption is still small, so pilot before normalizing it. [Package](https://pi.dev/packages/pi-knowledge), [repository](https://github.com/nczz/pi-knowledge).

3. **Shortlist one general memory package [MEDIUM].** Prefer `pi-hermes-memory` for Pi-only session recall, secret scanning, and conservative policy injection; prefer `pi-memory` for plain-Markdown simplicity; prefer Gentle Engram only when cross-agent or cross-machine sharing is an actual requirement. Do not install all three.

4. **Do not treat memory as authority [HIGH].** Any adopted memory package should point back to source, OpenWiki, Backlog records, and `CONCEPTS.md`; it should not silently revise them or inject captured guesses as settled project truth.

## Sources used

- Local qq contracts: [AGENTS.md](/home/qqp/projects/qq/AGENTS.md), [CONCEPTS.md](/home/qqp/projects/qq/CONCEPTS.md), [OpenWiki instructions](/home/qqp/projects/qq/openwiki/INSTRUCTIONS.md), [wrapper](/home/qqp/projects/qq/bin/qq-openwiki), [maintainer](/home/qqp/projects/qq/skills/openwiki-maintainer/SKILL.md), [compound](/home/qqp/projects/qq/skills/compound/SKILL.md), [idea](/home/qqp/projects/qq/skills/idea/SKILL.md), and [.mcp.json](/home/qqp/projects/qq/.mcp.json).
- Pi core: official [sessions](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/sessions.md), [compaction](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/compaction.md), [Skills](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md), [prompt templates](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/prompt-templates.md), [extensions](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/extensions.md), and [packages](https://pi.dev/docs/latest/packages). Context7 `/earendil-works/pi` corroborated the same official session, context-file, and extension behavior.
- Primary product/package sources linked inline above: OpenWiki, codebase-memory-mcp and its paper, `opencode-codebase-index`, RepoRecall, `pi-llm-wiki`, `pi-knowledge`, Hermes, Engram, ProjectMem, and the named Pi catalog candidates.

## Gaps and unverified items

- No candidate was installed or executed; release checks, source inspection, test layouts, and documentation were evaluated statically.
- No representative qq query corpus was run against `opencode-codebase-index`, CodeLens, or RepoRecall. That is the key evidence needed before changing the graph decision.
- Upstream OpenWiki’s CI workflow was not exercised against qq’s symlinked instruction files, long-lived update branch, provider restriction, or docs-only review boundary.
- `pi-cbm` source retrieval was incomplete because its new repository/package artifacts were unavailable through the restricted fetch path. Its ranking therefore remains low-confidence.
- Package download, star, issue, and release counts are July 19 snapshots and will change.
- Vendor benchmark claims were not reproduced. RepoRecall’s own README identifies its token figures as placeholders; codebase-memory’s paper and `opencode-codebase-index` evaluation harness are stronger evidence but still require a qq-specific check.
- Context7 had useful coverage for Pi core, but not enough verified coverage for the niche third-party packages to replace their repositories and published source as evidence.
