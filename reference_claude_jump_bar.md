---
name: reference_claude_jump_bar
description: "Jumping between messages in Claude Code on Windows Terminal — Ctrl+Up/Down over one mark per message, placed by the headless `claude message marks.ahk` watcher. Why the alternate screen had to go, why the overlay bar was removed, why VS Code (not WT) had the sticky bar the user remembered."
metadata:
  node_type: memory
  type: reference
  originSessionId: 8cae6285-834c-4e46-935c-46d18e42bd8b
  modified: 2026-09-08T13:18:21.455Z
---

The user wanted back a VS Code-style semi-transparent sticky bar, click to jump to the previous message, in Windows Terminal + Claude Code CLI (2026-09-07/08).

**What it actually was:** VS Code's integrated-terminal Sticky Scroll, NOT a WT or Claude Code feature. Proven: grepped the 218 MB `claude.exe` — zero `]133`/`]633`/`133;A`/`osc133`/`shellIntegration`/`stickyHeader` and no "jump to previous message" strings; WT's schema has no "sticky". VS Code had `claudeCode.preferredLocation: panel` dated 2026-06-03, so he ran Claude Code in VS Code's panel (shell = PowerShell). To get the ORIGINAL back: run Claude Code in VS Code's panel.

**What is shipped and KEPT — keyboard message-jump (Ctrl+Up / Ctrl+Down):**
- WT `settings.json` (LocalState): `showMarksOnScrollbar: true`, `autoMarkPrompts: false`, actions `scrollToMark previous/next` bound to **Ctrl+Up / Ctrl+Down**, and `addMark` bound to **Ctrl+Alt+Shift+M** (used only by the watcher below).
- **`claude message marks.ahk`** (AHK autostart folder, headless, no window, ~14 MB, one process for all sessions): every 500 ms it resolves the focused WT window's title to a transcript (`custom-title`/`ai-title` in the newest-first 256 KB tail, Quick Claude fallback), reads the LAST `"promptId"` on a `"type":"user"` line, and when it changes fires `Send "^!+m"` = WT addMark. Adopts a session on first sight without marking (fresh session adopted at `""` so its first prompt marks; a pre-existing session adopts its current id so history isn't retro-marked). If the terminal isn't focused at that tick it does NOT advance — it retries until focused, so a mark is never dropped. Verified in a simulated session: one tick per submitted prompt; Ctrl+Up steps prompt N → N-1 → N-2.
- Why not WT's `autoMarkPrompts`: its Enter heuristic misses prompts inside the Claude TUI (2 of 4, 4 of 7). Deterministic transcript-watching replaced it.
- REQUIRES Claude Code out of the alternate screen (else no scrollback, no marks, Ctrl+Up goes to top). Persisted in `~/.claude/settings.json` `env`: `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` + `CLAUDE_CODE_DISABLE_MOUSE=1` (approved 2026-09-08; backup `settings.json.bak-20260908-jumpbar`). Only tabs opened AFTER that render into scrollback. Trade-off: no flicker-free render, no mouse inside Claude Code.
- WT settings backup: `settings.json.bak-20260907` (LocalState).

**The overlay bar — BUILT then REMOVED 2026-09-08.** A translucent strip under the tab row showing the last prompt, click = Ctrl+Up. Deleted because WT exposes no per-pane geometry to an outside process: over a split-pane window it could only span the full width and collided with every pane ("window-long broken header"). He runs heavy pane splits. Do not retry an external overlay for paned layouts.

**HARD RULE from this build (2026-09-08): never run test windows that hold/steal focus on his machine** — it blocks him entirely. He will take screenshots for me on request instead.

**Dead ends (do not retry):** Claude Code emitting OSC 133 via a hook (`terminalSequence` allowlist is OSC 0/1/2/9/99/777+BEL only; hook stdout captured; child writing OSC 133 to `CONOUT$` placed zero marks). WT `scrollbarState: "always"` (appeared to eat the wheel in alt-buffer/ssh tabs).

**Related:** [[reference_ahk_autostart]], [[feedback_shortcuts_master_file]], [[reference_gsd_statusline]].
