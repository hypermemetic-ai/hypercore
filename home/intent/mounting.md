# mounting

each project the operator mounts is a distinct git repository, governed within itself.
a mounted project is a child node of this home, reached through a direct link under this
home node and carrying its own `intent/` tree -- never flattened into the home and never
copied into it.
a mounted external project may carry root-managed direct-path entrypoint links in its
target repository: `AGENTS.md` links to the root-managed mounted Codex entrypoint, and
`signoff` links to the root-managed home sign-off helper.
those links route direct-path work back to the governing root adapter and loop without
copying root process material into the mounted target.
the home currently mounts `codex-cockpit`.

## machine
a project mounts as a symbolic link under this home node -- at `home/<name>` from the root
-- pointing to a distinct repository outside the hypercore root. when the link target has
`intent/`, the link is a child-node entry point the recursive `check.sh` reaches; broken
links and links to non-nodes are dormant and do not materialize child-node content.
the target repository may carry an `AGENTS.md` link to
`<root>/adapter/codex-mounted.md` and a `signoff` link to `<root>/bin/home-signoff`; the
links are target entrypoints to root-managed process material, not target-owned process
copies.
the root-managed mounted entrypoints resolve the target's current path to its mounted node
path before routing direct-path work to the governing root adapter and loop.

---
endorsed by qqp-dev
