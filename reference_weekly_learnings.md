---
name: reference-weekly-learnings
description: "Curriculum tracker has a 'weekly learnings' layer at localhost:4117/weekly. Friday 19:30 cron pulls CDTM Engineering WA group + Alessandro's session transcripts. In-session push via /save-learning."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3e5af996-141e-4b40-9706-35240255faf4
---

# Weekly Learnings layer (curriculum tracker)

URL: **localhost:4117/weekly**

Three input streams roll up into one weekly digest, keyed by ISO week
(e.g. `2026-W21`):

1. **CDTM Engineering WhatsApp crawl** (pull). `crawl-wa.mjs` calls
   `wa-daemon/search.js --chat 120363071370133642@g.us --days 7 --json`,
   LLM-classifies messages against active curriculum topics (status `[~]`
   or `[x]`), writes results.
2. **Personal session crawl** (pull). `crawl-sessions.mjs` walks
   `~/.claude/projects/C--Users-Alessandro/*.jsonl` from the last 7 days,
   builds a per-session digest (user prompts + first assistant turn),
   classifies against active topics.
3. **Saved moments** (push). `/save-learning` skill POSTs to
   `localhost:4117/api/save-moment` and the moment appears in that week's
   digest. See [[save-learning skill]](../../../commands/save-learning/SKILL.md).

## Schedule

Windows Task Scheduler entry **`Curriculum-Weekly-Crawl`** runs
`C:\Users\Alessandro\.claude\curriculum-server\weekly-crawl.ps1` every
Friday at 19:30 local. Logs land in
`C:\Users\Alessandro\.claude\curriculum-server\logs\weekly-*.log`.

To stop / change cadence:
```powershell
Get-ScheduledTask -TaskName "Curriculum-Weekly-Crawl"
Unregister-ScheduledTask -TaskName "Curriculum-Weekly-Crawl" -Confirm:$false
```

## Files

- `C:\Users\Alessandro\.claude\curriculum-server\crawl-wa.mjs`
- `C:\Users\Alessandro\.claude\curriculum-server\crawl-sessions.mjs`
- `C:\Users\Alessandro\.claude\curriculum-server\lib\topics.mjs` (extracts active topics from the curriculum HTML)
- `C:\Users\Alessandro\.claude\curriculum-server\lib\classify.mjs` (gpt-4o-mini batch classifier)
- `C:\Users\Alessandro\.claude\curriculum-server\lib\weekly-store.mjs` (sidecar JSON read/write + ISO week helpers)
- `C:\Users\Alessandro\.claude\curriculum-server\weekly.html` (the view)

## Storage

Sidecar JSON at
`C:\Users\Alessandro\OneDrive - HEC Paris\learning\fullstack-curriculum-weekly.json`.
Curriculum `.md` / `.html` source files stay untouched.

## Server endpoints

- `GET /weekly` — serves the view
- `GET /api/weekly?week=YYYY-Www` — JSON for a week (default current)
- `POST /api/weekly/refresh` — runs both crawlers, returns when done
- `POST /api/save-moment` — appends a push into `saved_moments_inbox`

Related: [[feedback_curriculum_tracker]] (the broader tracker workflow),
[[reference_wa_sender]] (wa-daemon search/send), [[reference_onedrive_path]].
