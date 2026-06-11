# queue

## The interface opens fullscreen at login: the day…

> The interface opens fullscreen at login: the day starts where the decisions are. [machine]

- section: foundations
- context: the operator's words, 2026-06-11 — "we would like to launch the interface fullscreen at startup/login". An autostart entry (hyper.desktop) now opens ghostty fullscreen running hyper at login.
- approve: the autostart entry stands on endorsed intent.
- cut: the autostart entry comes out; hyper starts by hand from a shell. Nothing else breaks.

operator (2026-06-11): it did not start fullscreen. I had to hit ctrl+enter

machine (2026-06-11): the cause is upstream — ghostty ignores fullscreen=true at window creation on Linux (ghostty #11252); ctrl+enter is the toggle keybind, which works once the window is mapped. Every no-install route was tested dead: the config option, the CLI flag, the xterm escape sequence, a reload-config poke. You picked xdotool in conversation, with the entailments on screen: hyper now sends the window manager the same request your ctrl+enter makes, at launch, when the login entry starts it. It needs xdotool installed once (sudo apt-get install -y xdotool) — then the next login decides whether this statement holds.

operator (2026-06-11): didn't work. caused some error.

## The conversation is live: words spoken in the…

> The conversation is live: words spoken in the interface summon the machine on the spot, and the answer lands while the operator watches. An answer that waits for a restart is a defect. [machine]

- section: foundations
- context: the operator's words, 2026-06-11 — "I need conversations to happen in real time, not across restarts" and "I want this chat feel we have here to be part of the interface's capabilities". s and e now summon a headless machine session that answers onto the same card while the screen follows the disk; each summon spends one session's tokens; the summoned machine answers and records asks — it builds nothing.
- approve: the live channel stands on endorsed intent.
- cut: the summons come out; the machine answers only in sessions the operator starts by hand, and conversations cross restarts again. The decisions-in-flight statement loses its carrier.

## Until sent, words bind nothing: the operator sees…

> Until sent, words bind nothing: the operator sees everything they have typed and can change any of it before it crosses. [machine]

- section: foundations
- context: the operator's words, 2026-06-11 — "entering my words shouldn't bind me like it does (I can't go back to modify words while typing or even see words past the visible cutoff to my left)". the input line is now an editor: the text wraps whole, arrows move the cursor anywhere, esc abandons.
- approve: the editor stands on endorsed intent.
- cut: the words leave intent; the editor machinery stands unbacked — kept or torn out on your word. Nothing else breaks.

## Decisions surface while the work is in flight:…

> Decisions surface while the work is in flight: a call that commits the operator's resources or changes what they must later judge is settled in the queue before the material exists. Below that bar the machine scopes freely, visibly, and answers for the calls it kept. [machine]

- section: foundations
- context: the operator's words, 2026-06-11 — "important decisions being surfaced live as you work and settled by me BEFORE the work materializes. otherwise I'm captive to the machine's intent". Practiced the same day, before any build: the fullscreen route went to the operator with entailments and was settled by their pick.
- approve: the bar binds all machine work from here on.
- cut: build-then-accept returns — the machine builds on its own scope calls and the operator meets machinery only after it exists, with acceptance as the only lever.

