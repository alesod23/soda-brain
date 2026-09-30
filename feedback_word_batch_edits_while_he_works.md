---
name: feedback_word_batch_edits_while_he_works
description: "While he works in an open Word file, no live COM edits or dumps; collect changes in a JSON batch and apply once, with comments, when he says so"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 6b54fab2-34e6-4bcb-adfe-551af6707920
  modified: 2026-09-30T20:03:02.062Z
---

On 2026-09-30 at 20:35, during the thesis push, he stopped live edits on the open thesis file (`FINAL REVIEW.docx`, OneDrive, AutoSave): each COM edit made his Word too slow. From then on, changes are written to a batch file (`thesis-attempt/final-review/round9*.json`, applied with `apply_round4.ps1`) and applied in one go, each with its comment, only when he says so.

**Why:** his words, relayed by the "TTT Thesis round 2" session: live edits made Word "too slow" while he was typing in it.

**How to apply:** when he is actively editing a Word file, do not run COM against it, and that includes the read-only `dump_live.ps1` (1.7 MB WordOpenXML). Reason from the text he pastes and from the last dump. Before applying a queued batch, check that the anchors still match his latest wording: `apply_round4` aborts the whole batch on one missing anchor. Two sessions writing to the same file at once also happened that day; keep one writer. Related: [[reference_word_com_accept_all_trap]], [[project_thesis_final_review_2026_09_27]].
