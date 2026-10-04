# DATA-MAP: every store, who writes it, who reads it, where the copies are

The system keeps its state in a few hundred files spread over two machines, one Google Drive folder and a handful of cloud services; there is no database yet. Most state is JSON or JSONL inside the task-land repo (synced by git), the CRM is one 5.7 MB JSON file on the laptop with a read replica on the box, the memory is a git repo both machines write, and the message stores (WhatsApp, LinkedIn, Sent mail) are JSONL files that travel through the Drive `DA/` folder or do not travel at all. This document lists each domain as a table, then says for each kind of fact which copy is the truth, then lists the stores with no backup, then the planned Postgres on the box.

Last verified: 2026-10-01 (from the inventories of that day); 2026-10-04 19:15: Granola retired, the Meetings DB is fed by Notion's meeting AI; 2026-10-02: the CRM activity lines of inbound mail now
carry `full` (the mail text, 4,000 chars) next to `detail`, and `crm.json` is mirrored into Postgres `soda.crm` on the
box on every save (versions in `crm.doc_versions`).

Conventions: laptop paths start with `C:/Users/Alessandro/`, box paths with `/home/da/`. "mirror" = the robocopy or rsync copy that the git-sync scripts keep under `task-land/_system/laptop-tools/<name>/` or `_system/box-tools/<name>/` (secrets excluded; never run from a mirror). Sizes are from 2026-10-01. "Personal data" = names, emails, phones or message texts of third parties.

## 1. Tables per domain

### CRM (coattio)

| Store | Laptop path | Box path | Format and size | Writers | Readers | Backup | Personal data | In git |
|---|---|---|---|---|---|---|---|---|
| crm.json | `.medtech-crm/crm.json` | `coattio/crm.json` (`~/.medtech-crm` -> `/home/da/coattio`) | JSON 5.7 MB: `meta` 31 keys, `templates` 26, `companies` 441 with nested `people` 626, `signals` 41; about 140 person keys | ONE writer, `crm-app/server.js` `PUT /api/data`; through it: `intake-server.js` (:4137), `ingest-intake.js`, `crm-app/monitor.js`, `crm-app/peer.js` (box pull), `gtm-eng/commit-to-contacts.js` + `run-commit.py`, `coattio-notion-sync.js` | drawer-api, ask-api, review-api, events-api, handoff-api, owed.js, today-count.js, ai-draft, template-*, lemlist-*, `task-land/_system/hub_outdated.py`, `drafts/handoff.py`, `gtm-eng/campaign.py`, `agent/inbound_asks.py` | same-disk `backups/crm-<ts>.json` on every save (keep 30; 37 files on disk) + the box's pulled copy | yes | none (gitignored) |
| events-ledger.jsonl | `.medtech-crm/events-ledger.jsonl` | none | JSONL 861 KB, 1,762 lines | `monitor.js` | events-api, `campaign.py`, `inbound_asks.py` | none | yes | none |
| intake.jsonl, enrichments.jsonl, ai-drafts.jsonl, sent-log.jsonl | `.medtech-crm/` | none | JSONL (intake 476 lines) | intake-server, enrich worker, ai-draft, send path | intake UI, review | none | yes | none |
| monitor-state.json, observer-state.json, reader-state.json, reader-queue.json, lemlist-state.json, mirror-state.json, template-* | `.medtech-crm/` | none | JSON | the component of the same name | same | none | partly | none |
| review/<person>.json | `.medtech-crm/review/` | `coattio/review/` | JSON, 46 files (stores inventory) or 51 (repo inventory) | review-api | review UI | GitHub | yes | coattio |
| hospital-check/hospitals.json + inputs | `.medtech-crm/hospital-check/` | `coattio/hospital-check/` (tracked part) | JSON 164 KB tracked; inputs include a 2.1 MB crm copy and sent-mail metadata of 4 accounts (gitignored) | hospital-check scripts | CRM check board (box :4143 `crm-catchup.html`) | GitHub for the tracked file | yes | coattio (hospitals.json, no-email-items.json, two message texts) |
| crm.conflict-box-*.json (2), crm.before-*.json | `.medtech-crm/` | none | JSON 1.1 MB and 2.5 MB | one-off | nobody | none | yes | none |
| contacts-inbox.jsonl | `task-land/_system/contacts-inbox.jsonl` | same (synced) | JSONL | `triage/contacts_sync.py` on the box (every 30 min, failing since 2026-09-21) | hub card builder, intake | GitHub + both clones | yes | task-land |
| old CRM | `.lobbly-crm/crm.json` | none | JSON | nobody | nobody | none | yes | none |

### Tasks and the daily page

