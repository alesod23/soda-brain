---
name: feedback_tundra_deck_workflow
description: "Tundra pilot-deck edits must go through the actual Claude Design project (DesignSync + /tundra-de-en), never a hand-rolled HTML/CSS recreation rendered to PDF locally."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2128ab65-69ab-46de-9e4c-680c11ed4fc3
---

For any Tundra Health pilot-offer deck request (translate, edit, combine slides), use the
`/tundra-de-en` skill workflow (`~/.claude/commands/tundra-de-en/SKILL.md`), Path B:
`DesignSync` `get_file` on the real `.dc.html` in the Claude Design project → translate/edit
in place (same CSS classes/DOM, only text nodes change) → render via Playwright pointed at the
system Chrome (`channel: 'chrome'`) → save `<Deck title> (EN).pdf`.

**Why:** On 2026-07-12 I built a from-scratch HTML/CSS deck (my own dark-navy card-grid design)
and rendered it with headless Chrome `--print-to-pdf` instead of touching the actual Claude
Design source. The user called the result "a very disgusting new design" — it broke visual
consistency with their approved decks. The one file they ARE happy with ("Pilot Offer -
Klinikum Stuttgart (EN).pdf") was produced by the proper `/tundra-de-en` Path B flow: same
layout/CSS as the original German design, just the copy translated.

**How to apply:** Any time a Tundra deck needs new/edited/combined content, pull the actual
`.dc.html` from its Claude Design project (project IDs and file names are listed via
`DesignSync list_files` — e.g. project `41320ac3-fb9c-43a5-8f05-609d9aa46a2f` holds
`Angebot Pilot Klinik Stuttgart.dc.html` and `Angebot Pilot Medizintechnik - Komplett.dc.html`).
Never invent a new visual design for Tundra collateral — the brand's design lives in these
Claude Design projects, not in a Claude-Code-authored CSS file. Read methods on `DesignSync`
work even when the project's `type` isn't `PROJECT_TYPE_DESIGN_SYSTEM` (per the skill) — don't
block on that for get_file/list_files. See [[reference_tundra_stack]] for where Tundra
documents/decks live overall.
