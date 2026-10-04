---
name: reference-call-steps-get-no-draft
description: "A CRM step that is a phone call (text opens with call/phone/chiama..., or names only a call + a number) gets no message draft on the review board; every draft prompt lists what he already sent as binding (Alexis Dracker, 4 Oct 2026)"
metadata:
  type: reference
---

`~/.medtech-crm/review-api.js stepChannel(step)`: explicit `step.channel`, else 'call' when the text opens with a call verb
(call / phone / ring / chiama / telefona / appeler / anrufen; not "phone number", not "call for/with") or names only a call
plus a phone number. `channelFor` and `candidateChannel` return null for a call step, so the item is `no_channel` and
review.js shows "This step is a call". `alreadySentBlock()` puts === WHAT HE ALREADY SENT === (code-checked, binding) in
every generator prompt: never re-send the same introduction, referral, ask or pitch in other words.

**Why:** 4 Oct 2026 crm-review, Alexis Dracker: "this was already sent bro..". Her step "call Alexis ... on +1 415-987-3776"
had no channel (set by hand 24 Sept), the board fell back to email and Opus rewrote the 16 Sept email. Gmail (tundra)
holds only that one message to her. Same pattern on Rania Tohme and 8 others; all 10 got `channel: call` via :4124.

**How to apply:** code that writes a step for a call sets `channel: 'call'`; code that picks a message channel from a step
calls `stepChannel`, never `step.channel` alone. Test: `node --test tests/already-sent.test.js` from ~/.medtech-crm.

Related: [[reference-reply-check-before-draft]], [[project-crm-review-loop-vision]], [[reference-crm-not-target-family-friends]].