| Store | Laptop path | Box path | Format and size | Writers | Readers | Backup | Personal data | In git |
|---|---|---|---|---|---|---|---|---|
| Task files | `task-land/Tasks/{inbox 49, active 120, waiting 24, archive 173}` | `/home/da/task-land/Tasks/` | Markdown with YAML frontmatter (`status`, `bucket`, `project`, `due`, `surface_on`, `contact`, `stage`, `hub_card` ...) | `_system/daily-sync.ps1` + `daily-lib.ps1`, `capture.py`, `pipeline.py` (sole writer of `stage*`), `surface-sweep.ps1`, `crm-bridge.ps1`, the CRM's "Make it a task" | `/daily`, `/todo`, `/dump`, Obsidian, `/kb-query` task-join, box sessions | GitHub + box clone + OneDrive `_LAPTOP-BACKUP` (July) | yes (253 task files named after people) | task-land |
| Daily pages | `task-land/Daily/` 123 pages, `Events/` 2, `Habits/` 6 | synced | Markdown (editable checklist with `<!-- editable (subtasks:v1) -->` markers) | `daily-lib.ps1` render, Alessandro in Obsidian | `daily-sync.ps1` absorb | same | yes | task-land |
| context.md, agent-notes.md | `task-land/` | synced | Markdown | `vault-bridge-sync.ps1` (daily digest), sessions | `/daily`, `/compass`, `/triage` | same | some | task-land |
| daily-page-state.json, daily-mirror-ticks.json, slot-state.json | `task-land/_system/` | synced | JSON | `daily-lib.ps1` / `daily-sync.ps1`, `/slot-check` | the absorb pass | same | no | task-land |
| daily-sync.log, crm-bridge.log, surface-sweep.log | `task-land/_system/` | n/a | text | the scripts | debugging | mirror excludes logs (unverified whether these are tracked) | some | task-land (unverified) |

### Rules and evidence (the rule loop)

| Store | Laptop path | Box path | Format and size | Writers | Readers | Backup | Personal data | In git |
|---|---|---|---|---|---|---|---|---|
| Contracts | `task-land/_system/CRM-CONTRACT.md` (42 rules), `EMAIL-REVIEW-CONTRACT.md` (86), `HUB-CARD-CONTRACT.md` (21), `MEETING-CONTRACT.md` (8), `NOTIF-CONTRACT.md` (5); 162 rules | synced | Markdown, numbered rules with his quotes | `_system/drafts/addrule.py` only | `compile_skill.py` -> `~/.claude/skills/{crm,drafting,hub}/SKILL.md`; directly: `crm-app/reader.js` (CRM), `drafts/critic.py` (EMAIL), `agent/meeting_loop.py` (MEETING) | GitHub + both clones | his quotes name people | task-land |
| rule-hits.jsonl | `task-land/_system/rule-hits.jsonl` | synced | JSONL 1.5 MB, 7,384 lines, `merge=union` | `crm-app/observer.js`, `drafts/common.py`, `daily-campaign/build.py`, the hub guard on the box | `rule-stats.py`, `compile_skill.py`, `system-check.py`, `review-api.js` | same | some | task-land |
| decisions.jsonl | `task-land/_system/decisions.jsonl` | synced | JSONL 126 KB, 331 lines, `merge=union` | the hub on the box (every resolve or close), `review-api.js`, `events-api.js`, `board-server.js` | `feedback_worker.py`, `pipeline.py`, `system-check.py`, `box_linkedin_watch.py`, `hub_outdated.py` | same | yes (card texts) | task-land |
| system-feedback.jsonl (87), system-feedback-events.jsonl (108) | `task-land/_system/gtm-agent/` | synced | JSONL | `feedback_worker.py`, review-api "system" verdicts, `feedback_queue.py` | the GTM agent's updates | same | some | task-land |
| rule-loop-state.json, hub-edits.jsonl, hub-outdated-log.jsonl | `task-land/_system/` | synced | JSON / JSONL | the rule loop scripts, `hubedit.py`, `hub_outdated.py` | same | same | some | task-land |
| hints/ | `task-land/_system/hints/{agent-work,crm-reader,due-today,inbound-asks,meeting-loop}.md` | synced | Markdown | sessions | the gtm-eng agent scripts, every brief | same | no | task-land |
| outreach ledger | `task-land/_system/outreach/ledger.json` | synced | JSON 53 KB, caps + 247 entries | `ledger.py`, `campaign.py` | the send gate | same | yes | task-land |
| system checks | `task-land/_system/system-check-<n>.md` | synced | Markdown, weekly | `system-check.py` | `post_system_check.py` (22:58 cron) | same | some | task-land |

### Memory and brain

