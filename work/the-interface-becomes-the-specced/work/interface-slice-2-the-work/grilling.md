surfaced: 0

[CONTRACT]
The work view becomes the tree. The standing work no longer renders as a flat list: it renders as the tree it is, with each node's children nested beneath the node whose ask spawned them, and the view holds several foci at once because the work runs concurrently. A folded node is never an opaque dot — it carries a scent of what it holds: how many children, its shape, and whether what is under it passed or failed, so the operator reads where to look without unfolding it. And state reads from the glyph first: a node's glyph names its state, color only amplifying what the glyph already says — the slice-1 color law made concrete at the place state changes most. Motion is spent on exactly one thing — a single slow pulse on running work, stillness everywhere else. Validated against: the gated scenarios (the nested tree render, the folded-node scent, the glyph-first state read, and the running-pulse marker) go red→green. Watched on the running window: the slow pulse actually animating on running work, and stillness everywhere else.

[DELTA]
# delta — interface: the work renders as the tree, with scent and glyph-first state

## ADDED — interface

### Requirement: the standing work renders as the tree, with a scent on every folded node
The work view MUST render the standing work as the tree it is — each node's children nested beneath the
node whose ask spawned them — never a flattened list, and it holds several foci at once because the work
runs concurrently. A folded node in the view MUST never be an opaque dot: it carries a scent of what it
holds — how many children, its shape, and whether what is under it passed or failed — so the operator
reads where to look without unfolding it.

#### Scenario: a tree with depth renders nested, and a folded node carries its scent
- WHEN a frame is built for a tree whose standing work has children, with one branch folded over a result
- THEN the children render nested beneath their parent — the parent's row before its children's, each
  child indented under it — and the folded node's row carries its scent: its child count and whether what
  is under it passed or failed, never an opaque dot

  ```check
  arc
  nested
  scent
  ```

### Requirement: a node's state reads from the glyph first, and motion is a single slow pulse
A node's state MUST be legible from its glyph before its color — the glyph names the state and color
only amplifies what the glyph already says, the color law made concrete at the place state changes most.
Distinct states MUST carry distinct leading glyphs, so stripping all color leaves every node's state read
from its glyph alone. Motion MUST be spent on exactly one thing: a single slow pulse on running work, and
stillness everywhere else.

#### Scenario: state reads from the glyph first, and only running work carries the pulse
- WHEN a frame is built carrying running, awaiting, and at-rest nodes
- THEN every node's state is legible from its leading glyph with all color stripped — distinct states
  carry distinct leading glyphs — and exactly the running nodes carry the pulse marker, no other row

  ```check
  arc
  glyph-first
  pulse
  ```

#### Scenario: the running pulse animates on the live window
- WHEN the operator watches a window over a tree with running work
- THEN a single slow pulse plays on the running work and nothing else moves
- watched — a live motion fact no headless fixture certifies, confirmed on the running window
  (`python3 -m engine`), the honest home of the interface's motion
