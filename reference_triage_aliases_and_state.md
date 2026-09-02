---
name: Triage v3 — aliases.json + state.json + auto-done
description: WA aliases for unsaved senders and persistent triage state file with auto-done semantics
type: reference
originSessionId: 4ea78cff-05f2-45ae-964c-63e0bf48d72c
---
# Two new files supporting the triage skill (added 2026-05-08)

## `wa-daemon/aliases.json`

Manual `name → JID-or-phone` map. **Checked BEFORE `contacts.json`** in `send.js`. Survives Google Contacts re-sync (which would otherwise wipe direct edits to `contacts.json`).

Schema:
```json
{
  "_README": "...",
  "Caleb": "66232858505219@lid",
  "Rali": "226306256044228@lid",
  "Someone": "+393331234567"
}
```

Values can be E.164 phones (`+...`) or full JIDs (`<digits>@lid`, `<digits>@s.whatsapp.net`, `<groupid>@g.us`).

**Auto-population rule (triage skill):** when a triage round shows a WA contact whose chat label (a `pushName`) doesn't resolve via existing aliases or `contacts.json`, the skill appends `<pushName>: <chatJid>` to aliases.json. Means future `wa <Name> ...` requests succeed without manual `--jid` plumbing.

## `~/triage/state.json`

Persistent cross-channel triage state.

Schema:
```json
{
  "_README": "...",
  "last_triage_at": "2026-05-08T20:18:08Z",
  "last_triage_unix": 1778271489
}
```

Used to scope each round's queries:
- Gmail: `is:unread after:<last_triage_unix> -label:triage/todo -label:triage/done`
- WA: `triage.js --hours <ceil((now - last_triage_at)/3600)>`

After every successful triage round, the skill updates `last_triage_at` to the round's fetch timestamp.

## Auto-done semantics

Default: every item shown in a triage round and NOT explicitly preserved by the user (via `N todo` / `N defer` / explicit `preserve N`) is treated as seen and gets:
- Gmail: `triage/done` label + UNREAD removed
- WA: `wa-state.json#done` entry with `lastInTimestamp` (re-surfaces only on newer incoming)

`triage/action` label is now obsolete in the round-based model — don't apply it. Either an item is fresh (no label, surfaced this round) or it's user-postponed (`triage/todo`) or it's done (`triage/done`).

`reply: <text>` actions also apply done after the send completes.

## Why this shape

User asked for two things on 2026-05-08:
1. "Save them as contact under that name they have" — solved by aliases.json + auto-population.
2. "Triage memory ... unless I tell it to preserve some it means that they have all been read ... only check unread mess. that came from then until now" — solved by state.json + auto-done.

The user explicitly cited "cheaper compute" as a constraint elsewhere — auto-done means most items don't need re-classification next round.
