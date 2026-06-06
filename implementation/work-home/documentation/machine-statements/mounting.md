# mounting — machine statements

a work folder mounts as a git submodule under this home node's implementation/ — at implementation/work-home/implementation/<name>/ from the root — a distinct repository registered in the root repository's .gitmodules; the home is a child node, a plain subdirectory, not its own git boundary, so it has no .gitmodules of its own. checked out the submodule is a node the recursive check.sh reaches; absent, it is checked by its own repository.
