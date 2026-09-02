---
name: project-tundra-talents
description: "Tundra Talents — service helping startups/scaleups revolutionizing legacy sectors find AND evaluate hybrid hires (domain expert + AI savvy, e.g. \"legal engineer\"); opinion-research corpus at research-corpora\\tundra-talents\\"
metadata: 
  node_type: memory
  type: project
  originSessionId: 71376509-c46e-496b-a792-36a925ea7ff4
---

# Tundra Talents

**What:** Service for startups and scaleups revolutionizing legacy sectors who need to hire people who are both expert in that sector AND savvy with AI / recent tech.

**Canonical example:** "Legal engineer" for a legaltech scaleup like Lagora.

**Two pain axes the research must cover (BOTH are first-class):**
1. **Finding** — sourcing, market scarcity, channel issues, candidate self-identification
2. **Evaluating** — interview design, vetting hard-to-measure capabilities (especially "taste" — product/aesthetic judgment), distinguishing real-vs-surface domain depth, distinguishing real-vs-surface AI fluency, mis-hire stories, success-hire stories WITH THE HOW

Evaluation-done-well stories are gold — they answer the "is it overcome-able?" hypothesis test.

## Corpus

`C:\Users\Alessandro\.claude\research-corpora\tundra-talents\`
- `reports\stories-reddit.json`, `stories-hn.json`, `stories-blogs.json`, `stories-podcasts.json`, `stories-linkedin.json` (when LinkedIn helper extended)

Schema: Pain (4-part) with these augmentations:
- `setting.is_scaleup: yes | no | unclear` — score-boost but keep all in corpus (var/filter approach, NOT hard filter)
- `setting.sector: legal | healthcare | finance | insurance | industrial | logistics | other`
- Augmented `tags` vocabulary: `sourcing | evaluation | taste | domain-depth | ai-fluency | interview-design | mis-hire | success-hire | no-known-fix | scaleup | seed-stage | enterprise | comp-expectations | culture-fit | candidate-pool-thin`

## Sectors of priority

Legal/LegalTech, Healthcare/MedTech, Finance/InsurTech, Industrial/Manufacturing/Construction/Logistics. All four are in-scope for the first sweep.

## Prospect map (score-boost +15 when mentioned)

- **Legal**: Harvey, **Legora** (NOT "Lagora" — common transcription error), EvenUp, Spellbook, Robin AI, Eve, Hebbia, Norm Ai, Tritium
- **Healthcare**: Abridge, Hippocratic AI, Nabla, OpenEvidence, Suki, Glass Health, PathAI
- **Finance/Insurance**: Decagon, Cresta, Cohere Health, AgentSync, Numeral
- **Industrial**: Tulip Interfaces, Augury, Saronic, Nominal

(Working draft from 2026-05-18 first sweep — refine after seeing what surfaces.)

## Scoring tweaks specific to this corpus

On top of [[feedback-pain-corpus-scoring]] base rules:
- +10 if `evaluation` tag (under-covered angle, user cares about it most)
- +10 if `taste` tag (rare, direct hit on hardest-to-measure capability)
- +10 if `success-hire` with explicit HOW in workaround field
- +10 if `mis-hire` with explicit ROOT-CAUSE

## First-pass findings (2026-05-19, 63 stories merged)

Counts: 42 legal / 21 healthcare; 22 scaleup / 25 non-scaleup / 16 unclear. Top tags: domain-depth (46), sourcing (41), ai-fluency (39), evaluation (37), success-hire (12), mis-hire (8).

Dashboard: `tundra-talents-corpus.html` (also copied to `OneDrive\Pictures\`).

**Pattern-level insights (worth pushing back on the original framing):**
1. **AI-blank-slate is a deliberate hiring pattern at Harvey + Legora** — they hire ex-practising lawyers off partner-track and teach AI on the job. Inverts the "find a hybrid" framing toward "find a domain expert open to AI."
2. **Title chaos** — "legal engineer" goes by 5+ names (legal AI analyst, legal ops for AI, product counsel, legal data QA). Direct sourcing wedge for Tundra.
3. **ATS keyword filters** routinely reject the strongest hybrid candidates (Master's-degree filter blocks RN+22yr-tech candidates from informatics roles).
4. **Buyer-side evaluation pain** — hospitals/firms can't tell which AI tool works; "tools die in pilot hell" (Parachute YC S25). Suggests Tundra could anchor *evaluation services*, not just sourcing.
5. **Only practitioners catch semantic errors** in AI output (misattributed legal holdings, over-claimed clinical fairness). Pure ML/dev evaluators miss them.
6. **"Pool is tiny" self-confirmed** — multiple hybrid hires on the Tritium HN thread say it directly.
7. **r/HealthIT was thin on scaleup signal** — mostly Epic-analyst grind. Healthcare scaleup hiring signal lives elsewhere (operator essays, Hippocratic AI's clinician-eval-team writeup, podcasts).

## Related

- [[practitioner-research-methodology]] — 80/20 in-house large-co heuristic adapted here to "founder/CEO/Head of Hiring at named scaleup = top tier"
- [[reference-linkedin-helper]] — being extended with `search-posts` for this corpus
- [[project-langfuse-pains]] — similar opinion-research workflow precedent
