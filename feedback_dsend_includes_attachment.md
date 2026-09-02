---
name: feedback_dsend_includes_attachment
description: "An image attached to a dsend/send instruction IS part of the message — send the attachment along with the text, don't send text only and ask about the picture."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 76b27505-2fd7-4161-a548-77a992a2ef56
  modified: 2026-08-03T16:58:58.351Z
---

When Alessandro sends a message on a channel that carries an **attachment** plus a send instruction
(`dsend to caleb : nope` with a screenshot attached), the attachment is **part of the message he is
sending**, not background context for me. Send BOTH the text and the file, in one go.

**Why:** he attached it deliberately, in the same message, to the same recipient. The text is usually
the reaction and the image is the evidence the reaction refers to — "nope" plus the screenshot of the
Claude Design *Project not found* screen is a single reply to Caleb. Splitting them delivers a bare
"nope" that means nothing on its own, and then bills him a round trip to approve the obvious.

**How to apply:** `dsend`/`send` + attachment → send text and attachment together, no confirmation
step for the attachment. Use `send.js --jid <jid> --file <path> --image --confirmed` for photos
(inline preview) or `--file` alone for documents. Only hold back an attachment if it is plainly
unrelated to the recipient, or if he named a different destination for it.

Burned 2026-08-03: sent only "nope" to Caleb, held the screenshot back on privacy grounds and asked.
Correction: "you had to send it too." My privacy caution was mine to have, not his — he had already
chosen to send it. See [[feedback_message_send_protocol]], [[reference_wa_sender.md]].
