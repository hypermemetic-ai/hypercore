# frame - 001-flatten-material-tree

## work

Collapse the node layout so `intent/` is the only reserved tree. Everything currently
under a node's `material/` tree becomes node-local corpus beside `intent/`: leaf files,
durable child nodes, active work nodes, adapter materialization, checks, CLIs, and mount
entries.

## operator direction

The operator gave two settled directions before this frame:

- teach greenfield work the new methodology by installing a home skill first;
- collapse the `intent/` / `material/` folder distinction by placing `material/` contents
  at the same level as `intent/`, leaving no current `material/` folder.

The skill has already been installed outside this repository at
`$HOME/.codex/skills/hypercore-greenfield/`; this work adopts the repository methodology
and materialized tooling to match that flattened greenfield rule.

## addressed node

Root node (`.`).

## node-local work name

`001-flatten-material-tree`.

## target segments

- `organizing-document`: describe the methodology as materialized by root-level
  `hypercore.md`, `check.sh`, `adapter/`, and node-local corpus beside `intent/`; update
  the governed `home` child path.
- `structure`: replace the two-tree statement with the flattened node shape: `intent/`
  is reserved, and the rest of the node-local corpus is material.
- `active-work`: move new active work nodes from `material/<NNN-slug>/` to
  `<NNN-slug>/`, with frames still under `<NNN-slug>/intent/frame/`.
- `loop`: update gate wording and machine statements for addressed work paths, check
  command, and child addressing under the flattened shape.
- `adapter`: move root adapter materialization from `material/adapter/` to `adapter/`,
  update `AGENTS.md`, `signoff`, and all harness prose.
- `home`: move the durable home child from `material/home/` to `home/`, and move mounted
  project links from `material/home/material/<name>` to `home/<name>`.
- home child segment `mounting`: update the home node's own intent and README so project
  mounts are direct entries under `home/`, and linked projects are nodes when their target
  has `intent/`.

No change is intended for the operator-level meanings of `foundations`, `collaboration`,
`statements`, `endorsement`, or `sweep`, except where their prose materialization in
`hypercore.md` needs path examples updated.

## problem, constraints, and decision surface

Problem: the current corpus asserts and checks a two-tree layout. The requested new
methodology keeps `intent/` as the written contract but removes `material/` as a required
container, so all current path-bearing statements, checks, adapter entry points, child
paths, work paths, and home mount paths must change together.

Constraints:

- The current loop is still authoritative until this work is adopted.
- This work node was therefore scaffolded under the current path:
  `material/001-flatten-material-tree/`.
- The current `execute` process reads gate files from `material/adapter/gates/` and calls
  `./material/check.sh` while phase two is running.
- If implementation simply moves `material/adapter/` and `material/check.sh` away, the
  old in-flight orchestrator cannot reach check, sweep, archive, or the final archive
  move.
- The final adopted corpus should have no tracked live `material/` paths.
- Empty directories are not retained by git, so an empty transient `material/` directory
  after archive movement does not count as current corpus.

Decision surface:

- A pure single-step move is not executable by the old orchestrator because it removes the
  files the old process still needs.
- Leaving permanent compatibility wrappers under `material/` would keep the old layout
  alive and contradict the operator's direction.
- The chosen route is a self-hosting transition: phase two creates the new flat paths and
  new flat loop, leaves only the old-loop compatibility needed for the running process,
  and removes that compatibility before the old orchestrator performs its final archive
  move. The only remaining old-layout path at that moment may be the active work node
  itself, which the old orchestrator then moves into history.

No operator decision remains open for this route. The bootstrap shim is mechanical
execution support, not a methodology exception to retain after adoption.

## proposed parent amendments

Adopted intent should state:

- a node has one reserved tree, `intent/`;
- node-local material is the corpus outside `intent/`, including leaf material, durable
  child nodes, active work nodes, adapter materialization, checks, CLIs, and settled
  external references;
