# interface
<!-- vision: interface, window, screen, keyboard -->

The window: the operator's whole world. Keyboard-only, fullscreen, high-contrast
— a thin paint-and-input layer over the graph and the architect that holds
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
- WHEN a frame is built for a given graph and selection
- THEN the render returns a list of rows of (text, style) spans, computed without
  any terminal call

### Requirement: the resting face shows the queue over the work
At rest the window MUST show the queue of decisions above the standing work; a
fully-handled system shows an empty surface, which is the system at rest,
not a fault.

#### Scenario: nothing awaits
- WHEN no node is awaiting the operator and no work is standing
- THEN the queue reads "nothing awaiting you" and work reads "no standing work"

### Requirement: the operator opens the self-model from the window
The operator MUST be able to open the operator view from the window and return,
all by keyboard.

#### Scenario: opening and leaving the view
- WHEN the operator presses the view key from the resting face
- THEN the operator view opens in the window; pressing escape returns to the face
