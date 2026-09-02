---
name: feedback-future-due-to-inbox
description: "Tasks split deadline (`due`) from surface day (`surface_on`). /dump must parse surface intent from natural language; /daily honors surface_on (falls back to due). Deterministic \"surface on due date\" was too rigid — user almost always tells you when they plan to work on something separately from the deadline."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d776269f-9804-404b-ba29-e15dd5cf58fd
---

**The two fields:**
- `due:` — the hard deadline. When the world demands the work is done.
- `surface_on:` — the day the task should appear on the daily page's `## Today` section. When the USER plans to actually do the work.

These are usually different. The user almost always signals both in a dump.

**Engine rule (across every flow):**

For each task, `effective_surface_date = surface_on || due || today`.
- `effective_surface_date <= today` → lives in `Tasks/active/`, appears on Today.
- `effective_surface_date > today` → lives in `Tasks/inbox/`, hidden from Today until that date.

/daily migrates files between active/ and inbox/ each morning based on this rule. /dump must set `surface_on` from inferred intent (the harder, more important job).

**Why this matters (don't be lazy on /dump):**

The user is paying a context tax every time I shoehorn a dump into a deterministic default. The deadline alone is rarely the right surface day — surfacing on the deadline either creates last-minute panic or, if I default to "deadline = surface_on", buries the user in irrelevant Today noise on the day the work needs to be finished. The whole point of `/dump` is "I tell you the plan once, you handle it." Parse the intent.

**Phrases to parse for `surface_on` (non-exhaustive):**

| Verbal cue | Surface date |
|---|---|
| "do it that weekend" + deadline = Mon | Saturday before |
| "tackle it on Wednesday" | that Wednesday |
| "look at it after X" (where X has a date) | day after X |
| "remind me about this on the 15th" | the 15th |
| "draft the deck the weekend before the event" | Saturday 2 weeks before event |
| "next week" | next Monday |
| "blocked on Y, check back when…" | the unblock date |
| "for X event in 3 weeks, prep the weekend before" | the Saturday before |

**When to ask vs infer:**
- Strong verbal cue → infer, set `surface_on`, capture verbatim phrase in the task body so the user can audit.
- Deadline-only with no temporal cue ("submit by June 1st." period) → leave `surface_on` empty; /daily falls back to `due`. The user can always add a `⏳` defer line later.
- Genuinely opaque ("I should do something about X someday") → no `surface_on`, no `due`, file to inbox, don't ask. Bias to capturing.
- **Never ask per item in /dump.** Dump is a one-shot batch. If multiple items are unclear, default to inbox and surface a one-line "you may want to clarify surface dates for: X, Y" at the end.

**Manual override (always wins):**
- User drags an inbox line to Today on the daily page → /daily honors it.
- User ticks a future-dated active task → /daily syncs as done.
- User writes `⏳ YYYY-MM-DD` next to a task on the daily page → sets `defer:` which hides from Today (separate mechanism from `surface_on`, but same spirit).

**History:**
- 2026-05-24 morning: I put two future-due tasks (ltc-prep due +2, write-to-marc-langfuse due +10) on Today. User caught it. Locked v1 rule: "future-due → Inbox, auto-promote on due date".
- 2026-05-24 afternoon: User pushed back — too deterministic. EF/EWOR dump already contained surface intent ("should probably do the application that weekend") that I ignored. Locked v2 rule: separate `surface_on` from `due`; /dump must parse intent; /daily migrates based on `surface_on`.

Related: [[feedback_dump_dated_followups_to_inbox]] (predecessor — same family, narrower scope).
