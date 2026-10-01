---
name: reference_claude_jump_bar
description: "Message-jump in Claude Code on Windows Terminal — built then REVERTED 2026-09-08 (alt screen = no WT marks). CORRECTED 2026-09-20: the dim top bar he remembered IS a native Claude Code feature (fullscreen 'sticky prompt' header, docs /fullscreen), broken upstream in 2.1.247..~2.1.263 (#91102, #90537), back by 2.1.273. Evidence in ~/.claude/evidence/."
metadata:
  node_type: memory
  type: reference
  originSessionId: 8cae6285-834c-4e46-935c-46d18e42bd8b
  modified: 2026-09-08T14:43:21.220Z
---

**Outcome (2026-09-08): everything reverted, machine back to stock.** Claude `~/.claude/settings.json` `env` is `{}` again; Windows Terminal `settings.json` restored from `settings.json.bak-20260907` (LocalState); the AHK overlay (`claude jump bar (ctrl alt j).ahk`) and the headless marker (`claude message marks.ahk`) are deleted; no processes left. User's decision: "if they cannot coexist, I'd rather go to the Claude things."

**The hard incompatibility (do not re-attempt without a new fact):** Claude Code's native features — Ctrl+End / Ctrl+Home / PgUp / PgDn scroll keys, the clickable "Jump to bottom / N new messages" pill, mouse copy — all live in its **fullscreen renderer, which uses the alternate screen buffer**. The alternate buffer has no scrollback, so Windows Terminal cannot place or jump to marks there (`Terminal.cpp: if (_autoMarkPrompts && _mainBuffer && !_inAltBuffer())`). A WT-mark message-jump requires `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1`, which switches the renderer off and loses every native feature above. Mutually exclusive by construction. The fullscreen renderer's complete scroll action list (from the binary) is `scroll:top/bottom/pageUp/pageDown/halfPageUp/halfPageDown/fullPageUp/fullPageDown/lineUp/lineDown` — there is **no per-message navigation** to hook. Upstream request for exactly this: anthropics/claude-code#58991 (Ctrl+Up/Down jump), closed. True coexistence needs Anthropic to add it to the renderer.

**CORRECTION 2026-09-20 (he saw it again on 2.1.278 and asked for proof):** the semi-transparent bar he remembered IS Claude Code's own fullscreen "sticky prompt" header. Docs, verbatim (https://code.claude.com/docs/en/fullscreen): *"While you're scrolled up, a dim header row at the top of the conversation shows the most recent prompt that has scrolled above the view. Click the row to jump to that prompt."* The binary has `trackStickyPrompt` / `setStickyPrompt` in the virtualized transcript list (2.1.273, 2.1.276, 2.1.278 all checked). It was invisible on 2026-09-08 because he ran **2.1.263**, inside an upstream render regression (anthropics/claude-code #91102: gone since 2.1.247 after the scrollRef -> scrollViewport refactor; #90537: 2.1.251; last good 2.1.246; both still open on 2026-09-20), and that day the binary was grepped for `stickyHeader`/OSC 133 only, never `StickyPrompt`. No setting, env var or flag toggles it; it needs the alt-screen renderer (so `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` or `-p` removes it by design). Full evidence + screenshot: `~/.claude/evidence/2026-09-20-sticky-prompt-header.md`. Lesson: grep the binary for the feature's own identifiers before declaring a feature non-existent, and check the running version against upstream regressions ([[feedback_verify_agent_capability_claims]]).

**What was believed on 2026-09-08 (wrong, kept for the record):** VS Code's integrated-terminal Sticky Scroll (semi-transparent top bar, click to jump). Not a WT or Claude Code feature: grepped the 218 MB `claude.exe`, zero `]133`/`]633`/`133;A`/`osc133`/`shellIntegration`/`stickyHeader`; WT schema has no "sticky". VS Code had `claudeCode.preferredLocation: panel` dated 2026-06-03 — he ran Claude Code in VS Code's panel then. To get THAT back: run Claude Code in VS Code's panel (Sticky Scroll is on by default there).

**What was proven to work, if ever wanted again (at the cost of native mode):** with `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` + `CLAUDE_CODE_DISABLE_MOUSE=1`, WT `scrollToMark` bound to Ctrl+Up/Down steps message-by-message, and a headless AHK watcher that fires WT `addMark` on each new transcript `promptId` gives exactly one mark per message (WT's own `autoMarkPrompts` heuristic missed prompts: 2 of 4, 4 of 7). The overlay bar was removed earlier because WT exposes no per-pane geometry (full-width "broken header" over his split panes).

**Dead ends:** hook `terminalSequence` allowlist is OSC 0/1/2/9/99/777+BEL only; hook stdout captured; child writing OSC 133 to `CONOUT$` placed zero marks; WT `scrollbarState: "always"` appeared to eat the wheel in alt-buffer tabs.

**HARD RULE: never run test windows that hold/steal focus on his machine** — it blocks him entirely; he screenshots for me instead.

**Related:** [[reference_ahk_autostart]], [[feedback_shortcuts_master_file]], [[reference_gsd_statusline]].
