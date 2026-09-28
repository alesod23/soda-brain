---
name: reference-review-staged-commit
description: "CRM Today review since 2026-09-28 - a/s/c/r are HELD until commit (x removes), commit sends + digest reads each sentence (case / confirms rule / new rule / system), three groups on the board"
metadata:
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-28T14:04:23.355Z
---

His words, 2026-09-28: "im quickly going to get to 500 Hrules by this pace, so thats a problem ... the moment i send
a comment its a rule ... id rather do a little push commit each time, so ik when to look for results of my feedback
... make the prev comment/event deletable with an x next to it, only sent when committed ... everytime i do a/s and
commit, they go into a 'dealt with' part of the review which is down."

**How the review works now** (`~/.medtech-crm/review-api.js`, `crm-app/public/review.js`):
- `POST /review/verdict` only HOLDS (`r.staged`), nothing is filed, logged or rewritten. `POST /review/unstage` = the
  x. The commit button counts everything held ("Commit 3").
- `POST /review/commit`: decisions logged, approved messages sent, skips closed ("remind me in a couple of days" =
  out until that day, `snoozeDays`), then `digest()` in the background: ONE Opus read of all committed sentences
  with the three ledgers in front of it. Each sentence is `case` (kept in `r.case_notes`, read by the generator for
  that person), `rule` with `duplicate_of` (a line in `_system/rule-confirmations.jsonl`, no new rule), `rule` new
  (addrule.py), or `system` (`_system/gtm-agent/system-feedback.jsonl`, shown in the agent's updates until closed).
  Cards whose message must change are rewritten by themselves.
- Board groups, in this order, with separators: to review, "Commented, waiting for my work", "Dealt with today".
  The counter up top counts only the first group.
- "Generate missing" shows only with "upcoming too"; today's items are written by themselves.
- A failed load retries every 3 s and keeps "Exit review" on screen (review mode hides the menu).

**First real run:** his 8 sentences of 28 Sep had each become a rule (H79-H86). Through the digest: 1 new rule (H87,
name the open deliverable), 2 this person only, 4 system requests. The eight raw rows were moved to a RETIRED section
of EMAIL-REVIEW-CONTRACT.md. Rule of thumb for me: a sentence from a review is never filed with addrule.py directly
any more; it goes through the commit.

**Found on the way:** every Alt+L re-capture was logged as a new LinkedIn connection request (Emelyne Weimer "3
requests", 42 people, 107 lines). Fixed in `ingest-intake.js` and in the data (backup `crm.json.bak-20260928-recaptures`).

Related: [[project-crm-review-loop-vision]], [[reference-rule-loop]], [[reference-channel-search]], [[reference-system-agent]].
