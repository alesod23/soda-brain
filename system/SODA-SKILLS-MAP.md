# SODA SKILLS MAP: every skill, as it is tonight

The visual page is [SODA-SKILLS-MAP.html](file:///C:/Users/Alessandro/soda-brain/system/SODA-SKILLS-MAP.html); this file is the same content as Markdown links,
for Obsidian or any viewer. Built 4 Oct 2026 22:25 from the live files. See also [SODA-SYSTEM-MAP.md](file:///C:/Users/Alessandro/soda-brain/system/SODA-SYSTEM-MAP.md).

8 compiled skills, 2 ledgers read without a compiled skill, 24 hand-written skills.
Coverage (rule_loop_check.py --md): G green 77, A amber 16, R red 11 of 104 cells (+ 4 n/a: no such part by nature, reason in the cell).

## Read this first

1. **Read it.** Open a skill's `SKILL.md` (installed copy, or the mirror in task-land: same file).
2. **Say what is wrong.** One sentence where you see the thing it made (the "your input" line of each surface), or on Telegram. It is filed into the right ledger the same turn; you never edit a skill or a ledger.
3. **See which rule produced a line.** Every rule in a compiled skill ends with a tag like `[ledger H12]`: row H12 of its ledger, your sentence, dated and verbatim.

The file links open on the laptop only; on claude.ai they do not open.

## The rule loop

You say what is wrong once. That sentence is filed the same turn into the ledger it is about, in your words, with the date. A small map says which of your sentences belong together; the compiler turns ledger and map into one screen, with an example in your voice for each rule, and installs it. The code that makes the thing reads that screen on every call. Afterwards an observer checks what was made against the same rules and writes one line per check; those counts go back into the next compile, so what still goes wrong stays in front and what never fires steps back.

1. **You say it**: One sentence, anywhere: Telegram, a card comment, a box on a page, ((rule: ...)) on the daily page, the CRM row.
2. **addrule.py files it**: The same turn, into the ledger the sentence is ABOUT (you never pick it). [addrule.py](file:///C:/Users/Alessandro/task-land/_system/drafts/addrule.py)
3. **The ledger**: Your words, dated, verbatim, never edited: one row H<n> per sentence. `<SURFACE>-CONTRACT.md` [_system/](file:///C:/Users/Alessandro/task-land/_system/)
4. **The skill map**: Which ledger rows merge into which rule, the group, one example in your voice. `drafts/skill-map-<surface>.json`
5. **compile_skill.py**: Turns ledger + map + hit counts into one screen; checks itself; writes nothing if a check fails. [compile_skill.py](file:///C:/Users/Alessandro/task-land/_system/drafts/compile_skill.py)
6. **The compiled skill**: Up to 15 rules in front, each tagged [ledger H<n>]; the rest under "Assumed". Three copies: installed, mirrored in task-land, on the box. `~/.claude/skills/<name>/SKILL.md`
7. **Who loads it**: The code that decides, on every call (named in the skill's first line), or a session about to do that kind of work.
8. **The observer**: Checks each thing made against the rules after the fact; one line per check in rule-hits.jsonl. Never edits, never blocks. [rule-hits.jsonl](file:///C:/Users/Alessandro/task-land/_system/rule-hits.jsonl)

Back to step 5: the hit counts decide what stays in front; a rule with no hit in its last 50 checked cases sinks to "Assumed" (still checked, back in front the moment it fires). A "like" becomes the example of the rule it fits.

Sources: [RULE-LOOP.md](file:///C:/Users/Alessandro/task-land/_system/RULE-LOOP.md) (section 7 is the template) · [rule_loop_check.py](file:///C:/Users/Alessandro/task-land/_system/rule_loop_check.py) · [compile_skill.py](file:///C:/Users/Alessandro/task-land/_system/drafts/compile_skill.py) · [addrule.py](file:///C:/Users/Alessandro/task-land/_system/drafts/addrule.py)

## The 8 compiled skills

### Messages to a person (compiled)

READ THIS BEFORE WRITING ANY MESSAGE TO A PERSON - email, WhatsApp, LinkedIn DM, in any language, from any account. It is the compiled form of the rule file that governs how Alessandro's messages are written and of how a new rule gets added the moment he gives one. Use when drafting or revising outreach or follow-up, when he says "draft", "scrivi a", "rispondi a", "mandagli", when reviewing a draft, and whenever he gives feedback on something you wrote.

- Ledger: [EMAIL-REVIEW-CONTRACT.md](file:///C:/Users/Alessandro/task-land/_system/EMAIL-REVIEW-CONTRACT.md) · 95 rules · newest row H103, 2026-10-04
- Skill: [drafting/SKILL.md (installed)](file:///C:/Users/Alessandro/.claude/skills/drafting/SKILL.md) · [mirror in task-land](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/drafting/SKILL.md) · box `/home/da/.claude/skills/drafting/SKILL.md` · compiled 2026-10-03 (skill_v 2026-10-03a); 15 rules in front, compiled from 81 ledger rules; 44 [ledger H..] tags; 14 ledger rows newer than this compile, not in the skill yet
- Map: [skill-map-email.json](file:///C:/Users/Alessandro/task-land/_system/drafts/skill-map-email.json) · compile with `python task-land/_system/drafts/compile_skill.py --contract email --install`
- Loaded by: every session before it writes a message to a person (email, WhatsApp, LinkedIn); the draft critic reads the ledger itself; the event-page Confirmed worker reads it too
- Observer: 741 lines, 314 of them a hit (not "ok"); last line 4 Oct 19:37
- R1 as it reads in the skill: "Italian cold outreach (email AND LinkedIn note) never greets by first name. Open with 'Salve' or 'Gentile' (never 'Buongiorno': time-dependent) plus title and SURNAME: 'Ing. <Cognome>' for an engineer, 'Dott. <Cognome>' / 'Dott.ssa <Cognome>' for a graduate/doctor, 'Prof.' when it applies; no ..." `[ledger H64]`
- Coverage (email (drafts)): ledger G, skill G, box G, route G, observer G, brain G
- Your input: On the CRM review, a / s / c on the message (the reason box), or one sentence on Telegram or in a session: filed into this ledger the same turn.

### The CRM (compiled)

READ THIS BEFORE WRITING TO THE CRM (a person, a next step, a note) and, for the reader, BEFORE DECIDING A PERSON'S NEXT STEP. Compiled from CRM-CONTRACT.md.

- Ledger: [CRM-CONTRACT.md](file:///C:/Users/Alessandro/task-land/_system/CRM-CONTRACT.md) · 57 rules · newest row H57, 2026-10-04
- Skill: [crm/SKILL.md (installed)](file:///C:/Users/Alessandro/.claude/skills/crm/SKILL.md) · [mirror in task-land](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/crm/SKILL.md) · box `/home/da/.claude/skills/crm/SKILL.md` · compiled 2026-10-04 (skill_v 2026-10-04a); 15 rules in front, compiled from 54 ledger rules; 50 [ledger H..] tags; 3 ledger rows newer than this compile, not in the skill yet
- Map: [skill-map-crm.json](file:///C:/Users/Alessandro/task-land/_system/drafts/skill-map-crm.json) · compile with `python task-land/_system/drafts/compile_skill.py --contract crm --install`
- Loaded by: review-api.js (the CRM reader, before it decides a next step) and every session before it writes to the CRM; the event-page Confirmed worker
- Observer: 11,721 lines, 5,346 of them a hit (not "ok"); last line 4 Oct 22:20
- R1 as it reads in the skill: "A draft produced from the person panel (ask box) is a real Gmail draft, never only text in the panel's Draft tab; if the person has a thread, the draft is a reply in that thread. "this clealry doesnt work btw, i dont have that email drafted.... it should be a response, too."" `[ledger H25]`
- Coverage (CRM review + Ask box): ledger G, skill G, box G, route G, observer G, brain G
- Your input: On the CRM row, a / s / r / c or the Ask box; or say it on Telegram: filed the same turn.

### Hub cards (the Ping hub) (compiled)

READ THIS BEFORE POSTING ANY CARD to the Ping hub (POST 127.0.0.1:4180/pending) or acting on his verdict. Compiled from HUB-CARD-CONTRACT.md.

- Ledger: [HUB-CARD-CONTRACT.md](file:///C:/Users/Alessandro/task-land/_system/HUB-CARD-CONTRACT.md) · 59 rules · newest row H59, 2026-10-04
- Skill: [hub/SKILL.md (installed)](file:///C:/Users/Alessandro/.claude/skills/hub/SKILL.md) · [mirror in task-land](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/hub/SKILL.md) · box `/home/da/.claude/skills/hub/SKILL.md` · compiled 2026-10-04 (skill_v 2026-10-04a); 15 rules in front, compiled from 57 ledger rules; 45 [ledger H..] tags; 2 ledger rows newer than this compile, not in the skill yet
- Map: [skill-map-hub.json](file:///C:/Users/Alessandro/task-land/_system/drafts/skill-map-hub.json) · compile with `python task-land/_system/drafts/compile_skill.py --contract hub --install`
- Loaded by: every session before it posts a card to the hub (127.0.0.1:4180); the hub guard checks hub-rules.json
- Observer: 624 lines, 255 of them a hit (not "ok"); last line 4 Oct 22:20
- R1 as it reads in the skill: "Every new event (a message or email he sent, a reply that arrived, a meeting that happened) is checked against the open cards: a card whose proposal that event makes moot is closed or marked outdated the same run, never left open. "the moment that new event went out (the moment I sent that ..." `[ledger H15]`
- Coverage (hub cards): ledger G, skill G, box G, route G, observer G, brain G
- Your input: The comment box under any verdict on hub-review, or a reply to the card: filed the same turn.

### What the system picks up on its own (compiled)

READ THIS BEFORE PICKING UP A TO-DO ON YOUR OWN (pipeline.py pickup --auto), while doing it, and before handing it back (pipeline.py ready --auto). Compiled from PROACTIVE-CONTRACT.md.

- Ledger: [PROACTIVE-CONTRACT.md](file:///C:/Users/Alessandro/task-land/_system/PROACTIVE-CONTRACT.md) · 24 rules · newest row H24, 2026-10-04
- Skill: [proactive/SKILL.md (installed)](file:///C:/Users/Alessandro/.claude/skills/proactive/SKILL.md) · [mirror in task-land](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/proactive/SKILL.md) · box `/home/da/.claude/skills/proactive/SKILL.md` · compiled 2026-10-04 (skill_v 2026-10-04a); 15 rules in front, compiled from 24 ledger rules; 21 [ledger H..] tags
- Map: [skill-map-proactive.json](file:///C:/Users/Alessandro/task-land/_system/drafts/skill-map-proactive.json) · compile with `python task-land/_system/drafts/compile_skill.py --contract proactive --install`
- Loaded by: pipeline.py (pickup --auto / ready --auto), proactive_todo.decide on every call, and the daily page decider (Resolve-TaskDirective)
- Observer: 3 lines, 2 of them a hit (not "ok"); last line 4 Oct 21:09
- R1 as it reads in the skill: "Proactive pickups are live: the 3 Oct pause until the Tuesday reset (H1) was lifted on 4 Oct 20:48 (H24), so on every to-do the system can do it does the work on its own, unattended, on a schedule, until it is ready for his review. The gate is still AUTO_PAUSED_UNTIL in pipeline.py: pickup ..." `[ledger H1,H24]`
- Coverage (proactive (to-do pickup)): ledger G, skill G, box A, route A, observer G, brain G
- Coverage (proactive-todo (to-dos from an ask he accepted, G118)): ledger G, skill G, box G, route G, observer A, brain G
- Coverage (daily page + to-do lines): ledger G, skill G, box G, route G, observer G, brain G
- Your input: A comment on the hub card of the picked-up task, or ((rule: ...)) on any line of the daily page: filed the same turn.

### What reaches your phone unasked (compiled)

READ THIS BEFORE DECIDING WHAT REACHES HIS PHONE UNASKED (a SODANOtif card, the recap, the missed-earlier block, a done-notification) and before writing one. Loaded by the SODANOtif classifier (box sodanotif/daemon.js) on every batch. Compiled from NOTIF-CONTRACT.md.

- Ledger: [NOTIF-CONTRACT.md](file:///C:/Users/Alessandro/task-land/_system/NOTIF-CONTRACT.md) · 6 rules · newest row H6, 2026-10-04
- Skill: [notif/SKILL.md (installed)](file:///C:/Users/Alessandro/.claude/skills/notif/SKILL.md) · [mirror in task-land](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/notif/SKILL.md) · box `/home/da/.claude/skills/notif/SKILL.md` · compiled 2026-10-04 (skill_v 2026-10-04a); 4 rules in front, compiled from 5 ledger rules; 5 [ledger H..] tags; 1 ledger row newer than this compile, not in the skill yet
- Map: [skill-map-notif.json](file:///C:/Users/Alessandro/task-land/_system/drafts/skill-map-notif.json) · compile with `python task-land/_system/drafts/compile_skill.py --contract notif --install`
- Loaded by: the SODANOtif classifier on the box (sodanotif/daemon.js, buildSystemPrompt) on every batch
- Observer: 8 lines, 1 of them a hit (not "ok"); last line 4 Oct 22:10
- R1 as it reads in the skill: "Every line of a card names who wrote it (and the group, for a group) before the snippet. e.g. "Caleb: are you taking over the hotel in Orlando?" then "Rocco /GG SMOM Torino: ...", never a bare snippet" `[ledger H1]`
- Coverage (notifications (SODANOtif)): ledger G, skill G, box A, route G, observer G, brain G
- Your input: On Telegram, a message starting notif: (or a quote-reply to the card): filed the same turn.

### Fixes made without asking (compiled)

READ THIS BEFORE DECIDING WHETHER A SYSTEM CHANGE HE ASKED FOR IS MADE AT ONCE (a whitelist fix, no approval card) OR BECOMES AN APPROVAL CARD, and before reporting a whitelist fix. Loaded by drafts/whitelist_judge.py on every call. Compiled from WHITELIST-CONTRACT.md.

- Ledger: [WHITELIST-CONTRACT.md](file:///C:/Users/Alessandro/task-land/_system/WHITELIST-CONTRACT.md) · 3 rules · newest row H3, 2026-10-04
- Skill: [whitelist/SKILL.md (installed)](file:///C:/Users/Alessandro/.claude/skills/whitelist/SKILL.md) · [mirror in task-land](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/whitelist/SKILL.md) · box `/home/da/.claude/skills/whitelist/SKILL.md` · compiled 2026-10-04 (skill_v 2026-10-04a); 3 rules in front, compiled from 3 ledger rules; 3 [ledger H..] tags
- Map: [skill-map-whitelist.json](file:///C:/Users/Alessandro/task-land/_system/drafts/skill-map-whitelist.json) · compile with `python task-land/_system/drafts/compile_skill.py --contract whitelist --install`
- Loaded by: drafts/whitelist_judge.py on every call (made at once, or an approval card)
- Observer: 6 lines, 2 of them a hit (not "ok"); last line 4 Oct 21:01
- R1 as it reads in the skill: "A system change he asks for is made at once, with no approval card, only when the request is clear and specific, conflicts with no filed rule (read the ledgers of the surfaces it touches) and needs nothing from him. Otherwise it is an approval card. e.g. "put the CRM review count in the hub ..." `[ledger H1]`
- Coverage (whitelist fixes): ledger G, skill G, box G, route G, observer G, brain G
- Your input: The verdict box on the Whitelist tab of hub-review ("this needed approval", "this was fine"): filed the same turn.

### GTM boards (compiled)

READ THIS BEFORE PUTTING PEOPLE ON A GTM BOARD, PROPOSING A CHANNEL OR A SEQUENCE FOR SOMEONE ON IT, OR CHANGING HOW A BOARD (:4141, board-page.html) SHOWS AND COMMITS. Loaded by the daily-campaign research workers (gtm-eng/daily-campaign/workers.js) on every run. Compiled from BOARD-CONTRACT.md.

- Ledger: [BOARD-CONTRACT.md](file:///C:/Users/Alessandro/task-land/_system/BOARD-CONTRACT.md) · 4 rules · newest row H4, 2026-09-16
- Skill: [board/SKILL.md (installed)](file:///C:/Users/Alessandro/.claude/skills/board/SKILL.md) · [mirror in task-land](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/board/SKILL.md) · box `/home/da/.claude/skills/board/SKILL.md` · compiled 2026-10-04 (skill_v 2026-10-04a); 4 rules in front, compiled from 4 ledger rules; 4 [ledger H..] tags
- Map: [skill-map-board.json](file:///C:/Users/Alessandro/task-land/_system/drafts/skill-map-board.json) · compile with `python task-land/_system/drafts/compile_skill.py --contract board --install`
- Loaded by: the daily-campaign research workers (gtm-eng/daily-campaign/workers.js) on every run
- Observer: 3 lines, 0 of them a hit (not "ok"); last line 4 Oct 20:13
- R1 as it reads in the skill: "Every board is keyboard-drivable with a visible legend: a ready, s skip (both advance), e edit, Esc out of the box. e.g. 60 people on peer-60: a mouse trip per card is the whole cost of the review" `[ledger H1; memory feedback_review_pages_need_keyboard_shortcuts]`
- Coverage (GTM boards (s/c boxes)): ledger G, skill G, box G, route A, observer G, brain G
- Your input: The comment box under a board card (a / s / c, "why skip?"): filed the same turn.

### Cleanup (the janitor) (compiled)

READ THIS BEFORE TICKING, CLOSING, ARCHIVING, MERGING OR REWORDING AN ITEM ON ITS OWN (a to-do, a sub-item, a hub card, a CRM step, a Gmail draft, a Notion review row) and before proposing a cleanup. Loaded by hub_outdated.py's judge on every call. Compiled from CLEANING-CONTRACT.md.

- Ledger: [CLEANING-CONTRACT.md](file:///C:/Users/Alessandro/task-land/_system/CLEANING-CONTRACT.md) · 7 rules · newest row H7, 2026-10-03
- Skill: [cleaning/SKILL.md (installed)](file:///C:/Users/Alessandro/.claude/skills/cleaning/SKILL.md) · [mirror in task-land](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/cleaning/SKILL.md) · box `/home/da/.claude/skills/cleaning/SKILL.md` · compiled 2026-10-04 (skill_v 2026-10-04a); 7 rules in front, compiled from 7 ledger rules; 7 [ledger H..] tags
- Map: [skill-map-cleaning.json](file:///C:/Users/Alessandro/task-land/_system/drafts/skill-map-cleaning.json) · compile with `python task-land/_system/drafts/compile_skill.py --contract cleaning --install`
- Loaded by: hub_outdated.py's judge on every call (before it ticks, closes, merges or rewords an item on its own)
- Observer: no line in rule-hits.jsonl yet
- R1 as it reads in the skill: "Tick a sub-item the moment evidence exists (an email reply, a calendar event) and move a date the evidence moved; a tick backed by evidence needs no approval. e.g. the notary answered on the share capital: the sub-item is ticked; the appointment moved to Mon 5 Oct 16:00 on the calendar: the date ..." `[ledger H1]`
- Coverage (cleaning (janitor)): ledger G, skill G, box G, route A, observer A, brain G
- Your input: The box next to each line of the Cleaning tab on hub-review: filed the same turn.

## Read directly from the ledger

### Meeting notes into steps (ledger only, no skill)

Meeting notes (the Notion meeting AI page) turned into steps: what the meeting loop asks of each transcript and the steps it proposes.

- Ledger: [MEETING-CONTRACT.md](file:///C:/Users/Alessandro/task-land/_system/MEETING-CONTRACT.md) · 8 rules · newest row H8, 2026-09-29
- Skill: none, the decider reads the ledger itself
- Map: none (nothing is compiled for this surface)
- Loaded by: gtm-eng/agent/meeting_loop.py reads the ledger itself on every run (no compiled skill)
- Observer: 8 lines, 0 of them a hit (not "ok"); last line 4 Oct 19:56
- Coverage (meeting notes): ledger G, skill G, box A, route A, observer G, brain G
- Your input: A comment on the hub card the meeting loop produces, or one sentence on Telegram: filed the same turn.

### Trips (trippy) (ledger, skill hand-written)

How a trip is searched and judged: modes, layovers, overnights, departure times, comfort against price. preferences.json stays the engine's own store.

- Ledger: [TRIPPY-CONTRACT.md](file:///C:/Users/Alessandro/task-land/_system/TRIPPY-CONTRACT.md) · 21 rules · newest row H21 (no date on the row)
- Skill: [trippy/SKILL.md (installed)](file:///C:/Users/Alessandro/.claude/skills/trippy/SKILL.md) · [mirror in task-land](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/trippy/SKILL.md) · box `/home/da/.claude/skills/trippy/SKILL.md` · hand-written, 598 lines, no [ledger H..] tags
- Map: none (nothing is compiled for this surface)
- Loaded by: the trip worker reads the ledger and preferences.json; the trippy skill itself is hand-written
- Observer: 8 lines, 3 of them a hit (not "ok"); last line 4 Oct 21:03
- Coverage (trippy boards): ledger G, skill G, box G, route G, observer A, brain G
- Your input: A comment on a rule on the trip board, or a context duel: filed the same turn.

## The 24 hand-written skills

No ledger behind them: a session loads one when your ask matches its first line.

- **add-logos** (174 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/add-logos/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/add-logos/SKILL.md) · box `/home/da/.claude/skills/add-logos/SKILL.md`. Search the web for company logos, download them as local files, remove their backgrounds, and save the results into the logos folder. Optionally wire them into an HTML file. Use when the user says "/add-logos", "add logos", "download logos", "get company ...
- **ahk** (115 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/ahk/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/ahk/SKILL.md) · box `/home/da/.claude/skills/ahk/SKILL.md`. Create AutoHotkey scripts and save them to the user's AHK folder. Use when user says "/ahk", "create a shortcut", "make a hotkey", "write an AHK script", or describes an automation they want bound to a key.
- **cdtm** (64 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/cdtm/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/cdtm/SKILL.md) · box `/home/da/.claude/skills/cdtm/SKILL.md`. CDTM kickoff-taskforce assistant for Alessandro (onboarding captain). ALWAYS reads `~/cdtm-taskforce/_START-HERE.md` then `progress.json` first to get fully current, then works a workload. Use when the user invokes `/cdtm`, says "cdtm", "kickoff ...
- **design-sync** (41 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/design-sync/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/design-sync/SKILL.md) · box `/home/da/.claude/skills/design-sync/SKILL.md`. Keep Claude Design projects in step between teammates through the tundra-design GitHub repo: set up a new teammate's machine, add or share a project, run the end-of-day sync (fresh mirror, 3-way merge of the other person's pages into yours, push via ...
- **fede** (566 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/fede/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/fede/SKILL.md) · box `/home/da/.claude/skills/fede/SKILL.md`. Vendor-neutral AI building coach for beginners, operators, and AI-built prototypes. Use when a user is new to AI coding, has workflow ideas, has a localhost or "works on my machine" app from Cursor, Claude, Codex, Replit, Lovable, Bolt, or similar, and ...
- **floom** (67 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/floom/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/floom/SKILL.md) · box `/home/da/.claude/skills/floom/SKILL.md`. Run and manage Floom AI workers — background automations that run on a schedule or trigger. Use when the user wants to set up recurring work (triage inbox, draft follow-ups, screen candidates, publish content) or asks about Floom workers, loops, or runs.
- **langfuse-bananza** (69 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/langfuse-bananza/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/langfuse-bananza/SKILL.md) · box `/home/da/.claude/skills/langfuse-bananza/SKILL.md`. Launch the Langfuse autonomous optimizer loop on an instrumented script - self-paced, one full iteration per fire, writes REPORT.md when converged. Usage /langfuse-bananza <path to script> [RUN_NAME] or just /langfuse-bananza to be asked for the target. ...
- **linkedin-outreach** (167 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/linkedin-outreach/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/linkedin-outreach/SKILL.md) · box `/home/da/.claude/skills/linkedin-outreach/SKILL.md`. Write Alessandro's 1:1 outreach messages (LinkedIn notes and DMs, and short cold emails) and optionally send them. Covers all three of his outreach jobs - peer/mentor outreach to founders and ecosystem people, sales outreach to hospitals, and ...
- **opinion-research** (101 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/opinion-research/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/opinion-research/SKILL.md) · box `/home/da/.claude/skills/opinion-research/SKILL.md`. Build a navigable corpus of practitioner stories on any topic — pain stories, solution-tried stories, raw opinion artifacts — by dispatching parallel sweeps across Reddit, niche blogs, vendor case studies, Show HN, GitHub. Outputs a single filterable HTML ...
- **overnight** (40 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/overnight/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/overnight/SKILL.md) · box `/home/da/.claude/skills/overnight/SKILL.md`. Run a long/unattended agent task reliably — per-item checkpointing, an independent verifier loop, a hard token cap with circuit breaker, auth-work quarantine, fail-loud gates, and an honest report. Use for overnight batches, enrichment, audits, sweeps, or ...
- **prod-feedback** (70 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/prod-feedback/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/prod-feedback/SKILL.md) · box `/home/da/.claude/skills/prod-feedback/SKILL.md`. Turn a product or demo observation into feedback Caleb can act on, in Alessandro's fixed three-heading format, with the screenshot attached. Use whenever he says to send product feedback, demo feedback or a bug to Caleb, or hands over a screenshot of ...
- **sde** (73 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/sde/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/sde/SKILL.md) · box `/home/da/.claude/skills/sde/SKILL.md`. SDE curriculum source — mark one of Alessandro's own Claude-Code-built tools as a source for his software-engineering learning curriculum. Mines BOTH the project's handmade source code AND the Claude Code build-session transcript, classifies every excerpt ...
- **slack** (134 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/slack/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/slack/SKILL.md) · box `/home/da/.claude/skills/slack/SKILL.md`. Read Slack DMs/mentions and send Slack messages across cdtm + xplore workspaces via the local helper at C:\Users\Alessandro\.claude\slack\. Use when user says "check Slack", "Slack triage", "what came in on Slack", "send Slack to X", "DM X on Slack", ...
- **snm** (116 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/snm/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/snm/SKILL.md) · box `/home/da/.claude/skills/snm/SKILL.md`. Signal-to-Noise Maximizer — quick access to the every-20-min inbox actionable feed (Gmail cdtm+lobbly, WhatsApp DMs+groups, Slack cdtm+xplore). Reads `~/.claude/snm-receiver/state.json` populated by the background scan (`scan.ps1` via Task Scheduler ...
- **telegram-switch** (99 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/telegram-switch/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/telegram-switch/SKILL.md) · box `/home/da/.claude/skills/telegram-switch/SKILL.md`. Move the Telegram-facing daemons (tg-bridge @Soda2402_bot, sodanotif card pusher) between the laptop and the DA VPS. Usage /telegram-switch laptop or /telegram-switch vps. No QR or re-auth ever - bots are tokens; the only rule is ONE listener per bot, so ...
- **todo** (43 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/todo/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/todo/SKILL.md) · box `/home/da/.claude/skills/todo/SKILL.md`. Work Alessandro's to-dos through the pipeline: created -> in progress (picked up by AI) -> ready for review (a hub card, linked from the daily page) -> finished. Use when he says "/todo", "work my to-dos", "pick up my to-dos", "do what you can on my list", ...
- **tovps** (75 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/tovps/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/tovps/SKILL.md) · box `/home/da/.claude/skills/tovps/SKILL.md`. Migrate THE CURRENT Claude Code session from the laptop to the DA VPS so work continues there (phone-reachable via /rc) with the laptop off. Copies this session's transcript to the box, resumes it in tmux with a handoff prompt, and verifies it answered. ...
- **triage** (545 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/triage/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/triage/SKILL.md) · box `/home/da/.claude/skills/triage/SKILL.md`. Unified inbox triage across Gmail (cdtm + lobbly via C:\Users\Alessandro\triage\gmail.py), WhatsApp DMs + groups (via the wa-daemon at C:\Users\Alessandro\.claude\wa-daemon\), AND Slack DMs + @-mentions + recent channel activity for cdtm + xplore (via ...
- **trippy-old** (476 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/trippy-old/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/trippy-old/SKILL.md) · box `/home/da/.claude/skills/trippy-old/SKILL.md`. SUPERSEDED — the original one-shot travel sweep, formerly called /trippy. Its deliverable is a standalone cooked-trips HTML in OneDrive; it has NO persistent trip boards, NO context duels and NO preference wiki. Do NOT use it for new travel searches — use ...
- **trippy** (598 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/trippy/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/trippy/SKILL.md) · box `/home/da/.claude/skills/trippy/SKILL.md`. THE CURRENT TRIPPY. Deep multi-modal travel search (flights, trains, buses, ferries, rideshare) with learned effort allocation — persistent per-trip boards served by a local webapp, pairwise context duels that feed a big search, and a cross-trip preference ...
- **wa-search** (95 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/wa-search/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/wa-search/SKILL.md) · box `/home/da/.claude/skills/wa-search/SKILL.md`. Paraphrase / semantic search over WhatsApp message history. Dumps a chat's messages chronologically so the model can reason over them — finds topics even when the user's keyword isn't in the literal text. Use when user says "what did X say about Y", "find ...
- **wa** (201 lines): [installed](file:///C:/Users/Alessandro/.claude/skills/wa/SKILL.md) · [mirror](file:///C:/Users/Alessandro/task-land/_system/laptop-tools/skills/wa/SKILL.md) · box `/home/da/.claude/skills/wa/SKILL.md`. Send and read WhatsApp via two locally-linked Baileys devices. Use when user says "send WhatsApp to X", "WA triage", "what came in on WA", "message X on WhatsApp", or any WhatsApp send/read task.
- **people-search** (box only, not installed on the laptop): [box copy mirrored in task-land](file:///C:/Users/Alessandro/task-land/_system/box-tools/skills/people-search/SKILL.md) · box `/home/da/.claude/skills/people-search/SKILL.md`. Find and rank professional people for recruiting, partnerships, sales, or research from user-provided data, public web sources, an authenticated search session, or a connected provider. Use for people discovery, LinkedIn or Sales Navigator search design, ...
- **tundra-poc-deck** (box only, not installed on the laptop): [box copy mirrored in task-land](file:///C:/Users/Alessandro/task-land/_system/box-tools/skills/tundra-poc-deck/SKILL.md) · box `/home/da/.claude/skills/tundra-poc-deck/SKILL.md`. Rebuild the generic hospital PoC proposal PDF from a Claude Design export of the Tundra pitch deck, and version that export in the Tundra Shared Drive. Use when Alessandro supplies a new "Tundra Pitch Deck" .zip exported from Claude Design, or asks to ...

Box copies checked over ssh at 22:20 on 4 Oct: the eight compiled skills on the box are byte-identical (md5) to the laptop's and the mirror's; the box also has people-search and tundra-poc-deck, which the laptop does not.
