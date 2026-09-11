---
name: project_thesis_ttt_trip
description: Thesis train to Termoli (TTT) departs 2026-09-11 at 06:15; everything must be offline-ready before then. Where the offline pack and the Drive mirror live.
metadata: 
  node_type: memory
  type: project
  originSessionId: 6d6a4161-826b-4016-90da-5f2d7a0d8e7e
  modified: 2026-09-11T13:55:01.061Z
---

**The trip starts 2026-09-11 at 06:15.** From then Alessandro is on a train with no reliable
internet for a long stretch, doing the "human side" of the thesis: rewriting sections by hand,
reading sources in full, judging the interview citations one by one.

Everything he needs offline lives in two places:
- Local, always on disk: `C:\Users\Alessandro\thesis-attempt\` (entry point `sources/index.html`).
- Google Drive mirror, structured for the trip: `G:\My Drive\thesis-attempt\` with
  `00-READ-ME-FIRST.html`, `01-REVIEW-ON-THE-TRAIN`, `02-DOC1-AND-COMPARISON`,
  `03-EXPERIMENT-DATA`, `04-ARCHIVE-OLD-VERSIONS`, `05-CHAPTER-SOURCE-FILES`.
  He must mark the folder "Available offline" in Drive for Desktop himself.

He asked (2026-09-10) to also review draft ONE (`drafts/doc1-claude-deep.md`, parked since
1 September) against draft TWO (the working base), as a Google Doc with margin comments explaining
the differences, for inspiration on approach, citations and text.

**2026-09-11 01:50, the file he now works in:** `doc2-TTT-2026-09-11-LINKED.docx` (his 00:52 edit
of the v2 file with every source hyperlinked: 245 links to local PDFs in the Drive mirror, 54 online,
all tested; Seeling 2026 unlinked). Copies in `G:\My Drive\Downloads\`, `thesis-attempt\deliverables\`
and the 01 mirror. He edits the docx in Word from `G:\My Drive\Downloads` (Word's "Downloads"
location is the Drive folder, not `C:\Users\Alessandro\Downloads`). Regenerate links after his edits
with `hyperlink_sources.py <in> <out> report.md source_urls.json`, test with `verify_hyperlinks.py`.
His second train leaves around 05:00 on 2026-09-11 ("in 4 hours" said at 01:00).
Notion progress checklist (75 to-dos, one per chapter/sub-chapter), under his private "Thesis" page
in the Tundra Health workspace: https://app.notion.com/p/3d8b30c6d57e816ab649e0b8acb0ef77 . Created via
headless `claude -p` with the Notion MCP because the session's own Notion connection had failed.

**Why:** he may still message before 06:15; after that assume he is offline and cannot fetch
anything. Do not start work that needs him online after that time.
**How to apply:** before 06:15 on 2026-09-11, any deliverable must land in the Drive mirror AND
locally; after that, prepare things for when he is back. Related: [[project_thesis_checkpoint_2026_09]].
