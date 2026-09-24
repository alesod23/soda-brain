---
name: reference-coattio-servers
description: How the coattio CRM + intake servers stay alive — never start them via a reap-able tool background process.
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6c32b433-096b-4c00-9d06-03e5f167f558
---

The **coattio** stack has two long-running local servers:
- **4124** — CRM UI/API (`~/.medtech-crm/crm-app/server.js`)
- **4137** — intake + Alt+K/screenshot enrich worker (`~/.medtech-crm/intake-server.js`)

**They are kept alive by the `Coattio-Watchdog` scheduled task** (created via `schtasks`, runs every 5 min), which executes `~/.medtech-crm/coattio-serve.ps1` — an idempotent keeper that starts each server only if its port is down. So both self-heal at logon, every 5 minutes, AND (added 2026-07-08) within ~10s of resume-from-sleep via two event triggers (Power-Troubleshooter EventID 1, Kernel-Power EventID 107 on the System log). Battery-power restrictions were also removed from this task — see [[feedback_sodanotif_battery_power_task_setting]] for why that flag matters.

**Phone access is via Tailscale Serve** ([[reference_coattio_tailscale]]) proxying to `localhost:4124` — it depends entirely on these node servers being up, so any watchdog gap takes the phone UI down too even though the tailnet itself is fine.

**HARD RULE — never (re)start these via a tool `run_in_background` (Bash/PowerShell background).** The harness reaps those processes at cleanup and the server dies silently (this is why the CRM kept going down). Instead:
- To restart after a code change: `Stop-Process` the old pid, then `Start-Process node <script> -WindowStyle Hidden` (detached) **or** just run `coattio-serve.ps1`. The watchdog also brings them back within 5 min regardless.
- `Register-ScheduledTask` needs elevation (Access denied without admin) → use `schtasks /create … /sc minute /mo 5` instead.

Full system map: `medtech-brain/_system/OUTREACH-SYSTEM.md`. See [[reference_outreach_system]].

**2026-09-24, the cause of four box Telegram outages (16:19, 22:57, 14:56, 17:49 over four days), found by the savior:** a headless `claude -p` spawned by coattio on the box (intake classifier, ai-draft, comment-agent, notion-sync) inherited the REAL `TELEGRAM_STATE_DIR`, loaded the telegram plugin (`plugins/.../telegram/0.0.7/.in_use` written 17:49:29), became a second getUpdates consumer and killed the savior's poller 30 s later. The times were "when someone used the CRM", not a schedule. The laptop's hourly tar push was suspected and disproved by its log (it ships only skills+commands, no plugins/). Fixes: `start-box.sh` sets `TELEGRAM_STATE_DIR=$HOME/.claude/channels/telegram-null` (savior), and in code `hidden-claude.js childEnv()` defaults every child to the null dir on both OSes, the intake classifier and ai-draft add `--strict-mcp-config` (ed404ea). Rule: any new headless claude spawned by a coattio process goes through hidden-claude.js, never a bare execFile.
