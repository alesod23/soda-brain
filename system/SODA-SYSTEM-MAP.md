# SODA SYSTEM MAP: the agentic system and the brain, drawn

The visual map is `SODA-SYSTEM-MAP.html` in this folder (open it in Chrome; it works offline except for the fonts).
This page is its narrative and its index, so the brain can recall it. Same rules as the rest of `system/`: updated in
the same turn as a service, port, job, store or rule changes; dated; no secrets; no person records.

See also: the skills map, every skill in its current state with its ledger, map, loader, observer and coverage
([SODA-SKILLS-MAP.html](file:///C:/Users/Alessandro/soda-brain/system/SODA-SKILLS-MAP.html), Markdown twin
[SODA-SKILLS-MAP.md](file:///C:/Users/Alessandro/soda-brain/system/SODA-SKILLS-MAP.md), 2026-10-04).

Last verified: 2026-10-05 04:43 (laptop `schtasks` read at 03:17; box rows from the inventory of 1 Oct and the build
log of 3-4 Oct, not re-checked on the box that night). 2026-10-04 19:15: Granola retired (his ruling); node w_granola
is drawn retired (task Granola-Auto-Sweep disabled), the Notion meeting note is written by Notion's meeting AI.

## The shape

Six lanes. An event enters from the world (a mail, a WhatsApp, a LinkedIn accept, a Notion meeting note, a calendar
booking, a Slack DM, a line typed on the daily page, one of his sentences). A reader decides what it means for ONE
person: the CRM monitor and reader on the laptop, the meeting loop, inbound asks, due today, the sodanotif classifier
on the box, the page classifier in the daily watcher. The brain answers "what is already open": Postgres `soda` on the
box behind the door `:4150` (memory, rules, hints, CRM people with vectors, to-dos, hub cards, CRM review items as
their own kind `review` since G12), filled every 5 minutes from the repos, the task files and the CRM review board. His gate: Telegram through the savior, the hub-review page `:4142`, a GTM board,
CRM Today, the daily page. Execution by the system that owns the artifact: the hub sends by draft id, WhatsApp through
`:4119`, LinkedIn on the laptop, the CRM step moves, the to-do ticks with evidence. Learning: his sentence becomes a
ledger line the same turn (`addrule.py`), the compile makes it a skill, observers count hits, the cleaning layer tunes
thresholds, the simulation replays the misses.

The teal wires are what 3 and 4 October added: THE CONNECTION (`todo_match.on_event`, every event matched to open
to-dos, people and cards, one Opus judgement on a strong hit, a tick or a close with the quote), the REVERSE PASS
(every open card looks for its own outcome in the events about its person), the condition re-checker, the Cleaning
tab, and the learning layer (built, off until the Tuesday reset).

## The machines

The laptop sleeps, so it owns only what needs Chrome, Windows or him: the CRM writer `:4124` and intake `:4137`, the
GTM boards `:4141`, the LinkedIn poller and sends, Obsidian, 35 scheduled tasks (all through `run-hidden.vbs`). The
box never sleeps, so it owns every listener and every night job: the savior session (the only Telegram poller), the
approval hub `:4180`, hub-review `:4142`, the brain `:4150` with Postgres, the WhatsApp daemon, sodanotif, the cron and
timers (sweep every 10 min, reconcile every 5, sync every 60 s, dump at 03:30). The phone runs nothing. Git carries
the repos both ways; the Drive folder `DA/` carries the two stores too live for git.

Decided 4 Oct 04:00 and being built: the CRM becomes the place where every follow-up with a person is decided and
sent, the box becomes the CRM writer (the laptop a replica), the hub keeps non-person items and the "add this person
to the CRM?" cards. The HTML carries the state at the time above; the plan is in
`task-land/_system/WORKPLAN-20261001-soda-brain.md`, THE PLAN, item 10.

## The flows drawn in the HTML

1 an inbound email · 2 a WhatsApp message · 3 a Notion meeting note · 4 a LinkedIn accept or DM · 5 a to-do line typed
in Obsidian · 6 a daily campaign day (research paused to 7 Oct) · 7 a sentence from him (the rule loop) · 8 the night ·
9 THE CONNECTION · 10 THE REVERSE PASS · 11 the feedback session (armed) · 12 the learning layer (off).

## What the inventory corrected in the older pages (4 Oct 2026)

- `LOOPS.md` section 7 said `due_today.py` is not scheduled: task `DA-DueToday` runs daily 08:30.
- `MACHINES.md` section 4 said DA-MeetingLoop every 30 min: `schtasks` says every 5 min; Voice-Lane-Watch is enabled
  (every minute), not historical; eight tasks were missing from the table: DA-Supervisor (10 min), DA-InstinctInbox
  (15 min), DA-DueToday (08:30), Granola-Auto-Sweep (08:15), Peer60-AcceptCheck (09:00, 18:00),
  RuleLoop-SystemCheck (09:10), SODANOtif-Recap (2 h), CDTM-Kickoff-Weekly-Update (Thu 16:00).
- `LOOPS.md` section 1 names a task CRM-Monitor: no such task exists; the monitor ticks inside the CRM server.
- The hub-review page died at load from 3 Oct 23:50 to 4 Oct 03:57 ("Identifier 'rv' has already been declared", a
  duplicate `const` from the Cleaning patch): "loading cards" with the server healthy means a client error; read the
  browser console first.

## Changed node 4 Oct 2026 22:15: the LinkedIn event (`ev_li`) reads a quiet thread by person (G89)

`ev_li` was "inbox only": the poller reads the newest ~10 to 17 threads, so a reply in a quiet thread (the Ienna case)
never reached the store. Now every poll tick, in the same launcher, also opens up to 2 threads by id
(`linkedin-poll/li_person.py`, `fetch_person`): CRM Today people with LinkedIn whose thread is outside that window, each
once a day; and `poll.py --person <pid|url|thread>` does it on demand. It writes to the same store with the same ids,
his messages and their replies newer than what the store held; older inbound history is reported, never written. New
wire: ev_li reads the CRM (Today people, read-only). Details in `LOOPS.md` section 1.

## New node 4 Oct 2026 19:40: the UI walk (`w_uiwalk`, laptop, script)

`task-land/_system/system-agent/ui_walk.py`, task `DA-UIWalk` (08:00 to 23:00 every 3 h). It reads his gates the way
he sees them: `gate_review` (hub-review, every tab, 1568 and 390 px), `gate_crm` (CRM review mode and Today, box and
laptop), `gate_tg` (through the hub ledger's Telegram message ids). It writes faults into the System Agent's registry
(`broken.jsonl`, items `UI-<surface>-<width>`), which map-sync draws on those gate nodes. Wires: w_uiwalk -> gate_review,
gate_crm, gate_tg (reads); w_uiwalk -> the registry (writes). Not yet drawn in the HTML (the System Agent build owns
the NODES rebuild and its review loop); details in `LOOPS.md` section 7.

## New node 4 Oct 2026 19:40: the daily System Update and the Judge (`b_sysupdate`, box, script)

`task-land/_system/system-agent/system_update.py`, box cron at 08:00 Rome (`0 6,7,8 * * *`, self-gated): one page
`system-agent/updates/YYYY-MM-DD.html` and one hub `update` card a day (how it went, mistakes and good things, new rules,
the maintenance of the whole core, fix sessions per day for 7 days with the ALERT rules). On Sunday it calls THE JUDGE
(`judge.py`, Opus, weekly): one verdict over 7 days into the page and `judge.jsonl`; a SYSTEM-WIDE verdict becomes a
registry line. Wires: b_sysupdate reads the registry, nodes.json, decisions.jsonl, the ledgers, integration and UI walk
runs, health-vps.json; writes the hub (one card) and the registry (the Judge). Not yet drawn in the HTML or in
`nodes.json` (the System Agent build owns both); details in `LOOPS.md` section 7.

## New loop 4 Oct 2026 20:50: the CRM System log (item 18, G114)

His "Something missing / wrong" line on any CRM page (review mode included) is a row of `system-feedback.jsonl` on the
CRM writer (box), forwarded to hub-review `/api/feedback` (surface `crm-system`), routed by the box feedback session
(`ledger_verdict.py`, the same route as every feedback box) and answered back into the same line by
`task-land/_system/crm_system_log.py` (route, answer, proof). No new node: an edge CRM -> hub-review queue -> feedback
session -> CRM, and the System log list in hub-review's CRM tab. LOOPS.md section 8 has the contract.

## New loop 4 Oct 2026 21:35: proactive to-dos from an accepted ask (item 19, G118)

An ask someone made of him plus his yes becomes ONE `todo-proposal` hub card of to-dos, each with its owning system.
No new node and no new cron: the reader (`task-land/_system/proactive_todo.py scan`) rides on the box's `hub_outdated.py`
pass and reads the CRM monitor's event ledger (edge events-ledger -> hub_outdated -> hub /pending); his verdict comes back
through decisions.jsonl to the laptop task DA-ProactiveTodo (`proactive_todo.py apply`, edges decisions.jsonl -> trippy
trip to-dos / CRM intake :4137 task-handoff / capture.py). New store: `trips/<slug>/todos.jsonl` in trippy, shown on the
board's To-dos page. His words on the card: hub-review queue -> feedback session (`TYPE_ROUTES`) -> PROACTIVE-CONTRACT.
LOOPS.md section 9 has the contract.

## How to keep it

The data is one JS object at the bottom of the HTML (`NODES`, `EDGES` in `SHAPE` and `MACH`, `FLOWS`); the charts draw
themselves, so a change is a row, not a drawing. Move the "Last verified" line in both files.

**4 Oct 2026 23:05, G110 (plan item 17 + 17(f)).** `gate_review` (hub-review :4142) gets the System agent tab (Needs you,
Spot check, Whitelist changes, Review, Health) fed read-only from the System Agent's registry, incidents, whitelist changes
and System Update in the synced task-land, plus nodes.json, the laptop heartbeat and health-vps.json; and a left index on
every tab. New edge: hub-review spot verdict -> `system-agent/spot-verdicts.jsonl` (+ a Wrong to the feedback session).
The audit became `system-agent/whitelist_actions.py` (duplicate cards, booked-and-never-sent, automatic-reply successors),
reporting into `whitelist-changes.jsonl`. No new node; LOOPS.md sections 5 and 7.
