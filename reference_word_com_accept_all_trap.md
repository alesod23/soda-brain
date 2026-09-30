---
name: reference_word_com_accept_all_trap
description: "Word COM: Range.Revisions.AcceptAll() on the document's last paragraph accepted EVERY tracked change in the file; accept one revision at a time; Undo via COM reverses it"
metadata:
  node_type: memory
  type: reference
  originSessionId: 6d6a4161-826b-4016-90da-5f2d7a0d8e7e
  modified: 2026-09-30T13:28:18.094Z
---

Word automation traps met on the thesis file (2026-09-30), all in the document he had open:

- `$range.Revisions.AcceptAll()` on the last paragraph of the document accepted all 663 tracked changes of the whole file and removed 25 comments that sat on deleted text. Never call `AcceptAll`/`RejectAll` on a range. Accept one by one: `$rng.Revisions.Item(1).Accept()` in a loop, after checking that the revision's Range lies inside the target, and compare `$doc.Revisions.Count` before and after against the number expected.
- Recovery that worked: `$doc.Undo(1)` in a loop, reading `Revisions.Count` after every step, stop when the count is back (19 steps); if it never comes back, `$doc.Redo(n)` returns to the start. Do it at once, before he edits on top.
- Looping `$doc.Revisions.Item($i)` over the whole document is quadratic: 10 minutes without finishing on 660 revisions. Use the range's own `Revisions` collection.
- A file opened from OneDrive/SharePoint with AutoSave signs tracked changes and comments with the Office account ("Alessandro SODANO"), whatever `Application.UserName` says. My changes then carry his name; filter by time stamp, never by author.
- `Range.Information(3)` page numbers differ from the pages of an export without markup; export a block with `$range.ExportAsFixedFormat($pdf, 17, $false, 0, $false, 0)` instead of page numbers.
- A table is copied without the clipboard with `$dest.FormattedText = $table.Range.FormattedText`.
- Before any multi-step edit of his open document, copy `live.xml` (the `Content.WordOpenXML` dump) to a dated snapshot file.

Related: [[project_thesis_final_review_2026_09_27]], [[feedback_thesis_no_search_voice_real_summaries]].
