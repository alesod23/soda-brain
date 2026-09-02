---
name: triage-operations
description: "Canonical operations manual for /triage and /snm — display format, workflow rules (drafts, silence=read, state.json cutoff), permanent skip rules, and the multi-line email body workaround. Consolidates feedback_triage_display, feedback_triage_workflow_v3, feedback_triage_group_me_skip, and feedback_gmail_cmd_shim_bug."
metadata: 
  node_type: memory
  type: reference
  originSessionId: c19162ff-56f0-4383-9e07-0dfdff7a81b1
---

This file is the canonical operating manual for triage. It absorbs four prior feedback memories. See also [[reference_triage_v2_reply]] (threaded reply pattern), [[reference_triage_aliases_and_state]] (file schemas), [[feedback_shared_inbox_cutoff]] (cross-tool cutoff), [[feedback_triage_v3_replies_and_skips]] if it re-appears.

---

## 1. Display format (NON-NEGOTIABLE)

User has flagged display drift 5+ times. These rules must hold every round.

**1.1 Always show the real sender.** Fetch `get_thread` for every actionable Gmail item BEFORE displaying — don't infer from snippet body. Display full `From:` header (name + email) for Gmail. For WA, the resolved contact/group name from `triage.js`. For Slack, sender name (DM peer name, or `<sender> / #<channel>` for channel/mention items).

Why: snippets often start mid-body and look like outgoing emails when they're not. Inferred senders are wrong often enough to be useless.

**1.2 NO TABLES — 3-line block per item with color emoji.**

Markdown pipe-tables collapse to label:value lists in this terminal; fenced code blocks lose color. So abandon tables entirely. Each item is a 3-line block:

```
#: N · <COLOR EMOJI> <SRC> · <FROM> · <TIME>
Snippet: **<full snippet text, bolded>**
Why: <short reason>
```

Color emoji mapping (markdown ANSI is stripped — emoji is the only color signal that survives):

| Source | Code | Emoji |
|---|---|---|
| WhatsApp | `W` | 🟢 |
| Gmail cdtm | `C` | 🔴 |
| Gmail lobbly | `L` | 🔴 |
| Slack cdtm | `SC` | 🟣 |
| Slack xplore | `SX` | 🟣 |

Both Gmail accounts use red, both Slack workspaces use purple — per user spec. The src letter distinguishes within each color.

Snippet is bolded via `**...**` — visual-emphasis proxy for the "yellow snippet" the user originally asked for. The Why line stays plain text so the snippet jumps out when scanning.

**1.3 From field carries everything other than src/time:** contact name, group name, or `<sender> / #<channel>` for Slack channels. Use `(N)` count after the name if >4 messages from that chat (e.g., `Caleb (17)`).

**1.4 Time format:** `HH:MM` if today, `MM-DD HH:MM` if older. Use timestamp of latest incoming message in the thread.

**1.5 Source codes — single/double letter ONLY.** No full words, no parentheses, no email addresses. For Slack channel/mention items, put channel name in From column (e.g., `From: David Meyer / #26-1_mpd`); Source stays `SC`/`SX`. For TODO carryover, prefix code with `TODO ` (e.g., `TODO C`, `TODO W`). NEW items get no prefix.

**1.6 Snippet — NEVER truncate or summarize.**

- Default: show LATEST incoming message text VERBATIM. No shortening, paraphrasing, abbreviating. User explicitly flagged 2026-05-13 that summarizing snippets is a regression.
- **Burst exception:** if same sender/thread sent 2+ consecutive short messages, include ALL of them VERBATIM in the snippet, separated by ` / `. Critical for WhatsApp / Slack where people send several short messages instead of one long one.
- If MANY messages (>4) from same chat AND not a tight burst, show only the LAST one VERBATIM and append `(N)` count in From column (e.g., `Caleb (17)`). For a true burst of 5–8 in tight time, still show them all.
- Wrapping is fine, truncation is not. Inside a fenced code block, terminal wraps automatically — acceptable. NEVER replace text with `…` or paraphrase.
- User verbatim 2026-05-13: "I want the same level of detail you had in your last version."

**1.7 Numbering:** plain integers (`1, 2, 3, ...`). No emoji, no padding. User references items by number in batch reply.

**1.8 No prose paragraphs above the table.** Single header line: `ACTIONABLE (N) — since <ISO timestamp>`. If 0 actionable: `Inbox clear ✓` and skip the table entirely.

