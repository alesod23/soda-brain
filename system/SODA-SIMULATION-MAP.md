# SODA SIMULATION MAP: the harness that tests the system, drawn

The visual map is `SODA-SIMULATION-MAP.html` in this folder (open it in Chrome next to `SODA-SYSTEM-MAP.html`; it
works offline except for the fonts). This page is its narrative and its index, so the brain can recall it. Same rules
as the rest of `system/`: updated in the same turn as `~/sim/harness` changes; dated; no secrets; no real person (the
cast is fictional, at `.example`).

Last verified: 2026-10-04 16:17 (`compare.py report` on both roots, each run's `scores.jsonl`, `runner.log`,
`runs/night3/PROGRESS.md`, the harness code and git log). Harness changes of 2026-10-04 20:40 (G84, G85, G86 below)
written into both files; the results numbers are still the 16:17 reading.

## What it shows

1. How it works: one lane chart of the sandbox (the fake world, shims and guards, the system copied, the fake
   surfaces, him and the judge; every node a real script or store with its port) and the chain of one simulated day.
2. The alignment: 28 real components, each with its twin and a fidelity mark (7 run unchanged, 12 stand-ins, 4 stubs,
   5 missing) and its maintenance surface (own schedule, own store, own rule ledger), as a four-lane chart and a
   filterable table with the reason each is or is not faithful.
3. The approaches: arms A (no brain, 2 days), B (the brain in the readers, 17 days), C (Edge skill hints, built, not
   run), D (cleaning layer, designed only); guards G1 to G5; the cost cuts; the budget policy (week 35 stop, 33 slow,
   5-hour window 80); the GO / STOP files; the two roots on port bases 4200 and 4300.
4. The eval: the judge's path, the score formula (detected 20, person 10, timely 10, step 30, artifacts 20, clean 10;
   a send without his yes = 0), and every metric with its definition, its source file and how it can be misread.
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
- Never run in the sandbox: the box feedback session (`feedback_session.py`, which replaced `feedback_worker.py`, now a
  retired stub: the sandbox's `feedback` tick prints its pointer), the system agent, `reconcile.py`, the sodanotif
  classifier, Slack, the daily page and its watcher (12 seeded task files instead).
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

## How to keep it

The data is one JS block at the bottom of the HTML (`NODES`, `SANDBOX`, `ALIGN`, `METRICS`, `RESULTS`, `REG`); the
charts draw themselves. The page holds its own copy of the system map's chart engine (per-chart lane width and
gutter added). Review before he sees it, from `~/soda-brain`:
`python tools/review_map.py --html system/SODA-SIMULATION-MAP.html --out system/_review-sim --charts chart-sandbox,chart-align,ts --sections how,align,eval,results,registry --phone 390`
until RESULT: CLEAN, then look at every screenshot. Move the "Last verified" line in both files.
