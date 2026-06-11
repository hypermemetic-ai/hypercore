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

machine (2026-06-11): the error's exact words died with the screen — the flash is never written to disk, a legibility failure in its own right. What the record shows: xdotool is installed now, and the code can only flash two errors. Either that login ran before the install (then the flash said "xdotool is not installed" and the next login is the real test), or the request fired before the window manager had taken the window — a startup race the machine can harden with a retry. Both repairs are recorded in work.md: the flash lands on disk so an error is always quotable, and the request retries until it sticks. If you remember the error's words, speak them — they pick between the suspects at once.

