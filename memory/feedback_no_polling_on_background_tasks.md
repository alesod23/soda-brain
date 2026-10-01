---
name: no-polling-on-background-tasks
description: Never combine run_in_background with ScheduleWakeup as a poller — the harness auto-notifies on completion. Self-imposed wakeups add wasted wait time.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 08a010cc-3a1a-474f-995c-d20a76e7ae9c
---

When a Bash/PowerShell call is started with `run_in_background: true`, the harness automatically fires a `task-notification` system-reminder when it completes. Claude's session continues from that notification — no polling needed.

**Rule:** never call `ScheduleWakeup` after starting a background task, just to "check back". The wakeup adds latency equal to its delay even when the task finished earlier.

**Why:** observed 2026-05-23 during /triage. `fetch-all.js` ran in background, finished at 17:25:26 (elapsed 2:12). The auto-notification would have fired immediately, but I had also scheduled a 60s wakeup → I didn't re-engage until 17:27, wasting 90s. The CLAUDE.md rule "If waiting for a background task you started with `run_in_background`, you will be notified when it completes — do not poll" explicitly forbids this. I missed it.

**How to apply:**
- For a single long-running command (no parallel work to do in the meantime): prefer foreground with an explicit `timeout` higher than the expected runtime (e.g. PowerShell tool's default is 120000ms / 2 min — bump to 300000ms / 5 min for fetch-all-class jobs).
- For a long task WITH parallel work to do: use `run_in_background: true`, then immediately do the parallel work. The notification fires automatically; do NOT add a ScheduleWakeup as a backup.
- ScheduleWakeup is for external state the harness can't track (CI runs, deploys, remote queues) — NOT for harness-tracked background tasks.

**Related:** [[reference_triage_operations]] — /triage's fetch-all is the most common 2-min-ish job. Prefer foreground with a 5-min timeout there.
