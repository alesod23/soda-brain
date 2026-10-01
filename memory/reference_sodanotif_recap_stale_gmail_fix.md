---
name: sodanotif-recap-stale-gmail-fix
description: "SODANOtif recap.ps1 surfaced a 5-day-old Gmail thread in a \"last 12h\" catch-up because Gmail's after:<epoch> search operator silently doesn't filter — fixed with a code-level ts_unix post-filter."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 833c9bca-1d56-4c13-a3c5-19bf926ee404
---

[[reference_sodanotif]] `recap.ps1` enforces a hard rule (set 2026-06-23): the catch-up digest never shows anything older than `$Hours` (12h). It enforced this for Gmail solely via a query string: `is:unread -label:triage/done after:$cutoffUnix` (raw Unix epoch seconds).

**Bug (found 2026-07-06):** tested this query directly against the cdtm Gmail account — it returned threads spanning 5 days (Jul 1 09:58 through Jul 6 10:22) despite `after:<12h-ago-epoch>`. Gmail's `after:`/`before:` search operators don't reliably enforce an epoch-second cutoff (day-granularity at best, and can silently no-op on a raw epoch value) — the query-string filter was doing nothing. Result: a Jul 1 email from Julian Nast-Kolb surfaced in a Jul 6 "last 12h" catch-up. This is the SAME class of bug already documented for Slack in [[feedback_slack_cutoff_filter]] — never trust a source API's own date-filter syntax for correctness; it needs a real post-filter on the item's actual timestamp in code.

**Fix applied:** `Process-GmailThreads` in `recap.ps1` now takes an optional `$CutoffUnix` param and drops any thread whose `ts_unix < CutoffUnix` — a hard code-level post-filter, not a reliance on the Gmail query. Applied ONLY to the unread feed (`$gm_cdtm_unread`); the `triage/todo` carryover feed (`$gm_cdtm_todo`) stays unbounded on purpose (todos should persist until done, not expire on a clock). Verified via `DRY_RUN=1` dry run: the stale Jul 1 thread no longer appears, only genuinely-recent items do.

**Scope note:** `watch.ps1` (the 5-min flagger) has the same `after:$lastTriageUnix` query-string pattern for Gmail but is NOT vulnerable to this symptom — it dedupes by `historyId`/`threadId` against `notif-state.json#seen`, so an over-fetched stale thread just gets filtered out as "already seen," not re-pushed. Only `recap.ps1` was actually broken, because recap has no dedup layer (by design — it's "everything currently unread," recomputed from scratch each run).

**How to apply:** if a similar "old item shows up in a should-be-recent feed" report ever recurs anywhere in [[reference_sodanotif]] or [[reference_triage_operations]], check whether the time-bounding is done via a source API's search-query date operator alone (fragile, especially Gmail after:/before:) vs. a code-level post-filter on the item's actual parsed timestamp (reliable) — always prefer/add the latter.
