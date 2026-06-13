# words

## I don't like "it asks" for decisions

operator (2026-06-13): I don't like "it asks" for decisions. we use ASK for work, is there a reason we're not consistent? does this apply anywhere else? look for incongruities of this kind and make them congruent. this leads to very real legibility wins.

machine (2026-06-13): No reason — drift, not a choice. "it asks"/"it does" were written to read on a card before ASK settled as our work-word, and "it asks" reuses ASK (the first of ask/check/decide/do) as a verb. It applies in two more spots of the same kind: the same first field is labeled three ways — ASK (work view), "it asks" (decision), "it does" (acceptance) — and the commit head "the operator asks explain" reuses "asks" for "requests". The rest is cosmetic case/phrasing drift, not a collision. The fix is wording, which is yours — so I filed it as a decision in work.md (which voice: ASK everywhere / "the call" on decisions / smallest fix). It returns through the queue.

## under w I don't like what the list…

operator (2026-06-13): under w I don't like what the list looks like with a single bold line. we need to add something to make it look better. main w view looks good because of the small non-bold check blocks. some visual variety like that might be what we want, but think creatively aiming for a double win: looks better + provides useful information without expanding.

machine (2026-06-13): I see it — a column of bold-only lines is flat, and the folded-graph rows read better because the dim "check:" gives each a quieter second texture. The double win that mirrors it: under each entry's bold title, one dim line of its substance — its check if it has one, else the first line of its ask — so the list gains the bold-over-dim variety and each row says what it's about, no block opened. The taste call that's yours is which gist earns that line. I'll build a take (check/ask gist) and land it for acceptance so you can see it; redirect the gist if it's not the useful one.

## from the decision card, on ""it asks" reuses ASK as a verb — which congruent voice for the field labels" . 2026-06-13

operator (2026-06-13): no, you're confused. ask does not mean work. the ask is the ask - it's intent, operator input guiding the work.

machine (2026-06-13): You're right — I had it backwards. The ask is yours: intent, your input guiding the work, not "work". That narrows it cleanly: "the operator asks explain" is correct (you're the asker) and "it does" is fine (the machine does do the work). The one wrong note is "it asks" on a decision card — it casts the machine as the asker when the ask is yours; the machine only surfaces the decision. Reframed the decision card to that: the fix is just the label, the pick is which word names what it brings (the call / the decision / to decide).

## spoken items in the queue should…

operator (2026-06-13): spoken items in the queue should somehow fall under the relevant thread. we have some big changes in the pipeline involving these threads so this should fall under that. point is, if a queue item becomes just a tracker for a conversation, the conversation should go under threads where appropriate. queue items should disappear when operator takes action.

machine (2026-06-13): Agreed, and half holds today: a decision or slice disappears the instant you act — settle and accept both clear the card in the same commit (the snap-fix and the plan-readout shrink vanished from the queue when you accepted them). The visible exception is a card you've decided but the machine hasn't executed yet: the working-indicator has sat "decided" on the queue since you picked option 2 — that lingering is the smell. The rest — a tracker's conversation living under its thread, not on the card — is structural, part of the threads changes you're steering, so I won't front-run the design. Your calls: execute the working-indicator now so it clears, and/or fold "a decided-but-unexecuted card lives as a thread" into the threads work. I'll record whichever.