- a child node is a directory or settled linked entry point with `intent/`;
- a child node does not need a `material/` directory;
- new active work nodes live directly under the addressed node as `<NNN-slug>/`;
- a work node frame lives under `<NNN-slug>/intent/frame/`;
- root methodology prose is `hypercore.md`;
- the root structural check is `check.sh`;
- root adapter materialization is `adapter/codex.md`, `adapter/loop.sh`, and
  `adapter/gates/`;
- `AGENTS.md` points to `adapter/codex.md`;
- `./signoff` dispatches to `./adapter/loop.sh signoff "$@"`;
- home is the durable child node at `home/`;
- home's mount surface is `home/<name>`, with linked targets treated as child nodes when
  they have `intent/`;
- `bin/home greenfield <name> <target-path>` creates a flattened external node with
  `intent/` and no `material/` tree.

The term "material" may remain as the methodology's name for checked corpus, but it is no
longer the name of a required directory.

## material changes

Adopted work should move or rewrite the live tracked corpus as follows:

- `material/hypercore.md` -> `hypercore.md`;
- `material/check.sh` -> `check.sh`;
- `material/adapter/` -> `adapter/`;
- `material/bin/` -> `bin/`;
- `material/home/` -> `home/`;
- `material/home/material/README.md` -> `home/README.md`;
- `AGENTS.md` symlink target from `material/adapter/codex.md` to `adapter/codex.md`;
- `signoff` command from `./material/adapter/loop.sh signoff "$@"` to
  `./adapter/loop.sh signoff "$@"`;
- `material/home/material/<name>` mount examples to `home/<name>`;
- `material/bin/home` command examples to `bin/home`;
- `./material/check.sh` examples to `./check.sh`;
- `material/adapter/loop.sh` examples to `adapter/loop.sh`.

The new `adapter/loop.sh` should:

- use `INTENT_TREE=intent`;
- create new work nodes at `$NODE/$work_name`, not `$NODE/material/$work_name`;
- create frame directories at `$NODE/$work_name/intent/frame`;
- resolve `-C <node-path>` by requiring `$node_path/intent`, not
  `$node_path/intent` plus `$node_path/material`;
- run `./check.sh`;
- print flattened path examples in `start`, `frame`, `signoff`, `execute`, and `status`
  output;
- continue to support legacy signed frames under `intent/changes/<NNN-slug>/` if those
  paths are present;
- continue to archive addressed node-local work under `intent/history/adopted/` or
  `intent/history/shelved/`.

The new `check.sh` should:

- run from the root regardless of invocation path;
- discover current nodes by `intent/` presence, excluding `.git/`, `.agents/`, `.codex/`,
  `.claude/`, and `intent/history/` records from current-node recursion;
- check the root and every current child node, including linked home mounts whose targets
  have `intent/`;
- no longer require a node-level `material/` directory;
- still require each current segment to have a machine-statements file, `## machine`, and
  foot endorsement;
- still check adopted and shelved history collections under `intent/history/`;
- allow old archived work records to remain readable even when they were created before
  the flattening;
- prove that no tracked live path remains under `material/` after adoption, except for the
  current transition work node before the old orchestrator archives it;
- prove `hypercore.md`, `check.sh`, `adapter/codex.md`, `adapter/loop.sh`,
  `adapter/gates/*`, `bin/home`, `home/intent/`, and `home/README.md` exist;
- prove `AGENTS.md` routes Codex to the flat paths;
- prove `./signoff` dispatches to the flat loop;
- update the home greenfield self-test so a temporary external target receives `intent/`
  and no `material/`, mounts at `home/<name>`, and is discoverable as a child node.

The home CLI at `bin/home` should:

- keep `greenfield <name> <target-path>`;
- reject path-like names;
- reject existing mount paths;
- reject non-empty targets;
- reject targets inside the hypercore root;
- create the target as a git repository when needed;
- create `target/intent/organizing-document.md`;
- not create `target/material/`;
- not copy root `hypercore.md`, root `check.sh`, root `adapter/`, root `bin/`, or root
  `AGENTS.md`;
