# SODA SIMULATION MAP: the harness that tests the system, drawn

The visual map is `SODA-SIMULATION-MAP.html` in this folder (open it in Chrome next to `SODA-SYSTEM-MAP.html`; it
works offline except for the fonts). This page is its narrative and its index, so the brain can recall it. Same rules
as the rest of `system/`: updated in the same turn as `~/sim/harness` changes; dated; no secrets; no real person (the
cast is fictional, at `.example`).

Last verified: 2026-10-04 16:17 (`compare.py report` on both roots, each run's `scores.jsonl`, `runner.log`,
`runs/night3/PROGRESS.md`, the harness code and git log).

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
- No CRM review generator: `/review/items` is empty, so the simulated him decides on hub cards only, while since
  4 Oct 04:00 the CRM review is where he decides every follow-up.
- Never run in the sandbox: `crm-outdated.js` (the CRM hygiene worker), the system agent, `reconcile.py`, the
  sodanotif classifier, Slack, the daily page and its watcher (12 seeded task files instead).
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

## How to keep it

The data is one JS block at the bottom of the HTML (`NODES`, `SANDBOX`, `ALIGN`, `METRICS`, `RESULTS`, `REG`); the
charts draw themselves. The page holds its own copy of the system map's chart engine (per-chart lane width and
gutter added). Review before he sees it, from `~/soda-brain`:
`python tools/review_map.py --html system/SODA-SIMULATION-MAP.html --out system/_review-sim --charts chart-sandbox,chart-align,ts --sections how,align,eval,results,registry --phone 390`
until RESULT: CLEAN, then look at every screenshot. Move the "Last verified" line in both files.
