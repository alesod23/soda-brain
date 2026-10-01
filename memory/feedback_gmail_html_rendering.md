---
name: feedback-gmail-html-rendering
description: "gmail.py now sends multipart/alternative; *bold* and <url> render properly. Don't hard-wrap paragraphs."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4e231641-76c4-4d05-8867-f3a9a9b1a6d8
---

`C:\Users\Alessandro\triage\gmail.py` was upgraded on 2026-05-20 to fix two recurring email-formatting bugs:

1. **`cmd_send` was sending plaintext-only** (single `MIMEText`). It now builds `multipart/alternative` with a parallel HTML version, matching `cmd_draft`.
2. **HTML version was just html-escaped plaintext** — so `*Name*` rendered as literal asterisks and `<http://url>` as bracketed text. New helper `_plaintext_to_html()` converts:
   - `*text*` → `<b>text</b>`
   - `<http(s)://...>` → clickable `<a href>` (angle brackets removed)
   - Newlines → `<br>`, rest `html.escape`d.

**Why:** Pre-fix, Grabmair/Niemann/Nitya cold emails went out as plaintext, so the recipient saw raw asterisks + angle-bracket URLs in the signature. The Ann draft surfaced the visual bug.

**How to apply when drafting bodies:**
- **Never hard-wrap paragraph text** at ~74 chars. Write each paragraph as ONE long line, separated by blank lines. Gmail compose wraps it narrower than 74, so hard newlines become visible mid-sentence breaks.
- Asterisks for bold (`*Name*`) and `<http://url>` for clickable links work as plaintext conventions — they auto-convert on send.
- When using `--body-file`, keep the file in this format; let the recipient's client soft-wrap.

If `gmail.py` ever gets rewritten, preserve `_plaintext_to_html()` and the multipart logic in both `cmd_send` and `cmd_draft`. Related: [[reference_triage_operations]], [[reference_triage_v2_reply]].
