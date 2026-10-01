---
name: feedback_ps51_convertfrom_json_no_unroll
description: "PowerShell 5.1 trap: @(ConvertFrom-Json $raw) does NOT unroll the array — assign to a variable first, then iterate, or every loop iteration binds the whole array."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-08-03T15:30:48.021Z
---

In Windows PowerShell 5.1, `ConvertFrom-Json` emits a JSON array as a **single object**, not as
enumerated items. So `@(ConvertFrom-Json $raw)` wraps that one object instead of unrolling it:

```powershell
# BROKEN - $e is the ENTIRE array on the only iteration
foreach ($e in @(ConvertFrom-Json $raw)) { $map[$e.key] = $e.first_seen }

# CORRECT - assignment unrolls
$arr = ConvertFrom-Json $raw
foreach ($e in @($arr)) { $map[[string]$e.key] = [string]$e.first_seen }
```

The failure is nasty because it does not throw. `$e.key` on an array **member-enumerates**, returning
an array of every element's `key`, which stringifies into one space-joined key like
`"daemon:git-watch:missing port:BOGUS-TEST:down"`. You get a populated hashtable with `Count = 1` and
every real lookup missing. If the parse sits inside a `try/catch` (normal for state files), there is
no error either.

**Why:** Caught 2026-08-03 building the DA SYSTEM health-alert de-duplication. State-file lookups
silently missed, so every standing fault reported `is_new = true` forever and would have re-emailed
hourly. Found only because the fault-transition behaviour was explicitly tested rather than assumed
from a "0 faults, all green" run.

**How to apply:** Never iterate `ConvertFrom-Json` output inline. Assign, then `foreach ($x in @($var))`.
Cast keys and values with `[string]` when building a hashtable from parsed JSON. Whenever code
round-trips state through JSON to decide whether something is new/changed, TEST the transitions
(appears, persists, resolves, recurs) - a healthy-path run proves nothing about the state logic.
Related: [[feedback_ps1_ascii_only_no_unicode_dashes]], [[feedback_windows_tail_locks_logfile]].
