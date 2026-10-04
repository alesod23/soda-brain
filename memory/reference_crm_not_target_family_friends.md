---
name: reference-crm-not-target-family-friends
description: "Family and personal friends in the CRM carry p.not_target {why: family|friend}; every producer (todayFlags, reader, monitor, review digest, inbound_asks, due_today, instinct_inbox) skips them. Built 4 Oct 2026 after Guido Sodano (his father) got a reply draft."
metadata:
  node_type: memory
  type: reference
  originSessionId: 1018da9d-7f3a-4cec-96fa-8d25c023bdef
  modified: 2026-10-04T03:56:45.747Z
---

A CRM row with `not_target = {why: 'family'|'friend', note, rule: 'crm:H52'|'crm:H53', at}` is a contact, never a follow-up.
`M.notTarget(p)` in `~/.medtech-crm/crm-app/public/model.js` makes `todayFlags` return null (Today, review items, today-count);
`crm-app/reader.js` (queue tick + nightly pass) and `monitor.js eligible()` skip it; `gtm-eng/agent/inbound_asks.py not_target()`
returns before the Opus judge (matches email, phone, identifier_candidates, the `wa.me/<lid>` in notes, full name);
`due_today.py` and `instinct_inbox.py` skip it. Setting it: the review digest returns `not_target` for a "he's my father / a
friend" sentence and calls `review-api.js markNotTarget(pid, why, quote, rule)` (closes the step, clears reply_owed). By hand:
`node -e "require('./review-api.js').markNotTarget('<pid>','family','<his words>','crm:H52')"` from ~/.medtech-crm.

**Why:** 4 Oct 2026 crm-review, Guido Sodano: "He's my father, so that's something I'd rather catch up on myself." H52/H53
had been filed as rules but no code read them; the reader re-set "answer Guido" after his comment.

**How to apply:** a new producer that proposes steps or cards for a person checks `not_target` next to `state === 'dead'`.
No phone-call source exists yet (WhatsApp calls not captured by wa-daemon, cellular invisible): "you talked since" only sees
calendar / Notion meetings and logged call_done. Test: `node --test tests/not-target.test.js`.

**Before any row exists (added 4 Oct 2026, Nick's second sentence):** `inbound_asks.py saved_name(key)` reads the name he
saved the WhatsApp chat under (`~/.claude/wa-daemon/lid-overrides.json`, `aliases.json`, `contacts.json`; e.g. "Nick CDTM S26")
and the judge prompt gets it; the judge returns `personal: true` for a cohort/family-tagged saved name + casual chat with no work
ask, and handle_chat / handle return "personal" (log event `personal`, no row, no step, no card). Test:
`python tests/test_personal_chat.py` in ~/gtm-eng/agent. `inbound-asks.jsonl` event=personal lists every skip (check it if a real
ask from a CDTM peer goes missing).

Related: [[reference-reply-check-before-draft]], [[project-crm-review-loop-vision]].
