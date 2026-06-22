# ADR 0017 — the archive nests under work/, not beside it

Status: **operator-directed** (2026-06-21) — the operator named the smell ("open a project called
hypercore and immediately need to learn a bunch of jargon — archive is the complexity; hide it") and
chose the nesting, overriding ADR 0011's peer placement. The machine-side execution below is the
mechanism. [machine]

## Context

ADR 0011 ("the graph on disk is the folder") settled two things at once: that a graph is a **folder**
(the unit on disk is the graph, not the node), and that an open graph's folder lives in its parent's
`work/` while folding **moves it to a sibling `archive/`** — `work/` and `archive/` as peers at every
level, "neither existing empty." It adopted that placement as the intent's own §work law, verbatim.

The placement was challenged on the system's **first law**. `intent.md`: "operator legibility is
king… the operator reads the system's state at a glance." The repo root is hypercore's own graph
folder, so the peer placement put `archive/` — a directory of *completed history* — at the front
door, beside `work/`, where the first thing a newcomer meets is the `work`-vs-`archive` distinction
they must learn before they can read anything live. The archive is the complexity; the front door is
exactly where it should not be. ADR 0011 was told to answer for that, and on legibility grounds it
cannot: peer symmetry is an engineering aesthetic, and it loses to the front door a human reads first.

## Decision

**The archive nests inside work/.** An open graph lives in its parent's `work/`; folding moves it
into that `work/`'s own `archive/` — one level down, under the live work. Recursively the same: a
graph's folded children sit in its `work/archive/`. The front of the tree shows only live work; the
folded history is tucked one level below it.

At the repo root this means: `work/` holds the open arcs (and `work/archive/` the folded ones), and
there is no `archive/` at the root at all. The fold is still one move (`work/<g>` → `work/archive/<g>`),
location is still authoritative (a folded graph's path contains `/archive/`), and the views are still
computed by scanning `work/` recursively.

## Grounds

Legibility is king, and it decides this. The cost of nesting is small and named: "archive" living
*under* "work" reads slightly oddly, and the open/folded pair is no longer perfectly symmetric. The
benefit is the one the intent rates highest — a front door a newcomer reads without a glossary: the
top of the tree is `intent.md`, the spec, the engine, and the **work**; the archive of finished arcs
is where finished things belong, out of the first glance. ADR 0011's peer placement optimized for a
symmetry the operator never reads; this optimizes for the legibility the operator reads first.

## Consequences

- **Supersedes ADR 0011 in its placement only.** ADR 0011's core stands untouched: a graph is a
  folder, the fold is a folder-move, views are computed by a recursive scan, `next-work.md` stays
  retired. Only `work/`+`archive/`-as-peers becomes `work/` with a nested `archive/`.
- `engine/graph.py` rewired: `read_graph`/`_scan` scan `work/` and recurse (a lone `archive/` holds
  folded siblings), and `_fold`'s destination is `parent_dir/archive` (`.../work/archive`). The
  `folded` test is unchanged (the path still contains `/archive/`). `spec/graph.md` and the intent's
  §work law are updated to the nested shape; the slice checks that asserted the root `archive/` path
  and walked `("work", "archive")` now assert `work/archive/` and walk `work/` (which contains it).
- The four folded arcs moved `archive/*` → `work/archive/*`; the root no longer carries an `archive/`.
  The acceptance harness is green across all 14 slices. Frozen records (ADRs 0001–0016, the archived
  arcs' own intents) keep their `archive/`-at-root references as written — historical, not live.
