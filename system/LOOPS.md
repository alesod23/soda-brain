# LOOPS: how the system works

The system is a set of loops, not a set of apps. Each loop takes events from the world, proposes a decision to
Alessandro, executes his yes, and learns from his sentences. This page names every loop, what feeds it, where it
writes, where he decides, and where its rules live. Paths are given for the laptop (C:/Users/Alessandro/...) and the
box (/home/da/...); the machines are described in MACHINES.md, the stores in DATA-MAP.md.

Last verified: 2026-10-02 (from the code and the inventories of 1 Oct).

## The shape every loop shares

1. Events in: a message, a reply, a calendar booking, a Notion meeting note, a LinkedIn accept, a to-do line.
2. A reader (Opus, headless, with the rules of its surface and a PERFORMANCE HINTS block) decides what the event means
   for ONE person: the next step, who owes what, what artifact is needed.
3. An artifact: a Gmail draft, a WhatsApp draft, a calendar hold, a CRM step, a hub card.
4. His verdict: on Telegram (the savior relays it) or on the hub-review page, yes / no / one sentence. A committed
   batch on a board is the yes. Nothing is sent without it; the daily campaign fire is the one delegated exception.
5. Execution of the yes by the system that owns the artifact (the lane sends the draft, the CRM moves the step).
6. Learning: his sentence becomes a rule (ledger, compiled skill), a hint (component hint file) or a fix; observers
   write hit lines; the simulation replays the misses.

Three ledgers of truth cut across all loops: Sent mail, WhatsApp and LinkedIn outbound are the truth of what he did
(a message he sent counts as approved, whatever the card said); the CRM row is the truth of where a person stands;
`decisions.jsonl` is the truth of what he decided.

## 1. The event loop (CRM monitor and reader)

- Code: `.medtech-crm/crm-app/monitor.js` (task CRM-Monitor on the laptop, ticks every few minutes), `reader.js`,
  `reader-queue.js`, `observer.js`, `owed.js`, `sources.js`.
- Feeds: Gmail (the triage helper, several accounts), the WhatsApp store (`G:/My Drive/DA/wa-store.jsonl`, shipped by
  the box's daemon every minute), the LinkedIn store (`G:/My Drive/DA/linkedin-store.jsonl`, written by the laptop's
  LinkedIn poller every 15 min), the sent corpus, Google Calendar, the Notion Meetings database (relation Contact).
- Each event: matched to a CRM person (`matchPerson`), applied (`applyEvent`: replied, accepted, booked ...), written to
  `events-ledger.jsonl` with what the system did and why (CRM rule H33, H34: every event leaves a line, judgeable), and
  queued for the reader.
- The reader: per person, loads the CRM contract whole, the person's `relationship_state`, the events since
  `last_read_event_id`, the current step and its origin, the hints (`task-land/_system/hints/crm-reader.md`); answers
  one JSON: state, step {text, due, channel, who_owes}, origin_why, match_of_previous. Depth is switchable
  (`DA_DEPTH=full`: tools Read and Grep, more turns, higher effort).
- Writes: through `PUT :4124/api/data` only. From 2 Oct every save is mirrored to Postgres on the box (`pg-mirror.js`,
  phase 3a of the brain).