| Store | Laptop path | Box path | Format and size | Writers | Readers | Backup | Personal data | In git |
|---|---|---|---|---|---|---|---|---|
| Memory facts | `soda-brain/memory/` (360 files, 1.1 MB, `MEMORY.md` 13 KB index + sub-indexes, `_attic/` 6); Claude's path `.claude/projects/C--Users-Alessandro/memory` is a junction to it | `/home/da/soda-brain/memory/`; `~/.claude/memory` and `~/.claude/projects/-home-da/memory` are symlinks to it | Markdown with frontmatter (`type`: feedback 176, reference 136, project 29, user 2, none 14) | Claude sessions on both machines (topic file + an index line) | every session at start (MEMORY.md and sub-indexes), files on recall | GitHub + both clones | yes (notes name people) | soda-brain (two-way) |
| System map | `soda-brain/system/` (this folder) | `/home/da/soda-brain/system/` | Markdown | sessions, same turn as any service change | sessions before touching a service | same | no (by rule) | soda-brain |
| Secondary memory dirs | `.claude/projects/C--Users-Alessandro-task-land/memory` (13), `...quick-claude-workspace/memory` (25), `...sim-home/memory` (4, sim-born) | none | Markdown | sessions opened in those cwds | those sessions | none | some | none |
| Session transcripts | `.claude/projects/*/*.jsonl` about 900 MB, `history.jsonl` | `/home/da/.claude/projects/` (size unverified) | JSONL | Claude Code | `session-recall`, grep after compaction | none | yes | none |
| Claude config | `.claude/CLAUDE.md` 27 KB, `settings.json`, `settings.local.json`, `keybindings.json`, `.mcp.json`, `~/.claude.json` 96 KB (MCP servers, OAuth state), `mcp-parked/` | `/home/da/.claude/CLAUDE.md` -> `task-land/_system/vps/CLAUDE-box.md` (symlink), `settings.json` | Markdown, JSON | Alessandro, sessions | Claude Code | laptop: none; box CLAUDE.md: task-land | no | box CLAUDE.md only |
| Skills, commands, hooks, scripts | `.claude/skills/` 25 dirs 281 files (`synced/` 219 is the claude.ai cache), `commands/`, `hooks/`, `scripts/` 50, `loops/` | `/home/da/.claude/skills/` 28, `commands/` 72, hooks `tg-reply-context.py`, `block-destructive.sh`, `scan-secrets-before-push.sh` | files | the laptop (writer); pushed to the box by tar | Claude Code on both | hooks: `laptop-tools/hooks`; box skills: `box-tools/skills` (283 files, since 2026-10-01); laptop skills: `laptop-tools/skills` holds 3 files (the compiled crm, drafting, hub) | no | task-land mirrors only |

### Drafts lane (emails before they are sent)

| Store | Laptop path | Box path | Format and size | Writers | Readers | Backup | Personal data | In git |
|---|---|---|---|---|---|---|---|---|
| Sidecars | `task-land/_system/drafts/r*.md` (70) + `r*.critic.md` (97) | synced | Markdown with status (stub < registered < edited < finished), full message text | `register.py` on either machine, `critic.py`, `handoff.py`, `hubedit.py` | `reconcile.py` (box, every 5 min), the hub, `resolve_sidecar_conflicts.py` | GitHub + both clones | yes (full emails) | task-land |
| queue.jsonl | `task-land/_system/drafts/queue.jsonl` | synced | JSONL, `merge=union` | `register.py`, `send_card.py` | `reconcile.py` | same | yes | task-land |
| skill-map-*.json | `task-land/_system/drafts/` | synced | JSON | `compile_skill.py` | drafting skill | same | no | task-land |
| The Gmail drafts themselves | Google (accounts cdtm and tundra) | same | Gmail | sessions via `gmail.py` or the Gmail MCP | the hub (`gmail-send-draft` by draft id only, never edited text) | Google | yes | none |
| sent-log.jsonl | `.medtech-crm/sent-log.jsonl` | none | JSONL | the send path | audits | none | yes | none |

### Hub (approval cards)

| Store | Laptop path | Box path | Format and size | Writers | Readers | Backup | Personal data | In git |
|---|---|---|---|---|---|---|---|---|
| state.json (live) | none (the laptop `~/.claude/approval-hub/state.json` is a stale 2026-09-01 leftover) | `/home/da/approval-hub/state.json` | JSON, 204 to 208 KB of card texts; 63 open cards on 2026-10-01 18:11; resolved cards pruned 24 h after the verdict, open ones never | `approval-hub/server.js` only (`POST /pending`, `/resolve`, `/revise`, `/close`) | `hub-review/server.js` (reads the file from disk per request), the savior, `hub_outdated.py` (via HTTP), `daily-lib.ps1` (open-count via :4142) | rsync mirror `task-land/_system/box-tools/approval-hub/state.json` (tracked) | yes | task-land (mirror) |
| hub-rules.json, last-rejected.json | none | `/home/da/approval-hub/` | JSON | server.js | server.js, voice lane | mirror (hub-rules.json) | some | task-land (mirror) |
| hub-review queue | none | `/home/da/hub-review/queue.jsonl` | JSONL (commit lines the savior executes) | hub-review UI | the savior, `/api/queue/done` | none | yes | none |
| notification-log.jsonl | `.claude/sodanotif/notification-log.jsonl` (old laptop daemon) | `/home/da/sodanotif/notification-log.jsonl` | JSONL, every card ever pushed | sodanotif `push.js`, the hub | the savior (resolving "N" and bare replies) | none (mirror excludes *.jsonl) | yes | none |
| Durable verdicts | `task-land/_system/decisions.jsonl` | synced | see Rules and evidence | the hub | pipeline, feedback worker | GitHub | yes | task-land |

### Campaigns and boards (gtm-eng)

