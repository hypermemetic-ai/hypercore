---
id: T-125
title: Decide qq's standing agent web-access adoption
status: To Do
assignee: []
created_date: '2026-07-21 01:38'
updated_date: '2026-07-21 02:52'
labels: []
dependencies: []
documentation:
  - doc-70
  - doc-72
ordinal: 54000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
DECIDED (operator ruling 2026-07-21): adopt @juicesharp/rpiv-web-tools as qq's standing web-access package, Exa active + Brave registered standby; pi-web-access removed. No trial run — operator ruling: where authority and knowledge cannot narrow further, decide on other signals.

Rationale: doc-70 source-verified architecture audit — rpiv-web-tools: clean provider abstraction (SearchProvider/FetchProvider/ProviderMeta), CI with tsc --noEmit + 316 tests, config hardened 0600; pi-web-access: live crash paths in headless use (upstream #103/#126/#127, unmerged fixes, no CI/typecheck gate, no commits since 2026-06-25) — a process-kill risk in exactly qq's unattended delegate deployment, categorically worse than rpiv's survivable no-failover errors. Provider axis per doc-72: no independent comparison exists and vendor benchmarks mutually reverse, so provider reputation is not evidence; Exa active on the qq-like WebCode groundedness result + proven reachable from this machine; Brave registered standby for citation-precision strength and failover option value — combination held as a registered option, no routing machinery built (no preempting need).

Accepted risk with declared threat model: rpiv's SSRF guard is host-literal only (no DNS/redirect validation, upstream-acknowledged). Accepted for a single-user workstation with no internal services to reach; revisit if qq goes multi-machine or delegates gain network-adjacent surfaces.

Evidence: doc-70 (architecture audit, owner spot-checked), doc-72 (authority sweep, owner read-through; vendor benchmark reversals + official trial terms). Decision ledger: research rounds + codex/k3 execution, well-architected-over-small extension lens, zero-new-secret dropped for quality+speed, no-trial signal-based ruling, Exa+Brave combination, SSRF acceptance — all operator rulings, 2026-07-21 exchanges.
<!-- SECTION:DESCRIPTION:END -->
