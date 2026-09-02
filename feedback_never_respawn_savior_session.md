---
name: feedback-never-respawn-savior-session
description: NEVER auto-spawn/rerun a savior (TG channel) session as a recovery mechanism — alert-only; the fix is /mcp in the live session
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b75b1302-8e9b-4e42-b796-f57031e2eebf
  modified: 2026-09-01T12:39:19.801Z
---

User rule (2026-07-19, after two bad experiences the same night): when the Telegram lane dies, do NOT spawn a new `claude --channels`/start-savior2 session automatically — not from a watchdog, not as a "fix". A respawned session has no context, competes for the bot token, confuses the user with error tabs, and "You're not capable of that. That shouldn't be the fixed solution."

**Why:** the first auto-spawn attempt created competing sessions + a token war; the second attempt failed with a wt quoting error tab in the user's face. Meanwhile the ACTUAL fix takes seconds and preserves context.

**How to apply:** TG-Savior-Watchdog stays ALERT-ONLY (phone push via sodanotif push.js): "lane offline → run /mcp in the savior terminal; if the session is truly gone, run start-savior2.ps1 manually." `/mcp` reconnect in the live savior session re-acquires the token (proven repeatedly). Only the USER decides to start a fresh savior. See [[reference_telegram_channel_plugin]].

**2026-09-01 — the savior moved to the DA VPS.** The ritual is now: user double-Ctrl+C's any laptop savior, then types `restore-savior` on the box (or `vpsc` from laptop PowerShell = ssh + restore-savior). `/usr/local/bin/restore-savior` on the box is ATTACH-OR-CREATE for tmux session `savior` running `claude --continue --channels plugin:telegram@claude-plugins-official` — running it twice re-attaches, so the never-respawn rule is structurally enforced; ssh dropping only detaches. Token+allowlist live at `/home/da/.claude/channels/telegram/` (v3 bot). The rule still holds for ME: never start/kill the savior tmux as a "fix"; alert and let him run restore-savior.
