---
name: reference_interactive_console_tasks_open_windows
description: "Random terminal windows that appear and stay" = a Task Scheduler task whose action is cmd.exe/python/node directly in his interactive session; wrap every console task in a .vbs run by wscript.exe. Diagnosed 2026-09-25 (GTM-Campaign-Tick).
metadata:
  type: reference
---

**Symptom (his words 2026-09-25):** "I am starting to see random terminal windows appear again and just stay."
A Windows Terminal window titled `C:\WINDOWS\system32\cmd.` with only a cursor.

**Cause found:** the task `GTM-Campaign-Tick` (registered 2026-09-24 by another session) ran
`cmd.exe /c python campaign.py tick --all >> log` every 10 min with `Interactive only` logon: every fire
opened a console window in his session (Windows 11 "Let Windows decide" = Windows Terminal hosts it), the
tick sleeps up to 10 min to hit its drawn second so the window stayed, and closing it killed the tick
(campaign-tick.log `^C^C^C`, LastTaskResult 0xC000013A). Fixed: action = `wscript.exe //B //Nologo
campaign-tick-hidden.vbs` (`sh.Run "cmd.exe /c ...", 0, True`), same as `system-check-hidden.vbs`,
`start-intake.vbs`, `run-watchdog-hidden.vbs`.

**How to diagnose next time (one command):** `Get-ScheduledTask | % { $_.Actions }` filtered on
`Execute -match 'cmd|python|node|powershell'` with `Principal.LogonType Interactive`; or list live
`cmd.exe` via `Get-CimInstance Win32_Process` with parent name and CreationDate (mind the DATE, not just
the time). Headless `claude.exe` from hidden-claude.js is NOT the cause (wscript Run(...,0) hides it).

**How to apply:** any new scheduled task that runs a console program gets a `.vbs` launcher; never
`New-ScheduledTaskAction -Execute cmd.exe`. See [[reference_daily_campaign]], `index_laptop_and_misc` (schtasks VBS).
