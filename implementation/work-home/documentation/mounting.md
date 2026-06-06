# mounting

each work folder the operator mounts is a distinct git repository, governed within itself.
a mounted work folder is a child node of this home, carrying its own documentation and implementation trees together — never flattened into the home.
the home holds zero work folders until the operator mounts the first.

## machine
a work folder mounts as a git submodule under this home node's implementation/ — at implementation/work-home/implementation/<name>/ from the root — a distinct repository registered in the root repository's .gitmodules; the home is a child node, a plain subdirectory, not its own git boundary, so it has no .gitmodules of its own. checked out the submodule is a node the recursive check.sh reaches; absent, it is checked by its own repository.

---
endorsed by qqp-dev
