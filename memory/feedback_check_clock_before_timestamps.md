---
name: check-clock-before-timestamps
description: "Run Get-Date before writing any time into a message, file name, checkpoint or card; never carry a time forward from earlier in the thread"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 6d6a4161-826b-4016-90da-5f2d7a0d8e7e
  modified: 2026-10-01T10:06:26.900Z
---

Before writing any clock time (in a message to him or to another session, a checkpoint file, a snapshot name, a hub card), run `Get-Date -Format "yyyy-MM-dd HH:mm zzz"` in that same turn. Never reuse a time read earlier in the conversation and never infer one from the thread ("submission night", "five minutes left").

**Why:** on the thesis night (30 Sept to 1 Oct 2026) I told the savior session he was "submitting right now (00:30)" when the laptop clock said 12:06 the next day; the checkpoint file was named 2345 while the clock said 23:10. The savior had shipped three false cards the day before from the same kind of arithmetic (see [[reference_box_utc_timestamps_mktime_trap]]).

**How to apply:** one Get-Date call per turn that writes a time; file names and checkpoint headers take the printed value, not a guessed one; when a peer session quotes a time that disagrees with mine, check the clock before answering.
