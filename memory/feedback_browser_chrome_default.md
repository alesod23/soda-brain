---
name: feedback-browser-chrome-default
description: "COMET IS ABANDONED (user, 2026-09-02): never open or automate it again, for anything. Chrome is the ONLY browser — daily driver (CDTM profile), OS default handler, and all Playwright/CDP automation. Every old 'Comet exception' (trippy SNCF, WA Web, email drafts, HTML auto-open) now means Chrome."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7528a222-3515-4a7e-95d0-39ba429ccc6d
  modified: 2026-09-01T22:33:56.068Z
---

# COMET ABANDONED — Chrome only (2026-09-02)

User: "im officially abandoning comet. dont want to use it ever again. fully
shifting to chrome. on a cdtm account." This supersedes EVERY older rule,
memory line, or skill note that says to open, attach to, or fall back to Comet.
If any other file still says "Comet", read it as "Chrome (default browser)".

- **Daily driver:** Chrome, signed into the CDTM Google account
  (alessandro.sodano@cdtm.com). It is/becomes the OS default handler, so
  `Start-Process <url|file.html>` opens Chrome.
- **Automation:** Chrome only, as it always was:
  `C:\Program Files\Google\Chrome\Application\chrome.exe`, dedicated
  `user-data-dir` per skill, never his real profile.
- **Never launch `comet.exe` again** — not for trippy, not for WA Web, not for
  anything, not even "on explicit request" unless he reverses this rule in
  writing. Old Comet profiles (`travel-search\profile-comet\`,
  `lobbly-research\profile-comet\`, `approval-hub\whatsapp-sessions\`) are dead
  weight, kept only until he confirms deletion.

## Trippy (the old "Comet exception" — now Chrome)

The logged-in-carriers rationale still holds, the browser changed: trippy's
booking funnels / deep dives use a dedicated **Chrome** profile (e.g.
`travel-search\profile-chrome\`), attach via CDP to a running instance
(`--remote-debugging-port=9222 --user-data-dir=<profile>`), leave the window
open at checkout for the user to pay. **First use after the migration: the user
must log the carriers into that fresh profile** (Volotea, easyJet, Ryanair,
ITA, bahn.de, sncf-connect, italo) — until then expect aggregator-level prices
and say so rather than silently accepting them.

## Applies everywhere

Same rule on the VPS (headless chromium/Chrome for any browser work there).
Old references absorbed: `_attic/feedback_browser_comet.md`, the trippy-SNCF
Comet exception, [[feedback_open_wa_web_in_comet]] and
[[feedback_open_email_drafts_in_comet]] (both updated to Chrome),
[[feedback_output_delivery_rules]] (auto-opens land in Chrome now).
