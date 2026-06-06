# mounting

each project the operator mounts is a distinct git repository, governed within itself.
a mounted project is a child node of this home, reached through a direct link under this
home node and carrying its own `intent/` tree -- never flattened into the home and never
copied into it.
the home holds zero mounted projects until the operator mounts the first.

## machine
a project mounts as a symbolic link under this home node -- at `home/<name>` from the root
-- pointing to a distinct repository outside the hypercore root. when the link target has
`intent/`, the link is a child-node entry point the recursive `check.sh` reaches; broken
links and links to non-nodes are dormant and do not materialize child-node content.

---
endorsed by qqp-dev
