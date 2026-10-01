# Rules: where they are and how they live

The rules of the system are his sentences, dated, append-only, in five ledgers, compiled into skills that the agents
load, checked by observers that write hit lines, and demoted by numbers. Phase 2 of the brain moves the ledgers and
the hit ledger into this folder; until then they live in task-land (synced to both machines and to GitHub) and four
code bases read them by path. This file is the pointer and the description.

## The ledgers (task-land/_system/)

| Ledger | Surface | Rules on 2026-10-01 | Compiled into | Checked by |
|---|---|---|---|---|
| `EMAIL-REVIEW-CONTRACT.md` | every message to a person | 86 | `~/.claude/skills/drafting/SKILL.md` | `drafts/critic.py` at registration |
| `HUB-CARD-CONTRACT.md` | approval-hub cards | 21 | `~/.claude/skills/hub/SKILL.md` | the hub guard on the box (`hub-rules.json`) |
| `CRM-CONTRACT.md` | CRM writes, Today, the reader | 42 | `~/.claude/skills/crm/SKILL.md` | `crm-app/observer.js`; `crm-app/reader.js` loads the ledger whole |
| `MEETING-CONTRACT.md` | Notion meeting notes to steps | 8 | read whole by `gtm-eng/agent/meeting_loop.py` | the meeting loop |
| `NOTIF-CONTRACT.md` | what reaches his phone | 5 | sodanotif routing prompt | sodanotif |

Canonical description: `task-land/_system/RULE-LOOP.md` (v3). Evidence: `task-land/_system/rule-hits.jsonl` (one line
per observer decision, `{ts,surface,rule,action,item,...}`; `action:"ok"` lines are the denominator) and
`task-land/_system/decisions.jsonl` (his verdicts: hub, boards, CRM review). Hints that grow from misses:
`task-land/_system/hints/<component>.md` (crm-reader, inbound-asks, meeting-loop, due-today, agent-work), appended by
the simulation's learner and by sessions, read whole by the callers.

## How a rule is born, compiled, checked, demoted

1. He says one sentence: "this sucks because ...", "I like this", "this again", or asks for a change. The same turn:
   `python task-land/_system/drafts/addrule.py --contract email|hub|crm|notif|meeting --rule "..." --quote "his words"
   [--soft] [--like] [--item <id>]`. A change request becomes a build item in that surface's workplan instead.
2. Compile: `python task-land/_system/drafts/compile_skill.py --contract <surface> --install` rewrites the skill from
   the ledger (rules "in front" by hit counts, the rest "assumed"); the skill is never edited by hand.
3. Check: the observers append hit lines; `task-land/_system/rule-stats.py` reports per rule: applicable, hits, last
   hit, days since. Measured 2026-10-01: 160 rules, 35 ever checked, 125 never (78%); one CRM rule (H2) is 4,183 of
   7,184 hits.
4. Demote: a rule never checked for 30 days is either compiled into code (then it is not a rule) or goes to SOFT; the
   number from rule-stats decides, never a feeling. `brain check` (phase 2) automates this.
5. System check: `task-land/_system/system-check.py` (laptop task RuleLoop-SystemCheck, 09:10) writes
   `system-check-<n>.md` when the decision window is full; the box posts it as a hub update.

## The rules that bite first (pointers, not copies)

The short list a session must know before it does anything is in `memory/MEMORY.md`, section "Rules that bite first".
The full set of standing constraints of the owner is in `AGENTS.md`. Both are compiled from the ledgers and the
feedback memories; when they disagree with a ledger, the ledger wins and the copy is fixed.

## Phase 2 (planned)

Move `*-CONTRACT.md`, `rule-hits.jsonl`, `hints/` here; repoint `drafts/common.py`, `drafts/compile_skill.py`,
`drafts/addrule.py`, `drafts/critic.py`, `crm-app/reader.js`, `crm-app/observer.js`, `agent/meeting_loop.py` and the
agent scripts' `hints_text()` with one path constant each; keep `.gitattributes` `*.jsonl merge=union`; the box's hub
guard reads `hub-rules.json` from the hub folder (unchanged). Then every rule gets `since`, `checked_last`,
`superseded_by`, and `brain what-is-true`, `brain supersede`, `brain check` land.
