---
name: feedback_raw_note_filename_month_day
description: "When an assistant/skill writes a KB Raw note, name it \"MM-DD Title\" (month-day only, NO year) so the title stays readable in Obsidian's sidebar"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b368b9f8-3891-4177-926b-c83d59a190ae
---

When an assistant or skill writes a note into any vault's `Raw/` folder, the filename MUST be `MM-DD <Title>` — **month-day only, no year** (e.g. `06-09 Plan with Caleb - thesis kickoff.md`). NEVER prefix with the full `YYYY-MM-DD`.

**Why:** the year eats sidebar width in Obsidian and truncates the title — the part Alessandro actually reads. He flagged this 2026-06-09 with a screenshot of `2026-06-09 KB system idea - emai…` rows where the title was cut off. Month-day is enough to sort/disambiguate within a vault.

**How to apply:** Filename = `MM-DD <Title>` (human-readable spaces fine). Keep the full date in `created: YYYY-MM-DD` inside frontmatter/body, never in the filename. Applies to EVERY vault's Raw (vault_kb, thesis-kb, self-reflection-wiki) and every writer: `/dump` notes+questions, `/audio-to-notes`, manual agent writes, future `/granola`-style drops. Encoded in: `~/.claude/commands/dump/SKILL.md`, `~/.claude/commands/audio-to-notes/SKILL.md`, and `vault_kb/CLAUDE.md` "Quick capture into Raw/". Existing `YYYY-MM-DD…` Raw files were left as-is (renaming risks breaking `Sources/` `raw:` links); bulk-rename only on explicit request, rewriting referencing links too. See [[reference_kb_systems]], [[reference_kb_vault]].
