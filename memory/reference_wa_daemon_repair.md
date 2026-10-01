---
name: reference_wa_daemon_repair
description: "How to re-link the wa-daemon after it gets unlinked, and the syncFullHistory=false gotcha that makes a freshly-paired daemon 428-loop forever."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6ae8a5d1-8ed7-4951-926a-c95e51082ad5
  modified: 2026-08-23T20:46:21.643Z
---

When the wa-daemon device gets unlinked (user disconnects it, or logged-out), re-link it:

1. Get the number from the existing creds, don't guess: `python -c "import json;print(json.load(open('auth/creds.json'))['me']['id'])"` → e.g. `393459764713:xx@s.whatsapp.net`. Ale's WA number = **+393459764713**.
2. Stop the daemon (`stop.ps1`), back up + wipe `wa-daemon/auth/` (stale creds show `registered:true` so login.js won't request a NEW code — you MUST wipe to get a fresh code).
3. **ALWAYS PAIR VIA QR — user's standing rule (2026-08-23).** The pairing-CODE flow is DEAD: on 2026-08-22/23 ~10 code attempts failed ("Couldn't link device") across BOTH the VPS (Contabo IP) and the laptop (residential IP), on Baileys 6.7.18 AND 6.7.24, with the socket verifiably still ESTABLISHED — WhatsApp refuses the code server-side. A QR scan then worked FIRST TRY. Do not burn attempts on `login.js` codes again.
4. QR method: run `login-qr.js` (lives in `wa-daemon/vps-pair/`, portable) — it writes each rotating QR into `qr.html` (self-refreshing page, CDN qrcodejs) which you `Start-Process` so the user just scans: phone → Linked Devices → Link a Device → stay on the CAMERA screen. Expect one `restart required` reconnect before "LOGGED IN". To pair a device for a remote box: pair on the laptop this way, then `scp -r` the fresh `auth/` to the box and `chown -R da:da` — sessions survive the IP move (VPS daemon confirmed connecting fine on Contabo IP with laptop-minted creds, 2026-08-23).
5. On success login.js prints "Logged in as …:NN" and writes creds+pre-keys.

**THE GOTCHA (cost ~1hr on 2026-07-01):** after a fresh pair, `daemon.js` with `syncFullHistory: true` NEVER connects — it loops `disconnected (code=428 connectionClosed)` every ~6s forever, because a freshly-linked device chokes on the full-history sync and WhatsApp closes the socket. Tell: `login.js` connects fine (it uses `syncFullHistory:false`) but the daemon 428-loops on identical creds. **Fix already applied:** set `syncFullHistory: false` in daemon.js (line ~259). Live-message capture doesn't need backfill; chat names still populate via `groupFetchAllParticipating` on connect. WA Desktop/Web being open is NOT a conflict — linked devices coexist. See [[reference_wa_daemon_health]], [[reference_wa_sender]].