| Store | Laptop path | Box path | Format and size | Writers | Readers | Backup | Personal data | In git |
|---|---|---|---|---|---|---|---|---|
| Boards | `gtm-eng/boards/<slug>/` 22 boards, 7.3 MB: `board.json` (evidence), `state.json` (his verdicts), `campaign/plan.json`, `commits/*.json`, `research-*.json` | `/home/da/gtm-eng/` (a copy taken out of the mirror; its server is dead) | JSON | `board-server.js` :4141 (state), `campaign.py` (plan, never from `--dry`), `run-commit.py` (commits), `build.py` (daily boards) | the board UI, `daily-lib.ps1` (daily campaign line), `fire.py`, `gtm_agent.py` | mirror `task-land/_system/laptop-tools/gtm-eng/` (719 files) | yes (`plan.json`, `research-people.json`) | task-land (mirror) |
| Daily campaign | `gtm-eng/daily-campaign/`: `pool.json` 869 KB (440 people), `daily-state.json`, `bounces.json`, `competition.json`, `notion-*.json`, `notion-names-snapshot.json` (308 names), `runs/`, `drafts-cache.json`, `ICP.md` | none | JSON | `research.py`, `supervise.py`, `review.py`, `build.py`, `fire.py`, `postmortem.py` | `pick.py`, `build.py`, the board | mirror | yes | task-land (mirror) |
| Agent | `gtm-eng/agent/`: `config.json`, `state.json`, `runs.jsonl` 299, `incidents.jsonl` 356, `inbound-asks-state.json` + `.jsonl`, `meeting-loop-state.json` + `.jsonl`, `feedback-worker-state.json`, `inbound-bodies/`, `followup-bodies/` | heartbeat only: `~/.local/state/gtm-agent/heartbeat.json` | JSON / JSONL | `gtm_agent.py`, `inbound_asks.py`, `meeting_loop.py`, `feedback_worker.py` | `gtm_agent.py status|incidents|missed`, `box_watch.py` | mirror | yes (message bodies) | task-land (mirror) |
| Signatures | `gtm-eng/signatures/founder.{html,txt}`, `student.{html,txt}` | none | HTML, text | by hand | `draft.js`, `campaign.py` | mirror | his own | task-land (mirror) |
| Gmail labels `Campaign/<slug>` | Google (tundra account) | same | Gmail labels, set at send time | `campaign.py label_campaign` | `gmail_replied`, audits | Google | yes | none |
| lemlist | cloud (lemlist MCP) + `.medtech-crm/lemlist-state.json` | none | cloud + JSON | `lemlist-*` scripts | same | lemlist cloud | yes | none |

### Mail, calendar, contacts

| Store | Laptop path | Box path | Format and size | Writers | Readers | Backup | Personal data | In git |
|---|---|---|---|---|---|---|---|---|
| Mailboxes | Google: cdtm, tundra, sodano23, alesoda2002, lobbly; HEC is Outlook (no token) | same | Gmail | people, the hub (`gmail-send-draft`), `campaign.py` (tundra), `gmail.py` (cdtm) | `triage/gmail.py` (both machines), `sodanotif/pollers/gmail_poll.py` (box, 60 s), `hub_outdated.py` (every account, every 10 min), `reconcile.py`, the Gmail MCP | Google | yes | none |
| Token files | `triage/tokens/` 12 (`alesoda2002, cdtm, lobbly, sodano23, tundra`, `cal-*` x4, `contacts-alesoda2002`, `drive-cdtm`, `drive-tundra`), `triage/{credentials,calendar_token,drive_token}.json` | `/home/da/triage/tokens/*.json`, `credentials.json`, `calendar_token.json`, `drive_token.json` | JSON (secrets) | OAuth flows | gmail.py, gcal.py, drive.py, contacts_sync.py, eod_sweep.py | none by design (mirror excludes tokens) | n/a | none |
| triage state | `triage/state.json`, `wa-state.json` | `/home/da/triage/` | JSON | `/triage`, `/snm` | same | mirror (`laptop-tools/triage`, `box-tools/triage`) | some | task-land (mirror) |
| Sent corpus | `.claude/sent-corpus/corpus.jsonl` 3 MB, 8,897 lines | none | JSONL | `harvest.js` (task SentCorpus-Harvest) | `monitor.js`, `drawer-api.js`, `ask-api.js`, the drafting skill | none | yes | none |
| Voice corpus | `.claude/outreach/corpus.json` 192 KB | none | JSON | by hand / sessions | message-builder, drafting | none | his own voice, some names | none |
| Calendars | Google, `primary` of the chosen account (no group-calendar id hardcoded) | same | Google Calendar | `gcal.py`, `eod_sweep.py` (23:00 event), the dead-man switch ("VPS DOWN" events in the CDTM calendar), `/slot-check`, the Calendar MCP | `/daily`, slot checks, the meeting loop | Google | yes | none |
| Google Contacts | account alesoda2002 | same | Google | the phone | `contacts_sync.py` -> `contacts-inbox.jsonl` | Google | yes | none |
| Slack | `.claude/slack/tokens/{cdtm,horus,xplore}.json`, `slack.py` | `/home/da/slack/{slack.py,credentials.json,tokens/}` | JSON (secrets) + API | the hub (`slack-send`), `/slack` | `sodanotif/pollers/slack_poll.py` (60 s), `/triage` | Slack cloud; tokens not backed up | yes | none |
| sodanotif stores | none live (`.claude/sodanotif/` is the old laptop daemon) | `/home/da/sodanotif/stores/` (Gmail, Slack, LinkedIn, WA tap state) | JSON | `daemon.js`, the pollers | `daemon.js` classify, `push.js` | `task-land/_system/box-tools/sodanotif/` (the laptop inventories say Gmail/Slack state IS tracked there; the mirror rule says `stores/` is excluded) | yes | task-land (mirror, see FINDINGS) |

