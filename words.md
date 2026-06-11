# words

## from the queue . 2026-06-11

operator (2026-06-11): model text shouldn't be central now that I'm looking at it. ruins the minimalism. maybe better to the right of the top bar.

operator (2026-06-11): or bottom right? lots of ideas here.

machine (2026-06-11): bottom right — of your two spots, the right of the top bar is where the status counts already live, and crowding them repeats the crime. the name now sits dim beside the key hints, the top row is title and status alone, and the card waits for your a; one word moves it if the other spot wins on sight.

operator (2026-06-11): if all that not running behind is is a dedicated session that spawns just to commit changes, a dumb model should be able to handle this, right? let's start thinking about a class of busywork tasks that we can delegate to the mini-machine (probably sonnet for us now, but like with the other, shouldn't be hardcoded, just set).

machine (2026-06-11): mostly right — and the exception is the design constraint. most true-ups are exactly that: commit what the dead session left, message faithful to the diff. but the standing orders also ask a true-up to finish or correct half-done work, and that part takes judgment. so the proposal now on your queue: a `mini` file beside `machine` — same one-line format, model set there, sonnet today — and record-behind true-ups route to it under a hard bar: commit what is actually on disk, never finish or correct; anything ambiguous it leaves, named, for the full machine. that bar doubles as the class definition for what else goes mini: mechanically checkable, no latitude, no operator-facing words. nothing is built — it stands as a decide card, and your word sets it.

operator (2026-06-11): I don't like this "go" and similar structure for decisions. just like the rest, should be keys with confirmation. while we're at it, the text that appears after pressing a is noisy and the important thing - needing to press y to confirm, is drowned out.

operator (2026-06-11): I never did see the desktop shortcut. that item was folded I believe but the change didn't really land.

machine (2026-06-11): both landed, each an acceptance card on your queue. keys: on a decide card g goes and c cuts — y confirms, and the key lands the word on the card exactly as if you had typed it, committed in your name; s stays for redirects in your own words. and every confirm line now leads loud with "y confirms …", the entailment dim behind it — the y no longer drowns. the shortcut: your fold was honest, the link was being stolen. every launch of any copy of hyper — my own test copies in /tmp included — re-pointed the menu symlink at itself, and when the copy vanished the link dangled and cinnamon dropped the entry. test copies never touch it now, only a dangling link is reclaimed, the entry gained a category so the menu files it under accessories, and the link points at the repo again.

operator (2026-06-11): explain to me, what's the correspondence now between stuff I write and fable sessions? am I spawning multiple in parallel? when I see "the machine is answering - 810s" is that a combined session all my stuff is piling up into? or multiple sessions with separate concerns? are we worried about parallelism? what about session lenght/context? the operator doesn't strictly speaking have to know these things if they work, but they qualify as decisions they should be consulted about. speaking of, how mushy is our machinery for making decisions like "operator should know about this" (deciding what should be surfaced as a decision)? we need our system to function even if a model like opus is running it, not just frontier intelligence like fable. the machine is answering could be "the machine is working" because it isn't just answering really. these are disconnected thoughts largely but all real concerns.

