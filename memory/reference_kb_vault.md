---
name: reference-kb-vault
description: "Personal KNOWLEDGE vault at C:\\Users\\Alessandro\\kb\\, separate from the task vault at ~/task-land/. Wilkins/Karpathy pattern: Raw ingest → atomic Notes → Topic MOCs. Built 2026-05-21 to hold the user's multi-domain knowledge base.\n"
metadata: 
  node_type: memory
  type: reference
  originSessionId: edc9e9a2-24ac-4264-9ac7-c5fc72ce9dae
---

# KB — knowledge vault

**Root:** `C:\Users\Alessandro\kb\`. **Schema contract:** [[CLAUDE.md]] at vault root — read it before doing anything in this vault.

## Why TWO vaults

Wilkins' literal pattern: task vault (`~/task-land/`) stays focused on doing; knowledge vault (`~/kb/`) stays focused on thinking. Both opened side by side in Obsidian. Cross-link via `obsidian://open?vault=<name>&file=<path>`. ([source](https://www.jdhwilkins.com/how-i-built-an-ai-powered-task-system-with-obsidian-and-claude-code))

## Layout

```
~/kb/
├── README.md
├── CLAUDE.md          ← LLM contract/schema (READ FIRST)
├── index.md           ← catalogue / entry point
├── Raw/               ← unedited ingest (Web Clipper, paste, PDFs). NEVER DELETE.
├── Notes/             ← atomic notes (one idea each) + source summaries
├── Topics/            ← 10 MOCs (one per life-area)
├── people/            ← person notes, shared across topics
├── Assets/            ← images, PDFs, attachments
├── Templates/         ← atomic / person / source / moc / project / journal
├── Daily/             ← thinking journal (NOT tasks — those go in ~/task-land/)
└── .obsidian/         ← pre-configured (Dataview/Tasks/Calendar needed; user installs on first open)
```

## The 10 MOC domains

`lobbly`, `ai-patent-law`, `cdtm`, `thesis`, `travel`, `techie`, `ai-landscape`, `finance` (deprio), `learning-log`, `people` (cross-cutting).

Each MOC stub at `Topics/<slug>-MOC.md` has empty Dataview queries that auto-populate as notes accumulate.

## Conventions (canonical — full version in vault's CLAUDE.md)

- **Wikilinks only** — `[[anne-tryba]]`, never `[people/anne-tryba.md]`
- **Slugs are kebab-case**, max ~5 words
- **One person = one file**, listed in `topics:` of every life-area they touch
- **Frontmatter required**: `type`, `topics: []`, `tags: []`, `created`, `updated`. Atomic notes also have `sources: []`.
- **Don't dump long content into MOCs** — they're indexes
- **Don't write tasks here** — tasks go to `~/task-land/Tasks/` via `/capture`

## Karpathy-pattern flow

Raw (ingest) → Notes/atomic (compile) → Topics/MOC (link) → query → output → re-file back into vault. The LLM does most of the writing; user is the editor + ingestor + question-asker.

## Cross-vault linking

- From KB → task vault: `obsidian://open?vault=task-land&file=Tasks/active/<slug>`
- From task vault → KB: `obsidian://open?vault=kb&file=Notes/<slug>`
- Wikilinks `[[slug]]` resolve only WITHIN a single vault.

## Setup status

- ✅ Folder structure created
- ✅ CLAUDE.md schema written
- ✅ index.md catalogue written
- ✅ 10 MOC stubs in Topics/
- ✅ 6 templates in Templates/
- ✅ READMEs in Raw/, Notes/, people/, Assets/
- ✅ `.obsidian/` pre-configured
- ⏳ User to install Dataview + Tasks + Calendar plugins on first open
- ⏳ User to install Obsidian Web Clipper browser extension (Karpathy's ingest tool)
- ⏳ Walk-through with one concrete topic (TBD)
