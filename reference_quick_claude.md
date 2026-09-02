---
name: reference-quick-claude
description: Quick Claude — Ctrl+Alt+Q laptop hotkey → screenshot + dictated request → ephemeral claude -p executes → receipt to Claudio TG
metadata: 
  node_type: memory
  type: reference
  originSessionId: b75b1302-8e9b-4e42-b796-f57031e2eebf
  modified: 2026-08-05T20:29:16.121Z
---

**CURRENT HOTKEY IS `Alt+Win+J`** (`quick claude (alt win j).ahk`; `Ctrl+Alt+H` kept as a synthetic-chord fallback; the old `ctrl alt q`/`ctrl alt h` script is `_disabled -` prefixed). **NO PRE-WARM since 2026-08-05** — it used to launch a minimized Windows Terminal at AHK startup, which is exactly the boot clutter he banned ([[feedback_laptop_startup_clean]]); the panel is now created on the first keypress and the first one pays the cold start. The always-on-top floating mic button ("QC Button" GUI) is the one thing this script still puts on screen at login.

**REDESIGNED (user disliked the InputBox flow): the hotkey is a FLOATING CLAUDE TERMINAL toggle.** 64x16, right edge, y=25% of screen. Summon = restore + activate + (focus-confirmed) **LCtrl+LWin tap = WILLOW hands-free dictation** into the prompt (user's preferred transcriber; combo is Willow's hands-free toggle, press again stops, Enter sends). Voice = Claude Code native dictation, `settings.json voice:{enabled,mode:tap}`, bound to **F9** via `~/.claude/keybindings.json` (`voice:pushToTalk`, space nulled so normal sessions are unchanged). Tap F9 stops+auto-submits (≥3 words). Session is persistent until the user closes the window; profile guard gives it telegram-null (no token theft). Needs Windows mic permission for desktop apps. The v1 ephemeral flow below is RETIRED from the hotkey but `run.ps1`/`capture.ps1`/`system-prompt.md` remain — they're the executor intended for voice-lane v2 (draft-approve flow).

`C:\Users\Alessandro\.claude\quick-claude\` (built 2026-07-19). V1 (retired hotkey flow) was: one-button ephemeral Claude, desktop twin of [[reference-voice-lane]]:

- **Ctrl+Alt+Q** (`quick claude (ctrl alt q).ahk` in the AutoHotkey folder, autostarts with the rest): captures the FULL virtual screen first (`capture.ps1`), then shows an InputBox the user types into or dictates into with Willow.
- Enter → `run.ps1` (hidden): request file + screenshot path → `claude -p --model claude-sonnet-5 --system-prompt-file system-prompt.md --no-session-persistence`. The agent Reads the screenshot only when the request references something visual. TELEGRAM_STATE_DIR=telegram-null set (4th rule).
- Executor contract (`system-prompt.md`): WA send allowed ONLY on exact aliases/contacts name match via send.js `--to` (allowlisted in settings since 2026-07-19), else draft-only; todos via capture.py; email = gmail.py DRAFT only, never send; full python path; final message = the receipt.
- Receipt: runner pushes `⚡ Quick Claude` card (request + result) to the Claudio TG chat via sodanotif push.js. Request/screenshot temp files deleted after.
- GOTCHA that broke v1: AHK v2 single-quoted strings can't nest `'''` — never inline PowerShell with quotes in AHK; call a .ps1 with -File and pass paths as parameters.
