# AGENTS.md

For any agent, assistant or orchestrator that reads this repository: Claude Code sessions on the laptop and the box,
and any harness connected later. The owner is Alessandro Sodano (he/him), co-founder of Tundra Health, student at
TU Munich and CDTM; the system does his outreach, follow-ups, meetings and tasks with him as the only decider.

## What this repo is for

Recall what is true before acting. The system's own misses (measured in a 12-day simulation, October 2026) were
never memory misses: every miss was a decision taken without evidence that sat two files away. So: before you draft,
propose, schedule or change anything, read the relevant page here (`system/LOOPS.md` for how the loop works,
`rules/README.md` for the rule that governs the surface you are on, `memory/` for the lesson already learned).

## The contract every agent follows

1. Nothing is sent to anyone without his verdict. A send is a hub card (`POST http://127.0.0.1:4180/pending`
   on either machine, which is the box's approval hub) and his yes on it; a committed batch on a review board is the
   yes. The one delegated exception is the daily campaign fire at 16:55, on a ledger with caps he set.
2. Found contact details are proposed, never written: a card lists them, his yes files them.
3. Every email draft goes through the review lane (a real Gmail draft, a sidecar, the critic, a card), never chat text.
4. The CRM has one writer (`PUT :4124/api/data` through the CRM server or its intake routes); one person = one next
   step; every step carries its origin (which message, meeting or import set it).
5. Rules come from his sentences ("this sucks because", "I like this", "this again") and are filed the same turn
   with `addrule.py --contract email|hub|crm|notif|meeting`; a rule in chat that is not filed does not exist.
6. Nothing fake or invented enters the CRM, mail, Notion, memory or tasks. Facts come from a source you can name.
7. No console window ever opens on his screen; scheduled work on the laptop runs through `run-hidden.vbs`.
8. The map is updated in the same turn as the system (see README conventions). A change to a service, port, job,
   store or rule without its line in `system/` is an incomplete change.
9. Secrets are never written into a repo, a chat answer or a log. They are named by filename only.
10. Reversible first: back up (`.bak-<date>`), one commit per fix, tell him what changed and how to undo it.

## How to use the brain

- Static (any harness with file access): read `system/*.md`, grep `memory/` by the `description:` lines, open the fact.
- Live (the door, Tailscale only today): `GET http://100.85.52.84:4150/health`; `POST /brain/recall {"query": "...",
  "k": 8}`; `GET /brain/page?path=memory/<file>.md`; MCP at `/mcp` with tools `recall`, `what_is_true`, `page`,
  `crm_person`, `crm_search`. Header `X-Soda-Token` from `~/.env/soda.env` (never printed). Attach per session
  (`claude mcp add --transport http brain http://100.85.52.84:4150/mcp --header "X-Soda-Token: ..."`), never globally.
- Writing a fact: one markdown file in `memory/` with frontmatter `name`, `description`, `metadata.type`
  (user | feedback | project | reference), and from 2026-10-02 `since: YYYY-MM-DD`; one line in `memory/MEMORY.md`
  (or the matching `memory/index_*.md`), no frontmatter in the index, under 100 lines and 20 KB. A fact that
  replaces another gets `supersedes:` and the old one gets `superseded_by:`; nothing is deleted, `_attic/` is for
  retired files.
- Writing a rule: never by hand in a ledger; `python task-land/_system/drafts/addrule.py` (see `rules/README.md`).
- Writing to the CRM: never a file; the API or the intake routes, after his yes where the contract says so.

## What an orchestrator connected from outside may expect

The repo is the record; the door is live. Reads are free. Any write that reaches a person, the CRM or his calendar
goes through the hub as a card with the decision in `text` and the artifact in `context`; he answers on Telegram or
on the review page, and the system executes the yes. The rules it must respect are the ledgers named in
`rules/README.md`; the ones that bite first are in `memory/MEMORY.md` under "Rules that bite first".
