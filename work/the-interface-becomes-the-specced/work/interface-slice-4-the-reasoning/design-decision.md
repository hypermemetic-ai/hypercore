# design-it-twice: Interface slice 4 — the reasoning loop. A key pressed on any visible element tied to a model's [machine]

A load-bearing interface for "Interface slice 4 — the reasoning loop. A key pressed on any visible element tied to a model's" was designed twice — candidates minimize the interface, optimize the common caller, ports-and-adapters, each fenced, each built to a different brief — and compared on depth, locality, and seam placement.

design-decision: Interface slice 4 — the reasoning loop. A key pressed on any visible element tied to a model's → minimize the interface — the ReasoningLoop value-type, hybridized to reuse the existing Thread's turns as the steerable loop's steps. Deepest on depth (one small interface hides the whole two-mode behavior), best on locality (the steerable/read-only grain lives in one field, not smeared across window modes), and the seam falls at the knowledge boundary — a loop knows its own scope-node and grain of acting. Reusing Thread answers the common-caller brief's locality win without forking a second render, so 'one surface' stays literal. Ports-and-adapters' protocol is rejected as speculative generality for a two-case distinction the system fully knows.

## Grounds

- **minimize the interface**: WON — one render + one small type; 'one surface' is literal; the distinction is one field. Deepest, best locality, seam at the knowledge boundary.
- **optimize the common caller**: rejected on locality — the steerable/read-only split smears across window modes and two render paths, weakening 'one surface'. Its Thread-reuse win is folded into the winner.
- **ports-and-adapters**: rejected on depth — a protocol + two forwarding adapters pays interface cost forever for unused flexibility; special-general mixture.
