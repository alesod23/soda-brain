---
name: reference-wa-web-scrape
description: WA Web scrape pre-step in /triage — confirms phone-read state via the first-party WhatsApp Web client. Path A (additive only). Toggle on/off via config.json without code changes.
metadata: 
  node_type: memory
  type: reference
  originSessionId: d7cda427-75d2-40b5-93f1-2e4a03c2422b
---

# WA Web scrape pre-step for /triage

## What it is
A Playwright-driven headless Chrome that loads `web.whatsapp.com`, clicks the **Unread** filter, scrapes the chat-list DOM, and patches `~/.claude/wa-daemon/chats-state.json` with WhatsApp's first-party view of unread counts. Solves the long-standing "I read on phone but daemon never sees the markChatAsReadAction patch" problem (Baileys → server_sync push is unreliable; WA Web is the only client WhatsApp updates reliably).

Lives at `C:\Users\Alessandro\.claude\wa-web-scrape\`. Modular and deletable — removing the folder + flipping the config flag back to `false` leaves /triage running its original behavior.

## How it's wired
`C:\Users\Alessandro\triage\fetch-all.js` calls `node scrape.js --headless` BEFORE the parallel Gmail/WA/Slack fan-out, if and only if `wa-web-scrape/config.json#enabled === true`. Adds ~15-25s to each `/triage` round (Chromium boot + WA Web initial sync + DOM scrape). The bundle's `wa_web_scrape` field reports `{ enabled, ran, elapsed_ms, ok, error }` so you can see when it skipped or failed.

## Toggle on/off
Edit `C:\Users\Alessandro\.claude\wa-web-scrape\config.json`:
```json
{ "enabled": false }   // skip scrape, /triage at original speed
{ "enabled": true }    // scrape before every /triage, always-fresh state
```
Or one-shot bypass: `node fetch-all.js --no-wa-web-scrape`.

User was emphatic 2026-05-23 about wanting always-fresh state, but also worried scrape would slow `/triage` to a crawl. Toggle exists specifically so user can flip it off without touching code if the 15-25s cost becomes painful in practice. Default: enabled.

## Path A — additive only (decided 2026-05-23)
The scrape NEVER zeroes a chats-state entry just because WA Web didn't show that jid in the unread filter. Reasoning: if title→jid mapping fails (unmapped contact), a "didn't see it = it must be read" inference produces **false negatives** — real unread chats wrongly marked read, hiding them from /triage. The user surfaced this footgun during design.

The kept behavior: for chats whose title→jid mapping is CONFIRMED via any of (lid-overrides.json, chats.json, contacts.json, message-store pushNames), write `chats-state[jid].unreadCount = N` (whatever WA Web shows). For chats we can't map, the daemon's chats-state stays untouched — same behavior as before the WA Web scrape existed. Daemon is authoritative; WA Web is a confirmation layer for mapped chats only.

## jid↔name bridge
WA Web shows your address-book contact name (e.g. "Caleb Seeling"); daemon stores `@lid` jids. Bridge sources, priority order:
1. `wa-daemon/lid-overrides.json` — manual `{jid: "Display Name"}` overrides (authoritative)
2. `wa-daemon/chats.json` — groups (jid → group name)
3. `wa-daemon/contacts.json` — phone-DMs (name → +phone → `<digits>@s.whatsapp.net`)
4. `wa-daemon/message-store.jsonl` — most-recent pushName per @lid (fuzzy startswith match)

Run `node C:\Users\Alessandro\.claude\wa-web-scrape\suggest-mappings.js` after a scrape to auto-pair unmapped @lid jids with WA Web titles using pushName fuzzy matching. Prints ready-to-paste `lid-tag.js` commands for high-confidence pairs. The mapping table grows over time as new contacts message you.

## Outgoing-message fallback (separate, in `daemon.js`)
Independent of the WA Web scrape: when the daemon captures an outgoing message (`fromMe: true`) for any chat, it immediately sets `chats-state[chatJid].unreadCount = 0` with `readVia: outgoing-message-fallback`. Catches "I read AND replied" cases instantly without needing WA Web. The scrape covers the residual "read but didn't reply" case.

## Companion files
- `scrape.js` — main scraper
- `config.json` — toggle
- `suggest-mappings.js` — auto-pair unmapped names with @lid jids
- `inspect.js` / `inspect-jid.js` / `inspect-msg-keys.js` — DOM debugging helpers (safe to delete)
- `profile/` — persistent Chrome user-data-dir (preserves the QR-scanned WA Web session)
- `last-scrape.json` — last raw scrape output for inspection
- `lid-suggested.json` — output of suggest-mappings.js

## When this might need attention
- WA Web DOM selectors break (~every 3-6 months). Symptom: scrape returns `0 unique chat titles` despite WA Web showing chats. Fix: re-run `inspect.js` to find new selectors, update `scrape.js`.
- WhatsApp evicts the linked device after 14 days of inactivity. Symptom: scrape hits QR screen. Fix: run `node scrape.js` once without `--headless` to re-pair.
- Memory leak buildup in the Chromium profile. Symptom: scrape gets slower over time. Fix: delete `profile/`, re-pair on next run (loses cached chats, but rebuilds in ~30s).

Related memories: [[reference_wa_sender]], [[reference_wa_daemon_health]], [[feedback_wa_daemon_flap_and_outgoing_gap]].
