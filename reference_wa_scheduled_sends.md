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

**BOX TWIN (2026-09-11):** the same pattern now exists on the VPS, in the same folder
`/home/da/wa-daemon/scheduled-sends/` (which also carries the laptop's synced `.ps1`/`.vbs`
files - ignore those there). Per send: `<name>.txt` body, `<name>.sh` guard (sends only when
`date -u +%s >= TARGET_UTC`, state-file idempotency, `send.js --jid --text-file --confirmed`,
self-removes its crontab lines on a "Sent" result), two crontab lines - the exact minute plus
a `*/15` catch-up window for ~2h. Always: `<name>.sh --dry` before arming (prints
would_send=yes/no + the send.js dry run). First use `caleb-20260911-0801` (08:01 CEST =
06:01 UTC, epoch 1789106460). Cron on the box runs in CEST; the guard compares UTC epochs so
the cron minute only needs to be at-or-after the target.
