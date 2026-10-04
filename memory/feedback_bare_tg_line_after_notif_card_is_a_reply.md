---
name: feedback_bare_tg_line_after_notif_card_is_a_reply
description: A bare short Telegram line ("i got it") right after a SODANOtif card that asks him something is HIS ANSWER to that person; never let it drop while busy
metadata:
  type: feedback
---

On 4 Oct 2026 at 18:12 he sent "i got it" on Telegram while I was deep in the box cut-over with SODA SYSTEM. It answered Caleb's WhatsApp, shown on the SODANOtif card just before ("Are you taking over hotel booking in Orlando or should I? Same for train"). I filed it as noise; 27 min later: "did you miss this? ... you should've been able to infer from Caleb's txt".

**Why:** his Telegram replies are terse and often aimed at the person on the latest card, not at me. The swipe-reply resolver may show nothing (he did not swipe), so the meaning comes from the newest card's question.

**How to apply:** every inbound TG line gets a reply the same turn, even mid-task. If it reads like an answer to a question on the newest SODANOtif card, say so and offer the send (his words verbatim). Direct WA sends are classifier-blocked: offer a hub `wa-send` card or he sends it himself ([[feedback_message_send_protocol]]).
