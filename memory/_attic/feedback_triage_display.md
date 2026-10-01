---
name: triage-display-rules
description: NON-NEGOTIABLE markdown table for every triage actionable list. Compact 6-column terminal-readable format with single-letter source codes. User has flagged display drift 5+ times — keep enforcing.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5613f4ee-d778-418d-907a-3cbdcd94e11d
---

**1. Always show the real sender.** Fetch `get_thread` for every actionable Gmail item BEFORE displaying — don't infer who sent what from the snippet body. Display the full `From:` header value (name + email) for Gmail items. For WA items, show the resolved contact name or group name from `triage.js`. For Slack, show the sender name (DM peer name, or "<sender> / #<channel>" for channel/mention items).

**Why:** snippets often start mid-body and look like outgoing emails when they're not. Inferred senders are wrong often enough to be useless.

**2. NO TABLES — multi-line block per item with emoji color codes.** Markdown pipe-tables collapse to label:value lists in this terminal; fenced code blocks lose color and can't be widened safely. So abandon tables entirely. Each item is a 3-line block with colored emoji circles to flag the source channel at a glance.

**Exact layout — 3-line block per item, separated by blank lines:**

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

Both Gmail accounts use red and both Slack workspaces use purple — that's per the user's spec (C/L = red, SC/SX = purple). The src letter still distinguishes within each color.

The **snippet text is bolded** (markdown `**...**`) — this is the visual-emphasis proxy for "yellow snippet" the user originally asked for. The Why line stays plain text so the snippet jumps out when scanning.

The `From` field carries everything other than src/time: contact name, group name, or `<sender> / #<channel>` for Slack channels. Use `(N)` count after the name if there are >4 messages from that chat (e.g., `Caleb (17)`).

Time format: `HH:MM` if today, `MM-DD HH:MM` if older.

Example skeleton:

```text
#   From                                Src  Time         Snippet                                                      Why
--- ----------------------------------- ---- ------------ ------------------------------------------------------------ ------------------------------------
1   Caleb (17)                          W    17:48        20 past. Getting socks before going home                     co-founder, day-long unanswered
```

If the terminal is narrower than ~155 chars, the row wraps visually but stays monospace and readable — better than the markdown-table failure mode.

**3. Source column — single/double letter codes ONLY.** No full words, no parentheses, no email addresses.

| Channel | Source code |
|---|---|
| WhatsApp | `W` |
| Gmail cdtm | `C` |
| Gmail lobbly | `L` |
| Slack cdtm (DM or channel or mention) | `SC` |
| Slack xplore (DM or channel or mention) | `SX` |

For Slack channel/mention items, put the channel name in the From column instead of the Source column (e.g., `From: David Meyer / #26-1_mpd`). For Slack DMs, the From column carries the peer name; no channel.

If an item is a TODO carryover, prefix the code with `TODO ` (e.g., `TODO C`, `TODO W`). NEW items get no prefix.

**4. Time column** sits right after Source. Format: `HH:MM` for items received today (local time). For older items, `MM-DD HH:MM`. Use the timestamp of the latest incoming message in the thread.

**5. Snippet column rules — NEVER truncate or summarize.**

- Default: show the **latest** incoming message text VERBATIM. Do not shorten, do not paraphrase, do not abbreviate words. The user explicitly flagged 2026-05-13 that summarizing snippets is a regression.
- **Multi-message burst exception:** if the same sender (or thread) sent a burst of 2+ consecutive short messages, include ALL of them VERBATIM in the snippet column, separated by ` / `. This is critical for WhatsApp / Slack where people send several short msgs instead of one long one.
- If there are MANY messages (>4) from the same chat AND they're not a tight burst, show only the LAST one VERBATIM and append a `(N)` count in the From column (e.g., `Caleb (17)`). For a true burst of 5-8 in tight time, still show them all.
- **Wrapping is fine, truncation is not.** If a snippet is longer than the column width, let it visually wrap to the next line in the user's terminal. Inside a fenced code block, terminal will wrap automatically — that's acceptable. NEVER replace text with `…` or paraphrase.
- Per the user 2026-05-13: "I want the same level of detail you had in your last version" — full text always.

**6. The `#` column always uses 1, 2, 3, 4, 5...** Plain integers. No emoji, no padding. The user references items by number in their batch reply.

**7. No prose paragraphs above the table.** Header line above the table is single line: `ACTIONABLE (N) — since <ISO timestamp>`. If 0 actionable: `Inbox clear ✓` and skip the table entirely.

**8. Skipped-silently summary AFTER the table** as a single short paragraph, not bulleted. Keep tight; doesn't need to enumerate every item.

**9. Drafts/sends summary tables** (when reporting completed sends or pending drafts) follow same table principle — never raw prose lists. Columns adapt to context but always include the index column.

**10. Never put account email in parentheses next to the From or Source.** The Source column carries the source identity via its single/double-letter code.

## Why these specific rules

User wants a wide terminal-readable table where each column is short enough that everything fits on one line per row. Long source strings like `Slack cdtm mention #channel` blow this up. Single-letter codes + channel-in-From keep rows compact. Time-before-Snippet matters because scanning urgency-by-time is the second-most-common cognitive step after reading the From.

## Concrete worked example

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

Notice: green circle for WhatsApp, purple for Slack, red for Gmail (both cdtm and lobbly use red). Snippet text is bolded to draw the eye. Full content always preserved, no truncation.
