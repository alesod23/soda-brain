---
name: feedback_react_eyes_before_working
description: "Telegram: react 👀 to an inbound message as the FIRST action, before any tool call or reply — it is his only signal that I saw it and started working."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 76b27505-2fd7-4161-a548-77a992a2ef56
  modified: 2026-08-04T07:38:06.949Z
---

**Standing rule (set 2026-08-03):** when a Telegram message arrives and I am going to act on it,
**react with 👀 FIRST** — before searching, before reading files, before replying. Then do the work.

**Why:** he has no other way to tell "Claude hasn't seen it yet" from "Claude is working on it".
A long research task with no reaction looks identical to a dropped message, so he sits there
wondering. The reaction is a read receipt plus a "started" signal in one tap-sized artifact.

**EVERY message, including mid-turn arrivals (tightened 2026-08-03 after he caught me).** The rule
is not "react to the message that started the turn" — it is react to EVERY message of his. Messages
that land while I am already working arrive as `<channel>` system notifications; those need the 👀
too, the moment I see them, not at the end. I reacted to the turn-openers and silently skipped
"Berghausen" and "Cards" because they arrived mid-work, and he noticed. Same structural blind spot as
the swipe-reply resolver, which also only fires on turn-openers — see
[[reference_tg_reply_resolver]].

**NO EXCEPTIONS — the "short answers can skip it" loophole is REVOKED (2026-08-04).** This memory
used to end with "for a pure one-line answer the reaction can be skipped", and that clause is exactly
how the rule decayed: in one session I reacted to the opener, then let five consecutive messages
through with nothing while I worked, and he called it out — *"You stopped reacting with eyes emoji
when you read my messages. I thought we set it as a rule that survived across sessions. Make it so."*
Every inbound message gets 👀. Short ones, mid-turn ones, screenshots, corrections, all of them.
Judging which messages "deserve" it is the failure mode; the rule is unconditional so there is
nothing to judge.

**IT IS NOW MECHANICAL — a hook does it, not me (2026-08-04).** He asked for a rule that "survives
across sessions", and a memory instruction demonstrably did not: it decayed from every-message, to
turn-openers, to nothing, over three sessions. So it moved into the harness.
`C:\Users\Alessandro\.claude\hooks\tg_auto_react.py` is called from the existing `UserPromptSubmit`
gate `tg-reply-context.py` (one hook for both Telegram jobs). It regexes every `<channel …
source="…telegram…" chat_id=… message_id=…>` in the raw prompt and POSTs `setMessageReaction` with
👀, deduped in `.tg-auto-react-state.json`, 3s timeout, silent on failure, capped at 6 per prompt.
Token comes from `channels\telegram-v3\.env` (`TELEGRAM_BOT_TOKEN`). Verified live: `{"ok":true}`.
**The gap the hook does NOT cover: messages that arrive MID-TURN** as system notifications never pass
through `UserPromptSubmit`, so those still need a manual `react` call the moment I see them.

**How to apply (mid-turn arrivals, and any turn where the hook did not fire):**
`mcp__plugin_telegram_telegram__react` with `emoji: "👀"` and the inbound
`message_id`, as the first tool call after seeing the message. Telegram only accepts a whitelist
(👍 👎 ❤ 🔥 👀 🎉 …) — 👀 is on it. This is additive: the normal reply still goes out when the work
is done. Mid-turn arrivals can be batched into one parallel block of `react` calls, but they must go
out in the same block, not at the end of the turn.

See [[feedback_telegram_reply_tool_every_turn.md]], [[reference_telegram_channel_plugin.md]].
