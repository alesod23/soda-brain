---
name: feedback_open_email_drafts_in_comet
description: Any email I prepare for the user to send = create a REAL Gmail draft and auto-open it in the default browser (= CHROME since 2026-09-02, Comet abandoned) for visual review; never just paste the text in chat.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6ae8a5d1-8ed7-4951-926a-c95e51082ad5
  modified: 2026-09-01T22:34:17.092Z
---

> **2026-09-02: COMET ABANDONED — every "Comet" below now means CHROME (the default browser). See [[feedback-browser-chrome-default]].**

When the user asks me to send/prepare an email on their behalf (cdtm, lobbly, any account), I MUST:
1. Create a REAL Gmail draft via `~/triage/gmail.py draft --account <acct> ...` (NOT a `--dry-run` send, NOT just pasting the body into the chat/Telegram).
2. AUTO-OPEN that draft in Comet. `gmail.py draft` now PRINTS an `Open:` line with the exact URL — `Start-Process` THAT printed URL verbatim (do NOT hand-build it). Canonical format: `https://mail.google.com/mail/u/0/?authuser=<account-email>#drafts?compose=<message_id>` — it MUST contain BOTH the `/u/0/` path segment AND `?authuser=<email>`; dropping either loads a blank/wrong Gmail and the draft never appears. `message_id` = the hex id from `gmail.py draft`.
   Then **VERIFY it actually rendered** (screenshot the browser or ask the user) — `Start-Process` returning is NOT proof it opened; never claim "opened" until confirmed. NB the target account must be signed into Comet, else no URL can surface the draft.
3. Still surface the recipient + subject + body in chat AND wait for explicit "send/go" before firing `send-draft --confirmed` (send-confirmation rule unchanged).

**Why:** On 2026-07-01 I dry-ran an email to Julian and pasted the text into Telegram instead of creating a real draft and opening it in Comet. The user was annoyed: they want to REVIEW the actual draft visually in their own browser before it goes out. Pasting text in chat is not a substitute.

**REPEAT LAPSE (2026-07-06):** created a real draft (step 1) for Aaron/microAGI correctly, then skipped step 2 entirely — no `Start-Process` call, draft never opened in Comet — even though this memory already existed. The failure mode isn't "didn't know the rule," it's "the `gmail.py draft` call didn't trigger the open as a reflex." **Fix: treat `Start-Process` on the deep link as INSEPARABLE from the `gmail.py draft` call — the moment that command returns a `message_id`, the very next tool call (same turn) is the Comet open, no exceptions, not even when other tasks are in flight concurrently.**

**THIRD LAPSE (2026-07-07):** created the draft + DID call Start-Process, but hand-built a MANGLED URL (`https://mail.google.com/mail/?authuser=...` — dropped the `/u/` segment) so Comet loaded nothing useful, AND claimed "opened" from Start-Process returning without verifying. Two mechanical fixes now in place: (a) `gmail.py draft` emits the exact `Open:` URL so it is never hand-built again — just Start-Process it; (b) "opened" is not done until visually verified (screenshot / user confirm).

**How to apply:** This is the email analogue of the standing HTML/PDF-deliverable auto-open (an email draft is a deliverable to review). Opening a Gmail URL via the OS default handler (= Comet) is NOT browser *automation*, so it does not need the Chrome-for-automation path and IS the explicitly-approved Comet case. Auto-open is additive: still print the recipient/subject/body in chat too. Applies across ALL sessions and chats. Related: [[feedback_output_delivery_rules]], [[feedback_clickable_file_paths]], [[reference_triage_gmail]].