- He sees: CRM Today (:4124/#today, laptop; the box's :4124 is a pull), the review mode (j/k, a/s/c held until commit),
  the daily page's one line "Today's items in the CRM (n)".
- Rules: `CRM-CONTRACT.md` (42); observer scores H2, H15, H16, H17, H21 on every write and render.

## 2. Inbound asks (WhatsApp, LinkedIn, email asks)

- Code: `gtm-eng/agent/inbound_asks.py` (task DA-InboundAsks), reading the same stores; a question or a request in an
  inbound message becomes a card with a draft answer (email: a Gmail draft through the lane; WhatsApp: a wa-draft card
  with action wa-send; LinkedIn: a DM draft), never a claim of an attachment, and `questions_for_him` when the answer
  needs him. Accept guard: a LinkedIn accept on a person with an existing conversation does not reset the step.
- Hints: `task-land/_system/hints/inbound-asks.md`.

## 3. The meeting loop (Notion meeting notes)

- Code: `gtm-eng/agent/meeting_loop.py` (task DA-MeetingLoop, every 30 min on the laptop). Lists Notion meeting notes
  through the Notion MCP (`claude -p --strict-mcp-config`), reads the FULL transcript, interrogates it with
  `MEETING-CONTRACT.md` (next steps, who owes what, people and addresses, dates, deliverables) plus the hints
  (`hints/meeting-loop.md`); writes the step and the origin `notion:<page>` to the CRM; posts cards for owed artifacts.
- Since 2 Oct 2026: the reader returns `dated_items` (every commitment: who owes, due, quote, artifact) and
  `write_loops` records them as `relationship_state.open_loops` with `due` and `origin notion:<page>`; a call clears
  `reply_owed`; a step the reader or he set after the call is kept (`step_kept`), his own sentence always wins; a
  booking card closed without an explicit no keeps the call; a call with no email on the row gets a WhatsApp
  follow-up card. Measured latency live: the card lands 2 minutes after Notion stops editing the note (the note
  settles 22 to 49 minutes after the call starts).

## 4. The draft lane (every message to a person)

- Code: `task-land/_system/drafts/`: `register.py` (a real Gmail draft + a sidecar `r<draft_id>.md` + a hub card),
  `critic.py` (judges the draft against `EMAIL-REVIEW-CONTRACT.md`, writes hit lines), `reconcile.py` (box cron every
  5 min: Gmail drafts vs sidecars vs queue vs cards: sent, rejected, edited in Gmail), `handoff.py`, `hubedit.py`,
  `send_card.py`. Skill `drafting` (compiled from the ledger) is loaded before any message is written.
- His verdict: `N dsend` sends now, `N no` plus a sentence rewrites, `N change: ...` edits; Quick Claude Alt+Win+J
  then D on the laptop; the hub-review page on the phone. Attachments are his to add in Gmail.
- A draft is never deleted by the system; a message he sent himself closes the card (reconcile sees Sent).

## 5. The approval hub and the review page

- Code: `/home/da/approval-hub/server.js` (systemd `da-hub`, :4180 on the box; the laptop's 127.0.0.1:4180 is a
  forward over Tailscale), `/home/da/hub-review/server.js` (:4142, the phone page: j/k, a/s/x/c, one commit = the yes).
- A card: `POST /pending {text, context, notify:true}`; the decision in `text`, the artifact in `context`; it pings
  once on Telegram; resolved cards are pruned after 24 h from `state.json`, so counts come from `decisions.jsonl`.
- The guard (`hub-rules.json`) downgrades cards that break `HUB-CARD-CONTRACT.md` (kind update, never refuses).
- Hygiene: `task-land/_system/hub_outdated.py` (box cron every 10 min) closes cards made moot by later events; the
  23:00 digest (`triage/eod_sweep.py`) lists every open card; the 22:12 pre-sweep (savior) closes what he already did.
- Rule H15 (hub): he ticked the line himself = the card closes.

## 6. Campaigns and boards (GTM engine)

- Code: `gtm-eng/` (board-server.js :4141, `campaign.py`, `run-commit.py`, `commit-to-contacts.js`,
  `daily-campaign/` research.py, build.py, fire.py, postmortem.py, review.py; boards under `gtm-eng/boards/<slug>/`).
- A board = evidence per person, reviewed j/k in the GTM Chrome tab group (opened only via `open-board.ps1`); a commit
  = the yes; `run-commit.py` executes it (LinkedIn invites via the LinkedIn MCP on the poller profile, emails through
  the lane, CRM intake). `campaign.py` runs the sequences with waits (`campaign_wait_step`), replies pause a hospital
  (card), auto-replies are not replies, "remove me" suppresses for 12 months.
- The daily US campaign: 30 researched a day on `boards/daily-<date>`, the first 10 fire at 16:55 (task
  DailyCampaign-Fire) within the caps of `_system/outreach/ledger.json`; subject fixed, one provider sentence, named
  people not offices; SMTP check before any draft.
- LinkedIn session: `agent/li_restore.py` (exit 2 = he must sign in; the sign-in window must be opened by the system
  before any "needs you" card), `linkedin-poll/poll.py` (inbox every 15 min), the accept tick in monitor.js.

## 7. The system agent and the feedback worker

- Code: `gtm-eng/agent/gtm_agent.py` (task GTM-Agent, every 10 min): checks that campaigns run, follow-ups are current,
  hub items are not waiting, tools are usable; a whitelist of fixes; 2 update cards a day; `box_watch.py` on the box
  posts "laptop silent". `feedback_worker.py` (task DA-FeedbackWorker) takes system feedback items
  (`_system/gtm-agent/system-feedback.jsonl`, filed by `feedback_queue.py` from his sentences and by the simulation's
  learner) and fixes what is in its whitelist; items it cannot take are `needs_him`.
- `due_today.py` (built 1 Oct, not scheduled): a promise he made ("reach back in two weeks") comes back prepared on
  its day.

## 8. The rule loop

- His five sentences: "this sucks because", "I like this", "this again", a change request, "slower/faster".
- `addrule.py --contract email|hub|crm|notif|meeting` the same turn; `compile_skill.py --install` compiles the skill;
  observers (critic, hub guard, CRM observer) write `rule-hits.jsonl`; `rule-stats.py` counts; `system-check.py`
  (09:10) writes the weekly check when the decision window is full; the box posts it. Canonical: `task-land/_system/RULE-LOOP.md`.
- Phase 2 of the brain: ledgers and hits move into `soda-brain/rules/`, every rule gets `since`, `checked_last`,
  `superseded_by`; `brain check` demotes by the number.

## 9. Tasks and the daily page

- Code: `task-land/_system/daily-sync.ps1` + `daily-lib.ps1` (the watcher, task DailySync-Watchdog every 5 min),
  `capture.py`, `pipeline.py` (stage: created, in progress, ready for review, finished; the card decides the task),
  `surface-sweep.ps1`, `crm-bridge.ps1` (a to-do naming a person becomes that person's CRM step).
- The daily page (Obsidian, `Daily/<date>.md`) is the edit surface: ((prompt)) directives, retitle = rename, overwrite
  = replace, done items stay until the next day, three mirror lines (CRM count, hub count, daily campaign).

## 10. Notifications and voice

- `/home/da/sodanotif/` (systemd `da-sodanotif`, pollers every 60 s): Gmail, Slack, WhatsApp taps and the LinkedIn
  store, classified by `routing-prompt.md` and `NOTIF-CONTRACT.md`, pushed as Telegram cards; CDTM group mail never,
  noreply never, groups never.
- Voice: short notes on the laptop (`.claude/voice-lane`), long recordings on the Drive mount transcribed on the box
  (`da-voice.timer`, faster-whisper) and routed by the safe-word prompt.

## 11. The savior (the always-on session)

- A Claude Code session in tmux on the box (`savior`), the only Telegram poller (plugin), relays his words: verdicts
  on cards, "hub-review commit ...", corrections to file, questions to answer. It never runs the `claude` CLI, never
  respawns itself (cron `box-sessions.sh` keeps it alive), never sends anything that is not a verdict he gave.
- A laptop session (DA SYSTEM) does what needs Chrome, Windows, the CRM writer and the GTM boards.

## 12. The simulation (the judge of all loops)

- `~/sim/harness/` (laptop, local git): a sandbox copy of the whole system with a fake world (60 fictional people, mail,
  WhatsApp, LinkedIn, calendar, Notion notes), a "me" agent that decides as he does, a judge that scores detected /
  latency / sent-without-yes / artifacts, and a learner that turns misses into hints, rules, fixes or `needs_him`.
  12 simulated days on 1 Oct: score 56 to 61; the misses are in the artifact layer and hub hygiene, not in reading.
- Nothing fake ever enters the real CRM, mail, Notion, memory or tasks; the fake world is deleted on his word.

## 13. The brain (this repo) and the door

- `soda-brain` holds the map, the facts, the handoffs, the rule pointers; `da-brain` on the box (:4150) indexes it
  with pgvector every 5 min and serves `recall`, `what_is_true`, `page`, `crm_person`, `crm_search` over HTTP and MCP;
  the CRM document is mirrored into Postgres on every save (phase 3a); phase 3b makes Postgres the source and the box
  and the laptop read the same rows; phase 3c gives the orchestrator a propose route gated by the hub.
- The orchestrator (instinct, from 2 Oct 2026): uses its own connectors for Notion, WhatsApp, the Tundra Gmail and
  Calendar; reads this repo, task-land and coattio on GitHub; gets the CDTM account and LinkedIn through the door;
  proposes, never holds a send scope (his decision 2 Oct, to be relaxed rule by rule for what he never reviews); puts
  the rules it learns into `rules/inbox/` so they are filed in our ledgers and the orchestrator stays replaceable.

## Known gaps and open questions

- Measured 2 Oct 2026 (simulation `meetings-night`, 4 days, 85 events, days 2-4 average 64.6/100): meeting notes 62
  (accurate cards, 61 to 202 minutes after the call against the 30 the rule wants), bookings 37, LinkedIn inbound 33,
  hub surface 33, note-only promises 42. New people met in a note or on WhatsApp often get no CRM row. The learner's
  71 items are in `~/sim/runs/current/learn.jsonl`; the night's report is in
  `task-land/_system/WORKPLAN-20261001-soda-brain.md` (MORNING REPORT).
- Fixed the same night: the reader now receives the full inbound mail text (`gmail.py recent --with-body`, 4,000
  chars) instead of the Gmail snippet; a call with no email on the row gets a WhatsApp follow-up card.
- `due_today.py` is not scheduled; the meeting loop's open-loops change is designed, not built.
- Hub hygiene scored 32/100 in the simulation: cards stay open after he did the thing or the event passed.
- The LinkedIn accept tick and `li_restore.py` "needs you" cards: the sign-in window must be opened by the system first.
- The box's contacts sync and the sodano23 Gmail token are expired (FINDINGS-20261001.md); the 23:00 digest's Telegram
  send fails with HTTP 400.
