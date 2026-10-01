# HANDOFF 2026-09-28 (evening): the system agent, what is open

Written right before he compacts. READ THIS FIRST after the compaction, then the memory files named at the bottom.
Workplan: `~/gtm-eng/WORKPLAN-20260928-gtm-agent.md`. Everything listed under "Done" is built and verified today.

## 1. The deal on DKIM (his words: "me doing dkim then you doing something in return once im done")

- HE sets up DKIM for tundrahealth.ai (Google Admin console: Apps > Google Workspace > Gmail > Authenticate email,
  generate the key, add the TXT record `google._domainkey` at the DNS host, then "Start authentication").
- WHEN HE SAYS IT IS DONE, I do, in this order:
  1. Verify it: `nslookup -type=txt google._domainkey.tundrahealth.ai`, plus SPF and `_dmarc`; send one test mail to
     his own address and read the headers (`dkim=pass`). Say what is missing (DMARC record) if anything.
  2. Raise the email cap in the send ledger: `task-land/_system/outreach/ledger.py DEFAULT_CAPS["email"]` and the
     `caps` inside `ledger.json` (today 30 a day, 150 per 7 days; a session chose those numbers on 24 Sep, he never
     did). ASK HIM THE NUMBER, propose a ramp (for example 50 a day, 250 a week, then more after a week of clean
     delivery). Google's own limit is 2,000 a day.
  3. Release the queue (see 2).
- His words on the queue: "put all of them in the queue ready to go when we fix."

## 2. The queue to build BEFORE he is done (NOT built yet)

Today's daily campaign (`boards/daily-2026-09-28`, 10 people, already written into the CRM and Notion at 17:59) has
NO plan: `campaign.py plan` was refused by the ledger ("LEDGER REFUSED email 2026-09-30 1"). To do:
- make the plan exist with its steps scheduled but NOT booked (`booked` false), so the tick's own cap check defers
  them day by day ("deferred: email cap full") and they go by themselves the moment there is room or the cap rises.
  Read `cmd_plan` in `~/gtm-eng/campaign.py` around the `ledger_cmd("plan", ...)` call; there is a `--force` flag.
- same for every later daily board that gets refused: the agent's incident `daily:ledger-refused` must queue, not
  only tell him.
- the 18:00 US invites of us-campaign-100 failed while LinkedIn was logged out (Kelvin Knight, Jennifer Denault and
  maybe more, see `task-land/_system/window-watch/task-logs/US-Campaign-Daily.log`): check that they are rescheduled.

## 3. Three things he says the system should have caught (28 Sep evening). State of each

| What he said | What I found | Done | Still to do |
|---|---|---|---|
| "two emails from americans, unavailable but giving us a new direction ... we should reach out to those mentioning the first" | Automatic replies on tundra: Henry Stankiewicz (sigma-hc.com, retired, names Kenny Colavito and Kelsey Patel), 28 Sep; Corey Bialkowski (UMich, out until 4 Oct, names CE-ManagementTeam@med.umich.edu), 28 Sep; older: Holly Crawford (UT Southwestern, left, names Dinah.Middleton@UTSouthwestern.edu), Tim Bowers (VCU, names Tyler.Quinn@vcuhealth.org for biomed), 24 Sep | nothing | Check whether the event loop surfaced them (rule CRM H30 says a mailbox naming a successor is a referral): `~/.medtech-crm/events-ledger.jsonl`, `MAIL_NOISE` in `crm-app/monitor.js` may be dropping "Automatic reply". Then: the named person goes into the CRM as a new person with origin "referred by <first person>'s automatic reply", a first mail is drafted that mentions the first person, shown to him as a card. Addresses given in the reply are his to use; a name without an address (Kenny Colavito, Kelsey Patel) needs the address found and SMTP-checked (email rule H63) |
| "an automatic invitation on my calendar from one of the outreach - she clicked on the link. its as if she answered, stop campaign/pause" | Anna Candiani booked "30 min with Alessandro" for Tue 6 Oct 19:00 through his booking link, with anna.candiani@ieo.it; on the board she is anna.candiani@cardiologicomonzino.it (privati-nord) | Her remaining step cancelled; Monzino colleagues (2 steps) and IEO colleagues (2 steps: Silvio Capizzi, Silvia Oldazzi) paused until 7 Oct | Build it into the engine: `reply_sweep` in campaign.py must also read the calendars (tundra and cdtm) for events "Booked by <name> <email>" and match by NAME as well as address. Write the meeting and her second address on her CRM row |
| "valeria ingrosso ask better be in crm" | Her mail of 28 Sep asks for a document to prepare a deeper meeting with Humanitas clinical engineering. The CRM step is only "answer Valeria (email)" | nothing | Put the ask on her row: step "send Valeria the document she asked for, to prepare the meeting with Humanitas clinical engineering (email)", her words in the origin; rule H87 (name the deliverable we owe) applies |

