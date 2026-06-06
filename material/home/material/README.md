# home - mount point

The home node's material tree is the mount point for linked project nodes. Each mounted
project is a distinct git repository outside the hypercore root, exposed here by a symbolic
link at:

    material/home/material/<name>

Create the first local shape and mount link with:

    material/bin/home greenfield <name> <target-path>

The target receives only its own `intent/organizing-document.md` and `material/` tree. The
root methodology, root check script, adapter directory, and root `AGENTS.md` are not copied.
Work through the mount path when the node needs to inherit the root methodology.

The home holds zero mounted projects until the operator mounts the first. A valid link whose
target carries both `intent/` and `material/` is a node the recursive `check.sh` reaches;
broken links and links to non-nodes are not materialized child nodes.
