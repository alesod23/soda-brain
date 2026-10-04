# AUDIT 2026-10-04: where he gives feedback, and where the system does not learn from it

His ask, 4 Oct 2026 18:45: *"Do a check and tell me where else am I not applying this and should apply this. Where else
should I have a system like this replicate to the loop system that we have created? So that it can learn from me, but
it's currently not happening."* Written 19:20 to 19:40 by the laptop session that built the template.

The template (six parts per surface) is `task-land/_system/RULE-LOOP.md` section 7. The table is the output of
`python task-land/_system/rule_loop_check.py --md` at 19:35, evidence per cell; rerun it, never copy it forward.
G = present, A = built but unproven or partial, R = missing. Box code is read from its mirror (`_system/box-tools/`) or
the 18:17 fixture (`_system/test_fixtures/hub-review-20261004/`), so the notification row turns green on skill and box
once the savior applies the patches and the mirror refreshes.

## The checklist (surface x six parts)

| surface | ledger | skill | box | route | observer | brain |
|---|---|---|---|---|---|---|
| email (drafts) | G EMAIL-REVIEW-CONTRACT.md | G skills/drafting + critic reads the ledger | G CRM review a/s/c on the message | G review-api.js digest -> addrule | G 737 lines in rule-hits.jsonl | G *-CONTRACT.md glob in brain_index.py |
| hub cards | G HUB-CARD-CONTRACT.md | G skills/hub + guard reads hub-rules.json | G hub-review comment box on every verdict | G queue.jsonl -> feedback_session.py | G 606 lines in rule-hits.jsonl | G *-CONTRACT.md glob in brain_index.py |
| CRM review + Ask box | G CRM-CONTRACT.md | G skills/crm read by review-api.js | G review a/s/r/c + Ask box on the row | G review-api.js digest() | G 11690 lines in rule-hits.jsonl | G *-CONTRACT.md glob in brain_index.py |
| notifications (SODANOtif) | G NOTIF-CONTRACT.md | A compiled; daemon.js loads it after the box patch | A Telegram notif: live; tab after the box patch | G notif-feedback -> ledger_verdict | R not yet: no observer, 0 hits logged | G *-CONTRACT.md glob in brain_index.py |
| meeting notes | G MEETING-CONTRACT.md | G meeting_loop.py reads the ledger directly | A only through the hub card it produces | A via the hub queue, ledger picked by the session | R not yet: no observer, 0 hits logged | G *-CONTRACT.md glob in brain_index.py |
| proactive (to-do pickup) | G PROACTIVE-CONTRACT.md | G skills/proactive, pipeline.py | A the hub card of the picked-up task | A via the hub queue | A pipeline.py writes hits, 0 hits logged | G *-CONTRACT.md glob in brain_index.py |
| whitelist fixes | G WHITELIST-CONTRACT.md | G whitelist_judge.py loads it | G Whitelist tab verdict box | G whitelist-verdict -> whitelist_judge | R not yet: judge writes no hit line, 0 hits logged | G *-CONTRACT.md glob in brain_index.py |
| GTM boards (s/c boxes) | R no board ledger; comments feed hub/crm/email by hand | R none | G board-page.html a/s/c | A feedback_worker.py: system fixes, no ledger | R none | R decisions only, not indexed |
| daily page + to-do lines | A PROACTIVE covers pickup only | A skills/todo is hand-written | A ((prompt)) on a line = an instruction, never a rule | R no route from the page to a ledger | R none | A todo items indexed, his rules on the page are not |
| system + simulation maps | R none | R none | R not yet: feedback box -> /api/feedback | G kind feedback -> ledger_verdict | R review_map.py checks layout, not his rules | A the .md narrative is indexed, the .html is not |
| simulation reports | R none | R none | R no box on a report | A route exists, no box posts to it | R none | R not indexed |
| Quick Claude panel | R none | R none | A free chat | R a session files by hand, if it remembers | R none | R none |
| event pages | A CRM ledger by default | R none | R Confirmed button, no reason text | A route exists, no box | R none | R none |
| trippy boards | A own preference wiki, not a contract | A hand-written skill | G context duels | A own engine, not addrule | A own rule engine | R not indexed |
| GTM agent / Updates / Cleaning tabs | A janitor log in a workplan | R none | G comment per line | A agent-feedback -> session, no class | A cleaning_eval.py | R none |
| voice review | R none | R none | G POST /api/voice | R audio saved, never transcribed into the queue | R none | R none |

G green 37, A amber 24, R red 35 of 96 cells.

How much he uses each surface (`decisions.jsonl`, all time): hub 358, GTM boards 122, CRM review 26, GTM agent tab 1,
CRM Updates 1. Observer hits (`rule-hits.jsonl`): crm 11690, email 737, hub 606; every other surface 0.

## Top findings: where he is not learned from today

1. **GTM boards, his second busiest surface (122 verdicts with reasons), have no ledger.** His s/c sentences go to
   `gtm-eng/agent/feedback_worker.py`, which makes system fixes and files no rule: "never pick radiology chiefs for a
   pilot" is acted on once and forgotten. Two processors read review comments (feedback_worker.py and
   feedback_session.py) with no shared classifier.
2. **Notifications had a ledger and no loop**: 5 rules, all filed by hand, none read by the classifier (it loaded only
   the /triage skill). Fixed in this pass, see "Built".
3. **The daily page has no feedback path.** `((prompt))` is an instruction for one task, never a rule; "stop putting X
   on my Today" lives only in a session's memory, if one hears it.