**1.9 Skipped-silently summary AFTER the table** as one short paragraph, not bulleted. Tight; doesn't need to enumerate every item.

**1.10 Drafts/sends summary tables** (when reporting completed sends or pending drafts) follow same principle — never raw prose lists. Always include the index column.

**1.11 Never put account email in parentheses next to From or Source.** The Source column carries source identity via its letter code.

### Worked example

```
ACTIONABLE (3) — since 2026-05-13T15:52:24Z

#: 1 · 🟢 W · Caleb (17) · 17:48
Snippet: **20 past. Getting socks before going home**
Why: co-founder, day-long unanswered DMs

#: 2 · 🟣 SC · perrotc (6) · 05-12 17:34
Snippet: **Sure no problem :) / Looking forward to talk to you / It does not show a google meet link for me in the invite / Maybe it was filtered out / I just send you a teams link / The updated invite did not yet go through**
Why: meeting coordination, 6 unread msgs, NOT closure

#: 3 · 🔴 C · David M. Huber <david.m.huber@tum.de> · 09:14
Snippet: **Re: CDTM Lecture Visit — happy to slot you in next week, can you do Wednesday 14:00?**
Why: direct meeting-slot question
```

---

## 2. Workflow rules

### 2.1 Drafts always come paired with the original

When drafting an email reply, show in the same response:

1. **The full previous message** (sender + subject + body, untruncated). Pull from `gmail.cmd get --account <X> --thread-id <Y>` if not already in conversation context.
2. **The proposed draft** (recipient + subject + body) underneath it.

Reason: the user wants to verify the original is what they remember and that the draft actually addresses it. A draft alone has no anchor.

This applies any time the user asks for an email response — not just inside `/triage`. If they say "reply to X" or "draft a reply about Y," produce both halves.

### 2.2 Silence = read (cross-tool, /triage AND /snm)

After the triage skill displays its actionable list and the user provides a batch response, items the user did NOT mention are treated as **read** even if still UNREAD on the source side. Do NOT re-surface them in the next round.

**Strengthened 2026-05-14:** if the user takes time to give EXPLICIT instructions for SOME items (e.g., `1 reply: ...`, `2 answer ok`, detailed multi-step instructions), then everything else in that round is treated as **considered red / not worth keeping alive**. Signal: when the user invests effort selecting items to act on, the unselected are explicitly NOT worth a future round — drop them all.

User verbatim 2026-05-14: "If I take the time to exactly tell you what to do for certain items… then it means that nothing else is worth keeping alive for another triage session, because they're all red. This should be known between SnM, and Triage through shared memory."

**Applies BOTH ways across `/triage` and `/snm`:**

| User action | Effect |
|---|---|
| `/triage` round: user gives verbs for items 1, 2 | Items 3..N auto-marked done (per-channel state). SNM's `state.json#actionable` also cleared at round end (per `/triage` step 7d). |
| `/snm`: user says `1 done, 2 not urgent` (or detailed verbs) | Items 1+2 marked done in per-channel state. Other items in SNM's surfaced list also auto-marked done. |

**Implementation — at the end of every round, after applying explicit user verbs:**

- Gmail: for each unmentioned displayed item → apply `triage/done` + remove `UNREAD`.
- WA: for each unmentioned displayed item → append to `wa-state.json#done` with current `lastInTimestamp`.
- Slack: rely on shared cutoff (`~/triage/state.json#last_check_unix`) to exclude prior rounds' items in next fetch. (For items where the user explicitly wants something NOT to resurface even on new activity, would need a `slack-state.json` mirror — not built today; the cutoff handles typical patterns.)
- SNM state file: clear `state.json#actionable[]` at round end.

**Only carryover trigger phrases keep an item alive across rounds:** `todo`, `defer`, `keep for later`, `keep this for later`, `save for to-do`, `save this for my to-do`, `preserve`, or anything that semantically reads as "hold for next round". Anything else (including silence, `ok`, `done`, `read`, `reply: ...`, `suggest`) drops the item.

### 2.3 state.json cutoff is sacred

Every successful triage round MUST update `C:\Users\Alessandro\triage\state.json#last_triage_at` + `last_triage_unix`. The next round MUST fetch only items strictly after that timestamp:

- Gmail: `after:<last_triage_unix>` in every Query B.
- WA: `--hours ceil((now - last_triage_at) / 3600)` (rounded up).
- Slack: same `--hours` value.

**Plus** apply the local state filters:

