---
name: reference_daily_campaign
description: "The daily US campaign (2026-09-25): 30-person board a day, first 10 fire at 16:55 through campaign.py, research + next board afterwards; files, tasks, caps, what he asked."
metadata: 
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-25T10:23:12.535Z
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
- Research is a SCHEDULED task, never a session shell: `DailyCampaign-Research` every 20 min (17:00-24:00 for
  the next day, 08:00-16:20 for today) runs `supervise.py` = one round of 2 hidden Sonnet workers x 80 min
  while the day is short of 30 (`daily-state.json`), then `review.py`, then the board; IgnoreNew + the next
  trigger = the "safety mechanism that brings it back up" he asked for after Claude Code's memory guard
  killed the first run (2026-09-25 02:00, 2.4 GB free).
- Who fires (`pick.py`, his rulings 2026-09-25): his "a" pins; then 6 clinical engineering + 2 IT + 1
  procurement + 1 executive by rank; one hospital per day and 2 days between two people of one hospital;
  max 2 mailboxes; no age penalty in the rank.
- TRIMEDX review ("TriMatics" in his transcript): after each round, current affiliation = hospital swapped
  out, past = signal kept; rows in `competition.json` and the Notion database **Competition > TRIMEDX-
  affiliated hospitals** (page 3e6b30c6-d57e-8135-a67c-e81651d01d73, data source
  2cdbc0d0-de27-4681-9132-b9e0ec8a6be6, created 2026-09-25 as a private draft). Every card has a TRIMEDX bullet.
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
