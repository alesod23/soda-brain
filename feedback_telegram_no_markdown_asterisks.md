---
name: feedback-telegram-no-markdown-asterisks
description: "The telegram reply tool sends PLAIN TEXT by default, so **bold** arrives as literal asterisks; write without markdown unless format='markdownv2' is passed and every special char is escaped"
metadata:
  type: feedback
---

2026-09-28, mid-event: *"Questo messaggio bello broken eh... **?"* with a screenshot of my own
message showing `**Nel CRM**`, `**verificati**`, `**inoltra**` as literal asterisks. The pinned
message in the same chat had them too, so this had been happening for weeks and nobody saw it —
**I write into that chat, I never read it back.**

**The cause.** `mcp__plugin_telegram_telegram__reply` has a `format` parameter I was never
passing. It defaults to `"text"`, which sends the string verbatim. Markdown only renders with
`format: "markdownv2"`.

**The rule: write Telegram messages with no markdown emphasis.** No `**bold**`, no `__`, no
backticks for emphasis. Structure instead:
- lead the sentence with the word that matters, so the first three words carry the point;
- short paragraphs with a blank line between, which is what actually scans on a phone;
- a bare list with a middle dot when there are parallel items.

**Why not just switch to markdownv2.** MarkdownV2 requires a backslash before every
`_ * [ ] ( ) ~ > # + - = | { } . !` outside an entity. In Italian or French prose that is a
backslash before nearly every full stop and hyphen, and **one missed escape makes the send fail
outright**, so a message he is waiting for silently does not arrive. Not worth it for bold.
If it is ever wanted, build an escaper, test it on a throwaway message first, and only then use it.

**How to apply:** check what a formatting habit actually renders as before assuming it works,
especially on a surface where I only ever write. See [[feedback_telegram_reply_tool_every_turn]].
