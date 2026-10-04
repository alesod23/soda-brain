# MACHINES: the laptop, the box, the phone

The system runs on two computers and one phone joined by a Tailscale tailnet. The laptop (Windows 11, `desktop-1bojsrg`, Tailscale 100.127.7.80) is where Alessandro works: Chrome, Obsidian, the CRM writer, the GTM boards, and every scheduled task that touches his screen or his Chrome profiles. The box (Ubuntu 24.04 VPS, hostname `vmd202974`, Tailscale name `da-box`, 100.85.52.84) is always on and holds everything that must not depend on the laptop being awake: the Telegram savior session, the approval hub, the WhatsApp daemon, the notification daemon, the pollers, cron and systemd jobs, and the two Google Drive mounts. The phone (`pixel-9a`, 100.121.68.86) is a Telegram client and the hub-review page; it runs nothing of its own. The repos (task-land, soda-brain, vault_kb, medtech-brain, coattio, travel-search) are the shared state between the two computers; the Drive folder `DA/` carries the two data files that are too big or too live for git.

Last verified: 2026-10-01 (from the inventories of that day). 2026-10-04 03:17 (`schtasks /query`, laptop): the
table in section 4 is corrected by the visual map `SODA-SYSTEM-MAP.html`: DA-MeetingLoop every 5 min (not 30),
DA-InboundAsks 15 min, DA-FeedbackWorker 10 min, LinkedIn-Poll 15 min, SentCorpus-Harvest 07:30, Notion-MeetingFiler
hourly, DA-HubForward 5 min keep-alive, Voice-Lane-Watch enabled every minute; tasks missing here: DA-Supervisor
(10 min), DA-InstinctInbox (15 min), DA-DueToday (08:30), Granola-Auto-Sweep (08:15; DISABLED 4 Oct 19:12, Granola retired), Peer60-AcceptCheck (09:00,
18:00), RuleLoop-SystemCheck (09:10), SODANOtif-Recap (2 h), CDTM-Kickoff-Weekly-Update (Thu 16:00); the laptop
hub-era tasks (Approval-Hub-Watchdog, Push-Lane-Watchdog, WA-Daemon-*, TG-*, SODANOtif-Daemon-*) are Disabled.
`da-brain.service` and `da-brain-index.timer` (section 9) are live since 2 Oct. Section 3: the daily pg_dump at
03:30 writes to the Drive mount.

## 1. The three devices

| Device | Identity | OS and hardware | Role |
|---|---|---|---|
| Laptop | Tailscale `desktop-1bojsrg`, 100.127.7.80, tailnet `taile93f00.ts.net` | Windows 11 Home 10.0.26200, 16 GB RAM (Windows sees 11.7), PowerShell 5.1, Git Bash | Chrome (daily driver and all browser automation, dedicated user-data-dir per skill), Obsidian vaults, the CRM writer (coattio :4124 and intake :4137), GTM boards (:4141), the design-sync server (:4190), Claude Code sessions, every Windows scheduled task (always launched through `run-hidden.vbs`, never a visible console) |
| Box | hostname `vmd202974`, Tailscale `da-box`, 100.85.52.84, public IP 169.58.128.217 | Ubuntu 24.04, kernel 6.8.0-136, 4 vCPU, 7.9 GB RAM, 96 GB disk (19 GB used), uptime 57 days on 2026-10-01 (since about 2026-08-04); python3 3.12.3, node v22.23.2, bun, claude 2.1.283 at `/usr/bin/claude`, rclone; user `da` | Always on: the Telegram savior (tmux `savior`, the only Telegram poller), the approval hub (:4180), hub-review (:4142), WhatsApp daemon (Baileys, send API :4119), sodanotif, tg-bridge (second bot), Gmail and Slack pollers, cron, systemd timers, the two rclone Drive mounts, the git sync timers, the box copies of the CRM servers (:4124, :4137), trippy (:4126), the research-page servers (:4143 to :4145) |
| Phone | Tailscale `pixel-9a`, 100.121.68.86 | Android (Pixel 9a) | Telegram (savior lane, hub cards), hub-review page at `http://100.85.52.84:4142/` over Tailscale, CRM page at `http://100.85.52.84:4124`; no services |

