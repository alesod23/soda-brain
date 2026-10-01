---
name: feedback_dynamic_html_default
description: "Default to a NORMAL static HTML when asked for HTML; only build the server-backed dynamic-html when the user says 'dynamic'"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: eb084d3b-d52c-4019-a66b-a623cfb28a25
---

When Alessandro asks to "turn this into an HTML file" (e.g. "easy to navigate, complete for a human reader, auto-updates every iteration"), DEFAULT to a plain static `.html` deliverable as before.

Only build the [[reference_dynamic_html]] server-backed version (autosave + per-answer/whole-form comment boxes + live-reload) when he explicitly says **"dynamic"** (e.g. "make it a dynamic html"). He reserves a deliberate two-way choice: normal html vs dynamic html.

**Why:** dynamic html spins up the local server + a tool folder; that overhead is unwanted for a one-off report he just wants to read. Stated 2026-06-23.

**How to apply:** parse the request for the word "dynamic" (or an explicit ask for the comment-box/auto-update behavior). Absent that → normal static HTML (still honor the auto-open + `file:///` link rules). Present → scaffold a new `tools/<name>/` under the dynamic-html system.
