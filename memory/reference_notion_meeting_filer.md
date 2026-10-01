---
name: reference_notion_meeting_filer
description: "Phone-recorded Notion AI Meeting Notes land as loose pages even with \"Default meetings database\" set; the laptop task Notion-MeetingFiler (every 60 min, headless haiku + Notion MCP) moves them into the Meetings data source"
metadata: 
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-07T00:01:35.945Z
---

**Fact (verified 2026-09-06/07):** Notion AI Meeting Notes started from the phone app's "New Meeting Note" are created as standalone pages, NOT rows of the Tundra Meetings database, even after Alessandro set Settings > Notion AI > "Default meetings database" = Meetings. Laptop notes started from the database's New button land correctly. Notion custom-agent triggers are database-scoped, so no Notion agent can see the strays.

**Fix in place:** laptop scheduled task `Notion-MeetingFiler` (every 60 min, `wscript //B` on `~/.claude/scripts/notion-meeting-filer-hidden.vbs` -> `notion-meeting-filer.ps1`). It runs `claude -p --model haiku --strict-mcp-config --mcp-config notion-meeting-filer.mcp.json` (the Notion HTTP server only, so the Telegram plugin never loads; `TELEGRAM_STATE_DIR` pointed at telegram-null) with the procedure in `notion-meeting-filer.prompt.md`: `notion-query-meeting-notes` (past 3 days) -> `notion-fetch` each unseen note -> read `<ancestor-path>` -> `notion-move-pages` the PARENT page into data source `3a3b30c6-d57e-8093-9e35-000b79676b41` unless it is already in Meetings, is a row of another database, or sits under Thesis / supervisor chats / lobbly convos. Checked urls are kept in `notion-meeting-filer.state.json` (200 max) so each note is fetched once (a fetch pulls the whole transcript: first run cost $0.19 for 8 notes, steady state about $0.03). One line per run in `notion-meeting-filer.log`; a move posts ONE hub card (`http://100.85.52.84:4180/pending`).

**Limits / how to apply:** laptop only (the box's headless claude has no Notion tools under `--strict-mcp-config`, and a non-strict `claude -p` on the box would load the Telegram plugin and steal the bot token). A note recorded while the laptop is off is filed at the next wake. Moved rows still get completed by the Notion `Call Intake` agent (Date empty = unprocessed). `ReadToEnd()` on both stdout and stderr of the claude process deadlocked (hung 5 min): stderr is not redirected. See [[reference_notion_tundra_system]], [[feedback_verify_agent_capability_claims]].
