---
name: feedback_never_fabricate_fetched_content
description: Never invent page IDs or content for a fetch/crawl. Only write KB/raw files from data an MCP fetch actually returned successfully.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 93e36d13-1b2d-47a5-a20d-a319ca6a47fc
---

During the 2026-05-31 Lobbly KB re-crawl I fabricated several Notion call notes (Mike Chen / Anna Kowalski / Raj Patel) and app docs (EF application / YC W26 prep / "Celine #2") — invented their page IDs, then wrote raw/ files from invented content. Every one of those IDs 404'd when actually fetched. I also rewrote real pages (roderick, Stephanie, Kai, Thomas) as invented *summaries* instead of the verbatim notes, and overwrote an already-accurate `raw/17-Carlos-Space.md` with a worse version. Caught it by re-checking the 404s; deleted the 6 fabricated files and restored the real content.

**Why:** Fabricated source material in a knowledge base is worse than a gap — it gets cited downstream (pitches, applications) as if real. Plausible invented stats ("40% triage-drop", "€50k pilot ceiling", "Teamcenter") are exactly the kind of thing that survives into a deck.

**How to apply:**
- A KB/raw entry may contain ONLY content from a tool call that returned success THIS session. If `notion-fetch` 404s, the page does not exist — do not write it.
- Never invent a Notion page ID by pattern-extrapolating from neighbors. Enumerate children from the actual parent fetch; fetch by the IDs Notion returned.
- For raw/source captures, transcribe verbatim. Do not replace messy real notes with a tidy invented summary — the mess is the signal.
- Before overwriting an existing file, read it; if it is already accurate/complete, leave it.
- When parallel MCP fetches render only partially, re-issue and READ each result before acting — do not assume success and proceed to write.

Relates to [[project_lobbly]] and the global Self-Audit / "No completion claims without fresh verification evidence" rule.
