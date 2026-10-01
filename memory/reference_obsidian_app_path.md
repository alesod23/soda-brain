---
name: reference_obsidian_app_path
description: "Obsidian app executable path on this machine (verified) — for launching the app, distinct from the vault data folders."
metadata: 
  node_type: memory
  type: reference
  originSessionId: ee7b018d-be80-452d-afe0-260d146975b1
---

Obsidian (the application) is installed per-user at:

`C:\Users\Alessandro\AppData\Local\Programs\Obsidian\Obsidian.exe`

(Working dir: the same folder. Start Menu shortcut: `AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Obsidian.lnk`.)

**Not** the commonly-assumed `AppData\Local\Obsidian\Obsidian.exe` — newer Obsidian installers use `Local\Programs\`. Verified by resolving the .lnk target (Test-Path True) on 2026-06-06.

This is the APP exe, separate from the vault DATA folders: `~/task-land/` (tasks), `~/kb/` (knowledge), `~/thesis-kb/`, `~/vault_kb/`, `~/self-reflection-wiki`. To open a vault by URI without needing the exe, prefer `obsidian://open?vault=<task-land|kb>&file=<path>`. See [[reference_vault]], [[reference_kb_vault]], [[reference_kb_systems]].