## 4. Done today and running (do not rebuild)

- System agent: `~/gtm-eng/agent/gtm_agent.py`, task GTM-Agent every 10 min, updates 09:00 and 18:15, box fallback
  `task-land/_system/gtm-agent/box_watch.py`. Memory `reference_system_agent`.
- LinkedIn: launcher no longer kills other servers; automatic restore of a quarantined session (`li_restore.py`);
  engine skips a tick with no network. Memory `reference_linkedin_launcher_reaper`.
- No console windows: recorder + lint + `run-hidden.vbs`. Memory `reference_window_watch`.
- CRM review: full screen; a/s/c held until commit with x; digest sorts each sentence; three groups; snooze; keys act
  on the card on screen. Memory `reference_review_staged_commit`.
- Contact search for people with no channel (`channel-search.js`). Memory `reference_channel_search`.
- Event page Confirmed button (box, `~/research-page`). Memory `reference_event_confirm`.
- Tundra signature added by gmail.py itself on both machines. Memory `feedback_tundra_signature_always`.
- Campaign engine: a failure stops a channel not a board, retries, `Overslept` guard, reply sweep at every tick,
  forward detection (rule CRM H39). GSD: Emanuele Galbiati cancelled (call Thu 1 Oct 9:30, invite verified on the
  tundra calendar), Brunella Bellotti handed over, Zucchi paused 7 days, 14 grupposandonato.it people paused until
  Fri 2 Oct. San Raffaele (hsr.it) NOT paused: he has not said.
- Calendar helper: no bare account chooser, renewal opens on the right account. Tundra calendar renewed today and
  copied to the box.

## 5. Open system changes (not built)

1. Rule CRM H40: a reply that proposes an exact slot, free on his calendar = invite + short reply prepared as ONE
   decision; after his yes, check the invite went out before the reply is sent.
