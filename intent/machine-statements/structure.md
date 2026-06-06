# structure -- machine statements

every document is a markdown (.md) file.
the organizing document is `intent/organizing-document.md`.
each segment's intent document is `intent/<segment>.md`.
each segment's machine statements are in `intent/machine-statements/<segment>.md`.
the methodology prose is materialized in `material/hypercore.md`.
a child node is inlined at `material/<name>/` unless a machine statement settles it as an
external reference.
`material/check.sh` checks every node in the tree -- the root and each child node, a child
node being any directory holding both `intent/` and `material/`.
