---
name: feedback_email_not_findable_tracking
description: "coattio must record when a contact's email couldn't be found/is unusable, and how/where it was tried — this gates email-vs-call"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6c32b433-096b-4c00-9d06-03e5f167f558
---

In coattio's outreach model, **"à appeler" (call-only) is the exception, not the default** — most contacts should be BOTH *à emailer* AND *à appeler*. A contact is **call-only** in exactly two cases:
1. The email is **proven unusable**: `email_status` = invalid (none) OR verified-catch-all-without-result — we won't risk sending to those.
2. An **email was already sent** (touch2 sent) — then the escalation is the call.

**Why:** the user wants email+call offered together (the À faire column shows phone + email icons, multiselect), and only drops email when it's impossible or done.

**How to apply / TODO (not yet built):** the system MUST capture when an email **could not be found** after an attempt — a distinct state (not just "empty email"), plus **how/where it was searched** (e.g. Hunter no-result, Apollo unverified, catch-all domain). Surface that provenance in the appropriate column (the `contact_source` note already exists — extend it: on a failed email hunt, stamp "email introuvable — tenté via Hunter/Apollo le <date>"). Then `contactReadiness`/nextAction treat "email tried-and-failed" as call-only, distinct from "email not yet tried" (still à enrichir). Ties to [[reference_tundra_crm_taxonomy]] (graded `email_status`) and [[reference_outreach_system]].
