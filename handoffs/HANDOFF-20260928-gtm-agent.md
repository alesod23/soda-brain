# HANDOFF 2026-09-28: the GTM agent

Written right before he compacts. The next turn gets his prompt verbatim (he pastes it). READ THIS FIRST, then the
memory files at the bottom. Two workplans hold the detail of what was built on 27-28 Sept:
`_system/WORKPLAN-20260927-todo-pipeline-and-hub.md` and `_system/WORKPLAN-20260927b-event-loop-and-feedback-shortcut.md`.

## 1. His ask (his words, 2026-09-28 12:15)
"i want a GTM agent, obsessed with ensuring a push in gtm is present everyday. whose full job is to ensure that my
campaigns, my followup suggestions, my approval items in my hub that are CURRENT and waiting for me too long. it will
ping me on tg twice per day with an update, but it will constantly run to ensure stuff works. in this case, it would
have noticed that the campaign wasnt going. would have launched an investigation. fixed like you did. ensure my tools
are usable. try to reconnect linkedin mcp by itself, not that i have to do it myself manually on crm repair button
(tho keep that manual safety)."

Read it as four duties:
1. **Campaigns are actually going.** Every committed campaign sends what is due, every day. Not going = investigate,
   fix forward when safe, tell him what happened.
2. **Follow-up suggestions are current.** CRM Today / review items: nothing due and unattended, no stale step.
3. **Hub items are current and not waiting too long.** Current = not outdated (hub_outdated.py does that part);
   waiting too long = he has not decided and it matters: that goes in the ping.
4. **Tools are usable.** LinkedIn MCP reconnects by itself; Gmail tokens, the servers, the sync, the box. The CRM's
   manual Repair button stays.
Two Telegram pings a day with the state (a hub card `kind:"update"`, never another bot), and a constant run in between.

## 2. The incident that prompted it (what the agent must catch by itself)
- `privati-nord` (Italy, 93 steps) STOPPED 2026-09-25 10:16 UTC: one LinkedIn invite (susanna-pavanelli-2) failed
  with "exception: Connection closed"; the engine stopped the whole board, emails included. A card went out
  ("campagna FERMATA"), nobody acted, three days silent. Found only because he asked on the 28th at 11:45.
- Released 2026-09-28 11:53 (`campaign.py resolve privati-nord susanna-pavanelli-2 release`). Verified 12:20: 7 sent
  since (5 emails, 2 invites), no failure, 1 overdue left, LinkedIn worked.
- FIXED the same day in `~/gtm-eng/campaign.py` (backup `.bak-channels-20260928`): a failure stops its CHANNEL
  (`P["stopped_channels"]["email"|"linkedin"]`), never the board; a transient error (connection closed, timeout,
  no result, exception, 502/503) is retried `RETRY_MAX` 3 times, `RETRY_MIN` 30 minutes apart, before the channel
  stops; `resolve ... release` clears the channel; the alert card now starts with a warning sign and says which
  channel is down and that the other continues. Dry tick ran clean after the change.
- FIXED in `task-land/_system/hub_outdated.py` (laptop + box): a failure ALERT (`ALERT` regex: FERMATA, FERMO,
  failed, not sent, broken, error, down, guasto, conflict) never ages out; it is judged like a decision.
- NOT fixed: `plan.json` of privati-nord still carries `dry: true` (a leftover of the 25 Sep `plan --dry` bug); the
  tick does not read that flag, it is only misleading.

## 3. What exists that the agent stands on (do not rebuild)
- **Engine:** `~/gtm-eng/campaign.py` (plan, tick, status <slug>, resolve <slug> <step> accepted|not_accepted|release|
  cancel|release-org), plans in `boards/<slug>/campaign/plan.json` (steps: id, person, type email|li_invite|li_dm,
  status scheduled|waiting|sent|failed|cancelled|needs_check|paused_org, `due_at`, `sent_at`, `result`), send ledger
  caps (email 20/day hard, li_invite 20/day), `campaign-tick.log`. Task `GTM-Campaign-Tick` every 10 min through a
  .vbs; `DailyCampaign-Research` (08:00 and every hour check), `-Fire` 16:55, `-Postmortem` 09:30, `US-Campaign-Daily`
  18:00. Daily board `boards/daily-<date>` (30 people, first 10 fire at 16:55 whether reviewed or not).
- **A ready-made probe:** `~/hubrev-work/campaign_today.py [date]` prints per campaign what is due today, what is
  still to send, the next `due_at`, and the flags (stopped, dry). On 2026-09-28: 49 emails + 18 invites due over 7
  campaigns. Move it into gtm-eng when building.
- **CRM:** servers 4124 (crm-app/server.js) and 4137 (intake-server.js), keeper `~/.medtech-crm/coattio-serve.ps1`
  (Coattio-Watchdog, 5 min; since 27 Sep "up" means a listener on loopback). `monitor.js` ticks: corpus, wa, li,
  gmail (contact-status), **mail** (every message, 10 min), liaccept (LinkedIn MCP, 30 min). Reader (Opus) per
  person. Today review mode `/review/*`. Event ledger `~/.medtech-crm/events-ledger.jsonl`, Events view
  `http://127.0.0.1:4137/events`. `todayCount` in `crm-app/today-count.js`.
