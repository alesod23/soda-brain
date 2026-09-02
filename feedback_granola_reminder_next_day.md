---
name: feedback_granola_reminder_next_day
description: "/granola reminder surface_on must be SMART-inferred, never a fixed default"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 78548ccb-1d9b-4a84-9f2f-f49f5a65b069
---

`/granola`'s inferred follow-up task must have its `surface_on` **reasoned about per call — no fixed default** (neither the old "~1 week" nor a hardcoded "next day"). Decide it in priority order: (1) explicit instruction in the user's `/granola` invocation; (2) a timeframe stated/implied in the call's Next steps; (3) otherwise infer from the content — how time-sensitive and how soon the action is actually needed.

**Why:** `/granola` is fire-and-forget; the follow-up has to come back at the right moment — early enough not to go cold, not so early it nags for something distant. The user will usually specify timing in the prompt or the Next steps; when they don't, the skill figures it out. A rigid default (either direction) is wrong. (Caught 2026-06-17: a near-term taskforce-onboarding todo was parked +7 days when it should've surfaced next day; but the fix is smart inference, not a new fixed rule — the user explicitly rejected hardcoding "next day".)

**How to apply:** in the granola reminder step, reason about the surface date from the call. Also include `bucket: inbox` in the task frontmatter — the daily dashboard is bucket-driven ([[reference_daily_briefing]]); a task with no `bucket` won't render.
