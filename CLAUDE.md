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
   Only the operator's explicit words endorse, amend, or strike. The
   machine never touches an unmarked statement. Surface what a strike
   breaks before the decision, not after.
4. **Ratification protocol:** bring pending statements in small batches,
   in section order through intent.md (foundations, structure,
   statements, endorsement, work). Each batch goes through the option
   picker (AskUserQuestion) —
   one question per statement, at most four to a batch, options
   endorse / amend / strike / explain, with what each answer entails
   (what a strike breaks above all) shown before the pick. Explain means
   the statement isn't understood yet: the machine answers with the
   story (the scenario with the rule and without it) and a redrafted
   formulation that carries that value, and the statement comes back for
   a pick, still ` [machine]`. Apply the answers; commit with grounds in
   the message.
5. **Rebuild discipline:** no machinery before its absence has blocked
   work twice. Every new slice lands with a plain-words explanation and an
   acceptance question for the operator.

Read `.claude/skills/hypercore/SKILL.md` for the full ground rules.