2. The search for a deliverable we owe (Nevio Boscariol's document; rule email H87): when a person's history says
   we promised something, find it in his notes, mail and Drive before writing the follow-up.
   BUILT 2026-09-29 for task-land to-dos: `~/.medtech-crm/crm-app/owed.js` feeds the reader and the review generator
   (memory `reference_owed_todos_in_crm_prompts`). Mail and Drive promises not captured as a to-do are still unread.
3. Amos (Trieste): still no contact found; his WhatsApp chat is not in the local copy. The WhatsApp daemon should
   pull the history of a chat on demand.
4. Event mode: detect by itself that he is at an event, read his Telegram messages about it, watch notes he never
   confirms, check proposed slots against the calendar.
5. Tokens: copy a renewed authorisation to the other machine automatically; find out WHY they die. He has to look at
   Google Cloud console > OAuth consent screen > Publishing status (Testing = authorisations can expire after 7
   days; In production fixes it). Dead today: gmail alesoda2002 and sodano23 on the laptop (the box's alesoda2002
   was renewed by the savior today), contacts-alesoda2002.
6. The snooze of a skipped card lives in the review only: the CRM Today count still counts the person.
7. task-land sync: `merge=union` for the append-only logs.
8. Unknown senders: 192 of 237 events in 3 days come from people not in the CRM: no policy yet.
9. The unattended to-do worker: not built, needs his yes and a scope.
10. Per-board 17:15 campaign reports are now redundant with the agent's 18:15 update (7 cards a day): ask him.

## 6. His standing constraints that bit today

- Nothing is sent to a person without his verdict; a committed batch is the yes; pausing is always allowed.
- Never touch a file inside a synced repo on the box by hand (I deleted box_watch.py that way today).
- Never open a console window; every scheduled task through `run-hidden.vbs`.
- A sentence from a review is never filed with addrule.py directly any more: it goes through the commit digest.
- Interactive sign-in: trigger it myself with the account pre-selected.

## 7. Memory to read

`reference_system_agent`, `reference_review_staged_commit`, `reference_channel_search`, `reference_event_confirm`,
`reference_linkedin_launcher_reaper`, `reference_window_watch`, `feedback_tundra_signature_always`,
`feedback_never_touch_synced_repo_on_box_by_hand`, `reference_daily_campaign`, `feedback_commit_batch_is_the_yes`.

## 8. The domain's mail records, read 2026-09-28 19:00

- DNS host: GoDaddy (ns07/ns08.domaincontrol.com). The DKIM TXT record goes there.
- `google._domainkey.tundrahealth.ai`: does not exist. DKIM is not set up.
- `_dmarc.tundrahealth.ai`: `v=DMARC1; p=quarantine; adkim=r; aspf=r; rua=mailto:dmarc_rua@onsecureserver.net`.
  The policy already tells receivers to put failing mail in spam, and without DKIM every mail depends on SPF alone.
  This is the reason to do DKIM before raising any cap.
- SPF: `v=spf1 include:dc-aa8e722993._spfm.tundrahealth.ai ~all` (GoDaddy's managed record). Check that the
  include contains `_spf.google.com`; if it does not, mail sent through Google fails SPF too and, with the
  quarantine policy, goes to spam. Result of that check is in the reply I gave him right after this handoff.

## 9. Progress after the handoff was written (28 Sep, 20:55). This section wins over sections 2 and 3

DONE
- Wake-up guard for LinkedIn: no network = LinkedIn is not touched (send engine, inbox poller, CRM acceptance check,
  li_restore); after a gap of more than 25 min the engine has the session verified by `li_restore.py` before the
  first LinkedIn step; the agent runs the same check at its first run after a wake. Proof file
  `~/.linkedin-mcp/verified.json`, marker `~/gtm-eng/.wake.json`.
- Item 1, the queue: `campaign.py plan` no longer dies when the ledger refuses a day, those steps stay scheduled and
  unbooked. `boards/daily-2026-09-28` is planned: 10 first emails, 2 on 29 Sep, 8 on 1 Oct.
- Automatic replies were being recorded as REAL replies by the mail tick (against CRM H30); with today's reply
  sweep that would have cancelled the person and paused the hospital. Fixed in `crm-app/monitor.js` (`MAIL_AUTO`,
  `applyAutoReply`, an automatic reply that names somebody is `p.referral`), and 5 rows corrected (backup
  `crm.json.bak-20260928-autoreply`): Tim Bowers, Holly Crawford, Corey Bialkowski, Henry Stankiewicz as referrals,
  Micki Robertson as a plain automatic reply.

NEXT, in this order
1. Item 2, the referral outreach. The people named: Dinah.Middleton@UTSouthwestern.edu (by Holly Crawford, thread
   1a0d5c65624c6f88), Tyler.Quinn@vcuhealth.org for biomed (by Tim Bowers, thread 1a0d5780cfac02a8),
   CE-ManagementTeam@med.umich.edu (by Corey Bialkowski, thread 1a0e8da3e36b08fb; a team mailbox, and Corey is only
   away until 4 Oct: ask him whether to write to the team or wait for Corey), Kenny Colavito and Kelsey Patel at
   Sigma Health Consulting (by Henry Stankiewicz, thread 1a0e8ecce8973dfa; no addresses given: find them, SMTP-check
   them with gtm-eng/tools/smtpcheck.py, email rule H63). For each: a new person in the CRM through
   `POST :4137/intake` with the origin "named by <X>'s automatic reply", then a draft that is the mail X received
   plus one sentence saying X's automatic reply named them, through the draft lane (gmail.py draft, sidecar,
   register.py = one hub card each). Load the `drafting` skill first. Set `p.referral.handled` when done.
2. Item 3, Valeria Ingrosso's ask on her CRM row.
3. Item 4, calendar bookings caught by the engine (match by name as well as address); Anna Candiani's meeting and
   her IEO address on her row.
4. Item 5, the failed 18:00 US invites of us-campaign-100.
5. The DKIM deal (section 1) when he says it is done.

## 10. Progress 29 Sep, 15:00. This section wins over section 9

DONE
- Item 2, referrals: three drafts on hub cards, nothing sent. #9 Tyler Quinn (VCU, named by Tim Bowers), #10 Kenneth
  Colavito (Sigma, named by Henry Stankiewicz; address found, SMTP valid), #11 Dinah Middleton (UT Southwestern, she is
  in Communications: the draft asks who now looks after equipment spend). All three are in the CRM. Corey Bialkowski:
  nothing written to the team mailbox, waiting for his answer. Script `~/hubrev-work/referrals/referral_drafts.py`.
