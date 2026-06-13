# words

## I want better thread labels. short, clear. also…

operator (2026-06-13): I want better thread labels. short, clear. also the notification sound isn't loud enough.

machine (2026-06-13): Built both — two acceptance cards now on the queue, both tried by relaunching hyper. Labels: thread_label() now keeps the first sentence when it reads as a phrase, caps tighter (40 chars), cuts on a clause/word boundary, and strips trailing punctuation — so "I want better thread labels. short, clear. also…" becomes "I want better thread labels". Honest limit: a heuristic shortens and cleans but can't summarize, so an opening like "share your findings about the claude usage endpoint…" tightens to "share your findings about the claude…", not a crisp "Claude usage endpoint." Cue: play_cue() now amplifies ~200% (paplay --volume), the cue stream only — never your system volume; I couldn't re-master the sound file (no ffmpeg/sox here) and raising the system sink was off-limits, so stream-volume is the lever, and the value bumps if it's still short. One decision is yours: do you want truly crisp topic labels — which means the machine relabels a thread to a short summary when it answers it (the first-words label shows only while it waits; you can already rename by hand) — or is the tighter heuristic enough? Say the word and I'll build the relabel or leave it.

operator (2026-06-13): good as is, manual rename is fine for now

operator (2026-06-13): changed my mind.. I do want auto thread rename but only if the operator does not manually rename.

machine (2026-06-13): Built — acceptance card on the queue, and recorded in the standing orders (SKILL.md) so every session does it. How it works: when the machine answers a thread still wearing its raw first-words heading, it rewrites the heading to a short, true topic — the real summary the heuristic can't produce. Your hand always wins: renaming a thread (r) moves its heading off the first-words default, and the machine never overwrites a heading that isn't that default, whoever set it. So "auto rename, but only if you haven't renamed" falls out with no flag to track — a hand-named thread simply isn't a default-named one. The label is set once (while still default), not churned on every later answer. One restraint I kept: I didn't rename the threads already open this session, because a running hyper keys an open thread by its heading and renaming one you're reading would snap your view to home — so it takes effect on threads answered from here on. If you'd rather it keep refining a label as a thread grows instead of setting it once, say the word.

operator (2026-06-13): interesting idea, yes. cost would be low anyway.

## new idea, which I like…

operator (2026-06-13): new idea, which I like: some kind of "working on it" indicator for open threads. some looping animation maybe, unsure. this ends up touching on some complicated stuff. like, if the working indicator is associated with a thread, closing the thread would lose me information. maybe we keep threads open visually (cannot close?) while work is being done on them? if we do that, maybe we can walk back some of the action oriented language. I wouldn't mind getting a good response to chew on, clearing any doubts as to what the machine is thinking and planning while routing decisions to the queue so I think of the two interaction modes separately. this appears to make the "the machine is working" on the top right redundant. it would just be a global indicator, largely redundant if I can see all the open threads. if we pursue this, it might be nice to link threads to the work associated with them (w view), both ways via a keypress? think this out yourself, it's a change with big implications, exciting but nor something we should rush.

