---
name: project_thesis_final_review_2026_09_27
description: "Thesis final-review run (27 Word comments \"Comment for final review\") started 2026-09-27; where the working files, the workplan and the output contract live"
metadata:
  node_type: memory
  type: project
  originSessionId: 6d6a4161-826b-4016-90da-5f2d7a0d8e7e
  modified: 2026-09-27T11:56:20.412Z
---

On 2026-09-27 Alessandro asked to execute the 27 Word comments he left in the thesis (most prefixed
"Comment for final review") and said he wants to FINISH THE THESIS ON SUNDAY 2026-09-27.

**Working files (his, never modify):** `C:\Users\Alessandro\OneDrive - HEC Paris\THESIS TUM\`
`doc2-TTT-2026-09-11-LINKED.docx` (the thesis) and `section-3.2-3.3-rewrite-2026-09-11-v4.docx`
(my rewrite, which he edited with track changes). The Drive `Downloads` copies are older.

**Output contract:** a NEW docx in that same folder (`doc2-FINAL-REVIEW-claude-2026-09-27.docx`)
with my edits as Word tracked changes, every comment kept and given a reply starting
"Claude reviewed"; fallback = new text yellow-highlighted, old text right after in red. He reviews
every change himself.

**Source of truth:** `C:\Users\Alessandro\thesis-attempt\WORKPLAN-20260927-final-review-comments.md`
(per-comment plan, scrutiny protocol, standing rules, resources) and
`thesis-attempt\FINAL-REVIEW-comments.json` (each comment with its anchored text). Snapshots of his
two files are in `thesis-attempt\final-review\ORIGINAL-*.docx`.

**STATE 2026-09-27 13:55: DELIVERED.** `doc2-FINAL-REVIEW-claude-2026-09-27.docx` is in the OneDrive folder (649 tracked changes by "Claude", 26 replies, original untouched), with `FINAL-REVIEW-CHANGELOG.md/.html` and `PINPOINTS-REMOVED.md`. Email to Sebastian = hub card #1, not sent. The run lost 10 hours to frozen agents, see [[feedback_unattended_run_never_wait_on_agents]]. Tooling to rebuild: `thesis-attempt\final-review\` (`build_final.py` + `edits_*.py`, `tc_engine.py`, `audit.py`, `word_check.ps1`, `make_replies.py`, `make_changelog.py`). Open for him: Ann 2018 / Ullrich 2020 / Fromer 2009 unread; size classes of the roster; leftovers listed in changelog section 4 (markers, draft notes, Appendix D residue, reference list gaps); Notion progress rows for 3.1.4 and 8.1 need renumbering (needs his yes). Word gotcha: never pipe the COM script into `Select-Object -First`, it kills the script and leaves a hidden Word holding the file and the user name set to "Claude".

**Why:** he wants loop-target / overnight level scrutiny and a reviewable diff, not silent edits.
**How to apply:** read the workplan first; draft, verify with an independent agent, then apply;
questions for Sebastian go through the email draft lane, never sent. Phase B of the workplan
(replace old 3.3, remove Seeling's 11 mentions) follows his instruction of 2026-09-11 and is
flagged separately because it was not a Word comment. Related: [[project_thesis_ttt_trip]],
[[project_thesis_checkpoint_2026_09]], [[feedback_thesis_seeling_and_cumulative_conclusion]].
