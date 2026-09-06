---
name: reference_trippy_on_box
description: Trippy runs on the VPS and is phone-reachable; box does search and duels, laptop keeps checkout.
metadata:
  type: reference
---

Set up 2026-09-06. The trippy board is on the box and reachable from the phone:

  http://da-box.taile93f00.ts.net:4126/   (or http://100.85.52.84:4126/)

Tailnet only. Tailscale already encrypts that link, so there is NO HTTPS and
no `tailscale serve` (which would have needed root; `da` is not in sudoers at
all on this box, and root SSH is key-only). `server.js` binds `TRIPPY_HOST`,
defaulting to 127.0.0.1 — never bind 0.0.0.0, that would expose it publicly.

- Code: `/home/da/travel-search` = private repo `alesod23/travel-search`,
  branch **master**, cloned from the laptop's `travel-search\v2\`. Two-way,
  5-min cron sync via `repo-sync.sh`. Deploy key `~/.ssh/travel_search_ed25519`
  (host alias `github-travel`); the default `id_ed25519` only unlocks task-land.
- `alesod23/trippy-public` is a FROZEN showcase, renamed from `trippy`. Never
  push to it, never put trip data in it.
- No systemd: `da` cannot sudo. Crontab runs `~/.local/bin/trippy-supervise.sh`
  at @reboot + every 5 min; it restarts the app and swaps out a placeholder.
- Search engine is [[reference_gflights_engine]], not momondo.

**Division of labour: the box does search, boards and context duels. CHECKOUT
STAYS ON THE LAPTOP** — it needs a visible browser driving airline funnels, and
a browser on the box would not help anyway (the datacenter IP is the blocker).
