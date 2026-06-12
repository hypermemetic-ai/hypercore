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
  epoch. Approving removes the marker — only on the operator's explicit
  word in conversation, recorded with grounds in the git commit.
- The machine never cuts or rewords an unmarked (operator-owned)
  statement, and never removes a marker without the operator's word.
- Before relaying any cut or destructive decision, surface what it
  breaks — before the decision, not after.
- Operator judgment is never assumed; their words in conversation are the
  only warrant.

## Ratification mechanics

- Batches go to the operator through the option picker (the
  AskUserQuestion tool), never as plain prose to answer freehand: one
  question per statement, at most four to a batch, options Approve /
  Cut / Explain — two commands for when the operator knows, one for
  when they don't.
- What each answer entails lives in the option descriptions; what a
  cut breaks is spelled out before the pick, never after.
- There is no amend option (operator's word, 2026-06-10: it stalled
  twice and never ran once). The operator's words arrive through
  explain or as freehand — which is explain with words attached — and
  steer machine redrafts that stay ` [machine]` until approved. The
  operator's plain words always override the picker.
- An Explain pick means the operator can't decide yet, and carries
  their words optionally. With words, the machine answers them;
  without, it tells the story — the scenario with the rule and the
  same scenario without it, failure shown each way. Either way the
  machine's one obligation is to help the operator reach a decision;
  it may redraft its own statement along the way. The statement stays
  ` [machine]` and returns for a pick. Explain is never a decision;
  nothing changes in intent.md except the machine's own redraft of its
  own statement.
- The story is the deliverable, and it stands alone: the machine tells
  it and stops, leaving room for the operator to engage. The statement
  returns for a pick only in a later exchange, once the operator has
  had the story — never in the same breath as the telling. Redrafting
  the wording and re-presenting the picker is not an answer to Explain;
  that is the loop, not the way out of it (operator's word, 2026-06-10).

## Rebuild discipline

- Every statement carried from epoch 1 awaits re-ratification: the
  operator approves, cuts, or has it explained, one at a time, grounds
  each time.
- Nothing gets built ahead of the legibility it serves. Every slice of new
  machinery lands with a plain-words explanation and an acceptance
  question for the operator.
- Acceptance of machinery never runs through the option picker: the
  picker ratifies statements. The own-words bar was a proxy for the
  chance to test and fell on the operator's word (2026-06-11): every
  slice awaiting acceptance surfaces as a card — what it does, how to
  try it (interface changes are their own evidence) — and one
  frictionless act on the card accepts and releases it; the operator
  speaks only when they have reservations, and those words land on the
  card like any speech. Until accepted the slice stays machine-owned.
- Anti-ceremony holds: new machinery only after its absence blocks work
  twice.
- Standing work is the operator's action list (operator's word,
  2026-06-11): every work.md entry names a clear operator act in its
  state — "awaiting your decision" surfaces a decision card on the
  queue (fields: ask, options, state, since; the operator's word
  settles it — options are separated by " . ", hyper numbers them and
  1–9 picks one in the operator's name), "awaiting acceptance" an
  acceptance card (fields: ask,
  try, state). Every card files with a blocks field — what it blocks,
  what compounds while it waits (operator's word, 2026-06-11; the
  ratified order statement is the measure) — and the queue line and the
  card wear it. Work that waits on no operator act does not stand in
  work.md; git keeps the thinking until its forcing event arrives.
- Decisions before material (operator's word, 2026-06-11): a call that
  commits the operator's resources or changes what they must later judge
  is settled by the operator before the material exists — surfaced live,
  mid-work, with options and entailments (the picker serves here too;
  what it never decides is acceptance). Below the bar the machine scopes
  freely and visibly, and answers for the calls it kept. The bar has a
  written floor (ratified 2026-06-11 — operator-owned in foundations): at
  one named moment, before the first write or command that creates the
  material, five yes/no tests, any yes surfaces — it leaves the project
  folder (sends, publishes, installs, spends); it touches what the
  operator owns or uses (their words, their files, their environment);
  it binds future sessions (a default, a policy, a recurring job, a
  dependency); it takes more than one git command or one redo to take
  back; or the machine catches itself arguing that none apply — doubt
  surfaces. Judgment may surface more, never less.
- The interface summons a headless machine session when the operator
  speaks (hyper runs `claude -p`). That channel answers operator words
  onto their cards, records asks in work.md, and may build (operator's
  word, 2026-06-11) under the same orders as any session — decisions
  before material, every slice landed with its explanation and
  acceptance question. It never uses the option picker — nobody can
  see it there. It runs with full permissions (operator's word,
  2026-06-11), barred only from the irreversibly destructive — what
  git or a redo cannot bring back; in doubt, the act is the
  operator's decision.
- A session that arrives to uncommitted changes trues up the record
  before anything else: read the diff, verify what it claims against
  what is on disk, finish or correct what the dead session left, commit
  with grounds. In hyper, m summons the machine for exactly this.
- Commit after every meaningful move — and after every file finished,
  not once at the end; a session can die mid-flight, and only what is
  committed survives it. The git history is the transparency record.

## Execution graphs on disk (built 2026-06-11, on the operator's word)

- A big ask runs as an execution graph: a folder work/<name>/ holding
  graph.md. The doctrine is intent.md's work section; this is its
  machinery — there is no engine, the machine grows and folds graphs by
  editing graph.md and committing. work/ holds only current work; folded
  graphs live under history/ — the fold moves the folder there, and
  either folder exists only while it holds a graph (operator's word,
  2026-06-11).
- graph.md is a ledger of '## ' node blocks with '- key: value' fields,
  the same shape hyper reads everywhere. The first block is the root
  node: the ask that spawned the graph, born with its check (the folding
  condition) — fields ask, check, state, since. An ask whose check
  cannot be named is not ready to spawn.
- Further blocks are nodes earned only the two ways doctrine names: the
  operation crossed the operator–machine boundary, or the fold's trust
  rests on it. Fields: op (ask / check / decide / do), ask, check,
  result (when done), state, of (the parent node's head — relations live
  here). Everything else is do, absorbed into the operation it served.
- States are plain words: open, done, folded. A node waiting on an
  operator act names the act, exactly as work.md entries do — but the
  operator's cards stay in work.md; a graph never asks the operator
  anything directly.
- Folding: the result lands on the spawning node, the root state becomes
  folded, the folder moves under history/, the brief stops showing it,
  git keeps it and hyper still lists it, marked folded. When the
  root's check is an acceptance card, the card carries `- graph: <name>`
  and hyper folds the root in the acceptance commit itself — a fold can
  never lag its acceptance (built 2026-06-11 on the operator's word,
  "once is proof enough", after the first fold lagged). A session landing
  such a card writes the graph field; any other fold the machine lands by
  editing graph.md and committing. A graph that cannot meet its check
  never folds dirty — it returns as a decision card in work.md.
- hyper's work view lists every open graph beside hypercore and unfolds
  to its nodes; the session brief carries them to every summoned session.
