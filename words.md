# words

## from the decision card, on "how hypercore's own graphs sit in the system" . 2026-06-11

operator (2026-06-11): I think 2 is right but I want to be sure. do we agree that graph-machinery folding into hypercore should mean that its CONTENTS (intent included) should be placed in the hypercore folder? because right now I believe that is not the case.

machine (2026-06-11): half yes, half correction. the contents are already in the hypercore folder: work/graph-machinery/graph.md sits in this repository, committed — nested in its own folder, because "a folder holds one execution graph," and the nesting is the preserved relation; folding never pours the child's files loose into the parent's root. and there was no intent to move: graph-machinery had no intent file of its own — it ran directly under hypercore's intent, and the doctrine it produced was ratified into intent.md's work section. what is genuinely absent is the upward link, which is exactly what 2 builds: a hypercore ledger whose node owns the spawning ask and carries the fold's result as material. so if "placed in the hypercore folder" means a parent node holding the result — 2 is right, and the card awaits your pick. if it means moving files up out of work/, doctrine says leave them where they are.

operator (2026-06-11): I don't see it. surely if we do work which is relevant to hypercore which just happens to be complicated enough that it earns its own subgraph, that doesn't mean that when the work is over the work stays in the subgraph. the subgraph should be preserves as HISTORY, and so should every execution graph for that matter, but its contents should go exactly where they belong. if it affects root hypercore files, it does so directly. if it results in a new folder at root, that's its prerogative. but it won't be the fact that the work spawned a subgraph that decides where it ends.

machine (2026-06-11): agreed — and that is already what happened. graph-machinery's products landed directly where they belong as the work ran: the work view in hyper, the brief in its hook, the format section in SKILL.md, the doctrine in intent.md — all root hypercore files, edited in place. work/graph-machinery/ holds exactly one file, graph.md: the ledger, pure history. nothing of the work stays in the subgraph but its record. my last line defended only that ledger staying put, and read as if products were trapped there — they never were. your principle — folder is history, contents land where they belong, spawning never decides where results end — is drafted as a statement in the work section, [machine], returning through the queue (67c30d9). the card itself still awaits your pick; the principle holds under all three options.

operator (2026-06-11): I see, I understand now. I think if we treat that folder as history then we should name it as such. either history or archive. current work can go under work. if no work is current, we can lose the work folder. if no work is archived, then we don't need history/archive.

operator (2026-06-11): I don't know if I understand the difference between 1 and 2 now that we've clarified this. 2 seems to want to add a ledger. what does that do for us?

## from the acceptance card, on "folded graphs live under history" . 2026-06-11

operator (2026-06-11): I think I prefer archive over history