- WA: every `chatId` present in `wa-state.json#done` whose `lastInTimestamp >= currentChat.lastIn.timestamp` MUST be dropped before display. (Equality counts — same-timestamp means processed last round.)
- WA cleanup: drop `done[chatId]` only when new incoming has a strictly newer timestamp AND is not a pure reaction/emoji.

User verbatim 2026-05-11: "you are saving in your memory when the triages requests are made. then you are only looking at unread messages FROM the last triage and so the ones in the previous triage will never show up again."

An item that already showed in a prior round must never appear again unless a NEW non-reaction message arrived after the cutoff. Missing this filter is the #1 way to re-surface noise — verify wa-state.json IS being checked before printing the table.

See [[feedback_shared_inbox_cutoff]] for the cross-tool cutoff governing /triage, /snm, SNM cron, and informal "what's new" checks — all advance the same timestamp.

---

## 3. Permanent skip rules

### 3.1 WhatsApp group "Me"

The WA group whose label is literally `Me` (jid `120363023505333085@g.us`) is **never actionable**. Skip silently in every triage round, regardless of content (announcements, task asks, links, anything).

**Why:** User confirmed 2026-05-11 that this group's content is never something to act on from triage.

**How to apply:** In the WA classification step of `/triage`, BEFORE any other LLM judgment: if `label === "group: Me "` OR jid `=== "120363023505333085@g.us"` → drop the item, do not display, do not count as actionable. No need to add to `wa-state.json#done` (it's a classifier skip, not state).

Treat the same way as `status@broadcast`, Renata image-only messages, etc — per-chat permanent skip rule. Other permanent skips can be added with the same pattern.

---

## 4. Multi-line email bodies — gmail.cmd shim bug

### 4.1 What broke (2026-05-10)

Three emails sent to TUM contacts (Anne Tryba, Holger Patzelt, Fritz Tacke) arrived with **only the first line** of the body. Root cause: cmd.exe `%*` expansion truncates multi-line `--body` args to first line when forwarded from `gmail.cmd` → `python.exe`.

`gmail.cmd` is a Windows batch shim:
```
@echo off
"C:\Users\Alessandro\AppData\Local\Programs\Python\Python312\python.exe" "%~dp0gmail.py" %*
```

When PowerShell calls `gmail.cmd ... --body $multiLineString`, PowerShell forwards the string with newlines as a single arg. cmd.exe's `%*` expansion **truncates at the first newline** when forwarding to python.exe. Python receives `--body "Dear Prof. Tryba,"` and silently sends only that.

Known cmd.exe limitation. No PowerShell-side quoting trick fixes it.

### 4.2 Two safe paths

**A. python.exe directly (bypass the .cmd shim) — DEFAULT for triage multi-line:**

```powershell
$body = @'
Multi-line
body here
'@
& "C:\Users\Alessandro\AppData\Local\Programs\Python\Python312\python.exe" `
  "C:\Users\Alessandro\triage\gmail.py" send `
  --account cdtm --to addr@x.com --subject "..." --body $body --thread-id ... --confirmed
```

PowerShell → python.exe passes args directly with newlines intact. No cmd.exe in the chain. Verified 2026-05-10 with Anne body and Fritz body (multi-paragraph), both arriving in full.

**B. `--body-file <path>` (works through any shell, including the .cmd shim):**

```powershell
$body = @'
Multi-line
body here
'@
$tmp = [System.IO.Path]::GetTempFileName()
[System.IO.File]::WriteAllText($tmp, $body, [System.Text.UTF8Encoding]::new($false))
gmail.cmd send --account cdtm --to addr@x.com --subject "..." --body-file $tmp --thread-id ... --confirmed
Remove-Item $tmp
```

`gmail.py` was patched 2026-05-10 to accept `--body-file <path>` on both `send` and `draft`. File path survives `%*` expansion. The .cmd shim is fine for everything else.

### 4.3 Default for /triage

**Use path A (python.exe direct)** for any multi-line body. Fewer steps, no temp file cleanup. Path B is fallback for callers that prefer the shim or have very long bodies pulled from a file anyway.

For single-line bodies (`wa <X> "ok"` style), `--body "single line"` via the shim is still fine — the bug only fires when newlines are in the value.

### 4.4 wa-daemon send immunity

`wa-daemon/send.js` is invoked as `node send.js ...` directly (no .cmd shim). PowerShell → node passes args correctly. WA sends are immune. Only Gmail's gmail.cmd was affected.
