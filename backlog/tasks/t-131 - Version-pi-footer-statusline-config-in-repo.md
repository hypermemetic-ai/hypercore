---
id: T-131
title: Version pi-footer statusline config in repo
status: To Do
assignee: []
created_date: '2026-07-21 06:11'
labels: []
dependencies: []
ordinal: 57000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The live pi-footer config at ~/.pi/agent/extensions/pi-footer.json was edited directly (footer content fixes: keep only cost + context percent, warning>=20%/error>=50%, hide merge-ready ❔ badge) but is untracked. Bring it under Repository version control so changes land through GitHub Flow.

Decision ledger:
- Footer content (drop token counters except dollar; show context percent; thresholds warning 20 / danger 50; hide merge-ready ambient badge): settled by verbatim operator instruction in this session (asked-and-answered exchange).
- Version the config in the Repository and PR it: settled by verbatim operator instruction ('we need a branch and pr for mechanical reasons').
- Mechanism = track at extensions/pi-footer.json and symlink the package's fixed config path (~/.pi/agent/extensions/pi-footer.json) to it: consistent with the Repository pattern of settings.json referencing live repo paths; pi-footer's config path is fixed at $AGENT_DIR/extensions/pi-footer.json (only PI_FOOTER_CONFIG env override), so a symlink avoids env plumbing.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 extensions/pi-footer.json tracked in the Repository carries the agreed footer config
- [ ] #2 ~/.pi/agent/extensions/pi-footer.json resolves to the Repository content and pi-footer renders through it (verified headless)
- [ ] #3 Change lands on a branch as one PR; operator merges
<!-- AC:END -->
