---
name: project_crm_is_the_followup_surface
description: "His decision 4 Oct 2026 03:48: the CRM is where every follow-up with a person is decided and sent; the box becomes the CRM writer (laptop a replica); the hub keeps non-person items and 'add this person?' cards; the CRM inherits the hub pipeline (lane, hygiene worker, Updates page, ping once). Why, the measured overlap, where the build stands."
metadata:
  type: project
since: 2026-10-04
---

**The decision (his words, 4 Oct 2026 04:00):** "the crm is where i want to send followups. you are to do all your
suggested fixes. including the crm writer on the box. we keep the option to add a person to a crm if relevant (i'll
start teaching you as part of the rules when to ask me vs just do it, vs just do not do it, from the hub). i also want
to give the crm that same on phone availability. so we're going to have it run in the same way as the hub on the
server." It supersedes the mirror he chose an hour earlier (both surfaces linked, hub version shown on the CRM).

**Why:** measured at 03:27 the two surfaces overlapped by accident, not design: CRM Today 33 items, 38 open cards, 6
persons on both, 2 competing proposals (Guido: email vs a WhatsApp card; Vincent: a stale French CRM v1 vs the
critic-checked hub draft #19). A CRM item carries no card id; a card carries the pid only when its producer set
`meta.crm_pid`; two verdict ledgers, two executors (`DA.sendNext` vs the hub `executeAction`), two rule-filing paths.
The hub exists because the CRM writer is a laptop that sleeps.

**The build order (THE PLAN item 10 in `task-land/_system/WORKPLAN-20261001-soda-brain.md`):** (a) conflict #10
merged per record (done 04:07, `soda-brain/tools/crm_merge_conflict.py`); (b) the writer flip: `COATTIO_WRITER=box`
one switch, the laptop server a proxy/replica, every laptop tool keeps 127.0.0.1:4124 (branch `writer-flip`, worktree
`~/.medtech-crm-flip`; cut-over recipe in the flip design: merge first, commit with default laptop, shadow checks on
the box, hard cut at a quiet hour, rollback = one env var); (c) producers attach to the person's review item instead
of posting a card; (d) the CRM inherits the lane, a hygiene worker twin of `hub_outdated.py`, an Updates page (CRM
H51), ping once through the hub; (e) the phone opens review mode on the box `:4124`; (f) big jobs: a comment that is
work becomes `_system/jobs/<id>.json` run by `job_runner.py` as a multi-agent orchestration, the card stays
change-queued until the artifact is linked.

**How to apply:** never add a second writer of `crm.json` (the 3-4 Oct split came from the box accepting phone edits
while the laptop wrote); a person's follow-up is decided on the CRM, a card about a person is a link to it, not a
second proposal; a CRM draft goes through the lane like any other. See [[reference_soda_brain]],
[[reference_review_staged_commit]], [[feedback_hub_digest_replaced_by_review_page]].