- Item 3: Valeria Ingrosso's row carries the document she asked for (`deliverable_owed`, step due 30 Sep).
- Item 4: `campaign.py reply_sweep` case 3, a meeting on his calendar with somebody of a board (address OR full name)
  stops the person, pauses the hospital, writes the meeting on the CRM row. Test `agent/tests/test_calendar_booking.py`.
  Anna Candiani's row has the meeting and her ieo.it address.
- Item 5: the failed invites were NOT rescheduled, 20 people (25 and 28 Sep). Two causes fixed: `ledger.py` counted a
  plan of a past day for ever (`counts()`), and `us-campaign-100/daily.py` only read today's file (`carry_over()`,
  runs at every 18:00 run, leaves out anybody who replied, `--carry-dry` to look).
- "SODANOtif missed earlier" card (asked by the savior): `~/.claude/sodanotif/recap.ps1` skips a chat he answered,
  re-attaches the sender from the source, title "not shown to you before". Test `test-recap-restore.ps1`.

OPEN, new
- The CRM server (:4124) does not answer while a monitor tick runs (ticks of 40 to 205 s on 29 Sep): the ticks run in
  the server's own process. They belong in a child process.
- The laptop had 349 MB of free memory at 14:50: 19 claude processes, two of them headless and stale (pid 20456 since
  21 Sep, pid 15252 since 28 Sep 17:56). His call to close them.
