---
name: feedback_deck_pdf_needs_print_snapshot
description: A Claude Design .dc.html deck can never be printed to PDF directly — deck-stage is a one-slide-at-a-time viewer whose shadow !important beats author CSS; always build a print snapshot first.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1984c76b-671e-4733-b9d6-3b2db89db8bd
  modified: 2026-08-04T15:32:56.381Z
---

Rendering ANY Tundra `.dc.html` deck to PDF: **do not point Playwright at the deck.** Build a
**print snapshot** first. Two blockers, both diagnosed 2026-08-04 (cost ~5 failed renders):

1. `<deck-stage>` is a **presentation viewer**, not a layout. Its shadow CSS is
   `::slotted(*){position:absolute!important;inset:0!important;visibility:hidden}`, only
   `[data-deck-active]` visible. Shadow-tree `!important` **beats** author `!important`
   (importance reverses the cascade for `::slotted`), so injected CSS can never win. Symptom:
   every slide scaled to ~0.85 and stacked on one page.
2. Under `file://`, CORS blocks the runtime's `fetch` of `deck-stage.js`, so the element never
   upgrades, slides lose `position:relative`, and absolutely-positioned footers/page numbers
   escape and **overlap across slides**. Serve over **HTTP** instead.

**The snapshot recipe** (see `~/tundra-design/library/pilot-hospital-x-de/NOTES.md` for the worked
version + the `render.js` that starts its own throwaway static server):
- `<x-import …deck-stage…>` → plain `<div class="printdeck">`
- `<image-slot>` → plain `<div>`, else the real photo is replaced by a "Drop image here"
  placeholder (an archived deck has no `.image-slots.state.json`)
- add `<meta name="omelette-owns-print">` **and strip every `@page{size:…}`** — otherwise the deck
  runtime stamps its own page box and the PDF comes out **portrait 540×960** instead of landscape
- pin `.printdeck > section.slide` to 1280×720, `position:relative`, `break-after:page`
- Playwright on system Chrome (`channel:'chrome'`), `page.pdf({width:'1280px',height:'720px'})`

**Verify before claiming done:** open the PDF with `fitz`, assert page count == slide count and
`rect == 960×540`, and render 3–4 pages to PNG and actually look at them. The portrait bug and the
overlapping-footer bug both produce a valid-looking PDF of the right page count.

Related: [[feedback_deck_source_fingerprint_and_render]], [[reference_design_lib]],
[[feedback_tundra_deck_workflow]].
