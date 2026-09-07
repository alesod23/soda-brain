---
name: reference_claude_jump_bar
description: "Claude Jump Bar (Ctrl+Alt+J) — AHK v2 overlay under the Windows Terminal tab row showing the focused Claude session's last prompt; click = jump to the previous mark. Why alt-screen had to go, why hooks/OSC 133 cannot do it."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 8cae6285-834c-4e46-935c-46d18e42bd8b
  modified: 2026-09-07T23:40:53.575Z
---

Built 2026-09-07/08 after the user asked for the VS Code-style "semi-transparent sticky bar, click to jump back" inside Windows Terminal (he does not use VS Code). Nothing off the shelf does it on Windows (checked Warp, WezTerm, Tabby, Wave, Ghostty, Alacritty, Hyper, ConEmu, WT Canary — see session af24706c).

**Script:** `OneDrive - HEC Paris\Documents\AutoHotkey\claude jump bar (ctrl alt j).ahk` (autostart folder; starts OFF per [[feedback_laptop_startup_clean]]; args `on`, `debug` (log `%TEMP%\claude-jumpbar.log`), `any` (show over every WT window, testing)). One AHK64 process ≈ 14 MB WS / 3 MB private for all sessions.

**How it works**
- 400 ms timer: active window must be `WindowsTerminal.exe`; its title (minus the ✳ glyph) is matched against `"type":"custom-title"` / `"type":"ai-title"` records in the tail (64 KB) of every `~/.claude/projects/*/*.jsonl` modified in the last 12 h (re-read only when mtime changes). `Quick Claude…` titles fall back to the newest transcript in the quick-claude workspace. Prompt text = the last `"type":"last-prompt"` record.
- Bar = `Gui -Caption +AlwaysOnTop +ToolWindow +E0x08000000` (WS_EX_NOACTIVATE, so a click never steals focus), alpha 232, positioned at client-top + 40 px × per-monitor DPI (`GetDpiForWindow`; the 4K monitor is 144 dpi → 60 px tab strip, 45 px bar).
- Left-click sends Ctrl+Up, right-click Ctrl+Down → Windows Terminal `scrollToMark previous/next` (bound in WT settings.json).
- **Marks are placed by the bar, not by WT's Enter heuristic:** when the active tab's transcript shows a new prompt, the bar sends `ctrl+alt+shift+m` = WT `addMark` (autoMarkPrompts is now `false`; the Enter heuristic gave 4 marks for 7 prompts inside Claude Code).

**Prerequisites that took a day to establish**
- Claude Code's fullscreen TUI lives in the **alternate screen buffer**: no scrollback, no scrollbar thumb, and WT refuses to mark there (`Terminal.cpp: if (_autoMarkPrompts && _mainBuffer && !_inAltBuffer())`). `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` (+ `CLAUDE_CODE_DISABLE_MOUSE=1` so the wheel scrolls the terminal) is persisted in `~/.claude/settings.json` `env` (approved 2026-09-08; backup `settings.json.bak-20260908-jumpbar`).
- Claude Code cannot emit OSC 133 itself: hook `terminalSequence` allowlist is "OSC 0/1/2/9/99/777 and BEL" only (string in the binary), hook stdout is captured, and a child process writing OSC 133 to `CONOUT$` produced zero marks (tested).
- WT `scrollbarState: "always"` was tried and REVERTED: it appears to eat the wheel in alt-buffer tabs (ssh/tmux on the box).
- WT settings backup: `settings.json.bak-20260907` in the WT LocalState folder.

**Related:** [[reference_ahk_autostart]], [[feedback_shortcuts_master_file]] (row added), [[reference_gsd_statusline]] (the "context bar underneath" from the same era).