- Signature: student-voice mails from the tundra account get the founder signature (email H68 against H88). His call.
- recap.ps1 and watch.ps1 classify with Haiku; his rule says Haiku never. His call.
- Slack: one workspace answers invalid_auth / admin_deactivated_account.
- The critic added "(e.g. Nuvolo)" to a mail for a hospital nobody checked runs Nuvolo (removed by hand on card #9).
- The DKIM deal (section 1) when he says it is done.

## 11. Progress 29 Sep, 21:00. This section wins over section 10

DONE
- MEETING LOOP (CRM H41, his ask of 29 Sep): `gtm-eng/agent/meeting_loop.py`, task DA-MeetingLoop every 5 min. A call that
  ended (Notion meeting notes) = event on the CRM row + ONE hub card with the next step. Memory `reference_meeting_loop`.
  First two cards: Luigi Intrieri (San Raffaele), Sebastiano Caravaggi (#19). Bug of the first day: Sebastiano's call was
  written on Luigi's row (calendar window too wide), moved and fixed, test `agent/tests/test_meeting_match.py`.
- LINKEDIN SELF-HEAL, second round. The session was set aside at 18:05 on 28 AND 29 Sep and nothing put it back. Fixed:
  `li_restore.py` exit 2 only when LinkedIn refuses twice (exit 4 = no answer, retried); the agent ignores an old exit 2
  once the session was verified, and repairs whenever a quarantine folder is newer than `verified.json`; `daily.py`
  checks and restores before sending and once more mid-run, and session errors are never anomalies on his card;
  heartbeat on the box carries `linkedin: {down, down_since, verified_at, last_restore, needs_him}`; the savior's
  `box_linkedin_watch.py` is the safety net (card only past 60 min with a fresh heartbeat).
  US-Campaign-Daily moved from 18:00 to 18:15: Peer60-AcceptCheck-1800 started on LinkedIn at the same minute.
  Evening of 29 Sep: session restored, 9 of 10 notes of the day sent.

OPEN, new
- After his yes on a meeting card the step is set; the mail or the invite is not drafted by the loop yet (asked him).
- The meeting loop cannot prove its delay: Notion does not say when a call ended.
- Model starts take minutes when the laptop is short of memory; the loop belongs on the box in the long run.
- Whether 18:15 ends the 18:05 quarantine is to be read in `~/.linkedin-mcp/` on 30 Sep (no new invalid-state folder).

## 12. Progress 29 Sep, 21:45. This section wins over section 11

DONE
- Hub H17: a card the system believes outdated is CLOSED by the system (judgement moot, confidence 60 or more, drafts
  included, the Gmail draft untouched), never shown as "probably outdated"; a doubt stays a normal card.
  `task-land/_system/hub_outdated.py` (edited on the laptop, the sync carries it to the box); the review page no longer
  has the "Probably outdated" group.
- hub-review (box, `/home/da/hub-review`, backups `.bak-20260929-agent`): tab "GTM agent" next to "To decide". The
  agent's report is shown in sections, every line numbered (C1, C2 ... for campaigns), click or j/k + c to comment,
  voice works on the lines, nothing to approve. Comments go out with the commit: Telegram message to the savior
  (block GTM AGENT), `queue.jsonl` (kind agent-feedback) and one line each in `decisions.jsonl` (surface gtm-agent).
  The agent's report cards no longer count in "Hub cards still open".
- Agent: alerts kept in the outbox during an outage are posted once per incident, only while it is open, and their id
  is kept (16 stale duplicate alerts of 28 Sep closed by hand).

BLOCKED, HIS DECISION
- `gtm-eng/agent/feedback_worker.py` is written and its sorter tested (case / rule / system), but NOT scheduled:
  Claude Code's permission check refused to register an unattended session with full permissions. Until he decides,
  a comment typed on a review surface is recorded and carried to the savior, not fixed by itself.

## 13. 29 Sep, 22:15
- The agent has an AUDIT check (`check_audit` in gtm_agent.py, memory reference_system_agent): stale or double alert
  cards of its own (closed by itself), double cards, drafts closed without a word while still unsent in Gmail,
  referrals not acted on, sends booked and never sent, meeting loop blind. Section AUDIT in both daily reports.
  First live result: 5 drafts closed by a closed tab and still in Gmail (Sebastian Geigenberger, Martina Andellini,
  Tyler Quinn, Kenneth Colavito, Dinah Middleton); 34 sends booked on 25 and 28 Sep that never went; card
  "coattio: box edits collided" open twice (#9, #1). Waiting for his word on the five drafts.

## 14. 29 Sep, 22:50: his review comments now get fixed (his ruling of tonight)
- Order: 1 a live session (the savior hands it over or does it on the box); 2 laptop off: the box part now, the rest
  when the laptop is back; 3 nobody in 45 min: unattended worker on the laptop, full permissions, as the safety.
- Queue: `task-land/_system/gtm-agent/feedback_queue.py` (items written by the laptop, events appended by anybody,
  both files merge=union). Worker: `gtm-eng/agent/feedback_worker.py`, task DA-FeedbackWorker every 10 min (registered
  22:48, first real pass not yet seen). Savior told the protocol (claim / done / needs-him / release).
- hub-review: third tab "Updates" (cards with nothing to decide, comment per line), keys 1/2/3 switch tabs, a card
  fits one screen at 100% (header measured, text box sized, reviewer's note folded to two lines).

## 15. 29 Sep, 23:50: follow-ups after the calls (his complaint: not proactive)
- Drafts on cards, nothing sent: #24 UPMC (Scot Stevens + Kevin Marraccini, Cc Pat Cronin, Laurie, Caleb; signed
  Alessandro and Caleb; ATTACHMENT still to add by him, the deck and the pilot proposal are in Downloads), #25 Kevin
  alone (deep dive + who owns lifecycle decisions), #26 Luigi Intrieri (Italian, tu; says the invite for Tue 6 Oct
  11:00 was sent: CREATE THE INVITE FIRST on his yes: `python triage/gcal.py invite --account tundra --summary "Tundra
  <> San Raffaele - follow-up (Luigi Intrieri, Luca)" --start 2026-10-06T11:00 --end 2026-10-06T11:30 --tz Europe/Rome
  --to intrieri.luigi@hsr.it --meet --notify all --confirmed`).
- meeting_loop.py now: the reading returns the follow-up mail and the invite; the mail goes through the lane (own
  card), the invite is created on his yes to the meeting card; a calendar call with an outside attendee and no notes
  gets a card, his sentence on it becomes the draft (`calendar_ended`, `cal_only_verdicts`). Not yet seen on a real
  call: the next call is the test. Memory feedback_after_a_call_prepare_the_followup.
- UCSF: no inbound mail asking for material was found in tundra or cdtm (only his own mails to Ramana Sastry and
  Alexis Dracker, and a LinkedIn thread with Ramana of 17 Sep). Ask him where that email is.

## 16. 30 Sep, 00:40: inbound asks (his test on Ramana Sastry's mail)
- `gtm-eng/agent/inbound_asks.py`, task DA-InboundAsks every 15 min: an inbound mail (tundra, cdtm) whose newest
  message asks something is judged by Opus; the ask goes on the CRM row (`deliverable_owed`, step), the reply is
  drafted through the lane (own card). Ramana's mail of 29 Sep: card #5 of 30 Sep (confirm the two points, the site
  link; the pitch he attaches himself). Root causes: the sender was not in the CRM ("unmatched", dropped) and nobody
  read what a mail asks. The CRM did not answer during the test (laptop at 189 MB free): row write pending.
- Savior reports H42: a handoff card asked him to decide a step the monitor had already marked step_done_outside
  (Luigi Intrieri, 22:21 UTC); the judge's event counter frozen at 2557. Not looked at yet.
- Luigi: he answered Luigi himself at 21:16 UTC; card #26 (my draft) is superseded, reconcile.py handles it.

## 17. 30 Sep, 00:55: FIRST THINGS TOMORROW
1. task-land sync parked on the laptop since 23:21: `_system/hub_outdated.py` was edited on the laptop (H17) AND on the
   box by the savior (the degraded-run guard); the sync is pushing HEAD to `conflict-laptop` and git has been packing
   for 30 min at 189 MB free. Resolve by merging (never rebase): keep BOTH changes in hub_outdated.py, then let
   git-sync.ps1 run. The mutex holder is pid 21244 if it is still there. Laptop is behind 41 commits.
2. The unattended feedback worker did its first fix by itself at 22:54-23:10: `crm-app/owed.js` (open to-dos naming a
   CRM person are read by the review generator and the reader), backups `.bak-20260929-feedback`; the laptop's :4137
   and :4124 run the old code until restarted (Stop-Process + Start-ScheduledTask Coattio-Watchdog).
3. handoff-api.js cardStage: skip a person with an outbound or step_done_outside after the meeting (CRM H42).
4. Laptop memory: his call on the stale sessions; every failure of tonight sits on it.

## 18. START HERE after the compaction of 30 Sep, 12:00 (this section wins over all above)

State: everything of sections 10-17 is built and running (tasks GTM-Agent, DA-MeetingLoop, DA-FeedbackWorker,
DA-InboundAsks; hub-review with tabs To decide / GTM agent / Updates). Done this morning: the LinkedIn DM to Annika
Kaalep (card #29, his yes) was sent at 11:57.

Do these, in this order, without asking him:
1. task-land sync: check `git status -sb` and the tail of `_system/git-sync.log`. If still parked, merge by hand
   (merge, never rebase): `_system/hub_outdated.py` must keep BOTH the laptop's H17 change (CLOSE_CONFIDENCE 60, drafts
   closed too, the "1b" sweep of cards flagged by the old rule) and the box's degraded-run guard (mail_events returns
   (ev, failed), DEGRADATO log, no close when an account was unreadable; box commit 11671050a).
