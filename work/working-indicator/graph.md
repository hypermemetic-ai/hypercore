# graph: working-indicator

## the per-thread working indicator

- ask: from the operator's words (2026-06-13, thread "new idea, which I like…", settled option 2 — open it as a full graph and work the whole arc in order). The organizing idea: threads are the open thinking/working channel, the queue is for decisions. The arc, worked in order: (1) a per-thread working indicator + fold-protection; (2) thread↔work linking — a graph root records the thread that spawned it, and the two read across to each other; (3) the session-owns-thread model; (4) softening the action-oriented language. Each slice lands and is accepted before the next.
- check: threads carry the worked indicator and a worked thread is fold-protected; a graph root records the thread it was spawned from; a session owns its thread for its run; and the action-oriented language has softened — each slice accepted by the operator, so the thread stands as the open working channel the queue is not.
- state: open
- since: 2026-06-13
- of: hypercore

## the working indicator + fold-protection

- op: do
- ask: the first slice of the arc — a per-thread "working" indicator (a thread reads as worked when a session is running and its last word is yours) plus fold-protection so a thread being worked can't be folded away and lose that fact.
- check: the operator accepts the card "the working indicator + fold-protection" — a sent thread's label reads "working" while a session is on it and falls back to "sent" with no session, and c on a worked thread refuses the fold with a word instead of closing it. How to try it: speak to a thread, watch its label turn "working" while the machine runs; open it and press c — it holds until the answer lands.
- result: accepted by the operator from the card (2254d2b, 2026-06-13). draw_entry overrides the "sent" label to "working" (accent) when a machine runs; the exchange-view c blocks the fold for a thread whose last word is the operator's while a machine runs. The global top-right "the machine is working" indicator is left standing — retiring it is a later slice, once the per-thread one is lived with. Next on the arc: thread↔work linking (a graph root records the thread that spawned it).
- state: done
- of: the per-thread working indicator
