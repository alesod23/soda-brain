---
name: feedback-daily-is-interface-folders-are-plumbing
description: "task-land/Daily/<today>.md is the user's interface; Tasks/{active,inbox,archive} are internal plumbing I keep in sync with the daily, not the reverse"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: dcb4b264-a788-4271-a6cc-87bdb34ca2e4
---

**The daily note is the only thing Alessandro tweaks. Everything else is my plumbing.**

`task-land/Daily/<today>.md` = the user's single interface to today's work. Ticks, removals, manual additions, inline edits — all happen there. The `Tasks/active/`, `Tasks/inbox/`, `Tasks/archive/` folders are internal scheduling state that I maintain. The user does not curate folders directly.

**Directionality:**
- **Read direction:** User edits daily → I reconcile folders to match (sweep ticks to archive, remove items the user deleted, respect manual additions).
- **Write direction:** When I capture/dump/move tasks → I also update today's daily so the user sees the change immediately.

**Rules:**
1. **Before any capture/dump/move:** read today's `task-land/Daily/<today>.md` first. Treat it as the current source of truth for what's on the user's plate.
2. **After any capture/dump/move:** reflect the change into today's daily — add new items to Today (or Inbox section, per inbox/active rule from [[feedback_dump_dated_followups_to_inbox]]), so the user doesn't have to wait until tomorrow's `/daily` to see them.
3. **`/dump` specifically:** must refresh the daily as part of its run. Items dumped "for today" should appear in today's Today section. The user can then tick/edit there.
4. **Reconcile drift:** if folder state has diverged from daily (stale snapshot from earlier-in-day `/daily`), the refresh I do should resolve to match folder reality, with user `[x]` ticks preserved.

**Why:** Confirmed 2026-05-22 — user said: "daily is what i tweak myself (nothing else i want to tweak), so it should be the one you read to adjust your own scheduling system in the back." Without this, captures during the day are invisible to the user, and the daily silently drifts from folder reality, breaking trust in the system.

**How to apply:** Any flow that touches `Tasks/active/` or `Tasks/inbox/` (dump, capture, todo from /triage, future verbs) must also patch today's daily file. The `/daily` skill's idempotent-on-same-day rule still holds (it doesn't blow away user edits), but individual capture flows are responsible for inserting new items into the live daily as they happen.

Related: [[feedback_dump_dated_followups_to_inbox]], `/daily` skill at `C:\Users\Alessandro\.claude\commands\daily\SKILL.md`.
