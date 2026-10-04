---
name: reference-reply-check-before-draft
description: "Whether a CRM person replied is decided by code (M.replyOwed, M.inboundLines in model.js), never by a step text or the raw reply_owed flag; the review generator rejects drafts that thank for a reply not on file (Amy Fischer, H101, 2026-10-04)"
metadata:
  node_type: memory
  type: reference
  originSessionId: 879703ca-03ba-4195-8f02-ae93a57452dd
  modified: 2026-10-04T03:35:09.319Z
---

`~/.medtech-crm/crm-app/public/model.js`: `replyOwed(p, facts)` returns `p.reply_owed` only while it is real (its event is not an outbound line on the row, and nothing went out on or after its day); `inboundLines(p)` = the messages FROM THEM. todayFlags, `crm-app/reader.js` and `review-api.js` read these, never `p.reply_owed` directly. Both prompts carry a code-checked line ("Messages FROM THEM on file: NONE" / "=== DID THEY REPLY? === NO"). `review-api.js generate()` rejects a text matching `ASSUMES_REPLY_RE` (thanks for getting back / your reply / grazie per la risposta / merci pour votre retour ...) when no inbound is on file: one retry, then an error, so no such draft is served.

**Why:** 4 Oct 2026 crm-review, Amy Anne Fischer: "the draft that you created was bad because it assumed that this person answered, and she didn't". His own LinkedIn DM was stored as her reply (fromMe bug in li_inbox.py, fixed the same night by repair-fromme-20261004.js), and the repair left `reply_owed` on 4 rows, so Today still said "answer X".

**How to apply:** a repair that turns an inbound line back into outbound must also clear `reply_owed` (see `tools/clear-void-reply-owed-20261004.js`). New code that asks "did they reply?" calls `M.inboundLines` / `M.replyOwed`. Test: `node --test tests/no-reply.test.js`; check one person with `node review-api.js prompt <pid> | grep -A2 "DID THEY REPLY"`. Drafting rule H101 (EMAIL-REVIEW-CONTRACT.md).

Related: [[project-crm-review-loop-vision]], [[reference_owed_todos_in_crm_prompts]].
