---
name: reference_tool_mirrors
description: "Backup layout since 2026-09-10: task-land is the ONE shared repo; laptop tool folders (gtm-eng, triage, browser-extensions, quick-claude, claude-bar, hooks, AutoHotkey) are robocopy-mirrored into _system/laptop-tools/ and the box's approval-hub, sodanotif, triage into _system/box-tools/ by the git-sync scripts, secrets excluded. Mirrors are backups, never run from them."
metadata: 
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-10T14:24:55.817Z
---

**His fear (2026-09-10):** "when I restart this laptop, everything will be gone". Audit result: every piece autostarts (AHK via `_launch-all.ahk` startup shortcut, claude-bar via startup `.vbs`, intake/board servers via Coattio-Watchdog, box services via systemd/cron), so a reboot loses nothing. The real gap was BACKUP: seven laptop folders and three box folders lived outside every repo.

**Fix, his ruling: no new repos, reuse task-land** (he was confused by a "new GitHub repo" proposal; task-land already syncs laptop <-> GitHub <-> box).
- Laptop `_system/git-sync.ps1` step 0: `robocopy /MIR` of `~/gtm-eng`, `~/triage`, `~/browser-extensions`, `~/.claude/quick-claude`, `~/.claude/claude-bar`, `~/.claude/hooks`, `OneDrive\Documents\AutoHotkey` into `task-land/_system/laptop-tools/<name>/`. Excluded: tokens/, credentials.json, *token*.json, *.env, whatsapp-sessions, venv, node_modules, pids, logs, .qc-* state.
- Box `_system/vps/git-sync.sh` step 0: `rsync -a --delete` of `~/approval-hub`, `~/sodanotif`, `~/triage` into `task-land/_system/box-tools/<name>/`, same exclusions plus runtime state (stores/, state/, *.jsonl, state.json, push.env, pids).
- `.gitignore` carries the same secret patterns as a second guard. First commits verified: 267 laptop files, 61 box files, zero token/credential/env files tracked.

**How to apply:** to restore a tool, copy it OUT of the mirror to its real path; never edit or run inside `laptop-tools/` or `box-tools/` (the next sync overwrites them). gmail.py lives in both `triage` mirrors; the two machines' copies are kept identical by hand (scp + `.bak-<date>`). See [[reference_draft_review_lane]], [[project_da_system]].
