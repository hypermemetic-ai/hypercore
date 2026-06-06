# structure -- machine statements

every document is a markdown (.md) file.
the organizing document is `intent/organizing-document.md`.
each segment's intent document is `intent/<segment>.md`.
each segment's machine statements are in `intent/machine-statements/<segment>.md`.
the methodology prose is materialized in `hypercore.md`.
a child node is inlined at `<name>/` unless a machine statement settles a mount path there
as an external reference.
`check.sh` checks every current node in the tree -- the root and each child node, a child
node being any directory or settled linked entry point holding `intent/`.
