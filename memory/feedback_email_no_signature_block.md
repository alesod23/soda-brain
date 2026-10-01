---
name: feedback_email_no_signature_block
description: "Never add a signature block to any email draft, on any account - end with a bare 'Alessandro'; Gmail's per-account signature is his, he appends it himself"
metadata:
  node_type: memory
  type: feedback
---

Ruled 2026-09-08 during the email-review-contract pass (C3), verbatim: *"there's actually no
need to have a full rule that applies everywhere here. We'd rather go for the automatic
signature depending on which email I'm sending from... I've noticed that you're not really
capable of adding signatures the way that Gmail does, so I think I'll add them myself for now.
just end it with Alessandro."*

**The rule.** Every email draft I create, on cdtm, tundra, lobbly or any account, ends with
the close line and then `Alessandro` on its own line. No asterisk-bold name, no phone, no
CDTM URL, no "joint institution" line. Ever.

**Why:** the right signature depends on the SENDING ACCOUNT (cdtm vs tundra carry different
ones) and Gmail already holds each. A hand-built block is either wrong for the account or a
duplicate he has to delete. This generalises [[feedback_professor_email_style]]'s
professor-only no-signature rule to everything; the "match the style of prior mails" instinct
that put a full block on the 2026-09-07 UPMC and MEDICON drafts was the trigger.

**How to apply:** contract rule H17 in `task-land/_system/EMAIL-REVIEW-CONTRACT.md`. When a
prior mail in the thread carries his block, still do NOT reproduce it - that block was
Gmail's, not mine. If he ever says "include the full signature", that overrides for that mail.

Related: [[feedback_professor_email_style]], [[feedback_message_send_protocol]].
