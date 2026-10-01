---
name: reference-linkedin-connections-of-filter
description: "LinkedIn's \"Connections of\" filter DOES browse someone else's network without Sales Navigator; it collapses to mutuals only when the target hides their connection list."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3da174f5-ada2-42a8-959b-8bfe3be15b90
  modified: 2026-09-07T17:26:45.680Z
---

LinkedIn people search supports `connectionOf=["<member URN>"]` in the URL. It **works on the free
account and does browse that person's network**, returning 2nd-degree people who are not in
Alessandro's own network. No Sales Navigator needed. (Verified 2026-09-07 after I first claimed the
opposite and he pushed back; he was right.)

**Getting the URN:** fetch `/in/<slug>/` from the page context and regex `ACoAA[A-Za-z0-9_-]+`;
the first hit is the profile owner. The **public identifier does not work** in `connectionOf` —
LinkedIn silently ignores it and returns plain unfiltered results that look like success. Always
confirm the filter actually bit.

**The real variable is the TARGET's privacy setting.** If their profile shows a connection count
("500+ connections", "276 connections"), the filter returns their whole network. If the profile
shows only a follower count and no connection number or link, they hide their list and the filter
collapses to just your shared connections. Chris Masci: followers only, returns exactly the 2
mutuals. Caleb Love Seeling: followers only, returns exactly 105 = his mutual count with Alessandro.
Guido Sodano and Shane Waltsak: 500+ visible, filter returns full 2nd-degree networks.

**Check the connection count on the profile before concluding anything.** My first control was a
hidden-list profile, which produced a false general conclusion. A confounded control is worse than
no control: LinkedIn also sorts results by degree, so early pages are all-1st-degree either way.
Test on a target with VISIBLE connections and few mutuals. See
[[feedback_diagnose_before_naming_root_cause]].

Fallback when the target hides their list: run the persona query 2nd-degree + geo-restricted with
no `connectionOf`, and read the "X is a mutual connection" line on each card to learn who can make
the intro. Lossy (max two names shown) but every name shown is real.

Scraping notes: `main.innerText` parses reliably; `li` containers come back empty (virtualized);
both `sessionStorage` and `localStorage` are wiped on every navigation by the LinkedIn app, so a
scraper helper cannot persist across page loads, inline it each call. Many sequential `fetch()`
calls in one JS execution freeze the renderer (CDP timeout) — navigate instead, or batch two at a
time. Bash heredocs mangle large JSON/HTML here; use the Write tool.

Applied to the Tundra US outreach mapping; output in `gtm-eng/boards/chris-masci-network/`.
