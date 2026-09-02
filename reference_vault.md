---
name: reference-vault
description: "Personal task vault at C:\\Users\\Alessandro\\task-land\\. Obsidian-compatible markdown folder structure. One file per task with YAML frontmatter. Built 2026-05-20 to replace the old ~/TODO.md monolith.\n"
metadata: 
  node_type: memory
  type: reference
  originSessionId: edc9e9a2-24ac-4264-9ac7-c5fc72ce9dae
  modified: 2026-08-06T15:36:41.655Z
---

# Vault — personal task system

**Root:** `C:\Users\Alessandro\task-land\`. Plain markdown, no Obsidian app required (but layout is Obsidian-compatible if installed).

## ⛔ ROUTING RULE — actionable knowledge goes HERE, not into MEMORY.md (user, 2026-08-06)

**A contact, a lead, a link, a "save this for X" — none of it belongs in a memory file or in
`MEMORY.md`.** MEMORY.md is loaded into context EVERY session, so each line there is a permanent
tax; it is for how-I-work rules and durable pointers, not for a thing to act on once. His words:
*"it shouldn't really go into a big expensive memory file that we always look at… it should rather
be somewhere in task-land. There should be a to-do that is somewhat related to this, like send an
email out to EWOR about hacker house, and there we have this knowledge inside of it."*

**How to apply:** create the TASK the knowledge serves, and put the knowledge in the task's BODY —
who the person is, the link, why they matter, what's unverified, next actions. The task is the
container; the context rides inside it. Use `capture.py --body-file`. Caught live 2026-08-06: an
Egert Vinogradov / Nortal contact was filed as `reference_ewor_nortal_contact` + a MEMORY.md line;
both were deleted and rewritten as `Tasks/inbox/email-ewor-about-the-hacker-house-*.md`.

Memory is still right for: standing behavioural rules, system/architecture pointers, preferences.
If unsure — "would I want this sentence loaded every single session forever?" If no, it's a task.

## Layout

```
task-land/
├── Tasks/{inbox,active,archive}/   # one .md per task
├── Reminders/                       # date-bound one-shots
├── Repeating/                       # weekly retro, monthly review
├── Habits/                          # daily yes/no
├── Events/                          # calendar-like
├── Notes/                           # free-form
├── Daily/YYYY-MM-DD.md              # daily notes (built by /today)
└── _system/
    ├── context.md       # priority projects (single source of truth)
    ├── tags.md          # tag taxonomy
    ├── agent-notes.md   # Claude's running journal
    └── capture.py       # add-task helper
```

## Skills (each is a slash command)

- `/today` — builds `Daily/YYYY-MM-DD.md` from active + due + carryovers + habits + events; surfaces inbox count as a nudge section; picks suggested Big Three
- `/capture <text>` — wraps `capture.py`; smart project/tag inference. **Default dest = `active`** (user-typed = commitment). Land in `inbox` only if user says "park", "later", "maybe", "inbox", "not now".
- `/done <slug>` — moves task to `Tasks/archive/` with `completed: DATE`
- `/inbox` — lists `Tasks/inbox/` for batch triage (active / archive / drop). Inbox fills mainly from /triage, not from /capture.

## Task file schema

```yaml
---
id: <slug-matches-filename>
title: <human title>
status: open | active | done | dropped
created: YYYY-MM-DD
due: YYYY-MM-DD or empty
project: bmw | lobbly | cdtm | xplore | thesis | tundra-talents | tools | personal
source: self | wa | gmail-cdtm | gmail-lobbly | slack-cdtm | slack-xplore | linkedin
tags: [outreach, code, study, errand, admin, urgent, quick, ...]
---
```

## /triage integration (THE key wiring)

When `/triage` shows an item and the user picks `N todo`:
1. `capture.py` runs → task lands in `task-land/Tasks/inbox/` with `source:` set (e.g. `gmail-cdtm`, `wa`)
2. Source is marked DONE in its channel (Gmail `triage/done` label, WA `wa-state.json#done`)
3. /triage never re-surfaces the item — vault now owns it

This replaced the old behavior where `todo` carried items inside the source channel (Gmail `triage/todo`, WA `wa-state.json#todo`). See triage `SKILL.md` step 6 "Vault integration for `todo`".

## capture.py invocation

```powershell
$py = "C:\Users\Alessandro\AppData\Local\Programs\Python\Python312\python.exe"
& $py "C:\Users\Alessandro\task-land\_system\capture.py" `
    --title "<title>" --source <self|wa|gmail-X|slack-X> `
    --project "<project-or-empty>" --due "<YYYY-MM-DD>" `
    --tags "<comma-sep>" --dest <inbox|active>
```

Prints created file path to stdout, summary to stderr.

## What this replaced (deleted 2026-05-20)

- `C:\Users\Alessandro\TODO.md` — flat manual checklist
- `C:\Users\Alessandro\triage\todos.md` — empty stub
- `~/.claude/commands/vault/` — dead skill template (`<VAULT_PATH>` never filled)

Migration: all open items from old TODO.md were converted to `Tasks/active/*.md` (today-tier) or `Tasks/inbox/*.md` (later-tier); done items archived to `Tasks/archive/*.md`.