2. Restart the laptop's CRM servers so they load the worker's `crm-app/owed.js` wiring (Stop-Process on the listeners
   of :4124 and :4137, then Start-ScheduledTask Coattio-Watchdog; takes up to 40 s).
3. CRM H42: `~/.medtech-crm/handoff-api.js` cardStage must also skip a person with an outbound event or a
   `step_done_outside` after the meeting (a card asked him to decide what he had already done with Luigi Intrieri).
4. The CRM server blocks while its monitor ticks run (minutes when memory is short): move the ticks to a child
   process. Same root for the Notion read timeouts.
5. Write Ramana Sastry's row (inbound_asks left `crm_pending`): person + deliverable owed + step.
6. Read the first real results of the three new loops: `meeting_loop.py status`, `inbound_asks.py status`,
   `feedback_worker.py status`, `tests/run_audit_live.py`; fix what they show.

Waiting on HIM (say it once, do not nag):
- the five drafts closed without a word (Sebastian Geigenberger, Martina Andellini, Tyler Quinn, Kenneth Colavito,
  Dinah Middleton): which he rejected;
- cards #24 UPMC, #25 Kevin Marraccini (attachment his), #5 of 30 Sep Ramana Sastry (pitch his);
- the PoC document for Nevio (ARIS), overdue since 25 Sep;
- laptop memory (189 MB free on 29 Sep night; stale pids 20456 and 15252);
- DKIM: when he says done, section 1;
- signature for student-voice mails from tundra (H68 against H88); Haiku in the notification classifier; Slack
  workspace deactivated; whether a meeting card's yes should also send the draft.
