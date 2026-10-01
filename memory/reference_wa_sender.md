---
name: wa-stack-read-send-via-single-daemon
description: "Single-device Baileys setup on Windows. wa-daemon owns the only WA session and exposes both read AND send via a local HTTP endpoint. All data and helpers live in wa-daemon/; the old wa-sender folder was deleted on 2026-05-17."
metadata: 
  node_type: memory
  type: reference
  originSessionId: c303a26a-bf97-40a8-98e6-aaac6c9c9d6d
---

WhatsApp on this machine consolidated to ONE linked device (2026-05-17). The wa-sender folder is gone; everything lives in `wa-daemon/`.

| Folder | Linked device | Purpose |
|---|---|---|
| `C:\Users\Alessandro\.claude\wa-daemon\` | `:46` | **READ + SEND + DATA**. Long-running daemon (`daemon.js`) owns the Baileys session, captures messages into `message-store.jsonl`, AND exposes `POST /send` + `GET /health` on `127.0.0.1:4119`. Helpers: `triage.js` (read), `send.js` (thin HTTP client to /send), `sync-contacts.js` (Google People API sync). Data: `contacts.json` (Google-synced), `aliases.json` (manual JID overrides), `lid-overrides.json` (LID-to-name tags), `chats.json` (group names), `wa-groups-block.json` (muted groups). |

Why consolidated: two devices was over-engineering for a personal account. One Baileys session handles read+write at this volume; isolating them caused a silent-failure mode (sender logged out without anyone noticing).

## Send (via daemon HTTP endpoint)

```powershell
node C:\Users\Alessandro\.claude\wa-daemon\send.js --jid "<jid>" --text-file "<path.txt>" --confirmed   # PREFERRED: body from UTF-8 file
node C:\Users\Alessandro\.claude\wa-daemon\send.js --to "<name|+phone>" --text "<one-liner>"             # dry run, simple text only
node C:\Users\Alessandro\.claude\wa-daemon\send.js --to "<name|+phone>" --text "<one-liner>" --confirmed # actually send
```

> ⚠️ **HARD RULE — multi-line / quotes / emoji → ALWAYS use `--text-file` (added 2026-06-07).** PowerShell 5.1 silently TRUNCATES/mangles an inline `--text` argument the moment it contains a double-quote: it breaks at the first `"`. On 2026-06-07 a message to Caleb got cut to "…show" (the first `"` in the body) and sent that way. The `--text-file` flag reads the body from a UTF-8 file (write it with the Write tool, then pass the path) so the text NEVER touches shell quoting. send.js now also prints `Length: N chars | ends: …"<last 40>"` — **verify the tail matches** before trusting a send. Generalizes: never pass any multi-line/quoted string as an inline native-exe arg in PowerShell — use a file (or stdin). See [[feedback_clipboard_all_paste_drafts]] for the `!`-routes-to-bash quirk.

Resolution order: `wa-daemon/aliases.json` (manual overrides, may be a JID or +E164) -> `wa-daemon/contacts.json` (Google-synced names -> phones). Fuzzy match: case + accent insensitive, exact wins, ambiguous lists candidates and exits non-zero. Dry-run is free (no daemon needed). Confirmed send health-checks then hits `127.0.0.1:4119/send`.

**NEVER send without explicit user confirmation after showing the resolved phone. After any send, READ BACK the `Length`/tail echo (or the thread) to confirm the full body landed — the console `Message:` echo can itself look truncated.**

## aliases.json — auto-populate on every JID discovery (STANDING RULE, set 2026-06-10)

Any time a name<->JID association is **discovered or resolved** during a session — for an **individual OR a group** — append it to `wa-daemon/aliases.json` immediately, so the next interaction is a one-call `--to <name>` with no lookup dance. This is a behavioral rule for me (semantic judgment about "I just learned X = JID Y"), not a harness hook. Groups (`@g.us`) are explicitly in scope, not just people.

Known group aliases already saved:
- `me` -> `120363023505333085@g.us` (the user's WhatsApp self-chat group, stored on the phone as `"Me "` with a trailing space — that trailing space caused three wasted Grep misses on 2026-06-10 before the alias existed).

One-call send pattern (no group-name guessing):
```powershell
node C:\Users\Alessandro\.claude\wa-daemon\send.js --to me --file "<path>" [--caption "txt"] --confirmed
```
`send.js` self-validates the file (`existsSync`) — no pre-`ls`/Glob check needed; just call it. The ONLY necessary shell call for a send is the `send.js` invocation itself.

### Inline image vs document (added 2026-06-22)
`--file` alone sends as a **document** (tap-to-open file, no preview). For a real **photo preview** add `--image`:
```powershell
node C:\Users\Alessandro\.claude\wa-daemon\send.js --to me --file "<img.png>" --image [--caption "txt"] --confirmed
```
- `--image` sets `payload.asImage`; the daemon then builds Baileys `{ image: buf, caption, mimetype }` instead of `{ document: ... }`, but ONLY when the mimetype is `image/*` (else it falls back to document). Implemented in `daemon.js` /send handler (`asImage && mt.startsWith('image/')` branch) + `send.js` (`--image` flag).
- **Requires a daemon restart after any daemon.js edit** (stop.ps1 → start.ps1 → poll `/health` for `connected:true`); the running process holds the old code.
- Verify which path a send took via `daemon.log`: the line reads `image "<name>" (...)` vs `doc "<name>" (...)`. Outgoing sends are NOT echoed into `message-store.jsonl`, so the log is the source of truth, not the store.
- Built + tested on the `me` self-chat 2026-06-22 (id 3EB04076…, image/png, log confirmed `image`).

## Read / triage

Daemon ingests every incoming/outgoing message into a 7-day rolling JSONL store. Triage reads the store; the daemon owns the Baileys connection.

```powershell
# daemon control
powershell -ExecutionPolicy Bypass -File C:\Users\Alessandro\.claude\wa-daemon\start.ps1
powershell -ExecutionPolicy Bypass -File C:\Users\Alessandro\.claude\wa-daemon\stop.ps1
Get-Process -Id (Get-Content C:\Users\Alessandro\.claude\wa-daemon\daemon.pid) -ErrorAction SilentlyContinue
Get-Content   C:\Users\Alessandro\.claude\wa-daemon\daemon.log -Tail 20
curl http://127.0.0.1:4119/health

# read
node C:\Users\Alessandro\.claude\wa-daemon\triage.js --hours 48
node C:\Users\Alessandro\.claude\wa-daemon\triage.js --hours 48 --json
```

JSON includes `repliedSinceLastIncoming`, `lastIn`, `lastOut`, `totalIn/OutCount` per item. Outgoing messages sent via /send are captured by the same daemon (own-echo via messages.upsert), so `repliedSinceLastIncoming` naturally flips to true next triage round.

## Name resolution priority (in triage.js)

1. `lid-overrides.json` (manual overrides via `node lid-tag.js <lid> "Name"`)
2. `@s.whatsapp.net` JID -> digits -> `wa-daemon/contacts.json`
3. `@lid` with captured `senderPn` -> contact lookup
4. `@lid` with captured `pushName` (live messages only; history sync strips it)
5. Fallback: `unknown (lid <last6>)`

## Skill doc

`C:\Users\Alessandro\.claude\skills\wa\SKILL.md` (full setup, troubleshooting, integration reference).
