---
name: reference-overnight-email-find
description: The "find emails/phones/LinkedIn for a list of people" skill is /overnight — the harness he built for long agent batches.
metadata:
  type: reference
---

When Alessandro asks about "the skill that runs a bunch of agents for a long time to find emails and
phone numbers and LinkedIn", he means **`/overnight`** (`~/.claude/skills/overnight/`, engine
`harness.js`). It is a general long-batch harness, and contact enrichment is what he has actually
used it for.

Proof it was used this way: `~/tundra-outreach/crm-email-find/items/` holds 25 checkpointed items,
one JSON per French hospital contact, each with `email`, `emailBasis` (`published` vs
`pattern-inferred`), a `sources` array, a long `notes` paragraph justifying the address, and a
`needsAuth` flag.

Why it is the right tool for this job rather than a plain agent: per-item checkpointing (a crash
costs one contact, not the run), an independent verifier that the generator cannot self-grade past,
a hard token cap with a circuit breaker, and **auth quarantine** — anything needing a logged-in
tool goes to `_NEEDS-AUTH.md` for a daytime pass instead of being attempted unattended.

**lemlist is NOT the substitute.** Its enrichment endpoints (`bulk_enrich_data`, `enrich_lead`)
return "This feature is available starting the emailPro plan" on his current plan (verified
2026-09-04), so email/phone lookup through lemlist is unavailable until he upgrades.

Pair it with [[reference_gtm_boards]]: run `/overnight` to fill in contacts, then rebuild the
board's `build.js` so the found addresses land on the cards with their `verified` /
`pattern guess` badge. Never promote a pattern guess to verified.
