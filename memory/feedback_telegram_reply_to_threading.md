---
name: feedback_telegram_reply_to_threading
description: "Always pass reply_to (the inbound message_id) on every Telegram reply from now on — user explicitly liked seeing his message quoted/threaded and asked for it as a standing behavior."
metadata:
  node_type: memory
  type: feedback
  originSessionId: b205178d-e8c7-4fb5-bb4a-2728bf7343bd
---

**On every `mcp__plugin_telegram_telegram__reply` call, pass `reply_to` set to the `message_id` of the inbound message being answered.** The MCP tool description says reply_to is optional ("only when replying to an earlier message; the latest doesn't need a quote-reply") — that default no longer applies here.

**Why:** 2026-07-08 — I used `reply_to` once (message 727, "are you able to see which message im replying to") because it was a reply to an older message. The user saw the resulting quoted/threaded bubble in the Telegram UI and said "i love that you just referred to a specific message by replying to it like this. do it always when answering a message from me from now on." Explicit standing preference, not a one-off.

**How to apply:** Every `reply` call in a `plugin:telegram:telegram` channel session should include `reply_to: "<inbound message_id>"`, threading the response under the message it answers — even for the "obviously latest message" case where the tool's own default says it's unnecessary. When answering multiple queued inbound messages in one turn, thread each reply under its own message_id rather than merging into one reply_to.

See [[feedback_telegram_reply_tool_every_turn]] (related: reply tool must fire every turn) and [[feedback_channel_sequential_handling]] (each inbound message = its own task).
