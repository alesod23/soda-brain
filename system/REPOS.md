# REPOS: every repository of the system and the code that is not in one

Seven GitHub repositories under the user `alesod23` carry the system between the laptop and the box: task-land (the task system and, through its two mirror folders, the backup of every tool), soda-brain (the memory and this map; it was `claude-memory` until 2026-10-01 18:55), coattio (the CRM code, laptop writes, box pulls), vault_kb and medtech-brain (two Obsidian wikis), tundra-design (finished Claude Design work shared with a co-founder) and travel-search (trippy). All are private. A second group of code lives outside any repo: on the laptop gtm-eng, triage and the browser extension are backed only by their mirror inside task-land, sim/harness is a local git with no remote; on the box nine folders have only `.bak-*` files as rollback. Every clone on the box authenticates with its own deploy key through an ssh host alias; the laptop uses `gh` logged in as `alesod23`.

Last verified: 2026-10-01 (from the inventories of that day); 2026-10-04 19:15: `granola-auto` retired

Conventions: "conflict branch" is where a sync script parks HEAD when a merge fails (`GIT-SYNC-CONFLICT-*.md` appears at the repo root and the script exits non-zero every tick until someone resolves it). "Personal data carried" says what third-party names, emails or message texts are tracked.

## 1. The system's repositories

### task-land (`alesod23/task-land`, PRIVATE)

