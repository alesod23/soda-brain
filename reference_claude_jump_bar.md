---
name: reference_claude_jump_bar
description: "Claude Jump Bar (AHK v2, Ctrl+Alt+J) — semi-transparent sticky strip over Windows Terminal showing the previous prompt of the focused Claude session; click = jump to previous WT mark. Needs CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1."
metadata: 
  node_type: memory
  type: reference
  originSessionId: af24706c-a858-4161-b258-835e14e610bf
  modified: 2026-09-07T19:15:24.510Z
---

`OneDrive - HEC Paris\Documents\AutoHotkey\claude jump bar (ctrl alt j).ahk` (AHK v2, built 2026-09-07). One process (~14 MB WS / 3 MB private) serves every Claude session.

**Why it exists:** Claude Code's fullscreen TUI takes the alternate screen buffer, so Windows Terminal has no scrollback, no scrollbar thumb, and never places prompt marks (`Terminal.cpp`: `autoMarkPrompts` is skipped `_inAltBuffer()`). No Windows terminal has VS Code-style sticky scroll (WT #14754 backlog; Warp treats a Claude session as one block). Claude Code cannot emit OSC 133: hook `terminalSequence` allowlist is only OSC 0/1/2/9/99/777 + BEL (string in the binary), hook stdout is captured, and a child process writing OSC 133 to `CONOUT$` produced zero marks (tested). So the bar is an external overlay.

**How it works:** 400 ms timer; if the active window is `WindowsTerminal.exe`, strips the status glyph from its title and matches it against the last `"type":"custom-title"` / `"type":"ai-title"` record in recently-modified `~/.claude/projects/*/*.jsonl` (64 KB tail read, cached by mtime); shows the session's last `"type":"last-prompt"` text. Gui is `-Caption +AlwaysOnTop +ToolWindow +E0x08000000` (WS_EX_NOACTIVATE, so a click never steals focus), alpha 232, pinned at client-top + tab-strip height, all scaled by `GetDpiForWindow` (4K monitor = 144 dpi). Left-click sends `^{Up}`, right-click `^{Down}` — the WT keybindings added the same day (`scrollToMark previous/next`, in WT `settings.json`, backup `settings.json.bak-20260907`; also `showMarksOnScrollbar: true`, `scrollbarState: always`, `autoMarkPrompts: true`).

**Args:** `on` (start enabled; default is OFF per the launch-folder rule), `debug` (log to `%TEMP%\claude-jumpbar.log`, 1 line / 1.5 s), `any` (show over every WT window; testing only).

**Prerequisite:** the Claude session must run with `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` (terminal owns scrollback). Marks are per Enter keypress, not per message, and are not rebuilt on `--resume`. If the wheel dies in such a session, add `CLAUDE_CODE_DISABLE_MOUSE=1` (Claude keeps mouse tracking on otherwise). Verified 2026-09-07: click scrolled a test terminal from bottom to the previous mark; wheel still scrolls with the bar present.

**Gotchas:** every variable assigned inside `Tick()` must be in its `global` line (an unlisted one throws "local variable has not been assigned" and hides the bar). `wt.exe` word-splits `--title`/`-Command` args — pass a `-File` script. Hard rule from [[reference_ahk_autostart]]: nothing displayed at login. Listed in `task-land/_system/SHORTCUTS.md`.
