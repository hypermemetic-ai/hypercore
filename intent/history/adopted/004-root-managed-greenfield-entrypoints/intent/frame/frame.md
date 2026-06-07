# frame - 004-root-managed-greenfield-entrypoints

## work

Replace generated direct-path greenfield process files with root-managed entry points.

## operator direction

The operator settled the main direction before this frame: direct-path support should be
root-managed. Linked project targets should not own local copies of reusable hypercore
process material that can go stale.

## addressed node

Root node (`.`).

## node-local work name

`004-root-managed-greenfield-entrypoints`.

## target segments

- root `home`;
- root `adapter`;
- root `loop` only if helper or status wording needs a loop statement;
- home child node `mounting`;
- root checks and home CLI material.

## work in flight

This work node is the only active root work node found after orient. No active work node
was found in `home/` or in the current `home/codex-cockpit` mounted node.

Current live material is already dirty from prior adopted work and generated
`codex-cockpit` setup. This frame builds on the live files as current material and does
not revert unrelated dirty changes.

Related adopted records:

- `001-home-greenfield-setup` created the linked home greenfield model and deliberately
  left direct-path inheritance out of scope.
- `002-direct-path-greenfield-adapter` added generated target-local `AGENTS.md` and
  `signoff` files to close that gap.
- `003-phase-two-observability` altered loop state and status surfaces but does not set
  the greenfield entrypoint ownership model.

## problem

The current greenfield command creates regular files in each target repository:

- `AGENTS.md`, a short Codex pointer adapter generated from root data;
- `signoff`, a generated helper that dispatches to the root loop for that mount path.

That fixes direct-path openings, but it makes every linked target own a process snapshot.
If root adapter language, loop dispatch, sign-off mechanics, or mount resolution changes,
old targets can retain stale generated workflow. The root check now reinforces this by
requiring those files to be local regular files rather than links to root-managed material.

The live `home/codex-cockpit` mount already demonstrates the risk: its direct-path
`AGENTS.md` and `signoff` are target-local generated files, and the home intent also has a
small current-state drift because the home organizing document and README say
`codex-cockpit` is mounted while `home/intent/mounting.md` still says home holds zero
mounted projects.

A separate drift is visible in the current mount: root and home intent say mounted projects
are distinct git repositories, but `/home/qqp/projects/codex-cockpit` is not currently a
git repository. This work may repair that live mount to match the existing contract; it
must not weaken the repository contract unless phase two proves repair is impossible.

## constraints

The target project remains a distinct external node mounted under `home/<name>` by a
symbolic link.

The flattened layout remains: `intent/` is the only reserved tree and target material
lives beside it.

The target must not receive copies of root `hypercore.md`, root `check.sh`, root
`adapter/`, root `bin/`, or the root `AGENTS.md` entry point.

Direct-path support must still work when Codex opens the external target path rather than
the mount path.

The root-managed direct-path adapter cannot bake in one mount name. It must resolve the
current target path to the corresponding mounted node path before routing work to the root
loop.

The machine still does not sign off for the operator.

## route

Parent intent amendments:

- Update root `intent/home.md` and `intent/machine-statements/home.md` so
  `bin/home greenfield <name> <target-path>` creates the target's local node shape and
  root-managed direct-path entry points, not generated process copies.
- Update root `intent/adapter.md` and `intent/machine-statements/adapter.md` so a mounted
  external project may expose a target-local entry point that links to root-managed
  adapter material. The entry point routes direct-path openings back to the governing root
  adapter and loop; it is not copied adapter material and not target-owned process prose.
- Update `home/intent/mounting.md` and
  `home/intent/machine-statements/mounting.md` so mounted targets may carry root-managed
  direct-path entrypoint links, and so the current `codex-cockpit` mount is not
  contradicted by a stale "zero mounted projects" statement.
- Update home documentation material to describe root-managed direct-path entrypoints
  rather than generated pointer files.

Material amendments:

- Add a root-managed direct-path Codex entrypoint, expected as
  `adapter/codex-mounted.md`, whose job is to:
  - say it is root-managed material for external mounted project direct-path openings;
  - name the governing root;
  - tell Codex to read the local target `intent/` first;
  - tell Codex to resolve the current direct path to a mount path with
    `bin/home resolve`;
  - route adoption or shelving work to `adapter/loop.sh -C <resolved-mount-path>`;
  - tell Codex to read the root adapter at `adapter/codex.md` for the full loop contract;
  - keep local target checks as proof only when they exist;
  - stop rather than fabricate missing facts, dormant child nodes, or operator sign-off.
- Add or extend root-managed home helpers:
  - `bin/home resolve [<path>]` prints the mounted node path such as
    `home/codex-cockpit` for a direct target path or a path inside that target.
  - `bin/home resolve` without a path resolves the current working directory.
  - resolution scans `home/*` symlinks, compares physical target roots, requires the
    matched target to carry `intent/`, and fails clearly when the path is not under a
    mounted node.
  - a root-managed `signoff` entry helper, expected as `bin/home-signoff`, resolves the
    caller's target path and dispatches to
    `adapter/loop.sh -C <resolved-mount-path> signoff "$@"`.
