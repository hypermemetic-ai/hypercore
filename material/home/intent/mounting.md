# mounting

each project the operator mounts is a distinct git repository, governed within itself.
a mounted project is a child node of this home, reached through a link under this home's
`material/` tree and carrying its own `intent/` and `material/` trees together -- never
flattened into the home and never copied into it.
the home holds zero mounted projects until the operator mounts the first.

## machine
a project mounts as a symbolic link under this home node's `material/` -- at
`material/home/material/<name>` from the root -- pointing to a distinct repository outside
the hypercore root. when the link target has both `intent/` and `material/`, the link is a
child-node entry point the recursive `check.sh` reaches; broken links and links to
non-nodes are dormant and do not materialize child-node content.

---
endorsed by qqp-dev
