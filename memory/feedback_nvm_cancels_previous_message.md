---
name: feedback_nvm_cancels_previous_message
description: "A bare \"nvm\" on Telegram means: disregard the message I just sent. Drop that request, don't ask why, and say what (if anything) already happened."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 26333c6f-5f43-43b7-badf-07594a1db485
  modified: 2026-08-05T22:52:01.292Z
---

**Standing rule (set 2026-08-05, on Telegram):** when he sends a message by mistake, his retraction
is a short follow-up — usually the bare word **`nvm`**, nothing else. That means **disregard the
message immediately before it.** His words: *"Whenever I make a mistake in sending you a message, I
can also send a quick follow-up that will tell you to disregard the message that I just sent you. I
think it will be a very simple 'nvm' with nothing else. Then you'll know."*

**Why:** he fires messages off fast, often by voice and often mid-thought, so wrong sends happen. He
wants a one-token escape hatch instead of having to explain the mistake — and without a convention,
a bare "nvm" is ambiguous enough that I might keep working on the retracted request or, worse, ask
him to clarify what he meant, which costs more than the mistake did.

**How to apply:**
- **Scope = the single message it follows**, not the whole conversation and not the current task.
  If he sends A, then B, then "nvm", B is cancelled and A still stands.
- **Drop it silently-ish.** Acknowledge in a few words, don't interrogate, don't ask what he meant
  to send instead, don't offer alternatives. He'll say what he wants next.
- **If I already acted on it, say so plainly and state whether it is reversible** — a retracted
  message whose side effects already landed (a file written, a message sent, a Notion row created)
  is the one case where he needs a sentence back from me, and an offer to undo it.
- **If I am mid-work on it**, stop, and say what got left half-done.
- Treat obvious variants the same way ("ignore that", "scratch that", "disregard"), but `nvm` alone
  is the canonical form he committed to.
- A "nvm" arriving MID-TURN (as a `<channel>` notification while I'm already working) counts —
  same as any other mid-turn message, it still gets its 👀 and it still cancels.

Related: [[feedback_rule_requests_are_binding]], [[feedback_telegram_reply_tool_every_turn]],
[[feedback_react_eyes_before_working]], [[feedback_channel_sequential_handling]].
