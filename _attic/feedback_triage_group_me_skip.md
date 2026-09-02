---
name: Triage skip rule — "group: Me"
description: The WhatsApp group labeled "Me" is NEVER actionable in triage. Always skip silently regardless of content.
type: feedback
originSessionId: 9c5fc629-1542-42c2-b104-c7138c67d213
---
The WA group whose label is literally `Me` (jid `120363023505333085@g.us`) is **never actionable**. Skip silently in every triage round, regardless of message content (announcements, task asks, links, anything).

**Why:** User confirmed 2026-05-11 that this group's content is never something he needs to act on from triage. Treat it the same way as `status@broadcast`, Renata image-only messages, etc — a per-chat permanent skip rule.

**How to apply:** In the WA classification step of `/triage`, before any other LLM judgment, if `label === "group: Me "` OR jid `=== "120363023505333085@g.us"` → drop the item, do not display, do not count as actionable. No need to add to `wa-state.json#done` (it's a classifier skip, not state).
