---
kind: ask
state: standing
owner: operator
created: 2026-06-22
---
# adr-current-state — dissolve the decision corpus, retire the ADR concept

The operator settled it: hypercore retires the ADR concept entirely. A decision is already
recorded three ways without a hand-tended corpus — (a) a settled decision **card is a node**, so
the decision and its grounds ride on the node and **archive with the work** (`work/` → `work/archive/`);
(b) the decision's **outcome** lives in the living spec, the glossary, and intent; (c) design and
research **provenance is material on its node** (archives with it). The hand-written ADRs under
`spec/decisions/` were a redundant, hand-tended fourth copy that drifted ~16 terms behind the system.
This reverses the earlier "rewrite the ADRs to current state" framing: there is nothing to rewrite —
the corpus is dissolved.

## what was done
- **`spec/decisions/` deleted** — all 22 hand-written ADRs removed; nothing recreates the folder.
- **The term "ADR" retired across the corpus** — every `(ADR NNNN)` citation in `engine/`,
  `README.md`, `glossary.md`, and `spec/` dropped or reworded; the glossary `**ADR**` entry removed.
- **Design-decisions are node material** — `design.record` writes `design-decision.md` onto the
  contest node (carrying the parseable `design-decision: <subject> → <chosen> — <reason>` line and
  the `[machine]` marker), archiving with the work, not a numbered file under `spec/decisions/`.
- **The worker reference tail retired** — the worker holds the spec whole (the whole-picture
  keystone, sacred) and greps `work/archive/` in its own fence checkout for the long history and
  grounds of past decisions, just-in-time; no `spec/decisions/` pull.
- **The accepted-length record relocated** — it is live gate-state that must outlive the work, so it
  cannot archive on a node. The depth gate (`conditions.accepted_at`) now reads a **provisional**
  repo-root `accepted-lengths.md`. Its proper home and write path are deferred as debt
  (`work/accepted-length-home/`).

## folding condition
- `spec/decisions/` gone and not recreated; zero "ADR" mentions across `engine/`, `README.md`,
  `glossary.md`, `spec/`; design-decisions land as node material; the worker tail points at
  `work/archive/`; the accepted-length record reads from the provisional repo-root file with the
  proper-home debt filed; `python3 -m engine --check` is green.
