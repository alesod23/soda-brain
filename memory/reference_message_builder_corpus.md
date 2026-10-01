---
name: reference-message-builder-corpus
description: Passive sent-message corpus + /message-builder skill; the daily SentCorpus-Harvest task is USER-AUTHORIZED and local-only
metadata: 
  node_type: memory
  type: reference
  originSessionId: e52f35cb-8a2a-44d8-94e9-b5830f08839e
---

Passive "how Alessandro communicates" system, built 2026-07-21 (session "GTM eng").

- **Corpus:** `C:\Users\Alessandro\.claude\sent-corpus\corpus.jsonl` — append-only, one row per SENT message `{ts,date,channel,recipient,recipient_context,lang,topic_tags,register,text,thread_id,source}`. Seeded from mined Tundra pitch blurbs (registers: exploratory<realistic<visionary).
- **Harvester:** `harvest.js` (+ `harvest.vbs` hidden launcher, `state.json` per-channel cursors) pulls new sent messages from Gmail (cdtm+tundra via `~/triage/gmail.py`), WhatsApp (`wa-daemon/message-store.jsonl` fromMe), Slack cdtm (`slack.py`, filter `from:@alessandro.sodano`). LinkedIn = phase 2 (MCP not cron-scriptable). xplore Slack token expired = skipped.
- **Schedule:** daily 07:30 task **`SentCorpus-Harvest`** (interactive/logged-in only). **This standing automation is AUTHORIZED by Alessandro** (he asked for a passive monitor recording ALL sent messages, plugged into his triage tools). It is LOCAL-ONLY (nothing transmitted). Do NOT flag it as unauthorized persistence or disable it without asking. To pause: disable the task.
- **Consumer:** the `/message-builder` skill (`~/.claude/commands/message-builder/SKILL.md`) reads the corpus to draft ANY message in his voice (retrieve→infer→draft→self-review). Pitch blurbs are ONE lens; never assume Tundra. Audience→register: investor=visionary, referrer/clinical-engineer=realistic, cold expert=exploratory.
- First run only grabbed ~last 2 days + seed; deep history can be backfilled by lowering a cursor in `state.json`. Related: [[project_gtm_v3_stack]], [[reference_outreach_system]].
