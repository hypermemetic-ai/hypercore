# frame - 001-home-greenfield-setup

## work

Rename the durable root child from `work-home` to `home`, and replace the current
submodule mount contract with a link mount contract. Add the first greenfield setup
operation as an operator- and machine-runnable CLI: it creates a new external project
repository, gives it only its own local node shape, and mounts it into hypercore through a
link under `home` so work through that mount path inherits the root methodology.

## operator direction

The operator settled these points before the frame:

- the durable child should be named `home`, not `work-home`;
- mounted projects do not need submodule semantics;
- mounted projects should not practically live under `home`;
- `home` should hold a link to the real project so it behaves as if it were under `home`;
- the important inheritance path is the hypercore methodology changing in one place, not
  being duplicated into each project;
- greenfield setup comes first; brownfield setup is later work.

## addressed node

Root node (`.`).

## node-local work name

`001-home-greenfield-setup`.

## target segments

- `organizing-document`: rename the governed-work segment from `work-home` to `home` and
  describe linked mounted projects rather than mounted submodules.
- `work-home` -> `home`: rename the root child contract segment and its machine statement
  file, update the durable child path to `material/home/`, and state the link-based mount
  contract.
- `active-work`: update the statement that root-directed active work is a sibling to the
  durable home child, not under it.
- `structure`: keep the general child-node shape, but settle that a mounted project may
  be reached through a link under `home` rather than being inlined in the root repository.
- `adapter`: update live adapter prose examples that still name `work-home`; no gate order
  or sign-off behavior changes are intended.
- `loop`: update material only if needed so `loop.sh -C material/home/material/<name>` can
  address a linked mounted node by its mount path.
- child node `material/work-home/` -> `material/home/`, segment `mounting`: update the
  home node's own organizing document, mounting statements, machine statements, and README
  from submodule storage to link mounting.

## material changes

Adopted work should:

- move `material/work-home/` to `material/home/`;
- move `intent/work-home.md` to `intent/home.md`;
- move `intent/machine-statements/work-home.md` to `intent/machine-statements/home.md`;
- update live root prose, intent, machine statements, README material, and adapter prose
  so `work-home` is not a live current name;
- update the home child node so its mount point remains its material tree, with mounted
  projects represented by links at `material/home/material/<name>`;
- remove the current submodule requirement from live intent and material;
- add a root material CLI at `material/bin/home` with at least:
  - `material/bin/home greenfield <name> <target-path>`;
  - validation that `<name>` is a mount name, not a path;
  - validation that `<target-path>` is outside the hypercore root or at least not inside
    `material/home/`;
  - creation of `<target-path>` as a distinct Git repository when it does not exist;
  - creation of `<target-path>/intent/organizing-document.md` and
    `<target-path>/material/` as the new project node's local shape;
  - no copy of root `material/hypercore.md`, root `material/check.sh`, root
    `material/adapter/`, or root `AGENTS.md` into the target project;
  - creation of a symbolic link at `material/home/material/<name>` pointing to the target;
  - refusal to overwrite an existing mount path or non-empty target;
  - a help path that explains that inherited methodology is available when the machine or
    operator works through the mount path.
- update `material/check.sh` so it treats linked mounted nodes as nodes when the link
  target has both `intent/` and `material/`;
- update `material/check.sh` to prove the greenfield CLI exists and is executable, and to
  run a temporary greenfield self-test or equivalent non-destructive proof;
- leave adopted history unchanged except for normal archive movement of this work node.

The CLI may add narrowly-scoped implementation helpers if needed, but it should not add a
new package manager, language runtime dependency, or network dependency. A shell script is
sufficient for this first operation.

## inheritance model

The project target is a distinct repository outside the hypercore repository. The mount is
the hypercore-facing entry point:

```text
external project repository
  /somewhere/project/
    intent/
      organizing-document.md
    material/

hypercore repository
  material/home/material/project -> /somewhere/project
```

When Codex or another harness works from the mount path
`material/home/material/project`, the root adapter remains in the project instruction
chain, so the project inherits the current methodology and loop from hypercore. The setup
does not duplicate the methodology into the project; changes to hypercore's methodology
are reflected because the governing adapter remains the root one.