### WhatsApp

| Store | Laptop path | Box path | Format and size | Writers | Readers | Backup | Personal data | In git |
|---|---|---|---|---|---|---|---|---|
| Box message store (live) | read as `G:/My Drive/DA/wa-store.jsonl` 4.4 MB (`CRM_WA_SHIP`) | `/home/da/wa-daemon/message-store.jsonl`; copy at `/home/da/gdrive/DA/wa-store.jsonl` | JSONL | `wa-daemon/daemon.js` (Baileys, `da-wa.service`); `ship-wa-store.sh` copies it every minute | `monitor.js`, `drawer-api.js`, `inbound_asks.py`, `hub_outdated.py`, `sodanotif` (WA tap), `wa-daemon/search.js`, `/wa`, `/wa-search` | the Drive copy only | yes | none |
| Laptop message store (old daemon) | `.claude/wa-daemon/message-store.jsonl` 19 MB, 57,785 lines; `chats-state.json`, `contacts.json`, `chats.json`, `auth/` 7,633 Signal key files; laptop WA tasks Disabled | n/a | JSONL + Signal keys | nothing now | `drawer-api.js`, `monitor.js`, `inbound_asks.py`, wa skills (`WA_STORE`) | none | yes | none |
| Box daemon auth | none | `/home/da/wa-daemon/auth/` | Signal keys (secrets) | Baileys | Baileys | none by design | n/a | none |
| Send API | none | `127.0.0.1:4119`, `send.js` | HTTP | the hub (`wa-send` on a yes), sessions on the box | n/a | n/a | n/a | none (wa-daemon is not in any repo) |

### LinkedIn

| Store | Laptop path | Box path | Format and size | Writers | Readers | Backup | Personal data | In git |
|---|---|---|---|---|---|---|---|---|
| LinkedIn store | `G:/My Drive/DA/linkedin-store.jsonl` 53 KB, 79 lines (`LINKEDIN_STORE`) | `/home/da/gdrive/DA/linkedin-store.jsonl` | JSONL | `.claude/linkedin-poll/poll.py` (task LinkedIn-Poll, Chrome with a dedicated profile) | `monitor.js`, `drawer-api.js`, `inbound_asks.py`, box sodanotif | Drive | yes | none |
| Accept bot | `.claude/linkedin-accept-bot/*.json`, `~/.env/linkedin-accept-bot.env` | none | JSON | the accept bot | same | none | yes | none |
| Launcher and reaper | `.claude/linkedin-poll/` `reap.log`, `launcher.py` | none | log | `launcher.py` | debugging | none | no | none |
| Session safety | `gtm-eng/agent/li_probe.py` (laptop), `task-land/_system/gtm-agent/box_linkedin_watch.py` (box cron every 10 min) | synced script | code | n/a | n/a | task-land | no | task-land |
| Sends | `campaign.py` invites and DMs (plain invite, intro DM on accept, H74 DM) | n/a | LinkedIn | `campaign.py` | n/a | the CRM row's `campaigns[]` trace | yes | none |

### Notion

| Store | Laptop path | Box path | Format and size | Writers | Readers | Backup | Personal data | In git |
|---|---|---|---|---|---|---|---|---|
| Contacts DB | cloud; data source `a747cb32-a4bd-42bf-818e-df4c97390f4f` | same | Notion database | `coattio-notion-sync.js` (CRM -> Contacts), `campaign.py plan` (contacts to CRM + Notion first) | `daily-campaign/review.py`, `notion-names-snapshot.json` builder | Notion | yes | none |
| Meetings DB | cloud; data source `3a3b30c6-d57e-8093-9e35-000b79676b41` (env `CRM_NOTION_MEETINGS_DS`) | same | Notion database | Notion's meeting AI, `scripts/notion-meeting-filer.ps1` (task Notion-MeetingFiler); Granola, `granola-auto`, `/granola` retired 4 Oct 2026 | `crm-app/sources.js` notionScan (Meetings -> CRM), `agent/meeting_loop.py`, `drafts/handoff.py` | Notion | yes | none |
| Tundra workspace | cloud; `0f7b30c6-d57e-818c-ad08-0003a268b635` | same | Notion | people | same | Notion | yes | none |
| TRIMEDX-affiliated hospitals | cloud; page `3e6b30c6-d57e-8135-a67c-e81651d01d73`, data source `2cdbc0d0-de27-4681-9132-b9e0ec8a6be6` (private draft, 2026-09-25) | same | Notion database | `review.py` | the daily campaign cards | Notion; local `competition.json` | no (hospitals) | none |
| Access | no API token anywhere: the Notion MCP (`https://mcp.notion.com/mcp`, OAuth state in `~/.claude.json`) via `claude -p --strict-mcp-config --mcp-config <notion.mcp.json>` | same pattern on the box (`CLAUDE_BIN=/usr/bin/claude`) | n/a | n/a | n/a | n/a | n/a | n/a |
| Local snapshots | `gtm-eng/daily-campaign/notion-*.json`, `notion-names-snapshot.json`; `.claude/granola-auto/state.json` (retired 4 Oct 2026, kept as history) | none | JSON | the scripts above | the scripts above | mirror (gtm-eng) | yes | task-land (mirror) |

### Drive

