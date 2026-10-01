---
name: feedback_transcript_artifact_format
description: "Standard format for call-transcript viewer Artifacts (chronological summary + jump-linked full transcript), distinct from raw .md deliverables"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9f1cf0e2-dd80-42f9-9322-f8f4fa74b16e
---

For a call-recording Artifact (viewer page, not the .md sent to the other person), replicate the exact structure/design tokens from the reference clinic-call artifact — don't invent a new layout.

**Reference file:** `C:\Users\Alessandro\.claude\projects\C--Users-Alessandro\833c9bca-1d56-4c13-a3c5-19bf926ee404\tool-results\artifact-65ba02a0-1783082148-a4fd.html` ("Medtech Call — Jelena Teinovic, 03 Jul 2026"). Read this file directly (not a description of it) before building a new transcript artifact — copy its exact CSS custom properties (teal `--accent: #2f6f6b` / warm paper `--paper: #f6f4ef`, Georgia/Iowan/Palatino serif body, system-ui chrome), grid layout (`260px` sticky TOC + main), and structure:
1. Sticky left TOC with 3 groups: Overview (metadata + summary anchors), Full transcript (numbered `01`.. links to each `#sN`), Source (raw transcript anchor).
2. Masthead: eyebrow label, H1, `.meta-row` of pills (📅 date, 🎙 speaker(s), ⏱ duration, 🌐 language, 🎧 "Transcribed locally").
3. **"Chronological summary" section — numbered `.summary-item` grid cards (idx + h3 title + "read full →" jump link + one-sentence teaser), one per transcript section.** This layer is required — do not drop it even after being told "I don't want a summary, I wanted a transcript" for a *different* deliverable (see below).
4. "Full transcript" section: a `.note` disclosure box (diarization caveat etc.), then `.t-section` blocks per topic (not literal timestamps) with a "↑ back to summary" link, `NN · Title` heading, and `<span class="speaker">NAME</span>` verbatim paragraphs — single uniform accent color for the speaker label across all speakers (not per-speaker color-coding).
5. `<details class="raw">` collapsible with the unsegmented ASR transcript at the bottom, for full fidelity.
6. Footer describing the pipeline; scroll-spy JS keyed off `window.scrollY` (not IntersectionObserver) matching the reference's exact script.

**Why:** User corrected a first attempt (custom orange/teal two-speaker-color palette, no summary layer) back to this exact reference format 2026-07-07 — "i preferred it the way you created the other artifact: key points covered/sections summary chronologically with links to specific transcript sections each time." This is a standing preference for this artifact *type*, independent of content/topic — reuse the CSS tokens verbatim, only reskin if explicitly asked.

**How to apply:** Two different outputs from one call recording have two different rules — don't conflate them:
- The **.md sent to the other party** (email/WhatsApp attachment) = raw full verbatim transcript only, no summary layer (per [[feedback_never_fabricate_fetched_content]] — this was corrected 2026-07-07 too: "no this is bad. i dont want a summary, i wanted a transcript").
- The **Artifact viewer** (for Alessandro's own reading) = chronological summary-with-jump-links + full transcript + raw fallback, per this file.
