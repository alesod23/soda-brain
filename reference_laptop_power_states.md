---
name: reference_laptop_power_states
description: "The laptop is Modern-Standby-only (no S1/S2/S3), so SetSuspendState hibernates instead of sleeping — Ctrl+Alt+F12 looks like a shutdown"
metadata: 
  node_type: memory
  type: reference
  originSessionId: bcf4ed36-d8ed-4e48-817b-146c5998e5ca
  modified: 2026-08-06T16:59:12.454Z
---

`powercfg /a` on DESKTOP-1BOJSRG: only **Standby (S0 Low Power Idle) Network Connected**, **Hibernate** and **Fast Startup** are available. S1/S2/S3 are all unavailable (firmware + S0ix). Hybrid Sleep is listed as unavailable too (it needs S3), even though `HYBRIDSLEEP` is set to 1 in the scheme.

**Consequence:** `DllCall("PowrProf\SetSuspendState", 0, 0, 0)` in `OneDrive - HEC Paris\Documents\AutoHotkey\Sleep and screen off (ctrl alt f11 f12).ahk` (Ctrl+Alt+F12) requests a legacy S3 suspend, finds no S3, and falls through to **Hibernate (S4)**. Confirmed 2026-08-06 from the event log: Kernel-Power **event 42 with TargetState=5** (Hibernate) on 8/5 17:13, followed by Kernel-Boot **event 27 boot type 0x2** (hiberfile resume). This is why the hotkey looks like it powers the laptop off. Ctrl+Alt+F11 (screen off via `WM_SYSCOMMAND`/`SC_MONITORPOWER`) is unaffected.

Fix if he wants real sleep: `powercfg /h off` (admin) removes the hiberfile so the call lands in S0 standby; the cost is losing hibernate and Fast Startup. **Not applied — awaiting his go.**

Reading power events: TargetState/EffectiveState use `SYSTEM_POWER_STATE` (1=Working, 4=S3, **5=Hibernate**, 6=Shutdown). Kernel-Boot 27 boot type: **0x0=cold boot, 0x1/0x2=hiberfile resume**. Event 41 + EventLog 6008 = unclean power loss (one happened 2026-08-06 11:29:26, Bugcheck=0, no power-button flag, unrelated to the hotkey).