- create a symlink at `home/<name>` pointing to the target;
- explain the flat mount path in help text.

The current work node may delete its empty `material/` child during implementation so the
adopted history record for this migration is also flattened. If the old orchestrator needs
the work-node path itself until archive, leave `material/001-flatten-material-tree/` in
place until the orchestrator moves it.

## self-hosting transition requirement

Because this migration removes the paths used by the old running loop, phase two must
implement a temporary compatibility path with these properties:

- before moving tracked live paths, create the new flat paths and update the new flat
  `adapter/loop.sh`;
- keep enough old-path gate material available for the current `execute` process to run
  the check and archive gates;
- keep `material/check.sh` available as a compatibility command while the current old
  `execute` process still calls it;
- make the compatibility `material/check.sh` delegate to the new `./check.sh`;
- ensure that before the old orchestrator's final archive move, old-path compatibility is
  removed, leaving only the current active work node under `material/` if the old
  orchestrator still needs to move it;
- do not leave tracked compatibility wrappers under `material/` in the final adopted
  corpus.

One acceptable implementation is:

1. During implement, move tracked material to flat paths and leave temporary compatibility
   copies or wrappers under `material/adapter/gates/` and `material/check.sh`.
2. Have `material/check.sh` run `./check.sh`, and only after the archive gate has created
   an explicit final-cleanup marker, remove the old compatibility paths before delegating
   to `./check.sh`.
3. Have the archive gate create that marker immediately before it returns
   `ARCHIVE_DECISION: ADOPTED`, after parent intent has been folded.
4. Let the old orchestrator run its final `check_green`; the compatibility wrapper removes
   old compatibility and then `./check.sh` proves the flat corpus with only the active
   old-loop work node tolerated.
5. Let the old orchestrator move `material/001-flatten-material-tree/` to adopted history.

Equivalent implementations are acceptable if they satisfy the same end state and keep the
old running loop alive until it records history.

## route

1. Move root materialized files and directories to flat paths with `git mv` where tracked:
   `hypercore.md`, `check.sh`, `adapter/`, `bin/`, and `home/`.
2. Move home mount documentation from `home/material/README.md` to `home/README.md` and
   retire the nested `home/material/` mount surface.
3. Rewrite root methodology prose and README examples for the flattened node layout.
4. Rewrite `intent/structure.md` and `intent/machine-statements/structure.md` around
   `intent/` as the only reserved tree.
5. Rewrite `intent/active-work.md` and its machine statements so new work nodes are direct
   children of the addressed node.
6. Rewrite `intent/loop.md`, `intent/machine-statements/loop.md`, gate prompts, and
   `adapter/loop.sh` for flat work paths and `./check.sh`.
7. Rewrite `intent/adapter.md`, `intent/machine-statements/adapter.md`, `AGENTS.md`, and
   `signoff` for `adapter/`.
8. Rewrite `intent/home.md`, `intent/machine-statements/home.md`, and the home child
   `mounting` segment for `home/<name>` mounts and flattened greenfield targets.
9. Rewrite `bin/home` for flat target creation and flat mount paths.
10. Rewrite `check.sh` for flattened node discovery, history checks, adapter checks, and
    greenfield self-test.
11. Implement the self-hosting transition compatibility required for this old-loop run.
12. Run `./check.sh` and, while the old loop is still executing, allow
    `./material/check.sh` compatibility only as needed by that process.
13. Search the live tracked corpus for `material/` path references. Remaining current
    references must be either old-history descriptions, compatibility comments explaining
    this migration, or rejected by the sweep.
14. Sweep flattened node shape, child-node detection, home mounts, active work, adapter
    paths, and check commands across current intent, machine statements, materialized
    prose, scripts, and work in flight.
15. Adopt if checks are green and the sweep is coherent.

## proof state

Baseline before implementation:

- `./material/check.sh` exited zero after this work node was scaffolded.
- No active work node existed before this frame was created.
- The only active work node now in flight is
  `material/001-flatten-material-tree/`.
