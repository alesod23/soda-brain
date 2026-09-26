---
name: project-crm-review-loop-vision
description: His 2026-09-26 vision for the CRM (take himself out of the loop, deals, review-and-correct iteration) and the Today review mode built that day as the first concrete step
metadata:
  type: project
---

**His vision (2026-09-26, handwritten notes + voice, verbatim essentials).** "Taking myself out" of the three CRM
use cases: a campaign runs until a call is fixed; his own human work (calls, in person) is recorded into the same
workflow; both land in DEALS (a first call happened, next steps, follow-ups, who owes what). The CRM = "the central
system in which we have the information and the history of a conversation with a person" (the Kortyx / Cortex
method). Iteration: "a system where I see some results, I correct them manually, I gain the discipline to tell you
exactly how I'm correcting them ... automatically get closer to the level or realize we're not getting too close and
then reimagine how we're doing it ... where I don't have to put hands to a system ever again." The corpus (what he
actually sends) is the source of truth: always compare proposed vs sent, form hypotheses, validate as we go. His
notes: the CRM works a QUEUE, pulls every conversation, records/scores the previous step; idle until the call is
fixed; then "send high quality follow up w mix of PROACTIVE and PUSHY vs KIND/HUMAN/STUDENT/ENTHUSIASTIC YOUNG";
UPDATES + DRAFTS = the BRAIN, MATERIAL created on the go; NEXT: email replies/threads correct, QUICK REVIEW,
Tinder-like cards driven by RULES on WHEN to follow up and WHAT to follow up with.

**Built the same day (first concrete step): Today REVIEW MODE.** `~/.medtech-crm/review-api.js` + intake routes
`/review/*` + `crm-app/public/review.js` (hooks Today; button "Review" on the band). One item = one screen (design
system), left = who / step / WHY NOW (origin, open loop, rhythm, state), right = the follow-up Opus wrote for the
step (the two compiled skills inlined + relationship_state + events + 3 of his sent messages) with a/s/r/c: a verdict
is never blind (box with pills sucks | like | change and message | timing); a sentence becomes a rule the same turn
(`addrule.py --contract email|crm`, `--like`), a change request lands in the workplan; r = rewrite with the sentence
(new version, old one in the pane). ← opens the WHY pane: why now, why this content, why this style, "if I were more
proactive", rules used, previous versions, his comments, hypotheses, links to the skills / ledgers / the exact
prompts. Commit = the yes: approved items go out through the drawer's Send path and close the step. Nightly
`compare()`: proposed vs what he actually sent -> `review/compare.jsonl` -> Opus hypotheses in
`review/hypotheses.json` (proposed / confirmed / refuted), shown in the pane; `checkLine()` for the system check.
Workplan: `~/.medtech-crm/WORKPLAN-20260926-today-review-mode.md` (pipeline section = the rest of the vision).

**How to apply:** the review board is where he judges the CRM now; every sentence he gives there is already filed.
Next steps in the pipeline (not built): deals as objects, his human work recorded by voice into the row, the corpus
loop as the judge of every generator, a "proactive by default" test period.
