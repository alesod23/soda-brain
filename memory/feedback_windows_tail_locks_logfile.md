---
name: feedback_windows_tail_locks_logfile
description: "On Windows, a Monitor running `tail -f` on a log file LOCKS it, so the script writing that log dies on its next append. Never tail a log a live script appends to."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b3102940-5e76-40e1-8354-ffd1883e672a
  modified: 2026-08-03T00:01:25.031Z
---

**On Windows, `tail -f <logfile>` holds a file lock that blocks `Add-Content`/appends from another
process.** Unix semantics do not apply. A Monitor armed with
`tail -f watch.log | grep ...` silently broke the very watcher it was monitoring: the watcher's
first `Add-Content` threw `"The process cannot access the file ... because it is being used by
another process"`, and with `$ErrorActionPreference = 'Stop'` that killed the whole script on its
first log line. It then looked like the watcher "just didn't fire" for a full day.

**Why:** the Monitor reported "timed out", but the spawned `tail.exe` **kept running** and kept the
handle open. Monitor timeout does not guarantee the child process died.

**How to apply:**
1. **Never Monitor a log a live local script appends to on Windows.** Poll the file with
   `Get-Content -Tail N` in a normal command instead, which opens and closes cleanly.
2. **Make logging non-fatal in every long-running script.** Wrap the append in try/catch with a
   short retry and swallow the failure. A lost log line must never end the run. Anything can hold
   that lock: a tail, an editor, a log viewer.
3. **Clean up spawned processes.** Check `Get-CimInstance Win32_Process | Where CommandLine -like`
   for orphaned `tail.exe`/`grep` after a Monitor ends, and kill them.
4. **When a background script "silently does nothing", get the real error** by running it in the
   foreground with `Start-Process -RedirectStandardError`, rather than theorising about the logic.
   That is what finally surfaced this in one shot after a day of wrong hypotheses.

Related: [[reference_granola_auto]], [[feedback_local_server_start_pattern]],
[[feedback_ps1_ascii_only_no_unicode_dashes]].
