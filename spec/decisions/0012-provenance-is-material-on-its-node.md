# ADR 0012 — provenance is material on its node; `research/` is dissolved

Status: **operator-directed** (2026-06-21) — the operator reversed ADR 0010's placement, naming the
0010 ratification as made **under false pretense** (before the graph model of ADR 0011 was
understood) and refusing to let it harden into debt; the machine-side execution below awaits
ratification. [machine]

## Context

ADR 0010 ruled that `research/` "stays as honest provenance the ADRs and README cite." That ruling
was made before the graph model (ADR 0011) was in hand — `research/` was treated as a legitimate
permanent root directory, a peer of `intent.md` / `spec/` / `hyper/`. With the graph model
understood, that is the **orphan-material smell**: `intent.md` §work L116 says the result of work
"becomes that node's material" and the folded graph's folder "holds that history whole." Research is
work product — an investigation, a design — i.e. *material of the arc whose ask produced it_, not a
root-level fixture standing on its own. A ratification whose basis has since changed does not get to
become debt (intent: "inherited debt is not carried"; "the operator and the machine are both bound
by coherence").

## Decision

**Provenance is material, and material lives with the node whose ask produced it (§work L116). The
root `research/` directory is dissolved; each note moves to its work graph.**

- `research/assembly.md`, `research/context-files.md` → **`work/role-assembly/`** — the design and
  investigation of item 2, material of that still-open arc; they fold to `archive/` with it.
- `research/regrounding.md` → **`archive/depth-regrounding/`** — the design of the folded slice-7
  depth re-grounding (ADR 0006), now a folded arc holding its own material.

ADR 0010's **sound core stands**: research is provenance, not infrastructure — a standing artifact
may *cite* it, never *depend* on it (read it at runtime, or pin acceptance to its section). The
`research/aposd.md` → `spec/depth.md` promotion stands. Only the **placement** — research as a
standalone root directory — is reversed: provenance attaches to its node.

## Grounds

The graph model makes the home unambiguous. §work L116: work's result becomes its node's material,
and the folded graph's folder holds its history whole. A root `research/` was material with no node —
exactly the structure the graph model exists to retire. The correction is intent's own coherence law
applied to a ratification whose basis had changed: the newest understanding governs, and a stale
ratification is corrected in the open, not carried as debt.

## Consequences

- `research/` no longer exists. Live citations repointed: README's "On documents", ADR 0009
  (item-2 investigated/designed → `work/role-assembly/`), ADR 0006 (the slice-7 design →
  `archive/depth-regrounding/`). The moved notes are **frozen provenance**; their own internal
  references (to the retired `research/aposd.md`, to each other) are historical and kept as written
  — the ADR 0010 precedent for frozen provenance.
- **Supersedes ADR 0010 in part** (its placement decision) and overtakes ADR 0011's "`research/` is
  unaffected" line. The cite-don't-depend discipline and the depth promotion stand.
- A future arc's provenance lands in that arc's folder from the start — there is no root `research/`
  to be swept again.
