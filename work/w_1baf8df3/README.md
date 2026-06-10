# viewer comfort: dark mode, readability, live updates

`w_1baf8df3` · **open** · check: operator

on: `s_7b70bab7` — "The viewer is comfortable to live in: dark by default and easy on the eyes, readable, and…"
fold when: the operator works in the dark viewer comfortably and watches a change land without refreshing
produces:
- `s_cb9d5e78` — "The viewer keeps itself current: it watches a cheap fingerprint of the store and re-deriv…"

## gather

- `wn_4be9c36a` operator named the failures: the white background is hard on the eyes (wants dark mode), the UI needs further readability and UX work, and the view goes stale — changes require a manual refresh  (execute: machine, propose: operator)

## generate

- `wn_125be890` readability pass: larger and higher-contrast graph labels, calmer edge labels, panel typography and spacing tuned for reading  (execute: machine, propose: machine)
  - depends-on -> `wn_4be9c36a` "operator named the failures: the white background is hard o…"
- `wn_4290f510` live updates: GET /api/version fingerprints the store; the client polls it every few seconds and re-derives the whole view when it moves, preserving selection and viewport  (execute: machine, propose: machine)
  - depends-on -> `wn_4be9c36a` "operator named the failures: the white background is hard o…"
- `wn_4d2d491d` theme as CSS variables: dark by default (system- and toggle-overridable, persisted), every hardcoded color in index.html and the cytoscape style mapped through the palette  (execute: machine, propose: machine)
  - depends-on -> `wn_4be9c36a` "operator named the failures: the white background is hard o…"

## test

- `wn_29a709f4` a verb run outside the page shows up in the open viewer without a refresh  (execute: machine, judge: machine, propose: machine)
  - verdict: **pass** — CDP against a sandbox serve: add-statement from the CLI moved the toolbar count 9→10 within two 3s poll ticks; a window marker survived, so the page re-derived rather than reloaded; read-only verbs leave /api/version unchanged
  - tests -> `wn_4290f510` "live updates: GET /api/version fingerprints the store; the …"
- `wn_6afe45a5` the operator works in the dark viewer comfortably and watches a change land without refreshing  (execute: machine, judge: operator, propose: machine)
  - verdict: **open**
  - tests -> `wn_4290f510` "live updates: GET /api/version fingerprints the store; the …"
  - tests -> `wn_4d2d491d` "theme as CSS variables: dark by default (system- and toggle…"
  - tests -> `wn_125be890` "readability pass: larger and higher-contrast graph labels, …"
- `wn_9d25b35d` dark by default, light by toggle: both themes render coherently; the toggle persists and keeps the viewport  (execute: machine, judge: machine, propose: machine)
  - verdict: **pass** — headless screenshots of a sandbox serve in both themes, 2026-06-10; CDP toggle test: dark→light flips data-theme, persists to localStorage, zoom unchanged to 1e-9
  - tests -> `wn_4d2d491d` "theme as CSS variables: dark by default (system- and toggle…"
