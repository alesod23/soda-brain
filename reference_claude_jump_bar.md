---
name: reference_claude_jump_bar
description: "Jumping between messages in Claude Code on Windows Terminal — Ctrl+Up/Down over per-prompt marks. Why the alternate screen had to go, why the overlay bar was tried and removed, why VS Code (not WT) had the sticky bar the user remembered."
metadata:
  node_type: memory
  type: reference
  originSessionId: 8cae6285-834c-4e46-935c-46d18e42bd8b
  modified: 2026-09-08T12:39:02.717Z
---

The user wanted back a VS Code-style semi-transparent sticky bar at the top of the terminal, click to jump to the previous message, in Windows Terminal + Claude Code CLI (session af24706c/8cae6285, 2026-09-07/08).

**What it actually was:** that bar is **VS Code's integrated-terminal Sticky Scroll**, NOT a Windows Terminal or Claude Code feature. Proven: grepped the 218 MB `claude.exe` — zero `]133`/`]633`/`133;A`/`osc133`/`shellIntegration`/`stickyHeader` and no "jump to previous message" strings; WT's settings schema has no "sticky". The machine had `claudeCode.preferredLocation: panel` in VS Code settings dated 2026-06-03, so he'd run Claude Code in VS Code's panel (shell = PowerShell, hence "MS PowerShell terminal" in his memory). To truly get it back: run Claude Code in VS Code's panel.

**What we shipped instead — keyboard message-jump in Windows Terminal (KEEP):**
- WT `~/.claude`... no: WT `settings.json` (LocalState) has `autoMarkPrompts: true` + `showMarksOnScrollbar: true`, and two keybindings: **Ctrl+Up = `scrollToMark previous`, Ctrl+Down = `scrollToMark next`**. One mark per Enter; Ctrl+Up/Down step message-to-message (verified: bottom → prompt N → N-1 → N-2). Marks also show as scrollbar ticks.
- REQUIRES Claude Code out of the alternate screen, else there is no scrollback and no marks and Ctrl+Up just goes to the top. Persisted in `~/.claude/settings.json` `env`: `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` + `CLAUDE_CODE_DISABLE_MOUSE=1` (approved 2026-09-08; backup `settings.json.bak-20260908-jumpbar`). Only tabs opened AFTER that render into scrollback; older sessions stay alt-screen. Trade-off accepted: no flicker-free render, no mouse inside Claude Code.
- WT settings backup: `settings.json.bak-20260907` (LocalState).

**The overlay bar — BUILT then REMOVED 2026-09-08.** An AHK v2 overlay (`claude jump bar (ctrl alt j).ahk`) drew a translucent strip under the tab row showing the focused session's last prompt, click = Ctrl+Up. **Deleted** because Windows Terminal exposes no per-pane geometry to an outside process, so over a split-pane window the bar could only span the FULL window width and collided with every pane's top line ("window-long broken header"). The user runs heavy pane splits, so keyboard-only won. If ever rebuilt, this pane limitation is the blocker — do not retry the external-overlay approach for paned layouts.

**Dead ends (do not retry):**
- Claude Code emitting OSC 133 via a hook: the `terminalSequence` allowlist is "OSC 0/1/2/9/99/777 and BEL" only (string in the binary); hook stdout is captured; a child writing OSC 133 to `CONOUT$` placed zero marks. All tested.
- WT `scrollbarState: "always"`: tried and reverted, it appeared to eat the mouse wheel in alt-buffer tabs (ssh/tmux on the box).

**Related:** [[reference_ahk_autostart]], [[feedback_shortcuts_master_file]], [[reference_gsd_statusline]] (the "context bar underneath" from the same era).
