---
name: reference_getedge_people_search_skill
description: "Verdict on the getedgehq \"people-search\" Agent Skill (2026-09-18): audited clean, tested head-to-head, found nothing a plain search did not, ranked worse; REMOVED on his word. What the test taught about finding hospital clinical engineers."
metadata: 
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-18T17:47:21.260Z
---

**getedgehq/skills, folder `people-search` (Apache-2.0), evaluated 2026-09-18 on his instruction via the savior.**

- **Audit (every file read before install):** one network call, only to a user-supplied `--endpoint` with a bearer token from `PEOPLE_SEARCH_API_TOKEN`; no default endpoint, no telemetry, no browser, no LinkedIn, no disk writes (stdout JSON only). Providers HarvestAPI / Apify are prose, not code. Safe as a folder; its shipped tests hardcode `python3` (fail on Windows).
- **Tests:** three briefs (Lombardy clinical engineering vs the AIIC Lombardia brochure, SF Bay HTM vs the CMIA board, Estonian hospital digital heads vs the Estonia board) and a head-to-head on "clinical engineering at Ospedale Bambino Gesù" (skill arm vs plain WebSearch, same 12-minute box: both 4 min). Every name in every run came from web search; the runner only ranked and deduped a CSV the agent built. Ranking is `count of matched preference substrings` (a senior manager above the director; the technical-services parent level with the CE head), and URL-based dedupe merged two real people who cite the same PDF. Its one merit: the filter ledger and the forced evidence URL per person, which made the stale-name check explicit (Pietro Derrico, OPBG until 2022, still summarised by search engines as the sitting head).
- **Decision (his, terminal, 2026-09-18 evening): removed.** Folder deleted from `~/.claude/skills`; never installed on the box; no MCP, no key, never touched the LinkedIn poller profile.

**What the test taught, worth more than the skill:** hospital clinical engineers are found in procurement documents (pareri tecnici, tender contact points on the hospital's own PDF host: letterhead names the Responsabile), AIIC and conference programmes, and native-language queries (the Estonian query found Pruul and Kaalep when English failed); PDFs must be downloaded and parsed locally (WebFetch returns noise on scanned PDFs); always check the freshest primary evidence date and look for a "has left" signal before shipping the most-cited name. Facts found: Ing. Carlo Capussotto = Responsabile Servizio Ingegneria Clinica, OPBG (letterhead 09/2024, AIIC 05/2025); Adam Alkhato = Director of Biomedical Engineering, Stanford Health Care (candidate for the CMIA board, pending his word).
