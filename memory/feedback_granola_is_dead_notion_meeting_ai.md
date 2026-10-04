---
name: feedback_granola_is_dead_notion_meeting_ai
description: "Granola is dead (his ruling 4 Oct 2026): meeting notes come ONLY from Notion's meeting AI, read by the meeting loop; never read Granola, never propose /granola or the granola MCP."
since: 2026-10-04
metadata:
  type: feedback
---

His ruling (4 Oct 2026, goal run): "Granola is dead; meetings come from Notion's meeting AI; fix every node/loop that
still names Granola."

**Why:** he records calls with Notion's meeting AI now; the Granola MCP saw 0 notes for weeks (free tier, folders and
the public scope gone), yet the Granola-Auto-Sweep task kept running every morning and the maps still drew Granola as
the source of meetings.

**How to apply:**
- A meeting = a Notion meeting AI note. The ONE reader is the meeting loop `~/gtm-eng/agent/meeting_loop.py` (task
  DA-MeetingLoop, soda-brain `system/LOOPS.md` section 3). Never build a second reader.
- He hands you a Notion meeting page: `python ~/gtm-eng/agent/meeting_loop.py read <url>` (read-only) or `redo <url>`
  (a note of the last 24 h is read again on the next pass).
- Never call `mcp__granola__*`, never fetch `notes.granola.ai` for new work; an old Granola link = ask for the Notion page.
- Retired on 4 Oct: task Granola-Auto-Sweep (disabled, not deleted), `~/.claude/granola-auto/run.js` (exits unless
  `--force-retired`), `/granola` (now a redirect, old text kept under "Retired").
- Open, his to do: the `granola` MCP server in `~/.claude.json`, the Granola app autostart (HKCU Run `Granola`),
  the `/granola` mention in `~/.claude/CLAUDE.md` auto-open list.
- Older memories about Granola folders (`reference_mpd_granola_folder`, `reference_tundra_granola_folder`,
  `feedback_granola_reminder_next_day`) are history.
