---
name: wa-daemon-flap-and-outgoing-gap
description: "WA daemon (Baileys linked device :46) does NOT reliably capture fromMe:true events for messages sent from the phone, especially during connectionReplaced flap storms. /triage must compensate with a flap-detection banner and per-DM thread-context display."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fe213d10-7556-4d4b-96b7-247e5b46edba
  modified: 2026-09-01T12:38:50.007Z
---

`repliedSinceLastIncoming` from `triage.js` is NOT trustworthy as a sole source of truth for "did Ale reply on WA?". Two compounding failures cause it to lie.

**Why:** confirmed 2026-05-16 — user replied to Alberto ("Si dai :)... E te?") at 20:26 Munich on 2026-05-15 from his phone. Daemon's `message-store.jsonl` has zero `fromMe:true` entries for Alberto's chatJid ever, so triage flagged the chat as still-actionable the next morning. Two root causes:

1. **Connection-replaced flap storm**: when another linked device (or a duplicate daemon process) takes the `:46` slot, the daemon disconnects and reconnects every few seconds. During flap windows, `messages.upsert` events for outgoing-from-phone messages don't propagate to the store. On 2026-05-16 we found PID 7032 and PID 12560 both running `daemon.js` (watchdog probably double-started); daemon.log showed 30+ `disconnected (code=440 connectionReplaced)` events in 10 minutes.
2. **Baileys multi-device sync gap**: even when stable, the linked device doesn't always receive `fromMe:true` for short messages or messages sent during brief disconnects. `lastOut` in `triage.js` then shows an older message and `repliedSinceLastIncoming` returns false. This is structural — Baileys does not guarantee 100% outgoing-msg propagation to linked devices.

**How to apply:** Two checks live in `~/.claude/commands/triage/SKILL.md` as of 2026-05-16:
- **Step 2 / WhatsApp pre-flight**: parse `daemon.log` tail for `disconnected` events. If ≥3 in last 5min OR any `connectionReplaced` in last 60min, print a banner before the actionable list warning that OUT msgs may be missing. Suggest investigating duplicate processes (NEVER auto-kill — CLAUDE.md hard rule).
- **Step 5 / snippet rules for WA DMs**: instead of just `lastIn` verbatim, display last 4 messages from `message-store.jsonl` (mixed `← incoming` / `→ outgoing`, oldest-first). Lets user eyeball whether OUT msgs the daemon DID capture are present. Zero-`→`-lines + flap banner = "verify in WhatsApp directly before marking done".

When daemon is fully healthy AND no flaps, `repliedSinceLastIncoming` is usually reliable. Use it as a hint, never as ground truth.

---

**ROOT CAUSE FOUND 2026-09-01 — why duplicates keep happening at all.** Three daemons were running (PIDs 28028 from 28 Aug, 44548 from 06:19, 5140 from 14:29), 29x `code=440 connectionReplaced` in 2 minutes of log, cycling every ~8s, store frozen.

`daemon.js:386` does `fs.writeFileSync(PID_PATH, String(process.pid))` **unconditionally on startup**. `start.ps1`, `stop.ps1` and `watchdog.ps1` all address the daemon ONLY through `daemon.pid`. So a second daemon silently overwrites the first one's entry and **orphans it permanently** — nothing on the machine knows the old PID any more. Every "kill and respawn" then ADDS an orphan instead of replacing one. That is the entire mechanism; it is not a Baileys problem.

**Why no alarm ever fires:** all daemons share one `heartbeat` file and whichever is momentarily connected keeps it fresh, and `daemon.pid` always names a live process. Both watchdog checks therefore pass. `watchdog.log` at 14:34:05 said `ok: pid=5140 hb_age_sec=4` while WA was totally deaf. **A fresh heartbeat does NOT mean WA is capturing** — that is the blind spot in [[reference_wa_daemon_health]].

**Diagnostic (do this FIRST, before creds/network theories):**
```powershell
Get-CimInstance Win32_Process -Filter "Name='node.exe'" | ? { $_.CommandLine -like '*wa-daemon\daemon.js*' } | Select ProcessId,CreationDate
```
More than one row = deaf, regardless of what heartbeat or `/health` say. Read `daemon.log` tail with a **shared FileStream** (`[IO.FileShare]::ReadWrite`); `Get-Content -Tail` timed out at 2 min against 3 daemons writing concurrently.

**Fixes applied and live-tested 2026-09-01:** `start.ps1` and `stop.ps1` now enumerate by command line instead of the pidfile (start refuses when any daemon.js is alive; stop kills them ALL and exits 1 if any survive). `watchdog.ps1` checks duplicates FIRST and logs `DUPLICATE DAEMONS`, with a `$ReconcileDuplicates` flag to auto-kill all but the newest.

Related: [[reference_wa_daemon_health]] (heartbeat-based daemon-up check, predates the flap rule; the flap rule sits alongside it as a third failure mode), [[reference_wa_sender]], [[feedback_windows_tail_locks_logfile]].
