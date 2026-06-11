# words

## from the decision card, on "how hypercore's own graphs sit in the system" . 2026-06-11

operator (2026-06-11): I think 2 is right but I want to be sure. do we agree that graph-machinery folding into hypercore should mean that its CONTENTS (intent included) should be placed in the hypercore folder? because right now I believe that is not the case.

machine (2026-06-11): half yes, half correction. the contents are already in the hypercore folder: work/graph-machinery/graph.md sits in this repository, committed — nested in its own folder, because "a folder holds one execution graph," and the nesting is the preserved relation; folding never pours the child's files loose into the parent's root. and there was no intent to move: graph-machinery had no intent file of its own — it ran directly under hypercore's intent, and the doctrine it produced was ratified into intent.md's work section. what is genuinely absent is the upward link, which is exactly what 2 builds: a hypercore ledger whose node owns the spawning ask and carries the fold's result as material. so if "placed in the hypercore folder" means a parent node holding the result — 2 is right, and the card awaits your pick. if it means moving files up out of work/, doctrine says leave them where they are.

