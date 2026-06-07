# frame - 002-direct-path-greenfield-adapter

## work

Addressed node: root.

Node-local work name: `002-direct-path-greenfield-adapter`.

Target segments:

- root `home`;
- root `adapter`;
- home child node `mounting`.

Work in flight:

- `002-direct-path-greenfield-adapter` is the only active work node found in the root or
  home node after orient.

No related active or legacy work record is named by this frame.

## problem

`bin/home greenfield <name> <target-path>` creates a mounted external project node and a
link at `home/<name>`. Work started from the mount path is governed by the root Codex
adapter instruction chain. Work started from the external target's real path sees only
the target's local files. The current greenfield output therefore leaves the direct path
without a pointer to the governing root loop.

That direct-path gap lets a generated local `AGENTS.md`, or an operator-added one that
only names local checks, appear to be the governing adapter. The machine can then treat a
local check as sufficient workflow and bypass root adoption or shelving.

## constraints

The greenfield target stays flattened: `intent/` is the only reserved tree, and material
lives beside it.

The greenfield target is a distinct git repository outside the hypercore root, mounted
under `home/<name>` by symlink.

The target must not receive copies of root methodology prose, root `check.sh`, the root
`adapter/` directory, or root `bin/`.

The direct-path adapter must be a short pointer, not a copy of the root adapter. It must
name local intent, the governing root, the mount path, the root adapter, the root loop
command, and local checks only as proof when they exist.

The machine still does not sign off for the operator.

## route

Implement this as a greenfield-only change. Do not add a brownfield helper in this work;
existing external projects can be handled by later work when the operator asks for that
surface.

Parent intent amendments:

- Update root `intent/home.md` and `intent/machine-statements/home.md` so the greenfield
  command creates a short direct-path `AGENTS.md` pointer adapter in the target while
  still not copying root adapter material.
- Update `home/intent/mounting.md` and
  `home/intent/machine-statements/mounting.md` so a mounted project may carry that
  direct-path pointer adapter as part of its own target repository.
- Update root adapter intent only if needed to avoid a contradiction with the existing
  statement that nested nodes carry no adapter. The intended amendment is that root
  adapter material remains only at the methodology root, while a mounted external
  project may carry a pointer entry point that routes back to the root adapter and loop.

Material amendments:

- Update `bin/home` usage text to stop saying direct opening only sees local node shape.
- Add a helper that writes `AGENTS.md` into the target during greenfield creation.
- The generated `AGENTS.md` must include the absolute governing root path, the mount path
  `home/<name>`, the root adapter path `<root>/adapter/codex.md`, and the root loop
  command:

  ```text
  <root>/adapter/loop.sh -C home/<name> <gate> <work-name>
  ```

- The generated pointer must tell Codex to read local intent before editing and to stop
  rather than fabricate missing facts, dormant children, or operator sign-off.
- Keep rejecting path-like names, existing mount paths, non-empty targets, and targets
  inside the hypercore root.

Proof amendments:

- Update the home greenfield self-test in `check.sh` to require the target `AGENTS.md`.
- Require that the target pointer names the governing root adapter and loop command.
- Keep checks proving that `hypercore.md`, root `check.sh`, root `adapter/`, and root
  `bin/` are not copied.
- Replace the old check that greenfield does not create any `AGENTS.md` with a check that
  it does not copy the root adapter entry point and instead writes a pointer adapter.

## decision surface

The open decision from the tmp note was whether this work should also add a brownfield
helper for existing external projects. This frame settles the current work to the
greenfield command only, because the operator asked to finish fixing the greenfielding
logic. Brownfield adoption remains future work and is not a blocker for this change.

## proof state

Before sign-off, the frame is written and ready for the loop frame gate.

After sign-off, phase two must run:

```text
./check.sh
```

The work is ready to archive only when the structural check exits zero and the sweep does
not flag incoherence across root intent, home intent, the adapter material, `bin/home`,
and the active work node.

## archive

Adopt this work if the proof passes. Shelve it if the greenfield-only route proves
incoherent with the adapter or home contracts and no smaller correction can make the
written route hold.
