---
name: reference_claude_jump_bar
description: "Message-jump in Claude Code on Windows Terminal — built (overlay bar, then Ctrl+Up/Down marks), REVERTED 2026-09-08 because it cannot coexist with Claude Code's native fullscreen features. Why: alternate screen buffer. What the user remembered was VS Code's Sticky Scroll."
metadata:
  node_type: memory
  type: reference
  originSessionId: 8cae6285-834c-4e46-935c-46d18e42bd8b
  modified: 2026-09-08T14:43:21.220Z
---

**Outcome (2026-09-08): everything reverted, machine back to stock.** Claude `~/.claude/settings.json` `env` is `{}` again; Windows Terminal `settings.json` restored from `settings.json.bak-20260907` (LocalState); the AHK overlay (`claude jump bar (ctrl alt j).ahk`) and the headless marker (`claude message marks.ahk`) are deleted; no processes left. User's decision: "if they cannot coexist, I'd rather go to the Claude things."

**The hard incompatibility (do not re-attempt without a new fact):** Claude Code's native features — Ctrl+End / Ctrl+Home / PgUp / PgDn scroll keys, the clickable "Jump to bottom / N new messages" pill, mouse copy — all live in its **fullscreen renderer, which uses the alternate screen buffer**. The alternate buffer has no scrollback, so Windows Terminal cannot place or jump to marks there (`Terminal.cpp: if (_autoMarkPrompts && _mainBuffer && !_inAltBuffer())`). A WT-mark message-jump requires `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1`, which switches the renderer off and loses every native feature above. Mutually exclusive by construction. The fullscreen renderer's complete scroll action list (from the binary) is `scroll:top/bottom/pageUp/pageDown/halfPageUp/halfPageDown/fullPageUp/fullPageDown/lineUp/lineDown` — there is **no per-message navigation** to hook. Upstream request for exactly this: anthropics/claude-code#58991 (Ctrl+Up/Down jump), closed. True coexistence needs Anthropic to add it to the renderer.

**What the user actually remembered:** VS Code's integrated-terminal Sticky Scroll (semi-transparent top bar, click to jump). Not a WT or Claude Code feature: grepped the 218 MB `claude.exe`, zero `]133`/`]633`/`133;A`/`osc133`/`shellIntegration`/`stickyHeader`; WT schema has no "sticky". VS Code had `claudeCode.preferredLocation: panel` dated 2026-06-03 — he ran Claude Code in VS Code's panel then. To get THAT back: run Claude Code in VS Code's panel (Sticky Scroll is on by default there).

**What was proven to work, if ever wanted again (at the cost of native mode):** with `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` + `CLAUDE_CODE_DISABLE_MOUSE=1`, WT `scrollToMark` bound to Ctrl+Up/Down steps message-by-message, and a headless AHK watcher that fires WT `addMark` on each new transcript `promptId` gives exactly one mark per message (WT's own `autoMarkPrompts` heuristic missed prompts: 2 of 4, 4 of 7). The overlay bar was removed earlier because WT exposes no per-pane geometry (full-width "broken header" over his split panes).

**Dead ends:** hook `terminalSequence` allowlist is OSC 0/1/2/9/99/777+BEL only; hook stdout captured; child writing OSC 133 to `CONOUT$` placed zero marks; WT `scrollbarState: "always"` appeared to eat the wheel in alt-buffer tabs.

**HARD RULE: never run test windows that hold/steal focus on his machine** — it blocks him entirely; he screenshots for me instead.

**Related:** [[reference_ahk_autostart]], [[feedback_shortcuts_master_file]], [[reference_gsd_statusline]].
