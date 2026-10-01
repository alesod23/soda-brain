---
name: reference_big_move_backup
description: "Laptop -> HEC OneDrive backup script (THE BIG MOVE) — re-runnable, what it includes/excludes"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 46508f81-7930-4552-98f2-d3f8ea3882e2
  modified: 2026-07-25T04:31:35.524Z
---

Idempotent laptop backup to HEC OneDrive. Script: `C:\Users\Alessandro\.claude\scripts\big-move-backup.ps1`. Dest: `OneDrive - HEC Paris\_LAPTOP-BACKUP\` (per-folder `robocopy /MIR`, log dir `_logs\`, `BACKUP-MANIFEST.md` at root). Built + first run verified 2026-06-06 (~2.79 GB, 31,949 files).

Re-run anytime: `powershell -File "C:\Users\Alessandro\.claude\scripts\big-move-backup.ps1"`.

INCLUDES (irreplaceable handmade, outside OneDrive): `.claude`, `task-land`, `vault_kb`, `07-thesis-kb`, `self-reflection-wiki`, `thesis-system`, `triage`, `.env` (secrets), `.lobbly-crm`, `hec-outlook`, `Coding`, `dev`, `Learning tech`, `siemens-deploy`. Project corpora already living INSIDE OneDrive (KG Patent Idea, cooked trips, etc.) are not re-copied — already backed up.

EXCLUDES (regenerable, by dir name via `/XD`): `node_modules`, venvs, `__pycache__`, build/dist/.next, and Chromium cache dirs (`Cache`, `Code Cache`, `GPUCache`, `Service Worker`, etc.) — this strips travel-search's ~3 GB cache while KEEPING cookies/logins. Also excludes volatile Claude session state (`shell-snapshots`, `telemetry`, `session-env`) but KEEPS `projects/` transcripts. Whole-home junk never touched: `AppData` (45 GB), `.linkedin-mcp` (7 GB venv), `.cache`/`.local`/`.vscode`.

STALE-INCLUDE-LIST RISK (learned 2026-07-24): the include list is a hardcoded array, so a renamed or newly created project folder is skipped SILENTLY (`SKIP (missing)` scrolls past). `thesis-kb` -> `07-thesis-kb` rename meant the thesis KB went unbacked-up for ~5 weeks. Every run, diff `Get-ChildItem ~ -Directory` against the array. Still NOT covered as of 2026-07-24, pending user's call: `medtech-brain`, `.medtech-crm`, `Zotero`, `mpd-kb`, `_kb-archive`, `cdtm-taskforce`, `tundra-outreach`, `sodaos`, `gtm-eng`, `gmail-snippets`, `radiocli`, `lobbly-kb`, `logos`, `.ssh`, `.config`, `stripe-shopper` (~220 MB total; `.ssh` keys + Tundra client material on HEC institutional OneDrive is the open question).

GOTCHAS: `.claude` reports ERROR(11) whenever browsers are live — only locked Chromium session files (`linkedin-pw`, `quick-claude` whatsapp session, GPU caches). Verified 2026-07-24: zero non-profile files failed, so no handmade loss; close those browsers to capture session logins. robocopy exit code 1 = SUCCESS (files copied); 0–7 ok, 8+ error — the wrapper's overall exit 1 is not a failure. Files landing in the OneDrive folder on disk are NOT yet cloud-uploaded; the tray icon must read "Up to date" before a laptop death is survivable. Secrets (`.env`, session tokens) now sit on HEC institutional OneDrive — flagged to user 2026-06-06; can exclude `.env` + browser-session dirs on request. See [[reference_env_files]], [[reference_onedrive_path]].
