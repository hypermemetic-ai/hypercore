# mounting -- machine statements

a project mounts as a symbolic link under this home node's `material/` -- at
`material/home/material/<name>` from the root -- pointing to a distinct repository outside
the hypercore root. when the link target has both `intent/` and `material/`, the link is a
child-node entry point the recursive `check.sh` reaches; broken links and links to
non-nodes are dormant and do not materialize child-node content.
