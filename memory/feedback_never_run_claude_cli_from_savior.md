---
name: feedback_never_run_claude_cli_from_savior
description: "Never run any `claude` command (mcp list, -p, anything) from the savior session: the child loads the MCP config, steals the Telegram bot and kills the poller."
metadata:
  type: feedback
---

From inside the savior session on the box, **never invoke the `claude` CLI at all** - not
`claude -p`, not `claude mcp list`, not any subcommand. The child process loads the same MCP
config, connects `plugin:telegram:telegram` against the real `TELEGRAM_STATE_DIR`, becomes a
second `getUpdates` consumer, and when it exits it tears the connection down and takes the
savior's own poller with it. The session then loses every telegram tool and he stops receiving
anything until he types `/mcp reconnect plugin:telegram:telegram`.

Proven the hard way on 2026-09-19 20:55: one `claude mcp list`, run only to check which servers
were connected, killed the lane in the middle of a conversation. Full entry in
`task-land/_system/TELEGRAM-BRIDGE-LOG.md`.

**How to get the same information without the CLI (all read-only, cannot connect):**
- which MCP servers this session has: the tool list in context, or the session's own plugin logs
  in `~/.cache/claude-cli-nodejs/-home-da/mcp-logs-*/`
- is the telegram lane alive: `pgrep -a bun` (one poller = healthy, zero = dead) plus the newest
  plugin log carrying `Channel notifications registered` after its last `Successfully connected`
- is the bot healthy: `curl .../getWebhookInfo` - never `getUpdates`, which IS a competing consumer
- what is in the chat: `tg-reply-resolver/resolve.py` (his own user session, non-competing)

Outbound while the lane is down: Bot API `curl` `sendMessage` / `sendDocument`. That path is not
a consumer and is safe. Related: [[reference_telegram_channel_plugin]],
[[feedback_never_respawn_savior_session]], [[feedback_telegram_one_way_lane_mcp_reconnect]].
