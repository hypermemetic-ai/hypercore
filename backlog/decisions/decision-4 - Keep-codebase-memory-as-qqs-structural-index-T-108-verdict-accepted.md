---
id: decision-4
title: Keep codebase-memory as qq's structural index (T-108 verdict accepted)
date: '2026-07-19 21:27'
status: accepted
---
## Context

T-108 ran the settled structural-first pilot of opencode-codebase-index 0.14.0
against codebase-memory 0.9.0 over the qq repo (12-question corpus:
architecture, dependency, route, impact; no embeddings provider). Result:
challenger 0/12 — every structural path including index_codebase refuses
without an embedding-capable provider; incumbent 7 correct / 2 wrong / 3
cannot-answer, with extensionless bin/qq-* entrypoints unmodeled. Evidence:
pilot/ on main (corpus, comparison, 35 raw responses), PROPOSED verdict in
pilot/proposed-verdict.md.

## Decision

Operator accepted the proposed verdict 2026-07-19: KEEP codebase-memory as
qq's sole structural index. No second permanent index; no AGENTS.md routing
change. Reconsideration requires a challenger trial with a provider-free
structural index path AND verified inclusion of extensionless Bash
entrypoints.

## Consequences

- opencode-codebase-index is not adopted; no embeddings provider is
  provisioned for it.
- codebase-memory's extensionless-entrypoint gap stays visible as its known
  weakness; corpus questions touching bin/qq-* bodies need source
  verification (as AGENTS.md already requires).
- The pilot/ evidence and this record are the citation for any future
  retrial alignment.
