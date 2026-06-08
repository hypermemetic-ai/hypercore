# options - 011-phase-one-routing

Direction options are drafted by the machine for operator selection. The operator
selects one route, rejects all options, or aborts without writing direction.

## option 1

id: contract-only-denaming
kind: selected-route
summary: De-name the whole contract (collaboration/loop/adapter statements and machine statements, the adapter prose, and check.sh) to role and config terms; add the phase-one collaborator role and a phase-one routing/delegation seam with held defaults; keep the materialization product-specific, including the existing CODEX_* environment-knob names, which are materialization config rather than contract.
reversibility: one-way
tradeoff: Smallest diff to the running mechanism and to operator muscle memory; the contract is fully product-agnostic, but config-knob identifiers still read CODEX_*, a minor residual product name at the materialization edge.

## option 2

id: contract-and-knob-denaming
kind: selected-route
summary: Everything in option 1, plus neutralize the config-knob identifiers themselves (the CODEX_* environment variables become harness-neutral names), keeping the old names as cheap aliases where practical so existing configuration does not break.
reversibility: one-way
tradeoff: Fullest product-agnostic surface, down to the environment-variable names; larger blast radius across the loop.sh env interface, check.sh, and any references to the knob names, with alias upkeep to avoid breaking existing CODEX_* configuration. Also collides with the queued two-step builder-routing work unless alias and default precedence are nailed down now, since two-step later flips the builder default and must stay intelligible across both the old and the neutral knob names.

## rejection choices

none: Reject all options and send the work back to frame for a different route surface.
abort: Abort without recording direction.
