---
name: reference_ahk_autostart
description: "Which folder AHK scripts must live in to auto-run at login, and where the TODO/daily hotkeys are"
metadata: 
  node_type: memory
  type: reference
  originSessionId: e26e83a8-1688-47b2-bb78-0136884ee95a
  modified: 2026-08-05T20:29:03.139Z
---

AHK auto-start is driven by `shell:startup` shortcut **AHK Launch All** → `OneDrive - HEC Paris\Documents\AutoHotkey\_launch-all.ahk`, which runs every `.ahk` **in that one folder** (skips names starting with `_`).

TRAP: the `/ahk` skill saves to `C:\Users\Alessandro\AutoHotkey\` — NOT the launched folder — so those scripts never autostart. Any script that must run at login MUST live in `OneDrive - HEC Paris\Documents\AutoHotkey\`. (`:` is illegal in Windows filenames — never put `::td` literally in a filename.)

**HARD RULE (2026-08-05): a script in this folder may BIND a hotkey at login, it may NOT DISPLAY
anything.** No `Gui.Show()` at load, no `Run`-ing a terminal at load. Everything waits for the
keypress. Two scripts violated this and were fixed: `quick claude (alt win j).ahk` pre-warmed a
Windows Terminal panel (pre-warm deleted), `coattio KPI widget (ctrl alt s).ahk` showed its overlay
(now `Show("Hide …")` + `gVisible := false`, poll armed on show / disarmed on hide). See
[[feedback_laptop_startup_clean]].

Current hotkeys there:
- `::td` hotstring → `todo-assistant (td hotstring).ahk` (runs /rename TODO ASSISTANT then /color pink in Claude Code).
- `::sa` hotstring → `savior-3 (sa hotstring).ahk` (added 2026-06-30): runs `/rename savior 3 (DD-MM)` (today's date, filled at run time via `A_DD`/`A_MM`) then `/color green` in Claude Code. Mirrors `::td`. Titles+greens the always-on savior session; the "savior" title is also what `cc-sessions.ps1` (Restore-CC) matches to exclude that session from plain `claude -r` resume and give it its own start-savior2.ps1 tab. Pinned local (+P -U) so it autostarts.
- `Ctrl+Alt+T` → `Open daily page (ctrl alt t).ahk` opens the newest `task-land\Daily\YYYY-MM-DD.md` in Obsidian (`obsidian://open?vault=task-land&file=Daily/<date>`). Replaced the old Notepad TODO.md opener (2026-06-20). See [[reference_daily_briefing]].
- `Shift+Alt+G` → `Grammarly toggle global on-off (shift alt g).ahk` (added 2026-06-23): kills/launches `Grammarly.Desktop.exe` (launch uses `--autostart` → quiet to tray). Grammarly is now OFF by default — its HKCU `...Run\Grammarly` autostart value was DELETED (restore: `reg add` that key with the exe path + `--autostart`). Chosen over a Comet block-list toggle because Grammarly's Block List is **cloud/account-synced, NOT on disk** (verified: "comet" appears on disk only as floating-button position in `ButtonPositions.json` + editor cache in the `storage_v3_*.db` SQLite, never as a block entry) — so no file edit can toggle it. Distinct from the existing `Alt+G` (tab menu navigate); no conflict.

**ROOT CAUSE OF "shortcuts not up after a restart" (diagnosed 2026-06-27):** TWO compounding issues, check BOTH:
1. **The machine may not have actually rebooted.** `shell:startup` shortcuts only fire on a real Windows login. Verify with `(Get-CimInstance Win32_OperatingSystem).LastBootUpTime` — if it's days old, the user "restarted" an app/terminal/Claude, NOT Windows, so the launcher never re-ran. (On 2026-06-27 uptime was 6 days while the user thought they'd restarted.)
2. **The AHK files are OneDrive online-only placeholders.** `Get-Item _launch-all.ahk` showed `Attributes=Archive, ReparsePoint` = a Files-On-Demand placeholder. At login the Startup shortcut fires BEFORE OneDrive hydrates, so `Run()` of each placeholder `.ahk` fails silently and the hotkeys never come up (only manually-launched scripts survive). **FIX (done 2026-06-27): pin the whole folder to "Always keep on this device"** so the files are real local bytes, never placeholders: `cmd /c 'attrib +P -U "C:\Users\Alessandro\OneDrive - HEC Paris\Documents\AutoHotkey\*" /S'` (pinned attr = 0x80000; verify the launcher's Attributes no longer says ReparsePoint-only). Keep it pinned.

**To restore shortcuts mid-session** (no reboot needed): stop existing AHK (`Get-Process AutoHotkey* | Stop-Process -Force` — these are restartable hotkey daemons, zero saved state) then relaunch all via `& "C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe" "<folder>\_launch-all.ahk"`. Verify with `Get-Process AutoHotkey*` → expect one process per non-`_` script (9 as of 2026-06-27).

GOTCHA (AHK v2): `>` `<` between strings does a NUMERIC compare and throws "Expected a Number but got an empty string" on an empty seed. For string/lexical compare use `StrCompare(a, b) > 0`.
