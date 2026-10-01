---
name: feedback-professor-email-style
description: "How to draft cold emails to professors (intro phrasing, sign-off, no signature block)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4e231641-76c4-4d05-8867-f3a9a9b1a6d8
---

When drafting cold emails to professors (thesis supervision, office-hour requests, MIPLC/MSI/etc.):

**Intro line** — use this canonical self-introduction:

> I'm Alessandro, a Master in Management and Innovation (MiMI) student at TUM, currently part of the Center for Digital Technology and Management (CDTM) and the TUM Entrepreneurial Masterclass.

This is more accurate than just "student at CDTM" — it grounds the user in TUM's MiMI program first, with CDTM + EMC as add-ons.

**Sign-off** — `Kind regards,\nAlessandro`. Two lines. First name only. No surname.

**Signature block** — DO NOT include one. User has a canonical signature configured in Gmail that they will append manually before sending. Drafting any sig block (asterisks, phone, CDTM URL, address) just creates work for the user to delete.

**Salutation** — `Sehr geehrter Prof. <Surname>,` for German-speaking professors. Confirmed pattern from Henkel/Tryba/Grabmair/Ann threads.

**Why:** User established this style on 2026-05-20 after drafting the Ann email, having shipped Henkel/Grabmair under the older (verbose-sig, "Very best,") style and decided MiMI-first phrasing + kind-regards close + no-sig was the cleaner default. See [[reference_triage_operations]] for related Gmail draft conventions and [[feedback_gmail_html_rendering]] for the underlying gmail.py HTML fix.

**How to apply:** Default for any professor cold-email going forward. If the user explicitly requests "include the full signature" or a different sign-off, override. Do not transplant this style to non-professor outreach (founders, recruiters, vendor contacts) without checking — the formality + MiMI framing isn't universal.

**2026-09-08:** the no-signature-block rule is now UNIVERSAL, not professor-only - see [[feedback_email_no_signature_block]]. End every draft with a bare `Alessandro`.
