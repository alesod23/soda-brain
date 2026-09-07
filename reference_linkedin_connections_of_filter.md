---
name: reference-linkedin-connections-of-filter
description: "LinkedIn's \"Connections of\" filter cannot enumerate someone else's network on this account; use the mutual-connection column on 2nd-degree cards instead."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3da174f5-ada2-42a8-959b-8bfe3be15b90
  modified: 2026-09-07T17:13:36.943Z
---

LinkedIn people search supports `connectionOf=["<member URN>"]` in the URL (the URN is the
`ACoAA...` string; grab it by fetching `/in/<slug>/` from the page context and regexing for
`ACoAA[A-Za-z0-9_-]+` — the first hit is the profile owner). The **public identifier does not
work** there; LinkedIn silently ignores it and returns plain unfiltered results, which looks like
success. Always sanity-check that the filter actually bit.

**But the filter is useless for prospecting on this account.** It returns only the intersection
with Alessandro's own 1st-degree network, i.e. it is a *mutual connections* filter, not a
*browse their network* filter. Verified 2026-09-07 against a connection with ~105 shared
connections: every result on every page was already 1st-degree. Enumerating someone else's
network needs **Sales Navigator**. A target who hides their connection list (no connection count
or link on the profile, only a follower count) defeats it a second time.

**The workaround that does work:** run each persona query 2nd-degree + geo-restricted *without*
the connectionOf filter, and read the "X is a mutual connection" line LinkedIn prints on each
result card. That names who can make the intro. It is lossy in one direction only: LinkedIn shows
at most two mutual names, so an absence proves nothing, but every name shown is real.

Scraping notes: `main.innerText` parses reliably; `li` containers come back empty (virtualized),
and both `sessionStorage` and `localStorage` are **wiped on every navigation** by the LinkedIn app,
so a scraper helper cannot be persisted across page loads — inline it in each call. Bash heredocs
mangle large JSON/HTML here; use the Write tool. See [[feedback_mcp_over_pw]].

Applied for the Tundra US outreach mapping; output lives in `gtm-eng/boards/chris-masci-network/`.
