---
name: feedback_wa_web_for_media
description: "To view images/files the user shares via WhatsApp, use the WA Web Playwright session — the wa-daemon store has no media bytes"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 668acb3f-a008-4138-ab8f-33f25fe5852a
---

When the user says they "sent a screenshot/image/file on WhatsApp" (e.g. their "Me" chat) for Claude to view, fetch it via the **WA Web Playwright session** at `~/.claude/wa-web-scrape/` (the logged-in Chrome profile), NOT the wa-daemon.

**Why:** the wa-daemon's `message-store.jsonl` only persists a `text:"[image]"` marker (see daemon.js `mapMessage`); it does NOT keep `mediaKey`/`directPath`/the raw proto, so Baileys `downloadMediaMessage` can't reconstruct the file. The daemon can't surface media. WA Web renders the actual image, so open the chat there and screenshot/download it.

**How to apply:** for any "I sent you an image/file on WA, go look" request, drive WA Web (reuse the wa-web-scrape persistent profile — don't spawn a fresh login), navigate to the named chat, capture/download the media, then Read it. Generalizes to all media the user drops in WA. Established 2026-06-07 during the Happy-phone pairing debug (needed to view app screenshots). Relates to [[reference_wa_web_scrape]] and [[reference_wa_sender]].

**Superseding path (2026-06-07):** the canonical phone→desktop drop is now the Google Drive **"From phone"** folder, synced locally by Google Drive for Desktop at **`G:\My Drive\From phone\`** (cdtm acct — see [[project_phone_to_desktop]]). Prefer asking the user to drop media there and read it with normal file tools; WA-Web scrape is the last-resort fallback for media already sent in WA.
