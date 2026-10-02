---
name: reference_claude_bar
description: claude-bar — CodexBar-style Windows tray app showing Claude Code plan usage (5h/weekly %) from the OAuth usage endpoint; ClaudeBar task relaunches it every 5 min + logon + unlock (self-healing since 2026-09-28).
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

**Why it vanished, and how to relaunch (2026-09-18):** the bar died on 2026-09-15 17:39, right after a session restarted it with `Start-Process powershell ... -File claude-bar.ps1` from a tool shell: processes spawned from a tool shell are reaped when that shell ends (same class as feedback_local_server_start_pattern). It stayed dead for three days because nothing relaunches it between logons. Fix: scheduled task **ClaudeBar** (logon trigger, runs `wscript claude-bar.vbs`, no time limit, battery allowed). A session relaunches it with `Start-ScheduledTask ClaudeBar` (detached, survives the shell), never with Start-Process. The Startup-folder vbs still exists; the mutex `Local\ClaudeBarTray` makes the second copy exit, so a double start at logon is harmless. Alive check: `Get-CimInstance Win32_Process | ? CommandLine -match claude-bar.ps1` and a "claude-bar started" line in claude-bar.log.

**Self-healing since 2026-09-28 (his ask: "ensure it doesn't reoccur"):** it died AGAIN on 2026-09-23 17:40 (killed hard: no
"exited"/"fatal" log line) and stayed dead 5 days, because the logon trigger only fires at a real logon and he mostly
sleeps/wakes. The ClaudeBar task now has three triggers: logon, every 5 min indefinitely, and session unlock;
MultipleInstances IgnoreNew, StartWhenAvailable. A launch while it runs exits at once on the mutex (verified: 1 process
after a second start). So a dead bar comes back within 5 min with no session involved. Never remove the repeat trigger.

**The ".NET Framework: Unhandled exception ... Cannot process argument transformation on parameter 't'. Cannot convert
null to type System.DateTime" dialog = claude-bar (fixed 2026-10-02).** `Fmt-Countdown([datetime]$t)` converted its
argument before the null guard ran; resets_at is null right after a usage window resets, and the throw came from the
5-min timer handler (unguarded), which WinForms turns into that modal dialog. Now: untyped param, `Fmt-At` for the menu
times, and every refresh goes through `Refresh-Safe` (try/catch -> `refresh error:` in claude-bar.log). Rule for any
WinForms .ps1: never type a param that can be null, never call a handler body without try/catch.