Hosting provider: `CLAUDE-box.md` calls the box "Contabo"; `VPS-SETUP.md` describes a Hetzner CX32 (Falkenstein or Nuremberg, 8 GB RAM, 80 GB disk). The inventory measured 7.9 GB RAM and 96 GB disk, which matches neither document exactly. Unverified which provider bills the box.

Why this split: the laptop is the writer for anything that needs Chrome, Windows apps, or his attention (CRM edits, board reviews, drafting); it sleeps, so nothing time-critical lives only there. The box never sleeps, so it owns every listener (Telegram, WhatsApp, hub) and every schedule that must fire at night. The portability promise in `VPS-SETUP.md`: nothing in `task-land/_system/vps/` knows which provider it is on; `bootstrap.sh` plus the systemd units turn any Ubuntu machine into the box.

## 2. The Tailscale link

- Tailnet name `taile93f00.ts.net`. Three nodes: `da-box` 100.85.52.84, `desktop-1bojsrg` 100.127.7.80, `pixel-9a` 100.121.68.86.
- Laptop to box traffic: the laptop's `127.0.0.1:4180` is a raw TCP forward (`~/.claude/approval-hub/forward-to-box.js`, task `DA-HubForward`) to `100.85.52.84:4180`, so every laptop producer that posts to localhost reaches the box hub. `forward-hub-review.js` sits beside it.
- Laptop reads `http://100.85.52.84:4142/api/open-count` (daily page hub line), `pipeline.py` and `gtm_agent.py` read :4142 too.
- Box reads the laptop only through git (synced files) and through the GTM-agent heartbeat the laptop pushes over ssh into `/home/da/.local/state/gtm-agent/heartbeat.json`.
- Phone reaches :4142 and :4124 on the box over Tailscale. An older design proxied the laptop CRM to the phone with Tailscale Serve (`reference_coattio_tailscale`); the box now serves the phone directly.
- ssh: the laptop reaches the box as user `da`; `~/.ssh/` on the box holds `id_ed25519` plus one deploy key per GitHub repo, selected by host aliases in `~/.ssh/config`.

## 3. Ports and owners

### Laptop

| Port | Owner | Kept alive by | Notes |
|---|---|---|---|
| 4124 | `C:/Users/Alessandro/.medtech-crm/crm-app/server.js` (coattio CRM UI and API; the ONLY writer of `crm.json`) | `Coattio-Watchdog` every 5 min + resume-from-sleep event triggers (`coattio-serve.ps1`) | never start via a tool background process (the harness reaps it) |
| 4137 | `.medtech-crm/intake-server.js` (intake, Alt+K, task-handoff, enrich worker) | `Coattio-Watchdog` | `POST /task-handoff` is what `crm-bridge.ps1` calls |
| 4141 | `gtm-eng/board-server.js` (GTM board index and boards) | laptop task (named in sources as part of the Coattio-Watchdog family, exact task unverified) | daily page reads `/api/board/daily-<date>`; boards open ONLY via `open-board.ps1` |
| 4180 | `~/.claude/approval-hub/forward-to-box.js` | task `DA-HubForward` | TCP forward to the box hub; the laptop `server.js` beside it is a dead 2026-09-01 copy |
| 4190 | tundra-design `sync/dsync.py serve` (Claude Design <-> GitHub sync) | task `DesignMirror-Server` (logon, 1-min keep-alive, `pythonw`) | commits every extension snapshot, pulls, pushes |
| 4123 | old outreach CRM (`project_outreach_crm`) | none known | listed in memory only; unverified whether anything still listens |

### Box

