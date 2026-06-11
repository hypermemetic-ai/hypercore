# words

## from the queue . 2026-06-11

operator (2026-06-11): document opens documents for hypercore, should be the "selected work unit" whatever that means. either queue screen becomes sensitive to that or document moves to work view? unsure, work it out, present ideas

machine (2026-06-11): on the document key — a decision card is on the queue, "document and the selected work unit", three ideas with their costs. 1: d moves to the work view, on the selected project line, and leaves the queue. 2: d reads where you stand — the queue keeps intent.md, the work view gains the selected unit's documents. 3: a standing selected-unit state, set in the work view, named in the header, read by d from the queue. my read: 2 is the lean one — the selection already lives in the work view's project lines, nothing is lost on the queue, no hidden state rides the header. your pick on the card settles it; nothing is built until then.

operator (2026-06-11): how do sessions start when I send a message?

machine (2026-06-11): your words land in words.md and commit in your name; then hyper writes brief.md fresh (the live queue state) and starts the command in the machine file — claude -p with a standing summon instruction, headless, in this repo. that session reads the brief, queue.md and words.md, trues up the record if it is behind, answers every word not yet ended by a machine line, commits as it goes, and stops. one runs at a time — a pid lock; words that land mid-answer (like this one) wait and trigger one more summon when the run ends. a behind record with no words waiting goes to the mini instead, which only commits and never edits.

