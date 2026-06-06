# mounting -- machine statements

a project mounts as a symbolic link under this home node -- at `home/<name>` from the root
-- pointing to a distinct repository outside the hypercore root. when the link target has
`intent/`, the link is a child-node entry point the recursive `check.sh` reaches; broken
links and links to non-nodes are dormant and do not materialize child-node content.
