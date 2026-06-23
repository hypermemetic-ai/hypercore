# scenario-gate — provenance: the evidence

Research behind the grilling pass (2026-06-23). Provenance, not standing: the design cites it,
nothing depends on it.

## Concern 1 — strict red/green with frontier LLMs

The distinction that decided it: **tests-as-a-verification-gate** is well-supported; **test-first
ordering specifically helping an LLM** is not (no clean ablation isolates it; the human-TDD
meta-analysis finds the measured benefit is "tests exist," not "written first"). hypercore was
already on the supported side — test-*gated*, not test-*first*. The real, capability-scaling risk is
**reward-hacking the gate**, and stronger models hack *more* — acute precisely when the **builder
authors its own oracle**. That drove D1 (move oracle ownership to the architect). The one
ordering-specific benefit that *is* defensible — proving the gate bites (red before green) — is kept:
the architect's scenario must go red at the fork base, green at the tip.

- ImpossibleBench — arxiv 2510.20270 — frontier models cheat tests at high rates; "stronger models
  cheat more"; access controls beat instructions. The cautionary keystone.
- Mathews & Nagappan, *TDD for Code Generation* — arxiv 2402.13521 — tests-present-vs-absent gains;
  not an ordering ablation.
- *Investigating Test Overfitting on SWE-bench* — arxiv 2511.16858 — visible-pass / hidden-fail gap.
- Rafique & Mišić, *TDD meta-analysis* — IEEE 6197200 — human base rate: small quality gain, the
  ordering effect weak.
- Anthropic best-practices; Simon Willison, red/green — the defensible "red first" benefit (it proves
  the gate bites) and commit-the-test-first as anti-tamper.

## Concern 2 — test-suite organization

The on-point guidance: organize an agent's acceptance suite by **durable capability / behavior,
behind a stable seam** — not by the **unit of delivery** (a slice / work-item), which churns. Couple
the gate to behavior; let the builder find and extend by capability. That is exactly the
by-slice → by-capability move, and the spec → DSL/driver → system seam discipline is the deep-module
form D2 adopts.

- AAID acceptance-testing workflow — github.com/dawid-dahl-umain/augmented-ai-development — organize
  specs by domain concept, the four-layer model, agent-navigable naming. The most directly
  applicable source (an acceptance suite as the contract for an AI builder).
- quii, *Scaling Acceptance Tests* (learn-go-with-tests) — Specification → DSL → Driver → System;
  decouple test structure from system structure.
- Dave Farley, four-layer executable specifications; Architecture Weekly on vertical slices (maximize
  coupling *within* a slice, do not couple the *gate* to the delivery unit).