| Store | Laptop path | Box path | Format and size | Writers | Readers | Backup | Personal data | In git |
|---|---|---|---|---|---|---|---|---|
| CDTM My Drive | `G:/My Drive/` (Google Drive desktop client) | `/home/da/gdrive/` (rclone mount `cdtm:`, `da-gdrive.service`, 1.5 GB cached) | Google Drive | both machines | both machines | Google | yes | none |
| The DA exchange folder | `G:/My Drive/DA/` | `/home/da/gdrive/DA/`: `wa-store.jsonl`, `linkedin-store.jsonl`, `trippy/` | JSONL, JSON | box (wa-store, every minute), laptop (linkedin-store), trippy | the other machine | Google | yes | none |
| Phone verdict files (older lane) | `From phone/sodaos` on Drive | n/a | text files `claude-verdict-<id>-<yes|no>.txt` | MacroDroid (deactivated lane) | `watch-voice.ps1` (historical) | Google | no | none |
| Tundra Shared Drive | n/a (token `drive-tundra`) | `/home/da/tundra-drive/` (rclone mount `tundra:`, 386 MB cached) | Google Drive | Tundra team | `da-voice.timer` (long recordings), `drive.py` | Google | yes | none |
| Audio notes drop | `OneDrive - HEC Paris/Audio Notes/` (+ `_processed/`) | none | mp4, m4a, transcripts | the phone (email or save) | `/audio-to-notes`, `transcribe.py` | OneDrive | his own | none |
| OneDrive backup copies | `OneDrive - HEC Paris/_LAPTOP-BACKUP/` 44,086 files, newest 2026-07-25: task-land, vault_kb, 07-thesis-kb, self-reflection-wiki, July secrets | none | plain copies | nothing since July | nobody | OneDrive | yes | none |
| rclone config | none | `~/.config/rclone/rclone.conf` (remotes `cdtm:`, `tundra:`) | secret | once | the two mount units | none by design | n/a | none |

### Vaults (Obsidian, the LLM-wiki engine)