- 12:02: item 1 of section 18 is DONE: the sync recovered by itself in the morning (main level with origin/main), and
  `_system/hub_outdated.py` holds both changes and compiles. Start from item 2.
- 30 Sep 14:10: LinkedIn. The savior relayed his voice order (13:57) for a DM to Annika Kaalep ("5 minutes late"); it
  went at 14:07 after two failures: two restores ran in the same second and half-copied the profile (WinError 145 /
  183), LinkedIn refused that copy, the older copy of 29 Sep was accepted. `li_restore.py` now takes a lock
  (`~/.linkedin-mcp/restore.lock`) and tries the older set-aside copies before saying he has to sign in (backup
  `.bak-20260930-lock`). Still open: the heartbeat's `needs_him` is only as fresh as the agent's last pass; this
  session's own linkedin-mcp server holds the profile while connected, which is what collided with the engine's send:
  a session sends through ONE path, never both.

## 2026-09-30 · the agent can be dead for an hour and nothing says so (OPEN)

Two false "needs you" cards reached his phone (#35 calendar:tundra, #36 calendar:cdtm, created
67 ms apart at 15:11:43Z). Nothing was expired: `gcal.py whoami --account tundra` answered on
both machines. The same 15:09 pass had also logged `Gmail account tundra does not answer:
...connected party did not properly respond after a period of time...` — WSAETIMEDOUT. The
laptop lost its route to Google for a moment and all four probes fell together. The Gmail branch
reported that honestly and raised nothing; the calendar branch turned it into "his authorisation
expired", `needs_him=True`, no `min_runs`.

FIXED on the laptop the same evening: the calendar branch now shares the Gmail branch's
`AUTH_DEAD` regex, quotes the real output when the credential is not dead, and carries
`needs_him=dead` / `min_runs=1 if dead else 2`. Plus the part that mattered and was not in the
spec: the probe result is cached for `gmail_probe_min` (30 min), so `min_runs=2` alone would
have been met from the cache without ever re-probing. A failed probe that is not a dead
authorisation now clears `g["at"]`, so two REAL probes have to fail. Backup
`gtm_agent.py.bak-20260930-calendar`.

