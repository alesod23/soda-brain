---
name: daily-tag-css-split-fix
description: "Obsidian Live-Preview double-boxed category tags (\"#mpd\" / \"#tundra-medical\" rendered as \"# | word\" in two separate boxes) — root cause and the durable generic CSS fix (superseded an earlier, wrong, enumerated fix)."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 833c9bca-1d56-4c13-a3c5-19bf926ee404
---

`task-land/.obsidian/snippets/daily-categories.css` styles the project-category tag pills shown on the [[reference_vault]] daily page (`#lobbly #mpd #tuscany #tundra-medical` etc.) as an outline pill (border+padding+radius).

**Bug (found 2026-07-06):** CodeMirror6 Live Preview can split a hashtag into two DOM spans — one for the raw `#` formatting mark, one for the tag body — and both spans can end up boxed. Result: a visible "# | mpd" double-pill instead of one merged pill.

**First fix attempt (WRONG, corrected same day):** initially assumed this only affected the 12 hardcoded canonical taxonomy tags (`#lobbly #thesis #cdtm #mpd #tools #personal #bmw #xplore #tundra-talents #terminal-inbox #aura #uncat`) and that ad-hoc tags like `#tuscany` were naturally immune. Patched only the enumerated selectors with `:not(.cm-formatting)`. **This was wrong** — the user hit the same double-box glitch on brand-new ad-hoc tags (`#tuscany`, `#tundra-medical`) right after. The bug is generic to any tag, not tied to the hardcoded list — the earlier "ad-hoc tags are safe" theory was a coincidence of one screenshot, not a real distinction.

**Actual durable fix:** replaced the enumerated per-tag selectors with a GENERIC rule that boxes `a.tag[href^="#"]` (Reading view) and `.cm-hashtag:not(.cm-formatting)` (Live Preview) — i.e. every tag, named or not — and a matching generic `.cm-hashtag.cm-formatting` rule (color only, no box) for the raw `#` span. Per-tag *colors* (the distinct orange/blue/amber/etc. for the 12 canonical tags) are unaffected — they only set the `color` property, and the border already uses `currentColor`, so color and box-shape don't conflict regardless of which selector "wins" on specificity.

**Why this is durable across sessions:** no enumeration means no future category (any project tag typed in any future session) can ever be missed — the fix covers the *shape* generically, only per-tag *color* needs a future one-line addition, and skipping that only means "default/plugin color," never a broken rendering.

**How to apply:** if this glitch ever reappears, do NOT go back to enumerating selectors per tag — check whether something re-introduced a per-tag-only selector (bare `.cm-hashtag.cm-tag-X` without `:not(.cm-formatting)`) instead of relying on the generic rule.
