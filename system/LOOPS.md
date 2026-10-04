# LOOPS: how the system works

The system is a set of loops, not a set of apps. Each loop takes events from the world, proposes a decision to
Alessandro, executes his yes, and learns from his sentences. This page names every loop, what feeds it, where it
writes, where he decides, and where its rules live. Paths are given for the laptop (C:/Users/Alessandro/...) and the
box (/home/da/...); the machines are described in MACHINES.md, the stores in DATA-MAP.md.

Last verified: 2026-10-02 (from the code and the inventories of 1 Oct). 2026-10-04: the visual map
`SODA-SYSTEM-MAP.html` (+ `.md`) draws these loops; its inventory corrected this page: `due_today.py` IS scheduled
(task DA-DueToday, 08:30); there is no task CRM-Monitor, the monitor ticks inside the CRM server; the meeting loop
runs every 5 min. Decision of 4 Oct 03:48: the CRM becomes the surface where every follow-up with a person is decided
and sent and the box its writer (THE PLAN item 10; memory `project_crm_is_the_followup_surface`).

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
- Since 4 Oct 2026 05:00 (THE PLAN 10(d), CRM H51, the hub's double system on the CRM): the hygiene worker
  `.medtech-crm/crm-outdated.js` (laptop task CRM-Outdated, every 10 min through `run-hidden.vbs`; log
  `crm-outdated.log` + `crm-outdated.out.log`, state `crm-outdated-state.json`, lock beside it) checks every OPEN review
  item (`review-api.items({coming})`, about 180 on the first pass). PATH A: every new line of `events-ledger.jsonl` goes
  through `POST :4150/brain/match` (brain.match_event, the lookup of `todo_match.on_event`); the event's pid and a CRM
  person the brain returns whose first and last name the event carries are the items it touches, checked against that
  event only. PATH B (the reverse pass): every open item against the person's whole timeline. Rules in order: a call or
  meeting after the step / owed reply AND after the draft (H52) = remove; their message after the draft = rewrite (draft
  retired, Opus writes a new one); his own message on the draft's channel saying the same thing = remove; the
  conversation on another channel = channel; his message on another channel since the step = the Opus judge (moot at 70+,
  6 a pass, `judged` marks, never Haiku). A change goes through `POST :4137/review/updates/apply` (the review API owns
  the dossiers; the person through `PUT :4124/api/data`): versions are RETIRED, never deleted (`current()` skips them,
  so a retired draft is never sent); one line per change in `review/updates.jsonl` (id, ts, pid, name, kind
  rewrite|remove|redate|channel, before -> after, why, evidence {event_id, at, channel, text, would_also_B, brain},
  path A|B, judge, undo payload); `person.review_state.last_update` records it on the row (so the Postgres mirror and
  the brain see it). Measured: one line per pass in `review/crm-outdated-metrics.jsonl` (A: events, brain calls and
  failures, matched by pid / by the brain, strong to-do or card hits, items checked, changes, judged; B: items checked,
  changes, judged; overlap = an A change B would also have found); `node crm-outdated.js report` answers "which path
  solves most" with the undos counted. He sees: the `Updates (N new)` button on the review-mode bar opens the list
  (`GET :4137/review/updates`, last 24 h, newest first, marks seen; `?peek=1` does not), each line who / before -> after
  / why / evidence / Undo (`POST :4137/review/updates/undo {id}`: retired versions back, a version written for the
  update retired, the step, origin, reply_owed and reply_seen restored, a `step_restored` activity, a `crm-updates`
  line in decisions.jsonl). Deep link `?review=1&updates=1` or `#/today/updates`. Ping: ONE link-only hub card (kind
  update, `meta.origin crm-outdated`) at most every 12 h when a pass changed something. Tests:
  `node --test tests/crm-outdated.test.js` (a stub CRM on a copy; no model). Box: not scheduled yet (the CRM writer is
  the laptop); at the cut-over the cron line is
  `*/10 * * * * cd /home/da/coattio && flock -n /tmp/crm-outdated.lock node crm-outdated.js >> /home/da/.local/state/crm-outdated.log 2>&1`
  and the laptop task is disabled the same minute (one worker, one writer).
- Since 4 Oct 2026 (same build): the reader asks the brain before it writes a step (`crm-app/brain.js` -> `POST
  :4150/brain/match` with the person and the step, token `SODA_TOKEN_RO` from `~/.env/soda.env`); a strong open to-do or
  hub card (sim >= 0.84) is named in the origin's why in words ("already open in the brain: to-do ..."), the whole match
  is kept as `next_step_origin.brain`; the door down = the step is written anyway with `brain.ok false`.

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
- Since 3 Oct 2026 (S10, the producer check): the reader has a second MCP tool, `match_event` on the brain door
  (`~/.claude/scripts/meeting-reader.mcp.json`, token `${SODA_TOKEN_RO}`), calls it for every commitment it is about
  to propose, and returns `already_covered` + `next_step.covered_by`; the card then says "Already on your to-do (id):
  no new step" instead of proposing it again. Verified on Sophie Tollmann's note: the Pietro intro was found as the
  open sub-item `healthcare-ecosystem-push#3`.

## 4. The draft lane (every message to a person)

- Code: `task-land/_system/drafts/`: `register.py` (a real Gmail draft + a sidecar `r<draft_id>.md` + a hub card),
  `critic.py` (judges the draft against `EMAIL-REVIEW-CONTRACT.md`, writes hit lines), `reconcile.py` (box cron every
  5 min: Gmail drafts vs sidecars vs queue vs cards: sent, rejected, edited in Gmail), `handoff.py`, `hubedit.py`,
  `send_card.py`. Skill `drafting` (compiled from the ledger) is loaded before any message is written.
- His verdict: `N dsend` sends now, `N no` plus a sentence rewrites, `N change: ...` edits; Quick Claude Alt+Win+J
  then D on the laptop; the hub-review page on the phone. Attachments are his to add in Gmail.
- A draft is never deleted by the system; a message he sent himself closes the card (reconcile sees Sent).
- **Attachments survive a critic rewrite (box, 2026-10-01).** A rewrite builds a NEW Gmail draft from the critic's
  body and deletes the old one, so anything attached was silently lost and the mail still promised it: the Galbiati
  mail reached the card saying "in allegato trova una breve presentazione" with nothing attached. They are declared in
  the sidecar now, `attachments: [_system/drafts/attachments/<file>]`, re-attached by `register.py` on every rewrite,
  and a declared file that is missing stops the rewrite instead of shipping the promise. The line above, "attachments
  are his to add in Gmail", is no longer the whole truth: the lane attaches too, and `gmail.py update-draft` is the
  way to change a body WITHOUT losing one.
- **`answered_elsewhere` has an event floor (box, 2026-10-01).** It used to call a draft answered when ANY later
  message of his existed on the thread, so a post-call follow-up written three days after his own scheduling reply was
  killed before it ever reached a card. When the sidecar names a source event (`source: ... (YYYY-MM-DD)`) only a
  message sent after THAT counts. The Martina case it was built for is unaffected: no event, no floor.

## 4b. Producers attach to the CRM item, not a card (THE PLAN 10(c), built 4 Oct 2026 04:50)

- A producer's draft for a person with a CRM row goes onto that person's Today review item and posts NO hub card.
  Route `POST :4137/review/artifact {pid, draft_id, sidecar, critic_line, compose_url, card:{text, context}, channel,
  subject, text, when_why, questions, source}` (`.medtech-crm/review-artifact.js`): appends a version
  (`source: hub:<producer>`, `draft_id`, `step_text` = the current step, so CRM H48 serves it as the step's draft);
  idempotent on `draft_id` (same text = unchanged, a revised text for the same id = updated in place); a new version
  clears a held approve of the old text. Refuses: 400 unknown pid or a channel the row cannot use (`channelFor`),
  409 not on today's review or already dealt with today, 503 the answering server is not the writer (the box in
  local mode). On any refusal the producer posts its card as before: a draft is never lost.
- Callers: `task-land/_system/drafts/crm_artifact.py` (`attach`, `match_pid` by email, LinkedIn, unique name),
  used by the lane `send_card.py` (every email draft registered through `register.py`: due_today, inbound_asks,
  meeting_loop, instinct_inbox) and by the chat cards of `due_today.py`, `inbound_asks.py` (WhatsApp, LinkedIn) and
  `meeting_loop.py` (WhatsApp follow-up). Questions for him ride at the head of `when_why`.
- Still cards: "add this person?" (inbound_asks `propose`, `introduced`, CRM H39), non-person cards, call steps,
  the lane-failed and no-address cards, the meeting card (step + invite), a lane draft with declared `attachments`
  or `keep_card:` (meeting follow-up whose invite goes first), silent lanes (Quick Claude, CRM Ask), revisions of a
  card that is already open.
- Reach: the producers run on the laptop (DA-DueToday, DA-InboundAsks, DA-MeetingLoop) where :4137 is the writer; on
  the box 127.0.0.1:4137 proxies to the laptop while it answers, else 503 and the card. No queue.
- Off switch: `task-land/_system/drafts/crm-attach.off` (or env `CRM_ATTACH_OFF=1`) = cards again. Test:
  `node --test review-artifact.test.js` in `.medtech-crm` (a copy of crm.json, a fake person, a temp review dir).
- Gap: the review's approve sends through `drawer-api.sendNext` (a fresh Gmail draft, then send), not the lane's
  Gmail draft by id; the lane's Gmail draft stays in Drafts and its sidecar stays `drafted` (reconcile acts only
  when a draft leaves Drafts). `items()` does not
  serve `draft_id`/`compose_url` yet (review-api.js change owed).

