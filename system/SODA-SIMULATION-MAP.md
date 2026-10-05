# SODA SIMULATION MAP: the harness that tests the system, drawn

The visual map is `SODA-SIMULATION-MAP.html` in this folder (open it in Chrome next to `SODA-SYSTEM-MAP.html`; it
works offline except for the fonts). This page is its narrative and its index, so the brain can recall it. Same rules
as the rest of `system/`: updated in the same turn as `~/sim/harness` changes; dated; no secrets; no real person (the
cast is fictional, at `.example`).

Last verified: 2026-10-05 03:30 (the improver loop, item 25: `tests/test_i25_improve.py` ALL PASS x2); before that 2026-10-04 22:40 (harness code and git log, `tests/test_g133_twins.py` PASS x2; the results numbers are
still the 16:17 reading of `compare.py report` on both roots). Harness changes of 2026-10-04 20:40 (G84, G85, G86) and
22:30 (G133, the SIM-UPDATE twins and the G-P score) are written into both files.

## What it shows

1. How it works: one lane chart of the sandbox (the fake world, shims and guards, the system copied, the fake
   surfaces, him and the judge; every node a real script or store with its port) and the chain of one simulated day.
2. The alignment: 32 real components, each with its twin and a fidelity mark (11 run unchanged, 14 stand-ins, 4
   stubs, 3 missing; G133 added the proactive to-do reader, the unattended to-do worker, the CRM System log and the
   System Update, and the feedback session moved from missing to a twin) and its maintenance surface (own schedule, own store, own rule ledger), as a four-lane chart and a
   filterable table with the reason each is or is not faithful.
3. The approaches: arms A (no brain, 2 days), B (the brain in the readers, 17 days), C (Edge skill hints, built, not
   run), D (cleaning layer, designed only); guards G1 to G5; the cost cuts; the budget policy (week 35 stop, 33 slow,
   5-hour window 80); the GO / STOP files; the two roots on port bases 4200 and 4300.
4. The eval: the judge's path, the score formula (detected 20, person 10, timely 10, step 30, artifacts 20, clean 10;
   a send without his yes = 0), the G-P line of a proactive-ask scenario (card 30, set 40, owner 15, created after his
   yes 15; a to-do before his yes = 0; its own line, outside the day score), and every metric with its definition, its
   source file and how it can be misread.
5. The results: nights 1 to 3 run by run, and one time series of the event score and the hub surface per simulated
   day across all nights, with the failed days marked.
6. The registry of every harness part with its real twin. 7. How to keep it.

## Fidelity gaps (the honest list)

- The door is a stand-in: e5-small vector plus token overlap over the sandbox's own rows, not the Postgres hybrid; the
  CRM reader's query starts with the person's name, so the person's own row is a trivially strong hit (96% strong).
- The CRM review surface (G84, closed 4 Oct 20:40): every `/review/*` route of the sandbox intake runs the sandbox
  copy of `review-api.js` / `review-artifact.js` through `fakes/review_twin.js` (one node process per request, under
  the sandbox clock and wall); producers attach drafts (kind `waiting`, CRM H56), the hub-card mirror and
  `crm-outdated.js` tick after every event, the simulated him decides on the board (`crm_review.py`: approve / skip /
  comment, one commit that sends) and the judge sees the review item and counts a committed approve as his yes. Still
  not the real thing: `/review/generate` is synchronous (live 202 + a polled job); "generate missing" is capped at 4 a
  pass and 12 a day (`run.json` `review_gen_pass` / `review_gen_day`; live no cap); the board is read as JSON, not the
  review mode page; one CRM writer (live: the box writes, the laptop proxies); crm-outdated after each event, not every
  10 min. The smoke day showed `crm-outdated.js` ending with a libuv assertion at `process.exit` (exit 3221226505) after
  a complete pass: Node 20 on Windows, not seen in the live log; counted as a non-zero step, not a harness failure.
- Never run in the sandbox: the system agent, its UI walk and whitelist tabs, `reconcile.py`, the sodanotif
  classifier, Slack, the daily page and its watcher (12 seeded task files instead; no `((rule: ...))`), the two-node
  writer split (SIM-UPDATE rows 7, 10, 11, 16, 18, 19 stay GAPs).