4. **Only three observers have ever logged a hit** (crm, email, hub). Proactive, whitelist, meeting and notif rules are
   filed and compiled, but nothing scores the artifacts against them, so the compile cannot promote or demote by number.
5. **Event pages**: Confirmed carries out the next steps but takes no reason text; "wrong person to meet" never
   becomes a CRM rule.
6. **Quick Claude**: free chat; a rule given there is filed only if that session remembers the rule loop.
7. **Voice review**: the audio is stored and never transcribed into the queue; spoken feedback is lost to the rules.
8. **Simulation reports and the two maps**: no box on a report; the maps get one with a single include line (below).
9. **Trippy** learns on its own (preferences.json, rule-feedback.jsonl, duels) but outside the ledgers and the brain:
   recall cannot answer "what does he like when he travels".
10. **The GTM agent, Updates and Cleaning tabs** reach the queue (kind agent-feedback) but go to the Opus session
    without the like / confirmation / rule / case split; the janitor's rules still live in a workplan.

## Built in this pass (laptop, committed; the box parts are patch scripts the savior runs)

- **The template**: RULE-LOOP.md section 7; `task-land/_system/rule_loop_check.py` (the table above).
- **The generic route**: `task-land/_system/drafts/ledger_verdict.py`, ONE Opus classifier (like | confirmation | rule |
  case | system | work; the ledger chosen by what the sentence is about). `feedback_session.ledger_feedback` routes
  queue kinds `notif-feedback` and `feedback` through it in code, recompiles the touched skill, hands system / work to
  the session with `classified` set. A new surface = one line in `LEDGER_ROUTES` + one in `SURFACE_LEDGER`.
- **The notification loop, five parts of six**: compiled skill `~/.claude/skills/notif/SKILL.md`
  (`drafts/skill-map-notif.json`, `compile_skill.py --contract notif`); SODANOtif reads it on every batch and records
  each card's id and Telegram message id (`currency/patch-sodanotif-notifloop-20261004.py`); the Notifications tab on
  hub-review (key 6, every card of the last 48 h, a one-line box) and `POST /api/feedback`
  (`currency/patch-hub-review-notif-20261004.py`; the tab bar also stops overflowing a phone); Telegram
  `notif: <sentence>` or a swipe-reply on a card through `task-land/_system/notif_feedback.py` (savior instruction in
  `vps/CLAUDE-box.md`). Observer: sized below.
- **A box for any page**: `soda-brain/system/feedback-box.js` (one script line; posts the surface and the last thing he
  clicked). Tested on a fixture page against a patched hub-review copy.
- **The brain answers in his words**: every ledger was already indexed one page per row (kind rule).
  `brain_serve.py` adds `his_rules(topic, k, ledger)` = `POST /brain/rules` and the MCP tool `his_rules`: liked rows
  and ruled rows apart, with confirmation counts. No migration (a filtered `brain.search`).
- **Tests**: `task-land/_system/test_notif_loop.py` (the six classes, the routing, the notification resolution, both
  patches on fixture copies), `soda-brain/tools/tests/test_his_rules.py`; `test_whitelist.py` still passes. One live
  Opus classification: "group welcome messages like this one never need to reach my phone" -> rule, notif ledger.

## Sized, not built

| Gap | Size | What it takes |
|---|---|---|
| GTM boards: ledger + route | BIG (half a day) | BOARD-CONTRACT.md + skill-map, the board generator loading the skill, and ONE processor: fold feedback_worker.py's system fixes into feedback_session (class system) first. The route alone is one POST per board comment to `/api/feedback {surface: "gtm-board"}`, but switching it on before the fold makes two processors act on one sentence |
| Notification observer | MEDIUM (2 h, box) | a pass in daemon.js after classify: H1 (every line names a sender) and H2 (he wrote later on that jid; the WA store has fromMe) per card, a hit line with surface notif |
| Daily page feedback | MEDIUM (2 h) | a `((rule: ...))` directive in `Resolve-TaskDirective` that POSTs to `/api/feedback {surface: "daily"}` instead of editing the task |
| Map include lines | CHEAP (2 lines) | `<script src="feedback-box.js" data-surface="system-map">` (and `simulation-map`) before `</body>` of the two HTML maps; held back only because another session had both files open and uncommitted at 19:13 |
| Event pages reason box | CHEAP (1 h) | `research-page/build_snitem_dm.py` emits the feedback-box.js line with `data-surface="event-page"`; the route exists |
| Whitelist / proactive observers | CHEAP (1 h) | the code paths exist; write one hit line per decision (`whitelist_judge.judge`, `pipeline.py --auto`) |
| Meeting observer | MEDIUM | meeting_loop.py scores each produced step against the MEETING-CONTRACT questions and writes hits |
| Quick Claude | MEDIUM | the panel's prompt gets the six-class instruction and runs `ledger_verdict.py file --surface quick-claude` on a sentence that judges something |
| Trippy into the ledgers + brain | MEDIUM | index `preferences.json` and the preference wiki (a BRAIN_SOURCES glob), then a TRIPPY-CONTRACT the duels confirm |
| Janitor ledger | MEDIUM | the cleaning rules move from the workplan into CLEANING-CONTRACT.md; Cleaning tab rows carry section CLEANING -> kind feedback, surface cleaning |
| Voice review | BIG | transcribe review audio into queue entries (the voice lane's whisper path exists on the box) |
