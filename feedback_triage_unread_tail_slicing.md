---
name: triage-unread-tail-slicing
description: "In /triage WA classification, slice the burst to the last `unreadCount` IN messages — earlier messages are already read on phone. Apply closure-tail check on the unread tail, not the full burst."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 08a010cc-3a1a-474f-995c-d20a76e7ae9c
---

When a WA item carries fresh signals (`unreadStateUpdatedAt` ≤ 24h) and `unreadCount > 0` and `unreadCount < count`, only the **last `unreadCount` IN messages** in the burst are truly fresh. Everything earlier has been read on phone — and the daemon's outgoing-sync hole means the user may also have already replied from phone without the daemon capturing it.

**Two consequences:**

1. **Classification:** apply closure-tail short-circuit on the unread tail, not the full burst. If the last `unreadCount` IN messages are all closures (stickers, single emoji, reactions, "ok"/"thanks"/"got it"), DROP. The substantive earlier messages were handled on phone; the closures are decoration. This generalizes the original `done[]`-keyed closure-tail rule.

2. **Display:** when surfacing, the snippet shows ONLY the unread tail (last `unreadCount` IN messages plus interleaved OUT msgs). Earlier already-read IN messages make the item look fresher than it is — omit them from the bolded body. A `Read on phone: <N>` caption above the snippet is fine for context, but the earlier messages never appear in the substantive snippet body.

**Why:** observed 2026-05-23 with "Lara" — `count: 4, unreadCount: 1`. The burst was 3 substantive 16:52 messages + 1 sticker at 18:15. User had already replied "Yess nw" at 14:26 from phone (daemon never captured the outgoing — known [[feedback_wa_daemon_flap_and_outgoing_gap]] bug). The 1 unread = sticker = pure closure → should have been dropped silently. Instead the full 4-line burst was rendered with the sticker bolded, which made the conversation look fresh and unanswered. User sent a reply they didn't actually need to send.

**How to apply:**
- Check the math: `count` (total IN in burst) vs `unreadCount`. If unreadCount < count and unreadStateUpdatedAt is recent, only the tail is fresh.
- Classify the tail. Closure tail → drop. Substantive tail → surface with tail-only snippet.
- Don't trust `repliedSinceLastIncoming: false` as proof the user hasn't replied — the daemon's outgoing capture is unreliable (Baileys multi-device sync drops `fromMe: true` events even without flap).
- `unreadCount` is the trustworthy proxy: it counts what's actually unread on the user's phone client, regardless of whether the daemon caught the outgoing replies that cleared earlier messages.

**Related:** [[feedback_wa_daemon_flap_and_outgoing_gap]] — root cause of why `lastOut` can be days stale. [[reference_triage_operations]] — display format rules; this rule modifies the snippet content for items where unreadCount < count.
