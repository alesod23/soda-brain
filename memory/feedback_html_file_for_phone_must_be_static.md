---
name: feedback_html_file_for_phone_must_be_static
description: An HTML FILE sent by WhatsApp/Telegram must be a full static page (doctype, meta charset, no JavaScript) and be render-checked at phone width before it goes out
metadata:
  type: feedback
---

9 Oct 2026: I sent the hospital call sheet (an artifact page whose cards were drawn by JavaScript, no <meta charset>) as a .html file to Caleb on WhatsApp. On his Android viewer it showed an empty page with "路" for every "·". His words: "This what I see opening it... Make sure you can see what you sent (review what it shows)".

**Why:** phone file viewers (WhatsApp, Android HTML viewer) block scripts; without a charset the UTF-8 bytes are read as another encoding. An artifact page is a fragment wrapped by the artifact host, not a standalone file.

**How to apply:** render all content at build time (no <script>), start with `<!doctype html>` + `<meta charset="utf-8">` + viewport meta, then screenshot it at 390 px with the Playwright Chromium on the box (`~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome --headless --no-sandbox --window-size=390,1600 --screenshot=...`) and look at it before sending. Send to him first when he asks.
