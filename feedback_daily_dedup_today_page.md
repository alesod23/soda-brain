---
name: feedback_daily_dedup_today_page
description: Every /daily run must dedup/merge overlapping tasks on the Today page; ask when unsure
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f3369279-a104-4307-b6f1-e62111d951c5
---

On EVERY `/daily` (and any "review my today page" request), scan the Today + Inbox candidate set for duplicate / overlapping tasks and unify them BEFORE composing. Reason about the actual action/outcome, not the title string (open each task body — similar titles can be different jobs, different titles can be the same job). Keep the **more complete** task (more body, recipient/draft, richer provenance, dates), merge the unique valuable detail from the less-complete one into it, then DELETE the less-complete duplicate (file + daily line). This is a true dedup deletion, not the "vanished → park in Waiting" rule.

**Why:** the user found his Today page cluttered with overlapping tasks (e.g. two separate "email BMW about why saying NO to a patent is hard" tasks — one I'd just created in /dump, one richer existing `email-marc-bmw-disclosure-followup`). Mandated 2026-06-09.

**How to apply:** implemented as step **7b. DEDUP** in the `/daily` engine at `C:\Users\Alessandro\.claude\commands\daily\SKILL.md` (loads every run, so it persists across sessions/chats). On **genuine doubt** whether two items are the same: if run manually, ASK via AskUserQuestion (merge or keep separate?); if `/dump`-triggered (non-interactive), keep both and flag in the summary. Never merge genuinely different outcomes that only share a project/keyword. See [[reference_daily_briefing]], [[feedback_daily_is_interface_folders_are_plumbing]].