## 5. The approval hub and the review page

- Since 3 Oct 2026 23:20, THE CONNECTION: every new mail, WhatsApp and CRM event (hub_outdated.py on the box, every
  10 min) and every finished call (meeting_loop.py) goes through `todo_match.on_event`: lookup in the brain, one
  judgement only on a strong hit (sim >= 0.84), a to-do ticked with the quote (laptop) or a card closed through
  `/close` with no verdict; log `_system/todo-match.jsonl`. The review page's fourth tab, CLEANING (key 4), lists
  every automatic closure or tick of the last 72 h with its evidence, takes his judgement per row (c, goes out with
  the commit) and reverses one row on request (`/api/cleaning/reverse`: a card re-posted, a to-do reverse queued).
  The reverse pass (same cron, 3 Oct 23:45): every open card looks for its own outcome in the events about its person
  (mail, WhatsApp, CRM, LinkedIn in and out; his own messages up to 10 days before the card count), judged only when
  something new arrived (`card_marks`), verdicts in `todo-match.jsonl` as `event: reverse`.
  The learning layer (`_system/cleaning_eval.py`, OFF until `cleaning-eval.on` exists, from the Tuesday reset): every
  automatic action and judge traced (local jsonl + Langfuse where the SDK and keys exist); success = 72 h without a
  reverse or a "wrong" comment; a weekly spot check of 3 random successes in the Cleaning tab; path A (event push)
  vs path B (sweep) attribution with overlap and time-to-find; a failure raises the threshold of its path and adds
  a (producer, person) exception without asking him; `cleaning_eval.py report` per path and surface.
  Since 4 Oct 2026: Slack (cdtm, xplore) is an event source for the forward and reverse passes (`slack_events`, the
  helper `slack.py` on both machines, non-fatal when a workspace fails). Retention (docs/RETENTION.md): the to-do
  history is append-only (RESTRICT + trigger), one CRM document snapshot a day, nightly `pg_dump` to the Drive mount.
