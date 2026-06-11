# work

## the interface — first slice
- ask: a keyboard-only interface where the operator decides: the queue as home, decision cards with entailments, approve / cut / explain, every decision committed in the operator's name before the screen redraws
- state: in use, awaiting acceptance
- since: 2026-06-11
- waits on: the operator's own words, after use, with no lingering doubts

## the return path
- ask: machine answers land on the card that asked, shown as the exchange so far; the session brief stops nagging once a word is answered
- state: in use, awaiting acceptance
- since: 2026-06-11
- waits on: the operator's own words, after use

## work in flight, on disk and on screen
- ask: the machine's work state leaves its session memory for this file, and the interface shows it — what exists, what state it is in, what it waits on (w from the queue)
- state: awaiting acceptance
- since: 2026-06-11
- waits on: the operator reading the work view and accepting in their own words; the statement behind it stands [machine] in the queue

## speak from anywhere
- ask: s in any view takes the operator's words, lands them verbatim in words.md with the place attached, and commits; the machine answers onto the same block and the exchange shows on the queue
- state: in use, awaiting acceptance
- since: 2026-06-11
- waits on: the operator's own words, after use

## the interface at login
- ask: ghostty opens hyper fullscreen at login — high contrast, deliberate type, color only where it earns its place
- state: failed at first login — the operator saw "some error" and its exact words were never captured, because the flash lives only on screen. xdotool is installed now. Two suspects from the code: xdotool missing at that login (resolved by the install — the next login tests it), or the fullscreen request firing before the window manager had taken the window. Next slice, machine-scoped: write the flash to disk so an error is always quotable, and retry the request until it sticks
- since: 2026-06-11
- waits on: the operator's words on the error if remembered; one login seen fullscreen with the operator's own eyes; the statement behind it stands [machine] in the queue

## the conversation, live
- ask: speaking anywhere summons the machine on the spot — a headless session that answers onto the same card while the operator watches; the screen re-reads disk on a one-second tick, so the answer arrives with no restart anywhere; m summons by hand when words wait; the summoned machine only answers and records asks — it builds nothing; each summon spends one session's tokens
- state: awaiting acceptance
- since: 2026-06-11
- waits on: the operator speaking, watching the answer arrive, and accepting in their own words; the statement behind it stands [machine] in the queue

## words you can edit
- ask: the input line became an editor — everything typed stays visible, wrapped whole across lines; arrows move the cursor anywhere, home/end jump, backspace and delete edit in place; nothing binds until enter
- state: awaiting acceptance
- since: 2026-06-11
- waits on: the operator typing in it and accepting in their own words; the statement behind it stands [machine] in the queue

## one machine, any harness
- ask: the summon stops being an idea and becomes the interface opening a terminal session for the operator — the command it runs becomes one visible setting (claude today, codex or any harness that takes a prompt tomorrow), and the session brief becomes a file any harness reads. a cohesion cut, not a feature: nothing the shortcut does that a typed terminal couldn't
- state: picks settled (operator's words, 2026-06-11) — the summon stays and stays automatic: speaking is the summon, no extra action exists or will; the build-nothing leash is cut — summoned sessions build under the same orders as any session (decisions before material, slices with explanation and acceptance question). The cut is already landed in CLAUDE.md, the skill, and the summon instruction. What remains to build: the summon command as one visible setting, the brief as a file any harness reads
- since: 2026-06-11
- waits on: the remaining build landing; then the operator using it and accepting in their own words

## acceptance has a place
- ask: every slice awaiting acceptance surfaces as a card on the queue — what it does and how to try it, so evaluation is made easy (interface changes are their own evidence); one frictionless act on the card accepts and releases the slice; speaking is for reservations only, and those words land on the card like any speech
- state: pick settled (operator's words, 2026-06-11) — the own-words bar was a proxy for the opportunity to test, and it goes: acceptance is frictionless by default, the operator speaks only when they have reservations. The bar revision is landed in CLAUDE.md and the skill. Ready to build
- since: 2026-06-11
- waits on: the build landing; then the operator accepting slices through it

## the record never stays behind
- ask: when a machine session dies between writing and committing, the interface offers the repair instead of just the alarm — the red line names the stranded files and ends with the way out (m trues it up); m summons the machine whenever the record is behind, with first orders to verify what the strand claims, finish or correct it, and commit with grounds; the session brief flags a dirty tree to every session, typed or summoned; and summoned sessions commit after every file they finish, so a death strands less
- state: in use, awaiting acceptance — born from today's strand: a summon died on a 529 between writing and committing, the guard then blocked speech (the one recovery channel), and the operator had to leave the interface to get the record trued
- since: 2026-06-11
- try: the strand that occasioned it is already trued up — the log holds the story; if the red line ever shows again, the way out is written on it
- waits on: one act on its acceptance card

## across is horizontal
- ask: arrows doing what they look like — ←/→ across statements, ↑/↓ within the screen — and, by the operator's redirect (2026-06-11), j/k restored across statements with their effects inverted from the first slice (j to the previous statement, k to the next); space/b paging stays as it stands
- state: redirected — the slice cut j/k entirely, but the operator's criticism was the direction, not the keys; the restore is the next slice
- since: 2026-06-11
- waits on: the restore landing; then the operator moving with it and accepting in their own words; the operator's correction if the inversion recorded points the wrong way
