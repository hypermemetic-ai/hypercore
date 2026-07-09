---
id: TASK-14
title: 'Backlog board: compact card labels — kill the TASK- prefix noise'
status: Done
assignee:
  - task-14-board-labels
created_date: '2026-07-08 17:30'
updated_date: '2026-07-09 00:16'
labels:
  - parallel-ok
dependencies: []
priority: low
ordinal: 12000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Operator (07-08): the board makes poor use of horizontal space — 'TASK-x' eats most of a card while the prefix adds no information when task is the only type. Want a dense scheme that keeps cards real small: bare id plus a super-shortened label (single word, consonant-skeleton, aggressive abbreviation — survey prior art: tracker key schemes, tmux window naming, abbreviation algorithms). Avenues to evaluate: Backlog.md config (custom/empty id prefix?), board rendering options, an upstream feature request/PR to MrLesk/Backlog.md, or a thin qq-side board wrapper. ALSO (07-08, same cockpit-surface concern): backlog-board was launched via 'herdr agent start', so it shows up in herdr's agents list and eats sidebar space although it is not an agent — find the non-agent way to run a utility pane (plain pane launch, an exclude flag, or a herdr feature request) so the sidebar stays reserved for actual agents. Originally capture-only; implementation and verification notes are below.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 qq-board renders a compact kanban from the backlog: one row per task, bare numeric id (no TASK- prefix) plus a single-word consonant-skeleton abbreviation of the title; a card is ~12 chars
- [x] #2 qq-board --watch auto-refreshes for use as a persistent cockpit pane
- [x] #3 qq-board pane opens the board as a herdr utility pane that does NOT register in herdr agent list (the non-agent pane pattern: pane split + send-text + Enter)
- [x] #4 qq-activate.sh links qq-board onto PATH like qq-phase/qq-wip
- [x] #5 All four avenues from the description are evaluated and the findings recorded in the task (config prefix, board render options, upstream FR, qq-side wrapper)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Evaluate avenues: backlog config (task_prefix read-only/permanent after init — dead), board render options (layout only; card format hardcoded at src/ui/board.ts formatTaskListItem), upstream FR (optional follow-up; wrapper makes it non-blocking), qq-side wrapper (chosen). 2. Build bin/qq-board: parse 'backlog task list --plain', render status columns side by side, card = bare id + consonant-skeleton word, priority colors; --watch loop; pane subcommand via herdr pane split+rename+send-text+Enter. 3. Wire symlink in qq-activate.sh. 4. Verify: render output, agent-list non-registration. Prior art for the abbreviation: tracker keys (Jira short project keys / GitHub bare #N), tmux automatic-rename+truncation, disemvoweling (keep first letter, drop vowels, collapse repeats, truncate).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
AVENUES EVALUATED (AC5): (1) Backlog.md config — task_prefix exists in config.yml but is permanent after init ('Task prefix cannot be changed after initialization', v1.47.1); emptying it would need re-init + id migration of every task file. Dead. (2) Board rendering options — layout (horizontal/vertical) only; the card label is hardcoded upstream as '${task.id} - ${task.title}' in src/ui/board.ts formatTaskListItem. Dead. (3) Upstream FR/PR to MrLesk/Backlog.md — viable (a display-only compact-ids option), no existing issue found; NOT filed (outward-facing — operator's call), made non-blocking by (4). (4) qq-side wrapper — CHOSEN: bin/qq-board renders a dense read-only board from 'backlog task list --plain' (~30 cols total vs full-width TUI cards); the interactive TUI stays available as 'backlog board'.
ABBREVIATION SCHEME: first significant title word (articles/preps/generic verbs skipped); words <=4 chars kept whole; else first letter + disemvoweled remainder, adjacent repeats collapsed, truncated to 6 ('Orchestrate rework...' -> '8 orchst', 'Backlog board...' -> '14 bcklg'). Prior art surveyed: tracker key schemes (Jira short project keys; GitHub bare #N within one repo), tmux automatic-rename + window-name truncation, classic consonant-skeleton/disemvoweling. Collisions tolerated — the id disambiguates.
NON-AGENT UTILITY PANE (cockpit-surface concern): 'herdr pane split --current' + 'pane rename' + 'pane send-text' + 'pane send-keys Enter' creates a plain pane that does NOT register in 'herdr agent list' — verified live (test pane absent from agent list; 'herdr agent start' panes like gate-attach do register). Caveat: 'herdr pane run' returns rc=0 but silently does nothing — use send-text + Enter. 'qq-board pane [--direction] [--ratio]' wraps the whole pattern. After merge + qq-activate, relaunch the operator's board pane with 'qq-board pane' and close the old agent-started one.
<!-- SECTION:NOTES:END -->
