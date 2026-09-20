---
name: feedback_output_goes_into_the_owning_system
description: "If one of our systems already owns a kind of work, the output goes INSIDE it, never into a fresh one-off page. Unsure which system owns it? Ask him on Telegram first."
metadata:
  type: feedback
---

His ruling, 2026-09-20, after I built a standalone travel page on :4143 when trippy already
existed, persists trips and runs context duels on them: *"ma perche non me l'hai fatto con
trippy???? questo tratto di ritorno DEVE essere un trip separato in quel sistema. il duello da
fare li."* Then, to the rule itself: *"yes bish. ask me on tg if you're unsure."*

**The rule.** Before building any new page, board or file, ask which of our systems owns that kind
of work. If one does, the output goes INSIDE it, in its own data shape, so it persists, accumulates
and keeps learning. A fresh page is read once and dies, and everything it learned dies with it.

| Kind of work | The system that owns it |
|---|---|
| Any travel search | **trippy**, `:4126`, one folder per trip in `travel-search/app/trips/<slug>/` (options.json + duels.jsonl + meta.json). Separate legs = separate trips, so each gets its own duels. Cross-trip preferences live in `preferences.json`. |
| A follow-up with a person | **coattio CRM**, `:4124` (intake `:4137`). The CRM owns every person follow-up since 2026-09-19. |
| Outreach boards, item-by-item review | **gtm-eng boards**, `:4141`, to the review-board design system. |
| Anything needing a yes/no from him | **approval hub**, `:4180`, reviewed on **hub-review** `:4142`. |
| An email draft | the **draft-review lane**: gmail draft + sidecar + `register.py` -> hub card. |
| A task | **task-land**, the daily page. |
| Durable knowledge | `vault_kb` (personal) / `medtech-brain` (Tundra). |
| A rule or a fact about him | **claude-memory**, this repo. |

A one-off page on `:4143` is legitimate ONLY when no system owns the work: a research document to
read, a study page, a throwaway comparison. Even then, the underlying artifact belongs in a repo
that syncs.

**And when unsure which system owns it, ask him on Telegram before building.** One question costs a
minute; the wrong container costs the whole compounding value of the work.

Related: [[reference_trippy_on_box]], [[project_coattio_v2]], [[reference_gtm_boards]],
[[reference_approval_hub]], [[reference_hub_review_ui]], [[feedback_review_page_design_system]],
[[feedback_travel_comfort_door_time]].
