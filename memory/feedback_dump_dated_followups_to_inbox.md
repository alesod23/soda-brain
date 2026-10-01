---
name: feedback-dump-dated-followups-to-inbox
description: "For /dump, future-dated follow-up checks go to Tasks/inbox/ not Tasks/active/, even though the dump skill says reminders → active"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: dcb4b264-a788-4271-a6cc-87bdb34ca2e4
---

When `/dump` produces a future-dated check / follow-up task (e.g. "wait until Tuesday, then check if X accepted"), file it to `Tasks/inbox/` — NOT `Tasks/active/` — even though it has a due date.

**Why:** `active` means "I am actively working on this now." A follow-up that's gated on a future date isn't active work — it's queued, waiting for time to pass. The user's mental model treats `active` as "in-flight" and `inbox` as "queued / not started", regardless of due dates. Filing future checks to `active` clutters the active list with things you can't act on yet.

**How to apply:** In `/dump` (and any task-capture flow), when classifying a "wait until X, then do Y" item:
- Even though the dump skill table says reminders (action + date) → `Tasks/active/`, override that for the **wait-then-check** pattern → `Tasks/inbox/` with `--due <date>`.
- Heuristic: if the task can't be started today, it's inbox. If it can be started today and has a deadline, it's active.
- Confirmed 2026-05-22 after I filed the Tuesday Thomaier-referral acceptance check as active; user said it belonged in inbox.

Related: the `/dump` skill SKILL.md may want updating to reflect this. Don't edit it now — wait for user instruction.