Directly opening the external target path is outside this inheritance guarantee for this
work. If direct-path inheritance becomes required, that is separate work because it needs a
different adapter-loading contract.

## route

1. Rename the root governed-work segment and durable child from `work-home` to `home`.
2. Rewrite the root home contract from submodule storage to link mounting.
3. Rewrite the home child node's organizing document, `mounting` segment, machine
   statements, and README around link mounts.
4. Add `material/bin/home greenfield <name> <target-path>`.
5. Make the check script follow or explicitly inspect link-mounted nodes under
   `material/home/material/` without treating arbitrary broken links as materialized
   child nodes.
6. Add mechanical proof that the CLI can create a temporary external project node and
   mount link without touching live operator projects.
7. Update live examples and documentation references from `work-home` to `home`.
8. Run `./material/check.sh`.
9. Sweep the changed concepts across current intent, machine statements, material, the
   new CLI, and this work node.
10. Adopt if checks are green and the sweep is coherent.

## proof state

Baseline before implementation:

- `./material/check.sh` was green before this work node was started.
- The corpus has no active work nodes other than this frame.
- `material/work-home/` exists and holds zero mounted projects.
- There is no `.gitmodules` file in the root.
- A local shell probe showed that `find` does not traverse internal directory symlinks by
  default, while `find -L` does; the implementation must account for that explicitly.
- A local shell probe showed that Bash `pwd` preserves the logical symlink path by
  default, so `loop.sh -C material/home/material/<name>` can preserve the mount path if
  the orchestrator does not force physical-path resolution.

Required proof after implementation:

- `./material/check.sh` exits zero.
- Live current files no longer name `work-home` except in adopted history or this adopted
  work record.
- Live current files no longer require mounted projects to be Git submodules.
- `material/home/` is a child node with its own `intent/` and `material/`.
- `material/bin/home` exists, is executable, and its greenfield path is mechanically
  tested in temporary space.
- A linked mounted project with `intent/` and `material/` is reached by `material/check.sh`
  as a child node.
- No project-specific methodology prose, root check script, adapter directory, or root
  `AGENTS.md` is copied into the greenfield target.

## work in flight

No other active root work node or child work node was present before this frame was
created. The only work now in flight is `material/001-home-greenfield-setup/`.

No related work is named by this frame. Brownfield setup is intentionally not related work
for this node; it remains future work after greenfield setup is adopted.

## frame sweep

Map:

- `intent/organizing-document.md`, `intent/work-home.md`,
  `intent/machine-statements/work-home.md`, `intent/active-work.md`,
  `README.md`, `material/adapter/codex.md`, and the home child node currently carry the
  `work-home` name.
- The home child's `mounting` segment and README currently require a Git submodule under
  `material/work-home/material/<name>`.
- The root `structure` machine statement currently says a child node is inlined at
  `material/<name>/` unless a machine statement settles it as an external reference.
- `material/check.sh` currently discovers child nodes with `find "$root" -type d -name
  intent`, which does not traverse link-mounted project directories.
- `material/adapter/loop.sh` can address child nodes with `-C <node-path>`, but the
  implementation should confirm it preserves logical mount paths when the child is a
  symlink.

Read:

- Renaming only the directory would leave live root intent still binding `work-home`; the
  root segment and machine statement file must be renamed with it.
- Replacing submodules with links conflicts with the current home mounting machine
  statement until that statement is rewritten.
- Link-mounted child nodes conflict with the current recursive check implementation until
  the check follows or explicitly reads the link mount surface.
- The structure statement already allows a machine statement to settle an external
  reference, so a link mount does not require a new kind of child.
- The active-work rule still holds: root-directed active work stays directly under root
  `material/` as a sibling to `home`, not inside `home`.
- No sibling active work or mounted project conflicts with this route.

Sweep verdict for frame: coherent if adoption renames the live contract to `home`, rewrites
mounting from submodule storage to link mounting, proves linked nodes mechanically, and
keeps greenfield limited to creating an external project node plus a mount link.

## open questions

None for greenfield setup. Brownfield setup remains deliberately unframed.

## archive claim

Adopt this work into the root node after sign-off, implementation, green checks, and a
coherent sweep. Shelve it if link-mounted projects cannot inherit the methodology through
the `home` mount path without duplicating the root methodology or breaking recursive
checks.
