surfaced: 0

[CONTRACT]
The window stops inheriting the terminal. Every frame declares its own ground — warm dark ink on off-white paper, with a soft-dark polarity the operator toggles — and a small named palette holding one alarm hue in reserve, computed without any terminal default. And the color law holds: no state the frame shows rides on color alone; every state hue shares its row with a glyph or word, so stripping color leaves every state legible. Validated against: the gated scenarios (the frame's declared ground/palette/polarity; the redundant-cue check) go red→green. Watched on the running window: the truecolor ground actually painted.

[DELTA]
# delta — interface: the window owns its ground and the color law

## ADDED — interface

### Requirement: the window owns its ground and palette
The frame MUST declare its own ground and palette as data — warm dark ink on an off-white ground by
default, a small set of named load-bearing hues, and one alarm hue held in reserve — never inheriting
the operator's terminal colors. The soft-dark polarity is the operator's to toggle: the ground flips,
the palette's meaning does not.

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
Every state a frame shows MUST be carried by a glyph or word as well as its color: color is a
redundant, pre-attentive cue — a hue names a kind, never a magnitude — never the sole carrier of a
state. The one alarm hue is spent only on the single state held in reserve for it.

#### Scenario: no state rides on color alone
- WHEN a frame is built carrying running, awaiting, and at-rest nodes
- THEN every span that carries a state hue shares its row with a glyph or word naming that same state,
  so stripping all color from the frame leaves every state still legible

  ```check
  states
  redundant
  ```
