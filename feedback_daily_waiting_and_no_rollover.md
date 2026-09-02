---
name: feedback_daily_waiting_and_no_rollover
description: /daily — new Waiting bucket (manual-only) + rolled_over surfacing mechanic killed
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 71f193a5-7b12-47db-8787-41a7607b7381
---

Two /daily engine changes locked 2026-05-25:

1. **Waiting bucket.** New `Tasks/waiting/` folder + `## Waiting` section on the daily page (rendered after Inbox). Holds things the user has *consciously parked*: not timely, must NOT pop up unless pulled by hand. /daily never auto-surfaces, auto-promotes, or sweeps waiting items — they're exempt from surface migration regardless of any date. They leave Waiting only via a manual move on the daily page (→ Today sets `status: active`; → Inbox sets `status: open`). Moving a line INTO `## Waiting` parks it (`status: waiting`). First resident: `dm-people-Lisa-linkedin-lobbly-pivot`.

2. **`rolled_over` is dead.** Removed the "⚠ prefix + (rolled Nx) suffix after 3x rolled" visual AND the "rolled_over ranks higher" ordering. Don't read, render, or increment `rolled_over`; ignore leftover fields in old files.

**Why:** user said "im not a fan of this come up after 3x rolled thing. if there is something that had to come up, then you would have a surface date for it." Staleness is not a surfacing signal — only `surface_on`/`due` reaching today promotes a task to Today (see [[feedback_future_due_to_inbox]]). If something must resurface on a day, it gets a `surface_on`; otherwise it just sits in its folder/section without escalating.

**How to apply:** When running /daily or /dump, never add urgency markers based on age. Today ordering = (1) hard-date-today, (2) Mode-aligned, (3) external cadence, (4) steady-state, (5) tools last — no rollover tier. Also softened SWEEP: compare against the UNION of Today+Inbox+Waiting sections, never sweep `Tasks/waiting/`, and never silently archive a live active file that merely failed to render (re-surface + log instead). All encoded in `.claude/commands/daily/SKILL.md`. Builds on [[feedback_daily_is_interface_folders_are_plumbing]].