- Twins WITHOUT tools (G133, 4 Oct 22:30): the box feedback session (`fakes/feedback_session_twin.py`: the real script
  on the sandbox hub-review queue; what it does in code runs, the resumed session answers with no tools) and the
  unattended to-do worker (`fakes/todo_worker_twin.py`: the real tick, the work session with no tools, capped 3 triage
  calls and 2 sessions a simulated day). simclaude runs claude.exe under the REAL home, so no sandbox session gets
  tools; their decisions are real, their tool actions are not executed. Rules the session files land in the sandbox
  ledgers and last until the next day's build copies the live ledgers again.
- Cadences: the sweep every ~85 simulated minutes (live 10), the meeting loop on a 10-minute grid (live 5), the
  feedback worker every 2nd heavy pass (live 10 min); quick ticks right after each event, so latency is the harness's.
- Notion is a file: listing without a model, the note inlined in the prompt; settle times written by the world.
- LinkedIn is a stub: no browser, no 17-thread window, sends become outbox lines.
- The hub is the 30 Sep server mirror (no supersede of 3 and 4 Oct); the CRM has no replica, no Postgres mirror.
- The savior plays one job (rewrite a draft on his "no + words", max 2); the learner is off (G2), so a run cannot
  show the system learning from his feedback.
- The simulated him is Opus with a persona (not Sonnet: only the world agent runs on Sonnet in night 3); it lived the
  truth and answers every card at the next heavy pass. Outages and laptop sleep are scripted; one machine, no sync.

## Corrections found while drawing it (4 Oct 2026)

- The stop of 15:56 did not stop night 3: the runner was launched without `--wait-go`, so it watches
  `~/sim/runs/STOP`, not `runs/night3/GO.STOP`; it began day 18 at 16:06. `runs/STOP` was written at 16:17; the run
  ends after day 18. Day 18 is not in the page's numbers.
