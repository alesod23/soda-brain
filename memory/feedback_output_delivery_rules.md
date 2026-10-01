---
name: feedback_output_delivery_rules
description: "Canonical ordered ruleset for HOW Claude delivers output — file:/// links, clipboard, and auto-open (Obsidian/Comet). General rules apply by default; a skill's SKILL.md may override them locally."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f3457d46-d505-45b0-a458-a2e04efb2578
---

> **2026-09-02: COMET ABANDONED — every "Comet" below now means CHROME (the default browser). See [[feedback-browser-chrome-default]].**

The single source of truth for when to clipboard, when to give a `file:///` link, and when to auto-open a file. Settled with the user 2026-06-10. **TIER 0 = general rules (default everywhere); TIER 1 = a skill's own SKILL.md may override TIER 0 for its run.** Consolidates and points back to [[feedback_clickable_file_paths]], [[feedback_clipboard_all_paste_drafts]], [[feedback_message_send_protocol]].

## TIER 0 — general rules

### 1. `file:///` link — whenever I name a file the user might open
- Format: `file:///C:/Users/Alessandro/...` — forward slashes, drive letter kept, spaces → `%20`, **on its own line, plain text** (NOT code-fenced, NOT a markdown `[link]()`), so the terminal auto-linkifies it. Never hand a raw `C:\...` backslash path.
- Applies to EVERY file type and every file surfaced, **including files I also auto-open** (link + auto-open coexist).
- **Vault `.md` files get TWO extras:** (a) also print the bare Markdown filename (e.g. `2026-06-10.md`) on its own line so it can be pasted into Obsidian's search field, AND (b) **copy that filename to the clipboard** via `Set-Clipboard` (then verify with `Get-Clipboard -Raw`).

### 2. Auto-open
- **Obsidian vault `.md` → ALWAYS auto-open** via `Start-Process obsidian://open?vault=<vault>&file=<path>`. Covers `/daily`, `/audio-to-notes`, `/granola`, and ANY other `.md` written into a vault (not just the skills that already did it).
- **HTML deliverable → auto-open** via `Start-Process <file.html>` → resolves to the OS default handler = **Comet** (the user's daily driver). Confirmed 2026-06-10: default `.html`/`https` UserChoice ProgId = `CometHTM.PELFCJC3434QZISGBI3F5B2AYY`. This is the user's own default browser opening a deliverable, NOT browser automation — the Chrome-default / Comet-on-request rule [[feedback_browser_chrome_default]] governs Playwright/CDP control only, and does not conflict.
- **Email draft created → auto-open in Comet** via `Start-Process "https://mail.google.com/mail/?authuser=<account-email>#drafts/<message_id>"`. Lands on the correct account + opens the draft. Verified 2026-06-10 (cdtm + lobbly). Gmail lives in Comet, NOT Chrome — do not launch `chrome.exe`. See [[reference_triage_gmail.md]] / [[feedback_message_send_protocol]].
- **Calendar event created → ALWAYS auto-open** the event's `htmlLink` via `Start-Process "<htmlLink>"` so the user can eyeball it. Resolves to the OS default browser (Comet). Applies to every `create_event` (Google Calendar MCP) — link + auto-open coexist (still also print the `htmlLink` on its own line). Set 2026-06-10.
- **PDF deliverable I generate → ALWAYS auto-open** via `Start-Process <file.pdf>` (opens the OS default PDF handler). A finished report/doc/deck I rendered to PDF is a deliverable exactly like an HTML one: OPEN it, don't just link it. Scope = PDFs **I created as the deliverable**; NOT PDFs I downloaded/received or pre-existing reference PDFs. (Added 2026-06-23 — user called out that a 2-page report PDF was only linked, not opened, and wants this to never recur across sessions.)
- **All other file types** (.jsonl, .py, .txt, logs, downloaded/reference PDFs…) → **link only, no auto-open**.
- **Explicit verbal trigger** ("show me", "open it", "open in X") → open whatever the user points at, any type.

### 3. Clipboard (`Set-Clipboard`) — unchanged from prior rules
- **Clipboard:** pasteable drafts (essays, YC/app answers, form fields, bios, outreach, captions, AI-builder prompts); **real shell/terminal commands** I tell the user to run; the **DEFAULT message-send case** (draft + clipboard, then wait); **vault `.md` filenames** (new, per rule 1b).
- **Do NOT clipboard:** `/slash` commands (user types those); `dsend`/quoted-text sends (fire immediately); plain explanatory text / reports.
- **Honesty lock:** the words "copied / on your clipboard" may appear ONLY if `Set-Clipboard` actually ran THIS turn, verified via `Get-Clipboard -Raw`. Narrating an unexecuted copy is a lie.
- **Shell syntax:** `!`-prefixed = bash syntax (forward-slash paths, no `&` call op); PowerShell commands get PS syntax + a "separate window" note.

### 4. Message-send gate — unchanged ([[feedback_message_send_protocol]])
- `dsend`/`d send` = draft my wording + send now. Quoted `"..."` = send verbatim. Default = real platform draft (Gmail/Outlook where one exists) + clipboard + **wait for go-ahead**.

## TIER 1 — skills may override
A skill's `SKILL.md` can change any TIER 0 behavior for its own run (e.g. suppress the link, open a non-`.md` file). Skill instruction wins locally; TIER 0 is the fallback everywhere else.

## Where this is mirrored
CLAUDE.md › "Never Open Files or Browsers" (auto-open carve-out) and CLAUDE.md › Communication Standards (the `file:///` HARD RULE + vault `.md` extras) both point here. Gap "clipboard+file-link overlap for HTML" was left as-is per the user.
