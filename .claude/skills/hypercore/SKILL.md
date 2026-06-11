---
name: hypercore
description: Ground rules for the hypercore repository in epoch 2 — intent lives in intent.md at the root, everything else burned on the operator's reset. Operator legibility rules; ownership markers and operator-only decisions still bind. Use whenever working in this repository.
---

# hypercore, epoch 2

On 2026-06-10 the operator reset the project: the engine, viewer, database,
snapshots, and all work graphs were deleted. Git history holds the first
epoch. There is no engine and no derived views — one root intent
document, intent.md (sections: foundations, structure, statements,
endorsement, work), IS the system, edited directly, every change
committed to git with plain-words messages. The merge from five files
into one was the operator's call, on their own sworn words: a work
graph's intent document is singular, and this repo is hypercore's folder.

## The three ruling statements (operator-owned, head of foundations)

1. Operator legibility is king; when any concern competes with it, it wins.
2. Work on the system, above all other work, is transparent.
3. Inherited debt burns recurrently: tear down and rebuild until the
   operator accepts with no lingering doubts.

## Ownership still binds

- A statement ending ` [machine]` holds no operator endorsement in this
  epoch. Endorsing removes the marker — only on the operator's explicit
  word in conversation, recorded with grounds in the git commit.
- The machine never strikes or amends an unmarked (operator-owned)
  statement, and never removes a marker without the operator's word.
- Before relaying any strike or destructive decision, surface what it
  breaks — before the decision, not after.
- Operator judgment is never assumed; their words in conversation are the
  only warrant.

## Ratification mechanics

- Batches go to the operator through the option picker (the
  AskUserQuestion tool), never as plain prose to answer freehand: one
  question per statement, at most four to a batch, options Endorse /
  Amend / Strike / Explain.
- What each answer entails lives in the option descriptions; what a
  strike breaks is spelled out before the pick, never after.
- An Amend pick still needs the operator's wording: take it from the
  pick's note, or ask as a follow-up. The operator's plain words always
  override the picker.
- An Explain pick means the statement isn't understood yet. The machine
  answers with the story — the scenario with the rule and the same
  scenario without it, failure shown each way — and a redrafted
  formulation that moves the story's value into the wording. The
  statement stays ` [machine]` and returns for a pick. Explain is never
  a decision; nothing changes in intent.md except, after the story, the
  machine's own redraft of its own statement.
- The story is the deliverable, and it stands alone: the machine tells
  it and stops, leaving room for the operator to engage. The statement
  returns for a pick only in a later exchange, once the operator has
  had the story — never in the same breath as the telling. Redrafting
  the wording and re-presenting the picker is not an answer to Explain;
  that is the loop, not the way out of it (operator's word, 2026-06-10).

## Rebuild discipline

- Every statement carried from epoch 1 awaits re-ratification: the
  operator endorses, amends, or strikes, one at a time, grounds each time.
- Nothing gets built ahead of the legibility it serves. Every slice of new
  machinery lands with a plain-words explanation and an acceptance
  question for the operator.
- Anti-ceremony holds: new machinery only after its absence blocks work
  twice.
- Commit after every meaningful move; the git history is the transparency
  record.
