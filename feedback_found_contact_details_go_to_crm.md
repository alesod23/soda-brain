---
name: feedback_found_contact_details_go_to_crm
description: "When any session (Claude Code, Quick Claude, Telegram/savior) finds a person's email or phone for him, report it to the CRM with POST :4137/enrich-result so the row says 'found by Claude'; the Enrich button only queues a job file that nothing runs on its own (2026-09-20)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-20T12:35:37.788Z
---

**Rule (his question, 2026-09-20): "if i ask somewhere else on a claude session / qc / tg that i want to have his email to write him, then can you update this CRM? meaning it updates that we found the email through claude afterwards?"** Yes, and it is one call. Whenever an email or phone is found for a CRM person, in any session, before drafting:

```
POST http://127.0.0.1:4137/enrich-result
{"field":"email","value":"x@y.z","status":"published","source":"<url>","name":"<full name>","company":"<org>","session":"<where>"}
```
(`pid` or `linkedin` instead of `name` when known; `dry_run:true` to preview; `field:"phone"` works the same.) The intake server resolves the person, writes `p.email` + `p.email_status` (or `p.phone`) through the CRM's single writer, ticks `enrich.<field>.claude = true`, appends a dated note with the source, an activity line, and marks any queued enrich-queue job for that person done. Unknown person = 404, never a new row. From the box the same route goes through the box's intake proxy (`127.0.0.1:4137` there) while the laptop answers.

**Status honesty:** `published` = printed on a page fetched; `inferred` = a pattern guess (never promote to verified); `verified` only with evidence; `none (introuvable)` when nothing was found. An office address (segreteria, direzione) is `published` with `personal:false` and the note says so (Giovanni Gorgoni, ASL Asti: `direzionegenerale@asl.at.it`, 2026-09-20).

**Why:** the CRM "Enrich" button only writes `enrich-queue/<stamp>-<field>.json` and flips the box to "Queued"; NOTHING consumes that queue by itself (no task, no cron): it waits for a session to run `/overnight` on the job file. For one or two people a direct search in the session is faster than the harness; either way the result has to land in the row or the Missing-email list lies.

**How to apply:** any session that looks a contact up (for a draft, a call, a board) ends with this POST; the Quick Claude workspace CLAUDE.md carries the same instruction; the savior (box) uses it too. See [[project_coattio_v2]], [[reference_overnight_email_find]].
