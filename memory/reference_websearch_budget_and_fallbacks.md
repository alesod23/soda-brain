---
name: reference_websearch_budget_and_fallbacks
description: "WebSearch has a hard per-session budget (200 calls) SHARED with every subagent; when it and the Gemini free tier are both spent, only WebFetch survives. gemini-search.sh now exists as the search fallback."
metadata: 
  node_type: memory
  type: reference
  originSessionId: e7351fcb-845d-45ae-b97b-335e70d58b55
  modified: 2026-09-20T02:44:59.986Z
---

**A Claude Code session has a hard WebSearch budget of 200 calls, and subagents spend it from the
same pool.** On 2026-09-20 five research agents exhausted all 200 within the first ~25 minutes of an
overnight run, and every agent launched afterwards inherited a session that could not search at all.
The refusal message names the env var: `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`.

**Plan for it on any big research night:** give the early agents tight, high-yield query lists
rather than "search thoroughly", and keep budget in reserve for the enrichment passes that come
last. Ask him to raise the env var before starting if the run is genuinely search-heavy.

**The fallback chain, in the order it actually holds up:**

| Tool | State on 2026-09-20 |
|---|---|
| `WebFetch` | **Survives.** Not covered by the search budget. Fetch a constructed URL and read it. |
| `~/.claude/scripts/gemini-fetch.sh` | Works when the Gemini key has quota (`url_context` tool). |
| `~/.claude/scripts/gemini-search.sh` | **NEW, written that night.** Same shape as gemini-fetch but uses Gemini's `google_search` grounding and prints the grounding source URLs so the answer stays citable. Returns 429 when the free tier is spent, which it was. |
| DuckDuckGo (`html.` and `lite.`) | Captcha page, both endpoints. |
| SearXNG public instances | Cloudflare challenge. |
| Bing | Answers, but strips quotes and operators and geolocates, so exact-phrase work is useless. |

**What still works with WebFetch alone:** resolve a domain by guessing the URL and fetching it (a
200 that is clearly the right organisation is confirmation, a 404 is disproof); mine research/IRB,
newsroom, foundation and residency pages for published staff emails. **What does not:** anything
needing an index, so per-account screening and "find this person's profile" both die.

Two systemic blockers that cost real yield: many hospital sites 403 a fetch tool site-wide (WAF),
and several big systems (Seattle Children's, UVA, Wellstar, UT Southwestern) hide every staff
address behind Cloudflare's JS email obfuscation, which HTML-to-markdown cannot decode. **A real
browser fetch would recover those** - worth trying Playwright next time before giving up.

See [[reference_linkedin_scraper_direct_stdio]] for the night's other recovery, and
[[feedback_never_fabricate_fetched_content]]: the correct response to a dead search tool is fewer
rows, never invented ones. One subagent that night caught the Gemini fallback inventing a
trimedx.com page and an SEC quote, and discarded it before it entered the data.
