# words

## spoken items in the queue should…

operator (2026-06-13): spoken items in the queue should somehow fall under the relevant thread. we have some big changes in the pipeline involving these threads so this should fall under that. point is, if a queue item becomes just a tracker for a conversation, the conversation should go under threads where appropriate. queue items should disappear when operator takes action.

machine (2026-06-13): Agreed, and half holds today: a decision or slice disappears the instant you act — settle and accept both clear the card in the same commit (the snap-fix and the plan-readout shrink vanished from the queue when you accepted them). The visible exception is a card you've decided but the machine hasn't executed yet: the working-indicator has sat "decided" on the queue since you picked option 2 — that lingering is the smell. The rest — a tracker's conversation living under its thread, not on the card — is structural, part of the threads changes you're steering, so I won't front-run the design. Your calls: execute the working-indicator now so it clears, and/or fold "a decided-but-unexecuted card lives as a thread" into the threads work. I'll record whichever.

operator (2026-06-13): is this coming up as a card? if it isn't we have a problem.

machine (2026-06-13): Yes — as a thread, not a queue card. Your own pick (2026-06-13): exchanges are a first-class panel below the queue, never interleaved. Every words.md block you speak shows there — "sent" while it waits on the machine, "read" once answered. This exchange is in that panel now, answered. If it is not showing below the queue for you, that is a real bug — say so and I'll chase it. Whether spoken items should also be queue cards is the threads design just above.

operator (2026-06-13): no, you wrote "your calls, execute the etc. and/or etc." I'll record whatever. that's what I meant should come up as a card.

machine (2026-06-13): Caught — and the ground rules already say it (2026-06-13): a decision goes to the queue as a card, never into a thread; a thread may point at a card but not hold the call. My "your calls… I'll record whichever" broke that. Holding to it now. Concretely: the working-indicator is already a decided card on the queue (option 2), so it was never a loose prose choice — it stands there as that card, awaiting its build.

## from the decision card, on ""it asks" reuses ASK as a verb — which congruent voice for the field labels" . 2026-06-13

operator (2026-06-13): two issues. one, I'm approving three but the card isn't disappearing. two, what does a for approve even do for these? if I need to pick an option or talk there's nothing for approve to do.

machine (2026-06-13): One — right, it's a lag: a pick flips the card to "decided" but it clears only when a machine executes the word, and none was mid-run, so option 3 sat decided until this session executed it (2832c9c) — decision cards now read "to decide" and the card has cleared. That lag is the smell from your queue-under-threads word; closing it lives in that design. Two — exactly: a settles the card with the literal word "approve", which isn't one of your options, so on an options decision a (and c) are dead keys; only pick (1–9) and speak do anything. That touches "one verb set on every card", which is yours, so I filed the fix as a decision (drop a/c from decision cards / keep them only for a bare yes-no call / leave it).

operator (2026-06-13): "to decide" looks bad atm. too long, touches the start of the block to its right. we need to rethink these labels for all cards generally. let's do that here in one go.

machine (2026-06-13): Right — labels sit in a 7-wide gutter with the body at column 9, so "to decide" (9) touches the text. Per your own rule I put it on the queue as a decision rather than settle it here — and you've already picked option 2 (cap labels at 7). Executing it: the decision card's first field becomes "decide". Every other card label already fits in 7, so that is the only one that moves.

## what happened to the sts2 work

operator (2026-06-13): what happened to the sts2 work? doesn't appear under w, appears to have been dropped?

machine (2026-06-13): Not dropped — removed, and recoverable. On your word that outside work shouldn't live under hypercore, a session removed the STS2 overlay card from work.md (52f0652); that is why it is gone from w. Nothing is lost: the card and your settled config-tuning decision stand in git (602a33c, 2c8484b, the full card in 52f0652's parent). What did not happen is the move — the STS2 project was never stood up (no folder, not in registry.md), so the work has no home now; that is the dropped feeling. To restore it: stand up an STS2 project (folder + registry entry) and the work moves there, or re-card it in hypercore if you want it here. Your call — say the word and I set it up; I won't author your project's intent unprompted.

operator (2026-06-13): let's stand up the project so we can track the work and pick up where we left off.

