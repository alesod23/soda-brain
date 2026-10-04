---
name: reference-crm-mirrors-open-hub-draft-cards
description: An open hub email/LinkedIn draft card about a CRM person is mirrored (latest revision) onto that person's CRM review item every 10 min and before the board generates; the CRM never writes a second draft beside a card
metadata:
  type: reference
---

crm-review Vincent Carte-Jacquesson, 2026-10-04: "I've iterated more on the approval hub, and this is not really
reflecting the parallel card in the approval hub." Hub card #19 (2 Oct) predated PLAN 10(c), and `send_card.py`
attaches to the CRM only when it opens a NEW card, never on `/revise`, so the CRM wrote its own v1.

- `~/.medtech-crm/review-artifact.js mirrorHubCards({pid?})`: GET hub /pending, open `email-draft`/`linkedin-draft`
  cards with `meta.draft_id` + `meta.body`; pid = sidecar `crm_pid` else the single row holding `meta.to`; calls
  `attach({..., source: 'card #N', hub_card_id, allow_coming: true})`. Idempotent on draft_id; revisions update in place.
- Callers: `intake-server.js` tick (1 min after boot, every 10 min, writer only); `review-api.generate()` before Opus
  (not for a rewrite or a hygiene update; `opts.noHub` skips it).
- Refusals are normal and leave the card alone: 409 not due within the week, 400 the row has no address on that
  channel (the "add this person" cards for Vittoria / Donarini).
- The card stays open; a CRM approve sends the same Gmail draft (`drawer-api sendLaneDraft`, attachments kept) and closes the card.
- Test: `node --test review-artifact.test.js`. :4137 must restart to load the tick.

Related: [[project_crm_is_the_followup_surface]], [[reference-hub-yes-words-reach-crm-review]], [[reference-approval-hub]].
