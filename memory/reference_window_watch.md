---
name: reference-window-watch
description: "No console window ever in front of him - the recorder that names who opened each one, the lint of scheduled tasks, run-hidden.vbs; rules for anything I build"
metadata:
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-28T12:25:30.362Z
---

His rule, 2026-09-28: "i need a reviewer/rule to ensure tht you never open a random window of ms powershell in front
of me because of a poller/claude.exe. it happens. even more when i build something new".

**Rules for anything I build or schedule:**
- A scheduled task NEVER runs powershell, cmd, python, node or a .cmd directly. It runs
  `wscript.exe //B //Nologo "...\task-land\_system\window-watch\run-hidden.vbs" "<workdir>" "<log or ->" <program> <args>`
  (or its own .vbs). `-WindowStyle Hidden` is not enough, it flashes.
- Python that spawns: `creationflags=subprocess.CREATE_NO_WINDOW`. Node: `windowsHide: true`, never `detached` with a
  console program. A long-running background Python = `pythonw.exe`.
- After creating or changing a task: `python task-land/_system/window-watch/window_lint.py` must list nothing.

**The reviewer:** `task-land/_system/window-watch/window_watch.py` (task DA-WindowWatch, pythonw) looks at the screen
four times a second; every new console or Terminal window is a line in `windows.jsonl` with the program in it, who
started it, the chain up to the script or session, and how long it stayed. Verdict `his` when Explorer started the
shell. The system agent reads it at every run: a window by the system = an incident with the culprit named.
`window_lint.py --fix` rewraps tasks; originals in `task-originals.json`, `--restore <task>` undoes.

On day one the lint found five tasks opening a window: Archive-Screenshots, Curriculum-Daily-Crawl,
Curriculum-Weekly-Crawl, DailyCampaign-AB-Reminder, US-Campaign-Daily. All rewrapped.

Related: [[reference-interactive-console-tasks-open-windows]], [[reference-system-agent]].
