---
name: feedback-every-email-draft-goes-through-the-lane
description: "Drafting an email is not done at `gmail.py draft`. Every draft must also get a sidecar and be registered with register.py so it lands on the hub as card #N."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3da174f5-ada2-42a8-959b-8bfe3be15b90
  modified: 2026-09-10T15:20:10.048Z
---

When Alessandro says "draft that email", the deliverable is **three things in the same turn**, not one:

1. A real Gmail draft (`gmail.py draft --account <acct> --body-file ...`, never clipboard, never a .txt).
2. A **sidecar** `task-land/_system/drafts/<draft_id>.md`: front matter (draft_id, account, subject,
   to, cc, thread_id, compose_url, created, status, language, revision, deadline, origin_session_*,
   message_id, origin) plus `## Context`, `## Sources for every factual claim in the body (H6)`, and
   `## Open questions for him`.
3. `python register.py <draft_id> --sidecar <draft_id>.md --origin laptop`, which runs the critic,
   applies its rewrite as a new Gmail draft, appends to `queue.jsonl` (the Drafts Chrome tab group)
   and posts hub card #N to Telegram.

**Why:** he asked for this explicitly on 2026-09-10 ("lets test this draft tab thing too, if it's not
what you were going to do, then make sure next time it is"). Left to itself the default is to stop at
step 1, which is the behaviour the lane was built on 2026-09-08 to replace. A bare Gmail draft gets no
critic pass, no source audit, no card he can answer `N dsend` to from his phone.

**How to apply:** every outbound email, every time, including short ones and replies. Report the card
number and the critic diff back to him; the critic is still an open A/B test, so say what it changed
and what it only flagged. Never send. See [[reference_draft_review_lane]],
[[feedback_email_draft_must_be_real_not_clipboard]], [[feedback_message_send_protocol]].
