---
name: reference_coattio_box_hosting
description: "coattio phase 9, the CRM served from the DA box over Tailscale so the phone works with the laptop off; proxy/local modes, mirror + reconcile, git-only code travel."
metadata: 
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-06T13:54:42.434Z
---

# coattio on the box (phase 9, 2026-09-06)

Phone URL: http://100.85.52.84:4124 (MagicDNS http://da-box:4124), intake on :4137. Tailscale app must be ON on the phone.

Design (crm-app/peer.js):
- Box (`COATTIO_BOX=1`, set by `start-box.sh`) probes the laptop 100.127.7.80 every 15 s. Mode `proxy` while it answers: every request forwarded, the laptop stays the single writer. Mode `local` otherwise: the box serves `~/coattio/crm.json` and marks writes dirty in its `mirror-state.json`.
- Laptop pushes crm.json to the box (`PUT /api/mirror`) 2 s after every write and on a 30 s mtime poll; every 60 s it reconciles: box dirty + laptop unchanged since last push = laptop adopts the box copy (backup `backups/crm-before-boxpull-*.json`) and pushes back; both changed = laptop wins, box copy saved as `crm.conflict-box-<stamp>.json` next to crm.json, one approval-hub card.
- Routes: `GET /api/health` `{role, mode}`, `GET /api/mirror/status`, `GET|PUT /api/mirror` (PUT box only).

Operational facts:
- Box clone `/home/da/coattio` (`~/.medtech-crm` symlinks to it), read-only deploy key `coattio-box-readonly` (ssh host `github-coattio`). `start-box.sh` = tmux session `coattio` (windows crm / intake), `--restart` kills and restarts; logs `box-crm.log`, `box-intake.log`.
- Cron on the box: `*/2 * * * * /bin/bash /home/da/coattio/coattio-sync.sh` (git pull --ff-only, restart on HEAD move; log `~/.local/state/coattio-sync.log` only on pull/failure). The box NEVER commits; a local commit breaks the pull.
- Laptop side: `DA-VaultSync` task (10 min) commits + pushes `~/.medtech-crm`; `Coattio-Watchdog` (5 min) restarts dead ports via `coattio-serve.ps1`. The laptop must keep Tailscale up, otherwise the box drops to `local` and the laptop cannot push.
- Data never travels by git (crm.json, mirror-state.json, backups are git-ignored).
- Verified 2026-09-06: laptop killed -> box `local` in 5 s -> phone-style PUT on the box -> laptop restart -> adopted in 6 s with backup, box back to `proxy`, dirty cleared. Doc: `~/.medtech-crm/PORTABLE.md`, workplan section 13.
