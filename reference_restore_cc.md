---
name: reference_restore_cc
description: Restore-CC command reopens the Claude Code terminal sessions that were open before a laptop restart
metadata: 
  node_type: memory
  type: reference
  originSessionId: d18c0f7d-7979-45e9-a966-be332a9c9e16
  modified: 2026-08-06T16:58:58.916Z
---

`Restore-CC` (PowerShell function in `$PROFILE`) reopens the Claude Code terminal tabs that were up before a restart. Logic in `C:\Users\Alessandro\.claude\scripts\cc-sessions.ps1`.

How it works: scans `~/.claude/projects/*/*.jsonl`; an **interactive** session (a real tab, not an agent/subagent) is identified by containing a `"type":"mode"` line — agent transcripts lack it. Anchors to the newest interactive session's mtime (so a multi-day power-off still works) and keeps everything touched within `-WindowMinutes` (default 240). Titled sessions (Claude Code custom title) dedupe to their latest transcript; untitled ones stay distinct. Each survivor reopens as a Windows Terminal tab via `wt.exe new-tab -d <cwd> ... claude -r <sessionId>`.

Usage: `Restore-CC` (lists, then pick: Enter=all, `1 3 5`=subset, n=cancel) · `-All` (no prompt) · `-DryRun` (list only) · `-WindowMinutes 720`.

**Savior sessions are never resumed** (a plain `claude -r` would drop `--channels`). Detection is **content-based since 2026-08-06**: a transcript containing `<channel source=` is a savior session and is dropped from the work list (the run prints "Skipped N old savior session(s)"). The old title-regex-only test failed because the savior session usually has **no `customTitle` at all**, so it survived the filter and reopened as a useless extra pane. The fresh savior tab still comes from `start-savior2.ps1`, gated on `Test-SaviorAlive`, so nothing is double-launched. See [[feedback_never_respawn_savior_session]].

Limitation: there is **no** reliable "is this tab open right now" signal — CC doesn't lock its transcript and fresh sessions carry no session-id on the process command line. So detection is recency-based and may over-capture recently-*closed* sessions; the pick prompt is how you curate. A once-per-boot tip in `$PROFILE` reminds you to run it.

**`Restore-Savior` auto-recovers the TG MCP (2026-08-21, REWRITTEN 2026-08-31).** `start-savior2.ps1` launches `tg-savior-inject.ahk restore <TrustDelay> <ReconnectDelay>` IMMEDIATELY (not via a delayed hidden powershell), so the injector latches the foreground window handle while that window is still certainly the terminal the user just typed `Restore-Savior` in. On that window and nothing else it then does: wait `-TrustDelay` (5s) -> `{Enter}` (answers "Do you trust the files in this folder?"; harmless no-op on an empty prompt) -> wait `-ReconnectDelay` (5s) -> type `/mcp reconnect plugin:telegram:telegram` + Enter. If focus moved away in between it types NOTHING and exits 2. Opt out with `-NoReconnect`.

**THE TAB-MOVEMENT BUG (fixed 2026-08-31, user-reported):** restore used to reuse the injector's `reconnect` mode, which is title-gated on a tab whose title contains "savior" - but claude OVERWRITES the terminal title on boot, so 5s in the title never matched, and `FindSaviorTab()` fell through to Ctrl+Tab-cycling up to 12 tabs in every Windows Terminal window, activating each one. That was the "shortcut does something weird / moves across tabs" the user saw. `restore` mode now never hunts, never cycles tabs, never activates or restores a window. The watchdog's unattended `reconnect` mode keeps the cycling (nobody is looking when it fires). Verified 2026-08-31 end-to-end against an AHK Edit-control harness: latched HWND held across both checks, Enter then the full command landed. Backups: `start-savior2.ps1.bak-20260831`, `tg-savior-inject.ahk.bak-20260831`.

**There is no `/mcp connect`.** `/mcp reconnect <server>` is the single command and it covers both "never attached" and "dropped" (confirmed against the claude 2.1.251 binary: only `mcp reconnect <server>` / `mcp reconnect all` / `mcp enable` / `mcp disable` exist). So restore always types `reconnect`.
