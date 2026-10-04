---
name: reference-hub-yes-words-reach-crm-review
description: His words on a YES of a meeting/handoff hub card are the brief of the CRM step; stored as p.handoff_feedback and printed (binding) in the review prompt with the meeting record
metadata:
  type: reference
---

crm-review Sebastiano Caravaggi, 2026-10-04: "why is it in French? ... the card on the approval hub is so much better
than this." The hub card was better because his yes on #20 carried the brief (Italian, margin, tailored deck) and the
CRM kept only the step line.

- `~/.medtech-crm/handoff-api.js verdictPoll`: a yes now stores `handoff_feedback` (was only kept on a no).
- `review-api.js buildPrompt`: `handoffWordsBlock(p)` (binding while `next_step_origin.set_by === 'handoff'`) and
  `meetingBlock(p)` (`p.last_meeting` he_owes / they_owe + row `context_facts` when no relationship_state).
- `crm-app/channel-search.js OWN` excludes meeting-note bots (read.ai `executiveassistant@`, otter, fireflies, fathom,
  tldv, granola, notion, calendly): a bot address once became a person's email.
- A transcript where only his side was captured has no figures of theirs: never quote numbers he asks for that are
  not on record; say so in what_why.
- Test: `node --test tests/handoff-words.test.js`. :4137 must restart to load it.

Related: [[project-crm-review-loop-vision]], [[reference-review-staged-commit]], [[reference-approval-hub]].
