---
name: feedback_daily_deletion_parks_to_waiting
description: "Deleting a task line on a /daily page is an intentional \"off my plate\" signal — engine now parks it in Waiting + flags it once, never silently re-surfaces it to Today."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ee7b018d-be80-452d-afe0-260d146975b1
---

When the user deletes a task line from a `task-land/Daily/*.md` page, that is an **intentional signal** ("I don't want this nagging from Today"), not noise. The old `/daily` engine ignored it: a deleted line is *absent* from the page, so step-2 sync never saw it, and step-3 had two contradicting rules — "archive vanished active files as stale" vs "re-surface clearly-open ones as render drop-offs." Re-surface won, so deliberately-deleted tasks reappeared on Today every morning (their past `surface_on` kept re-promoting them). User flagged this 2026-06-05 after two thesis tasks he'd deleted in yesterday's view came back.

**Fixed in `~/.claude/commands/daily/SKILL.md` (2026-06-05):** a task that vanished from yesterday's page (deletion OR render drop-off — indistinguishable from one day's page) is moved to `Tasks/waiting/` (`status: waiting`) and surfaced ONCE in the morning brief as "Removed yesterday → parked in Waiting (drag to Today to restore, strike to cancel)". Never silently re-surface to Today; never silently archive.

**Why:** parking is reversible and non-destructive — it honors the deletion (stops the Today nag) while protecting against a genuine render bug eating real work. Hard-cancel/done stays reserved for an explicit `[x]` or `~~strike~~` ("crossed is crossed", resolved first in step 2). A bare deletion must never archive/cancel a task outright.

**How to apply:** the SKILL.md is the engine and is read on every `/daily` (and `/dump` sync) in every session, so the behavior is already global. If a user complains a deleted/removed item "keeps coming back," the root cause is almost always a past `surface_on`/`due` re-promoting an open file — check the task file's status + dates, don't just edit the rendered page. See [[feedback_daily_waiting_and_no_rollover]], [[feedback_daily_is_interface_folders_are_plumbing]], [[reference_daily_briefing]].
