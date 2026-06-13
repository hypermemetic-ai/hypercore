# work

## the working indicator + fold-protection

- ask: built the first slice of the working-indicator arc (your settled option 2). A thread now reads as "working" — not "sent" — while a session is running and its last word is yours: the label turns accent in the THREADS panel, so you can see at a glance which thread the machine is on; with no session on it, it falls back to "sent". And fold-protection: a thread being worked refuses to fold away (c flashes a word instead of closing it), so a thread in flight can't be lost. The global top-right "the machine is working · clock" is left standing for now — once you've lived with the per-thread indicator, retiring it can be its own slice.
- try: relaunch hyper (a running hyper reads its own code only at launch), press s on a thread (or open one and speak into it) — its line in THREADS reads "working" while the machine runs, and drops back to "sent" once the session ends; open that thread and press c while it's worked — it won't fold until the answer has landed.
- state: awaiting acceptance
- blocks: nothing compounds — reversible in one revert; the rest of the arc (thread↔work linking, the session-owns-thread model, softening the language) waits in the working-indicator graph until you've lived with this.

## two-column work view — list left, panel right

- ask: built the layout you confirmed (option 1). Unfolding hypercore — or a linked project, or a graph — now shows a compact entry list on the left (about a third of the width) and the selected entry's full content in a panel on the right, divided by a rule. j/k moves the selection and the panel follows it; there is no inline expand any more — the detail is always there for whatever is selected. enter still drops into a graph (its own two columns replace the panel); space/b scrolls the panel, top-anchored, when an entry runs long.
- try: relaunch hyper (a running hyper reads its own code only at launch), press w, then enter on hypercore. The titles sit left, the detail panel right — move j/k and watch the panel track the selection; space/b scrolls a long entry like the trak-backend graph (enter on it to drop into its nodes, same two columns).
- state: awaiting acceptance
- blocks: nothing compounds — the change is on disk and reverts in one git command; until you accept, it stays machine-owned material and the old single-column list is one revert away.

