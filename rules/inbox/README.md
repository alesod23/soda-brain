# rules/inbox: how an orchestrator proposes a rule

Any agent with write access to this repo (instinct, a Claude Code session, a future harness) proposes a rule by adding
ONE markdown file here. The box picks it up within 5 minutes (`tools/rules_inbox.py`, cron), posts it to Alessandro
as a hub card, and on his yes files it in the right ledger with `addrule.py`; on his no it records why. The file is
never deleted: the outcome is appended to it, so the proposer can read what happened.

## File

Name: `YYYY-MM-DD-<short-slug>.md` (one rule per file). Content:

```
---
surface: email | hub | crm | notif | meeting
rule: one or two sentences, in English, saying what to do or not do, on which surface
quote: his exact words that caused it (if any; empty if the rule comes from observation)
by: instinct
item: the id of the thing it was about (a draft id, a card number, a person id), optional
soft: false
---
Why (optional): one paragraph of context, the case that triggered it, what went wrong.
```

- `surface`: email = any message to a person; hub = approval cards; crm = steps, Today, the reader; notif = what reaches
  his phone; meeting = Notion meeting notes to steps.
- `soft: true` files a judgement flag instead of a hard rule (the critic warns instead of blocking).
- Never a secret, never a person's contact details in the rule text; name people by their CRM id if needed.

## What happens

1. `tools/rules_inbox.py` (box, every 5 min) sees a new file, posts a card: "instinct proposes a rule (<surface>): ...",
   with the quote and the why in the card body, and remembers the card number in `~/.local/state/rules-inbox.json`.
2. He answers on Telegram or on the review page: yes (filed, `addrule.py --contract <surface> --rule ... --quote ...`,
   the next compile puts it in the skill), no + a sentence (declined, his sentence appended), or he edits the sentence
   (`change: ...`): the changed sentence is filed.
3. The outcome is appended to the file under `## outcome` (date, verdict, ledger id or his sentence) and synced back
   to GitHub within 5 minutes.
