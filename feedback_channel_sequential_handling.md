---
name: feedback_channel_sequential_handling
description: "Telegram/channel session must handle each inbound message as a SEPARATE ordered request, never conflate a notification-reply with a command"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 76c7578e-cb6d-4ecd-b540-c161a381259a
---

> **2026-09-02: COMET ABANDONED — every "Comet" below now means CHROME (the default browser). See [[feedback-browser-chrome-default]].**

**When messages arrive via a channel (the Telegram session), handle EACH inbound message as its OWN separate, ordered request. Never lump or conflate them.**

**Why:** 2026-06-23 the user sent two messages seconds apart — (1) "write to simon cdtm on wa: ping pong in 15?" and (2) "more context" (a reply to a Caleb notification card). The session handled BOTH in one turn: it sent the ping-pong message to Simon AND said "saw the Caleb context too, didn't act on it since it didn't apply" — conflating the independent "more context" request into the send command and dropping it. The user (rightly) wants his messages QUEUED and each one acted on.

**How to apply:**
- **FIRST STEP of EVERY Telegram turn: load your memory of the conversation.** A `claude --channels` bot session boots BLANK and push.js sends cards without the session seeing them, so by default the bot is amnesiac (2026-06-29: tapped "✅ Yes, send it" on Andrea's card → bot said "send what, to whom?"). Before doing anything, run `node C:\Users\Alessandro\.claude\sodanotif\tg-history.js 12` — it reconstructs the last 12 TG messages exchanged (cards the bot pushed WITH their draft+jid, merged with your taps/replies and the bot's replies, time-ordered) from the durable cross-session sources (`notification-log.jsonl` + the recent bot transcript). That feed gives the bot the context a normal CC chat already has. For `✅ Yes, send it` specifically: the most recent `[card]` line (also in `last-notification.json`) is the pending send — send THAT draft to THAT exact jid (confirm the resolved contact in your reply).
- **ALWAYS reply back to the channel via the `reply` tool (pass the chat_id).** Doing the work in the terminal WITHOUT a `reply` leaves the user staring at silence on Telegram (happened 2026-06-23: the session searched + drafted a WhatsApp message to Marc but never replied to TG, so the user got nothing). Every channel turn MUST end with a `reply`. For long tasks, send an interim `reply` too.
- Treat each inbound `<channel source="telegram" ...>` message as its OWN task. If several are pending in one turn, address EACH explicitly and IN ORDER, confirming each separately. Do not answer two requests in one merged reply that drops one.
- NEVER treat a reply-to-a-notification (e.g. "context", "more context", "open it", "clear", a heart) as a modifier on another command — they are independent requests.
- **"context" / "more context" / "more on <name>" replying to a SODANOtif notification = its OWN task.** The session did NOT send the card (push.js did), so READ `~/.claude/sodanotif/last-notification.json` (the latest pushed card: per-item from/group/snippet/draft + the raw messages with their `jid`s) to learn what it refers to, then fetch that chat's recent history (`/wa-search` on the jid, or the relevant source) and summarize. Never guess or silently drop it.
- **SODANOtif reply-keyboard buttons (Path 1 tap path, built 2026-06-23):** push.js attaches a Telegram REPLY KEYBOARD (docks above the input) to every card via `--keyboard`. Tapping a key SENDS its exact label as plain text, which the telegram plugin forwards as a normal `message:text` (inline callback buttons are dropped by the plugin — reply keyboards are the ONLY tap path that works on the one-bot Claudio setup). The three labels (single source of truth = `KEYS` in `~/.claude/sodanotif/push.js`) map to actions, ALL resolved against `last-notification.json`:
  - `✅ Yes, send it` → send the drafted `suggested_reply` to the EXACT known `jid` from the latest card (jid is exact, not fuzzy, so the no-headless-fuzzy-send rule is satisfied; still confirm the target back in the reply). See [[feedback_no_headless_fuzzy_send.md]].
  - `❌ No` → dismiss; acknowledge, take no action.
  - `💬 More context` → same as the typed "more context" above (fetch + summarize that chat).
  - `📂 Open chat` → open that conversation for the user. WhatsApp → open WA Web in **Comet** (the agreed open-chat-in-Comet step, see [[feedback_track_phased_plans]]) and drive the logged-in wa-web-scrape Playwright session ([[reference_wa_web_scrape]]) to that `jid`/contact; Gmail → open the thread URL; Slack → open the slack deep link. Resolve the target from `last-notification.json`.
  Match these EXACT strings (with emoji) when they arrive as inbound text.

**The bot's MEMORY of what it told you (the "double memory") — ALWAYS consult before resolving any reference.** push.js sends cards directly via the Claudio bot, so the session never saw them; and `last-notification.json` holds ONLY the latest card (overwritten every push). So when a reply references something from an earlier card ("send to conor", "more on the BMW thread", "open that", "reply yes to him"), the session is blind and guesses the WRONG channel/contact. This caused the 2026-06-29 bug: a `Conor Callaghan (WA)` card, then a Caleb card overwrote state, then "dsend to conor" — the bot searched **Slack** for Conor (found none, refused) instead of WhatsApp, because it had no record that Conor came in on WA.

**Fix (built 2026-06-29): `~/.claude/sodanotif/notification-log.jsonl`** — an append-only log of EVERY card pushed (daemon + recap), each item carrying `from / group / jid / source / snippet / draft`. The daemon resolves the exact `jid` per item at push time (the only place a privacy-`@lid` contact's id is ever captured — it may not be in the alias DB).

**HARD RULE — resolving a SODANOtif reply that names a person/topic ("send to X", "more on X", "reply to X", "open X"):** FIRST run `node ~/.claude/sodanotif/notif-log.js recall "<the reference>"` (newest-first match over from/group/snippet/draft/raw text). Use the returned `source` + `jid` to route to the CORRECT channel and EXACT contact. A jid from the log is an EXACT recipient (not fuzzy), so a send to it is allowed via the safe path WITH a confirm naming the resolved contact — never fall through to a different channel's fuzzy name search (the Conor→Slack mistake). Only if `recall` returns nothing, fall back to `last-notification.json`, then ask. `node notif-log.js recent <n>` dumps the last n cards for broader context.

See [[reference_sodanotif]], [[reference_telegram_channel_plugin]], [[feedback_no_headless_fuzzy_send]].
