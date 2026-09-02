---
name: feedback_skills_install_on_both_machines
description: "Standing rule 2026-09-01: every new or updated skill gets installed on BOTH the laptop (~/.claude/skills/) and the DA VPS (/home/da/.claude/skills/), same turn."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-01T16:06:46.515Z
---

User rule (2026-09-01, while installing linkedin-outreach): "every skill from now on should go on both." Any skill created, installed from a zip, or meaningfully edited goes to BOTH machines in the same operation:

- Laptop: `~/.claude/skills/<name>/`
- Box: `/home/da/.claude/skills/<name>/` (scp + `chown -R da:da`)

**Why:** the box runs the savior + tg-bridge + all the migrated daemons; a skill existing only on the laptop is invisible to every box session, which is where more and more work happens.

**How to apply:** after writing/updating any `SKILL.md` (or command), scp it to the box path and chown. Same for `~/.claude/commands/`. The bulk baseline was synced 2026-09-01 (18 skills, 68 commands); this rule keeps the two from drifting. If a skill is inherently laptop-only (AHK, Obsidian, browser profiles), still copy it — the box copy is harmless and the box session will know its limits. See [[reference_vps_gdrive_mounts]], [[project_da_system]].
