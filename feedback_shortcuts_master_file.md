---
name: feedback_shortcuts_master_file
description: "task-land/_system/SHORTCUTS.md is the master list of every hotkey/hotstring/alias/skill; MUST be updated in the same turn any shortcut is created, changed, or removed"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-02T17:37:24.457Z
---

`C:\Users\Alessandro\task-land\_system\SHORTCUTS.md` (repo-synced to GitHub and the box) is the "onboarding to my life" file: every AHK hotkey, hotstring, PowerShell alias, ssh host, slash-command skill, Telegram bot command, and safe word, in one place.

**Why:** the user asked for it explicitly on 2026-09-02 ("create a file you MUST UPDATE each time with all the shortcuts, like an onboarding to my life, constantly updated"). Shortcuts were scattered across 16 AHK files, the PS profile, and a dozen memory files, and the memory counts had drifted (9 vs 15 daemons; Ctrl+Alt+S listed live but disabled).

**How to apply:** whenever a shortcut/alias/skill/bot command is added, renamed, rebound, disabled, or deleted (by `/ahk`, `/skill-creator`, profile edits, or by hand), edit SHORTCUTS.md in the same turn, before reporting done. Delete stale rows, do not annotate them. Link it whenever the user asks "what is the shortcut for X". See [[reference_ahk_autostart]], [[feedback_skills_install_on_both_machines]].