- Since 3 Oct 2026 (his currency rule): every hub card is a row of the brain (`hub.cards`, embedded, filled from the
  hub's state on every index pass; a resolved or pruned card keeps its row), `brain.match_event` returns open cards
  as kind `card`, and `todo_match.py` can close a card whose outcome an event proves (`POST /close`, evidence in the
  reason, never a verdict). The hub supersedes an open twin at post time by producer + person + action (patch
  prepared, his run); the ALERT rule in `hub_outdated.py` matches only the head of a card and never a routine report.

- Code: `/home/da/approval-hub/server.js` (systemd `da-hub`, :4180 on the box; the laptop's 127.0.0.1:4180 is a
  forward over Tailscale), `/home/da/hub-review/server.js` (:4142, the phone page: j/k, a/s/x/c, one commit = the yes).
- A card: `POST /pending {text, context, notify:true}`; the decision in `text`, the artifact in `context`; it pings
  once on Telegram; resolved cards are pruned after 24 h from `state.json`, so counts come from `decisions.jsonl`.
- The guard (`hub-rules.json`) downgrades cards that break `HUB-CARD-CONTRACT.md` (kind update, never refuses).
- Hygiene: `task-land/_system/hub_outdated.py` (box cron every 10 min) closes cards made moot by later events; the
  23:00 digest (`triage/eod_sweep.py`) lists every open card; the 22:12 pre-sweep (savior) closes what he already did.
- Rule H15 (hub): he ticked the line himself = the card closes.
- **The review page, three fixes of 2026-10-01, all client side in `page.html` (backups beside it).** A card he
  committed a CHANGE on was frozen (`ST.queued`) and had every button hidden, so (a) a second thought had nowhere to
  go and ended up in the next commit's free-text SYSTEM box, detached from its card; (b) the freeze never lifted when
  the revision came back, which left two finished mails undecidable for five hours; (c) a text he had rewritten on the
  page was transmitted only with a YES, so a session asked for a change worked on the old body while he assumed his
  version had been seen. Now: a queued card keeps the CHANGE button only, the freeze lifts by comparing a snapshot of
  the card content taken at commit, and his edit rides on a change as `his_body` in the queue entry with a line in the
  Telegram message saying the base is his version. Filed as H20 and H21 in `HUB-CARD-CONTRACT.md`.
- **Still open (H21):** the system-wide feedback box takes no images, and he reviews on a phone where a screenshot is
  the fastest way to show what is wrong.

## 6. Campaigns and boards (GTM engine)

- Code: `gtm-eng/` (board-server.js :4141, `campaign.py`, `run-commit.py`, `commit-to-contacts.js`,
  `daily-campaign/` research.py, build.py, fire.py, postmortem.py, review.py; boards under `gtm-eng/boards/<slug>/`).
- A board = evidence per person, reviewed j/k in the GTM Chrome tab group (opened only via `open-board.ps1`); a commit
  = the yes; `run-commit.py` executes it (LinkedIn invites via the LinkedIn MCP on the poller profile, emails through
  the lane, CRM intake). `campaign.py` runs the sequences with waits (`campaign_wait_step`), replies pause a hospital
  (card), auto-replies are not replies, "remove me" suppresses for 12 months.
- The daily US campaign: 30 researched a day on `boards/daily-<date>`, the first 10 fire at 16:55 (task
  DailyCampaign-Fire) within the caps of `_system/outreach/ledger.json`; subject fixed, one provider sentence, named
  people not offices; SMTP check before any draft. The research round (task DailyCampaign-Research, `supervise.py`,
  one Opus worker x 80 min) is the most expensive job on the plan (2 Oct: 659 calls, 185 M cached tokens, ~3% of
  the week per day); PAUSED by his word until 2026-10-07 through `daily-campaign/research-pause.json`, boards
  meanwhile built from the pool backlog (361 people, all drafted on 2 Oct).
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
- The to-dos are rows of the brain since 3 Oct 2026 (S10 phase 1, the mirror): schema `todo` (items, sub-items as
  `<slug>#<n>`, links, append-only history, embedded chunks) filled by `tools/todo_ingest.py` from task-land
  `Tasks/**` at the end of every index pass (310 rows on day one), plus `crm.people_chunks` (641 people embedded);
  `brain.match_event` = RRF over both, k per kind; served as `POST /brain/match` (read-only token) and the MCP tool
  `match_event`; `tools/todo_match.py` does the lookup, one Opus judgement (done / moved / none with the quote) and
  the tick through `pipeline.py tick|redate --evidence` (log `_system/todo-match.jsonl`). Done is a state with
  evidence, never a delete. Phase 2 (writers go through the door, task files written from the rows) is next.
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
