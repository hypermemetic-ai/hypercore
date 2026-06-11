# work

## the interface at login
- ask: ghostty opens hyper fullscreen at login — high contrast, deliberate type, color only where it earns its place
- state: hardened, awaiting acceptance — both repairs landed 2026-06-11: the flash writes to .hyper.log so an error is always quotable, and the fullscreen request retries each second until the window manager confirms it took (up to ten asks, every outcome logged). Both suspects from the failed login are covered: xdotool is installed, and the startup race loses to the retry
- since: 2026-06-11
- try: log out and in once — either hyper opens fullscreen, or .hyper.log holds the exact words of what failed; accept only after a login seen with your own eyes
- waits on: one act on its acceptance card, after one login; the statement behind it stands [machine] in the queue

## the conversation, live
- ask: speaking anywhere summons the machine on the spot — a headless session that answers onto the same card while the operator watches; the screen re-reads disk on a one-second tick, so the answer arrives with no restart anywhere; m summons for stragglers; the summoned machine may build under the standing orders (the build-nothing leash was cut on the operator's word, 5bf28f7); each summon spends one session's tokens
- state: awaiting acceptance
- since: 2026-06-11
- try: speak from anywhere and stay on the exchange — the answer lands while you watch, no restart
- waits on: one act on its acceptance card; the statement behind it stands [machine] in the queue

## words you can edit
- ask: the input line became an editor — everything typed stays visible, wrapped whole across lines; arrows move the cursor anywhere, home/end jump, backspace and delete edit in place; nothing binds until enter
- state: awaiting acceptance
- since: 2026-06-11
- try: press s and type past the margin — everything stays visible; move the cursor back with arrows; esc abandons, nothing binds until enter
- waits on: one act on its acceptance card; the statement behind it stands [machine] in the queue

## one machine, any harness
- ask: the summon stops being an idea and becomes the interface opening a terminal session for the operator — the command it runs becomes one visible setting (claude today, codex or any harness that takes a prompt tomorrow), and the session brief becomes a file any harness reads. a cohesion cut, not a feature: nothing the shortcut does that a typed terminal couldn't
- state: in use, awaiting acceptance — built 2026-06-11: the machine file at the root holds the one command ({prompt} stands for the summon instruction), and brief.md is written fresh at every summon for any harness to read
- since: 2026-06-11
- try: read the machine file at the root — one line names the harness; swap it for codex or anything that takes a prompt and speaking summons that instead; brief.md beside it is what any session reads first
- waits on: one act on its acceptance card

## acceptance has a place
- ask: every slice awaiting acceptance surfaces as a card on the queue — what it does and how to try it, so evaluation is made easy (interface changes are their own evidence); one frictionless act on the card accepts and releases the slice; speaking is for reservations only, and those words land on the record like any speech
- state: in use, awaiting acceptance — built 2026-06-11, on the bar the operator's words settled
- since: 2026-06-11
- try: this card is the slice showing itself — what you are reading, and the a that would release it; the entry leaves work.md and git keeps it
- waits on: one act on its own acceptance card

## the record never stays behind
- ask: when a machine session dies between writing and committing, the interface offers the repair instead of just the alarm — the red line names the stranded files and ends with the way out (m trues it up); m summons the machine whenever the record is behind, with first orders to verify what the strand claims, finish or correct it, and commit with grounds; the session brief flags a dirty tree to every session, typed or summoned; and summoned sessions commit after every file they finish, so a death strands less
- state: in use, awaiting acceptance — born from today's strand: a summon died on a 529 between writing and committing, the guard then blocked speech (the one recovery channel), and the operator had to leave the interface to get the record trued
- since: 2026-06-11
- try: the strand that occasioned it is already trued up — the log holds the story; if the red line ever shows again, the way out is written on it
- waits on: one act on its acceptance card

## across is horizontal
- ask: arrows doing what they look like — ←/→ across statements, ↑/↓ within the screen — and, by the operator's redirect (2026-06-11), j/k restored across statements with their effects inverted from the first slice (j to the previous statement, k to the next); space/b paging stays as it stands
- state: in use, awaiting acceptance — the restore landed 2026-06-11: j/k move across decision and acceptance cards, j previous and k next, arrows alongside
- since: 2026-06-11
- try: on any card, j and k — j to the previous, k to the next; if the inversion points the wrong way, say so and it lands the other way
- waits on: one act on its acceptance card; the operator's correction if the inversion points the wrong way

