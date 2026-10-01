---
name: feedback-us-hospital-english-review-loop
description: "English deck versions for US hospitals get US hospital terminology, checked by a reviewer loop until a pass returns nothing"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 6348fc75-8a1b-4478-85e9-3ebb6e4556d4
  modified: 2026-09-29T21:15:47.613Z
---

When a Tundra deck goes to a US hospital (first case: UPMC pitch, 2026-09-29), translate every medical / technical / clinical-engineering / hospital-ops term into the term a US hospital worker is used to seeing, and verify it with a review LOOP: a fresh reviewer agent flags non-US terms as JSON, I apply, a new reviewer re-checks, repeat until a pass returns [].

**Why:** his words: "translate with a review with a loop that checks until every term ... is translated into its American English counterpart".
**How to apply:** examples the loop caught: PoC -> pilot, patient data -> PHI, operator error -> use error / no problem found, procurement -> supply chain, call a technician -> call biomed, PM visits -> PMs, bedside exams -> portable exams, loaner (vendor's) vs backup unit (own), renewal file -> renewal package, Month Day, Year dates, "yrs" not "y", "Article 28" not "art. 28", $ in illustrative figures, "in Italy" on Italian stats. Also swap the hospital name and EU-only claims (Hosted in the EU -> US or EU). **Toggle = English by default + a VISIBLE on-slide EN/IT switch, verified on a fresh load of the copy in the project.** On 2026-09-29 I reported "done" while the page opened in Italian: `<html data-lang="it">`, the prop defaulted to Italiano, the localStorage key was shared with Humanitas, and the language component was the SECOND `data-dc-script` (support.js reads only the first, so the side-panel setting never worked). His reaction: "EVERYTHING IS IN ITALIAN". Test with an empty browser profile before claiming it is translated. Tooling from that run (`fix_lang.py`, `test_toggle.py` alongside): `tundra-design/sync/out/ale/upmc-pitch/apply_review.py`. Related: [[project-upmc-demo-brief]].
