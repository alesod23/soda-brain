---
name: feedback_telegram_ordinal_message_reference
description: "In this Telegram chat only: a bare number refers to the Nth-most-recent INDIVIDUAL SODANOtif notification card (recaps/catch-ups excluded), resolved from notification-log.jsonl. Older sent-message ordinal rule survives only for explicit 'your message' phrasing."
metadata:
  node_type: memory
  type: feedback
  originSessionId: b205178d-e8c7-4fb5-bb4a-2728bf7343bd
  modified: 2026-08-01T19:34:09.955Z
---

**Standing rule for the `plugin:telegram:telegram` chat (chat_id 5362797891) ONLY — not a general CC convention.**

**REDEFINED by the user 2026-08-01:** a bare number ("1", "sodanotif one", "number two") indexes the **individual SODANOtif notification cards, newest first, with recap/catch-up cards EXCLUDED from the count**. His words: "it will not be so much the number of messages you have sent me, but the number of notification messages, so SODANOtif, that I've received... between there was a catch-up, which is not really a SODANOtif message."

**How to resolve (verified same day):** read `~/.claude/sodanotif/notification-log.jsonl` newest-first and skip entries with `"source":"recap"` — individual pushes carry the real source (`WhatsApp`, gmail, slack) plus `items[]` (from/jid/snippet/draft) and `messages[]`. N=1 is the newest non-recap entry. This supersedes transcript-grepping for MY sent messages as the resolution mechanism; see [[feedback_resolve_reply_from_notiflog]].

**The OLD rule** (ordinal = my Nth-to-last sent Telegram reply) applies ONLY when he explicitly says "your message/reply number N". When ambiguous, the notification reading wins — that is the one he standardized.

**Why:** 2026-07-08 — set up right after the Yes/No-button dead end ([[feedback_telegram_reply_to_threading]] session), as a lighter-weight way for the user to point at something I sent without retyping it. He explicitly required a safety check alongside it: "to ensure this doesn't end up sending the wrong thing to the wrong person, you will also do a double check, ensuring that what I'm about to send makes sense for the person or channel I am sending it to."

**How to apply:**
1. **Resolve the ordinal against what I ACTUALLY sent**, not memory/assumption. Telegram's Bot API has no history/search (per the MCP server instructions), so the source of truth is either (a) my own conversation context if still in-window, or (b) if compacted/new session, grep the JSONL session transcript(s) under `~/.claude/projects/C--Users-Alessandro/` for my prior `mcp__plugin_telegram_telegram__reply` tool_use calls to this chat_id, ordered by timestamp, and count back from the newest.
2. **Before acting on the resolved message** (e.g. sending it somewhere, treating it as a confirmed draft), sanity-check that its content actually matches the destination/recipient/channel implied by the current request. If message #3 was drafted for one person/context and the current ask implies a different recipient or doesn't fit, STOP and flag the mismatch to the user instead of sending — don't silently force a fit.
3. Still apply [[feedback_read_source_thread_before_acting]] on top of this — resolving the ordinal is not a substitute for checking the real underlying thread when the action has a real-world side effect (a send, a calendar change, etc.).

See [[feedback_telegram_reply_to_threading]], [[feedback_message_send_protocol]].
