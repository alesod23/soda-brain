---
name: reference-alt-shift-m-ai-draft
description: "Alt+Shift+M now drafts with a background Claude job (/ai-draft on 4137), not the keyword template scorer."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3da174f5-ada2-42a8-959b-8bfe3be15b90
  modified: 2026-09-02T23:15:59.006Z
---

**Alt+L** (Medtech Capture extension) = save the LinkedIn profile to coattio: screenshot, category chip,
stage fix, outreach action, and stacked free-text comments. **Alt+Shift+M** = the message widget.

Since 2026-09-03 Alt+Shift+M runs **two lanes at once**:
1. `POST /message` — the old keyword scorer, instant, pastes the best-fitting approved template verbatim.
   Kept only so the box is never blank.
2. `POST /ai-draft` — the real one. `~/.medtech-crm/ai-draft.js` runs a hidden `claude -p --model sonnet`
   job that receives the WHOLE approved template library with its labels, `skills/linkedin-outreach/SKILL.md`
   + `examples.md`, the CRM row, and every Alt+L comment on that person, then writes one finished message in
   the recipient's language under a hard cap (300 chars unconnected, 900 for a 1st-degree DM), with a
   corrective second pass if it overruns.

Jobs are keyed by profile URL and **stack** (3 in parallel), survive navigating away, and are cached +
persisted to `ai-drafts.jsonl`, so re-pressing Alt+Shift+M on a profile is instant. `GET /ai-draft?url=`
polls one, `GET /ai-queue` returns the whole stack for the widget's indicator. Expect 50-85s per draft.

The scorer alone could not translate or adapt across cases, which is what made it feel like guessing;
the model gets the templates as raw material to adapt, never as a menu to paste. It is told explicitly
that the only facts it has are the ones printed in the prompt, because it otherwise borrows biographical
hooks out of `examples.md` and attaches them to the wrong person.

Restart after editing either file per [[reference_coattio_servers]] (never `run_in_background`).
Extension code lives in `~/medtech-capture-extension/` and must be reloaded in Chrome after a change.
