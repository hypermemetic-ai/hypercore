---
name: hypercore
description: Drive the hypercore graph — status first, statement verbs, execution graphs in the operation alphabet (frame/gather/derive/generate/test/commit), folding, and what only the operator may decide. Use whenever working in this repository.
---

# Driving hypercore

The database is the source of truth; everything readable on disk is a derived
view. Never hand-edit the root markdown, `work/`, `engine/graph.json`, or
`engine/statements.json` — author through the verbs, and every verb rewrites
every view.

All commands run from `engine/`: `../.venv/bin/python -m hypercore <verb>`.

## Start every session

1. `status` — pending endorsements, open work, recent folds.
2. Browse `work/<id>/README.md` for where each open graph stands.

## Who does what

The machine drives the verbs; the operator reads derived views (root
markdown, `status`, the viewer) and spends judgment. Operator judgment
enters in exactly three ways — never assume it:

- **endorse** — only the operator. Either they click endorse in the viewer,
  or they say it in conversation and the machine runs `endorse ID`
  recording their decision.
- **`--by operator` / `--operator-confirms`** — only when the operator has
  said so in this conversation; their words are the warrant.
- Machine-authored statements carry the trailing ` [machine]` marker; the
  machine never removes one. The machine never strikes operator-owned
  intent.

A commit operation's `decide` role is the operator's and cannot be
delegated (s_81c38173) — create the commit only once the decision exists.

## The alphabet (s_3729cb59)

A member of an execution graph is one operation: **frame · gather · derive ·
generate · test · commit**. Products are material on the operation node,
never a node kind. Relations carry the combinators (s_5365a11a):
`depends-on` (causal link), `tests`, `commits` (binds a generate),
`reframes` (frame→frame), `decomposes-into`; `contains` is membership
bookkeeping. Roles (propose/execute/judge/decide) live in props. The
alphabet never grows — name compound moves instead (s_e4f503c9).

## Compound moves (named clusters of operations)

**take-on** — bind new work to intent:
`add-statement` (if the intent isn't yet written) → `work-open --on S
--label ... --fold-when "..." --check machine|operator` → `work-add` a
frame if the problem needs instituting, and generates for candidate moves.

**run-the-loop** — the engine inside open work:
gather what's unknown → generate candidates → derive consequences (`--on`
the generate) → test (`--on` the candidate) → `work-check T --verdict
pass|fail --grounds "..."`. Re-generate while verdicts fail.

**settle-and-fold** — close it out:
the operator's word arrives → `work-add` a commit `--on` the winning
generate (its material records the decision) → `add-material` for products
→ `work-fold W [--operator-confirms]`. A machine-checked fold needs every
test passing; every fold needs a commit, or `--abandoned`.

**ratify** — the default motion (statements-11):
after the work proves something, draft it as a concrete machine-owned
statement, add it to the work's `produces` props, and leave endorsing,
amending, or striking to the operator.

## Hygiene

- New verbs only after their absence blocks work twice (anti-ceremony).
- The engine environment is load-bearing — Python 3.12, duckdb==1.4.1
  pinned; see `engine/README.md`. Do not re-derive it.
- Exercise mutating changes on a copy of the repo under /tmp first: every
  verb rewrites the real derived views in place.
- Commit to git after meaningful moves; the snapshots are the durable forms.
