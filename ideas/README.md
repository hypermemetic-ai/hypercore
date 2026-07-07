# Ideas

Informal backlog — dump thoughts here as they come, no ceremony. One line is
fine; a rough paragraph is fine. Nothing here is a commitment or a plan — it's a
holding pen. Groom it whenever: promote an idea to a plan (`writing-plans`), fold
it into `AGENTS.md`, or just delete it.

Quick thoughts go as bullets under **Backlog**. When an idea outgrows a line, give
it its own `NN-slug.md` file in this folder and leave a one-line pointer here.

## Backlog
- **The `/btw` ideas skill** → [`01-btw-ideas-skill.md`](01-btw-ideas-skill.md).
  Mid-session capture: type a thought, agent sharpens + researches in the
  background, files it ready to take on. Design aligned, three decisions open,
  not yet built. _(2026-07-06)_
- **Auto-compound, don't ask.** The agent shouldn't ask whether to compound or
  not — `ce-compound` (loop step 7) should just run when work lands green,
  capturing the solved problem and durable vocabulary without a yes/no prompt.
  The question itself is friction on something that should be automatic. _(2026-07-06)_
- **Orchestrate progress state** → [`02-orchestrate-phase-state.md`](02-orchestrate-phase-state.md).
  `qq-phase` stamps the loop's current phase to `.orchestrate/state.json` for a
  status widget. Built but unmerged — salvaged (with a re-appliable patch) from
  the pruned `qq-ac/orchestrate-progress` branch; promote or drop. _(2026-07-06)_
- **`codex exec` stdin-hang** → [`03-codex-exec-stdin-hang.md`](03-codex-exec-stdin-hang.md).
  `codex exec` blocks forever on `Reading additional input from stdin...` unless you
  close stdin — pass `< /dev/null`. One-line fix; wire it into `orchestrate`'s Build
  handoff so it never recurs. _(2026-07-06)_
- **Gate stuck after a rename** → [`04-gate-stale-path-after-rename.md`](04-gate-stale-path-after-rename.md).
  `git push no-mistakes` "succeeds" but no PR opens — the gate's stored repo path is
  the pre-rename `/home/qqp/projects/hypercore`; `no-mistakes init` repairs it. Add
  gate-refresh to the rename checklist. _(2026-07-06)_
