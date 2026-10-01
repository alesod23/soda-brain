---
name: reference_wa_daemon_creds_corruption
description: "Unclean shutdown zeroes wa-daemon auth/creds.json -> silent 408 reconnect loop forever; how to spot it in 30s, restore without re-pairing, and the guards now in daemon.js"
metadata: 
  node_type: memory
  type: reference
  originSessionId: f85a7d71-844e-4c73-90eb-29b50d9924f5
  modified: 2026-08-06T17:54:20.868Z
---

**The 2026-08-06 outage.** WA sends failed with `HTTP 500: Cannot read properties of undefined (reading 'id')`. Daemon logged `disconnected (code=408 connectionLost)` every ~170s for 5 hours. `/health` said `connected:true`. Network fine, single daemon, creds "present".

**Root cause: `auth/creds.json` was 2859 bytes of pure NUL.** Kernel-Power event 41 (`system rebooted without cleanly shutting down`) at 12:43; the file's directory entry kept its size but the data never flushed. Baileys' `useMultiFileAuthState` writes non-atomically, so a power loss mid-write zeroes it. Only 1 of 4255 auth files was hit.

**30-second diagnosis** (do this BEFORE theorising about network/wifi/duplicate daemons):
```powershell
$b=[IO.File]::ReadAllBytes("$env:USERPROFILE\.claude\wa-daemon\auth\creds.json"); @($b -ne 0).Count   # 0 = corrupt
Get-WinEvent -FilterHashtable @{LogName='System';ProviderName='Microsoft-Windows-Kernel-Power'} -MaxEvents 20 | ? Id -eq 41
```
Scan the whole dir fast with one pass: `Get-ChildItem auth\*.json | %{ $b=[IO.File]::ReadAllBytes($_.FullName); if(@($b -ne 0).Count -eq 0){$_.Name} }`. NEVER loop per-file in bash with `tr`/`wc` (4255 files, times out).

**Recovery without re-pairing:** copy a valid `creds.json` back and restart. Worked from a 6-week-old OneDrive `_LAPTOP-BACKUP` copy because the device registration (`393459764713:51`) was unchanged. Only re-pair (see [[reference_wa_daemon_repair]]) if the restore yields `401 loggedOut`.

**Guards added to daemon.js 2026-08-06** (verified working):
- Startup now `JSON.parse`s creds.json; if corrupt it auto-restores from `auth/creds.json.bak`, else exits loudly instead of 408-looping. Previously it only did `existsSync`, which a zeroed file passes.
- `backupCreds()` snapshots a known-good `creds.json.bak` on every successful `connection === 'open'` (temp file + `renameSync`, atomic on NTFS).
- New `waOpen` flag. `currentSock` is assigned when `makeWASocket()` RETURNS, before the handshake, so it was never a readiness signal. `/health` now returns `connected: waOpen` plus `socket:` for debugging, and `/send` + `/resync` refuse with a clear 503 instead of dying on `sock.user.id`.

**Second failure, equally important:** `WA-Daemon-Watchdog` never ran during the outage. It had `DisallowStartIfOnBatteries=True` / `StopIfGoingOnBatteries=True`, and he was travelling on battery. Same defect found and patched on `SentCorpus-Harvest`, `SNM-Receiver`, `Trippy-Requests-Watch`. This is the same class of bug already fixed once for SODANOtif, see [[feedback_sodanotif_battery_power_task_setting]] — **when creating ANY scheduled task, set AllowStartIfOnBatteries + DontStopIfGoingOnBatteries + StartWhenAvailable**, because this machine is a laptop that travels.

See [[reference_wa_daemon_health]], [[reference_wa_sender]].
