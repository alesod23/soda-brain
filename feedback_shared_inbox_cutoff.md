---
name: shared-inbox-cutoff
description: "One cutoff timestamp governs ALL inbox checks across /triage, /snm, SNM background scans, and informal \"what's new\" queries — every check must advance it"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5613f4ee-d778-418d-907a-3cbdcd94e11d
---

There is ONE shared cutoff that all inbox-checking tools coordinate around: `~/triage/state.json#last_check_at` (+ `last_check_unix` seconds form; legacy aliases `last_triage_at` / `last_triage_unix` are still written for backward compat). Every tool that fetches inbox data must:

1. **Read** the cutoff as the lower bound of its fetch window.
2. **Advance** it to the scan-start timestamp after the fetch+classify completes successfully.

**Who advances it:**

| Caller | When |
|---|---|
| `/triage` skill | At round end (step 7d) — `last_check_kind: "triage"` |
| SNM `scan.ps1` (every 20 min cron) | After the LLM classifier returns successfully — `last_check_kind: "snm"` |
| `/snm scan` (user-forced) | Same as cron path — `last_check_kind: "snm"` |
| **Informal** "tell me what's new across my channels" / "any unread?" / "email check" / etc. | After the assistant fetches inbox state and shows results to the user — `last_check_kind: "informal"` |

**Why:** Without this, SNM keeps scanning the same cumulative window since the last `/triage`, returning duplicates. Without it, an informal "what's new?" question leaves the cutoff stale and the next `/triage` re-shows items the user already saw informally.

**How to apply (informal checks):**

When the user asks something like:
- "tell me what's new"
- "anything across my channels?"
- "check my email/wa/slack"
- "/email-check"
- "any unread messages?"
- "morning briefing across my inboxes"

After fetching and showing results, write `~/triage/state.json` with the scan-start ISO timestamp as both `last_check_at` and `last_triage_at`, the unix-seconds equivalent as `last_check_unix` + `last_triage_unix`, and `last_check_kind: "informal"`. Use atomic write (write tmp, rename).

PowerShell idiom (PS 5.1, UTF-8 without BOM):
```powershell
$now = Get-Date
$nowIso = $now.ToString('o')
$nowUnix = [int][System.DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$state = @{
    "_README" = "Shared cutoff for all inbox checks..."
    last_check_at = $nowIso
    last_check_unix = $nowUnix
    last_check_kind = "informal"
    last_triage_at = $nowIso
    last_triage_unix = $nowUnix
} | ConvertTo-Json -Depth 4
$tmp = "C:\Users\Alessandro\triage\state.json.tmp"
[System.IO.File]::WriteAllText($tmp, $state, [System.Text.UTF8Encoding]::new($false))
Move-Item -Force $tmp "C:\Users\Alessandro\triage\state.json"
```

**Exception — don't advance the cutoff if:**
- The fetch failed (no usable result for the user → not really a "check").
- The user is doing a SEARCH ("find emails from X about Y") that explicitly bounds time, not a "what's new" query.
- The query is read-only on already-known state (e.g., `/snm status` reads state.json without fetching anything fresh).

**See also:** `[[reference_triage_aliases_and_state]]` for the original cutoff semantics, `[[feedback_triage_workflow_v3]]` for the auto-done semantic (rule C — "state.json cutoff is sacred"), and the `/snm` + `/triage` skill bodies for the implementation.
