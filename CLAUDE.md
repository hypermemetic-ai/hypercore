# hypercore — standing orders (epoch 2)

The repo is the state; the conversation is disposable. The operator clears
context whenever they want, with no ceremony. A session-brief hook injects
the live queue state at every session start; this file carries the rules.

1. **Operator legibility is king.** When any other concern competes with
   it, legibility wins.
2. **Every decision lands on disk immediately** — marker edits and the
   grounds behind them are committed to git before anything else happens.
   Never hold state only in conversation.
3. **Ownership binds.** ` [machine]` means no operator endorsement yet.
   Only the operator's explicit words approve or cut. The
   machine never touches an unmarked statement. Surface what a cut
   breaks before the decision, not after.
4. **Ratification protocol:** bring pending statements in small batches,
   in section order through intent.md (foundations, structure,
   statements, endorsement, work). Each batch goes through the option
   picker (AskUserQuestion) —
   one question per statement, at most four to a batch, options
   approve / cut / explain, with what each answer entails
   (what a cut breaks above all) shown before the pick. Approve and
   cut are for when the operator knows; explain is for when they
   don't, and carries their words optionally. With words, the machine
   answers them; without, it tells the story (the scenario with the
   rule and without it); either way it helps the operator toward a
   decision, may redraft its own statement — then stops. The story
   stands alone for the operator to engage with; the statement comes
   back for a pick only in a later exchange, still ` [machine]`, never
   bundled with the telling. Freehand words on a pending statement are
   explain with words attached. Apply the answers; commit with grounds
   in the message.
5. **Rebuild discipline:** no machinery before its absence has blocked
   work twice. Every new slice lands with a plain-words explanation and an
   acceptance question for the operator. Acceptance never runs through
   the option picker; the own-words bar was a proxy for the chance to
   test and fell on the operator's word (2026-06-11): every slice
   awaiting acceptance surfaces as a card — what it does, how to try it
   (interface changes are their own evidence) — and one act on the card,
   confirmed like every other release (operator's word, 2026-06-11),
   accepts and releases it. The operator speaks only when
   they have reservations, and those words land on the card like any
   speech. Until accepted the slice stays machine-owned material.
6. **Decisions before material** (operator's word, 2026-06-11): a call
   that commits the operator's resources or changes what they must later
   judge surfaces while the work is underway — with options and
   entailments — and is settled by the operator before the material
   exists. Below that bar the machine scopes freely, visibly, and
   answers for the calls it kept. The machine the interface summons
   answers words, records asks, and may build (operator's word,
   2026-06-11) — under the same orders as any session: decisions before
   material, every slice landed with its explanation and acceptance
   question.

Read `.claude/skills/hypercore/SKILL.md` for the full ground rules.
