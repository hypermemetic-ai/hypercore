# Cockpit

`cockpit/` is the source of truth for the human-driven terminal surface. The
activation script symlinks each file into `~/.config`, so editing here or through
the live config path edits the same file. It also wires the Claude Code status
line from `bin/qq-phase render` and links `bin/qq-board` for a compact Backlog.md
utility pane; those helpers live in `bin/` because they are executable glue, not
static config.

## Files
- `yazi/yazi.toml` — pane-first file navigation; markdown opens in-pane through
  mdcat by default, with tuned Glow as the alternate opener.
- `yazi/keymap.toml` — `!` opens a shell here; `g H` jumps to `~/projects/qq`.
- `glow/glow.yml` — fixed-width, no-pager Glow defaults for pane rendering.
- `glow/tuned.json` — the hand-tuned Markdown theme used by Glow.
- `herdr/config.toml` — tokyo-night, onboarding suppressed, agent sorting, and
  cockpit pane bindings: `prefix+f` runs `qqy`, `prefix+shift+f` runs `qqbr`.
- `shell/file-navigation.bash` — `QQ_HOME`, generic `y()`/`br()` wrappers,
  repo-focused `qqroot`/`qqy`/`qqbr`, and `qfiles`/`qtree` aliases.

## Linked Helpers
- `bin/qq-phase render` — Claude Code status-line reader for `.qq/state.json`.
- `bin/qq-board` — compact read-only Backlog.md kanban; `qq-board pane` opens it
  as a plain herdr utility pane, outside the agents sidebar.

## Flow
Herdr `prefix+f` spawns a pane running `qqy`; `qqy` opens yazi at the repo root;
Enter on a `.md` file renders in-pane via mdcat or Glow tuned to the pane width.
`prefix+shift+f` opens broot at the same root through `qqbr`. `qq-board pane`
opens the compact board for persistent cockpit visibility without registering a
fake agent.
