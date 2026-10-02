---
name: reference_soda_brain
description: "The SODA BRAIN (built 2026-10-01/02): repo alesod23/soda-brain (was claude-memory) at ~/soda-brain and /home/da/soda-brain with memory/ (Claude's memory dir via junction/symlink), system/ (the SODA SYSTEM map), handoffs/, rules/inbox/, tools/ (da-brain: Postgres + pgvector door on the box, :4150, Funnel at da-box.taile93f00.ts.net); the CRM mirrors every save into it; instinct is the orchestrator"
metadata:
  type: reference
since: 2026-10-02
---

**What it is.** His personal brain for every harness ("change the harness, keep the memory"): the memory repo renamed
and grown. Laptop `C:/Users/Alessandro/soda-brain`, box `/home/da/soda-brain`, GitHub `alesod23/soda-brain` (private).
`memory/` IS the Claude memory dir: the laptop path `.claude/projects/C--Users-Alessandro/memory` is a directory
junction into it, the box's `~/.claude/memory` a symlink. Sync unchanged: `DA-VaultSync` (10 min) and
`da-repo-sync@soda-brain.timer` (5 min). `system/` = the SODA SYSTEM map (LOOPS, MACHINES, DATA-MAP, REPOS, ACCOUNTS,
FINDINGS-20261001): **update it in the same turn as a service, port, job, store or rule changes.** `handoffs/` holds
every HANDOFF-*.md (moved out of task-land 2 Oct). `rules/README.md` points to the ledgers (they move in phase 2).
Entry files for any agent: `README.md`, `AGENTS.md`. Workplan: `task-land/_system/WORKPLAN-20261001-soda-brain.md`.

**The door (`tools/`).** `da-brain.service` on the box: FastAPI + MCP at `http://100.85.52.84:4150` (Tailscale) and
publicly `https://da-box.taile93f00.ts.net` (Tailscale Funnel, since 2 Oct 01:40). Postgres 16 + pgvector 0.6, db
`soda`, schemas `brain` (pages, chunks, hybrid search with local `multilingual-e5-small` embeddings; 545 pages, 1,480
chunks on day one: memory, system, handoffs, the 162 rules, the hints) and `crm` (doc versions, companies, people,
templates, signals, events). `da-brain-index.timer` re-indexes every 5 min (sha fast path, 0.7 s when unchanged).
Tokens in `~/.env/soda.env` on both machines (never printed): `SODA_TOKEN` (full), `SODA_TOKEN_RO` (public, reads
only: GET, /brain/recall, /mcp; refuses /crm/put, /crm/events, /brain/reindex: verified 2 Oct). Loopback is exempt
only without X-Forwarded-For. Attach to a session per session: `claude mcp add --transport http brain
http://100.85.52.84:4150/mcp --header "X-Soda-Token: ..."`; never globally. `tools/README.md` has the routes.

**The CRM in Postgres (phase 3a).** `.medtech-crm/crm-app/pg-mirror.js`: every `PUT /api/data` on the laptop mirrors
the document to `POST /crm/put` (fire-and-forget, sha skip, outbox + replay), the events ledger to `/crm/events`; the
5-min `coattio-serve.ps1` tick replays and verifies (`scripts/pg-verify.js`). The sandbox never mirrors
(`CRM_PG_MIRROR=0` in `simenv.env`). Phase 3b (Postgres becomes the source) and 3c (an orchestrator propose route gated
by the hub) are designed in `.medtech-crm/WORKPLAN-20261001-crm-postgres.md`.

**The orchestrator.** instinct (instinct.com) from 2 Oct: his decisions in the workplan D4-D7: it keeps its own
proactiveness; it proposes and never holds a send scope (relaxed rule by rule for what he never reviews); it uses its
own connectors for Notion, WhatsApp, the Tundra Gmail and Calendar; we help with the CDTM account and LinkedIn; it
reads soda-brain, task-land and coattio on GitHub with training opted out; it proposes rules by writing a file in
`rules/inbox/` (`tools/rules_inbox.py`, box cron every 5 min: one hub card, his yes files it with addrule.py).

**2 Oct morning builds (all live, logged in the workplan):** meeting loop records every dated commitment as open
loops; new people get rows (LinkedIn first touch, proposed rows from WhatsApp and introductions, a `team` list);
hub hygiene rules in `hub_outdated.py` and a Today that separates what they owe; the start-of-day lane
(`due_today.py`, task `DA-DueToday` 08:30) with critic blocks for placeholders and attachment claims; instinct's
WhatsApp proposals read into lane cards (`instinct_inbox.py`, task `DA-InstinctInbox`); `push_again.py` (the
"push again" ranking); the campaign `bounce_gate` (CRM H43). The NEXT STEPS section of the workplan is the queue.

**Lessons from the build.** `psql -c` does not interpolate `:'var'` (feed it on stdin); `sudo -u da VAR=x cmd` is
refused by sudoers (use `env`); `2>/dev/null` on an install step hides the reason it died; the vault sync commits an
agent's files while it works (review = the last commits); Windows Application Control blocks psycopg's binary wheel on
the laptop (the tests use the pure-Python mode). See [[reference_simulation_harness]],
[[feedback_performance_hints_in_every_prompt]], [[reference_rule_loop]].
