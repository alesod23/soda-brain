---
name: feedback_email_catchup_consistency
description: "SODANOtif email catch-up cards must render the SAME fields every run (date/time, type) — never drop details on a repeat; email side is being redesigned per WORKPLAN-email-deepdive.md."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6ae8a5d1-8ed7-4951-926a-c95e51082ad5
---

Alessandro's inbox catch-up (SODANOtif `recap.ps1` push) is **inconsistent and noisy on the email side**, flagged 2026-07-02. Durable rules:

1. **Rendering consistency (demanded "must not recur across sessions"):** the SAME item must show the SAME fields on every catch-up. Date/time appearing one run and vanishing the next is a bug. **Root cause:** the `claude -p` Haiku classifier improvises optional fields. **Fix pattern:** PRE-COMPUTE fields deterministically in PowerShell (like WA/Slack `_when` via `Fmt-Unix`) and have the classifier COPY verbatim + make them MANDATORY in the schema. Secondary guard: read the previous catch-up from `notification-log.jsonl` (keyed by thread id) and reuse prior rendering.
2. **Every email card needs date/time** (like Slack/WA cards).
3. **Type tag:** `event`/calendar vs `direct` email.
4. **Calendar noise filter:** NEVER surface pure "meeting accepted"/"meeting fixed for <date>" confirmations. ONLY show event emails that are (a) a NEW meeting/RSVP request from someone else, or (b) a meeting whose TIME CHANGED. Put those in a dedicated **"Calendar" catch-up section** (skimmable/skippable), separate from direct emails.
5. **Preference learning:** wants a "tinder swipe right/left + comment" mechanism (like trippy-v2's dueling context) to teach which emails matter.

**Why:** the email pipeline surfaces stuff he doesn't care about and renders unreliably. **How to apply:** full design + phased plan lives at `C:\Users\Alessandro\.claude\sodanotif\WORKPLAN-email-deepdive.md` — read it before touching the email catch-up. Related: [[reference_sodanotif]], [[feedback_sodanotif_card_format]], [[reference_lby_dead]], [[project_trippy_v2]].