- **LinkedIn MCP:** `C:\\Users\\Alessandro\\.linkedin-mcp\\launcher.py` (stdio, venv python), used by
  `gtm-eng/run-commit.py`, `campaign.py send_invite`, and the CRM's liaccept tick; the CRM has a manual Repair button
  (find its route in `crm-app/server.js`: `/api/li-fix`) and `data.meta.liMcpOk / liMcpError`. The LinkedIn poll lane
  is `~/.claude/linkedin-poll/` (task LinkedIn-Poll, 15 min, lock `.run.lock`). Memory `reference_linkedin_mcp`,
  `reference_linkedin_poll`. In this session the MCP showed "failed to connect" twice while the engine's own stdio
  calls worked: a session-side failure is not the engine's failure, test the engine's path.
- **Hub:** lives ON THE BOX (`/home/da/approval-hub/server.js`, systemd da-hub, laptop 127.0.0.1:4180 is a TCP
  forward). hub-review `http://100.85.52.84:4142/` (edit then approve, verdict box, `d` already done, voice, live).
  `hub_outdated.py` box cron every 10 min. Guard rules `hub-rules.json` (H3 tightened, Italian restored).
  Ping = `POST http://127.0.0.1:4180/pending {text, context, kind:"update"|..., notify:true}`; read the `hub` skill
  and `_system/HUB-CARD-CONTRACT.md` first. Cards ping ONCE. An update closes itself after 72 h or when superseded.
- **To-do pipeline:** `_system/pipeline.py`, `_system/PIPELINE-WORKER.md`, skill `/todo`.
- **The savior** (box, always on): session "savior box (19-09)", reachable with SendMessage to
  `bridge:session_01D7DFpQ9Y4u7UYnmwFJe1om`. It owns the Telegram lane. NEVER run the `claude` CLI from the savior.
  It already runs a 22:12 pre-sweep and the 23:00 sweep; it has his OK (27 Sep) for the identifier pass on the 41
  people without any contact detail.
- **Hooks:** all PreToolUse checks are `~/.claude/hooks/pretooluse.js`; other hooks go through `run-hook.js`.
  Never add a bash hook. Memory `reference_pretooluse_hook_hang_npx`.

## 4. Design constraints for the agent (from his standing rules)
- "Constantly run" must not mean a Claude session that waits: a scheduled watchdog (deterministic checks, cheap,
  every 10 min) that calls Opus only when something is wrong or for the two daily reports. Opus where it decides,
  Haiku never. Every scheduled console task goes through a .vbs (no window). Laptop sleeps at night: the parts that
  must run with the laptop off belong on the box.
- Fix forward only when safe and reversible; anything that sends to a person beyond what he already committed needs
  his verdict. A committed batch IS the yes: restarting a campaign he committed is in scope, inventing sends is not.
- The permission classifier of a session refuses to watch real sends in the background (seen 28 Sep): the agent must
  be its own scheduled process with its own log, not a session polling.
- Two pings a day, as hub cards `kind:"update"`, top down: first line = the state in one sentence (is GTM pushing
  today, yes or no), then campaigns (sent today / due / blocked and why), follow-ups waiting, hub items waiting too
  long with their age, tools (LinkedIn, Gmail tokens, servers, sync). What it fixed by itself since the last ping.
- It must be judgeable: every check leaves a line, every fix says what it did (RULE-LOOP, CRM H34).
- Output goes into the owning system: the agent lives in `~/gtm-eng/` (or `task-land/_system/` for the cross-system
  parts), state in its own folder, no new repo.

## 5. Known open items (unrelated to the agent, do not lose)
- Dead Gmail tokens `sodano23`, `alesoda2002` (his to re-authorise). DKIM on tundrahealth.ai (his).
- Box cannot serve https until he runs there `sudo tailscale set --operator=da`.
- 192 of 237 events in 3 days come from people not in the CRM: listed, nothing done.
- task-land sync: add `merge=union` for the append-only logs and an alarm on ahead/behind (parked twice in a month).
- Quick Claude widget bug (agent report never delivered).

## 6. Memory to read
`reference_gtm_boards`, `reference_daily_campaign`, `reference_linkedin_mcp`, `reference_linkedin_poll`,
`reference_hub_lives_on_the_box`, `reference_hub_review_ui`, `reference_event_loop_voice_feedback`,
`reference_todo_pipeline`, `reference_coattio_servers`, `reference_interactive_console_tasks_open_windows`,
`feedback_unattended_run_never_wait_on_agents`, `feedback_commit_batch_is_the_yes`, `feedback_approval_ping_once`,
`reference_pretooluse_hook_hang_npx`.
