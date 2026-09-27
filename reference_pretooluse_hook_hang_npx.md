---
name: reference_pretooluse_hook_hang_npx
description: Sessions freezing on "running PreToolUse hooks N/6" (2026-09-27). Real cause = Git Bash hook processes (bash, jq) that stall and keep the harness pipe open; fix = every hook runs through hooks/run-hook.js. The npx theory was only part of it.
metadata:
  type: reference
---

**Symptom (2026-09-27, twice the same day):** the session sits on `Actioning… (running PreToolUse hooks… 5/6 · 17m)`,
or stays frozen all night after the lid closes. Nothing is running: a hook has not returned.

**Cause, verified:** `~/.claude/hooks/post-compaction-recall.sh` was meant to run once per session. Its flag was keyed
on Claude's PID found with `ps -o ppid=`; Git Bash's `ps` has no `-o`, so the flag fell back to `$$` (new on every
call): 21,346 flag files in Temp, and the hook ran in full on EVERY tool call. `session-recall` is not installed as a
command, so each run fell through to `npx -y session-recall`, a network fetch. When the network stalls (resume from
sleep, flaky Wi-Fi) npx hangs; on Windows the hook timeout (5 s) kills bash but not the node child holding the pipe,
so the harness waits without limit.

**Fix (backup `post-compaction-recall.sh.bak-20260927`):** flag keyed on the `session_id` from stdin, no npx ever,
the one real call wrapped in `timeout 3`. Rule for any hook: a PreToolUse hook never touches the network and never
spawns a long-lived child.

**How to diagnose next time:** `python` over `~/.claude/settings.json` to list PreToolUse hooks in order with their
matcher and timeout (for a Bash call the six are: block-destructive, enforce-server-routing,
enforce-package-manager, scan-secrets-before-push, suggest-compact, post-compaction-recall); time each by hand with
`echo '{"session_id":"x"}' | bash hook.sh`; look for orphan node/npx with
`Get-CimInstance Win32_Process | ? CommandLine -match 'session-recall'`. Three hooks still have no timeout in
settings.json (enforce-package-manager, suggest-compact, protect-*): they are local and fast, not changed.

**CORRECTION, same day 16:50: the npx fix was NOT the root cause.** Twenty minutes after it another session froze on
5/6 again, and the process holding it was my rewritten hook itself: a `bash.exe post-compaction-recall.sh` alive for
3.5 minutes with no child and its parent gone. Seven orphaned `jq.exe -r ".tool_input.command // empty"` were alive
too, from 25, 26 and 27 Sept (three of them 01:50 to 02:21, the night the session froze). So: a Git Bash (msys)
process started by the harness can stall, or leave a jq behind reading a stdin that never closes; the `timeout` in
settings.json kills the shell that launched it but not the process that holds the pipe, and the harness waits.

**Real fix:** `~/.claude/hooks/run-hook.js` (native node). Every bash/jq hook in settings.json (PreToolUse,
PostToolUse, Stop: 13 of them) is now `node run-hook.js <seconds> <allow|block> <script>`. The wrapper owns the
pipes to the harness, gives the script its own, kills the script's whole tree with `taskkill /T /F` at the limit and
exits on its own clock. Guards (block-destructive, server routing, secrets, protect-*) REFUSE on timeout, the rest
allow. The two inline jq hooks were moved unchanged into `hooks/inline-*.sh`. Timeouts and slow runs are logged in
`hooks/hook-timeouts.log`: read it to learn which hook stalls. Backup: `settings.json.bak-20260927-hookwrap`.
Sessions load hooks at start: every open session keeps the old hooks until it is restarted.

**If a session is frozen right now:** stop the orphans, the session continues at once:
`Get-CimInstance Win32_Process | ? { ($_.Name -eq 'jq.exe' -and $_.CommandLine -match 'tool_input') -or ($_.Name -eq 'bash.exe' -and $_.CommandLine -match '\.claude.hooks') } | % { Stop-Process -Id $_.ProcessId -Force }`
