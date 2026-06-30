---
kind: ask
state: standing
owner: operator
created: 1782791499
---
The operator interface is rebuilt from scratch on NiceGUI — an in-process Python
web UI served fullscreen to a Chromium kiosk — and the curses window is retired.

Ratified contract (operator, 2026-06-29): The terminal is abandoned for an owned
window, and the character grid with it — the decision surface is a normal,
keyboard-first interface: proportional type, real layout, set in the window's own
warm palette in true color, never the host's. The UI runs inside the engine's own
process and calls the tree, scheduler, grilling, and transport directly; there is
no bridge, no IPC, no second runtime between the operator's window and the work. A
model's reasoning is shown as its real terminal session, not a reconstruction:
each running agent — a fenced worker, the architect — runs in a PTY the engine
owns, and the operator opens that live session to watch it as it truly runs. The
operator can work in a running agent's session directly, not just watch it —
keystrokes go to the agent, so anything you'd normally do at the terminal (ask it
something without stopping its work, redirect it, run a command) works here too.
Diagrams and illustrations are welcome wherever they help, not a grudging last
resort; glyphs are used freely, one symbol standing in for a word or several. The
interface stays fast and responsive no matter what's running — heavy work happens
in the background and never makes the window hang.

Decomposition (as-needed): Build a thin but real slice first — one live agent
session you can open, type into, and watch, in the actual look and feel — and
prove the risky parts (the terminal under load, the side channel, the theme)
early. The rest grows from there.

Folding condition: The operator runs and reads all their work from the new
interface — every move is made there, and the whole state of the system is legible
at a glance, without asking the machine. Legibility is the higher bar: if it works
but can't be read clearly, it isn't done. It fully replaces curses as the one
place the operator operates and reads the system's true state.
