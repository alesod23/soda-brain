---
name: project_thesis_checkpoint_2026_09
description: "Thesis state as of 2026-09-04 after the junior-supervisor call - read CHECKPOINT-20260904.md first; experiment is strong and significant, CITATIONS + over-reliance on his interviews are the open flank."
metadata: 
  node_type: memory
  type: project
  originSessionId: 6d6a4161-826b-4016-90da-5f2d7a0d8e7e
  modified: 2026-09-09T17:07:51.397Z
---

# Thesis checkpoint, 2026-09-04 (paused, resumes in a few days)

**Read `C:\Users\Alessandro\thesis-attempt\CHECKPOINT-20260904.md` first.** It holds the full
state: file map, call answers, the four Word comments with their anchors, and the next actions.

**2026-09-09 (TTT build, section 0 of the checkpoint):** all five comment items implemented; four
strict-reviewer agents rewrote every chapter in place; **39 `{source needed}` markers** left in the
text (yellow in the DOCX) for him to fill by hand. Three substantive corrections: §5(2) ArbnErfG was
misquoted (statute says *hat ... zu beschreiben*, not *soll ... darstellen*); Table 6.7's two
"enriched lower" directions were NOT pre-registered, so two-sided p recomputed (PatentSBERTa 0.020
survives, BERTScore 0.187 does not); §7.1 still claimed no significance. Benchmark master's theses
from IP-law chairs all use **footnotes with pinpointed Board of Appeal and BGH citations, 15-26
decisions each**; ours has two, unread, plus eight US cases, and no German commentary. That is the
biggest remaining gap. Offline pack at `thesis-attempt/sources/index.html`.

Fast orientation:

- **Base = doc2 lineage only.** Edit `drafts/ch*.md`, then `make_doc2.py` / `make_skeleton.py`.
  Supervisor's commented copy: `OneDrive - HEC Paris\thesis-tum.docx`.
- **The experiment is strong and statistically significant** (fixed 2026-09-04 by analysis, not
  new data): exact per-patent permutation tests + Fisher. Blind rubric p = 3.0e-06; PaECTER full
  p = 0.039; claims-similarity drop p = 0.0017. Both halves of the dissociation now significant
  in opposite directions. 80% power would need 8 completed pairs (currently 5).
- **THE OPEN FLANK IS CITATIONS**, not the experiment. Quality, quantity and type of sources are
  still to be reviewed. Next step is a red-team of the bibliography against IP-law-chair norms
  (share of primary legal material vs commentary vs CS/NLP papers), plus finding a benchmark
  thesis written **under an IP-law chair with an AI angle** - deliberately NOT the Caleb/Seeling
  shape, which is a CS-chair thesis with an IP topic. He wants to read the mirror image.
- **THE INTERVIEWS ARE OVER-USED (2026-09-05).** The thesis must stand on its own with every
  personal interview REMOVED and still meet the source-count/quality bar; interviews are an
  optional plus, still to be approved. 41 attributed `(interview notes, ...)` citations exist in
  the doc2 sources. Next session: walk `thesis-attempt/INTERVIEW-INVENTORY.md` mention by
  mention, state the phrasing and the claim it carries, he approves or rejects each one, and an
  approved one keeps its excerpt visible. Never batch this.

- **Settled in the call, do not reopen:** EU/US source mix is fine; one worked example in the
  appendix is fine with a disclaimer; 80 pages +/- 10%; Times New Roman 12pt, 1.5 spacing,
  3.5 cm left margin.
- **Four Word comments to action:** move the AI-use disclaimer to the end next to the declaration
  of ownership (see "Sebastian's example"); abstract is optional; justify why *these six* patents
  and the resulting limitation (§5.1); make §8.2 loop back to the Ch. 2-3 legal background.

**Why:** the project pauses for several days and the state is too large to reconstruct from the
transcript; the checkpoint file is the handoff.
**How to apply:** open the checkpoint file before any thesis work; keep it current as things move.
Related: [[feedback_thesis_seeling_and_cumulative_conclusion]], [[project_thesis_system]].
