---
name: feedback_long_telegram_messages_collapsed
description: Any long Telegram message to him (my replies, update cards, reports) = one short first line + the rest inside Telegram's expandable (collapsed) blockquote
metadata:
  type: feedback
---

7 Oct 2026: "These are very long messages you're sending me and I would like for them to be collapsed because they're taking up too much of my space ... if a text is too long you're going to diminish it ... I mean that clickable expandable section". Filed as hub ledger rule too.

**Why:** he reads on the phone; long updates push everything else off screen.

**How to apply:** for my own Telegram replies longer than ~5 lines, send with format markdownv2 using the expandable blockquote (`**>` on the first quoted line, `>` on the rest, `||` closing the last line; escape MarkdownV2 specials `_*[]()~\`>#+-=|{}.!`), first line outside the quote says the outcome. Short replies stay plain. Hub cards: the hub renders it (`<blockquote expandable>` HTML), see [[reference_approval_hub]]. Related: [[feedback_quick_feedback_gets_one_line_ack]].
