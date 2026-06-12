# words

## from the decision card, on "how hypercore's own graphs sit in the system" . 2026-06-11

operator (2026-06-11): I think 2 is right but I want to be sure. do we agree that graph-machinery folding into hypercore should mean that its CONTENTS (intent included) should be placed in the hypercore folder? because right now I believe that is not the case.

machine (2026-06-11): half yes, half correction. the contents are already in the hypercore folder: work/graph-machinery/graph.md sits in this repository, committed — nested in its own folder, because "a folder holds one execution graph," and the nesting is the preserved relation; folding never pours the child's files loose into the parent's root. and there was no intent to move: graph-machinery had no intent file of its own — it ran directly under hypercore's intent, and the doctrine it produced was ratified into intent.md's work section. what is genuinely absent is the upward link, which is exactly what 2 builds: a hypercore ledger whose node owns the spawning ask and carries the fold's result as material. so if "placed in the hypercore folder" means a parent node holding the result — 2 is right, and the card awaits your pick. if it means moving files up out of work/, doctrine says leave them where they are.

operator (2026-06-11): I don't see it. surely if we do work which is relevant to hypercore which just happens to be complicated enough that it earns its own subgraph, that doesn't mean that when the work is over the work stays in the subgraph. the subgraph should be preserves as HISTORY, and so should every execution graph for that matter, but its contents should go exactly where they belong. if it affects root hypercore files, it does so directly. if it results in a new folder at root, that's its prerogative. but it won't be the fact that the work spawned a subgraph that decides where it ends.

machine (2026-06-11): agreed — and that is already what happened. graph-machinery's products landed directly where they belong as the work ran: the work view in hyper, the brief in its hook, the format section in SKILL.md, the doctrine in intent.md — all root hypercore files, edited in place. work/graph-machinery/ holds exactly one file, graph.md: the ledger, pure history. nothing of the work stays in the subgraph but its record. my last line defended only that ledger staying put, and read as if products were trapped there — they never were. your principle — folder is history, contents land where they belong, spawning never decides where results end — is drafted as a statement in the work section, [machine], returning through the queue (67c30d9). the card itself still awaits your pick; the principle holds under all three options.

operator (2026-06-11): I see, I understand now. I think if we treat that folder as history then we should name it as such. either history or archive. current work can go under work. if no work is current, we can lose the work folder. if no work is archived, then we don't need history/archive.

machine (2026-06-11): done, and you already accepted it from its card while this session ran: folded graphs live in archive/ — your pick over my first choice, history — graph-machinery sits there now, work/ is gone until work is current, and hyper's fold moves every future folder in the act that folds it. the rule returns through the queue as a statement: "An open graph's folder sits in its parent's work/; the act that folds it moves it to archive/. Neither exists empty."

operator (2026-06-11): I don't know if I understand the difference between 1 and 2 now that we've clarified this. 2 seems to want to add a ledger. what does that do for us?

machine (2026-06-11): now that archive/ exists, very little. 2's ledger would be one file where every ask hypercore spawned is a node carrying its fold's result — one place to read instead of three. but ls archive/ already lists every folded graph, each graph.md carries its own ask and result, and work.md carries what awaits you; the ledger would restate all three and be one more file to keep true on every spawn and fold — and the first fold already lagged once. what 1 adds is the only thing actually missing: hypercore's graphs shown under it instead of beside it, every root naming its parent. the machine's read: 1, and a ledger can earn itself later if its absence ever blocks work twice. the pick stays yours on the card.

operator (2026-06-11): option 1 — subgraph, made visible — open graphs of hypercore appear under the hypercore line, reached by unfolding it, never beside it; every root names its parent (of: hypercore); the fold stays as it is, since the graph's folder already sits inside hypercore's — display and convention, one redo to take back

machine (2026-06-11): built, and you accepted it from its card while I worked (61bc55a) — relaunch hyper to see it, since the one open started before the code landed. w now shows one line, hypercore, its counts on the right; enter unfolds to the work entries with the graphs below them; enter on a graph line opens its nodes, headed hypercore › graph-machinery; esc walks back the same path. every root names its parent: of: hypercore sits on graph-machinery's root and the format in SKILL.md carries the rule. your pick also settled this card at last — the entry left work.md (a4982be); why it ever outlived the pick is answered on your other word.

## from the queue . 2026-06-11

operator (2026-06-11): once again I selected an option and still see the card in the queue.

machine (2026-06-11): your pick landed — the card just outlived it, and here is why: settle-at-word was accepted at 18:50, but the hyper you picked in was started before that, and a running hyper re-reads the ledgers every second while its own code it reads only at launch. the old pick path spoke the word without dropping the entry. the hyper you opened at 19:22 wears the fix — your next pick settles on the spot — and I have dropped the entry your pick earned (a4982be). the gap is general: every accepted slice stays invisible on screen until you relaunch. whether hyper should notice its own staleness is on a decision card — a notice line with a relaunch key, an automatic re-exec, or leave the relaunch yours.

## from the decision card, on "the interface wears old code until relaunched" . 2026-06-11

operator (2026-06-11): option 3 — leave it — relaunch stays yours, and every slice's try line keeps naming it

