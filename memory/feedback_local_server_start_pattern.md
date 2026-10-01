---
name: feedback_local_server_start_pattern
description: "Never start ANY new local dev server (not just coattio) via Bash/PowerShell run_in_background — the harness reaps it. Use Start-Process detached, or schtasks for durability."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 46a48b57-9810-4f97-b46c-01d6bfbe6f9b
---

The "never run_in_background for local servers" rule in [[reference_coattio_servers]] is
written as if it's coattio-specific, but it's actually a general harness behavior: any
process started via the Bash/PowerShell tool's `run_in_background: true` gets reaped when
the tool/turn's process tree is cleaned up, even though the tool result claims it's
"running in the background." Confirmed again 2026-07-14 building the `gmail-snippets`
local server (`C:\Users\Alessandro\gmail-snippets\server\server.js`, port 4160) — it was
silently killed twice in a row via `run_in_background`, each time reported back as a
`<task-notification status="killed">` shortly after.

**Why this matters:** don't trust a `run_in_background` "started successfully" result for
anything meant to keep running past the current turn. Verify with a live request
(curl/Invoke-WebRequest) before telling the user it's up, and don't be surprised if it's
dead a turn later.

**How to apply — for ANY new local Node/Python/etc. server, not just coattio:**
- One-off dev testing within the same turn: `run_in_background` is fine (it just won't
  survive past the turn).
- Anything the user needs to keep running (a server backing a browser extension, a CRM,
  etc.): use `Start-Process -FilePath node -ArgumentList <script> -WorkingDirectory <dir>
  -WindowStyle Hidden` for an immediately-detached process, independent of this session's
  process tree.
- For real durability (survives reboot, self-heals if it crashes): a `schtasks`-created
  scheduled task running an idempotent "start if port is down" keeper script, same pattern
  as `Coattio-Watchdog` / `coattio-serve.ps1`. `Register-ScheduledTask` needs elevation
  (access denied without admin) — use `schtasks /create … /sc minute /mo 5` instead.
