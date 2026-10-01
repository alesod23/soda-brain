---
name: reference-channel-search
description: "CRM H36 - a person with a step and no channel is a search task; channel-search.js, identifier_candidates shown on the review card, Approve confirms"
metadata:
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-28T12:25:39.126Z
---

His words, 2026-09-28, on Christopher Zubiate's card saying "no channel on file": "did we not establish his contact?
... its clear that we have a weak kortyx like system, because its missing a loop/goal objective of searching deeply
for the things on which its missing something."

What had happened: the monitor HAD found his number on 27 Sep (WhatsApp push name) and parked it in
`identifier_candidates`, which nothing showed and nothing used. A found detail that nobody sees is the same as not
found.

**Since 2026-09-28:**
- `~/.medtech-crm/crm-app/channel-search.js` searches WhatsApp (direct and groups), every Gmail account with a token,
  task-land notes and the CRM for everyone with a step and no email, LinkedIn or phone. Finds go to
  `identifier_candidates` with their source; `p.channel_search` records where it looked. Run hourly by the system
  agent; a person is searched again after 24 h. A first name alone never identifies unless one number carries it and
  its messages name the person's context.
- The Today review card shows "found, not confirmed yet: <value> (source)", writes the message for that channel, and
  his Approve writes the detail on the person (`review-api.js candidateChannel / applyCandidate`). Standing rule kept:
  found details are proposed, written after his yes.
- Review mode is full screen (CRM H35): no menu, no counters, bigger type, "Exit review" or Esc.

**How to apply:** never let a card say "nothing on file" without a search record next to it. Anything found goes in
front of him on the surface where he decides, the same run.

Related: [[feedback-found-contact-details-go-to-crm]], [[project-crm-review-loop-vision]], [[reference-system-agent]].