STILL OPEN, and the reason the cards sat there: **the agent did not complete a single run
between 15:09:16Z and 16:19:16Z.** The task was not stuck (Ready at 18:18 local, last result
0x41306 SCHED_S_TASK_TERMINATED, no process alive) and the laptop was awake and in use the whole
hour. `runs.jsonl` has no entry for that hour, `agent.log` is 0 bytes since 28 Sep, and the Task
Scheduler operational log returned no events for GTM-Agent — so there is no history to read. It
recovered by itself on the next pass.

The box's own net caught nothing: `box_watch.py` logged the growing silence every ten minutes
(`10 min old`, `30`, `60`, `70`) and said `nothing to do` each time, because its rule wants
business hours AND sends still due. The distinction worth building on, from the laptop session
that investigated: **a stale heartbeat with a laptop that ANSWERS is a different state from a
laptop that is off** — the second is the normal evening, the first is the agent being dead while
the machine is fine. Changing that rule is his call; asked on Telegram 2026-09-30, unanswered.
Whoever picks this up: `agent.log` being 0 bytes for two days is itself the reason the hour
cannot be explained, and is probably the first thing to fix.

## 2026-10-01 · the connectivity gate (AGREED, NOT BUILT) and the gcal mislabel (box done)

Four false "needs you" cards reached his phone in 24 hours and he said so plainly: "you cannot
tell me this every time that the freaking internet is down on my laptop."

All four are one bug wearing four coats: **the laptop cannot reach something, and reports that
something as broken.**

- LinkedIn down 122 minutes (really 2; my `mktime` bug, fixed, see
  [[reference_box_utc_timestamps_mktime_trap]]).
- `calendar:tundra` + `calendar:cdtm`, 67 ms apart, "its authorisation expired". It was a
  WSAETIMEDOUT on the laptop; the same pass also failed both Gmail probes. Branch fixed.
- `port:4142` plus "the hub's open cards cannot be read". The box answered 200 in 9 ms on the
  Tailscale IP throughout; the laptop could not reach it for ~20 minutes.
- `cdtm calendar cannot be read ... NameResolutionError ... Run: gcal.py auth --account cdtm`.
  The laptop had no DNS. His authorisation was fine, and the box read BOTH calendars while the
  card was open.

**The fix agreed with the laptop session, and NOT yet built.** Patching each branch does not close
the class. One connectivity probe at the top of `gtm_agent.py`'s run, deliberately **not** against
Google (Google being down must stay reportable). If it fails: one finding, "the laptop has no
network", `needs_him=False`, `min_runs=2`, and **every external probe skipped for that pass**.
Gmail, calendars, LinkedIn, the box ports and the hub read are all void when the machine is blind;
reporting them is four wrong stories instead of one true one. The per-branch handling stays as the
fallback for when connectivity is fine and one service really is down.

The threshold at which a sustained laptop outage becomes something he SEES is a `CFG` value and is
**left empty until he answers**. Asked on Telegram 2026-10-01 12:0x; my suggestion to him was
nothing under thirty minutes, and beyond that a card that says plainly it is the laptop's network
and not his data. Unanswered at the time of writing.

**Done on the box, still owed on the laptop:** `triage/gcal.py` now separates the two failures
(`gcal.py.bak-20261001-refresh`). `RefreshError` says the consent really is dead and gives the
`phone_auth.py --kind calendar` line; `TransportError` says "NETWORK FAILURE reaching Google ...
This is NOT an authorisation problem and no login will fix it. The token is untouched." The
no-refresh-token branch no longer calls `run_local_server` on a non-interactive run, which on a
headless box opened nothing and just hung. Verified: google-auth wraps `requests` exceptions into
`TransportError` (read the source), the two exception classes are siblings so the `except` order
holds, and both branches were exercised against a throwaway token dir.

**Who owes what.** The laptop session that agreed to this (TTT Thesis round 2) was closed by him
before it could start; it says the gate and the laptop `gcal.py` copy are in its memory for "the
next session today". Both files are already in `_system/box-tools/triage/` and pushed
(commit a5dd1ea91), so the next laptop session only has to copy them across and write the gate.
**If this is still open tomorrow, it has been dropped** — exactly like the three artefacts promised
on 25 September (`rule-stats.py`, the Brain section, the recall entry point), none of which existed
five days later.
