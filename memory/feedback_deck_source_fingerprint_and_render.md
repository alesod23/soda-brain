---
name: feedback_deck_source_fingerprint_and_render
description: "To translate/edit a deck to match a target PDF, fingerprint-verify the real source; verify the rasterized PDF, not element screenshots."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e29d7091-5808-492a-b725-082f5123e799
  modified: 2026-07-22T00:38:50.800Z
---

Two failures on the 2026-07-22 Tundra Asti-proposal job, both to prevent going forward.

**1. Wrong source deck.** I translated a same-named editable `.dc.html` that had drifted away from the target PDF. Filenames inside a Claude Design project drift and editables get edited AFTER a PDF is exported — **only the `project_id` is stable**, and the exact match may be a frozen `*-print-<hash>.dc.html` snapshot, not the editable.
**Why:** I inferred the source from a filename/memory instead of checking; `DECK-SOURCES.md` had no row for that PDF yet.
**How to apply:** Before redoing any deck to match a PDF, pull the PDF's unique text (slide-2 title, a stat line, the source-note line) and **grep every `.dc.html` in the project(s)** for those strings. Use the file that actually contains them. Then record it in `DECK-SOURCES.md` AND embed the source in the PDF's metadata `subject` (survives rename/move). See [[reference_tundra_bridged_deck_source]].

**2. Verified the wrong thing.** I checked Playwright `element.screenshot()` crops (which ALWAYS look perfect because they crop to the 1280×720 element) instead of the actual PDF. The PDF pages came out mis-sized (Chrome `page.pdf` swapped/ignored landscape geometry; the print snapshot's `@page{margin:0.5in}` also fought it).
**How to apply:** Always rasterize the FINAL PDF with PyMuPDF (`fitz` → `page.get_pixmap()`) and eyeball a real page before declaring done. For these Tundra 1280×720 decks, the reliable render is: screenshot each `section.slide` at deviceScaleFactor 2 → assemble with fitz `new_page(width=1280,height=720)` + `insert_image`, and **JPEG-compress** the images (q86, resize ~1920×1080) or the PDF balloons to >100 MB. Related: [[feedback_tundra_deck_workflow]], `~/.claude/commands/tundra-de-en/SKILL.md`.
