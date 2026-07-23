---
id: doc-83
title: Formatter canon primer — harness-wide doctrine options (T-147 briefing)
type: guide
created_date: '2026-07-23 02:13'
updated_date: '2026-07-23 02:14'
tags:
  - guide
---
# Formatter canon primer — harness-wide formatting doctrine options (T-147 briefing)

**Audience:** the operator, for the canon decision window. Plain language; no
formatter background assumed. Reading time ~20 minutes.

## Why this exists

On 2026-07-22 pi-lens's turn-end autoformat rewrote a test file in deciq's
primary main three times, blocking `qq-change land` each time. Root cause
(confirmed in pi-lens source): a bash restore command (`git show HEAD:f > f`)
re-queues the file for deferred formatting, so each restore re-armed the next
rewrite. Two lessons:

1. qq's land rail works — it caught every occurrence.
2. A formatter pass over a repo that never adopted that formatter is
   off-contract churn. The same pass over a repo that *has* adopted it is free
   consistency. This Task is about choosing adoption deliberately.

## What a code formatter is

A tool that rewrites source layout (indentation, spacing, line breaks) to a
fixed style without changing behavior — verified by parsing, not text
munging. "Canon" means: the repo adopts one formatter's style as law and its
Checks fail anything unformatted. Benefits: every file looks the same
regardless of author (human or agent), and style noise never appears in PR
diffs again. Costs: a one-time reformat of the whole tree, and the check
gate thereafter.

## The candidate tools (one per language is normal)

**Python — ruff format** (recommended for Python repos)
- From Astral; the Python ecosystem's current standard. `ruff format` is
  black-compatible (same style as the long-time incumbent `black`) but much
  faster and shares the binary with the `ruff check` linter.
- **deciq already runs `ruff check`** in its Checks, so adopting `ruff format`
  there extends a trusted tool instead of importing a new ecosystem.
- Config: optional (`pyproject.toml`); defaults are the community standard.

**JavaScript/TypeScript — biome** (recommended for TS/JS surfaces)
- One fast binary, formats and lints, near-zero configuration, defaults are
  the modern community style. Successor to prettier (older incumbent; fine
  but slower and a dependency tree).
- Covers qq's `extensions/*.ts`, `.pi/extensions/*.ts`, `lib/*.mjs`.
- Config: optional (`biome.json`); defaults recommended.

**Shell — shfmt** (not recommended initially)
- The standard bash formatter, but a Go binary with no clean npx-style
  provisioning: every qq machine and CI would gain a manual dependency for
  layout-only value. Bash stays human-styled, suite-gated. Revisit later if
  wanted.

**Markdown — none** (not recommended)
- Prose formatting canon is high-noise/low-value. qq already guards prose
  with the only-down ratchet and pi-lens's inline markdownlint autofix.

## What adopting canon mechanically means (per Repository)

1. One mechanical commit that reformats the tree (review is trivial: the
   check is green before and after, and nothing else is in the diff).
2. A new Check in the suite running the formatter's check mode
   (`biome format` / `ruff format --check`); any unformatted file fails.
3. Optional config file pinning style choices; defaults are recommended
   (zero config = zero maintenance of opinions).

## The pi-lens interplay (why canon makes autoformat an asset)

pi-lens's turn-end pass runs `ruff format`/`biome format` on agent-written
files and respects each repo's config. With canon adopted, edit-time
formatting and check-time enforcement agree, so autoformat becomes useful
instead of churn. The deciq restore-loop residue: with canon, a
restore-reformat produces canon output (semantically null); qq's doctrine
(agents never write in primary; operator-staged commands per T-144) removes
the primary-write vector; the land rail is the backstop. No new machinery.

## Recommendation

- **Harness-wide rule:** each Repository adopts the canon formatter for its
  languages, enforced in its own Checks. Not one tool everywhere — one tool
  per language, chosen once here.
- **qq repo:** biome over the TS/JS surfaces (bash/markdown excluded).
  One-time reformat + `tests/test-format.sh`.
- **deciq (separate Repository, separate decision):** add `ruff format
  --check` to `scripts/check.sh` beside the existing `ruff check`; one-time
  reformat. Carry the offer to the deciq side when this Task opens.
- **Other linked projects:** adopt at next natural touch; no retrofit
  campaign.

## Decisions the operator makes in the canon window

1. Adopt the per-language canon rule (ruff/Python, biome/TS-JS) or amend.
2. qq scope: confirm biome-only, or add bash (shfmt + provisioning) /
   markdown.
3. Defaults vs configured style (recommend defaults).
4. Whether deciq's adoption is offered now or later.
