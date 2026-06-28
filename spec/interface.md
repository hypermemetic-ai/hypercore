# interface
<!-- vision: interface, window, screen, keyboard -->

The window: the operator's whole world. Keyboard-only, fullscreen, high-contrast
— a thin paint-and-input layer over the tree and the architect that holds
nothing that isn't about the screen or the keyboard.

### Requirement: the interface is the only place the operator operates
Every move the system asks of the operator MUST be makeable at the keyboard,
inside the window. The operator never leaves it to act, and reads the system's
state there without asking the machine.

#### Scenario: the operator acts
- WHEN the operator approves, cuts, explains, speaks, or opens a view
- THEN each is a keystroke in the window, with no command run outside it

### Requirement: the input loop never blocks on durable work
The window's keystroke loop MUST service and echo every keystroke without waiting
on any git-bound or IO-bound work. Heavy work runs off the input loop.

#### Scenario: a heavy pass is in flight
- WHEN the architect is being summoned (a slow, off-loop call)
- THEN keystrokes are still serviced each frame and a thinking indicator shows,
  because the heavy pass runs on another thread and the loop polls its result

### Requirement: the operator can speak from anywhere
The operator MUST be able to start speaking from any place in the interface; the
place they spoke from travels with them and nothing more is asked.

#### Scenario: speaking while browsing the queue
- WHEN the operator is browsing cards and types a printable character
- THEN the window leaves browse, opens a thread, and the character begins the buffer

### Requirement: the window renders as pure frames
The screen MUST be produced by pure render functions that return styled spans, so
every frame is testable without a TTY; only the window maps spans to terminal
attributes.

#### Scenario: rendering off a TTY
- WHEN a frame is built for a given tree and selection
- THEN the render returns a list of rows of (text, style) spans, computed without
  any terminal call

  ```check
  card
  render
  spans
  ```

### Requirement: the window owns its ground and palette
The frame MUST declare its own ground and palette as data: warm dark ink on an off-white ground by
default, a small set of named load-bearing hues, and one alarm hue held in reserve. It MUST NOT inherit
the operator's terminal colors. The soft-dark polarity is the operator's to toggle: the ground flips,
and the palette's meaning does not.

#### Scenario: the frame carries its own ground
- WHEN a frame is built for a tree and a selection
- THEN it exposes a declared ground (ink and paper) and a named palette, computed without reading any
  terminal default; toggling the polarity returns the dark-ground variant with the same palette

  ```check
  render
  ground
  palette
  polarity
  ```

### Requirement: color names a kind, never the only carrier
Every state a frame shows MUST be carried by a glyph or word as well as its color. Color is a redundant,
pre-attentive cue: a hue names a kind; glyphs or words carry state identity, and layout carries
magnitude. The one alarm hue is spent only on the single state held in reserve for it.

#### Scenario: no state rides on color alone
- WHEN a frame is built carrying running, awaiting, and at-rest nodes
- THEN every span that carries a state hue shares its row with a glyph or word naming that same state,
  so stripping all color from the frame leaves every state still legible

  ```check
  states
  redundant
  ```

### Requirement: the resting face shows the queue over the work
At rest the window MUST show the queue of decisions above the standing work; a
fully-handled system shows an empty surface, which is the system at rest,
not a fault.

#### Scenario: nothing awaits
- WHEN no node is awaiting the operator and no work is standing
- THEN the queue reads "nothing awaiting you" and work reads "no standing work"

  ```check
  render
  empty
  ```

### Requirement: the operator opens the self-model from the window
The operator MUST be able to open the operator view from the window and return,
all by keyboard.

#### Scenario: opening and leaving the view
- WHEN the operator presses the view key from the resting face
- THEN the operator view opens in the window; pressing escape returns to the face

### Requirement: a non-live window shows it is not the dispatching loop
A window that does not hold the autonomous-loop lease MUST signal in its footer that it is not the
live loop, so the operator can tell at a glance which window dispatches. It remains a full operator
window — every keystroke move still works and the work it files is built by the live loop — so the
signal serves the operator's mental model, not a restriction.

#### Scenario: the footer marks the non-live window
- WHEN a window is open over a tree whose lease another window holds
- THEN its footer shows it is not the live loop, while the lease-holding window's footer does not

  ```check
  loops 2
  render holder footer-live
  render peer footer-not-live
  ```

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

### Requirement: the decision card lays out its full anatomy, decidable at a glance
The opened decision card MUST lay out its full anatomy on the grid — the synthesis, the options and what
each entails, the cost of its delay, and the machine's lean with the one flip. Every heading MUST state
its finding outright, never a bare label the operator must open to learn what it says. What is needed to
decide MUST be on the face; the confirming detail behind a line MUST sit one keystroke below it — held
off the face, advertised by its affordance, and surfaced only when summoned — so the card is decidable
at a glance.

#### Scenario: the opened decision card lays out its anatomy, every heading a synthesis
- WHEN a decision card carrying its full anatomy is opened on the resting face
- THEN its detail lays out the synthesis, the options and what each entails, the cost of its delay, and the
  machine's lean with the one flip, every heading stating its finding outright rather than naming a label to
  open

  ```check
  decide-card
  laid-out
  synthesis
  ```

#### Scenario: what is needed to decide is on the face, the confirming detail one keystroke below
- WHEN a decision card is opened on the resting face
- THEN what is needed to decide is on the face, and the confirming detail behind its lines is held off the
  face one keystroke below — advertised by its affordance and surfaced only when summoned

  ```check
  decide-card
  face
  confirm-below
  ```
