---
name: reference_coattio_spawns_claude_kills_telegram
description: "2026-09-24: the four silent Telegram-lane deaths of 21-24 Sept were coattio. Its servers ran without TELEGRAM_STATE_DIR, so every headless claude they spawned loaded the telegram plugin and became a second getUpdates consumer. Fixed in coattio/start-box.sh."
metadata:
  type: reference
---

**The cause of the four September outages, proved not guessed.** The coattio servers
(`crm-app/server.js` :4124, `intake-server.js` :4137) were started by `coattio/start-box.sh` with an
`$ENV` that did **not** contain `TELEGRAM_STATE_DIR`. Those servers spawn headless `claude` on
demand (intake enrichment, `comment-agent.js`, `ai-draft.js`, `coattio-notion-sync.js`), and each
child inherited the REAL telegram state dir, loaded the telegram plugin, and became a second
`getUpdates` consumer. One listener per bot: the savior's poller dies.

**The evidence that settles it**, in the order that found it:
1. `find ~/.claude/plugins ~/.claude/skills -newermt '<t>' ! -newermt '<t+90s>' -printf '%TT %p\n'`
   showed `telegram/0.0.7/.in_use` written at 17:49:29 and
   `~/.claude/projects/-home-da-coattio/` at 17:49:17, 39 seconds before `bun` was gone.
2. `tr '\0' '\n' < /proc/<pid>/environ | grep TELEGRAM_STATE_DIR` on both coattio servers: **unset**.
   On the savior: set. That is the whole bug in one command.

**Why the death times looked random** (16:19, 22:57, 14:56, 17:49): coattio spawns claude when
someone uses the CRM, not on a schedule. Stop looking for a cron pattern.

**The fix:** `TELEGRAM_STATE_DIR=$HOME/.claude/channels/telegram-null` in `$ENV` in
`coattio/start-box.sh`. Use the NULL DIR, **not `--strict-mcp-config`**: that flag kills every MCP
server, and `coattio-notion-sync.js` and `comment-agent.js` need Notion and Calendar.

**How to apply.** Any long-running process on the box that can spawn `claude` must carry
`TELEGRAM_STATE_DIR`. The sweep that proves it:
```
for p in $(ps -eo pid,comm | awk '$2=="node"||$2=="python3"{print $1}'); do
  e=$(tr '\0' '\n' < /proc/$p/environ 2>/dev/null)
  echo "$e" | grep -q CLAUDE_BIN && ! echo "$e" | grep -q TELEGRAM_STATE_DIR && echo "UNGUARDED $p"
done
```
And a correction worth remembering: I first blamed the laptop's hourly tar push, and the laptop
session disproved it with its own push log (the archive is `skills commands` only, and the death
fell between two pushes). Check `/proc/<pid>/environ` before blaming a remote writer.

Related: [[reference_telegram_channel_plugin]], [[reference_coattio_servers]],
[[../../task-land/_system/TELEGRAM-BRIDGE-LOG.md]].
