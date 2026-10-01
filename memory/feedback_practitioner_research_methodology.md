---
name: practitioner-research-methodology
description: "For practitioner-research goals (especially Lobbly IP research) — stories not claims, 80/20 in-house large-company focus, score by company-named + recurrence, saturation + coverage stop with 24h hard cap"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fb970009-ed69-4ae3-8035-21fda376ca60
---

When Alessandro asks for "what real practitioners say" research (Lobbly IP space, or any analogous customer-discovery effort), default to this methodology — do NOT simplify back to "list of claims" or "one summary doc."

**Unit of output is the STORY, not the claim.**
Each story has a four-part schema:
1. **Setting** — who (named practitioner with researched role), where (company, size), when (year)
2. **Pain** — the actual frustration in their own words (verbatim quote required)
3. **Current workaround / quick fix** — what they do today to cope
4. **What would help** — explicit or implicit ask

Prioritize *complete* stories (all four parts present). Pains-WITHOUT-fixes are tracked separately and weighted higher for product relevance — they are the most exploitable gaps.

**Source weighting — 80/20 in-house at large companies.**
80% effort: in-house IP counsel, IP managers, patent analysts at large/named corporates (Siemens, Philips, Bosch, IBM, Microsoft, Google, GE, Samsung, Qualcomm, BAT, Unilever, ABB, Volvo, Ericsson, Roche, Bayer, etc.). 20% effort: private patent attorneys, IP search firms, vendor blogs.

**Researcher MUST investigate the poster** when the content doesn't make their background clear. LinkedIn lookup, firm bio, "About" page — never trust unverified bylines. Tag every story with a verified role + employer.

**Scoring ingredients (per story):**
- Company size of employer (large=3, mid=2, small=1)
- Company name explicitly mentioned (yes=+2; anonymous "Fortune 500 medtech client"=+1; unknown=0)
- Independent recurrence — same pain reported by N distinct practitioners (this is the "is it recurring?" measure)
- Recency (2024+ heavier than older — AI-disclosure phenomenon is recent)
- Source tier: named in-house (3) > named outside counsel (2) > anonymous-but-claimed-credible (1) > vendor marketing (0.5)
- Completeness — full 4-part story (+2), pain-only (+0)

**Stop conditions: saturation AND coverage AND time.**
- Saturation = 3 consecutive iterations add <5% new unique stories
- Coverage = all platforms in target list swept to target depth
- Hard cap = 24 hours wall-clock — whichever fires first wins

**Why:** Alessandro is over-rotated on storytelling without practitioner evidence. Stories from named practitioners are durable; aggregated claims are not. The "is it recurring?" question is the actual product-validation signal. Aggregated claim-ledgers feel rigorous but lose the texture that makes a pitch land.

**How to apply:** When the user asks for this kind of research, draft the goal-prompt using the schema above. Output is dual: (a) story corpus with attribution + verbatim quotes, (b) recurring-pain leaderboard ranked by frequency. Always include "pains without known fixes" as a separate ranked list — that is the product roadmap. Related: [[project-lobbly]].
