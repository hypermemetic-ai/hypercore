# words

## from the queue . 2026-06-11

operator (2026-06-11): how does it refresh itself live? it's quite impressive. hyper that is.

machine (2026-06-11): no watchers, no push — a one-second tick. the screen waits at most a second for a keypress (curses timeout); when none comes, it re-reads everything from disk — intent, queue, words, work, the graphs, git status — and redraws from scratch. the screen holds no state of its own, so whatever any session commits is on screen within a second. the repo is the state; hyper is just a fast mirror of it.

operator (2026-06-11): thanks. very cool.

machine (2026-06-11): glad it reads well. the simplicity is the point — nothing to desync. nothing new asked, so nothing opened; the queue stays clear.

operator (2026-06-11): but how does the program change? how do we update the tui live? or do we?

machine (2026-06-11): we don't — and on purpose. the one-second tick re-reads data (the .md files, git), not code; a running hyper keeps the program it launched with. when the machine changes hyper it edits the file and commits, like any slice — the new code takes effect at the next launch (q, then ./hyper). no execv, no self-restart: a program that swaps its own code mid-frame can die mid-keypress, and a restart is one keystroke. so: data live, code on relaunch. if you want hyper to notice its own file changed and offer a restart, say so and i'll open the ask.

