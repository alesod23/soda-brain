---
name: feedback_clickable_file_paths
description: "Every file path surfaced to the user must be a clickable file:/// link, not a raw Windows path — applies to ALL file types, every session"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3fe86535-4f90-4bac-b07c-2b7763f6b0cb
---

Whenever you tell the user about a file they might open (ANY extension: .jsonl, .txt, .py, .md, .html, .pdf, logs, exports, ...), output it as a clickable `file:///` URL, never a raw `C:\...` backslash path.

Format: `file:///C:/Users/Alessandro/...` — forward slashes, keep the drive letter, encode spaces as `%20`, put it on its OWN LINE as plain text (NOT code-fenced, NOT a markdown `[link](...)`), so the terminal auto-linkifies it.

**Why:** A raw `C:\Users\...\file.jsonl` is dead text in the terminal — the user can't click it, has to hand-copy a long path. They flagged this with visible frustration on 2026-05-26 ("why are you giving me this not in a file: format that i can click on?"), noting we had already agreed on it. It is forgetting, not disagreement, so treat it as a completion-checklist item on every turn that names a file.

**How to apply:** Before sending any message that references a file path, convert it to the `file:///` form on its own line. This generalizes the HTML-only rule [[feedback_html_deliverable_browser_url]] (which adds clipboard + browser-open semantics for `.html` specifically) to every file type. Mirrored as a HARD RULE in CLAUDE.md > Communication Standards.
