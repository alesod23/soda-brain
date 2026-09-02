---
name: reference-wa-scheduled-sends
description: Pattern for future-dated WhatsApp sends — guard script + Task Scheduler in wa-daemon/scheduled-sends/
metadata: 
  node_type: memory
  type: reference
  originSessionId: b75b1302-8e9b-4e42-b796-f57031e2eebf
---

Future-dated WA sends live in `C:\Users\Alessandro\.claude\wa-daemon\scheduled-sends\` (first: `bea-20260726.*`, fires 2026-07-26 09:42 UTC to Beatrice UR).

Pattern: message body in a UTF-8 `.txt` (send.js `--text-file`), an ASCII-only `.ps1` guard that sends only when `nowUtc >= targetUtc` (timezone-proof if the laptop travels), state-file idempotency, self-deleting Task Scheduler task. Task triggers: once-at-date repeating /15min for 48h + AtLogOn catch-all; settings `-StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries` (see [[feedback_sodanotif_battery_power_task_setting]]). Verify with a guard dry-run (exit 0, no state file) + send.js dry run before registering.
