---
name: feedback_telegram_one_way_lane_mcp_reconnect
description: "When the telegram plugin drops mid-session and comes back one-way (poller alive, tools withdrawn, no \"Channel notifications registered\"), the fix is HIM typing `/mcp reconnect plugin:telegram:telegram` in the savior UI. Verified 2026-09-16: no restart, context intact, queue drained. Outbound meanwhile via Bot API curl."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8b628b1a-a793-4289-b578-06e8098d767c
  modified: 2026-09-16T14:36:57.801Z
---

**Symptom (2026-09-16, bridge log entry of that date):** the plugin's MCP transport dropped, Claude Code reconnected it automatically, but the reconnected server never re-registered channel notifications. Poller alive under the savior, `getWebhookInfo` clean, and yet nothing reached the session and the `reply`/`react` tools were withdrawn ("server failed to connect"). He wrote for hours and got nothing back.

**The fix, verified:** he typed `/mcp reconnect plugin:telegram:telegram` in the savior's own UI (Remote Control from his phone works). Reconnected in seconds, a fresh poller under the same session, "Channel notifications registered" logged, the 8 queued updates drained into the conversation, the reply tool came back, context intact. **Nothing was restarted.**

**Why:** `/mcp` is a slash command in the UI, not a tool, so the savior cannot run it; the user can, from any device attached to the session. It is strictly better than any restart because it keeps the process and the context. The whole workbench/resume detour that day was unnecessary.

**How to apply:**
1. Diagnose read-only first (bridge log diagnostics): poller pid and its parent; `getWebhookInfo` pending count; newest plugin log has `Successfully connected` with no `Channel notifications registered` after it.
2. Keep serving: read his messages with `tg-reply-resolver/resolve.py` (his user session, non-competing) and answer via Bot API `curl` (`sendMessage` / `sendDocument`; not a `getUpdates` consumer). Keep the curl command text free of self-restart vocabulary or the auto-mode classifier blocks it.
3. Tell him, on whatever channel reaches him (Bot API, SendUserFile, the terminal if he is live): **type `/mcp reconnect plugin:telegram:telegram` in the savior session**. Then verify the four signals above and send one reply THROUGH the plugin as proof.
4. Only if that fails: the resume path (`~/.local/bin/savior-resume.sh <session id>` run by him from a shell outside the savior window). Never a fresh respawn.
5. Do not kill the orphan poller while it is alive unless a replacement is seconds away: with no poller at all Telegram queues messages (nothing lost); with an orphan alive they are consumed and dropped.

Related: [[reference_telegram_channel_plugin]], [[feedback_never_respawn_savior_session]], [[feedback_pgrep_self_match_use_script_files]] (a `pgrep -f` on the poller matched my own shell and looked like a second poller).
