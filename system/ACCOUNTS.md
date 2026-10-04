# ACCOUNTS: identities, services, and where each credential lives

The system acts under Alessandro's own identities: five Google accounts (CDTM, Tundra, two Gmail, Lobbly) plus an HEC Outlook mailbox with no token, three Slack workspaces, two Telegram bots and one Telegram user session, one Notion workspace reached only through the Notion MCP, one LinkedIn profile driven through Chrome, one Langfuse project, one GitHub user and one Tailscale tailnet. No API key for a model provider is used anywhere (plan compute only). Every credential is a file; this document names the file and who reads it, never a value. Secrets live outside every repo on both machines (`~/.env/`, `~/.claude/`, `triage/tokens/`, `slack/tokens/`, `wa-daemon/auth/`, `~/.config/rclone/`), the mirror scripts exclude them by pattern, and `.gitignore` repeats the same patterns as a second guard.

Last verified: 2026-10-01 (from the inventories of that day); 2026-10-04 19:15: Granola retired (his ruling), meeting notes come from Notion's meeting AI

Conventions: laptop = `C:/Users/Alessandro/`, box = `/home/da/`. "Where" names the file; "Who uses it" names the scripts or services that read it.

## 1. Google

| Account (short name in code) | Address | Purpose | Token files (laptop) | Token files (box) | Who uses it |
|---|---|---|---|---|---|
| cdtm | alessandro.sodano@cdtm.com | main work mailbox and calendar; the claude.ai login and MCP connectors (Gmail, Calendar, Drive) follow this account; CDTM My Drive is the exchange folder | `triage/tokens/cdtm.json`, `triage/tokens/cal-cdtm.json` (one of the four `cal-*`), `triage/tokens/drive-cdtm.json`, `~/.env/gdrive_full_token.json`, `triage/drive_token.json`, `triage/calendar_token.json` (the account served by the last two is unverified) | `triage/tokens/cdtm.json`, `cal-*`, `drive-cdtm.json`; `~/.config/rclone/rclone.conf` remote `cdtm:` | `triage/gmail.py` (default sender), `gcal.py`, `drive.py`, `drafts/common.py`, `intake-server.js`, `crm-app/server.js`, the hub (`gmail-send-draft`, account cdtm), `sodanotif/pollers/gmail_poll.py`, `hub_outdated.py`, `reconcile.py`, `da-gdrive.service` (mount), Google Drive desktop on the laptop (`G:`), the dead-man "VPS DOWN" calendar events |
| tundra | alessandro@tundrahealth.ai | the company mailbox; every campaign email is sent from here; Tundra Shared Drive | `triage/tokens/tundra.json`, `cal-tundra.json`, `drive-tundra.json` | same names; `rclone.conf` remote `tundra:` | `gtm-eng/campaign.py` (sends, labels `Campaign/<slug>`), `daily-campaign/fire.py` and `build.py`, `drafts/common.py`, `intake-server.js`, `crm-app/server.js`, `hub_outdated.py` (the account that returns 403 and read timeouts), `da-tundra-drive.service`, `da-voice.timer` (recordings on the mount) |
| sodano23 | alessandrosodano23@gmail.com | personal Gmail | `triage/tokens/sodano23.json`, `cal-sodano23.json` | same | `gmail.py`, `reconcile.py` (AUTH REQUIRED on every pass since 2026-09-26: the box token is unusable), `hub_outdated.py` |
| alesoda2002 | alesoda2002@gmail.com | the phone's Google account: Contacts | `triage/tokens/alesoda2002.json`, `cal-alesoda2002.json`, `contacts-alesoda2002.json` | same (`contacts-alesoda2002.json` expired or revoked since 2026-09-21 13:00) | `triage/contacts_sync.py sync --account alesoda2002` (box cron every 30 min), `gmail.py` |
| lobbly | alessandro@lobbly.tech | the Lobbly mailbox | `triage/tokens/lobbly.json` | same | `gmail.py`, `/triage`, `hub_outdated.py` |
| hec | alessandro.sodano@hec.edu | HEC Paris, Outlook; no token anywhere | none | none | read by hand |
| OAuth client | n/a | the Google Cloud OAuth client used to mint the tokens above | `triage/credentials.json`; copies under `~/Downloads/client_secret_*.json` and `~/Downloads/credentials.json` | `triage/credentials.json` | the re-auth flows (always with `login_hint=<address>` so he only clicks Continue) |
| WhatsApp daemon Google token | n/a | purpose not stated in the sources | `~/.claude/wa-daemon/google-token.json` | none named | the laptop wa-daemon (disabled) |

