---
name: reference_claude_bar
description: claude-bar — CodexBar-style Windows tray app showing Claude Code plan usage (5h/weekly %) from the OAuth usage endpoint; autostarts at logon.
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4c7dee00-4d73-4594-a62e-6b10986085b6
  modified: 2026-07-31T03:07:57.433Z
---

`C:\Users\Alessandro\.claude\claude-bar\` — Windows system-tray equivalent of macOS CodexBar, built 2026-07-30.

- `claude-bar.ps1` (WinForms NotifyIcon, ASCII-only, singleton mutex `Local\ClaudeBarTray`). Tray icon = 5h-session % as colored digits (white <50 / gold / orange / red ≥90) + 3px bottom strip = weekly fill. Menu: 5h + weekly + model-scoped weekly with reset countdowns, live context-% of running CC sessions (read from the statusline's `%TEMP%\claude-ctx-*.json` bridge files, <15 min fresh — see [[reference_gsd_statusline]]), Refresh, open claude.ai usage page, log, Exit. Balloon warnings crossing 75%/90%.
- Data: `GET https://api.anthropic.com/api/oauth/usage` with `Authorization: Bearer <accessToken from ~/.claude/.credentials.json .claudeAiOauth>` + header `anthropic-beta: oauth-2025-04-20`. READ-ONLY on the credentials file; on 401 shows "token expired - run any claude turn" (Claude Code refreshes the token itself; never write .credentials.json).
- Launch: `claude-bar.vbs` (wscript, hidden — per [[feedback_schtasks_vbs_wrapper_no_console_flash]]); copy installed in `shell:startup`. Kill/restart: find powershell with CommandLine matching `claude-bar.ps1`, or Exit from the tray menu.
- Poll: 5 min timer + on-menu-open refresh if stale >2 min. Log: `claude-bar.log` in the same folder.
