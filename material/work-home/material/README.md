# work-home — mount point

The home node's code tree: the mount point its work folders mount into. Each work folder the
operator mounts becomes a child node of this home — a distinct git repository, added as a git
submodule registered in the **root** repository's `.gitmodules` (the home is a plain
subdirectory of the root, not its own git boundary):

    git submodule add <url> material/work-home/material/<name>

The home holds zero work folders yet. A checked-out work folder carries its own two trees and
is a node the recursive `check.sh` reaches; an absent one is checked by its own repository.
