# Codex mounted-node entrypoint

This is root-managed hypercore adapter material for direct-path openings of external
projects mounted under the governing root.

Governing root: `/home/qqp/projects/hypercore`
Root adapter: `/home/qqp/projects/hypercore/adapter/codex.md`
Mount resolver: `/home/qqp/projects/hypercore/bin/home resolve`

When Codex opens this external target path directly, read the local target `intent/`
first. Then resolve the current direct path to its mounted node path:

```sh
/home/qqp/projects/hypercore/bin/home resolve
```

Use the resolved path when routing hypercore work back through the governing root loop:

```sh
/home/qqp/projects/hypercore/adapter/loop.sh -C <resolved-mount-path> <gate> <work-name>
```

For the full loop contract, read the root adapter at
`/home/qqp/projects/hypercore/adapter/codex.md`.

Local target checks are proof only when they exist; they do not replace root adoption or
shelving. Stop rather than fabricate missing facts, dormant child nodes, or operator
sign-off. The machine never signs off for the operator.
