# manual archive - 011-phase-one-routing

Adopted manually on 2026-06-08, following the precedent of 008/009/010: the loop's automated
phase-two archive does not reliably carry methodology self-changes (the loop rewriting its own
`check.sh`/`loop.sh` mid-run), so the work was built and adopted by hand under independent
scrutiny equivalent to the loop's required acceptance.

## what happened

- Phase two (`loop.sh execute`) built **unit-001** (the contract de-naming + the product-absence
  check + role/held-default assertions) via a cleared strong-model builder. `./check.sh` green;
  tier-one acceptance PASS (real reviewer). The loop then halted at the resumable-cache record
  step before unit-002 and before the tier-two panel. No deterministic cause was found (the hash
  tool is present and every cache predicate passes on the saved artifacts) — it reads as a
  transient/ordering quirk in the cache code, not a build or acceptance failure.
- **unit-002** (the grammar self-tests, the two recorded debts, the comment de-naming in the
  orchestrator) was built by a cleared strong-model builder by hand. `./check.sh` green.
- The independent one-way **tier-two acceptance panel** (5 lenses, strong model, read-only) was
  run by hand since the loop halted before it. Result: `whole-acceptance-conformance`,
  `proof-integrity`, `independent-coherence`, `security-permissions` = PASS; **`red-team` = FLAG**
  — the product-absence scanner used word-boundary guards, so a product token embedded in a larger
  identifier (`HYPERCORE_CODEX_BUILDER_MODEL`, `CodexHarness`, `Review_GPT-5`) slipped through,
  violating the signed "no loophole" acceptance. No current violation existed (the de-named
  contract had no such token), but the check did not meet the signed bar.
- The loophole was fixed by a cleared strong-model builder (substring detection, exemptions and
  scoping preserved) plus an embedded-token self-test; `./check.sh` green; the **`red-team` lens
  re-judged PASS** (its own reproducers now caught, no new false positives). Raw lens outputs are
  preserved under `phase-two/tier-two-panel/`.

## carried debts (recorded in adapter/codex.md)

- the strong review floor is not yet mechanically pinned to a checked strong model (it can ride an
  ambient harness default); a future loop pins it.
- the phase-one one-way review reviewer prompt assumes a signed, route-settled frame and so cannot
  PASS a correctly-staged pre-direction frame (non-discriminating); a future loop re-prompts it.

## also surfaced — loop-hardening for a future loop, not folded here

- the resumable-cache record step halted this run after a clean unit-001 + tier-one PASS;
- the loop's implement(material) -> archive(fold intent) split does not fit work whose proof is a
  check over the intent statements themselves: to keep the intent-scanning product-absence check
  green at the implement boundary, the builder had to de-name intent during implement rather than
  leaving the fold to archive.

## adoption

`./check.sh` green; the contract is product-agnostic across `collaboration`/`loop`/`adapter`
(intent + machine statements), `hypercore.md`, and `intent/organizing-document.md`; the phase-one
collaborator, throughput-delegation, review-floor-independence, and routing statements are present
with held defaults; materialization (`adapter/codex.md`, `AGENTS.md`, `adapter/loop.sh`) still
binds the current harness and runs phase two. Touched segment feet remain endorsed by qqp-dev (the
signer).
