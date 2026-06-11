# queue

## The interface opens fullscreen at login: the day…

> The interface opens fullscreen at login: the day starts where the decisions are. [machine]

- section: foundations
- context: the operator's words, 2026-06-11 — "we would like to launch the interface fullscreen at startup/login". An autostart entry (hyper.desktop) now opens ghostty fullscreen running hyper at login.
- approve: the autostart entry stands on endorsed intent.
- cut: the autostart entry comes out; hyper starts by hand from a shell. Nothing else breaks.

## The interface is high contrast and set in…

> The interface is high contrast and set in deliberate type, with color spent only where it earns its place. [machine]

- section: foundations
- context: the operator's words, 2026-06-11 — "old school classy high contrast view, with well selected typography and sparse color use if any". The interface is now warm white on black, set in IBM Plex Mono, with one color left: red, meaning the record is behind.
- approve: the restyle and the launcher typography stand on endorsed intent.
- cut: no statement constrains the interface's look; the styling stays machine taste until something replaces it.

## Work in flight is readable from the interface:…

> Work in flight is readable from the interface: what exists, what state each piece is in, and what it waits on. Setting priorities takes nothing the interface does not show. [machine]

- section: foundations
- context: the operator's words, 2026-06-11 — "how am I supposed to know what needs to be prioritized if I can't see what work exists and what state it is in?" Until today the machine carried work state in its own session memory, against the sworn foundation that the graph, not the running conversation, is the durable shared state. work.md and the work view exist because of this statement.
- approve: the work ledger and the work view stand on endorsed intent; the machine maintains work.md, the operator only reads it.
- cut: work.md and the work view lose the statement behind them and come out; knowing what is in flight goes back to asking the machine, and setting priorities leaves the interface.
