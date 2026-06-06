# frame - 002-simplify-methodology-doc

## work

Rewrite the root methodology materialization so `material/hypercore.md` is shorter,
clearer, and more visual, and remove hardening from the root methodology taxonomy.

## operator direction

The current `material/hypercore.md` is too long, wordy, and difficult to follow. The
accepted direction is:

- use more illustrations;
- use fewer words;
- make the methodology's intent easier to see;
- cut the hardening section because it should not be there.

## addressed node

Root node (`.`).

## node-local work name

`002-simplify-methodology-doc`.

## target segments

- `organizing-document`: remove `hardening` from the methodology segment list and change
  the methodology count from ten to nine.
- `structure`: its machine statements identify `material/hypercore.md` as the
  methodology prose materialization and `material/check.sh` as the mechanical check over
  every node.
- `foundations`, `collaboration`, `statements`, `endorsement`, `active-work`, `loop`,
  `sweep`, and `adapter`: their operator statements remain current, but their prose
  materialization in `material/hypercore.md` should be rewritten to present the same
  methodology more directly.
- `hardening`: remove the segment and its machine-statements file; do not retain a
  hardening section in `material/hypercore.md`.

## material changes

Adopted work should:

- replace `material/hypercore.md` with a concise overview organized around diagrams and
  short statements;
- keep the core methodology visible: purpose, intent, nodes, statements, ownership,
  endorsement, active work, loop gates, sweep, adapter, collisions, node boundaries, and
  undecided topics;
- remove `## hardening` and the hardening prose entirely;
- update `intent/organizing-document.md` so the methodology group has nine segments and
  no `hardening` bullet;
- delete `intent/hardening.md`;
- delete `intent/machine-statements/hardening.md`;
- update `material/check.sh` so the structural check expects nine methodology segments
  rather than ten;
- leave unrelated adapter, loop, work-home, and history material unchanged.

## style constraints

The new methodology prose should favor:

- compact paragraphs and bullets;
- ASCII diagrams in fenced code blocks;
- terms already used by hypercore: node, segment, statement, intent, material, work node,
  loop, sweep, adapter, endorsement, adoption, shelving;
- plain explanations that make the methodology scannable without weakening the intent.

It should avoid:

- a hardening section or replacement hardening vocabulary;
- invented child-node content;
- new domain terms that collide with hypercore's vocabulary;
- changing current intent statements except for removing the `hardening` segment from the
  root taxonomy.

## route

1. Rewrite `material/hypercore.md` as a shorter illustrated methodology document.
2. Remove `hardening` from `intent/organizing-document.md`.
3. Delete the hardening segment files.
4. Update the methodology-count assertion in `material/check.sh`.
5. Run `./material/check.sh`.
6. Sweep the changed concepts against the corpus: methodology taxonomy, segment files,
   machine-statement files, materialization, loop gates, and active work.
7. Adopt the work if checks are green and the sweep is coherent.

## proof state

The mechanical proof is `./material/check.sh`. It must pass after implementation.

The semantic proof is the sweep. The known concept map before implementation:

- `hardening` appears only in `intent/hardening.md`,
  `intent/machine-statements/hardening.md`, `intent/organizing-document.md`,
  `material/hypercore.md`, and the current check assertion that says "ten segments".
- `failure modes` also appears in `intent/collaboration.md` and
  `material/hypercore.md` as part of reliance calibration. That collaboration use is not
  hardening and should remain.
- `material/hypercore.md` is grounded by the structure machine statement saying the
  methodology prose is materialized there.
- `material/check.sh` is grounded by the structure machine statement saying it checks
  every node in the tree.

## work in flight

No other active root work node or child work node was present before this frame was
created. The only work now in flight is `material/002-simplify-methodology-doc/`.

## sweep at frame

Likely clashes found:

- Removing `hardening` clashes with the current organizing-document count of ten
  methodology segments unless the count is changed to nine.
- Removing `hardening` clashes with `material/check.sh` while it requires the phrase
  "the ten segments describing the rules themselves"; the check must be updated with the
  organizing document.
- Deleting only the prose section would leave an orphaned `hardening` intent segment, so
  the segment files must be deleted as part of the same adopted delta.

No clash was found with active sibling work. No related work is named by this frame.

## open questions

None. The operator already settled the relevant direction: shorten and clarify the
methodology materialization, add illustrations, and remove hardening.

## archive claim

Adopt this work into the root node after sign-off, implementation, green checks, and a
coherent sweep.
