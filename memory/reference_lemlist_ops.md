---
name: reference_lemlist_ops
description: "lemlist API ops learned building Tundra campaigns — multi-campaign is free, per-lead constraints, launch/move limits"
metadata: 
  node_type: memory
  type: reference
  originSessionId: eb5345ef-3949-4955-99e7-d2f934030b28
---

lemlist operational facts (learned 2026-07-01 building Tundra outbound campaigns via the REST API, key in `C:\Users\Alessandro\dev\cdtm-gtm-engine\.env` LEMLIST_API_KEY; base `https://api.lemlist.com/api`, Basic auth empty-user + key, needs browser User-Agent or Cloudflare 403).

- **Multiple campaigns cost NOTHING extra.** Campaigns are unlimited on any plan; cost = plan (per seat/mo) + credits (email find/verify, per-lead once) + sending. So ALWAYS free to split into separate campaigns for different workflows (e.g. email-direct vs LinkedIn-first). Sending caps (trial ~50 email/day, LinkedIn ~20-25 invite/day) are ACCOUNT-level, shared across campaigns (splitting doesn't add throughput).
- **A lead/contact can be in only ONE campaign at a time.** Adding a lead already in another campaign → HTTP 500 "Lead already in other campaign".
- **API cannot MOVE a lead between campaigns.** DELETE `/campaigns/{cid}/leads/{email}` only *unsubscribes* (soft; needs an email or 404 "An email is required to unsub a lead"), lead stays "scanned"/associated. Deleting by leadId doesn't work. Full remove/move = UI only.
- **API cannot LAUNCH a draft campaign.** New/never-launched campaigns sit status "draft"; no working launch endpoint (`/start` says "already running" but stays draft; `/launch`,`/run` = 405). First go-live is the UI "Review and launch" button (needs a schedule assigned too). After first UI launch, API `/campaigns/{id}/pause` + `/start` can pause/resume.
- **Step delay is WHOLE DAYS only** via API (fractional/minute delays → 400). Minute/hour delays (e.g. "17 min after accept") are UI-only. Invitation note char cap: lemlist warns 200 though LinkedIn Premium allows 300; API stores up to 300 but UI may flag.
- **Custom variables** (e.g. `{{hook}}`): set them by PATCH `/campaigns/{cid}/leads/{leadId}` with the field (lead PATCH accepts arbitrary custom keys; step PATCH rejects unknown fields). Lead POST with the field also works. companyName + custom vars live on the LEAD, not the contact.fields.
- **Conditional/branch sequences** (fix the "message before accept bounces" warning): POST step `{type:"conditional", conditionKey:"linkedinInviteAccepted", delayType:"within", delay:<days>}` → returns `conditions[]` with an "Accepted invite" branch sequenceId + a `fallback:true` branch sequenceId. POST steps to each branch's `/sequences/{seqId}/steps`. Accepted branch = LinkedIn message; fallback branch = email. Condition keys incl: hasEmailAddress, hasLinkedinUrl, linkedinInviteAccepted, emailsOpened, meetingBooked, etc.
- **File-based scripts, not inline heredocs**, for anything with French/accented text — the block-destructive Bash hook chokes on inline accented heredocs; running `python <file>.py` (venv/py312) is clean. Read files with `encoding="utf-8"` (the lemlist push script's bug: it read the steps file as cp1252 → mojibake).
- Reset lemlist port/CRM note: the medtech CRM has its own live server (see [[reference_medtech_crm_sync]]).
