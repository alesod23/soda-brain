---
name: feedback_pgrep_self_match_use_script_files
description: pgrep -f / pkill -f match the very shell that runs them; never wait on or kill by a pattern from inline bash - use script files, pidfiles and kill -0 <pid>
metadata:
  node_type: memory
  type: feedback
---

Bit three times on 2026-09-14, on the box, while managing background transcriptions:
1. `pgrep -c -f 'bun server.ts'` returned 2 and looked like a second Telegram poller; the second match was my own `bash -c` whose command line contained the string.
2. A `nohup bash -c 'while pgrep -f "voice-longform-vps.py|transcribe-vps.py"; do sleep 30; done; ...'` waited forever: the pattern lived in its own argv.
3. `pkill -f 'first21min'` killed the shell that was starting the job (exit 144), so the job never started.

**Rules:**
- Long or background jobs go in a **script file** (`run.sh` + `run.py`) started with `nohup <file> &`, and the pid is saved to a **pidfile**. Wait with `kill -0 $(cat pid)`, never with `pgrep -f <pattern>`.
- When a `pgrep -f` count matters, pipe to `grep -v $$` or check `/proc/<pid>/cmdline` of each hit before believing it.
- Never `pkill -f` a pattern that could appear in an inline command; kill the pidfile's pid.

Related: [[feedback_no_polling_on_background_tasks]], [[reference_phone_recordings_on_box]].
