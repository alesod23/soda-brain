---
name: reference_todo_pipeline
description: "The to-do pipeline built 2026-09-27 (created / in progress / ready for review / finished), how a to-do links to its hub card, how calls go to the CRM Call page, and the /todo skill."
metadata:
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-27T13:59:01.642Z
---

**His ruling (2026-09-27):** "a to-do item is created, in progress, ready-for-review, finished"; in progress =
picked up by AI; ready for review = clickable, opens the summary of the AI's work; "all of these things ... are
actually hub cards, and there is a link to that specific hub card from the Obsidian". Categories: "I don't want
you to bother about this now".

**What exists:**
- `task-land/_system/pipeline.py` is the ONLY writer of the state (frontmatter `stage`, `stage_note`,
  `hub_card`, `hub_cards`, `picked_at`, `picked_by`, `ready_at`): `list | show | pickup | note | ready |
  release | finish | call | sync`. Log `_system/pipeline.log`.
- Daily page: `Format-StageLine` in `daily-lib.ps1` renders ONE indented non-checkbox line under the category
  bullet (robot = in progress, eyes = ready for review + `[open the card](http://100.85.52.84:4142/#c<id>)`).
  It is dropped on absorb by design (`Read-IndentedBlock` keeps only the category/date bullet and checkboxes).
- `daily-sync.ps1` step (f) runs `pipeline.py sync` after crm-bridge (not in `-RenderOnly`): card approved =
  task done; card rejected/closed = back to open with his words in the notes; he ticks the task = the card closes.
- `ready` posts one hub card per to-do (`type: todo-review`, `meta.task`), summary at most 58 lines, or links an
  existing card with `--card`.
- Calls (CRM ledger H31): `pipeline.py call <slug> --name ... [--phone]` finds or creates the CRM person, sets
  `contact:`; crm-bridge hands the step over; the person shows on the CRM Call page (the step text must contain
  "call": the Call page matches the English word). First one moved: Rania Tohme (CDC).
- Contract for sessions: `task-land/_system/PIPELINE-WORKER.md`; skill `/todo` (laptop + box).

**Not built, his decision:** a scheduled worker that picks to-dos up with nobody present. Today a session does
it when asked (`/todo`). An unattended worker runs tools without him, so it needs his explicit yes and a scope.

**How to apply:** never write `stage:` by hand; never leave a to-do in progress with nobody on it (`release`).
Related: [[reference_hub_review_ui]], [[reference_hub_lives_on_the_box]], [[reference_draft_review_lane]].
