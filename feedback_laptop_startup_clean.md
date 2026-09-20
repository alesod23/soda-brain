---
name: feedback_laptop_startup_clean
description: "Laptop startup opens NOTHING visible — no terminals, no Quick Claude, no widgets. He opens his own PowerShell and runs Restore-CC + Restore-Savior himself."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 26333c6f-5f43-43b7-badf-07594a1db485
  modified: 2026-09-02T17:37:53.707Z
---

**Standing rule (set 2026-08-05):** a Windows login must leave the screen **empty**. Nothing I
build or configure may open a terminal window, a Claude session, or an on-screen widget by itself
at boot. His words: *"I don't want you to open quick claude nor open terminal windows and leave
them there (you always open up too many). I'd like to just open my own MS PS and run my restore cc
and restore savior… nothing else."*

**The startup he wants** — one PowerShell window that he opens, in which he runs:
- `Restore-CC` → reopens the pre-restart Claude Code tabs ([[reference_restore_cc]])
- `Restore-Savior` → this terminal becomes the always-on Telegram savior lane

Both are functions in `$PROFILE`
(`OneDrive - HEC Paris\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`). That profile
is fine as-is — it only defines functions and prints a once-per-boot tip. Don't add anything to it
that *launches*.

**Why:** he ends up with a screen full of terminals he didn't ask for and can't tell apart, and a
savior lane started by a shortcut is one he never chose to start. Auto-started windows also make
"which session is which" unanswerable, which is the exact problem `Restore-CC`'s pick-prompt exists
to solve. Background work is welcome — **hidden** background work. Visible windows are his to open.

**Cleaned up 2026-08-05 (the three offenders, all verified live):**
- `Savior-V3.lnk` in `shell:startup` — `powershell -NoExit -File start-savior2.ps1`, i.e. a
  permanent terminal window every boot. **Moved to** `~\.claude\scripts\startup-disabled\`
  (restore = move it back). `Restore-Savior` replaces it.
- `quick claude (alt win j).ahk` — pre-warmed a Windows Terminal panel at AHK launch. Pre-warm
  **removed**; the panel is now created on the first `Alt+Win+J`. Cost: the first invocation pays
  the claude cold start. ([[reference_quick_claude]] — note the hotkey is Alt+Win+J, not Ctrl+Alt+Q.)
- `coattio KPI widget (ctrl alt s).ahk` — showed the always-on-top KPI overlay at login.
  Now created with `Show("Hide …")` and `gVisible := false`, so **Ctrl+Alt+S is the only way it
  appears**; the 15s poll of `localhost:4124` is armed on show and disarmed on hide.
  UPDATE 2026-09-02: the script is now `_disabled - coattio KPI widget (ctrl alt s).ahk`, skipped by
  the launcher, so Ctrl+Alt+S is bound to nothing. Master list: [[feedback_shortcuts_master_file]].

**How to apply going forward:** anything that must run at boot goes in as a hidden background
worker — a Task Scheduler job launching a `wscript //B` `.vbs`
([[feedback_schtasks_vbs_wrapper_no_console_flash]]) or a `-WindowStyle Hidden` powershell action.
Never a `shell:startup` `.lnk` to `powershell -NoExit`, never `wt.exe`, never an AHK GUI that
`Show()`s at load. An AHK script may *bind* a hotkey at login; it may not *display* anything until
the hotkey is pressed. Before declaring a startup clean, verify with the login-triggered task list
and the `shell:startup` folder, and confirm no visible top-level window belongs to the process.

**This extends past boot: don't leave terminal windows lying around mid-session either.** *"You
always open up too many."* Anything I start for my own purposes runs hidden/detached and gets
cleaned up; a visible window is only justified when he asked to see something running, and then I
say what it is and close it when done.

Related: [[reference_ahk_autostart]], [[feedback_local_server_start_pattern]],
[[feedback_no_polling_on_background_tasks]], [[feedback_rule_requests_are_binding]].

**2026-09-20: never park anything in a SUBFOLDER of the Startup folder.** Windows launches every shell item in `...\Start Menu\Programs\Startup`, and a folder item is "launched" by opening it in Explorer: the `Startup\_disabled\` folder (granola-auto-watch.vbs, OpenWhispr.lnk) popped an Explorer window at every logon ("a disabled folder with open wispr is open on file location"). Parked startup items now live in the sibling `...\Programs\Startup-disabled\` (outside Startup); anything else to disable goes there, never into Startup itself.
