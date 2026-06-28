# design-it-twice — the re-derive seam: how a code-bearing fold picks up the registry the replayed code just mutated

## The decision (load-bearing)

A code-bearing fold replays the worker's verified `engine/*.py` bytes onto the merged tree, then renders
the static channels. The bug: `channels.materialize` runs **in the folding process**, whose `methodology`
module — and the `channels.CHANNELS` tuple derived from it at import — were frozen before the replay. So a
fold that registers a new methodology renders the channels from the **pre-registration** registry: the new
skill and its anchor-index line are never written until a fresh process re-runs `materialize` (the
worker-disciplines drift, commit c699304). The seam decision: **where/how does the fold re-derive the
registry so the render reflects the just-replayed code** — and does it generalize to ANY module-level
registry the replayed code mutates, not only `METHODOLOGIES`.

## Candidates (isolated)

**C1 — render the merged tree in a fresh subprocess (mirror `reverify`).** After the merged-tree
re-verify is green, a code-bearing fold renders by spawning `python3 -m engine --materialize` at
`cwd=base_dir` (ENGINE_ROOT=base_dir). That fresh interpreter imports the **replayed** engine, so its
registry — and every other module-level registry — is current; it writes the channels and prints the
paths it wrote; the parent stages exactly those in the one held commit. A spec-only fold carries no
replayed code and keeps the in-process `channels.materialize` unchanged.

**C2 — in-process `importlib.reload`.** After the replay, reload `methodology`, rebuild `CHANNELS`, render
in-process.

**C3 — read the registry off disk, render in-process.** `materialize` exec's `base_dir`'s
`engine/methodology.py` source in an isolated namespace to recover `METHODOLOGIES`, then renders
in-process.

## The pick — C1, on depth, locality, generalization

- **Generalization (residue b).** C1 answers "yes, any module-level registry" **by construction**: a fresh
  process reading the replayed code is registry-agnostic — it sees `METHODOLOGIES` and anything else the
  code defines, with nothing enumerated. C2 generalizes only to the modules you name and reload in
  dependency order. C3 generalizes to nothing beyond the one dict it parses. Only C1 makes the honest
  general claim the spec will carry.
- **Locality.** C1 mirrors `scenario._run_merged` exactly — same `cwd=base_dir`, same fresh-process import
  of the replayed engine, same throwaway-record discipline. The fold's code-bearing path already does this
  for the re-verify; the render joins the seam already there. C2 mutates the long-lived architect process's
  module table permanently (a fold leaves the process altered); C3 adds a source-exec path nothing else
  uses.
- **Depth.** C1 is a small interface (render the merged tree, get the paths it wrote) over a deep
  implementation (the entire stale-import class of bugs dissolved, for every registry at once). C2 leaks
  "which modules, in what order" and risks identity breakage (exception classes, dataclasses, sibling
  `from . import x` bindings). C3 is a parse-and-exec smell fronting a partial fix.
- **Cost.** One subprocess per **code-bearing** fold — negligible beside the re-verify, which already
  spawns one process per capability. The spec-only fold pays nothing new.

No hybrid improves on C1; it subsumes the others' goals.

## The seam, placed

- `channels.materialize_merged(root)` (name the worker may sharpen): render the static channels of the
  on-disk tree at `root` in a fresh `python3 -m engine --materialize` process and return the paths
  written. `__main__.py` gains `--materialize`, which calls `channels.materialize(root)` in that fresh
  process.
- `delta.fold`: a **code-bearing** fold renders via `channels.materialize_merged(base_dir)` (after the
  green re-verify, before the commit); a **spec-only** fold keeps `channels.materialize(root)` in-process.
- The render's written paths are staged in the same one held commit, exactly as today — atomic in every
  direction, idempotent on retry.
