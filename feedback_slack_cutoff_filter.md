---
name: slack-cutoff-filter-mandatory
description: "/triage's fetch-all wrapper MUST post-filter Slack messages by the shared cutoff, otherwise already-handled channel items re-surface across rounds. Bug found 2026-05-21 on a BMW doc share."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e6c7fe19-de71-4b7a-82b5-ffe11ccad58a
---

When `fetch-all.js` runs `slack.cmd unread --hours N`, the helper fetches by whole-hour buckets back from `now`, which is COARSER than the shared cutoff in `~/triage/state.json#last_check_unix`. Without an explicit post-filter, a Slack message handled in a previous /triage round re-surfaces on the next round because its ts falls inside the 1h Slack lookback window but BEFORE the cutoff.

**Why:** 2026-05-21, the BMW `#26-1_mpd_bmw_only-us` Google Doc share from Ammar Idriz (ts 15:33Z) was clicked Done in a 16:06Z triage round, then re-surfaced in the 16:28Z round because no Slack post-filter existed. User: "i had already clicked done for the slack one in the last triage, you didnt record it ig? lets not have it happen again, from now on ensure you do."

**How to apply:**
- The fix lives in `C:\Users\Alessandro\triage\fetch-all.js` (step 8 in that file: `if (wantSlack) { ... w.dropped_24h = dropped; }`). It mirrors the Gmail/WA post-filters. Don't remove it.
- If the wrapper is bypassed (manual-fallback path in SKILL.md), apply the same filter by hand: drop `dm_recent`/`mentions`/`channel_recent.preview` entries where `Number(ts) < effective_cutoff_unix`. Drop the channel entry entirely if `preview` ends up empty.
- Slack has no per-message state file (unlike Gmail labels and `wa-state.json#done`); the shared cutoff in `state.json#last_check_at` is the only thing that prevents re-surfacing. Advancing the cutoff in step 7d is therefore load-bearing — never skip it.
- If a Slack item is shown in /triage, the next round's cutoff advance must cover it. The 7d step uses the fetch's `generated_at` (or `Date.now()`) as the new cutoff, which is correct.

Related: [[feedback_shared_inbox_cutoff]], [[reference_triage_operations]], [[reference_slack_helper]].
