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


**2026-09-04:** the panel launches `claude --model sonnet` (user: Sonnet only, for speed). Change the model in `quick claude (alt win j).ahk` line ~45 if that ever needs to move.

**2026-09-07 fixes.** (1) Windows Terminal splits ITS OWN command line at `;`, so `powershell -Command "$env:X=1; claude ..."` inside a `wt.exe new-tab ...` call became two wt subcommands and failed with "cannot find the file `\" claude --model sonnet ...`"; env vars for the panel are now set with `EnvSet` in the AHK script (child inherits), never inside the wt string. (2) Starting the AHK script (or any panel) from inside a Claude Code session makes the panel inherit `CLAUDE_CODE_CHILD_SESSION` and run with transcript saving off; the script now deletes the CLAUDECODE / CLAUDE_CODE_* markers before launching, and a manual restart must use `Start-Process -UseNewEnvironment`. (3) `AutoHotkey64.exe /validate` hung on this script (error dialog), do not rely on it; start the script (`#SingleInstance Force` replaces the old one) and check for an error dialog window titled with the script name instead. Counting instances with a CommandLine match also counts the bash/powershell shells running the query: filter on Name = AutoHotkey64.exe.

**2026-09-07 capability decision (asked via UI).** Quick Claude = Sonnet + `--strict-mcp-config --mcp-config ~/.claude/quick-claude/workspace/mcp-quick.json` (the remote Notion server only). Gmail, Calendar, Drive and Slack are reached through the CLI helpers (gmail.cmd draft/search/send, gcal.py, drive.cmd, slack.cmd) documented in the workspace `CLAUDE.md`; a "draft" in the panel must be a real Gmail draft (the 2026-09-07 Notepad-file draft was the trigger). Rejected: the claude.ai connectors (need non-strict mode, which also loads linkedin-mcp: ~0.5 GB and +10 s per press), Granola, lemlist (170 tool schemas), Opus. Reason the panel got slow before: every configured server loaded on each press.

**2026-09-07 later.** (4) NEVER restart the AHK script with `Start-Process -UseNewEnvironment`: that environment lacks the per-user variables (USERPROFILE, APPDATA, LOCALAPPDATA, TEMP), the panel's powershell.exe then dies with "Loading managed Windows PowerShell failed with error 8009001d" and the tab shows "process exited with code 4294901760". Restart it the way logon does: `explorer.exe "<path>\quick claude (alt win j).ahk"` (Explorer's full logon environment, no Claude markers). (5) Alt+Win+Shift+J opens an additional panel "Quick Claude N"; Alt+Win+J with a panel present dictates into / sends to the active one and never opens a second.

**2026-09-07 evening.** (6) Model prompt: both chords ask for one key after the press (InputHook L1 T8, same pattern as the stay-awake hotkey): S = Sonnet (default on timeout), O = Opus, Esc = cancel; only asked when a panel is being CREATED (no panel open, or the extra-panel chord), never on the dictate/send press. Panel title carries "(Opus)" when chosen.

**2026-09-07 final shape (user design).** ONE chord. Alt+Win+J then, within 5 s: J = new Sonnet window (always new; a quick double J with Alt+Win still held is caught by the hotkey re-fire and counts), K = new Opus window, nothing = the open window (dictate into it) or Sonnet if none, Esc = cancel. Alt+Win+K alone = new Opus window. The Shift chord and the S/O prompt are gone. Windows titled "Quick Claude", "Quick Claude 2", ... plus " (Opus)". The stop-and-send press never asks.