- Update `bin/home greenfield` so new targets receive:
  - `intent/organizing-document.md`;
  - `AGENTS.md` as a symlink to the root-managed mounted Codex entrypoint;
  - `signoff` as a symlink to the root-managed mounted sign-off helper;
  - a symlink at `home/<name>` pointing to the target.
- Keep the greenfield refusal rules: reject path-like names, existing mount paths,
  non-empty targets, and targets inside the hypercore root.
- Repair the current `home/codex-cockpit` mounted target to the same root-managed
  entrypoint shape by replacing its generated `AGENTS.md` and `signoff` with symlinks to
  the root-managed files.
- If `/home/qqp/projects/codex-cockpit` is still not a git repository when phase two
  implements this frame, initialize it as a git repository to satisfy the current home
  contract. If the phase-two harness cannot write to the external target, stop and report
  the permission blocker rather than weakening the contract.

Proof amendments:

- Update `check.sh` so the home greenfield self-test proves generated targets use
  root-managed symlink entrypoints:
  - `AGENTS.md` points at the root-managed mounted Codex entrypoint;
  - `signoff` points at the root-managed mounted sign-off helper;
  - neither file is a regular generated process copy.
- Add proof that `bin/home resolve "$target"` returns `home/<name>` for the greenfield
  self-test target, and that resolving a path inside the target returns the same mount
  path.
- Add proof that mounted targets with `intent/` do not carry generated regular
  direct-path `AGENTS.md` or `signoff` files when those entrypoints exist; they must point
  at the root-managed files.
- Add proof that each live `home/*` mounted node with `intent/` has a git repository if
  the current "distinct git repository" contract remains live.
- Keep the negative proof that greenfield does not copy root `hypercore.md`, root
  `check.sh`, root `adapter/`, root `bin/`, or root `AGENTS.md`.
- Run `./check.sh`.

## proof state

Baseline observations before sign-off:

- `./check.sh` exits zero against the current generated-file model.
- `check.sh` currently requires greenfield target `AGENTS.md` and `signoff` to be local
  non-symlink files.
- `home/codex-cockpit/AGENTS.md` and `home/codex-cockpit/signoff` are generated regular
  files, not root-managed symlinks.
- `home/intent/organizing-document.md` and `home/README.md` say home currently mounts
  `codex-cockpit`; `home/intent/mounting.md` still says home holds zero mounted projects.
- `home/codex-cockpit` points to `/home/qqp/projects/codex-cockpit`.
- `git -C /home/qqp/projects/codex-cockpit rev-parse --is-inside-work-tree` currently
  fails.

Required proof after implementation:

- `./check.sh` exits zero.
- New greenfield targets get root-managed symlink entrypoints rather than generated
  process files.
- `bin/home resolve` maps both a target root and a path inside it to the mounted node path.
- The current `home/codex-cockpit` target uses root-managed direct-path entrypoint links.
- The home mounting current-state statements agree about the live `codex-cockpit` mount.
- The current mounted `codex-cockpit` target satisfies the live git repository contract,
  or phase two stops with a blocker if external-target permissions prevent repair.
- No root methodology prose, root check script, root adapter directory, root bin directory,
  or root `AGENTS.md` entry point is copied into a greenfield target.

## frame sweep

Map:

- Root `home` intent and machine statements currently say greenfield writes a short
  direct-path `AGENTS.md` pointer adapter and target-local `signoff` helper.
- Root `adapter` intent and machine statements currently allow a target-local pointer
  entry point for direct-path openings.
- Home `mounting` intent currently allows target-local pointer/helper files and still
  says home has zero mounted projects.
- `bin/home` currently generates regular direct-path files with absolute root and mount
  path text.
- `check.sh` currently proves those generated files are regular local files.
- The current `home/codex-cockpit` target has generated regular entrypoint files.
- Adopted history `002-direct-path-greenfield-adapter` records why direct-path support was
  added; this work changes ownership of that support, not the need for it.

Read:

- Root-managed symlink entrypoints preserve direct-path support while keeping reusable
  process material in the governing root.
- A generic root-managed direct-path adapter needs a resolver because the same file must
  work for every mounted target.
- The root adapter statement "adapter material is materialized only at the methodology
  root" becomes clearer, not weaker, when mounted targets link to root-managed material
  instead of carrying generated prose.
- Requiring generated files to be regular local files is now the main check drift; the
  proof must invert to require root-managed symlinks.
- The `codex-cockpit` mount must be brought along or explicitly left as debt. This frame
  brings it along so live material demonstrates the current contract.
- The git repository mismatch is not caused by direct-path entrypoint ownership, but it is
  live drift against the home contract. Repairing it in the same implementation is
  smaller than weakening the contract.

Sweep verdict for frame: coherent if adoption makes direct-path entrypoints
root-managed, proves mount-path resolution mechanically, repairs the current
`codex-cockpit` entrypoints, and leaves no current home statement contradicting the live
mount.

## open questions

None. The operator selected the root-managed route. This frame treats the current
`codex-cockpit` mount as live material to repair rather than as unrelated brownfield debt.

## archive claim

Adopt this work into the root node after sign-off, implementation, green checks, and a
coherent sweep. Shelve it if direct-path openings cannot be routed through root-managed
entrypoints without copying root process material into mounted targets.
