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
  (4 Oct 19:19, goal run G10: that box cron crashed on every run, `lemlist-api.js:39` `path.join(USERPROFILE)` undefined
  on Linux; coattio 67ad780 falls back to `os.homedir()` in every box-required module; box check in
  `_system/box-steps-20261004-goal.sh` block G10.)
  and the laptop task is disabled the same minute (one worker, one writer).
  (4 Oct 19:48, goal run G111: path A's backlog of 8619 on the box had two causes. The ledger cursor lived in
  `crm-outdated-state.json`, which git tracks, so the box read the LAPTOP's byte offset against its own ledger; and the
  ledger repeats ids (laptop: 16073 lines, 1997 distinct ids, one corpus id 372 times). Now `scanLedger`: the cursor is
  machine-local in `.crm-outdated-ledger-cursor` (untracked, `.*-cursor`) with `seen` ids kept 14 days; a pass spends
  its 80 on DISTINCT unseen events oldest first and the offset stops before the first one it had no room for (deferred,
  never skipped); events older than 14 days are path B's. Metrics A gain `backlog`, `dup_lines`, `stale`; `report` gains
  `backlog` {distinct_unseen, repeated_lines, passes_to_drain} for THIS machine, read-only. coattio ae4783a; tests in
  `tests/crm-outdated.test.js` (3 new); box check block G111 in `_system/box-steps-20261004-goal.sh`.)
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

## 3. The meeting loop (Notion meeting AI notes; Granola retired 4 Oct 2026)

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
- Since 4 Oct 2026 19:15 (his ruling: "Granola is dead; meetings come from Notion's meeting AI"): this loop is the ONLY
  meeting reader. Granola is retired everywhere: task Granola-Auto-Sweep disabled (never deleted; window_lint clean),
  `~/.claude/granola-auto/run.js` exits unless `--force-retired`, `/granola` (`~/.claude/commands/granola/SKILL.md`) is a
  redirect to this loop (old text kept under "Retired"; for a Notion page link: `meeting_loop.py read <url>`
  read-only, `redo <url>` to re-read a note of the last 24 h). The reader is unchanged: listing
  `notion-query-meeting-notes` (sonnet, created in the last day) and per note `notion-fetch` with the transcript
  (opus), both through `~/.claude/scripts/notion-meeting-filer.mcp.json` / `meeting-reader.mcp.json`. Check:
  `python meeting_loop.py run --dry --force-list` (exit 0, nothing written) and `meeting_loop.py read <url>` on
  the Sophie Tollmann note returned the full interrogation (19:20). Gaps: the `granola` MCP server is still in
  `~/.claude.json` (his account-level config); granola-auto's medtech-brain `Raw/` copy of each Tundra call has no
  Notion-side replacement (closed by G96, next bullet); `~/.claude/CLAUDE.md` still names `/granola` in the auto-open
  list (his file).
