# SODA BRAIN

The brain of Alessandro Sodano's personal system: what is true about the system, the machines it runs on, the rules
he has given, and the facts the assistants have learned. One private repo, two-way on both machines (laptop and the
box), read by every assistant session and by any orchestrator that is connected to it. The system itself (the code
that reads mail, WhatsApp, LinkedIn and Notion, proposes decisions, drafts, sends after his yes, and learns from his
sentences) lives in other repos; this repo is the map and the memory of it.

Started 2026-10-01 from the repo `claude-memory` (the assistants' memory since May 2026), after Garry Tan's
"many harnesses, one shared brain": change the harness, keep the memory.

## Reading order

1. `AGENTS.md`: what an agent may and may not do here, and how to use the brain.
2. `system/LOOPS.md`: how the system works, as loops: events in, decisions out, his yes, rules learned.
3. `system/MACHINES.md`: the laptop, the box, the phone; services, ports, jobs, syncs.
4. `system/DATA-MAP.md`: every store, where it lives on each machine, who writes it, what is truth and what is a copy.
5. `system/REPOS.md`: the repositories and what each carries.
6. `system/ACCOUNTS.md`: identities and services (credentials are named, never stored here).
7. `rules/README.md`: where the rule ledgers are and how a rule is born, compiled, checked and demoted.
8. `memory/MEMORY.md`: the index of the 350 facts the assistants learned (one file per fact).
9. `handoffs/`: the notes one session wrote for another when a decision crossed machines or days.
10. `system/FINDINGS-20261001.md`: what the first full inventory found wrong, with severity and fix.
11. `system/SODA-SYSTEM-MAP.html` and `system/SODA-SIMULATION-MAP.html` (each with its `.md`): the system drawn, and the
    simulation harness that tests it drawn next to it (what runs unchanged, faked, stubbed or missing; the eval; the
    results over nights 1 to 3). Review both with `tools/review_map.py`.

## Layout

```
README.md, AGENTS.md
system/      the SODA SYSTEM map (LOOPS, MACHINES, DATA-MAP, REPOS, ACCOUNTS, FINDINGS-*, SODA-SYSTEM-MAP,
             SODA-SIMULATION-MAP)
memory/      the facts: MEMORY.md index, index_*.md sub-indexes, one markdown file per fact, _attic/
handoffs/    HANDOFF-*.md, dated
rules/       README.md pointer to the ledgers (they move here in phase 2)
tools/       the brain door: schema.sql (Postgres + pgvector), brain_index.py, brain_serve.py (HTTP + MCP), box-install.sh
```

## Where it runs

- Laptop (Windows): `C:/Users/Alessandro/soda-brain`. The assistants' memory path
  `C:/Users/Alessandro/.claude/projects/C--Users-Alessandro/memory` is a directory junction into `memory/`.
- Box (Ubuntu, always on, Tailscale 100.85.52.84): `/home/da/soda-brain`; `~/.claude/memory` is a symlink into `memory/`.
- Sync: both machines commit first, pull, push (`DA-VaultSync` every 10 min on the laptop, `da-repo-sync@soda-brain.timer`
  every 5 min on the box); a conflict parks on `conflict-laptop-soda-brain` / `conflict-vps-soda-brain` with an advisory
  file at the root.
- The door: `da-brain` on the box, `http://100.85.52.84:4150` (Tailscale only): hybrid recall over this repo and the
  rule ledgers (Postgres 16 + pgvector, local embeddings), the CRM rows mirrored from the laptop, MCP at `/mcp`.
  See `tools/README.md`.

## Conventions

- English, plain markdown, no em dashes, no emoji. Paths written plainly for both machines.
- A fact has a date. New facts carry `since:`; a replaced fact carries `superseded_by:` and is not deleted.
- Secrets never enter this repo: credentials are named by filename in `system/ACCOUNTS.md` and live in `~/.env/`,
  `~/triage/tokens/` and the other places listed there.
- No person records here: people live in the CRM; the brain holds how the system treats them, not who they are.
- The map is updated in the same turn as the system: a service, port, job, store or rule that changes is changed here too.
