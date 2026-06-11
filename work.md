# work

## the interface at login
- ask: ghostty opens hyper fullscreen at login — high contrast, deliberate type, color only where it earns its place
- state: hardened, awaiting acceptance — both repairs landed 2026-06-11: the flash writes to .hyper.log so an error is always quotable, and the fullscreen request retries each second until the window manager confirms it took (up to ten asks, every outcome logged). Both suspects from the failed login are covered: xdotool is installed, and the startup race loses to the retry
- since: 2026-06-11
- try: log out and in once — either hyper opens fullscreen, or .hyper.log holds the exact words of what failed; accept only after a login seen with your own eyes
- waits on: one act on its acceptance card, after one login; the statement behind it stands [machine] in the queue

## across is horizontal
- ask: arrows doing what they look like — ←/→ across statements, ↑/↓ within the screen — and, by the operator's redirect (2026-06-11), j/k restored across statements with their effects inverted from the first slice (j to the previous statement, k to the next); space/b paging stays as it stands
- state: in use, awaiting acceptance — the restore landed 2026-06-11: j/k move across decision and acceptance cards, j previous and k next, arrows alongside
- since: 2026-06-11
- try: on any card, j and k — j to the previous, k to the next; if the inversion points the wrong way, say so and it lands the other way
- waits on: one act on its acceptance card; the operator's correction if the inversion points the wrong way

