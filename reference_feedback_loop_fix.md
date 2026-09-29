---
name: reference_feedback_loop_fix
description: A sentence he types on any review surface gets FIXED like a sentence told to a session (2026-09-29): sorter + shared queue + live session first, unattended worker as the safety
metadata:
  type: reference
---

His ruling 2026-09-29: "if i send this as a skip comment in the approval hub, will that be enough for it not to reoccur? ... it should be. i dont want to have to come here, yet i want it fixed". Order: 1 a live session (the savior claims it and hands it to an open laptop session, or fixes it on the box); 2 laptop off: box part now, laptop part waits; 3 nobody in 45 min (savior down, no session): the unattended worker on the laptop, full permissions ("i want a safety that just does 1").

Pieces: `gtm-eng/agent/feedback_worker.py` (task DA-FeedbackWorker, every 10 min): reads his words from `task-land/_system/decisions.jsonl`, sorts each with Opus into case / rule (filed with addrule.py) / system, writes `task-land/_system/gtm-agent/system-feedback.jsonl`; `feedback_queue.py` in the same folder = the shared view (`list`, `claim`, `done`, `needs-him`, `release`), events in `system-feedback-events.jsonl`, both merge=union, never edited by hand. One hub card per finished item, whoever finished it. hub-review's tabs GTM agent and Updates feed the same path (surface gtm-agent).

**Gotchas:** the worker's sorter placeholder is `__HIS_WORDS__` (a wrong name sorted everything as "none" on the first test); registering the worker task was refused once by the permission check and went through after his explicit yes; the memory-starved laptop makes each model start take minutes.

Related: [[reference_system_agent]], [[reference_hub_review_ui]], [[reference_rule_loop]].
