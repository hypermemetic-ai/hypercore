# tree
<!-- vision: tree, node, durable, version-controlled -->

The durable model: execution trees as folders on disk, read live, written atomically and
committed. A tree is a **folder** — the unit on disk is the tree, not the single node (intent
§work) — and the queue and the standing work are both views computed from the folder tree, never
lists kept in sync.

### Requirement: a tree is a folder; the unit on disk is the tree, not the node
An execution tree MUST be a folder carrying its `intent.md` (its ask or statement, and its state);
open trees live under `work/` and folded trees under `work/archive/` — the archive nested one
level down so the live work sits at the front of the tree. A tree's child trees nest the same way
in its own `work/`. The on-disk unit is the tree, never the single node.

#### Scenario: reading the tree
- WHEN the tree is read
- THEN it is the folders under `work/` (its nested `archive/` included) read recursively, each one
  tree, with its operation kind, state, owner, and whether it carries the `[machine]` marker
  recovered from its `intent.md`

### Requirement: folding moves the tree's folder into work/archive/
A tree that folds MUST move from its `work/` into that work/'s own `archive/`; location is
authoritative, so a folded tree cannot sit directly in `work/`, nor an open one under `archive/`,
and the move carries the tree's material and child trees whole.

#### Scenario: a fold
- WHEN a tree is integrated, or a machine-owned decision is settled
- THEN its folder moves `work/` → `work/archive/` and the move is committed; the result lands as
  material in the parent

### Requirement: the queue and the standing work are computed, never stored
Every view MUST be computed by reading the folders fresh — the queue is the trees awaiting the
operator (a decision to settle, or a held ask whose grilling has surfaced a question), the standing
work the ready work — so nothing can go stale and no card or question is a stored file of its
own.

#### Scenario: computing the queue and the standing work
- WHEN the queue or the standing work is shown
- THEN it is derived by reading the folders and filtering by state, not from a separately maintained
  list; a grilling pass is read from its tree's `grilling.md`, never a scatter of question files

### Requirement: a mutation lands at once and the commit follows behind
Every mutation MUST write one `intent.md` atomically (or move/remove one folder), so the act lands
on disk the instant it is made; the durable commit follows behind and does not gate the act.

#### Scenario: filing intent
- WHEN the operator's captured intent is filed
- THEN one tree folder is written by atomic replace and is present immediately, and a commit of it
  is attempted after; a failed commit does not lose the act

### Requirement: durable state is version-controlled and recoverable
Everything that crosses the operator–machine boundary MUST land on disk and be committed, so the
operator reads the state directly and any episode recovers from the record.

#### Scenario: recovering after a restart
- WHEN the system is reopened
- THEN the tree read from disk is the whole durable state; no session is resumed
