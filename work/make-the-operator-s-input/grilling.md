surfaced: 0

[Q] Is the input one line or a multi-line field? "up/down movement" only has an intrinsic meaning in a multi-line field — on a single line, up/down has nothing to move over unless we invent submission-history recall (new stored state). So either the input becomes a small text area that grows upward from the footer (pushing the queue/work up) with up/down moving the caret between lines, or it stays one line and up/down recalls prior submissions.
lean: Make it a multi-line text area: left/right walks the line, up/down moves between lines, the field grows upward from the footer as lines are added and collapses back to one line when empty. This matches "up/down movement" literally, and hypercore asks are prose (this very ask is multi-clause) — a one-line footer is painful to compose them in.
flip: If the operator's asks to the architect are effectively always one line and longer composition happens elsewhere, keep it single-line — then up/down recalls previous submissions (a history ring) and a pasted multi-line block collapses its newlines to spaces.
answer: 

[Q] How is the caret drawn? Today it's a painted `▖` glyph (always visible, static, captured in every pure frame/screenshot). The alternative is the terminal's own hardware caret — `curs_set(1)` positioned by the window adapter from a caret column the pure frame carries — which blinks like every terminal app but is invisible to the headless frame/screenshot path.
lean: Switch to the native terminal caret, positioned from a pure caret column on the frame. It definitively fixes "too low" (the terminal draws its caret on the text baseline), feels like a real field, and keeps the frame pure (the column is data; only the adapter calls `curs_set`).
flip: If the painted face is the source of truth — the caret must show in the watched-on-running-window checks and in face screenshots, with no reliance on terminal caret behavior — keep it painted and just move the glyph onto the character cell (a reverse-video block) instead of the low quadrant.
answer: 

[Q] Does copy/paste cross to the operating system's clipboard, or stay inside hypercore? Crossing means the operator can paste text from their browser into the compose line and copy out of it into other apps; staying internal means copy/paste only move text within the running session.
lean: Cross the boundary with no external dependency: accept the terminal's bracketed-paste stream for paste-in (handles multi-line) and write the system clipboard via OSC 52 for copy-out. This is what "a real editable field" implies and needs no `xclip`/`pbpaste` binary.
flip: If the operator's terminal or SSH path doesn't carry bracketed paste / OSC 52, fall back to an internal yank register that copy and paste share within the session — no OS clipboard at all.
answer: 

[Q] Can the operator select part of the line to copy, or does copy take the whole input? A partial selection means a mark/anchor with shift+arrows (and shift+home/end), rendered as a highlighted span — a real selection sub-mode. Whole-line copy needs none of that.
lean: Whole-input copy, no partial selection: copy takes the entire current input and paste inserts at the caret. It covers the common case (lift the line, drop it elsewhere) and keeps the input free of a selection mode and its highlight rendering.
flip: If the operator routinely needs to copy a fragment (a path, a quoted phrase) out of a longer compose, add the selection: shift+arrows set a highlighted span and copy takes that span, the whole line only when nothing is marked.
answer:
