---
name: feedback_thesis_seeling_and_cumulative_conclusion
description: "Thesis feedback 2026-09-03 - scale back Seeling (co-founder) citations a lot; conclusion must be cumulative on existing patent-quality/role-of-patents literature, not a fresh argument; doc2-latex is the working base."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6d6a4161-826b-4016-90da-5f2d7a0d8e7e
  modified: 2026-09-03T02:41:19.588Z
---

Three standing decisions from Alessandro (2026-09-03), on the HEC x TUM thesis drafts ([[project_thesis_system]]):

1. **Seeling citations: scale back a lot.** The drafts cite the co-founder's sibling thesis (Seeling 2026) ~17 times in doc2. Too much. Keep the Ren-Seeling measurement tension (it is load-bearing for the metric-validity finding) but stop leaning on Seeling as recurring authority elsewhere. He is also asking the junior supervisor whether citing it is acceptable at all ("or too weak?") - apply the cut after that answer, harder or softer accordingly.
2. **Conclusion (Ch. 8) must be cumulative, not a new argument.** Build visibly on existing research: patent quality literature, role of patents in society, and studies/simulations of the patent system under stress (e.g. Machlup 1958, Merges & Nelson 1990, Wagner 2009, Boldrin & Levine 2013, Torrance & Tomlinson 2009 patent-system simulation). Stay "for a little bit" on that literature before adding anything of our own.
3. **doc2-latex is the working base** ("Doc True Latex"), not doc1 - only because it is the one he reviewed first and trusts; doc1 may return later. Any thesis edits go into the doc2 lineage first.

**Why:** supervisor-facing credibility - a thesis conclusion that ignores the canon reads as ungrounded; over-citing your own co-founder reads as weak sourcing.
**How to apply:** before any rewrite of ch8/ch9-conclusion or Seeling-touching sections, re-read this; edits target drafts/ch*.md then rebuild doc2 via make_doc2.py + md2tex/md2docx.
