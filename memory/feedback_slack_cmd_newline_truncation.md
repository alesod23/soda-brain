---
name: feedback_slack_cmd_newline_truncation
description: "slack.cmd silently truncates a multi-line --text at the first newline AND swallows --confirmed, so a \"send\" comes back as a dry run"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bcf4ed36-d8ed-4e48-817b-146c5998e5ca
  modified: 2026-08-07T10:31:45.535Z
---

`slack.cmd send --workspace cdtm --to "@x" --text "$(cat body.txt)" --confirmed` **fails silently** when the body has newlines: cmd.exe cuts the value at the first `\n` and drops every flag after it, so `--confirmed` never registers and the call returns `"dry_run": true` with a one-line `text`. Hit 2026-08-07 sending a 14-line draft.

**Why:** the `.cmd` shim (`slack.cmd` → `python slack.py %*`) re-parses argv through cmd.exe. `slack.py` has no `--body-file`/stdin option, only `--text`.

**How to apply:** for any multi-line Slack body, drive `cmd_send` directly instead of the shim — load `slack.py` with `importlib.util.spec_from_file_location`, read the body from a UTF-8 file, and pass a `types.SimpleNamespace(workspace, to, text, thread_ts, confirmed)`. Working driver: `scratchpad/send_nik_draft.py`. Single-line sends through `slack.cmd` are fine.

**Always read the send back** (`slack.cmd read --channel <id> --limit 1`) and check the char/line count — a `"dry_run": true` response is easy to skim past as success. Same class of trap as [[feedback_ps51_convertfrom_json_no_unroll]]: the failure returns valid-looking JSON instead of throwing. See [[reference_slack_helper]], [[feedback_python_full_path]].
