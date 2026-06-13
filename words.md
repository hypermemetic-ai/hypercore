# words

## words . 2026-06-13

operator (2026-06-13): I read that fable 5 has gone. we might need to set opus 4.8 xhigh

machine (2026-06-13): Confirmed, and done. I ran the interface's exact command and it errors: `claude -p ... --model claude-fable-5` → "There's an issue with the selected model (claude-fable-5). It may not exist or you may not have access to it." So every summon would have failed — you read right. I set the machine file to `--model claude-opus-4-8 --effort xhigh` (tested: returns clean), and the mini file to the same model at `--effort low` — its ratified design is "the same model as the full machine," so it moves with the machine rather than staying broken on fable. hyper reads both files fresh on each summon and for the bottom-right label, so the switch is already live — no relaunch needed. One `git revert` brings fable back if it returns.

