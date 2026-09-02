---
name: reference_coattio_tailscale
description: "coattio CRM is reachable from the phone via Tailscale Serve (private tailnet HTTPS), URL + how it works"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6c32b433-096b-4c00-9d06-03e5f167f558
---

coattio (the local CRM on port 4124) is exposed to the user's phone via **Tailscale Serve** (set up 2026-07-06), NOT Vercel — Vercel was rejected because coattio's data is a local `crm.json` + the capture pipeline is all local (would need a full DB migration + rewrite).

**Phone URL (tailnet-only, private to the user's own devices):**
`https://desktop-1bojsrg.taile93f00.ts.net/` — call page `…/#/appels` (the `tel:` links tap-to-dial on mobile).

- Laptop node = `desktop-1bojsrg` (tailnet IP `100.127.7.80`), tailnet `taile93f00.ts.net`, account `alesoda2002@`. Phone = `pixel-9a` (android, already on the tailnet).
- `tailscale serve --bg 4124` proxies the tailnet HTTPS root → `http://127.0.0.1:4124`, so coattio's loopback-only bind needed **no code change**. First HTTPS request provisions a Let's Encrypt cert (~can take 20-40s; give curl a long timeout).
- Requires tailnet **Serve** enabled once (admin page `login.tailscale.com/f/serve?node=…`). Persists across reboots (Tailscale service at boot + saved serve config + the `Coattio-Watchdog` keeps 4124 up — see [[reference_coattio_servers]]).
- To change/disable: `tailscale serve status` / `tailscale serve --https=443 off`. Tailscale at `C:\Program Files\Tailscale\tailscale.exe`.
