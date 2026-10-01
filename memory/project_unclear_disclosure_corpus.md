---
name: unclear-disclosure-corpus
description: Practitioner-story corpus of UNCLEAR invention disclosures for training a Lobbly model to distinguish relevant vs irrelevant info; 61 unique entries; dashboard at OneDrive\KG Patent Idea\claude files\unclear-invention-disclosures\dashboard.html
metadata: 
  node_type: memory
  type: project
  originSessionId: cffc319a-651a-4fe6-a56a-4baee1f12386
---

Built 2026-05-20 as training-data scaffolding for a Lobbly model that distinguishes RELEVANT vs IRRELEVANT info in invention disclosures. See [[project_lobbly]].

**Corpus location:** `C:\Users\Alessandro\OneDrive - HEC Paris\KG Patent Idea\claude files\unclear-invention-disclosures\` (moved here 2026-05-22 from `~/.claude/research-corpora/`)
- `merged.json` — 61 unique entries (deduped from 70 raw across 4 sweeps)
- `dashboard.html` — filterable (platform / tech_area / outcome / tags / min-score / search)
- `reports/stories-*.json` — per-source raw

**Schema (disclosure-gap):** id, platform, venue, url, title, author, author_role, firm_or_employer, setting, unclear_disclosure, what_was_missing, what_made_it_clearer, outcome, tech_area, year, score, tags, quotes.

**Coverage:**
- Court-case narration 22, blog 21, TTO 7, Reddit 5, HN 3, LinkedIn 2, IAM 1
- Tech: bio 14, software 8, mech 7, medical-device 6, chem 4, electrical 4, ai-ml 2
- 26 entries scored ≥80; top 5 all Fed Cir antibody/chem cases (Idenix, Amgen, Centocor, Ariad, AbbVie)

**Why:** Lobbly is training on what counts as "missing detail" in real disclosures. Court opinions give the cleanest narrate-the-gap stories; prosecutor war-story blogs give the second-cleanest; Reddit/HN give anonymized but specific anecdotes.

**How to apply:** When extending the corpus — the biggest known gap is verbatim first-person inventor-attorney dialogue with concrete missing-detail callouts. That material lives in podcast transcripts (Clause 8 with Eli Mazour is the richest seam), CLE talks, and private firm newsletters, NOT in public blogs. Pure "best practices" disclosure-form guides yield zero usable signal — skip those sources next time.

**Notes from this run:**
- Quora 403s reliably; AskPatents StackExchange access blocked; Patently-O mostly paywalled.
- Reddit on this topic is thin — 5 entries after dedup; the r/patents and r/AskPatents communities don't tell prosecution war stories the way r/inhouse lawyers do for other domains.
- Best non-court source: IPWatchdog deep-dives + Mr. IP Law + Akin Gump case digests.