Calendars: every caller uses `primary` of the chosen account; no group-calendar id is hardcoded. The four `cal-*` tokens correspond to four of the five accounts; which account lacks one is unverified.

Claude.ai account: the connectors in Claude Code (Gmail, Calendar, Drive, Docs) follow the claude.ai login; an account migration was in progress per the global CLAUDE.md banner (`~/.claude/MIGRATION-account-switch.md`), which lists which MCP servers are account-bound.

## 2. Slack

| Workspace | Where the credential lives (laptop) | Where (box) | Who uses it |
|---|---|---|---|
| cdtm | `~/.claude/slack/tokens/cdtm.json` | `/home/da/slack/tokens/cdtm.json` | `slack.py` (read DMs, mentions, send with `--confirmed`), the hub (`slack-send` action), `sodanotif/pollers/slack_poll.py` (every 60 s), `/slack`, `/triage`, `/snm` |
| xplore | `~/.claude/slack/tokens/xplore.json` | `/home/da/slack/tokens/xplore.json` | same |
| horus | `~/.claude/slack/tokens/horus.json` | `/home/da/slack/tokens/horus.json` | same (not named in the skill descriptions; present as a token on both machines) |
| the custom Slack app | n/a | `/home/da/slack/credentials.json` | the token refresh |

Box token files are mode 0644 (FINDINGS 14).

## 3. Telegram

Three distinct identities; confusing them has broken the lane about seven times (`task-land/_system/TELEGRAM-BRIDGE-LOG.md` is the fix log).

| Identity | What it is | Where the credential lives | Who uses it |
|---|---|---|---|
| The savior lane bot (`@Claudio_al_TG_v3_bot`) | the bot behind the Claude Code Telegram plugin; the ONLY `getUpdates` consumer is the tmux `savior` session on the box | box `~/.claude/channels/telegram/.env`, `~/.env/telegram.env`; laptop `~/.claude/channels/telegram*/.env` (the `telegram-v3` inbox holds his MacroDroid exports) | the savior (`claude --channels plugin:telegram`); the hub's one-time card ping; `tg-lane-watchdog.sh`; every other `claude` on the box runs with `TELEGRAM_STATE_DIR=~/.claude/channels/telegram-null` so it cannot steal the poller; `hidden-claude.js childEnv()` in coattio defaults children to the null dir on both machines; headless calls add `--strict-mcp-config`. Never debug with `getUpdates` (use `getWebhookInfo`); the laptop `telegram-switch` skill moves the lane |
| The second bot (tg-bridge) | a different bot in a different chat; the phone types to it and it pipes into headless `claude -p`; also `send-to-phone.js` for raw strings he explicitly asked for (an IP, a token, a URL); NEVER for pings | box `~/.env/tg-bridge.env` (service `da-tg-bridge`); laptop `~/.env/tg-bridge.env`, `~/.claude/tg-bridge/` (`send-to-phone.js`, `history.jsonl`) | `tg-bridge/bot.js`; pinging through it is a standing violation (he does not see it) |
| The Telethon user session | Alessandro's own Telegram account as a client (reads the bot chat history, recovers what a swipe-reply points to, sends as him) | box `/home/da/tg-reply-resolver/user.session` (mode 0644, FINDINGS 14), `~/.env/tg-user-api.env`; laptop `~/.env/tg-user-api.env` | `tg-reply-resolver/resolve.py`, the `UserPromptSubmit` hook `~/.claude/hooks/tg-reply-context.py` (reacts with eyes, quotes the original), `hub-review/notify.py`, `presweep-watchdog.sh` (a Telegram message), the savior when it "pulls" context |
| sodanotif push | the Bot API sender of the notification cards (digest, SODANOtif cards); which bot token it holds is unverified | box `/home/da/sodanotif/push.env` (0644), `~/.env/sodanotif.env`; laptop `~/.env/sodanotif.env` | `sodanotif/push.js`, the hub (`HUB_*` env points at it), `eod_sweep.py` (the 23:00 digest, failing with http 400 since 2026-09-28) |
| Other env names on the laptop | `~/.env/sodaos-bot`, `~/.env/tg-terminal` | laptop only | historical lanes (sodaos, terminal-inbox); unverified whether anything still reads them |

