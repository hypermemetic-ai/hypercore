---
kind: ask
state: folded
owner: operator
created: 2026-06-21
folded: 2026-06-21
---
# spec-as-segments — capabilities are flat document segments, not folders

The spec is **one specification**, segmented into capabilities for reading. A capability bears no
material of its own — it is a *section of a document*, not a node — so its on-disk form is a flat
`spec/<cap>.md`, never a `spec/<cap>/spec.md` folder. The folder shape is reserved for the one thing
that genuinely bears material: a **graph node** (`work/`, `archive/`), whose folder carries its
`intent.md`, its grilling pass, its produced material. This retires the folder-per-capability
ceremony (a folder holding a single file) and dissolves the depth/glossary asymmetry: `spec/depth.md`
and `spec/glossary.md` were already flat because they are non-capability segments, and now they sit
among the capability segments as the flat documents they are. `read_spec` tells a capability from a
cross-cutting segment by **content** — a capability declares `### Requirement:` — not by shape.

Folders bear material; flat files are documents. That is the whole cut.

## folding condition

`spec/` is a flat set of `<cap>.md` segments (no `<cap>/spec.md` folders), `hyper/spec.py` reads them
by content and `cap_path` writes them flat, every path that named the old shape (the fold, the skill
render and its pointer, the slice checks) follows, and the full acceptance harness is green
(`python3 -m hyper --check`). The redundant `CLAUDE.md` (Claude reads `AGENTS.md` directly) is dropped
in the same pass — one anchor file, no duplicate.

## open (not this graph)

- **the generated channels' home** (`skills/`, `AGENTS.md` at root) — output, not document, so neither
  a spec segment nor annotated into the vision; their standing home is decided structurally **with the
  pi/OMP harness seam** (who discovers them, and from where). Pinned to `role-assembly`, not resolved here.
- **`archive/` into `work/`** — the graph-layout refinement (the recursion: work is active, its archive
  the memory); a separate cut, offered, not bundled.

## result — folded

`spec/` is flat: eleven `<capability>.md` segments beside `glossary.md`, `depth.md`, and `decisions/`,
no `<cap>/spec.md` folders. `hyper/spec.py` reads a capability by content (it declares `### Requirement:`)
and `cap_path` writes it flat; the fold, the methodology skill render and its source pointer, and the
slice checks follow; the materialized skills point at `spec/<cap>.md`. The redundant `CLAUDE.md` is gone
— one `AGENTS.md` serves both roles (ADR 0009 §4 amended). ADR 0014 records the cut: folders bear
material (the graph node), flat files are documents (the spec segments). All slices 1–14 green. The two
open items are recorded above, not in the vision: the generated channels' home rides the harness seam,
`archive`-into-`work` is offered separately.
