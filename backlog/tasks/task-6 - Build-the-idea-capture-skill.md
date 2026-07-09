---
id: TASK-6
title: Build the /idea capture skill
status: Done
assignee:
  - task-6-idea-skill
created_date: '2026-07-08 14:41'
updated_date: '2026-07-09 00:38'
labels:
  - parallel-ok
dependencies:
  - TASK-3
priority: medium
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Idea #1, design locked 07-07: capture verbatim in-turn, detached researcher writes ideas/NN-slug.md, completion shows as ambient status on the qq-phase surface. Rides the status substrate; needs the multi-producer fix first.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 skills/idea/SKILL.md exists and passed the writing-skills eval loop: RED baseline failures observed without the skill, GREEN compliance observed with it
- [x] #2 Capture is verbatim-first: raw operator input is written to the ideas/ surface before sharpening or research
- [x] #3 Research path spawns a detached researcher (setsid ... < /dev/null &) that enriches ideas/NN-slug.md and stamps qq-phase --producer idea-NN (capturing -> researching -> done/red); producer-slot isolation is verified
- [x] #4 No-research ideas land as a README Backlog bullet with no status stamps; bare /idea captures a handoff-style session snapshot
- [x] #5 Nothing returns to the transcript: completion is ambient status only
- [x] #6 Methodology support line + skill index, SKILLS-ATTRIBUTION.md, and ideas/README.md reference the skill
<!-- AC:END -->
