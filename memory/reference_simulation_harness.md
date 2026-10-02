---
name: reference_simulation_harness
description: "The simulation harness (~/sim): a sandbox copy of the whole system with a fake outside world, agents that play the world and him, a judge and a score page; how to run it and what it found"
metadata:
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-30T17:45:38.196Z
---

**What it is (built 2026-09-30, his ask: "simulate 90 days worth of work ... measure the system score").**
`~/sim/harness/` (local git repo) builds `~/sim/home/`, a copy of the live code with every edge redirected
(`build_sandbox.py`: paths, ports 4180->4280, 4124->4224, 4137->4237, bare port numbers; `leak-allow.json`; a scan
fails the build on any live address). Fakes: `fakes/triage/gmail.py` + `gcal.py` (copies of the real files on a
JSON world), `fakes/hub_server.py`, `fakes/crm_server.py` (data + intake), stand-ins for smtpcheck, run-commit
(LinkedIn), li_restore, commit-to-contacts. Sandbox processes get `simenv.env()`: USERPROFILE = the fake home,
`pyshim/sitecustomize.py` (simulated clock via time-machine, a wall that refuses every non-loopback socket, claude
calls rerouted to `simclaude.py`, ssh/powershell/taskkill refused), `nodeshim/simclock.js` (same for Node,
NODE_OPTIONS --require), `CLAUDE_BIN=bin/simclaude.cmd`. `simclaude.py` = the one choke point for model calls:
budget guard (`budget.py`, reads the plan usage like claude-bar; stop at 58% week, pause at 80% of the 5h window),
Notion stand-in for the meeting loop (listing from `world/notion_notes.json`, reading = the note text inlined),
`runs/current/calls.jsonl` + one Langfuse generation per call (tag sim).

**Agents (headless opus, never me):** `world_gen.py` (cast of 60 fictional people at `*.example`, a 30-day plan
with outages and laptop-down slots, one call per simulated day writing the events AND the truth), `me_agent.py`
(plays him: verdicts on the fake hub, own actions outside the system, complaints as decisions lines),
`judge.py` (code measures detected / latency / sent-without-yes, one model call per day scores person, step,
artifacts, wrong actions; `~/sim/score.html`). `sim_day.py setup <run>` then `sim_day.py run <n> [<m>]`.
`runner.py` has the primitives (start/stop servers, jump, deliver, tick, seed, board).

**Rules in force:** nothing fake ever enters the real CRM, mail, Notion, memory or task-land; fake data is
deleted at the end (harness stays); sim-born rules go into the real ledgers marked `[sim]`, event rules
unlimited, drafting-style rules at most half of what the ledger holds; live fixes land as they are proven, one
commit each (`sim-fix:`), send paths and box code wait for his yes.

**What the first hours found:** see `task-land/_system/WORKPLAN-20260930-simulation.md` (Log section): the
ledger first-line drop (fixed live), the reader blind to inbound email bodies, WhatsApp asks with no draft, the
reader spending 84% of its reads on the campaign's own sends (F1 patch in `harness/patches/`), the uncached
prefix of every headless call (F2), two bugs the fake mail reproduces (reply detection without `--enrich` in
campaign.py:581 / daily.py:180; `send --thread-id` writes no In-Reply-To).

**Agents share his standing rules from one place (1 Oct):** `simenv.SIGNATURE_RULE` (H94: the Tundra signature under
'Alessandro' is required, never a fault) is injected into the JUDGE, LEARNER and ME prompts. A judge without it filed
false "critic lets the signature block through" items (Lff045c4c, E0040). When a sim item contradicts a live ledger
rule, fix the agent prompt here, not the live system.

**Second night (2 Oct 2026, run `meetings-night`, 4 days, 85 events, balanced mix with 3-4 Notion notes a day via
`SIM_MIX`):** days 2-4 average 64.6 (72.2, 60.5, 61.5; day 1 was an artifact: a restart left the sandbox meeting
loop's `listed_at` in the future, fixed by `sim_day.rewind_state`). Harness lesson: a world that keeps earlier truth
needs delivery keyed by (id, day), or a new run delivers nothing. Live fixes it produced: full inbound mail text to
the reader (`gmail.py recent --with-body`), WhatsApp follow-ups from meeting notes. Report: MORNING REPORT in
`task-land/_system/WORKPLAN-20261001-soda-brain.md`.

**Outcome of the first night (1 Oct 2026, 12 simulated days, 170 events):** score 56 (as it was) -> 61 (fixes) -> 60
uncapped; uncapped (DA_DEPTH=full) cost +86% for no gain: the misses are in the artifact layer (drafts, cards, hub
hygiene: surface score 32), not in reading. Worst kinds: LinkedIn in, what he sees on the hub, accepts, bookings,
meeting notes. The morning report is the MORNING REPORT section of the workplan. Lesson for the harness: an
unattended full-permission worker inside the sandbox escapes (ssh); never again; the live worker took sim items once
their claim went stale, so the learner files them `needs_him`. Fake data lives in `~/sim/world` and `~/sim/home`
until he says delete.
