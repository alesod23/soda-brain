---
name: reference-wa-daemon-health
description: "How to check whether the WA daemon is actually alive — heartbeat file and daemon_pid_alive, NOT triage.js's generated_at (which lies)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 5613f4ee-d778-418d-907a-3cbdcd94e11d
---

WA daemon health source-of-truth (post 2026-05-12 fix):

- **`~/.claude/wa-daemon/heartbeat`** — text file containing unix-ms timestamp. Daemon writes every 60s while WebSocket is open. Deleted on disconnect/exit. **Missing or stale >5 min = daemon disconnected.**
- **`~/.claude/wa-daemon/daemon.pid`** — the running node PID. Check liveness with `Get-Process -Id <n>` (PS) or `process.kill(n, 0)` (node).
- **`triage.js --json`** — emits `daemon_pid_alive` (bool) and `daemon_heartbeat_age_sec` (int|null). Always inspect these before trusting the items array.

**NEVER use `generated_at`** for daemon health — it's set fresh by `triage.js` every invocation regardless of daemon state. Caused a 34-hour silent WA outage on 2026-05-11 (daemon was dead but `generated_at` was always current, so the triage SKILL and `scan.ps1` thought WA was healthy).

The `WA-Daemon-Watchdog` scheduled task runs `watchdog.ps1` every 5 min: kills + restarts the daemon if PID dead OR heartbeat >5 min stale. So if you see `daemon_pid_alive=false` or stale heartbeat in `triage.js` output, just warn the user "WA daemon dead — watchdog will restart within 5 min, proceeding without WA" and move on. No need to restart manually unless the user is impatient or watchdog itself is broken.

**Why:** `triage.js` is a one-shot reader of `message-store.jsonl`. Its `generated_at` measures when *it* ran, not when the daemon last captured anything. The heartbeat file is the only signal that the daemon's WebSocket is actively connected.

**How to apply:** In any code or skill that reads WA data, always check daemon_pid_alive + heartbeat_age before trusting the items array. See [[reference_wa_sender]] for the rest of the WA stack.
