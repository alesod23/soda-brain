---
name: feedback-schtasks-vbs-wrapper-no-console-flash
description: "Scheduled tasks must exec wscript.exe + hidden .vbs wrapper, never powershell.exe directly — direct exec flashes a console window every trigger"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b75b1302-8e9b-4e42-b796-f57031e2eebf
---

A Task Scheduler action that executes `powershell.exe` directly flashes a visible conhost window on EVERY trigger, even with `-WindowStyle Hidden`. Two 5-min watchdog tasks registered this way on 2026-07-18 made a terminal window pop and close every few minutes until the user complained ("I'm sick of it. It should be headless").

**Why:** `-WindowStyle Hidden` only hides the window after the console host has already been created and shown; wscript.exe is a windowless host, and `WScript.Shell.Run "...", 0, False` starts the child with window style 0 from the start.

**How to apply:** any repeating scheduled task on this machine that runs a console app (powershell, node, python) gets a `.vbs` wrapper: `CreateObject("WScript.Shell").Run "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File ""<script>""", 0, False`, and the task action is `wscript.exe //B //Nologo "<wrapper.vbs>"`. This is the established house pattern (SODANOtif-Watch/Recap, Coattio-Watchdog, WA-Daemon-Watchdog, DailySync-Watchdog all do it). Wrappers live next to their .ps1. See [[reference_sodanotif]], [[reference_wa_scheduled_sends]].
