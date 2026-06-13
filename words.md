# words

## I want better thread labels. short, clear. also…

operator (2026-06-13): I want better thread labels. short, clear. also the notification sound isn't loud enough.

machine (2026-06-13): Built both — two acceptance cards now on the queue, both tried by relaunching hyper. Labels: thread_label() now keeps the first sentence when it reads as a phrase, caps tighter (40 chars), cuts on a clause/word boundary, and strips trailing punctuation — so "I want better thread labels. short, clear. also…" becomes "I want better thread labels". Honest limit: a heuristic shortens and cleans but can't summarize, so an opening like "share your findings about the claude usage endpoint…" tightens to "share your findings about the claude…", not a crisp "Claude usage endpoint." Cue: play_cue() now amplifies ~200% (paplay --volume), the cue stream only — never your system volume; I couldn't re-master the sound file (no ffmpeg/sox here) and raising the system sink was off-limits, so stream-volume is the lever, and the value bumps if it's still short. One decision is yours: do you want truly crisp topic labels — which means the machine relabels a thread to a short summary when it answers it (the first-words label shows only while it waits; you can already rename by hand) — or is the tighter heuristic enough? Say the word and I'll build the relabel or leave it.

operator (2026-06-13): good as is, manual rename is fine for now

operator (2026-06-13): changed my mind.. I do want auto thread rename but only if the operator does not manually rename.

## new idea, which I like…

operator (2026-06-13): new idea, which I like: some kind of "working on it" indicator for open threads. some looping animation maybe, unsure. this ends up touching on some complicated stuff. like, if the working indicator is associated with a thread, closing the thread would lose me information. maybe we keep threads open visually (cannot close?) while work is being done on them? if we do that, maybe we can walk back some of the action oriented language. I wouldn't mind getting a good response to chew on, clearing any doubts as to what the machine is thinking and planning while routing decisions to the queue so I think of the two interaction modes separately. this appears to make the "the machine is working" on the top right redundant. it would just be a global indicator, largely redundant if I can see all the open threads. if we pursue this, it might be nice to link threads to the work associated with them (w view), both ways via a keypress? think this out yourself, it's a change with big implications, exciting but nor something we should rush.

## work view is hard to navigate…

operator (2026-06-13): work view is hard to navigate, mostly due to the size of the node text blocks. if they all started collapsed it would be much easier to navigate at the cost of an extra keypress. another idea might be using empty space if available to display the text block there instead of under the node/graph label.

