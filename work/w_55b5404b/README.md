# viewer shows ownership and work status

`w_55b5404b` · **open** · check: operator

on: `s_f35147a3` — "The operator can read the system's state at a glance: the viewer shows who owns each stat…"
fold when: the operator opens the viewer and can tell machine-owned statements and open work apart at a glance

## gather

- `wn_92d11a1e` operator named the failures to fix: two-finger zoom is annoying to navigate, and the screen is a wall of node text, unreadable; statements now arrive beside the graph and need their own panel  (execute: machine, propose: operator)

## generate

- `wn_11774d3c` toolbar summary: counts of statements pending endorsement and open work  (execute: machine, propose: machine)
- `wn_4e9bde2c` carry owner and status from node props into viewer data so styles can select on them  (execute: machine, propose: machine)
- `wn_6d4117df` viewer: machine-owned statements amber and dashed, work nodes diamonds dimmed by status, toolbar counts pending endorsement and open work, details panel names owner and folding condition  (execute: machine, propose: machine)
- `wn_7bfef8fe` style: machine-owned statements amber and dashed; work nodes diamonds, dimmed once folded  (execute: machine, propose: machine)
- `wn_7c513a68` viewer v2: intent panel with endorse buttons, works as boxes containing their operations, deterministic layout, zoom controls, statement and operation detail panes  (execute: machine, propose: machine)
  - depends-on -> `wn_92d11a1e` "operator named the failures to fix: two-finger zoom is anno…"
  - depends-on -> `wn_7bfef8fe` "style: machine-owned statements amber and dashed; work node…"

## test

- `wn_39247829` operator opens the viewer and can tell machine-owned statements and open work apart at a glance  (judge: operator, propose: machine)
  - verdict: **open**
  - tests -> `wn_7c513a68` "viewer v2: intent panel with endorse buttons, works as boxe…"
  - tests -> `wn_6d4117df` "viewer: machine-owned statements amber and dashed, work nod…"
- `wn_543659fb` works render as boxes of their operations; membership is nesting; only combinators draw as edges; layout is deterministic  (execute: machine, judge: machine, propose: machine)
  - verdict: **pass** — headless screenshots of the sandbox viewer, 2026-06-10
  - tests -> `wn_7c513a68` "viewer v2: intent panel with endorse buttons, works as boxe…"
- `wn_627539fe` endorse endpoint takes statements on and rewrites the views; bad ids and empty payloads are refused  (execute: machine, judge: machine, propose: machine)
  - verdict: **pass** — curl against a sandbox server: endorsed, already-owned, missing id, and empty payload paths all answered correctly; work.md re-rendered
  - tests -> `wn_7c513a68` "viewer v2: intent panel with endorse buttons, works as boxe…"
- `wn_cc8f3249` navigation has explicit zoom controls and a gentler wheel  (execute: machine, judge: machine, propose: machine)
  - verdict: **pass** — headless screenshots; wheelSensitivity 0.2 plus toolbar buttons
  - tests -> `wn_7c513a68` "viewer v2: intent panel with endorse buttons, works as boxe…"

## material

- [viewer v2 design](m_3e9a2028.md) (document) — on wn_7c513a68