Chat ids: messages to Alessandro's own chat id are allowed without approval; sends to anyone else need "dsend" on a card.

## 4. WhatsApp

| Identity | Where the credential lives | Who uses it |
|---|---|---|
| Alessandro's WhatsApp number, linked as two Baileys devices | box `/home/da/wa-daemon/auth/` (the live device, `da-wa.service`); laptop `~/.claude/wa-daemon/auth/` (7,633 Signal key files, daemon tasks Disabled) | box: `daemon.js` (store, tap for sodanotif), `send.js` (send API 127.0.0.1:4119, the hub's `wa-send` action), `search.js`; laptop: `/wa`, `/wa-search` read the laptop store and the Drive-shipped box store |

## 5. Notion

| Item | Value or where | Who uses it |
|---|---|---|
| Workspace (Tundra) | id `0f7b30c6-d57e-818c-ad08-0003a268b635` | everything below |
| Contacts database | data source `a747cb32-a4bd-42bf-818e-df4c97390f4f` | `coattio-notion-sync.js` (CRM -> Contacts), `campaign.py plan`, `daily-campaign/review.py`, the names snapshot |
| Meetings database | data source `3a3b30c6-d57e-8093-9e35-000b79676b41` (env `CRM_NOTION_MEETINGS_DS`) | `crm-app/sources.js` notionScan, `agent/meeting_loop.py`, `scripts/notion-meeting-filer.ps1` (task Notion-MeetingFiler), `drafts/handoff.py`; written by Notion's meeting AI (`granola-auto` and `/granola` retired 4 Oct 2026) |
| Competition > TRIMEDX-affiliated hospitals | page `3e6b30c6-d57e-8135-a67c-e81651d01d73`, data source `2cdbc0d0-de27-4681-9132-b9e0ec8a6be6` (private draft, 2026-09-25) | `review.py` |
| Credential | NO API token anywhere. Access is the Notion MCP (`https://mcp.notion.com/mcp`) with OAuth state in `~/.claude.json` on each machine; scripts shell out `claude -p --strict-mcp-config --mcp-config <notion.mcp.json>` | the scripts above, on the laptop and on the box (`CLAUDE_BIN=/usr/bin/claude`) |

Granola is RETIRED (his ruling, 4 Oct 2026: "Granola is dead; meetings come from Notion's meeting AI"). Meeting notes are Notion's meeting AI notes, read by the meeting loop (LOOPS.md section 3). The MCP server `granola` is still registered in `~/.claude.json` (account-level config, left for him to remove); task Granola-Auto-Sweep is disabled and `~/.claude/granola-auto/run.js` exits unless `--force-retired`.

## 6. LinkedIn

| Item | Where | Who uses it |
|---|---|---|
| The live profile | Chrome, the daily CDTM profile (his own session, never automated) | him |
| The poller profile | `~/.claude/linkedin-poll/poll.py` drives Chrome (`C:/Program Files/Google/Chrome/Application/chrome.exe`) with a dedicated `user-data-dir` (the standing rule: one dedicated profile per skill, never the real profile); the session cookie lives in that profile directory, no token file is named in the sources | task LinkedIn-Poll (writes `G:/My Drive/DA/linkedin-store.jsonl`), `launcher.py` + `reap.log` (the reaper that stopped launchers killing each other), `gtm-eng/agent/li_probe.py` and the agent's `li_repair` fix, `campaign.py` (invites, DMs), the connection-closed fix of 2026-09-28 |
| The accept bot | `~/.env/linkedin-accept-bot.env`, `~/.claude/linkedin-accept-bot/*.json` | the accept bot (cadence unverified) |
| Box safety net | no credential; `task-land/_system/gtm-agent/box_linkedin_watch.py` (cron every 10 min) reads the laptop's signals | the GTM agent's incidents |
| linkedin-mcp | an MCP server registered in `~/.claude.json` (also a third-party clone under `.tmp-audit/linkedin-mcp-server`) | sessions, when it connects |

## 7. Langfuse

| Item | Where | Who uses it |
|---|---|---|
| Project on `cloud.langfuse.com` | keys in `~/.env/langfuse.env`; a plaintext duplicate sits in `~/.env/openai-thesis-note.txt` (FINDINGS); parked MCP config `~/.claude/mcp-parked/langfuse.mcp.json` | `~/.claude/hooks/langfuse_hook.py` (every Claude Code turn, state `~/.claude/state/langfuse_state.json`), `linkedin-poll/poll.py`, `loops/langfuse-optimizer/lf_calls.py`, `sim/harness` `simclaude.py`, `/langfuse-bananza` |

