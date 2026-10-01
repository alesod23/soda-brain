---
name: feedback_deliverable_figures_need_sources
description: Every number in a client-facing deliverable needs a traceable source. Never let derived arithmetic rest on an invented input.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a663f18a-252e-47b4-b092-035a97160645
  modified: 2026-08-22T08:35:23.832Z
---

On 2026-08-22, building the Tundra x UPMC pilot deck, I wrote a business-case slide with three big figures (~EUR 200k/yr saved, up to EUR 2M/yr on contracts, 500-1,000 hours of availability recovered). Alessandro asked "where does all of this come from? all made up fully?" — and he was right to. Tracing it back:

- The **rates** were real and citable: 94.5-98.2% linac availability (published five-machine Clinac series), 95-98% OEM uptime guarantees with a 5%-off-next-year's-contract penalty (Avante Health Solutions buyer's guide), $10bn US service-contract market (PartsSource), 10-20% recoverable spend (Klinikum Stuttgart discovery call — first-party, defensible but not linkable).
- The **euro amounts** were my own arithmetic, and the arithmetic rested on `~EUR 400-600 per service call-out` and `~25,000 fault reports/year, 40-60% not real defects` — figures I wrote with **no source at all**. Plausible, invented, and load-bearing.

**Why:** A derived figure is only as credible as its weakest input. One unsourced constant silently contaminates every number computed from it, and the contamination is invisible on the slide — it looks exactly like the sourced figures next to it. On a slide whose entire job is credibility with two CIOs, a single "prove that" question collapses the whole slide. This is the failure mode [[feedback_never_fabricate_fetched_content]] predicted in its own Why line: "plausible invented stats are exactly the kind of thing that survives into a deck."

**How to apply:**
- Before any number reaches a client-facing artifact, name its source. If I cannot name one, it does not ship — flag the gap to Alessandro instead of filling it with a plausible constant.
- Keep sourced rates and derived amounts visibly separate in my own working notes, so a later pass can tell which is which. Percentages and ratios from real studies are usually safe; absolute currency amounts almost always come from an assumed scale I invented.
- When a deliverable needs a business case and the sources do not exist yet, say so BEFORE building the slide, not after he asks.
- His preferred remedy: research published, linkable claims (competitors' own case studies, regulators, peer-reviewed work), then present **multiple sourced options with links in a comparison UI** and let him choose — rather than me picking one and presenting it as settled.
- Deck card copy: he caps these at **~30 words per card**.

Relates to [[feedback_diagnose_before_naming_root_cause.md]] and the global Self-Audit rule.
