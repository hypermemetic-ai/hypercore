# ADR 0014 — capabilities are flat document segments, not folders

Status: machine-owned, operator-directed (2026-06-21: "cut the folder, because capabilities are just
a way to SEGMENT a single specification"). [operator on the cut; machine on the mechanism]

## Context

The spec lived as `spec/<capability>/spec.md` — a folder per capability, each holding exactly one
file. Two cross-cutting documents that are *not* capabilities, `spec/glossary.md` and `spec/depth.md`,
were flat `.md` files. So one directory level carried two shapes (folders and flat files) with no
marker of the distinction beyond the shape itself, and every capability folder was a folder wrapping a
single leaf — ceremony. `hyper/spec.read_spec` encoded the old rule: a capability is any subdirectory
containing a `spec.md`.

The question raised: is the folder-per-capability earning its keep? The instinct that "a unit is a
folder" (ADR 0011's graph-as-folder, ADR 0012's provenance-is-material-on-its-node) is sound — but it
is about things that **bear material**. A capability does not. It is a **section of one specification**,
segmented for reading; it carries no material of its own, spawns no children, holds no provenance. The
folder was modelling a node where there is only a document segment.

## Decision

**A capability is a flat `spec/<capability>.md` — a document segment, not a folder.** The folder shape
is reserved for what genuinely bears material: the **graph node** (`work/`, `archive/`), whose
directory carries its `intent.md`, its grilling pass, and the material it produces. The cut is one line:

> **Folders bear material; flat files are documents.**

Concretely:

- `spec/` is a flat set of `<capability>.md` files, beside the non-capability segments `glossary.md`
  and `depth.md` (which were already flat — the asymmetry that looked arbitrary was the document/segment
  vs node confusion, now dissolved: they sit among the capability segments as the flat documents they
  are). `spec/decisions/` stays a directory — it is a collection of documents (the ADR tail), not a
  capability.
- `read_spec` tells a capability from a cross-cutting segment by **content** — a capability declares
  `### Requirement:` — not by shape. `cap_path` writes `spec/<name>.md`. Every path that named the old
  shape (the fold's write, the methodology skill's render and its source pointer, the slice checks)
  follows.

## Grounds

The shape now matches the thing: a document segment is a file, a material-bearing node is a folder, and
the one rule reads off the tree. It retires the single-file folder (ceremony) and the two-shapes-at-one-
level scan cost. It is a pure relocation of the on-disk *form* — `spec.py`'s docstring already held that
"the markdown form can change without touching" the delta or the view, because `spec.py` is the one
place that knows the shape; the model it returns is unchanged, so the worker (whole spec regardless) and
every acceptance check (1–14) see the same system. Nothing about *what* a capability is changed — only
the recognition that it was never a node.

Rejected in the same conversation: moving generated material (the per-capability skill, provenance) into
the capability file's neighbourhood to "justify" a folder. That inverts the cut — it is a
document-segmentation unit, so it must not become a material-segmentation one. The generated channels
(`skills/`, `AGENTS.md`) are **output, not document**; their standing home is a separate structural
question, decided with the pi/OMP harness seam (who discovers them, from where), not by folding them
into the spec.

## Consequences

`spec/` is eleven flat capability files plus `glossary.md`, `depth.md`, and `decisions/`. `hyper/spec.py`
reads capabilities by content and writes them flat; `delta.fold`, `methodology`, and the slice checks
that named `<cap>/spec.md` are updated; the materialized skills now point at `spec/<cap>.md`. Done as the
`spec-as-segments` work graph, folded by the mechanism it leaves intact. A future change that gives
capabilities material of their own (making them nodes) would carry an ADR superseding this one.
