---
name: sodanotif-battery-power-task-setting
description: "Recurring bug: schtasks created with default 'Stop On Battery/No Start On Batteries' silently die when the laptop is on battery. Hit SODANOtif-Watch/Recap first, then Coattio-Watchdog. Always disable both flags on any always-on watcher task."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 833c9bca-1d56-4c13-a3c5-19bf926ee404
---

Found 2026-07-06: [[reference_sodanotif]]'s `SODANOtif-Watch` (5-min flagger) missed 10-11 consecutive scheduled runs (~50 min silent gap) around 18:25-19:16. `Get-ScheduledTaskInfo` showed `LastTaskResult: 0` (no error) but `NumberOfMissedRuns` climbing and `NextRunTime` stuck. Root cause: `schtasks /query /v` showed `Power Management: Stop On Battery Mode, No Start On Batteries` on the task, and Windows System event log (Id 105 "Power source change") recorded a power-source transition right at the start of the gap (18:27). A background bot notifier must never silently pause just because the laptop briefly ran on battery — that defeats the entire point of an always-on watcher.

**Fix applied:** `Set-ScheduledTask` with `Settings.DisallowStartIfOnBatteries = $false` and `Settings.StopIfGoingOnBatteries = $false` on both `SODANOtif-Watch` and `SODANOtif-Recap`.

**How to apply:** If a scheduled background task (SODANOtif or any future always-on watcher/daemon task) appears to have silently stopped firing with no error in its own log, check `schtasks /query /tn <name> /v /fo list` for `Power Management` settings and cross-reference `Get-WinEvent -FilterHashtable @{LogName='System'; Id=105,106}` for a power-source-change event around the stall start. Any task meant to run continuously regardless of power state should have both battery-power flags disabled from the moment it's created — add this check to any future `schtasks /create` for a background watcher.

**Recurred 2026-07-08** on `Coattio-Watchdog` ([[reference_coattio_servers]]): same two flags (`DisallowStartIfOnBatteries`/`StopIfGoingOnBatteries`) were `true` by default, and killed the coattio CRM/intake node servers whenever unplugged, which took the Tailscale-Serve phone proxy down with them (it just proxies to localhost). Fixed the same way via `Set-ScheduledTask`. **Confirmed pattern: `schtasks /create` defaults these flags to `true`** — any new always-on watcher task must have them explicitly disabled at creation time, don't wait to discover it via an outage.
