---
name: feedback_found_contact_details_go_to_crm
description: "Found emails reach the CRM through the 23:00 sweep RAKE (sent mail + drafts scanned, one approval card, he approves), NOT through a per-session 'post it when you find it' workflow; that idea was given and retracted the same day (2026-09-20). POST :4137/enrich-result exists only as the apply step for rows he approved."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-20T14:46:00.796Z
---

**What he ruled (Telegram 2026-09-20 14:55, relayed by the savior), reversing his own earlier instruction:** "Ho dato un'istruzione sbagliata ... Non creiamo un workflow separato." No pipe that fires when he asks a session for someone's address. The truth is what he produces anyway: **Gmail drafts and sent mail**. A **rake** ("rastrello") inside the **23:00 EOD sweep on the box** reads the day's sent mail and drafts across the four accounts (`triage/gmail.py search --account <cdtm|tundra|sodano23|lobbly> --query "in:sent newer_than:1d"`, `list-drafts`), pulls out addresses of CRM people whose row has no email, and proposes them **as lines inside the sweep card, not a card of their own** ("tra le varie cose di quelle 11 di sera c'e' anche questa"). Nothing is written silently: "io mi faccio il bottleneck". Same shape as `triage/contacts_sync.py` (one card per batch, yes = all, no + numbers = those, no + nothing = skip). Rule behind it (his memory `feedback_output_goes_into_the_owning_system`): the result goes into the system that owns that work, people belong to coattio, decisions to the hub, no new surface.

**What stays from the retracted version:** `POST http://127.0.0.1:4137/enrich-result {field, value, status, source, pid|linkedin|name(+company), session, dry_run}` in `intake-server.js` (commit 8f857aa), the single-writer apply step: sets `p.email`/`p.email_status` (or `p.phone`), ticks `enrich.<field>.claude`, dated note + activity, closes queued enrich-queue jobs; 404 for an unknown person, never creates a row. The rake calls it for the rows he approved (from the box through the intake proxy). Sessions do NOT call it on their own; the Quick Claude workspace instruction to do so was removed.

**Status honesty for the rake:** an address he actually sent to = `verified`; one only in a draft = `inferred` until sent; an office address (segreteria) = `published` with `personal:false`.

**Also learned that day:** the CRM "Enrich" button only writes `enrich-queue/<stamp>-<field>.json` and flips the box to "Queued"; nothing consumes the queue by itself (no task, no cron), it waits for a session to run `/overnight`. For one person a direct search in the session is faster (Giovanni Gorgoni, ASL Asti: no personal address published, `direzionegenerale@asl.at.it` = Segreteria di Direzione).

**How to apply:** do not build request-time hooks for contact details; when the rake exists (box side, eod_sweep.py), its approved rows flow through `/enrich-result`. See [[project_coattio_v2]], [[reference_contacts_sync]], [[reference_overnight_email_find]].