- Since 4 Oct 2026 (G96, the medtech-brain Raw copy): the reader also answers `tundra_type` (granola-auto's three
  folders: `Client Call` = hospital or clinical-engineering buyer, `Ecosystem` = anyone else about Tundra, `Internal` =
  Tundra's team on Tundra, `""` = not Tundra business: CDTM, personal, other projects) and, for a Tundra call only,
  `notes_verbatim` (the page's own meeting-AI notes). `raw_copy()` then writes ONE file
  `~/medtech-brain/Raw/MM-DD <Title>.md` (no year in the name, `created:` inside; a generic Notion title such as
  "Meeting" becomes "Call with <name> (<org>)"): frontmatter `notion_page_id`, the meeting-AI notes verbatim, the
  reading's summary, key points (he owes, they owe, facts, commitments) and the transcript answers with their quotes.
  Idempotent by `notion_page_id` (a second pass finds the file and writes nothing); never overwrites (open "x", a
  same-name file gets " (2)"); no ingest (`/kb-ingest` is his). It runs after the empty/recording checks and BEFORE
  the internal skip, so a Tundra team meeting is kept as granola-auto kept it; any other note follows the old path
  unchanged (no state key, no print, no log). `--dry` prints the path and the first 25 lines, writes nothing;
  `meeting_loop.py read <url> [<created>] [<title>]` also prints the Raw file a Tundra note would get (always dry).
  Logged `raw` / `raw-failed` in `meeting-loop.jsonl`; the state note carries `raw: {state, path}`. Test:
  `python tests/test_raw_copy.py` (temp dir only: one write, second call none, non-Tundra none, dry none, no
  overwrite). Backfill (4 Oct, orchestrator's request): `meeting_loop.py backfill-raw [--since 2026-09-01] [--dry]`
  re-reads (read-only, once; readings cached in `meeting-loop-backfill.json`) the notes the loop processed before G96
  (state done / carded / internal) that have no Raw file, then calls `raw_copy`; it never writes the loop's state
  file. Run once for real: 8 files written (Ale x cal, Luigi Intrieri, Sebastiano, Annika, Istituti Clinici Zucchi,
  Ale x Caleb, Vincent Carte-Jacquesson of Hopital Foch, Sophie Tollmann); "Personal Finances" read as not Tundra. Backup `meeting_loop.py.bak-20261004-raw` (gtm-eng is not a git repo; the task-land
  mirror `_system/laptop-tools/gtm-eng/` picks it up on git-sync).
- Since 4 Oct 2026 (G103, the meeting OBSERVER): `gtm-eng/agent/meeting_observer.py`, called by `meeting_loop.py` after the
  card text is built (run, also `--dry`) and in `read <url>`. One hit line per HARD row of `MEETING-CONTRACT.md` into
  `task-land/_system/rule-hits.jsonl`, surface `meeting`: `ok` when his question was put to the transcript (an
  interrogation answer `from: H<n>`) and the code check of that rule held (H1 a step with a real date and who owes it,
  H2 the register quoted and a Lei call's Italian follow-up without tu, H3 every address used went through the SMTP
  check, H4 every dated item a real date), else `flag` with what failed. Never blocks, never edits. First real hits: 8 ok
  on the GSD call (`read`, 19:56). Test: `python task-land/_system/test_meeting_observer.py` (6 stored readings + a
  doctored one flagging H1 H2 H3 H4 H6; temp hits file).

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
  clears a held approve of the old text. Refuses: 400 unknown pid, a channel the row cannot use (`channelFor`) or a
  row marked not a target (the producer posts a "REFUSED by the CRM" card); 409 already dealt with today or he holds a
  verdict on that version (NO card: the item is on the board, `crm_or_card` answers route crm + held); 503 the
  answering server is not the writer (FAILED card). A draft is never lost.
- **The waiting kind (CRM H56 / HUB H41, 4 Oct 2026 19:05).** ANY known person takes the draft, whatever the step
  date: "not on today's review" is gone. The board's kinds are reply, due, WAITING, coming, done (in that order).
  `waiting` = "waiting for your verdict": a person whose live version (written for this step, H48) or job artifact is
  newer than his last decision on the item (sent, a committed skip, dealt with; a committed approve not yet sent keeps
  it) is on the board whatever the step date (`review-api.js waitingFor`); the card has its own heading inside "to
  review", the badge "draft ready" / "artifact ready" and the line "here: draft from the lane (card #19), attached
  4 Oct 18:15" or "here: artifact from the job <id>, attached ...". A person with NO step gets the H2 default step
  ("decide next step", +2 working days) before the version is written, origin `set_by lane|job`, source
  `draft:<id>|job:<id>` ("set by the lane on <day> from the draft <id>"). A job artifact answers `on_review: true`
  for every row except one marked not a target. crm-outdated sweeps waiting items like the others; the hub mirror no
  longer needs `allow_coming`. Tests: `node --test tests/waiting-kind.test.js`, `python tests/waiting_board_test.py`
  (headless 1568 / 390, light; review.js and styles.css from the working tree, the live list plus two synthetic
  waiting items, read-only).
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
- The send (closed 4 Oct 05:24): his approve of an EMAIL version that carries a lane `draft_id` goes through
  `drawer-api.sendLaneDraft`, the lane's own path: `gmail.py update-draft --account <sidecar account> --draft-id <id>`
  with his board edit (only when he edited; a failed update sends nothing), then `gmail.py send-draft --account
  <sidecar account> --draft-id <id> --confirmed` (what the hub's `gmail-send-draft` action runs). Never a second
  Gmail draft. The sidecar is then written through the lane's `common.py` like the reconciler does (`status: sent`,
  `sent_at`, `sent_message_id`, `sent_thread_id`, `sent_by: crm-review`, his text as `## Body as registered` plus
  `## His edit (CRM review)`), an open hub card on it is closed as sent, the CRM fact and `sent-log.jsonl` as for any
  drawer send. A sidecar already finished (`sent`, `rejected`, `abandoned`, ...) refuses with 409. LinkedIn and
  WhatsApp versions (no Gmail id) stay on `drawer-api.sendNext`. `items()` serves `source`, `draft_id`,
  `compose_url`, `questions`; the card shows "from the lane: <producer> · open draft" and the questions.
  Test: `.medtech-crm/tools/lane-test/test_lane.js` and `test_lane_full.js` (stubs for gmail.py, the CRM API and the
  sent-log; a fixture sidecar). Phone layout of the board: `.medtech-crm/tools/review_board_check.py`.

- **H41 / H42 / CRM H56 (his rules 4 Oct 2026 16:30): a message to a person NEVER appears as a hub card.** One door:
  `task-land/_system/drafts/crm_artifact.py crm_or_card()`. Known person (pid, email, LinkedIn URL, unique exact name,
  or a row whose whole name is the mailbox name) -> attached to the CRM card (`allow_coming`), no card; a call or a step
  with no text -> the CRM's own Today item, no card; unknown named person -> THE import card (`queue_import`: one open
  card at a time, revised in place without a ping, people in `meta.people`; "Import these N people into the CRM? yes =
  all, no + numbers = those", kind decision); the CRM refuses -> a card whose first line is `REFUSED by the CRM: ...`;
  the CRM does not answer or the producer failed -> first line `FAILED: ...`; both carry `meta.crm_pid` + `crm_url`.
  An email reaches the CRM only with its Gmail draft id (`sendLaneDraft`). His verdict on the import card:
  `apply_import_decisions()` (decisions.jsonl; rows via `POST :4137/intake`, matched by name with no org so a row that
  lacked its address is completed; then the message attached and its old card closed), called by inbound_asks.run
  (`import_opened` sets the reply owed) and instinct_inbox.run (`lane_on_yes` puts the shown draft in the lane, his
  words rewrite it). Callers of crm_or_card: due_today, inbound_asks, instinct_inbox, meeting_loop, send_card.py.
  Left as cards on purpose: silent loops (Quick Claude, CRM Ask), a bare number (not a named person, H56), the
  meeting loop's "next step?" questions. Executor state `~/gtm-eng/agent/crm-import-state.json`. Tests
  `drafts/test_crm_or_card.py` (11), the producer tests in `gtm-eng/agent/tests`. The 4 Oct sweep: `drafts/hub_sweep.py`
  (THE PLAN item 13).

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
- **THE ITERATION LOG (HUB H40 / CRM H55, his rule of 4 Oct 2026 16:13, built 16:35).** A card that came back to him
  after a CHANGE shows, on its face, every earlier input of his, verbatim and dated, with the version it produced, so
  he decides from the record and not from memory. One shape on both surfaces:
  `iterations: [{n, at, by, kind: change|comment|edit, his_words (verbatim, never trimmed), his_text? (his own version
  of the message), produced: {version, at, label} | null (= not yet applied), outcome? (the handler's note when the
  card text did not change), source}]` plus `version` (v1 as created, +1 per revision that changed what he reads:
  text, body, subject, context, action; a flag-only revise from hub_outdated or pipeline is not a version).
  Hub: the field lives ON the card. `POST /iterate {id, add | set, version}` (add one input; `set` = the backfill,
  keeps live entries it does not know); `POST /revise` links every open iteration to the version it produced and
  takes `iteration` (his words or text that caused this revision). Writers: hub-review COMMIT (a CHANGE, or a skip
  with a comment, appends his words), `reconcile.py` (his Gmail edit = its own version), `register.py` /
  `send_card.py --his-words "..." [--his-by telegram]` (a session revising after his Telegram "N change: ..."),
  `iterations.py add --card <id> --words "..."` for anything else; jobs.py and the feedback session need nothing,
  their `/revise` links the open entries. Derivation from the older records (hub-review `queue.jsonl` change and
  comment lines, `hub-edits.jsonl`, the sidecar's `## His edit (Gmail)`, `decisions.jsonl` feedback that is not
  `[observer]`) and the backfill: `task-land/_system/iterations.py derive|backfill [--apply]|add`. Telegram carries
  ONE line ("Your N earlier comments are on the card (now vN): <hub-review link>"); hub-review shows the block
  "Your earlier comments on this card" under the draft (under the text on other cards) and a "vN · N earlier
  comments" chip in the card head that scrolls to it. CRM: `review-api.js items()` exposes the same `iterations`,
  `current_version`, `current_after` from the dossier's versions (`comment`, `rewrite_of`) and the crm-review
  feedback lines; `review.js` shows the same block on the item's face. Box patches:
  `task-land/_system/currency/patch-hub-iterations-20261004.py` (hub) and
  `patch-hub-review-iterations-20261004.py` (page + server). Tests: `task-land/_system/test_iterations.py`.

- **The SodaPing hub (H42, 4 Oct 2026):** the Telegram header of every card reads "SodaPing hub"; a card with
  `meta.crm_url` / `meta.crm_pid` ends with "Open the CRM card" -> `CRM_PUBLIC_URL/?review=1#/today/<pid>`; /revise of
  the import card edits its Telegram message in place. Box patch `currency/patch-hub-sodaping-20261004.py`.
- **The CRM tab on hub-review (H41):** `GET /api/crm` reads the CRM review items (`CRM_ITEMS_URL`, default the laptop
  writer `http://desktop-1bojsrg:4137/review/items?coming=1`, fallback the box intake), keeps what waits for him (today's
  items with a draft, a call or a comment being worked; a later item only when iterated, commented or NOT sent), one
  line each (name, org, "NOT sent ...", "vN after your comment of <date>, waiting for your verdict", ...) linking to that
  exact CRM card. Nothing is decided on the hub. Box patch `currency/patch-hub-review-crm-20261004.py`.
- **The CRM card deep link:** `#/today/<pid>` on the CRM board (`crm-app/public/review.js`) opens review mode with that
  card current, turning "coming up" on when the person is due later this week. Base URL in ONE place per process:
  env `CRM_PUBLIC_URL` (default `https://desktop-1bojsrg.taile93f00.ts.net`, the laptop over Tailscale; after the
  writer flip set it to the box address). Test `.medtech-crm/tests/deep_link_test.py` (1568 and 390 px).

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
- **The board rule loop (goal run G99, 4 Oct 2026; RULE-LOOP.md section 7).** Ledger `task-land/_system/BOARD-CONTRACT.md`
  (`addrule.py --contract board`); skill `~/.claude/skills/board/SKILL.md` (`compile_skill.py --contract board --install`,
  laptop and box), recompiled and appended to the research workers' prompt on every run (`daily-campaign/workers.js`,
  env BOARD_SKILL overrides). His comment under a card (a / s open the box) or a category note: `board-server.js`
  `routeComment` appends it to `gtm-eng/agent/board-feedback-outbox.jsonl`, then posts hub-review `POST /api/feedback
  {surface: "gtm-board", item: <slug>/<person id>}` (retried every 5 min and on the next comment; a category note waits
  45 s for the last keystroke); the box feedback session classifies it with `ledger_verdict.py` (board ledger by
  default, email when it is about the wording) and recompiles. Live on :4141 from the server's next restart (the node
  process keeps the code it loaded; `rule_loop_check.py` shows the route amber until then). Test
  `task-land/_system/test_board_loop.py`. Observer `gtm-eng/board-observer.js`: hit lines (surface board) into `_system/rule-hits.jsonl` on every board page render (H1 keys, H2 j back / k fwd, H3 nothing he must read folded; once per board, rule, day, outcome) and every commit (H4 no confirmation card); `node board-observer.js <slug>` renders a real board read-only.

## 7. The system agent and the feedback worker

- **THE SYSTEM AGENT (built 4 Oct 2026 18:44 to 20:00; DESIGN-20261004-system-agent.md), the maintainer of the whole
  SODA SYSTEM.** `task-land/_system/system-agent/system_agent.py`, task `DA-SystemAgent` every 10 min through
  run-hidden.vbs. Its manual is THE LEDGER `soda-brain/system/nodes.json` (his word 19:13: per node the checks with
  probe, healthy_when, if_fails, known_fixes, rollback, escalate, his_command, for_him; ports, tasks, paths); the map's
  NODES are rendered from it (`soda-brain/tools/build_map.py`; edit the ledger, never the HTML block; a hand edit of
  the HTML is absorbed into the ledger at the next build). Every tick: (1) the checks moved from the GTM agent (servers,
  tasks, Gmail, calendars, LinkedIn, sync, console windows, the hub, the system audit, his system feedback), one
  read-only ssh to the box for every box probe of the ledger, `inbox.jsonl` from the GTM agent; `check --only <key>`
  runs ONE check (what a fix session reproduces and proves with); (2) the whitelist fixes (start_task, start_servers,
  li_repair, hide_task, close_own_cards, close_duplicates, disable_task), capped, 25 min apart; (3) THE REGISTRY
  `system-agent/broken.jsonl` (id, node, key, what, since, class maintenance | his_command | his_decision, owner agent |
  fix_session | him, status open | fixing | verifying | stuck | fixed | gone): a line closes only when its check passes
  twice in the agent's own ticks, or once after a fix session's own pass; a maintenance line owned by the fix session
  starts ONE fix job (`jobs.add_fix`, `job_runner.py run --job`, lane mutex `runner-fix.lock`): Opus, 30 min soft, 45
  hard kill, 1 week point read from `sim/harness/budget.py`, extended once to 2 only when progress.json shows a
  reproduction, never at 80% of the 5-hour window, never when `system-agent/OFF` exists, one per line per day, three a
  day; the never-list is enforced by the PreToolUse hook `system-agent/fix_guard.py` (fail-closed preflight); the box is
  read-only for a fix session (a box change = a laptop commit in a synced repo, or a for_him command); a cause on the
  never-list = `stuck` at once (his word 19:13). (4) A STUCK card ("STUCK on X: I did ... I need you to do exactly
  this ... YES = ... NO = ...") only after a fix session returned stuck, or for a check the LEDGER marks his_command;
  his yes is performed by `unstuck.py` (task `DA-Unstuck` every minute): auth = the sign-in page with the account
  pre-selected; terminal = "a window opens with the command pre-typed; nothing runs until you press Enter" (the one
  approved console window, recorded `his-yes` through `window-watch/expected.jsonl`); run = executed hidden, output on
  the line. (5) The drift check: a ledger task missing, a code path missing, a port listening on a node marked
  off/retired/planned/paused = node `stale-ledger` + a fix-session line `ledger:<node>`. (6) map-sync: the registry onto
  the ledger (status broken / stale-ledger, the `broken` field) and the map re-rendered, the Known-broken card
  generated. (7) `blockers.json` for the GTM agent, the heartbeat to the box (`box_watch.py` reads it), and THE ONE
  COMBINED REPORT at 09:00 and 18:15 (head "GTM: pushing today YES/NO" = the GTM agent's own section via `gtm_agent.py
  section --json`, then "SYSTEM: N broken, a for the agent, b in a fix session, c need you", decisions waiting, hub,
  AUDIT, since the last update). Shared engine `system-agent/agentlib.py`. Judge it: `system_agent.py status |
  incidents | registry [--all] | brief <id>`, `runs.jsonl`, `incidents.jsonl`, `jobs/fix-*`. Kill switch for fix
  sessions: touch `system-agent/OFF`. Tests: `system-agent/tests/` (engine replay, split, registry, fix jobs, unstuck).
- **The GTM agent (campaigns only since 4 Oct 2026).** `gtm-eng/agent/gtm_agent.py` (task GTM-Agent, every 10 min):
  campaigns, the daily board and fire, push by noon, CRM Today, contacts to find, the campaign audit (booked and never
  sent, an automatic reply naming somebody); fixes release_channel (held while `blockers.json` names that channel) and
  start_task of the campaign tasks; a non-campaign fault goes to the System Agent's `inbox.jsonl`, never a card of its
  own; it posts no report any more (its section is in the combined one). `box_watch.py` on the box posts "laptop
  silent" from the System Agent's heartbeat. `feedback_worker.py` (task DA-FeedbackWorker, DISABLED on the laptop 2026-10-04 19:19, the box
  feedback session took over: one filer) took system feedback items
  (`_system/gtm-agent/system-feedback.jsonl`, filed by `feedback_queue.py` from his sentences and by the simulation's
  learner) and fixed what was in its whitelist. **Since 4 Oct 2026 (goal run G99) it is a STUB that processes nothing**
  (old code `feedback_worker.py.bak-20261004-fold`): the box feedback session is the one processor of his sentences.
  What it alone did moved: board comments go through the board route (section 6), its `add` is
  `task-land/_system/feedback_session.py add --surface <x> --text "..."`, a system request is the session's
  `jobs.py whitelist` / `jobs.py add`. `system-feedback.jsonl` stays (CRM digest, simulation learner, savior claims).
- `due_today.py` (built 1 Oct, laptop task DA-DueToday): a promise he made ("reach back in two weeks") comes back prepared on
  its day.
- **The feedback session (hub; built, armed, OFF until the cut-over).** `task-land/_system/feedback_session.py`, box
  cron `*/5` with flock, exits while `/home/da/hub-review/no-telegram` is absent. One resumed Opus session reads the
  open hub-review `queue.jsonl` entries, splits every entry into RULES (addrule.py now) and WORK (a job, below); "big
  job: ..." is a job of size big, his words verbatim. One "told" update card per batch; log
  `_system/feedback-session.jsonl`. Turning it on: the command list in THE PLAN, RESUME item (4).
- **Big jobs (THE PLAN item 7).** `_system/jobs.py` stores one file per job (`_system/jobs/<id>.json` + `jobs.jsonl`);
  `_system/job_runner.py run` takes the oldest `queued` job, runs ONE Opus orchestrator (`claude -p`, bypassPermissions,
  specialists through the Agent tool, 90 min wall), and links each artifact with `jobs.link`, the only path to `done`;
  `needs_him` = ONE update card, the job parks until re-queued. Since 4 Oct 16:45 it runs ON THE LAPTOP: task
  `DA-JobRunner` every 5 min through `run-hidden.vbs` (no window); the mutex `_system/jobs/runner.lock` (pid,
  started_at, stale after 100 min) makes a tick exit while a job runs. The box line (`flock -n /tmp/da-job-runner.lock
  python3 .../job_runner.py run`) is for after the writer cut-over, with DA-JobRunner disabled the same minute: the two
  locks do not see each other. Status: `python _system/job_runner.py status`; log `_system/jobs/runner.log`.
- **The CRM feedback path (the CRM commit, built 4 Oct 16:50).** A commit on the CRM review board hands his sentences to
  `review-api.js digest()`, ONE Opus categorizer with four scopes: `case` (a case note on the dossier, read by the
  generator for that person), `rule` (addrule.py, or a confirmation of an existing rule), `system` (system-feedback.jsonl
  + the CRM workplan's change requests + a big job, expect document:repo), `work` (a deliverable: deck, translation,
  document, one-pager, research, "build", "prepare", "make me"; "big job:" is always work) -> `jobs.py add --surface
  crm-review --card crm-review:<pid> --person <pid>`, his words verbatim as `spec.words`, the step, the draft and the
  digest's reading as `spec.expansion`. The dossier carries `job: {id, status}`; the card says "work in progress: <id>";
  when the runner links the artifact, `jobs.link` posts `POST :4137/review/artifact {pid, job_artifact}`: the comment line
  "artifact ready: <link>", the work comment resolved, the item back to review (an artifact is never a message version,
  so it cannot be approved into a send). A person off today's board gets the one hub update card instead. Test
  `.medtech-crm/tests/work-job.test.js`.
- **The integration check (goal run, 4 Oct 2026; performance hint 18).** `task-land/_system/goal-run/integration_check.py`:
  randomized, read-only end-to-end checks across the surfaces, run by the goal orchestrator after every landed build and
  by laptop task `DA-IntegrationCheck` every 2 h from 21:00 (run-hidden.vbs, window_lint clean). Each run picks 5 of 10
  checks (seed printed; `--all`, `--seed N`, `--only a,b`, `--list`): `crm-health` (laptop :4124 proxy, box writer),
  `crm-board` (#today in headless Chrome at 1568 and 390, own user-data-dir under `~/.cache/integration-check`, every
  write answered locally), `crm-review` (calls `.medtech-crm/tools/review_board_check.py`), `hub-pending` (GET :4180),
  `hub-review-count` (box :4142), `brain-recall` (a random ledger rule's own chunk in the door's top 8), `event-dry-run`
  (a synthetic event built from a random open to-do through `todo_match.py lookup` + `event --dry`, TASKLAND = a temp
  dir, a stub judge, the real todo-match.jsonl must not grow), `window-lint`, `health-lines` (health.json,
  health-vps.json, door /health), `maps-fresh` (map "Last verified" not older than the newest LOOPS.md change once
  that change is 60 min old). A FAIL becomes a registry item `IC-<check>` (key `integration:<check>`, maintenance,
  owner agent) through `system-agent/registry.py put`: a repeat appends a newer state of the same id (fails+1), two
  passes close it (`registry_close_after_passes`). Runs: `goal-run/integration.jsonl`. Test flags `--inject-fail
  <check>` and `--registry <temp file>` (tests never write the real registry).

- **The UI walk (goal run, 4 Oct 2026; his "a walker that physically opens the places he goes to").**
  `task-land/_system/system-agent/ui_walk.py`, laptop task `DA-UIWalk` at 08:00, 11:00, 14:00, 17:00, 20:00, 23:00
  (run-hidden.vbs, window_lint clean; `register-ui-walk-task.ps1`). System Chrome headless with its own profile
  `~/.ui-walk-chrome`, at 1568 x 900 and 390 x 844 (touch): hub-review `:4142/?dry=1` (every tab found on the page, the
  Messages filter, two cards opened by `#c<id>`), CRM review mode `?review=1#/today` (board, Next / Prev, Why, Updates;
  plus `review_board_check.py`'s CHECK_JS, imported), CRM Today `#today`, on the box (writer) and on the laptop
  (replica); the Telegram chat through the hub's ledger (GET :4180/pending: every open non-silent card carries the
  Telegram message id push.js returned; no broken characters), no browser and no bot call. Read-only by construction:
  every non-GET request is answered locally and listed in the report (the review board fires POST /review/generate on
  load: blocked), /review/updates is read with ?peek=1. Checks per state: console and page errors, failed requests,
  horizontal page scroll, clipped text, a key field cut by an ellipsis, overlapping fixed bars, a floating element
  lying on a control, broken characters (U+FFFD) on screen, "loading" after 10 s, counts against the API (hub header
  and tabs vs /api/cards and /api/open-count, laptop Today badge vs the box), empty states where the API has items.
  Faults: one registry item per page `UI-<surface>-<width>` (key `ui-walk:<surface>@<width>`, maintenance, owner
  fix_session, agent when the page does not answer), a repeat updates the same id (`seen`+1), two clean walks close it
  as fixed. Screenshots and `report-HHMM.json` / `last.json` in `task-land/_system/goal-run/ui-walk/<date>/` (gitignored,
  3 days kept), log `ui-walk.log` there. Every full walk (not `--plant`) also writes the small TRACKED summary
  `system-agent/ui-walk-last.json` (run time, per page pass/fail, fault count and kinds, registry id; no screenshots,
  no page text), which the task-land sync carries to the box for the System Update (19:55). Drill: `python tests/test_ui_walk.py` (the planted page
  `tests/ui_walk_plant.html` twice into a registry copy: one item, then an update, then closed by two clean walks).
  Not covered: how Telegram itself draws a card (Telegram Web needs his one-time login in the walker's profile; PARKED,
  not asked).

- **The daily System Update and the Judge (goal run G74, G94, G95; 4 Oct 2026 19:40).**
  `task-land/_system/system-agent/system_update.py run --cron`. Runs on the LAPTOP: task `DA-SystemUpdate` daily 08:00
  (run-hidden.vbs, `--until 23`: a slot missed asleep runs at wake until 23:00; window_lint clean), box data read only
  through the synced repos and HTTP. The box line (`0 6,7,8 * * * ... run --cron`, 08:00 hour only) is PARKED for him:
  his one-liner for the laptop-asleep case, in `_system/box-steps-20261004-goal.sh`. The synced `updates.jsonl` (field
  `by` = hostname) is the cross-machine guard: a day with a posted card is only verified, never posted again;
  `updates/NO-POST-ONCE` makes the next run post nothing (a task test-start). It reads the last 24 h and 7 days: the ledger `soda-brain/system/nodes.json` (node states), the System
  Agent's `runs.jsonl` (ticks, failing checks) and `incidents.jsonl` (plus the GTM agent's history while it exists),
  the registry `broken.jsonl` (opened, closed, open by owner, open over 60 min), `decisions.jsonl` (his verdicts, the
  system's closes), `rule-hits.jsonl`, the new rules (rows of the `*-CONTRACT.md` ledgers whose id was not in git at
  the window start), `goal-run/integration.jsonl`, `goal-run/ui-walk/<date>/last.json`, `health-vps.json`, the hub's
  open count, and the fix sessions (`sessions.jsonl`, or the `sessions` lists on registry lines until it exists). It
  writes ONE page `system-agent/updates/YYYY-MM-DD.html` (light, 390 px, long lists folded) and ONE hub card kind
  `update` (head on line one, summary in `context`, page path in meta; series "system update", so hub_outdated closes
  yesterday's), plus `updates.jsonl` (the once-a-day guard). ALERT rules on rolling 24 h windows: the last window's
  fix-session count or points above the 7-window mean + 1 sd AND the window before too; or one node with a session in
  each of the last 3 windows. The ALERT rides on the card's first line, so its SodaPing is that card's one ping (H5,
  H7). `--no-post` writes the page and `YYYY-MM-DD.card.json` only; `--root DIR` runs on a fixture tree.
  THE JUDGE (`system-agent/judge.py`), WEEKLY on Sunday (scope change 19:17) inside that day's update, other days the
  line "next Judge: <date>": one Opus pass (claude CLI, `--model opus`, no tools, CREATE_NO_WINDOW, the hub_outdated.py
  shell-out) over the 7-day bundle (`system_update.week_evidence`: registry, sessions and the trend, incidents per day,
  integration runs, UI walk, sim scores `~/sim/runs/night.jsonl`, hub verdicts and closes per day, rule hits, nodes, box
  health, hub open). Verdict "no system-wide problem" or "SYSTEM-WIDE: <line>" with evidence and an action; every
  verdict a line in `judge.jsonl` (id `J-YYYYMMDD`, `held: null`), the next week's run appends `held` true/false with
  why; a SYSTEM-WIDE verdict becomes registry line `J-SW-YYYYMMDD` through `registry.put` (maintenance / fix_session,
  or his_command / him). First real verdict J-20261004: "no system-wide problem". Test
  `system-agent/tests/test_system_update.py` (fixture: both ALERTs, a stub hub on a temp port gets exactly one card, a
  stub claude, `held` filled the next Sunday). When `goal-run/ui-walk/` is absent (the box) the UI walk line comes from `ui-walk-last.json`.
  Gap: the update node is not yet in `nodes.json` (the System Agent build owns the ledger).

## 8. The rule loop

- His five sentences: "this sucks because", "I like this", "this again", a change request, "slower/faster".
- `addrule.py --contract email|hub|crm|notif|meeting|proactive|whitelist` the same turn; `compile_skill.py --install` compiles the skill;
  observers (critic, hub guard, CRM observer) write `rule-hits.jsonl`; `rule-stats.py` counts; `system-check.py`
  (09:10) writes the weekly check when the decision window is full; the box posts it. Canonical: `task-land/_system/RULE-LOOP.md`.
- Phase 2 of the brain: ledgers and hits move into `soda-brain/rules/`, every rule gets `since`, `checked_last`,
  `superseded_by`; `brain check` demotes by the number.
- **Observers on every ledger (goal-run G101 G103 G108, 4 Oct 2026 19:45 to 20:05).** Hit lines now come from the
  notif observer (box `sodanotif/notif-observer.js`: H1 each card line names who wrote, H2 a chat he already answered is
  not presented; patch `currency/patch-sodanotif-observer-20261004.py`, applied by the box 19:44), the meeting observer
  (`gtm-eng/agent/meeting_observer.py`, section 3), the whitelist observer (`whitelist_judge.observe` on every `judge()`:
  H2 block|ok, H1 ok|downgrade; `observe_commit` from `job_runner.run_whitelist`: H2 on the commit's real files, H3) and
  the proactive one (`pipeline.py pickup|ready --auto`; while paused the H1 gate's `block` is the hit). Tests:
  `test_notif_observer.py` (patch on a temp copy, the patched daemon under node), `test_meeting_observer.py`,
  `test_whitelist.py` (observer test added; hits to a temp file).
- **The fifth ledger, the WHITELIST (his rule of 4 Oct 2026 17:00, HUB H43).** *"if it's very clear what I want, and it
  doesn't really conflict much with what we've put already out there, and it doesn't need further approval ... I don't
  need an approval card. I need it to be treated more as a whitelist fix."* A system change he asks for (a hub comment,
  the hub's system box, a CRM review sentence of scope `system`) goes through ONE classifier,
  `task-land/_system/drafts/whitelist_judge.py judge`: the never list in CODE first (secret, env file, permission, send,
  deletion, login, a synced repo on the box by hand = approval card, no model call), then ONE Opus call whose prompt is the
  compiled skill `~/.claude/skills/whitelist/SKILL.md` + the HARD rules of the ledgers the request touches + his sentence;
  it answers `{whitelist, why, risk_flags[], one_line}`; any failure = approval card.
  - Entry: `jobs.py whitelist --words ... --card ... --touches ... --run-now` (the CRM path: `review-api.js addWhitelist`
    from `digest()`; the hub path: `feedback_session.py`'s session runs the same command). Whitelist = a job of kind
    `whitelist`, started at once in its own lane (`job_runner.py`, mutex `runner-wl.lock`, wall 45 min, acceptEdits with an
    allowlist and a denylist, no MCP, no Agent); not whitelist = the job held as `needs_him` + ONE approval card
    (`meta.section: "whitelist-request"`); the runner reads that card on every run: yes = queued, no = failed.
  - Proof: the session commits naming his sentence and names its check; the runner verifies the commit and its message,
    re-checks the files against `FORBIDDEN_PATH` (a hit on an unapproved job is reverted and becomes an approval card),
    then `jobs.whitelist_done` posts ONE card `kind: update`, `meta.section: "whitelist"`, text `whitelist fix: <one line>`,
    context = his words verbatim, files + commit, proof, undo. The GTM agent's own fixes that held (restarts, releases,
    re-hide) post the same card, silent (`gtm_agent.whitelist_card`).
  - The section: hub-review tab **Whitelist** (key 5, `currency/patch-hub-review-whitelist-20261004.py`, live 4 Oct
    17:20): one line per fix, click / c = the verdict box. Telegram reads `whitelist: ...` for these and `done: ...` for any
    other inform (approval-hub `updPrefix`).
  - The loop: his verdict on a line ("this needed approval", "this was fine", "never touch X on your own") is queued as
    `whitelist-verdict` and routed IN CODE by `feedback_session.whitelist_verdicts` (also any comment on a card whose
    `meta.section` is whitelist) to `whitelist_judge.file_verdict`: a like (maps to H1), a confirmation of an existing rule
    (`rule-confirmations.jsonl`), or a new row (`addrule.py --contract whitelist`); the skill recompiles at once and the next
    classifier call reads it. Ledger `task-land/_system/WHITELIST-CONTRACT.md`, map `drafts/skill-map-whitelist.json`.
  - Limits: a fix to a file outside git (the box's `hub-review/`, `approval-hub/`) cannot carry its proof, so it is never a
    whitelist fix; a job created on the box runs on the box (`run_on`), the laptop leaves it 15 min.
  - Tests: `python task-land/_system/test_whitelist.py` (6 classifier fixtures, the job end to end in a temp JOBS_DIR, the
    revert, the routing; `WL_LIVE=1` adds one live Opus call), `node --test tests/whitelist-path.test.js` in `.medtech-crm`.

- **RULE LOOPS EVERYWHERE (his ask of 4 Oct 2026 18:45; built 18:50 to 19:30).** *"I want a feedback session that
  understands: they will always understand if there are rules coming out of my feedback, what type of rules, and where
  to put them."* One template, six parts per surface (RULE-LOOP.md section 7): ledger, skill loaded by the decider, input
  box, route, observer, brain index; `task-land/_system/rule_loop_check.py --md` prints the coverage table. The route is
  ONE classifier in code, `drafts/ledger_verdict.py` (like -> LIKED row, confirmation -> `rule-confirmations.jsonl`,
  rule -> `addrule.py` in the ledger the sentence is about, case -> `rule-cases.jsonl`, system / work -> the Opus
  session), called by `feedback_session.ledger_feedback` for queue kinds `notif-feedback` and `feedback`. Inputs: the
  hub-review **Notifications** tab (key 6, every SODANOtif card of the last 48 h), Telegram `notif: <sentence>` or a
  swipe-reply on a card (the savior runs `_system/notif_feedback.py`), and `POST :4142/api/feedback {surface, item, line,
  text}` for any page (`soda-brain/system/feedback-box.js`, one script line). The SODANOtif classifier reads the compiled
  notif skill on every batch. Box side = three patch scripts in `task-land/_system/currency/` (THE PLAN item 16).
  The brain answers from the ledgers: `POST /brain/rules {topic}`, MCP `his_rules`.

## 9. Tasks and the daily page

- Code: `task-land/_system/daily-sync.ps1` + `daily-lib.ps1` (the watcher, task DailySync-Watchdog every 5 min),
  `capture.py`, `pipeline.py` (stage: created, in progress, ready for review, finished; the card decides the task),
  `surface-sweep.ps1`, `crm-bridge.ps1` (a to-do naming a person becomes that person's CRM step).
- The daily page (Obsidian, `Daily/<date>.md`) is the edit surface: ((prompt)) directives, retitle = rename, overwrite
  = replace, done items stay until the next day, three mirror lines (CRM count, hub count, daily campaign).
- **`((rule: ...))` on any line (G102, 4 Oct 2026)**: a rule for the system, not an instruction for the task. daily-sync
  collects it, `task-land/_system/rule_directive.py` files it (ledger_verdict picks the ledger it is about, addrule writes
  his words verbatim), the line's task is untouched, a rule-only line creates no task; `directive: rule` in daily-sync.log.
- **Quick Claude `rule:` (G104, 4 Oct 2026)**: a Quick Claude message starting `rule:` is filed the same way
  (`--surface quick-claude`): in code by `~/.claude/quick-claude/run.ps1` (the dictated runner, also what the voice lane
  spawns), by the panel's workspace CLAUDE.md in an interactive window.

## 10. Notifications and voice

- `/home/da/sodanotif/` (systemd `da-sodanotif`, pollers every 60 s): Gmail, Slack, WhatsApp taps and the LinkedIn
  store, classified by `routing-prompt.md` and `NOTIF-CONTRACT.md`, pushed as Telegram cards; CDTM group mail never,
  noreply never, groups never.
- Observer (G101, 4 Oct 2026): `notif-observer.js` writes `rule-hits.jsonl` lines, surface `notif`, on every rendered card
  (H1 sender on every line, H2 per WhatsApp card) and on every batch the answered() filter thins (H2 `block`). Hits reach
  the laptop through the task-land sync.
- Voice: short notes on the laptop (`.claude/voice-lane`), long recordings on the Drive mount transcribed on the box
  (`da-voice.timer`, faster-whisper) and routed by the safe-word prompt.
- **The janitor's ledger (G106, 4 Oct 2026)**: `task-land/_system/CLEANING-CONTRACT.md` (his cleaning rules, out of
  the janitor workplan), compiled to `skills/cleaning`, read by `hub_outdated.py`'s judge on every call (ledger rows when
  the skill is not on that machine); a line on the hub-review Cleaning tab = kind feedback, surface cleaning ->
  ledger_verdict (box patch `currency/patch-hub-review-cleaning-20261004.py`).
- **A spoken rule enters the feedback queue (G100, 4 Oct 2026)**: a sentence he says is a rule ("Rule: ...", "regola:
  ...") in a voice review (`task-land/_system/voice/voice_review.py`, result.json `rules`) or in a phone recording (box
  lane `vps/voice-longform-vps.py`, before the classifier) goes through `rule_directive.queue` to hub-review
  `POST /api/feedback` (kind feedback, surface voice) and the feedback session files it; refused = filed at once.

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
- Drawn in `SODA-SIMULATION-MAP.html` (+ `.md`, 4 Oct 2026): the sandbox, every real component's twin and its
  fidelity, the arms A to D and guards G1 to G5, the judge's metrics and their weaknesses, nights 1 to 3 over time.
  Night 3 (4 Oct, brain arm B, 17 days, 14 scored): event score 71.3, hub surface 53 falling as stale Today rows pile
  up, the brain closed 0 cards and ticked 1 to-do; arm A on the same two days scored the same.
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
- `due_today.py` runs as the laptop task DA-DueToday; the meeting loop's open-loops change is designed, not built.
- Hub hygiene scored 32/100 in the simulation: cards stay open after he did the thing or the event passed.
- The LinkedIn accept tick and `li_restore.py` "needs you" cards: the sign-in window must be opened by the system first.
- The box's contacts sync and the sodano23 Gmail token are expired (FINDINGS-20261001.md); the 23:00 digest's Telegram
  send fails with HTTP 400.
