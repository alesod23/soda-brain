---
name: reference_pretooluse_hook_hang_npx
description: Sessions freezing on "running PreToolUse hooks N/6" for minutes or hours (2026-09-27) came from post-compaction-recall.sh running `npx -y session-recall` on every tool call; fixed, with the diagnosis recipe.
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
