---
name: html-deliverable-browser-url
description: "HARD RULE — every time you write/produce an HTML file the user will view, end the response with a bare plain-text file:/// URL on its own line (clickable) + Set-Clipboard. Applies in EVERY chat, no exceptions."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7015c673-ec0d-448d-be2e-afb6c9236d1e
---

# HARD RULE — applies in every session, every project, no exceptions

Whenever you produce or update an HTML artifact the user will open in a browser (dashboard, report, mockup, rendered page, exported doc), you MUST end that response with:

1. **The full `file:///` URL as plain text on its OWN LINE — NOT inside a code fence, NOT as a `[text](url)` markdown link, NOT inline mid-sentence.** Bare plain-text URLs auto-linkify (become clickable) in the Claude Code terminal; code-fenced or markdown-wrapped ones do NOT. URL-encode spaces as `%20`.
2. **`Set-Clipboard -Value $url`** in the same turn (best-effort; if the clipboard is locked, the printed link still satisfies the rule).

## This was reinforced TWICE on 2026-05-24

> "I ACTUALLY LOVE THAT YOU PUT THE FULL THING BC IT BECAME A LINK. ENSURE TO ALWAYS DO THAT WHEN YOU RETURN ME AN HTML THING."

Then again, after catching a chat where I forgot: *"I just checked and you didnt in another chat (SAVE IT by memory)."* — so the failure mode is FORGETTING to do it, not doing it wrong. Treat this as a checklist item that fires on every HTML deliverable, the same way the self-audit fires before completion claims.

**Why:** naming the Windows disk path alone is friction — the user has to convert backslashes, escape spaces, prefix `file:///` by hand. A bare clickable link = one click to open. Clipboard = backup paste path.

**How to apply:** fires on any HTML the user will view visually (typically under OneDrive `KG Patent Idea\`, `cooked trips\`, or a localhost-served file). Does NOT apply to HTML fragments embedded in other docs, or HTML written to temp paths purely for tool consumption. Format: `file:///C:/full/path/with/%20encoded/spaces.html`, on its own line, no backticks, no markdown link wrapping.

Related: [[reference_onedrive_path]] (OneDrive = `C:\Users\Alessandro\OneDrive - HEC Paris\`, which encodes to `OneDrive%20-%20HEC%20Paris`). Localhost-served HTML belongs to that session only per [[feedback_curriculum_tracker]].