| Port | Bind | Owner | Kept alive by |
|---|---|---|---|
| 22 | 0.0.0.0 | sshd | systemd (stock) |
| 4119 | 127.0.0.1 | `wa-daemon/daemon.js` send API | `da-wa.service` |
| 4124 | loopback + Tailscale | `coattio/crm-app/server.js` (box copy, `COATTIO_BOX=1`) | tmux `coattio`; `coattio-sync.sh` every 2 min ensures both servers are up |
| 4126 | 100.85.52.84 | trippy `travel-search/app/server.js` | cron `trippy-supervise.sh` (@reboot and every 5 min, see surprise 1) |
| 4137 | loopback + Tailscale | `coattio/intake-server.js` (box copy) | tmux `coattio` + `coattio-sync.sh` |
| 4141 | nothing | gtm-board-server dead since 2026-09-19 | nothing starts it |
| 4142 | 100.85.52.84 | `hub-review/server.js` (phone review page; reads the hub's `state.json` from disk, writes only through hub HTTP routes; loopback refuses by design) | cron `hub-review-supervise.sh` (@reboot and every 5 min) |
| 4143 | unverified | `research-page` static `http.server` (event companion pages) | nothing (orphaned claude shell parent) |
| 4144 | unverified | `research-page/event_server.py` | nothing |
| 4145 | unverified | `research-page/snitem_server.py` | nothing |
| 4180 | 0.0.0.0 | `approval-hub/server.js` (the live hub; `HUB_HOST=0.0.0.0`) | `da-hub.service` (`Restart=always`) |
| 4150 | 100.85.52.84 | PLANNED `da-brain` (see section 9) | PLANNED systemd |

## 4. Scheduled tasks on the laptop (schtasks)

Every task named in the sources. Cadence and script as the sources state them; a task with no cadence in any source is marked unverified. Standing rule since 2026-09-28: a scheduled task never runs powershell, cmd, python, node or a .cmd directly; it runs `wscript.exe //B //Nologo "C:/Users/Alessandro/task-land/_system/window-watch/run-hidden.vbs" "<workdir>" "<log or ->" <program> <args>` or its own .vbs; `python task-land/_system/window-watch/window_lint.py` must list nothing under "bad" after any task change.

| Task | Cadence | Script | Purpose |
|---|---|---|---|
| TaskLand-GitSync | every 15 min + logon | `git-sync-hidden.vbs` -> `task-land/_system/git-sync.ps1` | step 0 robocopy /MIR of gtm-eng, triage, browser-extensions, quick-claude, claude-bar, hooks, AutoHotkey into `_system/laptop-tools/`; commit; merge origin/main; push; conflict parks on `conflict-laptop` |
| DA-VaultSync | every 10 min (no logon trigger) | `vault-git-sync-hidden.vbs` -> `_system/vault-git-sync.ps1` | commit-first, pull, push of vault_kb, medtech-brain, the memory repo (soda-brain), `.medtech-crm` (coattio); also tars the memory folder to the box over ssh |
| DailySync-Watchdog | every 5 min | `start-watcher.ps1` -> `watch-daily.ps1` + `vault-bridge-sync.ps1` | keeps the daily-page watcher alive (absorbs page edits about 60 s after typing stops, re-renders, runs `crm-bridge.ps1` and `pipeline.py sync` at the end of each pass, triggers git-sync on change); `vault-bridge-sync.ps1` appends the once-a-day cross-vault digest to `context.md` |
| CRM-Outdated | every 10 min (from 2026-10-04 05:00) | `run-hidden.vbs` -> `node .medtech-crm/crm-outdated.js` | the CRM hygiene worker (CRM H51): retires / rewrites / closes stale review items, paths A (events through the brain match) and B (per-person re-check), `review/updates.jsonl`, Updates page in review mode; see LOOPS.md section 1 |
| Coattio-Watchdog | every 5 min + logon + resume-from-sleep (Power-Troubleshooter 1, Kernel-Power 107) | `.medtech-crm/coattio-serve.ps1` | starts :4124 and :4137 only if their port is down |
| DesignMirror-Server | logon, 1-min keep-alive | `pythonw tundra-design/sync/dsync.py serve` | design-sync server :4190; commits, pulls, pushes tundra-design |
| DA-HubForward | unverified (keep-alive) | `~/.claude/approval-hub/forward-to-box.js` | laptop :4180 -> box :4180 |
| DA-WindowWatch | continuous (`pythonw`, 4 samples a second) | `task-land/_system/window-watch/window_watch.py` | records every new console window with its opener in `window-watch/windows.jsonl` |
| GTM-Agent | every 10 min | `gtm-agent-hidden.vbs` -> `gtm-eng/agent/gtm_agent.py` | the system agent: checks campaigns, CRM Today, hub cards, servers, tasks, Gmail, LinkedIn, sync, console windows; whitelist fixes; updates at 09:00 and 18:15 Rome; heartbeat pushed to the box |
| GTM-Campaign-Tick | every 10 min | `gtm-eng/campaign.py` tick (via .vbs since 2026-09-25) | sends campaign steps inside 08:00-17:00 PT from the tundra account; cap `EMAIL_HARD` 20/day |
| DailyCampaign-Fire | 16:55 Rome | `daily-campaign-hidden.vbs` -> `gtm-eng/daily-campaign/fire.py` | first 10 of `boards/daily-<today>` -> commit -> `campaign.py plan` -> update card -> research for the next board |
| DailyCampaign-Research | every 20 min (17:00-24:00 for the next day, 08:00-16:20 for today) | `daily-campaign/supervise.py` | one round of 2 hidden Sonnet workers x 80 min while the day is short of 30 people, then `review.py`, then the board |
| DailyCampaign-Postmortem | monthly (card on the 1st) | `daily-campaign/postmortem.py` | proposed-vs-sent post-mortem card |
| DailyCampaign-AB-Reminder | unverified | unverified | A/B reminder; was rewrapped by `window_lint.py --fix` on 2026-09-28 |
| US-Campaign-Daily | unverified | unverified | the 114-person US wave (`us-campaign-emails`); rewrapped 2026-09-28 |
| DA-FeedbackWorker | unverified | `gtm-eng/agent/feedback_worker.py` | lifts system sentences from review fields into `_system/gtm-agent/system-feedback.jsonl` |
| DA-InboundAsks | unverified | `gtm-eng/agent/inbound_asks.py` | reads WhatsApp, LinkedIn and events ledger for asks owed to people |
| DA-MeetingLoop | unverified | `gtm-eng/agent/meeting_loop.py` | reads Notion meetings, drives the booked-call loop |
| LinkedIn-Poll | unverified | `~/.claude/linkedin-poll/poll.py` | writes `G:/My Drive/DA/linkedin-store.jsonl` (Langfuse-traced) |
| SentCorpus-Harvest | unverified | `~/.claude/sent-corpus/harvest.js` | harvests Sent mail into `corpus.jsonl` |
| Notion-MeetingFiler | unverified | `~/.claude/scripts/notion-meeting-filer.ps1` | files meetings into Notion through the MCP |
| Trippy-RailLane, Trippy-Requests-Watch | intervals (unverified) | .vbs wrappers | trippy rail lane and request watcher; `rail_lane.py` posts hub cards |
| Archive-Screenshots, Curriculum-Daily-Crawl, Curriculum-Weekly-Crawl | unverified | unverified | found opening console windows on 2026-09-28, rewrapped |
| Push-Lane-Watchdog, Approval-Hub-Watchdog, Voice-Lane-Watch | historical (August 2026) | `approval-hub/push-watchdog.ps1`, `start-hub.ps1`, `watch-voice.ps1` | the laptop hub and popup lane; laptop and phone popups were deactivated (Telegram only) and the live hub moved to the box; whether these tasks still exist is unverified |

Laptop WA tasks: Disabled (the laptop wa-daemon store is kept but the box daemon is the live one).

## 5. Cron on the box (user `da`)

Crontab header sets `TELEGRAM_STATE_DIR=/home/da/.claude/channels/telegram-null` so no cron-spawned `claude` can steal the Telegram poller. Root crontab is not readable without a password (unverified). `/etc/cron.d` is stock.

| Schedule | Script | Purpose |
|---|---|---|
| `*/5` | `~/.local/bin/box-sessions.sh` | keeps two tmux Claude Code sessions alive: `savior` (Telegram plugin + Remote Control, the only bot poller) and `workbench` |
| `@reboot` + `*/5` | `~/.local/bin/trippy-supervise.sh` | keeps trippy `travel-search/app/server.js` on :4126 (buggy: see FINDINGS 1) |
| `*/5` | `task-land/_system/vps/repo-sync.sh /home/da/travel-search` | commit-first, pull --rebase, push |
| `* * * * *` | `~/.local/bin/ship-wa-store.sh` | copies `wa-daemon/message-store.jsonl` to `~/gdrive/DA/wa-store.jsonl` (the laptop CRM reads WhatsApp from Drive) |
| `*/2` | `coattio/coattio-sync.sh` | fetch + ff-only merge of coattio; on HEAD move `start-box.sh --restart`, else ensure the two coattio servers are up |
| `*/5` | `task-land/_system/drafts/reconcile.py` | draft lane: Gmail drafts vs sidecars vs queue vs hub cards; never sends |
| `*/30` | `triage/contacts_sync.py sync --account alesoda2002` | Google Contacts -> `_system/contacts-inbox.jsonl` -> one hub card per batch -> coattio intake :4137 (failing since 2026-09-21, FINDINGS 2) |
| `0 23` | `triage/eod_sweep.py` | 23:00 digest card + calendar event (card post failing, FINDINGS 4) |
| `@reboot` + `*/5` | `~/.local/bin/hub-review-supervise.sh` | keeps hub-review :4142 up |
| `47 22` | `~/.local/bin/presweep-watchdog.sh` | Telegram message if the savior's 22:12 pre-sweep stamp is missing |
| `0 9 21 9 *` | `travel-search/refresh_milan_paris.py` | one-off, still in crontab (fires again 2027-09-21) |
| `* * * * *` | `~/.local/bin/tg-lane-watchdog.sh` | dead Telegram lane detector |
| `58 22` | `task-land/_system/post_system_check.py` | posts the newest weekly `system-check-<n>.md` as a hub update |
| `*/10` | `task-land/_system/hub_outdated.py` | closes hub cards made moot by later events; holds everything when a Gmail account could not be read (`DEGRADATO`) |
| `*/10` | `task-land/_system/gtm-agent/box_watch.py` | laptop GTM-agent heartbeat watch; one card a day if the laptop is silent 60 min in business hours with sends due |
| `*/10` | `task-land/_system/gtm-agent/box_linkedin_watch.py` | LinkedIn session safety net |
| `* * * * *` | `task-land/_system/vps/savior_prompt_watch.py` | one hub card when a claude permission prompt sits unanswered in the savior pane |

## 6. systemd on the box

Unit sources live in `task-land/_system/vps/*.service|timer`; `units.list` is the install list.

| Unit | Cadence | What it runs | State on 2026-10-01 |
|---|---|---|---|
| `da-hub.service` | always | `node server.js` in `/home/da/approval-hub`, :4180, env points at wa-daemon send, sodanotif push, triage python and gmail, slack | running |
| `da-wa.service` | always | `node daemon.js` in `/home/da/wa-daemon` (Baileys WhatsApp, send API :4119) | running 19 d |
| `da-sodanotif.service` | always | `node daemon.js` in `/home/da/sodanotif` (WA tap + LinkedIn, Gmail, Slack stores -> classify -> Telegram card) | running 19 d |
| `da-tg-bridge.service` | always | `node bot.js` in `/home/da/tg-bridge` (second bot, phone -> `claude -p`) | running 19 d |
| `da-gdrive.service` | always | rclone mount `cdtm:` at `/home/da/gdrive` (CDTM My Drive) | running 32 d |
| `da-tundra-drive.service` | always | rclone mount `tundra:` at `/home/da/tundra-drive` (Tundra Shared Drive) | running 38 d |
| `da-sync.timer` | 60 s | `_system/vps/git-sync.sh` (task-land: step 0 rsync of box tools into `_system/box-tools/`, commit, merge origin/main, push; conflict parks on `conflict-vps`) | ok |
| `da-repo-sync@vault_kb.timer`, `da-repo-sync@medtech-brain.timer`, `da-repo-sync@soda-brain.timer` | 5 min | `_system/vps/repo-sync.sh <repo>` | ok (the inventory, taken before the 18:55 rename, still lists the third instance as `claude-memory`) |
| `da-health.timer` | 5 min | `health-vps.sh` -> `_system/health-vps.json` (synced to the laptop, which raises a "VPS DOWN" calendar event when it goes stale) | ok |
| `da-alert.timer` | 5 min | `alert-bridge.sh` (the laptop's synced `_system/health.json` -> Telegram) | ok |
| `da-voice.timer` | 5 min | `voice-longform-vps.py` (long recordings on the Drive mount -> faster-whisper -> safe-word routing) | ok |
| `da-gmail-poll.timer`, `da-slack-poll.timer` | 60 s | `sodanotif/pollers/*_poll.py` | ok |
| `da-brain.service` | always | PLANNED, see section 9 | not built |
| `da-brain-index.timer` | PLANNED cadence unverified | PLANNED, see section 9 | not built |

`units.list` names 13 units and does not include `da-sync.timer` or `da-health.timer`, both of which the inventory saw running (FINDINGS, cross-source).

tmux sessions (not units): `savior` since 2026-09-19 (`claude --name "savior box (19-09)" --remote-control --channels plugin:telegram`, child `bun ... telegram server.ts`; never kill or respawn it, only Alessandro runs `restore-savior`), `workbench` since 2026-09-08 (`claude --remote-control`), `coattio` (the two CRM servers with `COATTIO_BOX=1`, `TELEGRAM_STATE_DIR=telegram-null`, `CLAUDE_BIN=/usr/bin/claude`, `CRM_GMAIL=triage/gmail.py`). Unsupervised processes whose parent is an orphaned claude shell (a reboot drops them): trippy :4126 (cron tries), hub-review :4142 (cron), research-page :4143, :4144, :4145 (nothing).

## 7. Sync mechanisms

| What | Laptop side | Box side | Conflict handling |
|---|---|---|---|
| task-land (`alesod23/task-land`) | `TaskLand-GitSync` every 15 min + logon, plus the daily watcher on change: step 0 mirrors seven tool folders into `_system/laptop-tools/` (robocopy /MIR, excludes tokens/, credentials.json, *token*.json, *.env, whatsapp-sessions, venv, node_modules, pids, logs, .qc-* state); commit; `git merge origin/main`; push | `da-sync.timer` every 60 s: step 0 rsyncs `approval-hub`, `sodanotif`, `triage`, `~/.claude/skills` into `_system/box-tools/` (same exclusions plus stores/, state/, *.jsonl, state.json, push.env, pids; skills added 2026-10-01); commit; merge; push | failed merge parks HEAD on `conflict-laptop` / `conflict-vps`, writes `GIT-SYNC-CONFLICT-*.md` at the repo root, exits non-zero every tick until resolved. `.gitattributes` has `*.jsonl merge=union` (append-only logs merge by line); `_system/drafts/resolve_sidecar_conflicts.py` runs after a failed merge and lets the more advanced sidecar win (finished > edited > registered > stub, tie = longer). Both scripts switched from `pull --rebase --autostash` to merge on 2026-09-28 after three multi-day parks (10 to 17 Sep box, 25 to 27 Sep laptop, 28 Sep box). Manual recipe: hold the lock (`flock /tmp/da-git-sync.lock` on the box, mutex `Global\TaskLandGitSync` on the laptop), `git merge --no-commit origin/main`, jsonl = union by ts, mirrored tools = the owning machine, sidecars = the writer, delete the advisory, commit, push, delete the conflict branch |
| soda-brain (`alesod23/soda-brain`, was `claude-memory` until 2026-10-01 18:55) | `DA-VaultSync` every 10 min, commit-first, pull, push; `~/.claude/projects/C--Users-Alessandro/memory` is a junction to `C:/Users/Alessandro/soda-brain/memory` | `da-repo-sync@soda-brain.timer` every 5 min; `/home/da/soda-brain`, `~/.claude/memory` -> `/home/da/soda-brain/memory` (symlink), `~/.claude/projects/-home-da/memory` -> `~/.claude/memory` | two-way; a memory saved on one side is on the other within 5 to 10 min; the losing side parks on `conflict-vps-soda-brain` / `conflict-laptop-soda-brain` with a `GIT-SYNC-CONFLICT-*.md` advisory; resolve with `git pull --rebase origin main`, the next sync clears it |
| vault_kb, medtech-brain | `DA-VaultSync` every 10 min | `da-repo-sync@<repo>.timer` every 5 min (`repo-sync.sh`: commit-first, pull --rebase, push) | same parking pattern; conflict branch names for these two repos are not stated in the sources (unverified) |
| coattio (`alesod23/coattio`) | laptop is the writer; `DA-VaultSync` commits and pushes `.medtech-crm` every 10 min | cron `coattio-sync.sh` every 2 min: fetch + `merge --ff-only` with a read-only deploy key; on HEAD move `start-box.sh --restart` | pull-only, so a conflict is impossible unless the box clone is dirty; it IS dirty (`start-box.sh`, FINDINGS 9) |
| crm.json (data, gitignored) | the only writer is `crm-app/server.js` on the laptop | `crm-app/peer.js` pulls the laptop's data into the box copy | the box copy is a read replica; two `crm.conflict-box-*.json` files on the laptop are leftovers nobody reads |
| travel-search (`alesod23/travel-search`) | none (hand commits; 23 dirty files under `results/us-tour-2026-10/` on 2026-10-01) | cron `repo-sync.sh` every 5 min | box-only automation |
| tundra-design (`alesod23/tundra-design`) | `DesignMirror-Server` (commits every extension snapshot, pull, push) | none (cloned 2026-09-30, moves only by hand) | laptop-only automation |
| Skills and commands | the laptop is the writer; an "hourly tar push" ships `~/.claude/skills` and `commands` to the box (CLAUDE-box.md); the laptop repo inventory places a memory tar in `DA-VaultSync` (10 min) instead | box `~/.claude/skills` (28 entries) is rsync-mirrored into `_system/box-tools/skills/` since 2026-10-01 | which task performs the hourly skills push is not named in the sources (unverified) |
| WhatsApp store | reads `G:/My Drive/DA/wa-store.jsonl` (Google Drive desktop client, `CRM_WA_SHIP`) | `ship-wa-store.sh` every minute copies `wa-daemon/message-store.jsonl` to `~/gdrive/DA/wa-store.jsonl` | one-way box -> Drive -> laptop |
| LinkedIn store | `linkedin-poll/poll.py` writes `G:/My Drive/DA/linkedin-store.jsonl` | sodanotif reads `~/gdrive/DA/linkedin-store.jsonl` | one-way laptop -> Drive -> box |
| Health | `_system/health.json` (tracked in task-land; the cloud and `da-alert.timer` read it) | `_system/health-vps.json` written every 5 min by `da-health.timer` | the laptop's dead-man switch raises a "DA SYSTEM: VPS DOWN" calendar event when `health-vps.json` is stale, which is also what a parked sync looks like |
| GTM-agent heartbeat | pushed over ssh by `gtm_agent.py` | `~/.local/state/gtm-agent/heartbeat.json`, read by `box_watch.py` every 10 min | one-way laptop -> box |

## 8. What runs unsupervised, and where the logs are

Unsupervised (no unit, no watchdog, a reboot or a closed shell kills it): box research-page servers :4143, :4144, :4145; the box `gtm-eng` copy (nothing starts :4141). Cron-supervised only (restart within 5 min, no crash detection between ticks): trippy :4126, hub-review :4142. Everything else on the box is a systemd unit with `Restart=always` or a timer; everything on the laptop is a schtasks task with a watchdog, except travel-search commits (by hand).

Logs:

| Machine | Where | What |
|---|---|---|
| Box | `~/.local/state/` | every cron and timer log (one dir or file per job), including `hub-outdated/run.log` (grep `DEGRADATO`), `gtm-agent/heartbeat.json` |
| Box | `travel-search/trippy.log` | trippy supervise noise (5 MB of EADDRINUSE on 2026-10-01) |
| Box | `sodanotif/notification-log.jsonl` | every card sodanotif and the hub ever pushed |
| Box | `task-land/_system/TELEGRAM-BRIDGE-LOG.md` | the Telegram lane fix log (read before touching Telegram, append after every fix) |
| Box | `task-land/_system/vps/git-sync.log` (name as cited in memory: "git-sync.log 18:44") | sync ticks, "MERGED with sidecar auto-resolve" |
| Laptop | `task-land/_system/daily-sync.log` | every absorb decision: `directive:`, `replace:`, `datebullet:`, `retitle:`, `renamed:`, `mirror tick held:`, `SAFETY:`, classifier confidence |
| Laptop | `task-land/_system/crm-bridge.log`, `surface-sweep.log`, `git-sync.log` | owner flip, capacity-gated surfacing, laptop sync |
| Laptop | `task-land/_system/window-watch/windows.jsonl` | every console window, with the opener; read it first when he reports a window |
| Laptop | `gtm-eng/agent/runs.jsonl` (299 lines), `incidents.jsonl` (356) | the system agent's runs and incidents; `python gtm_agent.py status|incidents|missed` |
| Laptop | `gtm-eng/daily-campaign/runs/` | campaign runs |
| Laptop | `~/.claude/linkedin-poll` `reap.log` (path as cited) | LinkedIn launcher reaper |
| Both | `task-land/_system/decisions.jsonl`, `rule-hits.jsonl` | durable records of hub verdicts and rule hits (synced, union-merged) |

## 9. PLANNED tonight: `da-brain` and `da-brain-index.timer`

Not built as of the inventories; described here so the map does not go stale on the first evening.

- `da-brain.service`: a Python service on `100.85.52.84:4150` (Tailscale address, so laptop and phone reach it, the public internet does not). It owns a Postgres database `soda` on the box with two schemas: `brain` (the index over `soda-brain/memory/` and `system/`, so a session can search facts instead of reading 360 files) and `crm` (CRM document versions and rows, written through the service so the box stops being a read replica of a laptop JSON file). Two doors: MCP (for Claude Code sessions on either machine) and HTTP (for scripts). Unit source goes in `task-land/_system/vps/` and the name in `units.list` like every other unit.
- `da-brain-index.timer`: rebuilds the `brain` schema from the repo on a cadence (cadence not yet decided); the repo stays the source of truth, the index is a copy.
- Port 4150 is free on both machines today.

## Known gaps and open questions

- Hosting provider: Contabo (CLAUDE-box.md) or Hetzner (VPS-SETUP.md)? The measured 96 GB disk matches neither document.
- `units.list` omits `da-sync.timer` and `da-health.timer`; either they were installed by hand or the list is incomplete.
- The task that performs the hourly skills and commands tar push to the box is not named anywhere; CLAUDE-box.md says hourly, the laptop inventory folds a memory tar into `DA-VaultSync` (10 min).
- Cadences of DA-HubForward, DA-FeedbackWorker, DA-InboundAsks, DA-MeetingLoop, LinkedIn-Poll, SentCorpus-Harvest, Notion-MeetingFiler, DailyCampaign-AB-Reminder, US-Campaign-Daily, Archive-Screenshots, Curriculum-* are not in the sources; `schtasks /query` would settle them.
- Whether Push-Lane-Watchdog, Approval-Hub-Watchdog and Voice-Lane-Watch still exist after the hub moved to the box (the laptop popups were deactivated).
- Root crontab on the box is unknown (sudo needs a password).
- Bind addresses of :4143 to :4145 were not recorded.
- Conflict branch names used by `repo-sync.sh` for vault_kb and medtech-brain.
- The box `gtm-eng` dir: is it still needed now that :4141 is laptop-only?
- `da-brain-index.timer` cadence and whether the `crm` schema becomes the writer (replacing `crm.json`) or a versioned copy first.
