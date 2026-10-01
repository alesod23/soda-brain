---
name: feedback-file-path-clickable-url
description: "ALWAYS present any file location to the user as a clickable file:/// URL, every time, in every session — never a raw C:\\ path."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5b79f08b-7900-4194-840e-4800be587dbe
---

Every time you mention a file location to the user, format it as a clickable `file:///` URL — NOT a raw `C:\...` path. This applies to ANY file reference (briefs, scripts, data files, dashboards, configs — anything), not just HTML deliverables.

**Why:** Raw Windows paths aren't clickable; the user wants to click a file location and have it open. They demanded this explicitly and with frustration on 2026-05-26, and said it must apply across ALL sessions/chats, every single instance — treat as a hard, permanent rule.

**How to apply:**
- Convert absolute path → file URL: `C:\X\Y Z\f.md` → `file:///C:/X/Y%20Z/f.md`. Rules: prefix `file:///`, backslashes `\` → forward slashes `/`, spaces → `%20`, percent-encode other special chars as needed.
- Print it as **bare plain text on its own line** — NOT inside a code fence, NOT as a `[markdown](link)` — so the terminal auto-linkifies it.
- Use the real synced OneDrive root when relevant: `C:\Users\Alessandro\OneDrive - HEC Paris\` → `file:///C:/Users/Alessandro/OneDrive%20-%20HEC%20Paris/` (see [[reference_onedrive_path]]).
- For HTML files the user will view, ALSO copy to clipboard via Set-Clipboard per [[feedback_html_deliverable_browser_url]]. This rule generalizes that one to every file type.
