---
name: telegram-reply-tool-every-turn
description: "In a Telegram-channel session, every single turn must call the reply tool — plain assistant text is invisible on the user's phone even mid-conversation, not just on the first message."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 833c9bca-1d56-4c13-a3c5-19bf926ee404
---

Caught 2026-07-06: mid-conversation in a `plugin:telegram:telegram` channel session, one turn (explaining a Caleb WhatsApp draft) was answered as plain assistant text without calling `mcp__plugin_telegram_telegram__reply`. It rendered fine in the terminal/CLI transcript but never reached the user's actual Telegram app — they only got whatever ambient notification Telegram itself shows, and were confused why "the message" didn't exist on their phone.

**Why:** the MCP server instructions already say this ("your transcript output never reaches their chat") but it's easy to lapse on a turn that feels like a continuation of the same back-and-forth rather than a fresh inbound message — the model can slip into terminal-only text as if the terminal were the real channel.

**How to apply:** in ANY turn inside a telegram-channel conversation (`source="plugin:telegram:telegram"` or similar), regardless of how minor or how continuous it feels with the prior turn, the outbound content MUST go through the `reply` tool call. Never end a turn with plain assistant text as the only communication when a channel tag is present anywhere in the active conversation. Treat "did I call reply this turn" as a mandatory checklist item before ending any response in a channel session.

**RECURRED 2026-07-09, three turns in a row** (todo-add confirmation, a WA-group-send confirmation, a WA-DM-send confirmation) — each ended with plain assistant text only, no `reply` call, so none reached the user's phone. Only discovered because a later "2 dsend this" (ordinal reference, see [[feedback_telegram_ordinal_message_reference]]) forced a grep of the session JSONL for actual `mcp__plugin_telegram_telegram__reply` tool_use calls, which showed a 3-turn gap. **This means the failure mode is not self-evident from my own transcript** — the plain-text turn looks identical to a real reply in my own context, so I can't just "remember" whether I called it. Concrete fix: after finishing the SUBSTANTIVE work of any channel turn (sends, file edits, lookups), before ending the turn, explicitly ask "did the last tool call in this turn have name `mcp__plugin_telegram_telegram__reply`?" — if the last tool call was something else (Write/Edit/PowerShell/etc.), one is still owed. When in doubt whether a prior turn's reply actually landed, grep the current session's JSONL transcript for the tool name rather than trusting recollection.

**RECURRED AGAIN 2026-07-13**: user sent a photo (email bounce screenshot) via Telegram asking to explain it. Answered entirely in plain assistant text (a substantial multi-paragraph explanation) with zero `reply` tool call — despite this being the exact scenario the rule already covers (image-analysis turns feel like "just answering a question," not "sending a message"). User had to explicitly ask "why didn't you answer this on the telegram chat?" before it was caught. **Pattern across all three lapses: the turn "feels" like pure Q&A/explanation rather than an action, which is precisely when the reply call gets skipped.** Explanation/analysis turns are NOT exempt — they need `reply` exactly as much as send-confirmation turns do.
