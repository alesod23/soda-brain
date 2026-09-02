---
name: feedback_approvals_are_pings
description: "\"Ping\" is Alessandro's word for an approval-hub card; every approval request goes to the hub, never a numbered question in chat"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8416f96f-965c-41e3-a618-179e3b6cd758
  modified: 2026-08-03T19:14:20.541Z
---

**"Ping" / "pings" / "pinging" always means an approval-hub card** — the push that fires on his
phone and his laptop popup at the same time (`POST http://localhost:4180/pending` with
`notify:true`). When he says "ask me for confirmation", "approval", "let me approve", or "ping me",
the deliverable is a hub card, **not** a numbered list of questions in the chat.

**Why:** on 2026-08-03 he asked for the CDTM speaker pre-sends "as an approval point" and I put the
full emails plus three numbered questions in the chat instead. He pushed back: "Why are you asking
me in this chat? I told you specifically that I would want it as approved notifications." Chat only
reaches him when he is at the terminal; the ping reaches him anywhere, which is the entire point.

**How to apply:**
- One card per decision. `text` = the decision, self-contained and truthful (it is the whole phone
  popup). `context` = the full artifact, e.g. the complete email body, so `/item/<id>` shows
  everything.
- Yes/no only. For an either/or, state the recommended option in `text` so YES means that option,
  and say what to reject-with-feedback to get the alternative.
- `action` currently supports only `wa-send` and `slack-send`. Email and calendar approvals carry
  no action, so approving is a verdict I read back and execute; say so on the card.
- Superseding a card = resolve `no` WITH feedback text (a bare no fires a disapprove ping at him).
- Check for a verdict already set by `phone-macrodroid` before assuming a card is unanswered.

Related: [[reference_approval_hub]], [[feedback_message_send_protocol]], [[reference_voice_lane]].
