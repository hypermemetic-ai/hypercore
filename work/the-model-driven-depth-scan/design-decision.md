# design-it-twice: the shared depth-assessment seam [machine]

A load-bearing interface for 'the shared depth-assessment seam' was designed twice — candidates minimal, flexible, caller,
ports, each briefed to design the same seam radically differently — and compared on depth, locality,
and seam placement. The seam is the single place the model-driven depth judgment is computed,
consulted by the standing whole-tree scan (#8) and fed the one flagged file at the fold (#9).

design-decision: the shared depth-assessment seam → minimal (with the transport injected, ports-flavoured) — one verb
`assess(targets, review, transport) -> Assessment(findings, lean, flip)` is the deepest shape: it is
handed the architecture review's already-computed `Review` (it consults that map, never walking the
tree a second time), a target set, and the model transport (injected, so the verdict is deterministic
under a scripted fake exactly like every other seam); it hides the depth-judgment prompt assembly, the
map-consultation, and the finding shape behind one small surface. Both scopes differ only in their
target set and their disposition: the standing scan passes the whole module list and commits a watched
verdict trace; the at-fold assessment passes the one flagged file and raises advisory prose with a lean
and a flip. The depth standard lives in exactly one module, so there is no second copy to drift.

## Grounds

- **minimal**: one `assess(targets, review, transport)` over a target set, the Review consulted and the
  model injected. Smallest surface every caller pays; the depth-judgment assembly, the map-consultation,
  and the finding shape are all pulled down inside. Deletion test: removing it scatters the prompt
  assembly and the Review-consultation into both the standing scan and the integrate path. Deepest on
  depth and locality; the chosen shape.
- **flexible**: two public entries `scan_tree(review, transport)` and `assess_file(rel, review, diff,
  transport)` sharing private internals. Future scopes are cheap, but two verbs is a wider interface
  paid by every reader, and the two bodies overlap almost entirely — it risks restating the
  depth-judgment assembly twice or threading a mode flag. Shallower than one `assess` over a target set.
- **caller**: shape the seam around the dominant caller (the standing scan runs on the read-live path;
  the at-fold path is rare). Optimising the standing caller pushes the one-file at-fold case into an
  awkward special form (a single target dressed as a whole tree) and couples the seam to the standing
  render cadence. Worse locality.
- **ports**: isolate the model behind a named adapter object the core never references. The minimal
  candidate already injects the transport (the ports benefit — a scripted fake in the check, codex
  live), so a separate adapter is ceremony the one transport seam does not earn. Folded into the pick
  as the injected-transport flavour rather than a standalone candidate.
