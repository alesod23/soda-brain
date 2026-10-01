---
name: feedback-tundra-signature-always
description: Every mail from the tundra account carries the Tundra signature; gmail.py adds it by itself (draft, update, send, send-draft), never rely on Gmail's own signature for API drafts
metadata:
  type: feedback
---

Every mail from the tundra account carries the Tundra signature. Always create and send tundra mail through
`gmail.py` / `gmail.cmd` (laptop `~/triage`, box `~/triage`), never through a Gmail connector: gmail.py appends the
signature by default for account `tundra` (`ACCOUNT_SIGNATURE`), on `draft`, `update-draft`, `send` and, as a last
gate, `send-draft` (what the hub runs when he approves from the phone). `--signature student` chooses the other one,
`--no-signature` opts out. The body still ends with "Alessandro" alone, no signature written by the writer.

**Why:** 2026-09-28, the drafts to Mathieu Costa and Alexandre Benoist made by the event worker had no signature.
A draft created through the API never gets the account's Gmail signature (only Gmail's compose window inserts it);
email ledger H17 said "Gmail's per-account signature does the rest", which was false for every draft a session makes.
Only campaign mail passed `--signature` (H68). His words: "ensure that it doesn't reoccur in the future (even
across different sessions/chats)".

**How to apply:** nothing to remember when using gmail.py. If a draft was made another way,
`gmail.cmd sign-draft --account tundra --draft-id <id>`, or wait: the system agent runs
`gmail.cmd sign-drafts --account tundra` every 30 minutes. Drafts to himself and empty drafts are left alone.
Signature files: laptop `~/gtm-eng/signatures`, box `~/triage/signatures`.

Related: [[feedback-email-no-signature-block]], [[reference-draft-review-lane]], [[reference-system-agent]].