- `PROGRESS.md` repeats the previous score on a failed or unscored day (days 11, 13, 16: 58.5, 71.4, 71.8): use
  `compare.py` and `scores.jsonl`. Day 13 (24 Oct) is unscored as a whole day (the judge's one call returned bad JSON).
  FIXED 4 Oct evening (G85, `tests/test_g85_harness_bugs.py`): `world_gen.last_json` repairs one stray closer and
  takes the corrected last object, `claude_json` asks again once when the shape is wrong (world day and judge); a
  reply to a thread of the other mailbox lands where the thread lives (`runner.thread_home`); `run_night` writes only
  that day's judge line (`day_record`, field `scored`). Also: `budget.allowed()` re-judges the cached figures with its
  own caps, and `run_night --cap/--slow` hands its caps to every child (simclaude's guard read 35 before).
- `compare.py` "judge failures" counts the brain's todo_match judge, not the day judge.
- 845 of arm B's 1,949 call lines are free stand-ins (mostly the Notion listing); real model calls are 1,104.
- The brief said the simulated him runs on Sonnet: the code runs it on Opus.
- The system map's legend scrolls the page sideways at 390 px (the status dots do not wrap); this page wraps them.

## Improvement over time

Event score by run: 54.8, 60.7, 63.3 (night 1), 63.8 (night 2), 71.3 (night 3, arm B); arm A 66.5. Not a clean
series: a different world every night, the judge changed on 1 Oct (surface line, H94 signature rule) and on 4 Oct
(false-close line), and the one same-world comparison (A vs B, 12 and 13 Oct) shows no difference. The hub surface
falls within every night (night 2: 47 to 19; night 3: 80 to 27-30) as stale Today rows pile up. A frozen regression
world re-run after each change, with the judge version stamped, would make the question answerable.

## The acceptance run (G86, goal condition 3)

One run, arm B, on the final system, in a fresh root that copies night 3's world (cast, arcs, plan and the generated
days 1 to 18: the world night 3 B was judged on), launched hidden:
`powershell -NoProfile -File ~/sim/harness/accept.ps1 -Root C:/Users/Alessandro/sim/accept -Base 4400 -Name accept-B -Days 1-7 -Setup -Launch`
then `python ~/sim/harness/compare.py goal --root C:/Users/Alessandro/sim/accept` (exit 0 = PASS). The per-day table:
event score, sends without his yes, stale Today (board items the simulated him called not relevant or not current,
over the items shown), hub open cards at the end of the day (`runs/current/surface.jsonl`, written by `sim_day`),
CRM board open items; PASS needs arm B, at least 5 scored days, an event average of at least 71.3, 0 sends without
his yes, stale Today at most 20%, a hub-open slope of at most 0.5 cards a day, 0 harness failures (days that raised or
ended without a judge line). Smoke day: `-Root C:/Users/Alessandro/sim/smoke -Base 4500 -Name smoke-B -Days 1-1`.
Smoke day run 4 Oct 20:37 to 21:39 (62 min wall, day 1 = 12 Oct, 15 events): score 56.9 (night 3 B on the same
day: 55.4), fatal 2 (both the meeting loop's invite after a confirmed meeting card: the open question G87), the board
in the loop (9 drafts generated, 3 commits, the commit's sends counted as his yes), 0 harness failures; week 45 to 52%
over that hour, other builders included. G127 (4 Oct 21:40): `run_night.py` tears down every fake it starts (a
Windows job object with kill-on-close, finally + atexit, `runs/<night>/pids.json`, `run_night.py reap [<night>]`
that checks each pid's command line is a harness fake); proof `tests/test_g127_teardown.py` (STOP, an injected day
failure, a hard kill).

## The SIM-UPDATE twins (G133, 4 Oct 2026 22:30)

Every TO BUILD row of `~/sim/harness/SIM-UPDATE-20261004.md` runs in the sandbox on real system code copied by
`build_sandbox.py` (leak scan 0):
- row 14, the proactive to-do reader + executor: tick `proactive` after every event and after his heavy pass =
  `proactive_todo.py scan` (reads the sandbox events ledger, ONE todo-proposal card on the fake hub) + `apply` (his
  yes -> each line through its owner: the real `trip_todos.py` on `world/trips.json`, `capture.py`, the CRM step route);
- the scored goal G-P: the world adds an ask + his yes on about 1 day in 3 (`world_gen.proactive_scenario`, one call,
  `truth.proactive` with the expected to-dos); `judge.gp_day` writes one `proactive_todo` line per scenario and prints
  `G-P <id> <person>: <score>/100 (card, set, owner, after_yes)`; `compare.py goal` prints the G-P block after
  condition 3 (PASS = average >= 80 over >= 3 scenarios, 0 to-dos before a yes), condition 3's verdict unchanged;
- row 8, observers: `rule_directive.py`, `board-observer.js` and the proactive / cleaning / board skills copied; every
  observer writes the sandbox `rule-hits.jsonl`; the judge sees the lines of an event's card as `rule_hits`;
- row 6: the fake door indexes the CRM review items as kind `review`;
- row 9: tick `feedbacksession` every 2nd heavy pass (the twin above); the fake hub serves hub-review's queue
  (`/api/feedback`, `/api/queue`, `/api/queue/done`) and his card words enter it;
- row 13: the simulated him has a 4th complaint surface, `crm-system`, POSTed to the fake CRM `/api/system-feedback`
  (the sandbox `system-feedback.js` through `review_twin.js`, forwarded to the queue);
- row 15: tick `todoworker` in every heavy pass (the twin above, capped);
- row 12: tick `sysupdate` at the day's first pass, `--no-post`, the page kept in the sandbox.
Proof: `python tests/test_g133_twins.py` (39 checks, no model call) and `python tests/check_g133_gp_day.py` (run_night
setup + the first 3 events of `tests/fixtures/gp-day.json`, his Caleb case with Caspar Lind, stopped through STOP,
real model calls). New `run_night.py` flags: `--fixture-day <events.json>`, `--max-events N`.

## The improver loop (build item 25, 5 Oct 2026)

His word, 02:44: "a live system change during the simulation: i WANT THAT. i want to then see if it improves because
of that." `~/sim/harness/improve.py`, called by `run_night.py` after every scored day (`--improve`, default ON;
`--no-improve` off; `accept.ps1 -Improve` / `-NoImprove`, `-ImproveMax N`):
1. Case tests: every earlier live change's `~/sim/harness/cases/<id>.py` runs again on the live tree (`--root <repo>`).
2. Revert check: day n ran on the changes made after day n-1. Each day is read against its baseline (what other runs
   scored on the same world and date, `compare.baseline`), because two consecutive days carry different events (55 and
   83 in night 3 B). If (s_n - base_n) < (s_n-1 - base_n-1) - `compare.noise_band()` (same world, same date, different
   runs: twice the mean difference, at least 3 points, 5 without pairs; `python compare.py noise`), the day's changes
   are reverted (`git revert` of their commit; a rule whose revert conflicts loses its row by an exact edit) and logged
   "tried, reverted". Without both baselines the raw scores are compared.
3. Misses: judged events under 60 or with a FATAL, plus the guard G1 lines of the day (blocked connections), grouped by
   class (kind + FATAL reason, else the costliest point bucket), worst first; a class already changed in the run is skipped.
4. Per class (at most `--improve-max`, default 2, each under `budget.allowed()`), ONE Opus decide call (read-only tools)
   sees the worst case, its event and truth, the ledgers, the real code the sandbox runs (`manifest.json`) and the
   run's earlier changes, and answers rule / code / none:
   - RULE: `addrule.py --contract <x>` with the simulated case as the quote and `source: simulation <run> day <n> (<id>)`,
     `compile_skill.py --install` when a skill map exists, one task-land commit `sim-improve: ...`; the case test checks
     the row (tagged with the case id, holding the rule's key words) is in the ledger.
   - CODE: a fix job through the System Agent's path (`jobs.add_fix` + `job_runner.py run --job`: the never-list guard
     `fix_guard.py`, the 45-min wall, the budget point); the session edits the REAL code with a `.bak`, writes the case
     test, makes ONE commit `sim-improve: ...`; a line in `system-agent/sessions.jsonl` (the orchestrator's memory).
   - NONE: the miss is the simulation's own (a twin, the judge): logged, nothing changed.
5. Proof per change: the case test runs on a sparse git worktree of the commit's parent (must FAIL) and on the live tree
   (must PASS); a test that does not discriminate reverts the change at once.
6. The sandbox is rebuilt from the live files (`build_sandbox.py` + the G5 leak scan; a leak reverts the day's
   changes), so the next simulated day runs on the changed system.
Ledger: `~/sim/runs/<run>/results.jsonl` (one line per change; later lines per change add case runs, the next-day
effect, the revert). The hub tab's data: `task-land/_system/sim-results/<run>.json` (`improve.py export`), drawn by
hub-review's "Simulation results" tab (currency patch `patch-hub-review-simres-20261005.py`, marker SIMRES-I25, on top of
ITEM22): one card per run (date, arm, days, the score curve), System changes, New rules, Tests, Right / Wrong + one line
per change -> `sim-results/verdicts.jsonl` -> `improve.py verdicts` (at every run_night start): the line through
`ledger_verdict` (surface simulation), a Wrong reverts the change. A STOP file seen during the improver ends it after
the change in hand (committed and tested, or reverted). Proof: `python ~/sim/harness/tests/test_i25_improve.py` (no
model call) and the smoke day below.

## How to keep it

The data is one JS block at the bottom of the HTML (`NODES`, `SANDBOX`, `ALIGN`, `METRICS`, `RESULTS`, `REG`); the
charts draw themselves. The page holds its own copy of the system map's chart engine (per-chart lane width and
gutter added). Review before he sees it, from `~/soda-brain`:
`python tools/review_map.py --html system/SODA-SIMULATION-MAP.html --out system/_review-sim --charts chart-sandbox,chart-align,ts --sections how,align,eval,results,registry --phone 390`
until RESULT: CLEAN, then look at every screenshot. Move the "Last verified" line in both files.