## 8. GitHub

| Item | Where | Who uses it |
|---|---|---|
| User `alesod23` | laptop: `gh auth` (logged in as alesod23); git over https | `gh`, the laptop sync tasks, `DesignMirror-Server` |
| Box deploy keys | `~/.ssh/` (`id_ed25519` + one deploy key per repo, host aliases in `~/.ssh/config`); the coattio key is read-only | `da-sync.timer`, `da-repo-sync@*.timer`, cron `repo-sync.sh`, `coattio-sync.sh` |
| Repos | see REPOS.md; all private since 2026-10-01 | |

## 9. Tailscale

| Item | Where | Who uses it |
|---|---|---|
| Tailnet `taile93f00.ts.net`: `da-box` 100.85.52.84, `desktop-1bojsrg` 100.127.7.80, `pixel-9a` 100.121.68.86 | Tailscale's own state on each device (joined once by clicking an auth URL; file path not in the sources) | `forward-to-box.js` (laptop :4180 -> box), the daily page (:4142 open-count), `pipeline.py`, `gtm_agent.py`, the phone (hub-review, CRM), ssh laptop -> box, the GTM-agent heartbeat push |
| Tailscale Serve (older) | laptop, proxied `localhost:4124` to the phone | superseded by the box CRM copy; whether Serve is still configured is unverified |

## 10. Claude Code itself

| Item | Where (laptop) | Where (box) | Who uses it |
|---|---|---|---|
| Login and OAuth state | `~/.claude/.credentials.json`, `~/.claude.json` (also MCP servers: notion, linkedin-mcp, lemlist, oxygen, granola, edge) | `~/.claude/.credentials.json`, `~/.claude.json`, `~/.env/claude.env`, `~/.claude/sessions/*.key` | every session; the savior; headless `claude -p` from coattio, the classifier in `daily-lib.ps1`, the Notion shell-outs |
| Rule | plan compute, never an API key; parked MCPs are per session (`cc-with`), never global | same | |
| Telegram plugin | `settings.json` (box: model opus, plugin enabled) | | the savior only |

## 11. Other services with a credential file

| Service | Where | Who uses it |
|---|---|---|
| lemlist | the lemlist MCP (OAuth in `~/.claude.json`); `.medtech-crm/lemlist-state.json` | `lemlist-*` scripts, campaign hand-off (`campaigns[]` is lemlist-ready) |
| Floom | `~/.env/floom`, `~/.config/floom/*` | `/floom` |
| AI sidecar | `~/.config/ai-sidecar/*` | unverified |
| EPO (patents), Gemini, Obsidian | `~/.env/epo`, `~/.env/gemini` (used by `~/.claude/scripts/gemini-fetch.sh`, the WebFetch fallback), `~/.env/obs` | thesis tooling, the fetch fallback, vault scripts |
| OpenAI (thesis note) | `~/.env/openai-thesis-note.txt` (also carries the Langfuse duplicate) | thesis experiments |
| Zotero | local API, `~/.claude/mcp-parked/zotero.mcp.json` | the thesis skills when parked in |
| MacroDroid webhook (phone) | the URL in `voice-lane/config.json` | the deactivated phone popup lane |
| Project `.env` files | under `Coding/`, `dev/` | those projects |
| OneDrive July copies | `OneDrive - HEC Paris/_LAPTOP-BACKUP/` carries July copies of some of the above | nothing; they rotate and are stale |

## Known gaps and open questions

- Which bot token `sodanotif/push.env` holds (the savior bot or a third).
- Whether `~/.env/sodaos-bot` and `~/.env/tg-terminal` are still read by anything.
- Which account `triage/drive_token.json` and `triage/calendar_token.json` serve, and which of the five accounts has no `cal-*` token.
- The purpose of `~/.claude/wa-daemon/google-token.json`.
- Where Tailscale keeps its node key on each device, and whether Tailscale Serve is still configured on the laptop.
- The poller's Chrome `user-data-dir` path.
- The claude.ai account migration status (`~/.claude/MIGRATION-account-switch.md`).
- The `horus` Slack workspace: what it is for.
