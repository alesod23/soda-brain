---
name: feedback_daily_full_section_contract
description: "/daily must ALWAYS render all sections (Today/Inbox/Habits/Next7/Waiting) from source folders, never copy the prior note's skeleton; truncation self-propagates"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b368b9f8-3891-4177-926b-c83d59a190ae
---

On 2026-06-08/09 the daily page lost Habits, Next 7 days, Waiting, and most of Inbox — only `## Today` survived. Root cause: a `/daily` run (the `/dump`-triggered one, no weather line) emitted only `## Today`, and the next day's run read that truncated note **as its structural template** and reproduced the gap. The data was never lost (it lives in `task-land/Tasks/` + `Habits/`); the page is only a rendered view. Section drop-off self-propagates because COMPOSE treated the prior note as the skeleton.

**Why:** the skill was pure LLM-discretion with no output contract and no verification, so any hurried/sub-run could silently shrink the note and the loss compounded forever.

**How to apply:** Engine hardened in `~/.claude/commands/daily/SKILL.md` — step 10 now has a 🔒 OUTPUT CONTRACT (Habits ALWAYS all-5; Inbox/Next7/Waiting whenever their folder is non-empty; **regenerate every section from the source folders each run, never copy the prior note's section structure**), plus step 12b SELF-VERIFY (re-read the written file, assert each section vs source, regenerate on any miss before finishing) and step 12c SANITY (never write a note that drops a section whose folder is still non-empty). `/dump` step 7 reworded from "rebuilds Today + Inbox" → "rebuilds the FULL daily note + must pass step-12b". A daily note containing only `## Today` is a FAILED compose, never acceptable. Side effect of the original bug: habit streaks froze for 2 days (step 4 leaves a habit alone if its section was missing) — restore/recompute manually if it recurs. See [[reference_daily_briefing]], [[feedback_daily_dedup_today_page]].