| | |
|---|---|
| Laptop | `C:/Users/Alessandro/task-land` (Obsidian vault, 826 md; main; 39,393 commits; `.git` 90 MB, 42 packs, 6,596 loose objects, never gc'd) |
| Box | `/home/da/task-land` (main) |
| Tracked | 2,214 to 2,215 files: `Tasks/`, `Daily/`, `Events/`, `Habits/`, `context.md`, `agent-notes.md`, `_system/` (scripts, contracts, drafts sidecars, decisions.jsonl, rule-hits.jsonl, health.json, health-vps.json, vps units, hints, handoffs, workplans), `_system/laptop-tools/` 948 files (gtm-eng 719, quick-claude 117, hooks 52, triage 26, browser-extensions 11, skills 3, claude-bar, autohotkey), `_system/box-tools/` 357 files (approval-hub `state.json` 208 KB + `hub-rules.json`, sodanotif stores, triage, skills 283) |
| Deliberately ignored | tokens/, credentials.json, *token*.json, *.env, whatsapp-sessions, venv, node_modules, pids, logs, *.bak-*, .qc-* state (mirror exclusions, repeated in `.gitignore` as a second guard); on the box side also stores/, state/, *.jsonl, state.json, push.env |
| Laptop sync | `TaskLand-GitSync` every 15 min + logon (`_system/git-sync.ps1`: step 0 robocopy mirrors, commit (never with MERGE_HEAD or conflict markers, since 5 Oct 2026; `*.bak*` and `*.md.orig` backups are not scanned), `git merge origin/main`, retried once after committing late writes when git refuses with "would be overwritten by merge", since 10 Oct 2026, push) plus the daily watcher, which triggers a sync on change |
| Box sync | `da-sync.timer` every 60 s (`_system/vps/git-sync.sh`: step 0 rsync mirrors, commit, merge, push) |
| Conflict branches | `conflict-laptop` / `conflict-vps`; `.gitattributes` `*.jsonl merge=union`; `_system/drafts/resolve_sidecar_conflicts.py` after a failed merge; `_system/vps/sync-guards.sh` |
| Personal data carried | `_system/contacts-inbox.jsonl`, `_system/box-tools/approval-hub/state.json` (card texts), `_system/decisions.jsonl`, draft sidecars with full email text, the gtm-eng mirror's `boards/*/campaign/plan.json` and `research-people.json`, sodanotif gmail/slack state, 253 task files named after people, `box-tools/sodanotif/bds2023.pdf` 16 MB |
| Notes | The ONE shared repo by his ruling (2026-09-10: no new repos, reuse task-land). The box's `~/.claude/CLAUDE.md` is a symlink to `_system/vps/CLAUDE-box.md` inside it. Parked three times (10 to 17 Sep, 25 to 27 Sep, 28 Sep) before the merge-based sync of 2026-09-28 |

### soda-brain (`alesod23/soda-brain`, PRIVATE; was `alesod23/claude-memory` until 2026-10-01 18:55)

| | |
|---|---|
| Laptop | `C:/Users/Alessandro/soda-brain` (main, 224 commits before the rename). Claude's memory path `C:/Users/Alessandro/.claude/projects/C--Users-Alessandro/memory` is a directory junction to `C:/Users/Alessandro/soda-brain/memory` (verified 2026-10-01: reparse tag 0xa0000003, target as stated) |
| Box | `/home/da/soda-brain`; `~/.claude/memory` -> `/home/da/soda-brain/memory` (symlink); `~/.claude/projects/-home-da/memory` -> `~/.claude/memory`. The box inventory (taken 18:13-18:20, before the rename) still shows `/home/da/claude-memory` with remote `alesod23/claude-memory` and timer `da-repo-sync@claude-memory.timer`; `units.list` and `CLAUDE-box.md` carry the new name |
| Tracked | 360 files: `memory/*.md` (the facts: feedback 176, reference 136, project 29, user 2, none 14; `MEMORY.md` 13 KB + sub-indexes; `_attic/` 6), `system/*.md` (this map: MACHINES, DATA-MAP, REPOS, ACCOUNTS, FINDINGS; LOOPS named in CLAUDE-box.md, not yet written). `.gitignore` is empty. The rename commit message says "340 facts"; the inventories count 360 files |
| Deliberately ignored | nothing (by rule: no person records, no secrets, no runtime data may enter this repo) |
| Laptop sync | `DA-VaultSync` every 10 min (`_system/vault-git-sync.ps1`: commit-first, pull, push; no logon trigger) |
| Box sync | `da-repo-sync@soda-brain.timer` every 5 min (`repo-sync.sh`) |
| Conflict branches | `conflict-laptop-soda-brain` / `conflict-vps-soda-brain`; resolve with `git pull --rebase origin main`, the next sync clears it; never commit or push by hand on the box |
| Personal data carried | memory notes name people (feedback and reference files quote him and name counterparts) |
| Notes | Two-way: both machines write. Skills and commands are NOT in it (they travel by the laptop's tar push) |

### coattio (`alesod23/coattio`, PRIVATE)

| | |
|---|---|
| Laptop | `C:/Users/Alessandro/.medtech-crm` (main, clean, 96 commits) |
| Box | `/home/da/coattio` (main); `~/.medtech-crm` -> this dir; 1 dirty file `start-box.sh` (the `TELEGRAM_STATE_DIR` guard, uncommitted) |
| Tracked | 139 files: `crm-app/` (server.js, model.js, monitor.js, peer.js, observer.js, reader.js, review-api.js, drawer-api, ask-api, events-api, handoff-api, owed.js, today-count.js, sources.js), `intake-server.js`, `ingest-intake.js`, `coattio-notion-sync.js`, ai-draft, `hidden-claude.js`, `coattio-serve.ps1`, `start-box.sh`, `coattio-sync.sh`, `PORTABLE.md`, 8 workplans; data tracked: `review/<person>.json` dossiers (46 or 51), `hospital-check/hospitals.json` 164 KB, `no-email-items.json`, two message texts |
| Deliberately ignored | `crm.json` 5.7 MB, `backups/`, `*.jsonl` (events-ledger, intake, enrichments, ai-drafts, sent-log), `*-state.json`, `crm.conflict-box-*.json`, `hospital-check/` inputs, `enrich-queue/`, `verify-shots/` |
| Laptop sync | `DA-VaultSync` every 10 min (the laptop is the writer) |
| Box sync | cron `coattio-sync.sh` every 2 min: fetch + `merge --ff-only` with a READ-ONLY deploy key; on HEAD move `start-box.sh --restart`, otherwise ensure :4124 and :4137 are up |
| Conflict branches | none (pull-only); a laptop commit touching `start-box.sh` will make the ff-only merge fail on the box until the local edit is committed or reset (FINDINGS 9) |
| Personal data carried | the review dossiers, the hospital list, two message texts; `crm.json` itself is NOT on GitHub |
| Notes | the CRM data moves box-ward by `peer.js` pull, not by git |

### vault_kb (`alesod23/vault_kb`, PRIVATE)

| | |
|---|---|
| Laptop | `C:/Users/Alessandro/vault_kb` (main, clean; 148 md) |
| Box | `/home/da/vault_kb` (main) |
| Tracked | 168 files: `Raw/ Sources/ Self/ Projects/ People/ Orgs/ Topics/`, `index.md`, `catalog.jsonl`, `log.md`, `project-registry.md`, `CLAUDE.md` (the contract), `_meta/UNDERSTANDING OUR KB SYSTEMS (READ ME).md` |
| Deliberately ignored | none stated |
| Laptop sync | `DA-VaultSync` every 10 min |
| Box sync | `da-repo-sync@vault_kb.timer` every 5 min |
| Conflict branches | not stated in the sources (unverified; the same `repo-sync.sh` family as soda-brain) |
| Personal data carried | `People/` pages, two thesis PDFs in `Raw/` |

### medtech-brain (`alesod23/medtech-brain`, PRIVATE)

| | |
|---|---|
| Laptop | `C:/Users/Alessandro/medtech-brain` (main, clean; 173 md) |
| Box | `/home/da/medtech-brain` (main) |
| Tracked | 229 files: `Raw/ Sources/ Company/ Accounts/ Market/ People/ Topics/ _system/ Clippings/`, `CLAUDE.md`, `_system/OUTREACH-SYSTEM.md` |
| Deliberately ignored | none stated |
| Laptop sync | `DA-VaultSync` every 10 min |
| Box sync | `da-repo-sync@medtech-brain.timer` every 5 min |
| Conflict branches | not stated (unverified) |
| Personal data carried | `Accounts/`, `People/`, call notes, the AIIC brochure (4.3 MB) |
| Notes | task-land is deliberately NOT bridged to it (`bridge: false`, `task_join: false`); Tundra facts found while working tasks go in through `/kb-ingest` |

### tundra-design (`alesod23/tundra-design`, PRIVATE)

| | |
|---|---|
| Laptop | `C:/Users/Alessandro/tundra-design` (master; 2 untracked; 1,280 untracked files / 44 MB under `live/caleb/website-recreation/uploads/`) |
| Box | `/home/da/tundra-design` (master, 489 tracked; cloned 2026-09-30; moves only by hand) |
| Tracked | 489 to 490 files: the shared library of finished Claude Design work (two contributors), `sync/dsync.py` (the extension mirror and :4190 server), `sync/.versions-ale.json` (local state) |
| Deliberately ignored | the `uploads/` tree (untracked, not stated whether ignored) |
| Laptop sync | `DesignMirror-Server` (logon, 1-min keep-alive; `pythonw sync/dsync.py serve` commits every extension snapshot, pulls, pushes) |
| Box sync | NONE |
| Conflict branches | n/a |
| Personal data carried | none |
| Notes | a deck that went out in a mail is finished work and lives here; read it from the repo |

### travel-search (`alesod23/travel-search`, PRIVATE)

| | |
|---|---|
| Laptop | `C:/Users/Alessandro/.claude/travel-search/v2` (master; 23 dirty files under `results/us-tour-2026-10/` on 2026-10-01). The parent `.claude/travel-search/` is 8.5 GB of browser profiles, outside the repo |
| Box | `/home/da/travel-search` (master, 353 tracked): trippy-v2, engines gflights, omio, bahn, italo, momondo, `app/` webapp on :4126 |
| Tracked | 353 files |
| Deliberately ignored | browser profiles (unverified), results partly uncommitted |
| Laptop sync | NONE (hand commits) |
| Box sync | cron `repo-sync.sh /home/da/travel-search` every 5 min |
| Conflict branches | as `repo-sync.sh` (unverified) |
| Personal data carried | trip boards with travellers' names |
| Notes | the Sep 6-25 stall: the box committed filenames with ":" that Windows cannot check out; fixed with `guard_winnames` on the box; JSON conflicts there resolve as union by id |

## 2. Code that is in no repository

### Laptop

| Folder | What | Backup | Personal data |
|---|---|---|---|
| `C:/Users/Alessandro/gtm-eng` | the real GTM engine: `board-server.js` (:4141), `campaign.py`, `commit-to-contacts.js`, `run-commit.py`, `open-board.ps1`, `close-board.ps1`, `daily-campaign/`, `agent/`, `boards/`, `signatures/`, `DESIGN-SYSTEM.md`, 5 workplans | mirror `task-land/_system/laptop-tools/gtm-eng` (719 files, 15 min) | yes (boards, pool, message bodies) |
| `C:/Users/Alessandro/triage` | `gmail.py`, `gcal.py`, `drive.py`, `contacts_sync.py`, `eod_sweep.py`, `state.json`, tokens | mirror `laptop-tools/triage` (26 files, tokens excluded); the box has its own copy kept identical by hand (scp + `.bak-<date>`) | state only |
| `C:/Users/Alessandro/browser-extensions/gtm-tabs` | the Chrome extension that owns the GTM tab group (unpacked; reload by hand at `chrome://extensions`) | mirror `laptop-tools/browser-extensions` (11 files) | no |
| `C:/Users/Alessandro/.claude/quick-claude`, `claude-bar`, `hooks`, `OneDrive/Documents/AutoHotkey` | hotkey tools, status bar, harness hooks (incl. `langfuse_hook.py`, `kb-systems-drift-guard.sh`), AHK scripts | mirrors under `laptop-tools/` | no |
| `C:/Users/Alessandro/.claude/skills` (25 dirs, 281 files), `commands/`, `scripts/` (50), `loops/`, `CLAUDE.md`, `settings*.json`, `.mcp.json`, `keybindings.json` | the harness configuration | skills: the box copy is mirrored into `box-tools/skills` since 2026-10-01 (283 files) and the laptop is its writer, so the content is backed by that route; `laptop-tools/skills` has 3 files (compiled crm, drafting, hub). Everything else: no backup | no |
| `C:/Users/Alessandro/.claude/approval-hub` | `forward-to-box.js`, `forward-hub-review.js`, a dead 2026-09-01 `server.js`, stale `state.json` | none | stale card texts |
| `C:/Users/Alessandro/.claude/tg-bridge`, `linkedin-poll`, `linkedin-accept-bot`, `sent-corpus`, `wa-daemon`, `voice-lane`, `audio-notes`, `sodanotif` (old), `snm-receiver`, `granola-auto` (retired 4 Oct 2026), `jobs`, `curriculum-server` | small tools and their state | none (curriculum-server's code is on GitHub, see below) | some (sent corpus, WA store, tg history) |
| `C:/Users/Alessandro/sim/harness` | the simulation harness (git, master, 30 commits, 130 tracked, NO remote) | none, only copy on disk | sandbox copies of the email ledger, fake tokens |
| `C:/Users/Alessandro/07-thesis-kb`, `mpd-kb`, `self-reflection-wiki`, `_kb-archive`, `lobbly-kb`, `thesis-system` | vaults and the thesis workspace | OneDrive July copy for 07-thesis-kb and self-reflection-wiki (June); mpd-kb none | yes |
| `C:/Users/Alessandro/OneDrive - HEC Paris/_LAPTOP-BACKUP` | plain copies of task-land, vault_kb, 07-thesis-kb, self-reflection-wiki, 44,086 files, newest 2026-07-25 | is itself a (stale) backup | yes, including July secrets |

### Box

| Folder | What | Backup |
|---|---|---|
| `/home/da/approval-hub` | the live hub `server.js`, `state.json`, `hub-rules.json`, `last-rejected.json` | rsync mirror `task-land/_system/box-tools/approval-hub` every minute |
| `/home/da/sodanotif` | `daemon.js`, `pollers/`, `push.js`, `routing-prompt.md`, `stores/`, `notification-log.jsonl`, `push.env` | mirror `box-tools/sodanotif` (stores and secrets excluded by rule; see DATA-MAP gap) |
| `/home/da/triage` | box copy of the triage tools + `venv/` + tokens | mirror `box-tools/triage` (tokens excluded) |
| `/home/da/.claude/skills` (28), `commands/` (72) | pushed from the laptop | mirror `box-tools/skills` since 2026-10-01 |
| `/home/da/hub-review` | phone review page `server.js` (:4142), `notify.py` (Telethon, sends as Alessandro), `queue.jsonl` | NONE (`.bak-*` only) |
| `/home/da/wa-daemon` | Baileys daemon, `send.js`, `search.js`, `message-store.jsonl`, `auth/` | NONE |
| `/home/da/tg-bridge` | second Telegram bot `bot.js`, `send-to-phone.js` | NONE |
| `/home/da/slack` | custom Slack app `slack.py`, `credentials.json`, `tokens/` | NONE |
| `/home/da/research-page` | event companion pages and their three servers | NONE |
| `/home/da/gtm-eng` | a copy of the GTM boards server taken out of the mirror; its server is dead | NONE (the laptop original is the truth) |
| `/home/da/tg-reply-resolver` | Telethon user session, `resolve.py` | NONE |
| `/home/da/voice-lane` | long-form voice lane state + venv | NONE |
| `/home/da/.local/bin/*` | `restore-savior`, `savior-resume.sh`, `savior-trigger-watch.sh`, `alarm.sh`, `tg-hub-ping.sh`, `gtm-board-server.sh`, `hub-review-server.sh`, `trippy-bootstrap.sh`, `box-sessions.sh`, `trippy-supervise.sh`, `ship-wa-store.sh`, `hub-review-supervise.sh`, `presweep-watchdog.sh`, `tg-lane-watchdog.sh`, `markless` | NONE |
| `/home/da/.claude/hooks` | `tg-reply-context.py`, `block-destructive.sh`, `scan-secrets-before-push.sh` | unverified (the laptop `hooks` mirror may or may not hold the same files) |

## 3. Other repositories on the laptop (not the system)

- His own, dormant: `C:/Users/Alessandro/.claude/curriculum-server` (`alesod23/curriculum-tracker`) and `C:/Users/Alessandro/triage-share-raphael` (`alesod23/terminal-inbox`, code only, no data). Both were PUBLIC on the morning of 2026-10-01, against the "always private" rule; both were made PRIVATE on 2026-10-01 (per the brief for this map).
- No remote: `Coding/tundratalents`, `f--k customer support` (11 dirty), `test vs/my-app`.
- Private, his: `dev/LobblyDemo` and `thesis-attempt/experiment/LobblyDemo` (CodeCLS), `thesis-attempt/repo-thesis` (Thesis_Understanding_Layer), `TundraPage` (Tundra-Health org).
- Third-party clones: `.claude/skills/fede` (floomhq/fede), `.tmp-audit/linkedin-mcp-server`, `dev/cdtm-gtm-engine` (gtmadviser), `dev/claude-setup` + `dev/moto` (the same floomhq repo twice), `thesis-attempt/experiment/OpenPatent`, `Learning tech/tech-presentation`, `OneDrive - HEC Paris/thesis-workspace` + `thesis-system/reference/research-assistant` (the same paablos8 repo twice), `.codex/.tmp/plugins`.

## 4. Authentication and visibility

- Laptop: `gh` logged in as `alesod23`; git pushes over https (`https://github.com/alesod23/soda-brain.git` is the remote form on the laptop).
- Box: one deploy key per repo, selected by an ssh host alias in `~/.ssh/config`; the coattio key is read-only; `~/.ssh/` also holds `id_ed25519`. A `scan-secrets-before-push.sh` hook runs on the box.
- All seven system repos are PRIVATE. The rule: `gh repo create --private`, public only after an audit for secrets.
- The brain repo must not inherit personal data from task-land or coattio: no person records, no card texts, no sidecars.

## 5. Mirrors since 2026-10-01

- Laptop skills: the brief states they are mirrored into task-land since 2026-10-01. The laptop stores inventory of the same day shows `_system/laptop-tools/skills` with 3 files and `_system/box-tools/skills` with 283 files, the latter rsynced from the box's `~/.claude/skills`, which is itself pushed from the laptop. The content is therefore in task-land, by the box route; whether `git-sync.ps1` step 0 now also mirrors `~/.claude/skills` directly is unverified.
- Box skills: rsynced into `_system/box-tools/skills/` by `git-sync.sh` step 0 (added 2026-10-01).

## Known gaps and open questions

- Memory count 340 (rename commit message) vs 360 (both inventories).
- `review/*.json` 46 vs 51.
- Conflict branch names for vault_kb, medtech-brain and travel-search under `repo-sync.sh`.
- Whether `git-sync.ps1` step 0 mirrors `~/.claude/skills` on the laptop directly.
- Whether the box `.claude/hooks` are covered by the laptop `hooks` mirror.
- `tundra-design` uploads tree: ignored or merely untracked.
- `thesis-system` and `lobbly-kb` git state.
- The `system/LOOPS.md` named in CLAUDE-box.md does not exist yet.
