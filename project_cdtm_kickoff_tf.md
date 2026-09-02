---
name: project_cdtm_kickoff_tf
description: "CDTM kickoff taskforce work — folder, session note, progress tracker, Friday weekly-update draft system"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2c6881fb-6fd3-4d90-a9ae-1fcdef10bea0
---

CDTM Onboarding/Kickoff Taskforce (Spring 2026 class). Alessandro is a kickoff captain alongside Raunaq Jain (lead), Giulia Balzaretti, Simon Peter. Reports weekly to `raunaq.jain@cdtm.com`.

**Recall in a new chat: the `/cdtm` skill** (`~/.claude/skills/cdtm/SKILL.md`) — it reads `_START-HERE.md` + `progress.json` first, prints a Done/In-progress/Next snapshot, then works whatever workload the user names (or an onboarding item that surfaced from /daily or /triage). Also fires on "cdtm" / "kickoff taskforce".

**All work lives in `C:\Users\Alessandro\cdtm-taskforce\`** (read with normal file tools). **In a new chat, READ `_START-HERE.md` FIRST, then `progress.json`** — that fully orients you.
- `_START-HERE.md` — orientation contract: folder map, how-to-work, key people/emails/dates, open items.
- `SESSION-NOTE-2026-06-17-raunaq.md` — canonical plan: his items split into 8 workloads (WL1–WL8) ordered by when-to-do, with materials/templates/links and 🔗 joint-with-Raunaq flags. Built from the 17 Jun transcript + the planning sheet.
- `links.json` — all 140 cell hyperlinks extracted from the master sheet (templates, decks, forms).
- `progress.json` — LIVING tracker. When a workload is worked on, append `{"date","note"}` to its `log` and flip `status` (todo→in_progress→done). This is the "context" the weekly email pulls from.
- `weekly_update.py` — drafts the weekly status email to Raunaq into cdtm Gmail drafts (never sends). Uses `~/triage/gmail.py draft --account cdtm`. Run manually any time.
- `extract_links.py` / `register-task.ps1`.

**Friday automation:** scheduled task `CDTM-Kickoff-Weekly-Update` runs `weekly_update.py` every Fri 16:00 → fresh draft sits in cdtm drafts for Alessandro to review/send. To refresh content, just keep `progress.json` current.

**The master planning sheet** is login-walled (Google). Read it via Drive MCP `read_file_content` (text, drops hyperlinks) or export XLSX via `download_file_content` (exportMimeType=…spreadsheetml.sheet) then openpyxl for `cell.hyperlink` — anonymous HTTP 401s. Sheet id `1AdK3RduGEZEgbtyT_Xcm6V9ShlbUmWEg8FaoY878wNA`.

Fixed dates (in `CONTEXT-dates-class.md`): class = **Fall 2026**; onboarding survey closes **31 Jul** (gates Who's-Who + big email); **Pre-Kickoff Tue 18 Aug** at CDTM (welcome speeches ~17:00); **Kickoff Fri 21-Sun 23 Aug** Burghausen; Alessandro's "Navigating Life" session Sun 23 Aug 9:30. Speakers: Prof. **Klaus Diepold** kldi@tum.de (alt Jelena Spanjol spanjol@lmu.de), alumni Andi Franz + Matthias Möller. gmail.py `draft` now supports `--cc`. See [[reference_triage_gmail]] for the cdtm gmail helper.
