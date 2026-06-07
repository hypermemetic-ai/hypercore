# mounting -- machine statements

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
