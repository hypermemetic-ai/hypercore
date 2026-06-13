# graph: working-indicator

## the per-thread working indicator

- ask: from the operator's words (2026-06-13, thread "new idea, which I like…", settled option 2 — open it as a full graph and work the whole arc in order). The organizing idea: threads are the open thinking/working channel, the queue is for decisions. The arc, worked in order: (1) a per-thread working indicator + fold-protection; (2) thread↔work linking — a graph root records the thread that spawned it, and the two read across to each other; (3) the session-owns-thread model; (4) softening the action-oriented language. Each slice lands and is accepted before the next.
- check: threads carry the worked indicator and a worked thread is fold-protected; a graph root records the thread it was spawned from; a session owns its thread for its run; and the action-oriented language has softened — each slice accepted by the operator, so the thread stands as the open working channel the queue is not.
- state: open
- since: 2026-06-13
- of: hypercore
- thread: new idea, which I like…

## the working indicator + fold-protection

- op: do
- ask: the first slice of the arc — a per-thread "working" indicator (a thread reads as worked when a session is running and its last word is yours) plus fold-protection so a thread being worked can't be folded away and lose that fact.
- check: the operator accepts the card "the working indicator + fold-protection" — a sent thread's label reads "working" while a session is on it and falls back to "sent" with no session, and c on a worked thread refuses the fold with a word instead of closing it. How to try it: speak to a thread, watch its label turn "working" while the machine runs; open it and press c — it holds until the answer lands.
- result: accepted by the operator from the card (2254d2b, 2026-06-13). draw_entry overrides the "sent" label to "working" (accent) when a machine runs; the exchange-view c blocks the fold for a thread whose last word is the operator's while a machine runs. The global top-right "the machine is working" indicator is left standing — retiring it is a later slice, once the per-thread one is lived with. Next on the arc: thread↔work linking (a graph root records the thread that spawned it).
- state: done
- of: the per-thread working indicator

## the thread↔work link

- op: do
- ask: the second slice of the arc — a graph root records the thread that spawned it, and the thread and that work read across to each other. A root born from a thread carries a thread: field (the thread's heading); the work view shows it on the root, and a live thread whose heading a root recorded names the work it became on its own view.
- check: the operator accepts the card "the thread↔work link" — the working-indicator graph's panel names the thread it was spawned from, and a thread that became a graph shows that graph back, so a thread and its work point at each other. How to try it: relaunch hyper, w, enter on hypercore, select the working-indicator graph line — its panel carries a THREAD row naming the thread it came from. The back-link shows on a thread's own exchange view whenever that thread's heading matches a graph root's record (today's threads have folded past their graphs, so it lights the next time a thread you speak becomes a graph).
- result: built this session — the interface reads the link both ways (48abf8c): the work-view root panel shows the root's thread field, the exchange view names the work a thread spawned, matched by the recorded heading across hypercore's graphs. This root now records its own spawning thread ("new idea, which I like…"). The match is best-effort by heading, named in SKILL.md (145efe2); a later rename loosens the back-link, the forward record stays true. Awaiting the operator's acceptance.
- state: awaiting acceptance
- of: the per-thread working indicator