| Store | Laptop path | Box path | Format and size | Writers | Readers | Backup | Personal data | In git |
|---|---|---|---|---|---|---|---|---|
| vault_kb (personal second brain) | `vault_kb/` 148 md (168 tracked): `Raw/ Sources/ Self/ Projects/ People/ Orgs/ Topics/`, `index.md`, `catalog.jsonl`, `log.md`, `project-registry.md` (the join key to task-land), `_meta/` (the KB README, engine-ignored) | `/home/da/vault_kb/` | Markdown + catalog.jsonl; `task_join: enabled`, `related_vaults: [mpd-kb, medtech-brain]`, bridge target of mpd-kb (`MPD:STATE`) and of `cdtm-taskforce/progress.json` (`CDTM-ONBOARDING:STATE`) | `/kb-ingest`, `/kb-maintain`, `/granola`, `/audio-to-notes`, `/cdtm`, Alessandro in `Raw/` | `/kb-query`, `/dump`, `/daily` (registry), Obsidian | GitHub + box clone + OneDrive July | yes (People/ pages, two thesis PDFs) | vault_kb |
| medtech-brain (Tundra company brain) | `medtech-brain/` 173 md: `Raw/ Sources/ Company/ Accounts/ Market/ People/ Topics/ _system/ Clippings/`; `_system/OUTREACH-SYSTEM.md` | `/home/da/medtech-brain/` | Markdown; `bridge: false`, `task_join: false`, standalone | `/kb-ingest` targeted at it (push-back from Tundra tasks, reviewable `Sources/` page) | `/kb-query` (also via vault_kb's related_vaults), `Projects/tundra.md` pointer | GitHub + box clone | yes (Accounts/, People/, call notes, AIIC brochure 4.3 MB) | medtech-brain |
| task-land (as a vault) | `task-land/` 826 md | `/home/da/task-land/` | see Tasks | see Tasks | Obsidian | GitHub + box | yes | task-land |
| 07-thesis-kb | `07-thesis-kb/` 92 md, 19.6 MB (`Raw/Sources/Concepts/Topics/Authors/Projects`, `citation_rule: strict`, `bridge: disabled`, `task_join: disabled`) | none | Markdown + PDFs | `/kb-*` | `/kb-query`; the thinking skills still read vault_kb | OneDrive copy of July only | yes (practitioner calls) | none |
| mpd-kb | `mpd-kb/` 228 md (99 Sources, 14 to 15 compiled; bridge to `vault_kb/Projects/mpd.md`) | none | Markdown | `/kb-*` (ingest complete 2026-07-11) | `/kb-query` via vault_kb | NONE (no copy at all) | yes (about 90 interviews) | none |
| self-reflection-wiki | `self-reflection-wiki/` 22 md, 34 MB, contract-less (not yet an engine), `isolation: true` planned | none | Markdown | Alessandro | nobody yet | OneDrive copy of June | yes (private) | none |
| _kb-archive | `_kb-archive/thesis-kb-merged-2026-07-03/`, `vault_kb-mpd-split-2026-07-11/` | none | copies | nothing | revert path | none | yes | none |
| lobbly-kb | `lobbly-kb/` (`build-kb-html.py` + `raw/` -> HTML; not an engine vault) | none | HTML corpus | the script | browser | none | some | none (unverified) |
| thesis-system | `thesis-system/` (drafts, the reference repo, `CLAUDE.md` contract, `architecture.html`) | none | Markdown | `/scientific-drafting` | Alessandro | third-party clone inside is on GitHub (paablos8); drafts unverified | no | partial (unverified) |
| Zotero | `%USERPROFILE%/Zotero/storage/<KEY>/` (collections `founder-legitimacy`, `deterministic-legal-ai`) | none | PDFs + Zotero DB | Zotero app | the thesis skills (MCP parked: `mcp-parked/zotero.mcp.json`) | Zotero sync (unverified) | no | none |

### Voice

| Store | Laptop path | Box path | Format and size | Writers | Readers | Backup | Personal data | In git |
|---|---|---|---|---|---|---|---|---|
| Long-form voice lane | n/a | `/home/da/voice-lane/` 457 MB (state + venv with faster-whisper); input = long recordings on the Drive mount | audio, transcripts, state | `da-voice.timer` every 5 min (`voice-longform-vps.py`, safe-word routing) | the routing (hub cards, tasks) | none (not in any repo) | yes | none |
| Fast lane (laptop) | `.claude/voice-lane/state.json`, `voice-lane/config.json` (phone webhook URL) | none | JSON | the voice lane, `rail_lane.py` | the hub (`/pending`) | none | some | none |
| Audio notes | `OneDrive - HEC Paris/Audio Notes/`, `.claude/audio-notes/transcribe.py` (faster-whisper small, CPU) | none | mp4 + `.transcript.txt` | the phone, `/audio-to-notes` | the target vault's `Raw/` | OneDrive | his own | none |
| Quick Claude | `.claude/quick-claude/` (Alt+Win+J then J/K/D) | none | code + `.qc-*` state | the hotkey | n/a | mirror `laptop-tools/quick-claude` (117 files, state excluded) | no | task-land (mirror) |

### Langfuse

| Store | Laptop path | Box path | Format and size | Writers | Readers | Backup | Personal data | In git |
|---|---|---|---|---|---|---|---|---|
| Traces | cloud, host `cloud.langfuse.com` | same | Langfuse | `.claude/hooks/langfuse_hook.py` (every Claude Code turn; state `.claude/state/langfuse_state.json`), `linkedin-poll/poll.py`, `loops/langfuse-optimizer/lf_calls.py`, the simulation (`simclaude.py`) | `/langfuse-bananza`, the optimizer loop | Langfuse cloud | yes (prompts carry names) | none |
| Keys | `~/.env/langfuse.env` (plus a plaintext duplicate inside `~/.env/openai-thesis-note.txt`); `mcp-parked/langfuse.mcp.json` | none named | secret | once | the hook and scripts | none by design | n/a | none |

### Simulation

| Store | Laptop path | Box path | Format and size | Writers | Readers | Backup | Personal data | In git |
|---|---|---|---|---|---|---|---|---|
| sim/harness | `sim/harness/` (git, master, 30 commits, 130 tracked, NO remote) | none | code + sandbox copies of the email ledger, fake tokens | the simulation | `simclaude.py`, Langfuse | none (only copy on disk) | sandbox copies only | local git, no remote |
| sim-home memory | `.claude/projects/...sim-home/memory` (4 files) | none | Markdown | sim sessions | nobody (to delete) | none | no | none |

## 2. Truth and copies

| Kind of fact | Source of truth | Copies and what they are |
|---|---|---|
| A person, their stage, their next step | `crm.json` on the laptop, written only by `crm-app/server.js` | the box `coattio/crm.json` is a pull (`peer.js`), a read replica for the phone page and the box scripts; `backups/crm-<ts>.json` are same-disk snapshots; Notion Contacts is a projection kept by `coattio-notion-sync.js`; `review/*.json` dossiers are derived; `task files with contact:` are retired (the CRM owns every follow-up since 2026-09-19) |
| Whether an email was sent | Sent mail in the Google account (cdtm or tundra) | a hub card is a proposal, never state; `sent-log.jsonl`, `outreach/ledger.json`, the CRM activity line and the `Campaign/<slug>` label are records written at send time; check SENT and the calendar before saying "pending" |
| A hub decision | `task-land/_system/decisions.jsonl` (append-only, synced, union-merged) | the hub's `state.json` holds the open cards and resolved ones for 24 h; `box-tools/approval-hub/state.json` is a minute-old mirror; the hub-review page is a view of the same file; a committed hub-review batch IS the yes |
| An email in review | the Gmail draft (by draft id) | the sidecar `_system/drafts/r*.md` carries status and text, the card carries the preview; the hub sends by draft id only, never edited text; a conflict between two sidecars resolves to the more advanced status |
| A task, its bucket and date | the task file's frontmatter under `task-land/Tasks/` | the daily page is a rendered view that is absorbed back on every watcher pass; `daily-page-state.json` says what we rendered; `stage` is written by `pipeline.py` from the hub card |
| A rule | the contract file (`*-CONTRACT.md`), one numbered line per rule | the compiled skills (`crm`, `drafting`, `hub`) are generated; `rule-hits.jsonl` is evidence of use, not the rule |
| A memory | `soda-brain/memory/<topic>.md` plus its index line | the repo is two-way: both clones are peers, GitHub is the meeting point; the planned `brain` schema is an index, not a second truth |
| A WhatsApp message | the box daemon's `message-store.jsonl` (the live linked device) | `gdrive/DA/wa-store.jsonl` is a minute-old copy the laptop reads; the laptop `wa-daemon` store is a frozen older history (different line count, 57,785) |
| A LinkedIn event | LinkedIn itself | `DA/linkedin-store.jsonl` is what the laptop poller saw; the CRM row's `campaigns[]` is the trace of what we sent |
| A meeting | Notion's meeting AI note (Granola retired 4 Oct 2026) | the CRM row's `meeting_event_id`, the meeting loop's state file; old vault `Raw/` notes from the retired `/granola` |
| Company knowledge | the vault's compiled pages (`medtech-brain` for Tundra, `vault_kb` for Alessandro) | `catalog.jsonl` and `index.md` are generated; `Raw/` is immutable input; the task-land digest in `context.md` is a daily summary |
| The code of a tool | its real folder (`gtm-eng/`, `triage/`, `approval-hub/` ...) | `laptop-tools/` and `box-tools/` mirrors are backups refreshed by the sync scripts: restore by copying OUT, never run or edit inside |
| Which machine is up | `_system/health.json` (laptop) and `_system/health-vps.json` (box), each written by its own machine | the other machine reads the synced copy; staleness is the alarm (and also what a parked sync looks like) |
| Files exchanged between the machines | the Drive `DA/` folder (`G:/My Drive/DA` = `/home/da/gdrive/DA`) | not git: the two stores there are too live for a repo |

## 3. Stores with no backup (as of 2026-10-01)

1. `C:/Users/Alessandro/.claude/wa-daemon/` (19 MB store, chats, contacts, 7,633 Signal key files). The box daemon's `auth/` is equally unbacked.
2. `C:/Users/Alessandro/.claude/sent-corpus/corpus.jsonl` (3 MB) and `C:/Users/Alessandro/.claude/outreach/corpus.json` (192 KB).
3. `C:/Users/Alessandro/.claude/skills/` (24 to 25 skills), `loops/`, `scripts/`, `CLAUDE.md`, `settings.json`, `.mcp.json`. The box's copy of the skills is mirrored into task-land since 2026-10-01; the laptop mirror `laptop-tools/skills` holds only the three compiled skills.
4. Session transcripts (about 900 MB) and `history.jsonl`, both machines.
5. `.medtech-crm` runtime data: `crm.json`, `events-ledger.jsonl`, every state file; only same-disk `backups/` and the box's pulled `crm.json`.
6. Vaults 07-thesis-kb (OneDrive copy of July), mpd-kb (no copy at all), self-reflection-wiki (June copy), `_kb-archive`.
7. Secrets on both machines (excluded by design; the OneDrive July copies are stale and rotate).
8. The small `~/.claude/*` state dirs (granola-auto, snm-receiver, voice-lane, linkedin-accept-bot, tg-bridge history, jobs timelines, curriculum-server data) and the secondary memory dirs (task-land 13 files, quick-claude 25).
9. Box code outside any repo and outside the mirrors: `hub-review/`, `wa-daemon/`, `tg-bridge/`, `slack/`, `research-page/`, `gtm-eng/`, `tg-reply-resolver/`, `voice-lane/`, `~/.local/bin/*.sh` (only `.bak-*` files as rollback).
10. `hub-review/queue.jsonl` and `sodanotif/notification-log.jsonl` on the box (runtime JSONL excluded from the mirror).

## 4. Planned: Postgres on the box

Database `soda` on the box, owned by the `da-brain` service (`100.85.52.84:4150`, MCP + HTTP), two schemas:

- `brain`: an index over `soda-brain/memory/*.md` and `soda-brain/system/*.md` (one row per file with frontmatter fields, one row per chunk for search), rebuilt by `da-brain-index.timer`. The repo stays the source of truth; the schema is a derived copy and can be dropped and rebuilt at any time.
- `crm`: CRM document versions (every `PUT /api/data` becomes a versioned row, replacing the same-disk `backups/crm-<ts>.json` ring of 30) and CRM rows (companies, people, signals) written through the `da-brain` service. What moves there first: the version history and the row projection; `crm.json` on the laptop stays the writer until the service is proven, after which the box stops being a pull replica.

Open: cadence of the index timer; whether the `crm` schema takes writes from the laptop over Tailscale or from the box copy; backup of the Postgres data directory (the box has no snapshot policy recorded in the sources).

## Known gaps and open questions

- `review/*.json` count: 46 (stores inventory) vs 51 (repo inventory).
- Whether sodanotif Gmail/Slack state is tracked in `box-tools/sodanotif/` (the laptop inventories say yes; the mirror rule says `stores/` and `*.jsonl` are excluded).
- Whether the `_system/*.log` files of task-land are tracked or ignored.
- The box's `.claude/projects/` transcript size.
- Bind address and data of `lobbly-kb` and `thesis-system` git state.
- The size of the box `coattio/crm.json` replica and how often `peer.js` pulls.
- Secondary memory dirs: which of the 13 task-land and 25 quick-claude notes are worth moving into `soda-brain/memory/`.
- Zotero sync status.
