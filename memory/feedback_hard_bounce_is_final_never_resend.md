---
name: feedback_hard_bounce_is_final_never_resend
description: An address that hard-bounces (no such mailbox, or an MX that refuses the connection) is dead: mark it, never send to it again, and read bounces before any further step.
metadata:
  type: feedback
---

2026-10-03, after the privati-nord mail to Ing. Marco Pattano
(marco.pattano@ic-cittastudi.it, sent once on 30 Sep 11:26) produced three
Mail Delivery Subsystem notices and a final "Message not delivered" at 13:37
on 3 Oct: *"Make it a rule that you will stop sending it if it's clearly a
spamsorry, clearly a non-existing email account"*.

The rule: a hard bounce is final. An address that bounces with a non-existent
mailbox, or whose domain's mail server refuses the connection
(`FAILED_PRECONDITION: connect error`), is marked dead on the board and in the
CRM the same day and never receives another email, from that campaign or any
other. Every campaign reads its own bounces before taking a further step to
that person; a step whose only channel was that address becomes a SEARCH for a
working address, never a resend.

**Why:** he sees the bounces in his own inbox, so every retry reads to him as
us spamming a dead address, and it burns the sending domain's reputation.
[[reference_daily_campaign]]

**How to apply:** H96 in `task-land/_system/EMAIL-REVIEW-CONTRACT.md`
(`--contract email`). The SMTP pre-check (H14, `gtm-eng/tools/smtpcheck.py`)
catches these BEFORE drafting; as of 3 Oct 2026 nothing in `gtm-eng` reads the
bounces AFTER sending, which is the open hole. Gmail retries one send for ~48h
and files a notice each time: three notices are one send, not three, so check
SENT before telling him anything about how many went out.
[[feedback_diagnose_before_naming_root_cause]]
