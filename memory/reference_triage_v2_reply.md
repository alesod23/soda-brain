---
name: Triage v2 — Threaded Reply Pattern
description: For threaded replies in triage, use gmail.py draft + send-draft (NOT gmail.py send). Verified working across cdtm + lobbly on 2026-05-07.
type: reference
originSessionId: 4ea78cff-05f2-45ae-964c-63e0bf48d72c
---
For any threaded reply (the `reply: <text>` and `suggest` verbs in the triage skill, or any reply-into-existing-thread elsewhere), use the **two-step draft pattern**:

```
gmail.cmd draft --account <X> --thread-id <Y> --to <addr> --subject "Re: ..." --body "..."
# Output includes draft_id like r-12345...
gmail.cmd send-draft --account <X> --draft-id r-12345... --confirmed
```

## Why two steps (not just `send`)

The simpler `gmail.cmd send --thread-id ...` produces a plain text MIMEText with In-Reply-To, but Gmail's recipient-side threading heuristic doesn't reliably fire — the reply lands as a separate "Re: ..." email rather than threaded under the original. Verified failure on 2026-05-07 with multiple attempts.

The `draft` subcommand mirrors how the claude.ai Gmail MCP `create_draft` (replyToMessageId) builds replies: **multipart/alternative body** with a Gmail-style auto-quoted blockquote of the original, and **In-Reply-To/References** pointing to the latest non-self message in the thread (skipping prior SENT and DRAFT entries). That structure threads correctly on recipient's side.

## Permission hook on send-draft

The harness has a permission hook that blocks `send-draft` on a content-aware basis. A bare "go" or "ok" from the user is NOT enough — the user must reference the content (e.g. "send the draft", "yes send the reply about X"). Show the draft body before the send and ask the user to confirm explicitly.

## When to use which

- **Threaded reply (has --thread-id):** always `draft` + `send-draft`.
- **Fresh email (no parent thread):** the existing `gmail.cmd send` (dry-run + --confirmed) still works and is fine.
- **Just want to draft for later manual review in Gmail:** `gmail.cmd draft` and stop there. The user opens Gmail and sends.

## Multi-account

Both flows work on either account (`--account cdtm` or `--account lobbly`) because gmail.py uses per-account OAuth tokens stored in `~/triage/tokens/<account>.json`. No MCP swap needed. This is the architectural advantage of having our own custom OAuth app over relying on the single-account claude.ai Gmail MCP.
