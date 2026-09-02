---
name: reference_linkedin_poll
description: "LinkedIn DM poller lane (built 2026-09-02): ~/.claude/linkedin-poll polls get_inbox every 15 min on a CLONED profile, writes new incoming previews to the shared Drive store, the VPS sodanotif daemon tails it as the 4th source (blue dot cards). Paths, cadence knob, re-login procedure, Langfuse probe."
metadata: 
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-02T16:28:34.999Z
---

# LinkedIn poll lane (SODANOtif 4th source)

Read-only inbox watcher. `get_inbox` ONLY, never `get_conversation` (that marks a thread read), never sends.

## Pieces
- **Laptop poller** `C:\Users\Alessandro\.claude\linkedin-poll\`
  - `poll.py` (venv `linkedin-poll\venv`, pinned mcp 1.27.1 + langfuse 4.6.1): spawns `~/.linkedin-mcp/launcher.py --tool-timeout 600 --user-data-dir ~/.linkedin-mcp/profile-poll` (hand-rolled JSON-RPC over stdio, 120s call timeout), `get_inbox(25)`, parses text dump + `references.inbox`, diffs preview hashes against `state.json` (`{last_seen: {thread_id: hash}}`), appends NEW non-"You:" previews to the store, then **taskkill /T /F** the launcher tree (never a graceful close: that would re-export the shared `~/.linkedin-mcp/cookies.json`). Logs to `poll.log`; raw last inbox in `last-inbox.json`. `--seed` = record everything, emit nothing (first run / after a storm risk). Corrupt or missing state.json without `--seed` is FATAL by design (no notification storm).
  - `li_inbox.py` = shared engine (spawn / call / parse / store-line shape). `tracing.py` = Langfuse spans (copy of stripe-shopper pattern).
  - **Run lock** `linkedin-poll/.run.lock` (pid, stale-safe): poll and probe serialize on it (bounded 150s wait) because two launchers on the profile-poll class reap each other (launcher.py singleton guard). Found live: the task-land supervisor "repaired" the never-run task while probe.py was running. Running the optimizer loop alongside the 15-min task is safe because of this lock; `lock_wait` shows up in the probe timings.
  - **Cadence knob:** `POLL_INTERVAL_MIN = 15` at the top of `poll.py` AND the schtask trigger `LinkedIn-Poll` (wscript `poll-hidden.vbs`, `-Once` + `RepetitionInterval` 15 min, no elevation). Change both. Health: `task-land\_system\health-snapshot.ps1` `$TaskExpect['LinkedIn-Poll']=45`.
  - **Store** `G:\My Drive\DA\linkedin-store.jsonl` (== VPS `/home/da/gdrive/DA/linkedin-store.jsonl`, rclone ~10-30s). Line = WA-store-like object: `{id:"li:<thread>:<hash>", ts, iso, timestamp (detection unix s), source:"linkedin", chatId, chatName, sender, text, time_label, ts_precision, url, fromMe:false}`.
- **Daemon source** `sodanotif/sources/linkedin.js` (`startLinkedInSource`, same contract as wa.js: offset tail, start-gate on `timestamp`, dedupe by id, 5s poll is the real trigger on the FUSE mount). Wired in `daemon.js` next to WA: source key `LinkedIn`, blue dot `🔵`, no "(LinkedIn)" tag, thread url rendered as one `<a>open</a>` link and stored in notif-log/last-notification (`url` field). Day-only labels ("Sep 1") are passed as `when` verbatim instead of "Sep 1, 00:00". VPS unit has `Environment=SODANOTIF_LI_STORE=/home/da/gdrive/DA/linkedin-store.jsonl`. WA prompt verified byte-identical after the refactor. Unit test: `node sodanotif/test-linkedin-source.js`.
- **Langfuse:** poll = trace `linkedin-poll` (spans spawn/get_inbox/parse/diff/write); `probe.py` = trace `linkedin-probe` (spawn/get_inbox/parse, no state, no write) = TARGET for /langfuse-bananza, launch prompt at `~/.claude/loops/langfuse-optimizer/launch-linkedin.md`. Baseline 2026-09-02: spawn 4.3s, get_inbox 25.4s, total 30s.

## Profile clone (why + how to re-login)
The poller MUST NOT share `~/.linkedin-mcp/profile` with a live Claude session's server (Chromium lock + launcher.py reaps same-class launchers; the poller passes `--user-data-dir` so it is its own class). `clone-profile.ps1` robocopy-/MIR-mirrors profile -> `profile-poll` excluding lock files AND the Cookies DB (exclusively locked while a session is up), then `seed-cookies.py` (server venv) imports `~/.linkedin-mcp/cookies.json` into the clone and checks the feed loads. Refuses to run while a poller launcher is alive.

**Re-login procedure:** `C:\Users\Alessandro\.linkedin-mcp\venv\Scripts\python.exe -m linkedin_mcp_server --login` on the live profile (rewrites cookies.json), THEN `powershell -File C:\Users\Alessandro\.claude\linkedin-poll\clone-profile.ps1`. Symptom of a dead clone: `poll.log` shows `ERROR ... Stored runtime profile is invalid` / auth errors on every tick.

## Deploy to the VPS
Edit laptop `sodanotif/` (canonical) -> `scp -i ~/.ssh/da-vps_ed25519 <file> root@169.58.128.217:/home/da/sodanotif/...` -> `chown da:da` -> `systemctl restart da-sodanotif` -> `journalctl -u da-sodanotif -n 10`. Expect `sources=WhatsApp,LinkedIn (li store=...)` on the up-line and `LI in: <name>: ...` when a line lands.
