# words

## from the queue . 2026-06-11

operator (2026-06-11): how does it refresh itself live? it's quite impressive. hyper that is.

machine (2026-06-11): no watchers, no push — a one-second tick. the screen waits at most a second for a keypress (curses timeout); when none comes, it re-reads everything from disk — intent, queue, words, work, the graphs, git status — and redraws from scratch. the screen holds no state of its own, so whatever any session commits is on screen within a second. the repo is the state; hyper is just a fast mirror of it.

operator (2026-06-11): thanks. very cool.

machine (2026-06-11): glad it reads well. the simplicity is the point — nothing to desync. nothing new asked, so nothing opened; the queue stays clear.

