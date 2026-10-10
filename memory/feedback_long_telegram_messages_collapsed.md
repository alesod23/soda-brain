---
name: feedback_long_telegram_messages_collapsed
description: Any long Telegram message to him (my replies, update cards, reports) = one short first line + the rest inside Telegram's expandable (collapsed) blockquote
metadata:
  type: feedback
---

7 Oct 2026: "These are very long messages you're sending me and I would like for them to be collapsed because they're taking up too much of my space ... if a text is too long you're going to diminish it ... I mean that clickable expandable section". Filed as hub ledger rule too.

**Why:** he reads on the phone; long updates push everything else off screen.

**Refined 7 Oct 21:00:** ONE emoji per message: 🆕 update (was 🟣 until 21:02) (title line + collapsed body), ✅❌ approval (full length, he reads it all). The hub renders this since 7 Oct (server.js patched on the box).

**10 Oct 2026:** native Telegram Yes/No buttons are live on hub decision cards (HUB-TGBTN-1005 + plugin HUBBTN-20261005), so the ✅❌ glyph came off the hub's approval titles (HUB-NOGLYPH); tick times use HUB_TZ, default America/New_York.

**How to apply:** for my own Telegram replies longer than ~5 lines, send with format markdownv2 using the expandable blockquote (`**>` on the first quoted line, `>` on the rest, `||` closing the last line; escape MarkdownV2 specials `_*[]()~\`>#+-=|{}.!`), first line outside the quote says the outcome. Short replies stay plain. Hub cards: the hub renders it (`<blockquote expandable>` HTML), see [[reference_approval_hub]]. Related: [[feedback_quick_feedback_gets_one_line_ack]].