- `git ls-files | rg '(^|/)material(/|$)'` currently reports only live tracked paths
  under `material/`: adapter files, home files, `bin/home`, `check.sh`, and
  `hypercore.md`.
- Existing adopted work history has no tracked `material/` files, only empty untracked
  old-layout directories in the working tree.

Required proof after implementation:

- `./check.sh` exits zero.
- The old-loop compatibility command `./material/check.sh` exits zero during this
  transition only, then removes old-path compatibility before the old orchestrator's final
  archive move.
- `git ls-files | rg '(^|/)material(/|$)'` returns no tracked path after adoption.
- `find . -path './material' -o -path './*/material'` finds no current live material
  directory after archive, aside from old archived records if intentionally retained as
  readable history.
- `AGENTS.md` points to `adapter/codex.md`.
- `./signoff` dispatches to `./adapter/loop.sh`.
- `adapter/loop.sh start 002-example --help` is not required, but normal loop usage text
  and gate prompts name flat paths.
- New work started after adoption would be scaffolded as `002-example/intent/frame/`, not
  `material/002-example/intent/frame/`.
- `home/` is a child node with `home/intent/`.
- `home/<name>` symlink mounts are discoverable as child nodes when their targets have
  `intent/`.
- `bin/home greenfield <name> <target-path>` creates a flattened external node with
  `intent/` and no `material/`.
- Live current prose and scripts no longer tell operators or machines to use
  `material/hypercore.md`, `material/check.sh`, `material/adapter/`, `material/home/`, or
  `material/home/material/<name>`.

## work in flight

No active root work node or child work node was present before this frame was created.
The only active work now in flight is `material/001-flatten-material-tree/`.

No related work node is named by this frame. The migration is broad but atomic because
the current path contracts, adapter paths, check paths, child detection, and home mount
paths must agree for the corpus to remain coherent.

## frame sweep

Map:

- `intent/structure.md`, `intent/machine-statements/structure.md`, `hypercore.md`, and
  `README.md` define the current two-tree node shape and the current `material/` paths.
- `intent/active-work.md`, `intent/machine-statements/active-work.md`,
  `intent/loop.md`, `intent/machine-statements/loop.md`, `adapter/gates/*`, and
  `adapter/loop.sh` define where work nodes are created and how frames are found.
- `intent/adapter.md`, `intent/machine-statements/adapter.md`, `AGENTS.md`, `signoff`,
  and adapter prose define the harness entry points and loop path.
- `intent/home.md`, `intent/machine-statements/home.md`, `home/intent/*`, `home/README.md`,
  `bin/home`, and `check.sh` define home mounting and greenfield creation.
- `check.sh` is the mechanical proof for path shape, node discovery, history collections,
  adapter wording, and home greenfield behavior.
- The current running old loop is itself a path-bearing dependency during this migration.

Read:

- Moving only files without changing statements leaves the parent intent false.
- Changing statements without moving files leaves checks and adapter materialization false.
- Removing `material/check.sh` and `material/adapter/gates/` too early breaks the current
  old-loop `execute` process before it can check, sweep, archive, and record history.
- Keeping permanent compatibility wrappers under `material/` contradicts the operator's
  direction and the new structure statements.
- Home mounts must move with the home contract; otherwise `check.sh`, `bin/home`, and the
  home child intent will disagree on where linked projects live.
- Existing old adopted work history may remain readable, but it must not define the
  current node shape.
- No sibling work proposes a conflicting path shape.

Sweep verdict for frame: coherent if adoption changes the statements, scripts, adapter
paths, home paths, checks, and materialized prose together, and if any old-path
compatibility exists only long enough for this old-loop execution to complete.

## open questions

None.

## archive claim

Adopt this work into the root node after operator sign-off, implementation, green checks,
and a coherent sweep. Shelve it if the flattened layout cannot be adopted without either
leaving a live `material/` compatibility surface or breaking the loop before it can record
the work in history.
