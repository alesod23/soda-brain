---
name: reference_daily_campaign
description: "The daily US campaign (2026-09-25): 30-person board a day, first 10 fire at 16:55 through campaign.py, research + next board afterwards; files, tasks, caps, what he asked."
metadata: 
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-25T00:01:04.932Z
---

**Daily campaign (US), built 2026-09-25 on his order** ("finding emails of people to contact, giving them to
me as a daily review, then firing the first 10 of those 30 email drafts, which i may or may not have reviewed,
doesnt matter, will still fire ... 10 emails daily"). Code: `~/gtm-eng/daily-campaign/` (README there),
workplan `~/gtm-eng/WORKPLAN-20260925-daily-campaign.md`.

- Task `DailyCampaign-Fire` 16:55 Rome (wscript + `daily-campaign-hidden.vbs`) runs `fire.py`: first 10 of
  `boards/daily-<today>` not skipped (his edited text and note win, max 2 department mailboxes) -> commit ->
  `campaign.py plan` (`board.campaign.per_day_email [10,10]`, contacts to CRM + Notion first, ledger) -> the
  10-min tick sends inside 08:00-17:00 PT from alessandro@tundrahealth.ai; one 📋 update card; then
  `research.py` (2 hidden Sonnet workers x 60 min, exclusions = CRM + Notion snapshot + every board + pool)
  -> `pool.json` -> `build.py --open` for the next business day (Opus emails via `draft.js`, drafting skill
  inlined, observer hits in `rule-hits.jsonl` path daily-campaign). Weekends: research only.
- His rules in code: subject exactly "Quick question on clinical engineering in your hospital (<name>)"
  (email rule H65); one sentence naming the reader's CMMS/OEM (Caleb's Nova/waveware move), GE HealthCare
  as the example when nothing is known; people not offices (mailbox max 4/30 researched, 2/10 sent);
  addresses only published or SMTP-valid.
- Caps: `campaign.py EMAIL_HARD` 20/day across campaigns (Caleb). While the 114-wave (`us-campaign-emails`,
  built 2026-09-24 by the privati-nord session) runs, the daily 10 take what is left and slide a day.
- Daily page: the third mirror line is now `Daily campaign: 30 to review, 10 fire at 16:55 (N reviewed)`
  and REPLACED "Urgent GTM boards" (his ruling). Boards carry a favicon by kind (daily = calendar).
- Notion Contacts vs CRM (checked 2026-09-25): US universe fully mirrored; only-in-Notion = Caleb's 8
  German rows + 23 warm US ecosystem people; only-in-CRM = 107 French cold-call rows. Snapshot of the 308
  Notion names in `daily-campaign/notion-names-snapshot.json` (refresh when Caleb adds people).

**How to apply:** never a third send engine; a new campaign is a board + `campaign.py plan`. Any scheduled
console task goes through a `.vbs` (see [[reference_interactive_console_tasks_open_windows]]). Related:
[[reference_gtm_boards]], [[reference_rule_loop]], [[feedback_cold_email_operator_ask_for_advice]].
